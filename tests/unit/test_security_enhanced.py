"""
Test per le nuove funzionalità di sicurezza implementate.
Test REALI senza mock pesanti - focus su sicurezza e autenticazione.
"""

import asyncio
import time
from unittest.mock import Mock, patch

import pytest
from cryptography.fernet import InvalidToken

from sigma_nex.server import AuthManager, RateLimiter, SigmaServer
from sigma_nex.utils.security import decrypt, derive_key, encrypt


class TestEnhancedSecurity:
    """Test per le nuove funzionalità di sicurezza KDF."""

    def test_pbkdf2_key_derivation_real(self):
        """Test derivazione chiave con PBKDF2 reale."""
        password = "test_password_123"

        # Test con salt diversi
        key1 = derive_key(password)
        key2 = derive_key(password)

        # Chiavi dovrebbero essere diverse per salt diversi
        assert key1 != key2
        assert len(key1) == 44  # Base64 encoded 32-byte key
        assert len(key2) == 44

    def test_pbkdf2_same_salt_consistency_real(self):
        """Test consistenza con stesso salt."""
        password = "consistent_password"
        salt = b"12345678abcdefgh"  # 16 bytes

        key1 = derive_key(password, salt)
        key2 = derive_key(password, salt)

        # Stesso salt = stessa chiave
        assert key1 == key2

    def test_enhanced_encrypt_decrypt_real(self):
        """Test crittografia con salt embedded."""
        data = b"Enhanced encryption test data"
        password = "enhanced_password"

        encrypted = encrypt(data, password)
        decrypted = decrypt(encrypted, password)

        # Dati originali recuperati correttamente
        assert decrypted == data

        # Encrypted data contiene salt (16 bytes) + encrypted data
        assert len(encrypted) > len(data) + 16

    def test_enhanced_encrypt_unique_each_time_real(self):
        """Test che ogni crittografia produce risultati diversi."""
        data = b"Same data, different encryption"
        password = "same_password"

        encrypted1 = encrypt(data, password)
        encrypted2 = encrypt(data, password)
        encrypted3 = encrypt(data, password)

        # Crittogrammi diversi ogni volta (salt diverso)
        assert encrypted1 != encrypted2 != encrypted3

        # Ma tutti decrittografabili agli stessi dati
        assert decrypt(encrypted1, password) == data
        assert decrypt(encrypted2, password) == data
        assert decrypt(encrypted3, password) == data

    def test_enhanced_decrypt_wrong_password_real(self):
        """Test decrittografia con password sbagliata."""
        data = b"Secret enhanced data"
        correct_password = "correct_password"
        wrong_password = "wrong_password"

        encrypted = encrypt(data, correct_password)

        # Password sbagliata deve fallire
        with pytest.raises(InvalidToken):
            decrypt(encrypted, wrong_password)

    def test_enhanced_security_edge_cases_real(self):
        """Test casi limite per enhanced security."""
        # Test con dati vuoti
        empty_data = b""
        password = "empty_test"
        encrypted = encrypt(empty_data, password)
        assert decrypt(encrypted, password) == empty_data

        # Test con dati lunghi
        long_data = b"x" * 10000
        encrypted_long = encrypt(long_data, password)
        assert decrypt(encrypted_long, password) == long_data

        # Test con password unicode
        unicode_password = "pässwörd_ñoñó_测试"
        unicode_data = "Dati con càratteri spëciali 中文".encode("utf-8")
        encrypted_unicode = encrypt(unicode_data, unicode_password)
        assert decrypt(encrypted_unicode, unicode_password) == unicode_data


class TestAuthManager:
    """Test per il gestore autenticazione API."""

    def test_auth_manager_creation_real(self):
        """Test creazione AuthManager."""
        # Con API keys personalizzate
        custom_keys = ["key1", "key2", "key3"]
        auth = AuthManager(custom_keys)

        assert auth.validate_key("key1")
        assert auth.validate_key("key2")
        assert not auth.validate_key("invalid_key")

    def test_auth_manager_default_keys_real(self):
        """Test AuthManager con chiavi default in ambiente test."""
        auth = AuthManager()  # In test env, dovrebbe usare chiave default

        # Chiave di test dovrebbe essere presente
        assert auth.validate_key("test_api_key_12345")
        assert not auth.validate_key("random-key")

    def test_auth_manager_key_management_real(self):
        """Test gestione chiavi dinamica."""
        auth = AuthManager([])

        # Inizialmente nessuna chiave
        assert not auth.validate_key("test-key")

        # Aggiungi chiave
        auth.add_key("test-key")
        assert auth.validate_key("test-key")

        # Rimuovi chiave
        auth.remove_key("test-key")
        assert not auth.validate_key("test-key")


class TestRateLimiter:
    """Test per il rate limiter in memoria."""

    def test_rate_limiter_creation_real(self):
        """Test creazione RateLimiter."""
        limiter = RateLimiter(max_requests=10, window_seconds=60)

        assert limiter.max_requests == 10
        assert limiter.window_seconds == 60

    def test_rate_limiter_allows_requests_real(self):
        """Test che il rate limiter permette richieste entro il limite."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        client_id = "test_client"

        # Prime 5 richieste dovrebbero essere permesse
        for i in range(5):
            assert limiter.is_allowed(client_id)

    def test_rate_limiter_blocks_excess_requests_real(self):
        """Test che il rate limiter blocca richieste in eccesso."""
        limiter = RateLimiter(max_requests=3, window_seconds=60)
        client_id = "test_client_block"

        # Prime 3 richieste permesse
        for i in range(3):
            assert limiter.is_allowed(client_id)

        # Quarta richiesta bloccata
        assert not limiter.is_allowed(client_id)

    def test_rate_limiter_window_expiry_real(self):
        """Test scadenza finestra temporale."""
        limiter = RateLimiter(max_requests=2, window_seconds=1)  # 1 secondo
        client_id = "test_client_expiry"

        # Prime 2 richieste permesse
        assert limiter.is_allowed(client_id)
        assert limiter.is_allowed(client_id)

        # Terza richiesta bloccata
        assert not limiter.is_allowed(client_id)

        # Aspetta scadenza finestra
        time.sleep(1.1)

        # Richiesta dovrebbe essere permessa dopo scadenza
        assert limiter.is_allowed(client_id)

    def test_rate_limiter_multiple_clients_real(self):
        """Test isolamento tra client diversi."""
        limiter = RateLimiter(max_requests=2, window_seconds=60)

        client1 = "client_1"
        client2 = "client_2"

        # Ogni client ha il suo limite indipendente
        assert limiter.is_allowed(client1)
        assert limiter.is_allowed(client1)
        assert not limiter.is_allowed(client1)  # Client1 bloccato

        # Client2 ancora disponibile
        assert limiter.is_allowed(client2)
        assert limiter.is_allowed(client2)
        assert not limiter.is_allowed(client2)  # Client2 bloccato


class TestServerSecurityIntegration:
    """Test integrazione sicurezza nel server."""

    def test_server_with_auth_enabled_real(self):
        """Test server con autenticazione abilitata."""
        config = {"model_name": "test_model", "auth_enabled": True, "api_keys": ["test-secure-key"], "debug": False}

        with patch("sigma_nex.server.load_config", return_value=config):
            server = SigmaServer()

            assert server.auth_manager is not None
            assert server.auth_manager.validate_key("test-secure-key")
            assert not server.auth_manager.validate_key("invalid-key")

    def test_server_with_auth_disabled_real(self):
        """Test server con autenticazione disabilitata."""
        config = {"model_name": "test_model", "auth_enabled": False, "debug": False}

        with patch("sigma_nex.server.load_config", return_value=config):
            server = SigmaServer()

            assert server.auth_manager is None

    def test_server_rate_limiter_configuration_real(self):
        """Test configurazione rate limiter nel server."""
        config = {"model_name": "test_model", "rate_limit_requests": 30, "rate_limit_window": 120, "debug": False}

        with patch("sigma_nex.server.load_config", return_value=config):
            server = SigmaServer()

            assert server.rate_limiter.max_requests == 30
            assert server.rate_limiter.window_seconds == 120

    def test_server_medical_enhancement_flag_real(self):
        """Test flag per disabilitare medical enhancement."""
        config_enabled = {"model_name": "test_model", "medical_enhancement_enabled": True, "debug": False}

        config_disabled = {"model_name": "test_model", "medical_enhancement_enabled": False, "debug": False}

        with patch("sigma_nex.server.load_config", return_value=config_enabled):
            server_enabled = SigmaServer()
            assert server_enabled.config.get("medical_enhancement_enabled", True)

        with patch("sigma_nex.server.load_config", return_value=config_disabled):
            server_disabled = SigmaServer()
            assert not server_disabled.config.get("medical_enhancement_enabled", True)


class TestAsyncLogQueue:
    """Test per il sistema di logging asincrono con queue."""

    def test_log_queue_initialization_real(self):
        """Test inizializzazione queue di logging."""
        config = {"model_name": "test_model", "debug": False}

        with patch("sigma_nex.server.load_config", return_value=config):
            server = SigmaServer()

            assert server.log_queue is not None
            assert server.log_queue.maxsize == 1000

    @pytest.mark.asyncio
    async def test_async_log_request_real(self):
        """Test logging asincrono reale."""
        config = {"model_name": "test_model", "debug": False}

        with patch("sigma_nex.server.load_config", return_value=config):
            server = SigmaServer()

            test_data = {
                "timestamp": "2025-01-01T12:00:00Z",
                "user_id": 123,
                "question": "test question",
                "status": "success",
            }

            # Test che logging asincrono non sollevi eccezioni
            await server._log_request(test_data)

            # Verifica che entry sia stata aggiunta alla queue
            assert not server.log_queue.empty()

    @pytest.mark.asyncio
    async def test_log_worker_processing_real(self):
        """Test worker di processing dei log."""
        config = {"model_name": "test_model", "debug": False}

        with patch("sigma_nex.server.load_config", return_value=config):
            server = SigmaServer()

            # Mock del file writing per evitare IO reale
            with patch.object(server, "_write_log_sync") as mock_write:
                # Aggiungi entry alla queue
                await server.log_queue.put('{"test": "log_entry"}')

                # Avvia worker brevemente
                worker_task = asyncio.create_task(server._log_worker())

                # Aspetta processing
                await asyncio.sleep(0.1)

                # Cancella worker
                worker_task.cancel()
                try:
                    await worker_task
                except asyncio.CancelledError:
                    pass

                # Verifica che entry sia stata processata
                mock_write.assert_called_once_with('{"test": "log_entry"}')
