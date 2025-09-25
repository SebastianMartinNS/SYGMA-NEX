"""
Integration tests for end-to-end system functionality.
Tests complete workflows that a user would experience.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, Mock
from click.testing import CliRunner

from sigma_nex.cli import main
from sigma_nex.config import SigmaConfig
from sigma_nex.data_loader import load_json_data
from sigma_nex.core.runner import Runner


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""

    def test_complete_cli_workflow(self):
        """Test complete CLI workflow from start to finish."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test framework file
            framework_path = Path(temp_dir) / "framework.json"
            framework_data = {
                "modules": [
                    {
                        "name": "emergency",
                        "content": "In case of emergency, stay calm and assess the situation"
                    }
                ]
            }
            framework_path.write_text(json.dumps(framework_data))
            
            with patch("sigma_nex.config.find_project_root", return_value=temp_dir):
                # 1. First run - initialization
                result = runner.invoke(main, ["self-check"])
                assert result.exit_code == 0
                
                # 2. Load framework
                result = runner.invoke(main, ["load-framework", str(framework_path)])
                assert result.exit_code == 0
                
                # 3. Another self-check to verify everything is working
                result = runner.invoke(main, ["self-check"])
                assert result.exit_code == 0

    def test_config_persistence_workflow(self):
        """Test configuration persistence across multiple operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Initial configuration
            config = SigmaConfig(temp_dir)
            config.set("model", "mistral:latest")
            config.set("temperature", 0.8)
            config.set("max_tokens", 1500)
            config.save()
            
            # Simulate restart - create new config instance
            config2 = SigmaConfig(temp_dir)
            assert config2.get("model") == "mistral:latest"
            assert config2.get("temperature") == 0.8
            assert config2.get("max_tokens") == 1500
            
            # Test runner initialization with persisted config
            runner = Runner(config2.config)
            assert runner.model == "mistral:latest"
            assert runner.config["temperature"] == 0.8

    def test_data_loading_workflow(self):
        """Test complete data loading and processing workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create comprehensive test data
            framework_path = Path(temp_dir) / "framework.json"
            faq_path = Path(temp_dir) / "faq.json"
            
            framework_data = {
                "modules": [
                    {"name": "water", "content": "Find clean water sources"},
                    {"name": "fire", "content": "Start fire for warmth and cooking"},
                    {"name": "shelter", "content": "Build appropriate shelter"}
                ]
            }
            
            faq_data = {
                "questions": [
                    {
                        "question": "How do I purify water?",
                        "answer": "Boil water for at least 1 minute to kill pathogens"
                    }
                ]
            }
            
            framework_path.write_text(json.dumps(framework_data))
            faq_path.write_text(json.dumps(faq_data))
            
            # Test loading both files
            framework = load_json_data(str(framework_path))
            faq = load_json_data(str(faq_path))
            
            assert framework is not None
            assert faq is not None
            assert len(framework["modules"]) == 3
            assert len(faq["questions"]) == 1
            
            # Test configuration with data paths
            config = SigmaConfig(temp_dir)
            config.set("data.framework_path", str(framework_path))
            config.set("data.faq_path", str(faq_path))
            
            # Test runner initialization
            runner = Runner(config.config)
            assert runner is not None

    @patch("subprocess.run")
    def test_ollama_integration_workflow(self, mock_subprocess):
        """Test Ollama integration workflow."""
        # Mock Ollama availability
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "mistral:latest\nllama2:7b\n"
        mock_subprocess.return_value = mock_result
        
        test_config = {
            "model": "mistral:latest",
            "temperature": 0.7
        }
        
        with patch("shutil.which", return_value="/usr/bin/ollama"):
            runner = Runner(test_config)
            
            # Test self-check
            runner.self_check()  # Should not raise exception
            
            # Test that subprocess was called
            mock_subprocess.assert_called_with(
                ["ollama", "list"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )


class TestErrorHandlingWorkflows:
    """Test error handling in complete workflows."""

    def test_missing_files_workflow(self):
        """Test workflow with missing configuration files."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.config.find_project_root", return_value=temp_dir):
                # Should handle missing config gracefully
                result = runner.invoke(main, ["self-check"])
                assert result.exit_code == 0
                
                # Should handle missing framework file gracefully
                result = runner.invoke(main, ["load-framework", "/nonexistent/file.json"])
                # Might fail but shouldn't crash
                assert result.exit_code in [0, 1]

    def test_corrupted_data_workflow(self):
        """Test workflow with corrupted data files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create corrupted JSON file
            bad_json_path = Path(temp_dir) / "bad.json"
            bad_json_path.write_text("{ invalid json content")
            
            # Should handle gracefully
            data = load_json_data(str(bad_json_path))
            assert data is None or data == {}

    def test_permission_error_workflow(self):
        """Test workflow with permission errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SigmaConfig(temp_dir)
            
            with patch.object(config, 'save', side_effect=PermissionError("Access denied")):
                # Should handle permission errors gracefully
                try:
                    config.set("test", "value")
                    config.save()
                except PermissionError:
                    pass  # Expected
                
                # Config should still be functional for reading
                config.set("test2", "value2")  # Should work in memory


class TestPerformanceWorkflows:
    """Test performance aspects of workflows."""

    def test_large_data_workflow(self):
        """Test workflow with larger datasets."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create larger framework file
            framework_path = Path(temp_dir) / "large_framework.json"
            
            modules = []
            for i in range(100):  # Create 100 modules
                modules.append({
                    "name": f"module_{i}",
                    "content": f"Content for module {i} " * 50  # Longer content
                })
            
            framework_data = {"modules": modules}
            framework_path.write_text(json.dumps(framework_data))
            
            # Test loading large data
            data = load_json_data(str(framework_path))
            assert data is not None
            assert len(data["modules"]) == 100
            
            # Test runner with large dataset
            config = SigmaConfig(temp_dir)
            config.set("data.framework_path", str(framework_path))
            
            runner = Runner(config.config)
            assert runner is not None

    def test_multiple_operations_workflow(self):
        """Test workflow with multiple consecutive operations."""
        test_config = {
            "model": "test:model",
            "max_history": 50
        }
        
        runner = Runner(test_config)
        
        # Simulate multiple user interactions
        for i in range(20):
            runner.add_to_history("user", f"Query {i}")
            runner.add_to_history("assistant", f"Response {i}")
        
        # Test that history is managed correctly
        context = runner.get_context()
        assert len(context) <= test_config["max_history"] * 2  # user + assistant pairs


class TestRealWorldScenarios:
    """Test realistic usage scenarios."""

    def test_new_user_setup_scenario(self):
        """Test scenario of a new user setting up the system."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("sigma_nex.config.find_project_root", return_value=temp_dir):
                # New user runs help first
                result = runner.invoke(main, ["--help"])
                assert result.exit_code == 0
                assert "SIGMA-NEX" in result.output
                
                # Then runs self-check
                result = runner.invoke(main, ["self-check"])
                assert result.exit_code == 0
                
                # Verify config was created
                config_path = Path(temp_dir) / "config.yaml"
                assert config_path.exists()

    def test_daily_usage_scenario(self):
        """Test typical daily usage scenario."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Setup like an existing user would have
            framework_path = Path(temp_dir) / "framework.json"
            framework_data = {
                "modules": [
                    {"name": "daily_survival", "content": "Daily survival tips"},
                    {"name": "emergency_prep", "content": "Emergency preparedness"}
                ]
            }
            framework_path.write_text(json.dumps(framework_data))
            
            config = SigmaConfig(temp_dir)
            config.set("data.framework_path", str(framework_path))
            config.set("model", "mistral:latest")
            config.save()
            
            # Daily usage - create runner and process queries
            runner = Runner(config.config)
            
            # Simulate conversation
            queries = [
                "What should I do first in an emergency?",
                "How do I signal for help?",
                "What are the priorities for survival?"
            ]
            
            for query in queries:
                runner.add_to_history("user", query)
                # In real usage, this would call Ollama
                runner.add_to_history("assistant", f"Response to: {query}")
            
            # Verify conversation state
            history = runner.get_context()
            assert len(history) == len(queries) * 2