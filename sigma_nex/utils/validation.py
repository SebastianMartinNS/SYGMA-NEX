"""
SIGMA-NEX Input Validation and Security Utilities

Centralized input validation and security functions.
"""

import html
import re
from pathlib import Path
from typing import Any, Optional, Union


class ValidationError(ValueError):
    """Custom exception for validation errors."""


def sanitize_text_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize text input for safety.

    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized text

    Raises:
        ValidationError: If input is invalid
    """
    if text is None:
        return ""

    if not isinstance(text, str):
        raise ValidationError("Input must be a string")

    # Truncate if too long instead of raising error
    if len(text) > max_length:
        text = text[:max_length]

    # Remove script tags
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<script[^>]*>", "", text, flags=re.IGNORECASE)

    # Remove SQL injection patterns (case insensitive)
    text = re.sub(r";\s*drop\s+table[^;]*", "", text, flags=re.IGNORECASE)
    text = re.sub(r";\s*delete\s+from[^;]*", "", text, flags=re.IGNORECASE)
    text = re.sub(r";\s*update[^;]*set.*--", "", text, flags=re.IGNORECASE)

    # Remove template injection patterns
    text = re.sub(r"\{\{.*?\}\}", "", text)
    text = re.sub(r"\$\{.*?\}", "", text)

    # Remove path traversal
    text = re.sub(r"\.\./", "", text)

    # Remove potentially dangerous characters
    # Allow most Unicode characters but remove control characters
    sanitized = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

    # Decode HTML entities (don't escape back to prevent double-encoding)
    sanitized = html.unescape(sanitized)

    return sanitized.strip()


def validate_file_path(
    file_path: Union[str, Path],
    base_directory: Optional[Union[str, Path]] = None,
    allowed_extensions: Optional[list] = None,
) -> Path:
    """
    Validate and sanitize file paths to prevent path traversal attacks.

    Args:
        file_path: Path to validate
        base_directory: Base directory to restrict access to
        allowed_extensions: List of allowed file extensions

    Returns:
        Validated Path object

    Raises:
        ValidationError: If path is invalid or unsafe
    """
    if not file_path:
        raise ValidationError("File path cannot be empty")

    path = Path(file_path)

    # Check if it's a symbolic link BEFORE resolving (potential security risk)
    if path.is_symlink():
        raise ValidationError("Symbolic links are not allowed")

    # Now resolve the path
    path = path.resolve()

    # Check for path traversal attempts (only dangerous patterns)
    file_str = str(file_path)

    # Block directory traversal attempts
    if ".." in file_str and ("/" in file_str or "\\" in file_str):
        # Only block ".." when it's part of a path (not just in filename)
        if "/.." in file_str or "\\.." in file_str or file_str.startswith(".."):
            raise ValidationError("Path traversal detected")

    # Block suspicious absolute paths to system files
    suspicious_paths = [
        "/etc/",
        "/bin/",
        "/usr/bin/",
        "/var/",
        "/root/",
        "c:\\windows\\",
        "c:\\program files\\",
        "\\windows\\system32\\",
    ]
    file_lower = file_str.lower()
    for suspicious in suspicious_paths:
        if file_lower.startswith(suspicious.lower()):
            raise ValidationError("Path traversal detected")

    # Restrict to base directory if specified
    if base_directory:
        base_path = Path(base_directory).resolve()
        try:
            path.relative_to(base_path)
        except ValueError:
            raise ValidationError(f"Path outside allowed directory: {base_directory}")

    # Check if file exists
    if not path.exists():
        raise ValidationError("File does not exist")

    # Check if it's a file (not a directory)
    if not path.is_file():
        raise ValidationError("Path is not a file")

    # Check file extension
    if allowed_extensions:
        if path.suffix.lower() not in [ext.lower() for ext in allowed_extensions]:
            raise ValidationError(f"File extension not allowed. Allowed: {allowed_extensions}")

    return path


def validate_user_id(user_id: Any) -> int:
    """
    Validate user ID.

    Args:
        user_id: User ID to validate

    Returns:
        Validated user ID as integer

    Raises:
        ValidationError: If user ID is invalid
    """
    if user_id is None:
        raise ValidationError("User ID cannot be None")

    if isinstance(user_id, float):
        raise ValidationError("User ID cannot be a float")

    try:
        uid = int(user_id)
    except (ValueError, TypeError):
        raise ValidationError("User ID must be a valid integer")

    if uid < 0:
        raise ValidationError("User ID must be positive")
    if uid > 2**63 - 1:  # Max int64
        raise ValidationError("User ID too large")
    return uid


def validate_model_name(model_name: str) -> str:
    """
    Validate model name for Ollama.

    Args:
        model_name: Model name to validate

    Returns:
        Validated model name

    Raises:
        ValidationError: If model name is invalid
    """
    if not model_name or not isinstance(model_name, str):
        raise ValidationError("Model name must be a non-empty string")

    # Strip whitespace first
    model_name = model_name.strip()

    if not model_name:
        raise ValidationError("Model name cannot be empty after stripping")

    # Allow alphanumeric, hyphens, underscores, and colons (for tags)
    if not re.match(r"^[a-zA-Z0-9._:-]+$", model_name):
        raise ValidationError("Model name contains invalid characters")

    if len(model_name) > 100:
        raise ValidationError("Model name too long")

    return model_name


def validate_prompt(prompt: str) -> str:
    """
    Validate and sanitize prompt input.

    Args:
        prompt: Prompt to validate

    Returns:
        Validated prompt

    Raises:
        ValidationError: If prompt is invalid
    """
    if not isinstance(prompt, str):
        raise ValidationError("Prompt must be a string")

    if not prompt.strip():
        raise ValidationError("Prompt cannot be empty")

    # Check for extremely long prompts that might cause issues
    if len(prompt) > 50000:
        raise ValidationError("Prompt too long (max 50000 characters)")

    # Remove null bytes and other problematic characters
    sanitized = prompt.replace("\x00", "").strip()

    return sanitized


def is_safe_command(command: str) -> bool:
    """
    Check if a command is safe to execute.

    Args:
        command: Command to check

    Returns:
        True if command appears safe, False otherwise
    """
    if not isinstance(command, str):
        return False

    # List of dangerous commands/patterns
    dangerous_patterns = [
        r"\brm\b.*-rf",  # rm -rf
        r"\bformat\b",  # format command
        r"\bdel\b.*[/\\]",  # del with paths
        r">\s*/dev/",  # redirect to device files
        r"\bnc\b.*\|",  # netcat piping (corrected)
        r"\bcurl\b.*\|",  # curl piping
        r"\bwget\b.*\|",  # wget piping
        r";\s*rm\b",  # chained rm
        r"&&\s*rm\b",  # chained rm
        r"\bpowersh?ell\b.*-e",  # encoded powershell
        r"\bcmd\b.*\/c",  # cmd execution
    ]

    command_lower = command.lower()
    for pattern in dangerous_patterns:
        if re.search(pattern, command_lower):
            return False

    return True


def sanitize_log_data(data: Any) -> Any:
    """
    Sanitize data before logging to prevent injection and redact secrets.

    Args:
        data: Data to sanitize (dict, list, or other types)

    Returns:
        Sanitized data
    """
    if data is None:
        return None

    if isinstance(data, dict):
        sanitized = {}
        sensitive_fields = {
            "password",
            "api_key",
            "token",
            "secret",
            "key",
            "authorization",
        }

        for key, value in data.items():
            # Sanitize key
            safe_key = re.sub(r"[^\w_-]", "_", str(key))[:50]

            # Check if field is sensitive
            if any(sensitive in safe_key.lower() for sensitive in sensitive_fields):
                sanitized[safe_key] = "[REDACTED]"
            else:
                # Recursively sanitize nested structures
                sanitized[safe_key] = sanitize_log_data(value)

        return sanitized

    elif isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    elif isinstance(data, str):
        # Remove control characters and limit length
        safe_value = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", data)[:1000]
        return safe_value

    elif isinstance(data, (int, float, bool)):
        return data

    else:
        # Convert to string and truncate
        return str(data)[:500]
