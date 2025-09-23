"""
Unit tests for SIGMA-NEX core runner module.
"""

import sys
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sigma_nex.core.runner import Runner
from sigma_nex.core.context import build_prompt


class TestRunnerInitialization:
    """Test suite for Runner initialization."""
    
    def test_runner_initialization_default(self, test_config_obj):
        """Test runner initialization with default configuration."""
        runner = Runner(test_config_obj)
        
        assert runner.config is test_config_obj
        assert runner.model_name == test_config_obj.get('model_name')
        assert runner.max_history == test_config_obj.get('max_history', 100)
        assert len(runner.history) == 0
        assert len(runner.performance_stats) == 0
        
    def test_runner_initialization_custom_params(self, test_config_obj):
        """Test runner initialization with custom parameters."""
        runner = Runner(
            test_config_obj, 
            model_name="custom-model",
            max_history=50
        )
        
        assert runner.model_name == "custom-model"
        assert runner.max_history == 50
        
    def test_runner_temp_files_registry(self, test_config_obj):
        """Test temporary files registry initialization."""
        runner = Runner(test_config_obj)
        
        assert hasattr(runner, 'temp_files')
        assert len(runner.temp_files) == 0


class TestRunnerHistoryManagement:
    """Test suite for conversation history management."""
    
    def test_add_to_history_basic(self, test_config_obj):
        """Test basic history addition."""
        runner = Runner(test_config_obj)
        
        runner.add_to_history("Test question")
        assert len(runner.history) == 1
        assert runner.history[0] == "Test question"
        
    def test_add_to_history_max_limit(self, test_config_obj):
        """Test history limit enforcement."""
        runner = Runner(test_config_obj, max_history=3)
        
        # Add more entries than the limit
        for i in range(5):
            runner.add_to_history(f"Question {i}")
            
        assert len(runner.history) == 3
        assert runner.history[0] == "Question 2"  # Oldest entries removed
        assert runner.history[-1] == "Question 4"
        
    def test_get_history_context(self, test_config_obj):
        """Test getting history context."""
        runner = Runner(test_config_obj)
        
        history_list = [
            "Utente: Come accendere un fuoco?",
            "SIGMA-NEX: Puoi usare acciarino e pietra focaia...",
            "Utente: E senza strumenti?"
        ]
        
        for item in history_list:
            runner.add_to_history(item)
            
        context = runner.get_history_context()
        
        assert len(context) == 3
        assert all(item in context for item in history_list)
        
    def test_clear_history(self, test_config_obj):
        """Test history clearing."""
        runner = Runner(test_config_obj)
        
        runner.add_to_history("Test 1")
        runner.add_to_history("Test 2")
        assert len(runner.history) == 2
        
        runner.clear_history()
        assert len(runner.history) == 0


class TestRunnerQueryProcessing:
    """Test suite for query processing functionality."""
    
    @patch('requests.post')
    def test_process_query_successful(self, mock_post, test_config_obj, mock_ollama_response):
        """Test successful query processing."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_ollama_response
        mock_post.return_value = mock_response
        
        runner = Runner(test_config_obj)
        
        result = runner.process_query("Come accendere un fuoco?")
        
        assert "response" in result
        assert result["response"] == mock_ollama_response["response"]
        assert "processing_time" in result
        
    @patch('requests.post')
    def test_process_query_timeout_error(self, mock_post, test_config_obj):
        """Test handling of timeout errors."""
        mock_post.side_effect = Exception("Timeout")
        
        runner = Runner(test_config_obj)
        
        result = runner.process_query("Test question")
        
        assert "error" in result
        assert "Timeout" in result["error"]


class TestRunnerTempFileManagement:
    """Test suite for temporary file management."""
    
    def test_register_temp_file(self, test_config_obj):
        """Test temporary file registration."""
        runner = Runner(test_config_obj)
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_path = Path(tmp.name)
            
        runner.register_temp_file(temp_path)
        
        assert temp_path in runner.temp_files
        
        # Cleanup
        if temp_path.exists():
            temp_path.unlink()
            
    def test_cleanup_temp_files(self, test_config_obj):
        """Test temporary file cleanup."""
        runner = Runner(test_config_obj)
        
        # Create temporary files
        temp_files = []
        for i in range(3):
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                temp_path = Path(tmp.name)
                temp_files.append(temp_path)
                runner.register_temp_file(temp_path)
                
        assert len(runner.temp_files) == 3
        
        # Cleanup
        runner.cleanup_temp_files()
        
        assert len(runner.temp_files) == 0
        
        # Verify files are actually deleted
        for temp_path in temp_files:
            assert not temp_path.exists()


class TestRunnerPerformanceStats:
    """Test suite for performance statistics."""
    
    @patch('requests.post')
    def test_performance_stats_collection(self, mock_post, test_config_obj, mock_ollama_response):
        """Test performance statistics collection."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_ollama_response
        mock_post.return_value = mock_response
        
        runner = Runner(test_config_obj)
        
        # Process a few queries
        for i in range(3):
            runner.process_query(f"Question {i}")
            
        stats = runner.get_performance_stats()
        
        assert stats["total_queries"] == 3
        assert "average_response_time" in stats
        assert "total_response_time" in stats
        assert len(runner.performance_stats) == 3
        
    def test_performance_stats_empty(self, test_config_obj):
        """Test performance stats when no queries processed."""
        runner = Runner(test_config_obj)
        
        stats = runner.get_performance_stats()
        
        assert stats["total_queries"] == 0
        assert stats["average_response_time"] == 0
        assert stats["total_response_time"] == 0


class TestRunnerHistoryManagement:
    """Test suite for conversation history management."""
    
    def test_add_to_history_basic(self, test_config_obj):
        """Test basic history addition."""
        runner = Runner(test_config_obj)
        
        runner.add_to_history("Test question")
        assert len(runner.history) == 1
        assert runner.history[0] == "Test question"
        
    def test_add_to_history_max_limit(self, test_config_obj):
        """Test history limit enforcement."""
        runner = Runner(test_config_obj, max_history=3)
        
        # Add more entries than the limit
        for i in range(5):
            runner.add_to_history(f"Question {i}")
            
        assert len(runner.history) == 3
        assert runner.history[0] == "Question 2"  # Oldest entries removed
        assert runner.history[-1] == "Question 4"
        
    def test_get_history_context(self, test_config_obj):
        """Test getting history context."""
        runner = Runner(test_config_obj)
        
        history_list = [
            "Utente: Come accendere un fuoco?",
            "SIGMA-NEX: Puoi usare acciarino e pietra focaia...",
            "Utente: E senza strumenti?"
        ]
        
        for item in history_list:
            runner.add_to_history(item)
            
        context = runner.get_history_context()
        
        assert len(context) == 3
        assert all(item in context for item in history_list)
        
    def test_clear_history(self, test_config_obj):
        """Test history clearing."""
        runner = Runner(test_config_obj)
        
        runner.add_to_history("Test 1")
        runner.add_to_history("Test 2")
        assert len(runner.history) == 2
        
        runner.clear_history()
        assert len(runner.history) == 0


class TestRunnerQueryProcessing:
    """Test suite for query processing functionality."""
    
    @patch('requests.post')
    def test_process_query_successful(self, mock_post, test_config_obj, mock_ollama_response):
        """Test successful query processing."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_ollama_response
        mock_post.return_value = mock_response
        
        runner = Runner(test_config_obj)
        
        result = runner.process_query("Come accendere un fuoco?")
        
        assert "response" in result
        assert result["response"] == mock_ollama_response["response"]
        assert "processing_time" in result
        
    @patch('requests.post')
    def test_process_query_timeout_error(self, mock_post, test_config_obj):
        """Test handling of timeout errors."""
        mock_post.side_effect = Exception("Timeout")
        
        runner = Runner(test_config_obj)
        
        result = runner.process_query("Test question")
        
        assert "error" in result
        assert "Timeout" in result["error"]


class TestRunnerTempFileManagement:
    """Test suite for temporary file management."""
    
    def test_register_temp_file(self, test_config_obj):
        """Test temporary file registration."""
        runner = Runner(test_config_obj)
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_path = Path(tmp.name)
            
        runner.register_temp_file(temp_path)
        
        assert temp_path in runner.temp_files
        
        # Cleanup
        if temp_path.exists():
            temp_path.unlink()
            
    def test_cleanup_temp_files(self, test_config_obj):
        """Test temporary file cleanup."""
        runner = Runner(test_config_obj)
        
        # Create temporary files
        temp_files = []
        for i in range(3):
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                temp_path = Path(tmp.name)
                temp_files.append(temp_path)
                runner.register_temp_file(temp_path)
                
        assert len(runner.temp_files) == 3
        
        # Cleanup
        runner.cleanup_temp_files()
        
        assert len(runner.temp_files) == 0
        
        # Verify files are actually deleted
        for temp_path in temp_files:
            assert not temp_path.exists()


class TestRunnerPerformanceStats:
    """Test suite for performance statistics."""
    
    @patch('requests.post')
    def test_performance_stats_collection(self, mock_post, test_config_obj, mock_ollama_response):
        """Test performance statistics collection."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_ollama_response
        mock_post.return_value = mock_response
        
        runner = Runner(test_config_obj)
        
        # Process a few queries
        for i in range(3):
            runner.process_query(f"Question {i}")
            
        stats = runner.get_performance_stats()
        
        assert stats["total_queries"] == 3
        assert "average_response_time" in stats
        assert "total_response_time" in stats
        assert len(runner.performance_stats) == 3
        
    def test_performance_stats_empty(self, test_config_obj):
        """Test performance stats when no queries processed."""
        runner = Runner(test_config_obj)
        
        stats = runner.get_performance_stats()
        
        assert stats["total_queries"] == 0
        assert stats["average_response_time"] == 0
        assert stats["total_response_time"] == 0


class TestContextBuilding:
    """Test suite for context and prompt building."""
    
    @patch('sigma_nex.core.retriever.search_moduli')
    def test_build_prompt_with_retrieval(self, mock_search):
        """Test prompt building with successful module retrieval."""
        mock_search.return_value = ["Module1 :: Description1", "Module2 :: Description2"]
        
        system_prompt = "You are SIGMA-NEX"
        history = ["Utente: Hello", "Assistant: Hi"]
        query = "How to survive?"
        
        result = build_prompt(system_prompt, history, query)
        
        assert system_prompt in result
        assert "Contesto:" in result
        assert "[MODULO 1: MODULE1]" in result
        assert "Description1" in result
        assert "Utente: How to survive?" in result
        assert "Assistant:" in result
        
    def test_build_prompt_without_retrieval(self):
        """Test prompt building when retrieval fails."""
        with patch('sigma_nex.core.retriever.search_moduli', side_effect=Exception("No FAISS")):
            system_prompt = "You are SIGMA-NEX"
            history = ["Utente: Hello"]
            query = "Test query"
            
            result = build_prompt(system_prompt, history, query)
            
            assert system_prompt in result
            # Contesto section is omitted when retrieval fails and no knowledge is available
            assert "Contesto:" not in result
            assert "Utente: Test query" in result
            
    def test_build_prompt_malformed_module(self):
        """Test prompt building with malformed module strings."""
        with patch('sigma_nex.core.retriever.search_moduli', return_value=["Malformed module string"]):
            system_prompt = "You are SIGMA-NEX"
            history = []
            query = "Test"
            
            result = build_prompt(system_prompt, history, query)
            
            assert "[MODULO 1]" in result
            assert "Malformed module string" in result


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
