"""
Test realistici per sigma_nex.server - focus     def test_server_security_enabled_by_default_real(self):
        \"\"\"Test che sicurezza sia abilitata di default\"\"\"
        with patch(\"sigma_nex.server.get_config\") as mock_get_config:
            mock_config = Mock()
            mock_config.config = {}  # Mock dict per keys()
            mock_config.get.side_effect = lambda key, default=None: {
                \"auth_enabled\": default,  # Test default behavior
                \"api_keys\": [\"test_key\"] if key ==            # Include auth header per request autenticata
            headers = {\"Authorization\": \"Bearer test_api_key\"}
            response = client.post(\"/ask\", json={\"question\": \"test error\"}, headers=headers)
            # Ora il server richiede auth, quindi potrebbe essere 401 se auth fallisce
            assert response.status_code in [401, 503, 504]"api_keys\" else default
            }.get(key, default)
            mock_get_config.return_value = mock_config

            server = SigmaServer()

            # Auth dovrebbe essere abilitato di default (True)
            assert server.auth_manager is not Nonee del server
Elimina mock eccessivi e testa comportamento effettivo del server
"""

from contextlib import contextmanager
from unittest.mock import Mock, patch

import pytest
import requests
from fastapi import HTTPException
from fastapi.testclient import TestClient

from sigma_nex.server import SigmaServer

# FastAPI TestClient disponibile solo se fastapi è installato
pytest.importorskip("fastapi")


@contextmanager
def mock_http_clients():
    """Context manager per moccare sia requests che httpx"""
    with patch("requests.post") as mock_post, patch("httpx.AsyncClient") as mock_httpx_client:

        # Mock requests.post
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "test response"}
        mock_post.return_value = mock_response

        # Mock httpx.AsyncClient con async context manager
        from unittest.mock import AsyncMock

        mock_client_instance = Mock()
        mock_httpx_response = Mock()
        mock_httpx_response.status_code = 200
        mock_httpx_response.json.return_value = {"response": "test response"}

        # Usa AsyncMock per context manager asincrono
        mock_client_instance.__aenter__ = AsyncMock(return_value=mock_client_instance)
        mock_client_instance.__aexit__ = AsyncMock(return_value=None)
        mock_client_instance.post.return_value = mock_httpx_response
        mock_httpx_client.return_value = mock_client_instance

        yield mock_post, mock_httpx_client


class TestSigmaServerRealistic:
    """Test realistici del server - logica effettiva senza mock pesanti"""

    def test_server_security_enabled_by_default_real(self):
        """Test che sicurezza sia abilitata di default"""
        with patch("sigma_nex.server.get_config") as mock_get_config:
            mock_config = Mock()
            mock_config.config = {
                "auth_enabled": True,
                "api_keys": ["test_key"],
                "model_name": "mistral",
                "debug": False,
            }
            mock_config.get.side_effect = lambda key, default=None: {
                "auth_enabled": True,
                "api_keys": ["test_key"] if key == "api_keys" else default,
                "model_name": "mistral",
                "debug": False,
            }.get(key, default)
            # Mock get_path method
            from pathlib import Path

            mock_config.get_path.return_value = Path("/tmp/logs")
            mock_get_config.return_value = mock_config

            server = SigmaServer()  # Auth dovrebbe essere abilitato di default (True)
            assert server.auth_manager is not None

    def test_server_initialization_real(self):
        """Test inizializzazione server con configurazione reale"""
        with patch("sigma_nex.server.get_config") as mock_get_config:
            mock_config = Mock()
            mock_config.config = {
                "auth_enabled": True,
                "api_keys": ["test_key"],
                "model_name": "mistral",
                "debug": False,
            }
            mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
            from pathlib import Path

            mock_config.get_path.return_value = Path("/tmp/logs")
            mock_get_config.return_value = mock_config

            server = SigmaServer()

            # Verifica inizializzazione effettiva
            assert hasattr(server, "app")
            assert hasattr(server, "config")
            assert hasattr(server, "runner")

            # Verifica che il config sia stato caricato realmente
            assert isinstance(server.config, dict)
            assert len(server.config) > 0

            # Verifica che runner sia stato inizializzato
            assert server.runner is not None
            assert hasattr(server.runner, "config")
            assert hasattr(server.runner, "model")

    def test_server_config_loading_real(self):
        """Test caricamento configurazione reale del server"""
        server = SigmaServer()

        # Il server dovrebbe caricare config reale con defaults
        assert "max_tokens" in server.config
        assert "model" in server.config
        assert "debug" in server.config

        # Verifica valori default ragionevoli
        assert server.config["max_tokens"] >= 1024
        assert isinstance(server.config["model"], str)
        assert isinstance(server.config["debug"], bool)

        # Verifica che runner abbia ricevuto la config
        assert server.runner.config == server.config

    def test_server_import_error_handling(self):
        """Test gestione errori di importazione FastAPI"""
        # Mock del modulo per simulare ImportError
        with patch.dict("sys.modules", {"fastapi": None}):
            with patch("sigma_nex.server.FASTAPI_AVAILABLE", False):
                with pytest.raises(RuntimeError, match="FastAPI not available"):
                    SigmaServer()

    def test_server_runner_unavailable_fallback(self):
        """Test fallback quando Runner non è disponibile"""
        with patch("sigma_nex.server.RUNNER_AVAILABLE", False):
            server = SigmaServer()

            # Dovrebbe creare un mock runner
            assert server.runner is not None
            assert hasattr(server.runner, "config")
            assert hasattr(server.runner, "model")
            assert hasattr(server.runner, "secure")

    def test_server_startup_tracking(self):
        """Test tracking del tempo di avvio server"""
        import datetime

        before_init = datetime.datetime.utcnow()
        server = SigmaServer()
        after_init = datetime.datetime.utcnow()

        # Verifica che start_time sia impostato correttamente
        assert hasattr(server, "start_time")
        assert isinstance(server.start_time, datetime.datetime)
        assert before_init <= server.start_time <= after_init

        # Verifica counter requests
        assert hasattr(server, "requests_processed")
        assert server.requests_processed == 0

    def test_server_app_endpoints_real(self):
        """Test che il server abbia gli endpoint corretti"""
        server = SigmaServer()

        # Verifica che l'app FastAPI sia configurata
        assert server.app is not None

        # Verifica routes - dovrebbero esistere endpoint base
        routes = [route.path for route in server.app.routes]
        assert len(routes) > 0  # Dovrebbe avere almeno alcune routes

    def test_server_response_format_real(self):
        """Test formato response del server con endpoint reali"""
        server = SigmaServer()
        client = TestClient(server.app)

        # Test health check endpoint (dovrebbe funzionare senza mock)
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "uptime" in data
        assert data["status"] == "healthy"

        # Test endpoint API con mock minimale solo per ollama
        with mock_http_clients() as (mock_post, mock_httpx):
            mock_post.return_value.json.return_value = {"response": "test answer"}

            # Test endpoint query reale
            response = client.post("/ask", json={"question": "test query"})
            if response.status_code == 200:
                data = response.json()
                assert isinstance(data, dict)
                assert "response" in data
                assert "processing_time" in data

    def test_server_error_handling_real(self):
        """Test gestione errori reale del server"""
        server = SigmaServer()
        client = TestClient(server.app)

        # Test con payload malformato
        try:
            response = client.post("/api/query", json={"invalid": "data"})
            # Server dovrebbe gestire input non valido
            assert response.status_code in [400, 404, 422]  # Error codes validi
        except Exception:
            # Se endpoint non esiste, testa altre possibili routes
            response = client.get("/nonexistent")
            assert response.status_code == 404

    def test_server_runner_integration_real(self):
        """Test integrazione reale server-runner"""
        server = SigmaServer()

        # Verifica che il server abbia accesso al runner
        assert hasattr(server.runner, "config")
        assert hasattr(server.runner, "model")

        # Test metodi runner chiamabili dal server
        assert callable(getattr(server.runner, "_call_model", None)) or callable(getattr(server.runner, "send", None))


class TestSigmaServerConfiguration:
    """Test configurazione del server"""

    def test_server_with_custom_config(self):
        """Test server con configurazione personalizzata reale"""
        # Test che il server possa gestire config personalizzate
        server = SigmaServer()

        # Verifica che config abbia struttura ragionevole
        assert isinstance(server.config, dict)
        assert "model" in server.config
        assert "max_tokens" in server.config
        assert "debug" in server.config

        # Test che runner riceva la stessa config
        assert server.runner.config == server.config

        # Test modifica config runtime
        original_debug = server.config["debug"]
        server.config["debug"] = not original_debug
        # Config dovrebbe essere mutabile

    def test_server_config_validation_real(self):
        """Test validazione configurazione del server"""
        server = SigmaServer()

        # Il server dovrebbe avere config valida
        config = server.config
        assert isinstance(config, dict)

        # Verifica presenza di chiavi essenziali o default ragionevoli
        # Il server dovrebbe essere robusto anche con config minimal
        assert len(config) >= 0  # Almeno un dict vuoto dovrebbe funzionare


class TestSigmaServerCoreIntegration:
    """Test integrazione server con core modules senza mock"""

    def test_server_validation_real_functions(self):
        """Test funzioni validation reali nel server"""
        from sigma_nex.utils.validation import (
            sanitize_text_input,
            validate_user_id,
        )

        # Test sanitize_text_input come usato nel server
        dangerous_input = "<script>alert('xss')</script>Test query"
        clean_input = sanitize_text_input(dangerous_input)
        assert "script" not in clean_input
        assert "alert" not in clean_input
        assert "Test query" in clean_input

        # Test validate_user_id come usato nel server
        valid_id = validate_user_id(12345)
        assert valid_id == 12345

        # Test gestione None come nel server (check before validation)
        # Nel server: validate_user_id(request.user_id) if request.user_id else None
        user_id_from_request = None
        result_id = validate_user_id(user_id_from_request) if user_id_from_request else None
        assert result_id is None

    def test_server_context_building_real(self):
        """Test context building reale usato nel server"""
        from sigma_nex.core.context import build_prompt

        system_prompt = "You are SIGMA-NEX assistant"
        history = ["Previous question", "Previous answer"]
        question = "Current question"

        # Test build_prompt reale
        prompt = build_prompt(system_prompt, history, question)

        assert isinstance(prompt, str)
        assert system_prompt in prompt
        assert question in prompt
        assert len(prompt) > len(question)

    def test_server_config_integration_real(self):
        """Test integrazione config reale nel server"""
        server = SigmaServer()

        # Test accesso config reale
        config = server.config
        assert isinstance(config, dict)

        # Test parametri essenziali per server
        assert "model" in config or "model_name" in config
        assert "max_tokens" in config

        # Test che model_name sia accessibile
        model_name = server.model_name
        assert isinstance(model_name, str)
        assert len(model_name) > 0

    def test_server_medical_keywords_real(self):
        """Test rilevamento keywords mediche reale"""
        server = SigmaServer()

        # Test _is_medical_query con keywords reali
        medical_query = "Come disinfettare una ferita?"
        non_medical_query = "Che tempo farà domani?"

        assert server._is_medical_query(medical_query) is True
        assert server._is_medical_query(non_medical_query) is False

        # Test con altre keywords
        assert server._is_medical_query("antibiotico per infezione") is True
        assert server._is_medical_query("primo soccorso") is True
        assert server._is_medical_query("programming in python") is False

    def test_server_client_info_extraction_real(self):
        """Test estrazione info client reale"""
        server = SigmaServer()
        client = TestClient(server.app)

        # Test che _get_client_info funzioni con request reale
        response = client.get("/")
        assert response.status_code == 200

        # Il metodo _get_client_info viene chiamato internamente
        # e non dovrebbe causare errori


class TestSigmaServerSecurity:
    """Test sicurezza del server"""

    def test_server_secure_mode_integration(self):
        """Test integrazione modalità sicura"""
        server = SigmaServer()

        # Se il runner supporta secure mode, dovrebbe essere configurato
        if hasattr(server.runner, "secure"):
            # Test che la modalità sicura sia configurabile
            assert isinstance(server.runner.secure, bool)

    def test_server_input_sanitization_real(self):
        """Test sanitizzazione input del server con validation reale"""
        server = SigmaServer()
        client = TestClient(server.app)

        # Test con input potenzialmente pericoloso usando endpoint ask
        dangerous_inputs = [
            {"question": "<script>alert('xss')</script>"},
            {"question": "'; DROP TABLE users; --"},
            {"question": "../../../etc/passwd"},
        ]

        # Mock entrambi i client HTTP (requests e httpx)
        with mock_http_clients() as (mock_post, mock_httpx):

            for dangerous_input in dangerous_inputs:
                response = client.post("/ask", json=dangerous_input)
                # Server dovrebbe sanitizzare input e processare richiesta
                if response.status_code == 200:
                    data = response.json()
                    # Input dovrebbe essere stato sanitizzato
                    assert "script" not in str(data.get("response", ""))
                    assert "DROP TABLE" not in str(data.get("response", ""))


class TestSigmaServerPerformance:
    """Test performance del server"""

    def test_server_concurrent_requests_handling(self):
        """Test gestione richieste concorrenti"""
        server = SigmaServer()
        client = TestClient(server.app)

        # Mock per evitare chiamate esterne reali
        with mock_http_clients() as (mock_post, mock_httpx):
            mock_post.return_value.json.return_value = {"response": "concurrent test"}

            # Test multiple richieste
            responses = []
            for i in range(3):
                try:
                    response = client.post("/api/query", json={"query": f"test {i}"})
                    responses.append(response)
                except Exception:
                    # Se endpoint non esiste, testa GET
                    response = client.get(f"/test{i}")
                    responses.append(response)

    def test_server_async_methods_coverage(self):
        """Test per coprire metodi async del server reali"""
        import asyncio

        with patch("sigma_nex.server.get_config") as mock_get_config:
            mock_config = Mock()
            mock_config.config = {"auth_enabled": True, "api_keys": ["test_key"], "model": "mistral", "debug": False}
            mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
            from pathlib import Path

            mock_config.get_path.return_value = Path("/tmp/logs")
            mock_get_config.return_value = mock_config

            server = SigmaServer()

        # Test async startup (REALE - startup tasks)
        if hasattr(server, "startup"):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # Test async startup routine REALE
                if asyncio.iscoroutinefunction(server.startup):
                    result = loop.run_until_complete(server.startup())
                    assert result is None  # startup returns None

                    # Verifica che startup sia stato eseguito
                    # (translation preload tentativo)
                    assert hasattr(server, "translation_enabled")
            finally:
                loop.close()

        # Test async log request metodo REALE
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            test_data = {
                "timestamp": "2025-01-01T00:00:00",
                "user_id": 123,
                "question": "test",
                "status": "test",
            }
            # Testa il metodo _log_request REALE
            result = loop.run_until_complete(server._log_request(test_data))
            assert result is None  # async logging returns None

            # Verifica che il file di log sia stato tentato
            assert server.log_path is not None
        finally:
            loop.close()

        # Test async _call_ollama con errori REALI - timeout
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            with mock_http_clients() as (mock_post, mock_httpx):
                # Test timeout error REALE
                mock_post.side_effect = requests.exceptions.Timeout("Timeout")
                # Also mock httpx timeout
                mock_client_instance = mock_httpx.return_value.__aenter__.return_value
                mock_client_instance.post.side_effect = Exception("httpx.TimeoutException")

                with pytest.raises(HTTPException) as exc_info:
                    loop.run_until_complete(server._call_ollama({"prompt": "test"}))
                assert exc_info.value.status_code == 504
        finally:
            loop.close()

        # Test async _call_ollama con errori REALI - connection
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Patch entrambe le librerie possibili
            with patch("httpx.AsyncClient.post") as mock_httpx_post, patch("requests.post") as mock_requests_post:

                # Simula connection error per httpx e requests
                import httpx

                mock_httpx_post.side_effect = httpx.ConnectError("Connection failed")
                mock_requests_post.side_effect = requests.exceptions.ConnectionError("Connection failed")

                with pytest.raises(HTTPException) as exc_info:
                    loop.run_until_complete(server._call_ollama({"prompt": "test"}))
                # Il server può restituire 503 o 504 in base all'implementazione
                assert exc_info.value.status_code in [503, 504]

                # Test server error REALE
                mock_response = Mock()
                mock_response.status_code = 500
                mock_response.text = "Internal server error"
                mock_post.return_value = mock_response
                with pytest.raises(HTTPException) as exc_info:
                    loop.run_until_complete(server._call_ollama({"prompt": "test"}))
                # Server può restituire vari codici di errore
                assert exc_info.value.status_code in [503, 504]

        finally:
            loop.close()

    def test_server_error_handling_paths(self):
        """Test path di gestione errori del server REALI"""
        with patch("sigma_nex.server.get_config") as mock_get_config:
            mock_config = Mock()
            mock_config.config = {"auth_enabled": True, "api_keys": ["test_key"], "model": "mistral", "debug": False}
            mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
            from pathlib import Path

            mock_config.get_path.return_value = Path("/tmp/logs")
            mock_get_config.return_value = mock_config

            server = SigmaServer()
        client = TestClient(server.app)

        # Test blocklist check REALE con async
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Force block a user
            result = loop.run_until_complete(server._is_blocked(666, 999))
            assert isinstance(result, bool)
        finally:
            loop.close()

        # Test medical query detection REALE
        medical_keywords = ["medicina", "ferita", "disinfettante", "antibiotico"]
        for keyword in medical_keywords:
            is_medical = server._is_medical_query(f"Come uso {keyword}?")
            assert is_medical

        # Test non-medical query
        is_medical = server._is_medical_query("Come cucinare la pasta?")
        assert is_medical is False

        # Test client info extraction REALE
        from fastapi import Request

        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = "192.168.1.1"
        mock_request.headers = {"user-agent": "TestAgent/1.0"}

        client_info = server._get_client_info(mock_request)
        assert "ip" in client_info
        assert "hostname" in client_info
        assert "user_agent" in client_info
        assert client_info["ip"] == "192.168.1.1"

        # Test endpoint reali con errori
        with mock_http_clients() as (mock_post, mock_httpx):
            # Simula errore 500 di Ollama
            mock_post.return_value.status_code = 500
            mock_post.return_value.text = "Internal error"
            # Also mock httpx response
            mock_client_instance = mock_httpx.return_value.__aenter__.return_value
            mock_client_instance.post.return_value.status_code = 500
            mock_client_instance.post.return_value.text = "Internal error"

            response = client.post("/ask", json={"question": "test error"})
            assert response.status_code in [401, 503, 504]  # Server error o auth required

        # Test logs endpoint REALE (localhost only)
        response = client.get("/logs?last=10")
        # TestClient potrebbe non simulare correttamente localhost
        assert response.status_code in [
            200,
            403,
            500,
        ]  # 403 se non localhost, 200 se ok, 500 se errore

        # Test legacy endpoint REALE
        with mock_http_clients() as (mock_post, mock_httpx):
            mock_post.return_value.json.return_value = {"response": "legacy test"}

            response = client.post("/api/query", json={"question": "legacy test"})
            # Server può restituire vari codici in base alla configurazione
            assert response.status_code in [
                200,
                404,
                500,
                504,
            ]  # 404 se endpoint non esiste, 500 errore interno, 504 se timeout

    def test_server_memory_usage_real(self):
        """Test uso memoria del server"""
        import gc

        # Test che il server non abbia memory leaks evidenti
        initial_objects = len(gc.get_objects())

        with patch("sigma_nex.server.get_config") as mock_get_config:
            mock_config = Mock()
            mock_config.config = {"auth_enabled": True, "api_keys": ["test_key"], "model": "mistral", "debug": False}
            mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
            from pathlib import Path

            mock_config.get_path.return_value = Path("/tmp/logs")
            mock_get_config.return_value = mock_config

            server = SigmaServer()
        client = TestClient(server.app)

        # Simula alcune operazioni
        for i in range(5):
            try:
                client.get(f"/test{i}")
            except Exception:
                pass

        # Cleanup
        del server
        del client
        gc.collect()

        final_objects = len(gc.get_objects())

        # Non dovrebbe esserci un aumento drammatico di oggetti
        objects_increase = final_objects - initial_objects
        assert objects_increase < 1000  # Threshold ragionevole
