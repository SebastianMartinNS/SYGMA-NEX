import pytest
from sigma_nex.utils.security import derive_key, encrypt, decrypt


def test_encrypt_decrypt_roundtrip():
    pw = "secret-password"
    data = b"hello world"
    token = encrypt(data, pw)
    assert token != data
    out = decrypt(token, pw)
    assert out == data


def test_derive_key_deterministic():
    assert derive_key("a") == derive_key("a")
    assert derive_key("a") != derive_key("b")


def test_decrypt_wrong_password_raises():
    pw1 = "pass1"
    pw2 = "pass2"
    token = encrypt(b"data", pw1)
    with pytest.raises(Exception):
        decrypt(token, pw2)
