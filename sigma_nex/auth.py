"""
SIGMA-NEX CLI Authentication System

Secure CLI authentication with session persistence for multi-process
environments. No hardcoded credentials - uses environment variables only.
"""

import hashlib
import json
import os
import secrets
import tempfile
import time
from typing import Dict, Optional, Tuple

from .utils.validation import sanitize_text_input

# Conditional import for file locking
try:
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False


class CLIAuthSession:
    """CLI authentication session manager with file persistence."""

    def __init__(self, session_timeout: int = 3600):
        self._failed_attempts: Dict[str, int] = {}
        self._lockout_times: Dict[str, float] = {}
        # Validazione range timeout per sicurezza (1 min - 8 ore)
        if session_timeout < 60:
            session_timeout = 60
        elif session_timeout > 28800:  # 8 ore max
            session_timeout = 28800
        self.session_timeout = session_timeout
        self.max_failed_attempts = 3
        self.lockout_duration = 300  # 5 minutes
        # Session storage per persistenza multi-processo
        self._session_file = os.path.join(tempfile.gettempdir(), ".sigma_nex_sessions")

    def _get_client_id(self) -> str:
        """Get a client identifier with additional entropy for security."""
        import socket

        hostname = socket.gethostname()
        user = os.getenv("USERNAME", os.getenv("USER", "unknown"))
        # Aggiungi entropy casuale per rendere meno prevedibile
        entropy = secrets.token_hex(8)
        return hashlib.sha256(f"{hostname}:{user}:{entropy}".encode()).hexdigest()[:16]

    def _is_locked_out(self, client_id: str) -> bool:
        """Check if client is locked out due to failed attempts."""
        if client_id not in self._lockout_times:
            return False

        if time.time() - self._lockout_times[client_id] > self.lockout_duration:
            self._lockout_times.pop(client_id, None)
            self._failed_attempts.pop(client_id, None)
            return False

        return True

    def _record_failed_attempt(self, client_id: str) -> None:
        """Record a failed login attempt."""
        self._failed_attempts[client_id] = self._failed_attempts.get(client_id, 0) + 1
        if self._failed_attempts[client_id] >= self.max_failed_attempts:
            self._lockout_times[client_id] = time.time()

    def _load_sessions(self) -> Dict[str, Dict]:
        """Load sessions from file."""
        try:
            if os.path.exists(self._session_file):
                with open(self._session_file, "r") as f:
                    sessions = json.load(f)
                    # Cleanup expired sessions
                    current_time = time.time()
                    valid_sessions = {}
                    for token, session_data in sessions.items():
                        if current_time - session_data["created_at"] <= self.session_timeout:
                            valid_sessions[token] = session_data
                    return valid_sessions
        except (json.JSONDecodeError, OSError):
            pass
        return {}

    def _log_security_event(self, event_type: str, details: Dict) -> None:
        """Log security events for audit purposes."""
        import logging

        logger = logging.getLogger(__name__)

        # Log eventi di sicurezza con livello WARNING
        logger.warning(f"SECURITY_EVENT: {event_type} - {details}")

        # Per eventi critici, salva anche su file separato
        if event_type in ["max_sessions_exceeded", "invalid_token_access"]:
            try:
                security_log = os.path.join(os.path.dirname(self._session_file), "security.log")
                with open(security_log, "a") as f:
                    import datetime

                    timestamp = datetime.datetime.now().isoformat()
                    f.write(f"{timestamp} - {event_type} - {details}\n")
            except OSError:
                pass  # Non fallire se non può scrivere il log di sicurezza

    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Authenticate user with username/password."""
        username = sanitize_text_input(username, max_length=50)
        client_id = self._get_client_id()

        if self._is_locked_out(client_id):
            return False, None, "Account temporarily locked due to failed attempts"

        # Rimossi hash hardcoded - ora usa solo environment variables
        # Credenziali DEV e ADMIN devono essere configurate via env var

        # Validazione credenziali - solo env vars, niente hardcoded
        if username == "user":
            # Utente pubblico disabilitato per sicurezza
            self._record_failed_attempt(client_id)
            return False, None, "Public user access disabled for security"
        elif username in ["dev", "admin"]:
            # Per dev/admin, richiede env var obbligatoria
            env_var_name = f"SIGMA_{username.upper()}_PASSWORD"
            required_password = os.getenv(env_var_name)

            if not required_password:
                self._record_failed_attempt(client_id)
                return (
                    False,
                    None,
                    f"Environment variable {env_var_name} not set. Configure secure password.",
                )

            # Validazione password diretta (per compatibilità con test)
            if password != required_password:
                self._record_failed_attempt(client_id)
                return False, None, "Invalid credentials"
        else:
            self._record_failed_attempt(client_id)
            return False, None, "Invalid username"

        # Imposta permessi basati su username
        if username == "user":
            permissions = {"query": True, "translate": False, "config": False, "admin": False}
        elif username == "dev":
            permissions = {"query": True, "translate": True, "config": True, "admin": False}
        elif username == "admin":
            permissions = {"query": True, "translate": True, "config": True, "admin": True}
        else:
            permissions = {"query": False, "translate": False, "config": False, "admin": False}

        # Carica sessioni esistenti per controllo concorrente
        sessions = self._load_sessions()
        current_time = time.time()

        # Limita sessioni concorrenti per utente (max 3)
        active_user_sessions = sum(
            1 for s in sessions.values() if (s.get("username") == username and current_time - s.get("last_activity", 0) <= self.session_timeout)
        )

        if active_user_sessions >= 3:
            self._log_security_event("max_sessions_exceeded", {"username": username})
            return False, None, "Maximum concurrent sessions exceeded"

        # Genera token sessione sicuro
        session_token = secrets.token_urlsafe(32)
        session_data = {
            "client_id": client_id,
            "created_at": time.time(),
            "last_activity": time.time(),
            "permissions": permissions,
            "username": username,
            "token_expiry": time.time() + 3600,  # 1 ora assoluta
        }

        # Salva sessione in modo atomico
        self._save_session_atomic(session_token, session_data)

        return True, session_token, None

    def validate_session(self, session_token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Validate session token and return permissions."""
        sessions = self._load_sessions()

        if not session_token or session_token not in sessions:
            # Log tentativo di accesso con token invalido
            token_preview = (session_token[:8] + "...") if session_token else "None"
            self._log_security_event("invalid_token_access", {"token": token_preview})
            return False, None, "Invalid session token"

        session_data = sessions[session_token]
        current_time = time.time()

        # Check absolute token expiry
        token_expiry = session_data.get("token_expiry", 0)
        if current_time > token_expiry:
            # Rimuovi sessione scaduta
            del sessions[session_token]
            self._save_sessions(sessions)
            self._log_security_event("token_expired", {"username": session_data.get("username")})
            return False, None, "Session token expired"

        # Check timeout
        last_activity = session_data.get("last_activity", session_data["created_at"])
        if current_time - last_activity > self.session_timeout:
            # Rimuovi sessione scaduta
            del sessions[session_token]
            self._save_sessions(sessions)
            self._log_security_event("session_timeout", {"username": session_data.get("username")})
            return False, None, "Session expired"

        # Aggiorna last_activity in modo atomico
        session_data["last_activity"] = current_time
        self._save_session_atomic(session_token, session_data)

        return True, session_data, None

    def has_permission(self, session_token: str, permission: str) -> bool:
        """Check if session has specific permission."""
        valid, session_data, _ = self.validate_session(session_token)
        if not valid or not session_data:
            return False
        permissions = session_data.get("permissions", {})
        return permissions.get(permission, False)

    def logout(self, session_token: str) -> bool:
        """Logout and invalidate session."""
        sessions = self._load_sessions()
        if session_token in sessions:
            username = sessions[session_token].get("username")
            del sessions[session_token]
            self._save_sessions(sessions)
            self._log_security_event("logout", {"username": username})
            return True
        return False

    def get_session_info(self, session_token: str) -> Optional[Dict]:
        """Get session information for given token."""
        sessions = self._load_sessions()
        return sessions.get(session_token)

    def get_active_sessions(self) -> int:
        """Get count of active sessions."""
        sessions = self._load_sessions()
        current_time = time.time()
        active_count = 0

        for session_data in sessions.values():
            last_activity = session_data.get("last_activity", session_data.get("created_at", 0))
            if current_time - last_activity <= self.session_timeout:
                active_count += 1

        return active_count

    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions."""
        sessions = self._load_sessions()
        current_time = time.time()
        expired_tokens = []

        for token, session_data in sessions.items():
            last_activity = session_data.get("last_activity", session_data.get("created_at", 0))
            if current_time - last_activity > self.session_timeout:
                expired_tokens.append(token)

        for token in expired_tokens:
            del sessions[token]

        if expired_tokens:
            self._save_sessions(sessions)

        return len(expired_tokens)

    def cleanup_all_sessions(self) -> None:
        """Remove all sessions (for testing)."""
        self._save_sessions({})

    def _save_sessions(self, sessions: Dict) -> None:
        """Save sessions to file."""
        try:
            os.makedirs(os.path.dirname(self._session_file), exist_ok=True)
            with open(self._session_file, "w") as f:
                json.dump(sessions, f)
        except OSError:
            pass  # Ignore file errors in favor of functionality

    def _save_session_atomic(self, session_token: str, session_data: Dict) -> None:
        """Save session atomically to prevent race conditions."""
        import platform

        if platform.system() == "Windows":
            # On Windows, use a simple file lock approach
            import msvcrt

            try:
                with open(self._session_file, "r+") as f:
                    # Try to lock the file
                    msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
                    try:
                        # Read current sessions
                        f.seek(0)
                        content = f.read()
                        if content.strip():
                            sessions = json.loads(content)
                        else:
                            sessions = {}

                        # Update session
                        sessions[session_token] = session_data

                        # Write back atomically
                        f.seek(0)
                        f.truncate()
                        json.dump(sessions, f)
                    finally:
                        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)  # Unlock
            except (OSError, json.JSONDecodeError):
                # Fallback to non-atomic save if locking fails
                sessions = self._load_sessions()
                sessions[session_token] = session_data
                self._save_sessions(sessions)
        else:
            # Unix-like systems
            if not HAS_FCNTL:
                # Fallback - no file locking
                sessions = self._load_sessions()
                sessions[session_token] = session_data
                self._save_sessions(sessions)
                return

            import fcntl  # type: ignore[import]

            try:
                with open(self._session_file, "r+") as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # type: ignore[attr-defined]
                    try:
                        # Read current sessions
                        f.seek(0)
                        content = f.read()
                        if content.strip():
                            sessions = json.loads(content)
                        else:
                            sessions = {}

                        # Update session
                        sessions[session_token] = session_data

                        # Write back atomically
                        f.seek(0)
                        f.truncate()
                        json.dump(sessions, f)
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)  # type: ignore[attr-defined]
            except (OSError, json.JSONDecodeError):
                # Fallback to non-atomic save if locking fails
                sessions = self._load_sessions()
                sessions[session_token] = session_data
                self._save_sessions(sessions)


# Global session manager instance
_auth_session = CLIAuthSession()


def get_auth_session() -> CLIAuthSession:
    """Get the global authentication session manager."""
    return _auth_session


def login_cli(username: str, password: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """CLI login function."""
    return get_auth_session().authenticate(username, password)


def validate_cli_session(session_token: str) -> bool:
    """Validate CLI session token."""
    valid, _, _ = get_auth_session().validate_session(session_token)
    return valid


def check_cli_permission(session_token: str, permission: str) -> bool:
    """Check CLI permission for session."""
    return get_auth_session().has_permission(session_token, permission)


def logout_cli(session_token: str) -> bool:
    """CLI logout function."""
    return get_auth_session().logout(session_token)
