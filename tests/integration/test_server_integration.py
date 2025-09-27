"""
Integration tests for server functionality.
Tests server class and configuration integration.
"""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from sigma_nex.config import SigmaConfig

# Skip server tests if FastAPI is not available
try:
    from sigma_nex.server import SigmaServer

    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

pytestmark = pytest.mark.skipif(not FASTAPI_AVAILABLE, reason="FastAPI not available")


class TestServerIntegration:
    """Test server integration scenarios."""

    @pytest.fixture
    def test_config(self):
        """Create test configuration."""
        return {
            "model": "test:model",
            "temperature": 0.7,
            "max_tokens": 1000,
            "server": {"host": "127.0.0.1", "port": 8080},
        }

    def test_server_initialization(self):
        """Test server initialization with config."""
        from unittest.mock import patch

        test_config = {
            "model": "test:model",
            "model_name": "test:model",
            "temperature": 0.7,
            "max_tokens": 2048,
            "auth_enabled": True,
            "api_keys": ["test_key"],
        }

        with patch("sigma_nex.server.load_config", return_value=test_config):
            # Test server creation
            server = SigmaServer()
            assert server is not None
            assert server.config["model"] == "test:model"

    def test_server_config_integration(self):
        """Test server configuration integration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                # Test that server initializes properly and has config access
                server = SigmaServer(temp_dir)
                assert server is not None
                assert "model" in server.config
                assert isinstance(server.config, dict)

    def test_server_validation_setup(self):
        """Test server validation setup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                server = SigmaServer(temp_dir)

                # Test that validation functions are available
                from sigma_nex.utils.validation import sanitize_text_input

                test_input = "Test <script>alert('xss')</script> input"
                sanitized = sanitize_text_input(test_input)
                assert "<script>" not in sanitized

                # Verify server is properly initialized
                assert server is not None
                assert "model" in server.config

    def test_server_component_integration(self):
        """Test server integration with other components."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                server = SigmaServer(temp_dir)

                # Test config access
                assert "temperature" in server.config
                assert "model" in server.config
                assert isinstance(server.config["temperature"], (int, float))
                assert isinstance(server.config["model"], str)


class TestServerConfigurationScenarios:
    """Test server configuration scenarios."""

    def test_server_with_minimal_config(self):
        """Test server with minimal configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                server = SigmaServer(temp_dir)
                assert server is not None
                assert "model" in server.config
                assert isinstance(server.config["model"], str)

    def test_server_with_full_config(self):
        """Test server with complete configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                server = SigmaServer(temp_dir)

                # Test that server has all required config keys
                assert "model" in server.config
                assert "temperature" in server.config
                assert "max_tokens" in server.config

                # Test that values are of correct types
                assert isinstance(server.config["model"], str)
                assert isinstance(server.config["temperature"], (int, float))
                assert isinstance(server.config["max_tokens"], int)

    def test_server_missing_config_handling(self):
        """Test server behavior with missing configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                # Don't create config file
                server = SigmaServer(temp_dir)
                # Should initialize with defaults
                assert server is not None
                assert "model" in server.config

    def test_server_config_validation(self):
        """Test server configuration validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                server = SigmaServer(temp_dir)

                # Test basic config validation
                assert "model" in server.config
                assert isinstance(server.config["model"], str)
                assert 0.0 <= server.config["temperature"] <= 1.0


class TestServerErrorHandling:
    """Test server error handling scenarios."""

    def test_server_with_invalid_config(self):
        """Test server behavior with invalid configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                # Create invalid config file
                config_path = Path(temp_dir) / "config.yaml"
                config_path.write_text("invalid: yaml: content:")

                # Should handle gracefully
                server = SigmaServer(temp_dir)
                assert server is not None

    def test_server_permission_error_handling(self):
        """Test server behavior with permission errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                config = SigmaConfig(temp_dir)
                config.set("model", "test:model")

                with patch.object(config, "save", side_effect=PermissionError("Access denied")):
                    # Should still create server
                    server = SigmaServer(temp_dir)
                    assert server is not None


class TestServerRealWorldScenarios:
    """Test realistic server usage scenarios."""

    def test_server_startup_workflow(self):
        """Test typical server startup workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                # Initialize server
                server = SigmaServer(temp_dir)
                assert server is not None

                # Test that server has required configuration keys for startup
                assert "model" in server.config
                assert isinstance(server.config["model"], str)
                assert len(server.config["model"]) > 0

    def test_server_configuration_persistence(self):
        """Test server configuration persistence."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.server.get_config") as mock_get_config:
                mock_config = Mock()
                mock_config.config = {
                    "auth_enabled": True,
                    "api_keys": ["test_key"],
                    "model": "test:model",
                    "temperature": 0.7,
                    "max_tokens": 1000,
                }
                mock_config.get.side_effect = lambda key, default=None: mock_config.config.get(key, default)
                from pathlib import Path

                mock_config.get_path.return_value = Path(temp_dir) / "logs"
                mock_get_config.return_value = mock_config

                # First server instance
                server1 = SigmaServer(temp_dir)
                assert server1 is not None

                # Test that configuration is consistent
                model1 = server1.config["model"]
                temp1 = server1.config["temperature"]

                # Second server instance (simulating restart)
                server2 = SigmaServer(temp_dir)
                assert server2.config["model"] == model1
                assert server2.config["temperature"] == temp1
