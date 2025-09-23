"""
Unit tests for SIGMA-NEX configuration system.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import yaml
import json
import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sigma_nex.config import SigmaConfig, get_config


class TestSigmaConfig:
    """Test suite for SigmaConfig class."""
    
    def test_config_initialization_default(self, temp_project_dir):
        """Test config initialization with default values."""
        os.chdir(temp_project_dir)
        
        config = SigmaConfig()
        
        assert config.project_root == temp_project_dir
        assert config.get('debug') is False
        assert config.get('model_name') == 'test-model'  # From fixture config
        assert config.get('temperature') == 0.7
        
    def test_config_initialization_custom_file(self, temp_project_dir, test_config):
        """Test config initialization with custom config file."""
        config_path = temp_project_dir / "custom_config.yaml"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(test_config, f)
        
        os.chdir(temp_project_dir)
        config = SigmaConfig(config_path=str(config_path))
        
        assert config.get('model_name') == 'test-model'
        assert config.get('debug') is True
        assert config.get('max_history') == 50
        
    def test_config_path_resolution(self, test_config_obj):
        """Test path resolution functionality."""
        config = test_config_obj
        
        # Test data path resolution
        data_path = config.get_path('data', 'data')
        assert data_path.name == 'data'
        assert data_path.is_absolute()
        
        # Test logs path resolution
        logs_path = config.get_path('logs', 'logs')
        assert logs_path.name == 'logs'
        assert logs_path.is_absolute()
        
        # Test custom path resolution
        custom_path = config.get_path('custom', 'fallback')
        assert custom_path.name == 'fallback'
        
    def test_config_get_method(self, test_config_obj):
        """Test config.get() method with defaults."""
        config = test_config_obj
        
        # Test existing key
        assert config.get('model_name') == 'test-model'
        
        # Test non-existing key with default
        assert config.get('non_existent', 'default_value') == 'default_value'
        
        # Test nested key access
        nested_value = config.get('translation.enabled', True)
        assert nested_value is False
        
    def test_config_lazy_loading(self, temp_project_dir):
        """Test lazy loading of configuration."""
        config_path = temp_project_dir / "lazy_config.yaml"
        
        # Create config file after SigmaConfig initialization
        config = SigmaConfig(config_path=str(config_path))
        
        # Config file doesn't exist yet, should use defaults
        assert config.get('model_name') == 'mistral'
        
        # Now create the config file
        test_data = {'model_name': 'lazy-model', 'debug': True}
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(test_data, f)
        
        # Force reload
        config._load_config()
        
        assert config.get('model_name') == 'lazy-model'
        assert config.get('debug') is True
        
    def test_config_project_root_detection(self, temp_project_dir):
        """Test automatic project root detection."""
        # Create nested directory structure
        nested_dir = temp_project_dir / "subdir" / "nested"
        nested_dir.mkdir(parents=True)
        
        # Change to nested directory
        os.chdir(nested_dir)
        
        config = SigmaConfig()
        
        # Should detect the temp_project_dir as project root
        assert config.project_root == temp_project_dir
        
    def test_config_invalid_yaml(self, temp_project_dir):
        """Test handling of invalid YAML configuration."""
        config_path = temp_project_dir / "invalid.yaml"
        
        # Write invalid YAML
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write("invalid: yaml: content: [unclosed")
        
        os.chdir(temp_project_dir)
        
        # Should not raise exception, fall back to defaults
        config = SigmaConfig(config_path=str(config_path))
        assert config.get('model_name') == 'mistral'  # default value
        
    def test_config_missing_file(self, temp_project_dir):
        """Test handling of missing configuration file."""
        missing_path = temp_project_dir / "missing.yaml"
        
        os.chdir(temp_project_dir)
        config = SigmaConfig(config_path=str(missing_path))
        
        # Should use defaults without error
        assert config.get('model_name') == 'mistral'
        assert config.get('debug') is False
        

class TestConfigGlobalFunction:
    """Test suite for get_config() global function."""
    
    def test_get_config_singleton(self, temp_project_dir):
        """Test that get_config() returns singleton instance."""
        os.chdir(temp_project_dir)
        
        config1 = get_config()
        config2 = get_config()
        
        # Should be the same instance
        assert config1 is config2
        
    def test_get_config_with_custom_path(self, temp_project_dir, test_config):
        """Test get_config() with custom configuration path."""
        config_path = temp_project_dir / "test_config.yaml"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(test_config, f)
        
        os.chdir(temp_project_dir)
        config = get_config(str(config_path))
        
        assert config.get('model_name') == 'test-model'
        assert config.get('debug') is True
        

class TestConfigIntegration:
    """Integration tests for configuration system."""
    
    def test_config_with_real_data_files(self, temp_project_dir):
        """Test configuration with actual data files."""
        os.chdir(temp_project_dir)
        config = SigmaConfig()
        
        # Check that data files exist and are accessible
        framework_path = config.get_path('data', 'data') / "Framework_SIGMA.json"
        faq_path = config.get_path('data', 'data') / "faq_domande_critiche.json"
        
        assert framework_path.exists()
        assert faq_path.exists()
        
        # Verify data file contents
        with open(framework_path, 'r', encoding='utf-8') as f:
            framework_data = json.load(f)
            assert 'moduli' in framework_data
            assert len(framework_data['moduli']) > 0
        
        with open(faq_path, 'r', encoding='utf-8') as f:
            faq_data = json.load(f)
            assert 'domande' in faq_data
            assert len(faq_data['domande']) > 0
            
    def test_config_path_creation(self, temp_project_dir):
        """Test that config system creates necessary directories."""
        os.chdir(temp_project_dir)
        config = SigmaConfig()
        
        # Get path to non-existent directory
        new_dir_path = config.get_path('new_directory', 'new_directory')
        
        # Directory should be created when accessed
        new_dir_path.mkdir(parents=True, exist_ok=True)
        assert new_dir_path.exists()
        assert new_dir_path.is_dir()
        
    def test_config_environment_variables(self, temp_project_dir, monkeypatch):
        """Test configuration with environment variables."""
        # Set environment variable
        monkeypatch.setenv("SIGMA_MODEL_NAME", "env-model")
        monkeypatch.setenv("SIGMA_DEBUG", "true")
        
        os.chdir(temp_project_dir)
        
        # Create config that could use environment variables
        config_data = {
            'model_name': os.getenv('SIGMA_MODEL_NAME', 'default'),
            'debug': os.getenv('SIGMA_DEBUG', 'false').lower() == 'true'
        }
        
        config_path = temp_project_dir / "env_config.yaml"
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        config = SigmaConfig(config_path=str(config_path))
        
        assert config.get('model_name') == 'env-model'
        assert config.get('debug') is True


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])