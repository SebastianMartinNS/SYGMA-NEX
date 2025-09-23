"""
Test configuration and fixtures for SIGMA-NEX test suite.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
import json
import yaml

import pytest

# Add sigma_nex to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sigma_nex.config import SigmaConfig


@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """Test configuration dictionary."""
    return {
        "system_prompt": "Test system prompt for SIGMA-NEX cognitive agent.",
        "model_name": "test-model",
        "debug": True,
        "max_history": 50,
        "temperature": 0.7,
        "max_tokens": 2000,
        "timeout": 120,
        "translation": {
            "enabled": False,
            "models_path": "models/translate"
        },
        "data": {
            "framework_path": "data/Framework_SIGMA.json",
            "faq_path": "data/faq_domande_critiche.json"
        }
    }


@pytest.fixture
def temp_project_dir() -> Generator[Path, None, None]:
    """Create a temporary project directory with test structure.

    Ensures we exit the temp directory before cleanup to avoid Windows
    TemporaryDirectory removal issues (can't delete current working dir).
    """
    old_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)
        
        # Create directory structure
        (project_dir / "sigma_nex").mkdir()
        (project_dir / "data").mkdir()
        (project_dir / "logs").mkdir()
        (project_dir / "models").mkdir()
        (project_dir / "tests").mkdir()
        
        # Create test config file
        config_data = {
            "system_prompt": "Test prompt",
            "model_name": "test-model"
            # Removed debug: True to test defaults
        }
        
        with open(project_dir / "config.yaml", "w", encoding="utf-8") as f:
            yaml.dump(config_data, f, default_flow_style=False)
        
        # Create test data files
        framework_data = {
            "moduli": [
                {
                    "titolo": "Test Module 1",
                    "contenuto": "Test content for module 1",
                    "keywords": ["test", "module"]
                },
                {
                    "titolo": "Test Module 2", 
                    "contenuto": "Test content for module 2",
                    "keywords": ["test", "example"]
                }
            ]
        }
        
        with open(project_dir / "data" / "Framework_SIGMA.json", "w", encoding="utf-8") as f:
            json.dump(framework_data, f, ensure_ascii=False, indent=2)
        
        faq_data = {
            "domande": [
                {
                    "domanda": "Test question 1?",
                    "risposta": "Test answer 1",
                    "categoria": "test"
                },
                {
                    "domanda": "Test question 2?",
                    "risposta": "Test answer 2", 
                    "categoria": "example"
                }
            ]
        }
        
        with open(project_dir / "data" / "faq_domande_critiche.json", "w", encoding="utf-8") as f:
            json.dump(faq_data, f, ensure_ascii=False, indent=2)
        
        yield project_dir

        # Always move out of the temporary directory after test to a safe location
        # (repo root), to avoid Windows deletion issues for TemporaryDirectory.
        try:
            safe_root = Path(__file__).parent.parent.resolve()
            os.chdir(str(safe_root))
        except Exception:
            try:
                os.chdir(old_cwd)
            except Exception:
                pass


@pytest.fixture
def test_config_obj(temp_project_dir: Path, test_config: Dict[str, Any]) -> Generator[SigmaConfig, None, None]:
    """Create a test SigmaConfig instance."""
    config_path = temp_project_dir / "config.yaml"
    
    # Update config with temp directory paths
    test_config["project_root"] = str(temp_project_dir)
    
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(test_config, f, default_flow_style=False)
    
    # Change to temp directory
    old_cwd = os.getcwd()
    os.chdir(temp_project_dir)
    
    try:
        config = SigmaConfig(config_path=str(config_path))
        yield config
    finally:
        os.chdir(old_cwd)


@pytest.fixture
def sample_history() -> list:
    """Sample conversation history for testing."""
    return [
        "Utente: Come posso accendere un fuoco senza fiammiferi?",
        "SIGMA-NEX: Puoi usare il metodo dell'acciarino e pietra focaia...",
        "Utente: E se non ho questi strumenti?",
        "SIGMA-NEX: Esistono diversi metodi alternativi come l'archetto per il fuoco..."
    ]


@pytest.fixture
def sample_questions() -> list:
    """Sample questions for testing."""
    return [
        "Come posso purificare l'acqua in natura?",
        "Quali sono i segnali di soccorso internazionali?",
        "Come costruire un riparo di emergenza?",
        "Quali piante sono commestibili in Italia?",
        "Come medicare una ferita profonda?",
        "Come orientarsi senza bussola?",
        "Cosa fare in caso di attacco di animali selvatici?",
        "Come conservare il cibo senza frigorifero?"
    ]


@pytest.fixture
def mock_medical_keywords() -> list:
    """Medical keywords for testing."""
    return [
        "medicina", "disinfettante", "ferita", "primo soccorso",
        "antibiotico", "antiseptico", "farmaco", "sangue",
        "ustione", "infezione", "medicazione"
    ]


@pytest.fixture
def mock_ollama_response() -> Dict[str, Any]:
    """Mock Ollama API response."""
    return {
        "response": "Questa è una risposta di test dal modello SIGMA-NEX.",
        "model": "test-model",
        "created_at": "2024-01-15T10:00:00Z",
        "done": True
    }


@pytest.fixture(autouse=True)
def cleanup_temp_files():
    """Automatically cleanup temporary files after each test."""
    yield
    
    # Clean up any temporary files in current directory
    temp_patterns = ["*.tmp", "*.temp", "test_*.log", "test_*.json"]
    
    for pattern in temp_patterns:
        for file_path in Path.cwd().glob(pattern):
            try:
                file_path.unlink()
            except Exception:
                pass


# Ensure we always leave the current working directory in a safe location
# after each test. Some tests change cwd into a TemporaryDirectory without
# restoring it, which can cause Windows to fail deleting that directory.
@pytest.fixture(autouse=True)
def _restore_cwd():
    original_cwd = os.getcwd()
    try:
        yield
    finally:
        try:
            os.chdir(original_cwd)
        except Exception:
            # As a last resort, go to the repository root
            os.chdir(str(Path(__file__).parent.parent.resolve()))


class MockOllamaServer:
    """Mock Ollama server for testing."""
    
    def __init__(self, responses: Dict[str, str] = None):
        self.responses = responses or {
            "default": "Mock response from SIGMA-NEX test model."
        }
        self.call_count = 0
        
    def generate_response(self, prompt: str, model: str = None) -> Dict[str, Any]:
        """Generate a mock response."""
        self.call_count += 1
        
        # Choose response based on prompt content
        response_text = self.responses.get("default")
        
        if "medical" in prompt.lower() or "medicina" in prompt.lower():
            response_text = self.responses.get("medical", response_text)
        elif "survival" in prompt.lower() or "sopravvivenza" in prompt.lower():
            response_text = self.responses.get("survival", response_text)
        
        return {
            "response": response_text,
            "model": model or "test-model",
            "done": True,
            "total_duration": 1000000000,  # 1 second in nanoseconds
            "load_duration": 100000000,    # 0.1 second
            "prompt_eval_count": 50,
            "eval_count": 100
        }


@pytest.fixture
def mock_ollama_server() -> MockOllamaServer:
    """Create a mock Ollama server instance."""
    responses = {
        "default": "Risposta di test da SIGMA-NEX per query generica.",
        "medical": "Risposta medica di test: consulta sempre un medico per problemi gravi.",
        "survival": "Risposta di sopravvivenza di test: trova riparo, acqua e cibo in quest'ordine."
    }
    return MockOllamaServer(responses)


# Test data constants
TEST_SURVIVAL_MODULES = [
    {
        "titolo": "Acqua e Idratazione",
        "contenuto": "L'acqua è la priorità numero uno per la sopravvivenza...",
        "keywords": ["acqua", "idratazione", "purificazione", "potabile"]
    },
    {
        "titolo": "Riparo e Protezione",
        "contenuto": "Un riparo adeguato protegge dalle intemperie...",
        "keywords": ["riparo", "protezione", "tenda", "rifugio"]
    },
    {
        "titolo": "Fuoco e Calore",
        "contenuto": "Il fuoco fornisce calore, luce e protezione...",
        "keywords": ["fuoco", "accensione", "legna", "calore"]
    }
]

TEST_FAQ_DATA = [
    {
        "domanda": "Come accendere un fuoco senza fiammiferi?",
        "risposta": "Puoi usare l'acciarino, il metodo dell'archetto, o la lente di ingrandimento.",
        "categoria": "fuoco"
    },
    {
        "domanda": "Quali sono le piante velenose più comuni in Italia?",
        "risposta": "Oleandro, belladonna, cicuta e amanita phalloides sono molto pericolose.",
        "categoria": "botanica"
    }
]