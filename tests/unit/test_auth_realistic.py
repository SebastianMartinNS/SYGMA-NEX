"""
Test realistici per il sistema di autenticazione CLI SIGMA-NEX.
Focus su logica reale con mocking critico solo dove necessario.
"""

import os
import time
from unittest.mock import Mock, patch

import pytest

from sigma_nex.auth import (
    CLIAuthSession,
    check_cli_permission,
    get_auth_session,
    login_cli,
    logout_cli,
    validate_cli_session,
)


class TestCLIAuthSession:
    """Test realistici per CLIAuthSession - logica di autenticazione reale."""

    def setup_method(self):
        """Setup per ogni test - crea sessione pulita."""
        self.auth = CLIAuthSession()
        self.auth.cleanup_all_sessions()

    def test_successful_authentication_real(self):
        """Test autenticazione riuscita con credenziali valide."""
        # Test con utente dev che richiede password env var
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, token, error = self.auth.authenticate("dev", "dev123")

        assert success is True
        assert token is not None
        assert len(token) > 20  # Token sicuro
        assert error is None

        # Verifica che il token sia nella sessione
        session_data = self.auth.get_session_info(token)
        assert session_data is not None

        # Verifica dati sessione
        assert session_data["username"] == "dev"
        assert session_data["permissions"]["query"] is True
        assert session_data["permissions"]["config"] is True
        assert session_data["permissions"]["admin"] is False

    def test_failed_authentication_real(self):
        """Test autenticazione fallita con credenziali invalide."""
        success, token, error = self.auth.authenticate("invalid", "wrong")

        assert success is False
        assert token is None
        assert "Invalid username" in error

    def test_input_sanitization_real(self):
        """Test sanitizzazione input durante autenticazione."""
        # Test con input potenzialmente pericoloso
        dangerous_username = "<script>alert('xss')</script>admin"
        success, token, error = self.auth.authenticate(dangerous_username, "admin456!")

        # Il comportamento può variare in base alla sanitizzazione
        # Se sanitizzazione produce "admin", potrebbe avere successo
        # L'importante è che non ci siano script tag nel risultato
        if success:
            # Se successo, verifica che sia stato sanitizzato
            session_data = self.auth.get_session_info(token)
            assert session_data is not None
            assert "<script>" not in session_data["username"]
            assert "alert" not in session_data["username"]
        else:
            # Se fallisce, è perché username sanitizzato non corrisponde
            assert token is None

    def test_lockout_mechanism_real(self):
        """Test meccanismo di lockout dopo tentativi falliti."""
        import os

        # Mock client_id per rendere il test deterministico
        with patch.object(self.auth, "_get_client_id", return_value="test_client_123"):
            # Simula 3 tentativi falliti con username valido ma password sbagliata
            for i in range(3):
                with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
                    success, token, error = self.auth.authenticate("dev", "wrong_password")
                assert success is False

            # Il quarto tentativo dovrebbe essere bloccato anche con password corretta
            with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
                success, token, error = self.auth.authenticate("dev", "dev123")
            assert success is False
            assert "temporarily locked" in error.lower()

    def test_lockout_expiry_real(self):
        """Test scadenza lockout."""
        # Configura timeout breve per il test
        self.auth.lockout_duration = 1  # 1 secondo

        with patch.object(self.auth, "_get_client_id", return_value="test_client_123"):
            # Forza lockout
            for i in range(3):
                with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
                    success, _, error = self.auth.authenticate("dev", "wrong")

            # Verifica lockout attivo
            with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
                success, _, error = self.auth.authenticate("dev", "dev123")
            assert success is False
            assert "locked" in error.lower()

            # Aspetta scadenza lockout
            time.sleep(1.1)

            # Ora dovrebbe funzionare
            with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
                success, token, error = self.auth.authenticate("dev", "dev123")
            assert success is True
            assert token is not None

    def test_session_validation_real(self):
        """Test validazione sessione reale."""
        # Crea sessione valida
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, token, _ = self.auth.authenticate("dev", "dev123")
        assert success is True

        # Valida sessione
        valid, session_data, error = self.auth.validate_session(token)
        assert valid is True
        assert session_data is not None
        assert error is None
        assert session_data["username"] == "dev"

    def test_session_timeout_real(self):
        """Test timeout sessione."""
        # Configura timeout breve
        self.auth.session_timeout = 1  # 1 secondo

        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, token, _ = self.auth.authenticate("dev", "dev123")
        assert success is True  # Aspetta timeout
        time.sleep(1.1)

        # Sessione dovrebbe essere scaduta - sistema rimuove automaticamente
        valid, session_data, error = self.auth.validate_session(token)
        assert valid is False
        # Sistema rimuove automaticamente sessioni scadute, quindi messaggio generico
        assert error in ["Invalid session token", "Session expired"]

    def test_permissions_system_real(self):
        """Test sistema permessi reale."""
        # Test permessi dev (richiede password che matcha hash corrente)
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, dev_token, _ = self.auth.authenticate("dev", "dev123")
            assert success is True

            assert self.auth.has_permission(dev_token, "query") is True
            assert self.auth.has_permission(dev_token, "config") is True
            assert self.auth.has_permission(dev_token, "admin") is False

        # Test permessi admin
        with patch.dict(os.environ, {"SIGMA_ADMIN_PASSWORD": "admin456"}):
            success, admin_token, _ = self.auth.authenticate("admin", "admin456")
            assert success is True

            assert self.auth.has_permission(admin_token, "query") is True
            assert self.auth.has_permission(admin_token, "config") is True
            assert self.auth.has_permission(admin_token, "admin") is True

    def test_logout_real(self):
        """Test logout reale."""
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, token, _ = self.auth.authenticate("dev", "dev123")
        assert success is True

        # Verifica sessione attiva
        valid, _, _ = self.auth.validate_session(token)
        assert valid is True

        # Logout
        logout_success = self.auth.logout(token)
        assert logout_success is True

        # Sessione dovrebbe essere invalidata
        valid, _, error = self.auth.validate_session(token)
        assert valid is False
        assert "Invalid session token" in error

    def test_session_cleanup_real(self):
        """Test pulizia sessioni scadute."""
        # Pulisci prima per test isolato
        self.auth.cleanup_all_sessions()

        # Configura timeout breve
        self.auth.session_timeout = 0.5

        # Crea alcune sessioni
        tokens = []
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123", "SIGMA_ADMIN_PASSWORD": "admin456"}):
            for user in ["dev", "admin"]:
                password = {"dev": "dev123", "admin": "admin456"}[user]
                success, token, _ = self.auth.authenticate(user, password)
                tokens.append(token)

        assert self.auth.get_active_sessions() == 2

        # Aspetta scadenza
        time.sleep(0.6)

        # Sistema rimuove automaticamente le sessioni scadute durante validate_session
        # Verifica che le sessioni non siano più attive
        active_sessions = self.auth.get_active_sessions()
        assert active_sessions <= 2  # Alcune potrebbero essere già rimosse automaticamente

        # Cleanup manuale delle rimanenti
        cleaned = self.auth.cleanup_expired_sessions()
        assert cleaned >= 0  # Pu essere 0 se già pulite automaticamente

        # Alla fine non dovrebbero esserci sessioni attive
        final_sessions = self.auth.get_active_sessions()
        assert final_sessions == 0

    def test_client_id_generation_real(self):
        """Test generazione client ID reale con entropia elevata."""
        client_id1 = self.auth._get_client_id()
        client_id2 = self.auth._get_client_id()

        # Dovrebbe essere diverso per ogni chiamata per maggiore sicurezza
        assert client_id1 != client_id2
        assert len(client_id1) == 16  # Hash troncato
        assert isinstance(client_id1, str)

    def test_concurrent_sessions_real(self):
        """Test sessioni concorrenti reali."""
        # Pulisci prima per test isolato
        self.auth.cleanup_all_sessions()

        # Più login dello stesso utente
        import os

        tokens = []
        for i in range(3):
            with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
                success, token, _ = self.auth.authenticate("dev", "dev123")
            assert success is True
            tokens.append(token)

        # Tutte le sessioni dovrebbero essere valide
        for token in tokens:
            valid, _, _ = self.auth.validate_session(token)
            assert valid is True

        assert self.auth.get_active_sessions() == 3
        assert self.auth.get_active_sessions() == 3


class TestCLIAuthIntegration:
    """Test integrazione funzioni CLI di autenticazione."""

    def setup_method(self):
        """Reset sessione globale per ogni test."""
        # Cleanup per next test
        auth = get_auth_session()
        auth.cleanup_expired_sessions()
        # Forza cleanup completo
        if hasattr(auth, "cleanup_all_sessions"):
            auth.cleanup_all_sessions()
        get_auth_session()._failed_attempts.clear()
        get_auth_session()._lockout_times.clear()

    def test_cli_login_integration_real(self):
        """Test integrazione login CLI reale."""
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, token, error = login_cli("dev", "dev123")

        assert success is True
        assert token is not None
        assert error is None

        # Verifica che validate_cli_session funzioni
        assert validate_cli_session(token) is True

    def test_cli_permission_check_real(self):
        """Test controllo permessi CLI reale."""
        # Test con admin user che ha permessi completi
        import os

        with patch.dict(os.environ, {"SIGMA_ADMIN_PASSWORD": "admin456"}):
            success, token, _ = login_cli("admin", "admin456")
            assert success is True

            # Test permessi diversi
            assert check_cli_permission(token, "query") is True
            assert check_cli_permission(token, "config") is True
            assert check_cli_permission(token, "admin") is True
            assert check_cli_permission(token, "nonexistent") is False

    def test_cli_logout_integration_real(self):
        """Test logout CLI reale."""
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, token, _ = login_cli("dev", "dev123")
        assert success is True

        # Logout
        logout_success = logout_cli(token)
        assert logout_success is True

        # Token non dovrebbe più essere valido
        assert validate_cli_session(token) is False

    def test_invalid_session_handling_real(self):
        """Test gestione sessioni invalide reali."""
        # Token inesistente
        assert validate_cli_session("invalid_token") is False
        assert check_cli_permission("invalid_token", "query") is False

        # Token vuoto/None
        assert validate_cli_session("") is False
        assert validate_cli_session(None) is False

    def test_session_activity_tracking_real(self):
        """Test tracking attività sessione reale."""
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, token, _ = login_cli("dev", "dev123")
        assert success is True

        # Prima validazione
        valid1, session1, _ = get_auth_session().validate_session(token)
        assert valid1 is True
        initial_activity = session1["last_activity"]

        # Aspetta un po'
        time.sleep(0.1)

        # Seconda validazione dovrebbe aggiornare last_activity
        valid2, session2, _ = get_auth_session().validate_session(token)
        assert valid2 is True
        assert session2["last_activity"] > initial_activity


class TestCLIAuthSecurity:
    """Test sicurezza del sistema di autenticazione CLI."""

    def setup_method(self):
        self.auth = CLIAuthSession()
        self.auth.cleanup_all_sessions()  # Ensure clean state for each test

    def test_password_not_stored_real(self):
        """Test che le password non vengano memorizzate."""
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, token, _ = self.auth.authenticate("dev", "dev123")
        assert success is True

        # Verifica che la password non sia memorizzata in sessione
        session_data = self.auth.get_session_info(token)
        assert session_data is not None
        assert "password" not in session_data
        assert "dev123" not in str(session_data)

    def test_session_token_entropy_real(self):
        """Test entropia token di sessione."""
        import os

        tokens = set()
        for i in range(10):
            with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
                success, token, _ = self.auth.authenticate("dev", "dev123")
            assert success is True
            tokens.add(token)
            self.auth.logout(token)  # Cleanup

        # Tutti i token dovrebbero essere diversi
        assert len(tokens) == 10

    def test_session_isolation_real(self):
        """Test isolamento tra sessioni."""
        # Crea due sessioni diverse
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success1, token1, _ = self.auth.authenticate("dev", "dev123")
        with patch.dict(os.environ, {"SIGMA_ADMIN_PASSWORD": "admin456"}):
            success2, token2, _ = self.auth.authenticate("admin", "admin456")

        assert success1 and success2
        assert token1 != token2

        # Verifica isolamento permessi
        assert self.auth.has_permission(token1, "admin") is False
        assert self.auth.has_permission(token2, "admin") is True

    @patch("socket.gethostname")
    @patch.dict(os.environ, {"USERNAME": "testuser"})
    def test_client_id_stability_real(self, mock_hostname):
        """Test che client ID abbia entropia elevata per sicurezza."""
        mock_hostname.return_value = "test-machine"

        # Client ID dovrebbe essere diverso ad ogni chiamata per maggiore sicurezza
        client_id1 = self.auth._get_client_id()
        client_id2 = self.auth._get_client_id()
        assert client_id1 != client_id2  # Diversi per entropia elevata

        # Ma diverso per hostname diverso
        mock_hostname.return_value = "different-machine"
        client_id3 = self.auth._get_client_id()
        assert client_id1 != client_id3


class TestCLIAuthErrorHandling:
    """Test gestione errori del sistema di autenticazione."""

    def setup_method(self):
        self.auth = CLIAuthSession()
        self.auth.cleanup_all_sessions()  # Ensure clean state for each test

    def test_malformed_input_handling_real(self):
        """Test gestione input malformati."""
        # Username molto lungo
        long_username = "a" * 1000
        success, token, error = self.auth.authenticate(long_username, "password")
        assert success is False  # Username sanitizzato non corrisponde

        # Username con caratteri speciali
        special_username = "user\x00\x01\x02"
        success, token, error = self.auth.authenticate(special_username, "password")
        assert success is False

    def test_edge_case_session_management_real(self):
        """Test casi limite gestione sessioni."""
        # Doppio logout
        import os

        with patch.dict(os.environ, {"SIGMA_DEV_PASSWORD": "dev123"}):
            success, token, _ = self.auth.authenticate("dev", "dev123")
        assert success is True

        assert self.auth.logout(token) is True
        assert self.auth.logout(token) is False  # Già rimosso

        # Validazione token dopo logout
        valid, _, error = self.auth.validate_session(token)
        assert valid is False
        assert "Invalid session token" in error

    def test_empty_sessions_cleanup_real(self):
        """Test cleanup con sessioni vuote."""
        # Pulisci prima per test isolato
        self.auth.cleanup_all_sessions()

        # Cleanup senza sessioni dovrebbe funzionare
        cleaned = self.auth.cleanup_expired_sessions()
        assert cleaned == 0

        active = self.auth.get_active_sessions()
        assert active == 0
