"""
Basic integration test that can pass CI/CD.
"""

import json
import tempfile
from pathlib import Path

import pytest

from sigma_nex.config import SigmaConfig
from sigma_nex.data_loader import load_json_data


class TestBasicIntegration:
    """Basic integration tests that should pass."""

    def test_config_creation(self):
        """Test basic config creation without file operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SigmaConfig(temp_dir)
            config.set("model", "test:model")
            assert config.get("model") == "test:model"

    def test_data_loader_with_valid_json(self):
        """Test data loader with valid JSON file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.json"
            test_data = {"test": "value", "modules": [{"name": "test"}]}
            test_file.write_text(json.dumps(test_data))

            result = load_json_data(str(test_file))
            assert result is not None
            assert result["test"] == "value"

    def test_data_loader_with_missing_file(self):
        """Test data loader with missing file."""
        result = load_json_data("/nonexistent/file.json")
        # Should return empty list, not None
        assert result == []

    def test_config_without_save(self):
        """Test config operations without saving to disk."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SigmaConfig(temp_dir)

            # Test nested keys
            config.set("nested.key", "value")
            assert config.get("nested.key") == "value"

            # Test default values
            assert config.get("nonexistent", "default") == "default"

    def test_json_data_structure_validation(self):
        """Test that JSON data has expected structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test framework structure
            framework_file = Path(temp_dir) / "framework.json"
            framework_data = {
                "modules": [{"name": "test_module", "content": "test content"}]
            }
            framework_file.write_text(json.dumps(framework_data))

            result = load_json_data(str(framework_file))
            assert "modules" in result
            assert len(result["modules"]) == 1
            assert result["modules"][0]["name"] == "test_module"


class TestSystemComponents:
    """Test system component integration."""

    def test_config_and_dataloader_integration(self):
        """Test config and data loader working together."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test data
            data_file = Path(temp_dir) / "data.json"
            data_content = {"test": "integration", "modules": []}
            data_file.write_text(json.dumps(data_content))

            # Create config
            config = SigmaConfig(temp_dir)
            config.set("data.path", str(data_file))

            # Test that data can be loaded using path from config
            data_path = config.get("data.path")
            loaded_data = load_json_data(data_path)

            assert loaded_data is not None
            assert loaded_data["test"] == "integration"

    def test_error_handling_integration(self):
        """Test error handling across components."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SigmaConfig(temp_dir)

            # Test config with invalid data
            config.set("test.value", None)
            assert config.get("test.value") is None

            # Test data loader with invalid file
            invalid_data = load_json_data("/invalid/path")
            assert invalid_data == []  # Should return empty list


class TestRealWorldScenarios:
    """Test realistic usage scenarios."""

    def test_basic_setup_workflow(self):
        """Test basic application setup workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Create configuration
            config = SigmaConfig(temp_dir)
            config.set("model", "mistral:latest")
            config.set("temperature", 0.7)

            # 2. Verify configuration
            assert config.get("model") == "mistral:latest"
            assert config.get("temperature") == 0.7

            # 3. Create data file
            data_file = Path(temp_dir) / "data.json"
            data_file.write_text('{"modules": [{"name": "test"}]}')

            # 4. Load data
            data = load_json_data(str(data_file))
            assert data is not None
            assert len(data["modules"]) == 1

    def test_configuration_flexibility(self):
        """Test configuration flexibility."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SigmaConfig(temp_dir)

            # Test various data types
            config.set("string_value", "test")
            config.set("int_value", 42)
            config.set("float_value", 3.14)
            config.set("bool_value", True)
            config.set("list_value", [1, 2, 3])
            config.set("dict_value", {"nested": "value"})

            # Verify all values
            assert config.get("string_value") == "test"
            assert config.get("int_value") == 42
            assert config.get("float_value") == 3.14
            assert config.get("bool_value") is True
            assert config.get("list_value") == [1, 2, 3]
            assert config.get("dict_value")["nested"] == "value"
