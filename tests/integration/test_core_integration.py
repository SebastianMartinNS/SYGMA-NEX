"""
Integration tests for core component interactions.
Tests how Runner, Config, DataLoader, and other core components work together.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, Mock

from sigma_nex.config import SigmaConfig, get_config
from sigma_nex.data_loader import load_json_data
from sigma_nex.core.runner import Runner
from sigma_nex.core.context import build_prompt


class TestCoreIntegration:
    """Test integration between core components."""

    def test_config_dataloader_integration(self):
        """Test that Config and DataLoader work together correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test data files
            framework_path = Path(temp_dir) / "framework.json"
            framework_data = {
                "modules": [
                    {"name": "survival", "content": "Basic survival knowledge"},
                    {"name": "medical", "content": "First aid procedures"}
                ]
            }
            framework_path.write_text(json.dumps(framework_data))
            
            # Create config
            config = SigmaConfig(temp_dir)
            config.set("data.framework_path", str(framework_path))
            
            # Test data loading
            data = load_json_data(str(framework_path))
            assert data is not None
            assert "modules" in data
            assert len(data["modules"]) == 2

    def test_config_runner_integration(self):
        """Test that Config and Runner integrate properly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_data = {
                "model": "mistral:latest",
                "temperature": 0.7,
                "max_tokens": 1000,
                "debug": False
            }
            
            config = SigmaConfig(temp_dir)
            for key, value in config_data.items():
                config.set(key, value)
            
            # Test Runner initialization with config
            runner = Runner(config.config)
            assert runner.model == "mistral:latest"
            assert runner.config["temperature"] == 0.7
            assert runner.config["max_tokens"] == 1000

    def test_runner_context_integration(self):
        """Test Runner and Context building integration."""
        test_config = {
            "model": "test:model",
            "temperature": 0.5,
            "max_tokens": 500,
            "system_prompt": "You are a survival assistant."
        }
        
        runner = Runner(test_config)
        history = ["What should I do in an emergency?"]
        
        # Test context building
        with patch("sigma_nex.core.context.build_prompt") as mock_build:
            mock_build.return_value = "Built prompt with context"
            
            # This would be called internally by runner
            prompt = build_prompt("Test query", history)
            assert prompt is not None
            mock_build.assert_called_once()


class TestDataFlowIntegration:
    """Test data flow between components."""

    def test_complete_data_flow(self):
        """Test complete data flow from config to response."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Setup test data
            framework_path = Path(temp_dir) / "framework.json" 
            framework_data = {
                "modules": [
                    {"name": "test", "content": "Test knowledge base"}
                ]
            }
            framework_path.write_text(json.dumps(framework_data))
            
            # Setup config
            config = SigmaConfig(temp_dir)
            config.set("data.framework_path", str(framework_path))
            config.set("model", "test:model")
            
            # Test data loading
            data = load_json_data(str(framework_path))
            assert data is not None
            
            # Test runner creation
            runner = Runner(config.config)
            assert runner is not None
            
            # Test history management
            runner.add_to_history("user", "Test query")
            history = runner.get_context()
            assert len(history) > 0

    def test_error_propagation_integration(self):
        """Test how errors propagate through the system."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SigmaConfig(temp_dir)
            
            # Test with invalid framework path
            config.set("data.framework_path", "/nonexistent/path.json")
            
            # Should handle gracefully
            data = load_json_data("/nonexistent/path.json")
            assert data is None or data == {}


class TestConfigurationIntegration:
    """Test configuration system integration."""

    def test_global_config_integration(self):
        """Test global configuration system."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.config.find_project_root", return_value=temp_dir):
                # Test global config access
                config1 = get_config()
                config2 = get_config()
                
                # Should be same instance (singleton)
                assert config1 is config2
                
                # Test configuration persistence
                config1.set("test_key", "test_value")
                assert config2.get("test_key") == "test_value"

    def test_config_file_operations_integration(self):
        """Test configuration file operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SigmaConfig(temp_dir)
            
            # Test setting and getting values
            config.set("nested.key", "value")
            assert config.get("nested.key") == "value"
            
            # Test saving and loading
            config.save()
            
            # Create new config instance to test loading
            config2 = SigmaConfig(temp_dir)
            assert config2.get("nested.key") == "value"


class TestComponentInteractionScenarios:
    """Test realistic component interaction scenarios."""

    def test_startup_sequence_integration(self):
        """Test typical application startup sequence."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.config.find_project_root", return_value=temp_dir):
                # 1. Get global config (like CLI would do)
                config = get_config()
                assert config is not None
                
                # 2. Initialize runner (like CLI would do)
                runner = Runner(config.config)
                assert runner is not None
                
                # 3. Perform self-check (like CLI would do)
                runner.self_check()  # Should not raise exceptions

    def test_user_interaction_flow(self):
        """Test typical user interaction flow."""
        test_config = {
            "model": "test:model",
            "temperature": 0.7,
            "max_history": 10
        }
        
        runner = Runner(test_config)
        
        # Simulate user conversation
        queries = [
            "What is survival?",
            "How do I find water?", 
            "Tell me about shelter building"
        ]
        
        for query in queries:
            runner.add_to_history("user", query)
            runner.add_to_history("assistant", f"Response to: {query}")
        
        # Verify history management
        context = runner.get_context()
        assert len(context) == len(queries) * 2  # user + assistant messages