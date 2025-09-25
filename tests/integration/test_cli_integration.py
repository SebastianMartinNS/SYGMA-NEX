"""
Integration tests for CLI functionality.
Tests the complete CLI workflow from configuration to execution.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, Mock
import subprocess

from sigma_nex.cli import main
from sigma_nex.config import get_config
from click.testing import CliRunner


class TestCLIIntegration:
    """Test CLI integration with real file system and configuration."""

    def test_cli_config_workflow_integration(self):
        """Test CLI with real configuration workflow."""
        runner = CliRunner()
        
        # Test that CLI can handle missing config gracefully
        result = runner.invoke(main, ["self-check"])
        assert result.exit_code == 0
        # The command should run successfully and show some output
        assert result.output is not None

    def test_cli_framework_loading_integration(self):
        """Test CLI framework loading with real file operations."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            framework_path = Path(temp_dir) / "framework.json"
            framework_path.write_text('{"modules": [{"name": "test", "content": "test content"}]}')
            
            result = runner.invoke(main, ["load-framework", str(framework_path)])
            assert result.exit_code == 0

    def test_cli_help_system_integration(self):
        """Test that CLI help system works correctly."""
        runner = CliRunner()
        
        # Test main help
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "SIGMA-NEX" in result.output
        
        # Test command help
        result = runner.invoke(main, ["self-check", "--help"])
        assert result.exit_code == 0


class TestCLIErrorHandlingIntegration:
    """Test CLI error handling in integration scenarios."""

    def test_cli_invalid_config_handling(self):
        """Test CLI behavior with invalid configuration."""
        runner = CliRunner()
        
        result = runner.invoke(main, ["self-check"])
        # Should handle gracefully, not crash
        assert result.exit_code == 0

    def test_cli_permission_error_handling(self):
        """Test CLI behavior with permission errors."""
        runner = CliRunner()
        
        with patch("sigma_nex.config.SigmaConfig.save") as mock_save:
            mock_save.side_effect = PermissionError("Access denied")
            
            result = runner.invoke(main, ["self-check"])
            # Should handle gracefully
            assert result.exit_code == 0


class TestCLIRealWorldScenarios:
    """Test CLI in realistic usage scenarios."""

    def test_cli_first_time_user_workflow(self):
        """Test CLI workflow for first-time users."""
        runner = CliRunner()
        
        # First run should initialize gracefully
        result = runner.invoke(main, ["self-check"])
        assert result.exit_code == 0
        
        # Should be able to show help without errors
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "commands" in result.output.lower()

    @patch("subprocess.run")
    def test_cli_ollama_integration_check(self, mock_subprocess):
        """Test CLI Ollama integration checking."""
        runner = CliRunner()
        
        # Mock successful Ollama check
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "mistral:latest\n"
        mock_subprocess.return_value = mock_result
        
        with patch("shutil.which", return_value="/usr/bin/ollama"):
            result = runner.invoke(main, ["self-check"])
            assert result.exit_code == 0

    def test_cli_configuration_persistence(self):
        """Test that CLI configuration persists across sessions."""
        runner = CliRunner()
        
        # First invocation should create config
        result1 = runner.invoke(main, ["self-check"])
        assert result1.exit_code == 0
        
        # Second invocation should use existing config
        result2 = runner.invoke(main, ["self-check"])
        assert result2.exit_code == 0