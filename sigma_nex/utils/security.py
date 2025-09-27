import base64

# hashlib non più necessario - rimosso per evitare warning F401
import os
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(password: str, salt: Optional[bytes] = None) -> bytes:
    """
    Derive encryption key using secure PBKDF2 key derivation function.

    Args:
        password: Password string
        salt: Optional salt bytes. If None, generates new salt.

    Returns:
        Base64 encoded key suitable for Fernet
    """
    if salt is None:
        salt = os.urandom(16)  # 128-bit salt

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        iterations=100000,  # OWASP recommended minimum
    )
    key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(key)


def encrypt(data: bytes, password: str) -> bytes:
    """
    Encrypt data using Fernet symmetric encryption with secure KDF.

    Args:
        data: Data to encrypt
        password: Password for encryption

    Returns:
        Encrypted data with embedded salt
    """
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)
    encrypted = f.encrypt(data)
    # Prepend salt to encrypted data for decryption
    return salt + encrypted


def decrypt(token: bytes, password: str) -> bytes:
    """
    Decrypt data using Fernet symmetric encryption with secure KDF.

    Args:
        token: Encrypted data with embedded salt
        password: Password for decryption

    Returns:
        Decrypted data
    """
    # Extract salt from first 16 bytes
    salt = token[:16]
    encrypted_data = token[16:]

    key = derive_key(password, salt)
    f = Fernet(key)
    return f.decrypt(encrypted_data)
