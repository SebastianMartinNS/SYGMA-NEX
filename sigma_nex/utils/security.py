import hashlib
import base64
from cryptography.fernet import Fernet

def derive_key(password: str) -> bytes:
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt(data: bytes, password: str) -> bytes:
    f = Fernet(derive_key(password))
    return f.encrypt(data)

def decrypt(token: bytes, password: str) -> bytes:
    f = Fernet(derive_key(password))
    return f.decrypt(token)
