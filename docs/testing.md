# 🧪 SIGMA-NEX Testing Guide

## Panoramica

SIGMA-NEX include una suite di test completa che garantisce la qualità e affidabilità del sistema in condizioni operative critiche.

## 📊 Metriche Attuali

- **Test Coverage**: 60%+
- **Test Suite**: 97 test totali
- **Test Files**: 12 file di test
- **Rapporto Test/Codice**: 0.67 (1720 linee test / 2574 linee codice)

## 🏗️ Struttura Test

```
tests/
├── conftest.py              # Configurazioni pytest globali
├── test_cli.py             # Test interfaccia CLI
├── test_cli_extended.py    # Test CLI avanzati
├── test_config.py          # Test configurazione
├── test_dataloader.py      # Test caricamento dati
├── test_retriever.py       # Test ricerca semantica
├── test_runner.py          # Test engine principale
├── test_security.py        # Test sicurezza
├── test_server.py          # Test API server
├── test_server_medical.py  # Test moduli medici
├── test_translate.py       # Test traduzione
└── test_validation.py      # Test validazione input
```

## 🚀 Esecuzione Test

### Test Completi
```bash
# Esegui tutta la suite di test
pytest

# Test con output verboso
pytest -v

# Test con coverage report
pytest --cov=sigma_nex --cov-report=html
```

### Test Specifici
```bash
# Test di un singolo modulo
pytest tests/test_runner.py -v

# Test di una singola classe
pytest tests/test_runner.py::TestContextBuilding -v

# Test con keyword filter
pytest -k "test_security" -v
```

### Test Task (Raccomandato)
```bash
# Usa i task predefiniti
sigma-nex> Run pytest now
sigma-nex> Run tests with coverage 95%
```

## 📋 Categorie di Test

### 🔧 Unit Test
- **Runner**: Test engine di esecuzione
- **Context**: Test costruzione prompt
- **Retriever**: Test ricerca semantica FAISS
- **Validation**: Test sanitizzazione input
- **Security**: Test crittografia e accessi

### 🌐 Integration Test
- **CLI**: Test interfaccia a riga di comando
- **Server**: Test API REST endpoints
- **Translation**: Test pipeline multilingue
- **Data Loader**: Test caricamento framework

### 🛡️ Security Test
- **Input Validation**: SQL injection, XSS, path traversal
- **Authentication**: Token validation, rate limiting
- **Encryption**: Test algoritmi crittografici
- **Access Control**: Verifica permessi

### 🏥 Medical Test
- **Medical Models**: Test modelli specializzati
- **Emergency Protocols**: Test procedure critiche
- **Drug Interactions**: Test interazioni farmaci

## 🎯 Test Guidelines

### Writing Test
```python
import pytest
from sigma_nex.core.runner import Runner

class TestRunner:
    def test_basic_functionality(self):
        """Test delle funzionalità base."""
        runner = Runner({'model_name': 'test'})
        result = runner.process_query("test query")
        assert result is not None
        
    def test_error_handling(self):
        """Test gestione errori."""
        with pytest.raises(ValidationError):
            invalid_operation()
```

### Test Conventions
- **Naming**: `test_<functionality>_<scenario>`
- **Structure**: Arrange, Act, Assert
- **Isolation**: Ogni test deve essere indipendente
- **Mocking**: Usa mock per dipendenze esterne

### Test Data
```python
# Fixtures per dati di test
@pytest.fixture
def sample_config():
    return {
        'model_name': 'mistral',
        'temperature': 0.7,
        'max_tokens': 2048
    }

@pytest.fixture
def mock_ollama_response():
    return {
        "response": "Test response",
        "done": True
    }
```

## 🔍 Debugging Test

### Test Failures
```bash
# Debug con pdb
pytest --pdb

# Mostra traceback completo
pytest --tb=long

# Ferma al primo errore
pytest -x
```

### Performance Testing
```bash
# Test con profiling
pytest --profile

# Test con timing
pytest --durations=10
```

## ⚡ Continuous Integration

### GitHub Actions
I test vengono eseguiti automaticamente su:
- **Push su master**
- **Pull Request**
- **Release tags**

### Test Matrix
- **Python**: 3.10, 3.11, 3.12
- **OS**: Ubuntu, Windows, macOS
- **Dependencies**: Latest stable versions

### Coverage Requirements
- **Minimum**: 60% line coverage
- **Target**: 80% line coverage
- **Critical paths**: 95% coverage obbligatorio

## 🛠️ Test Tools

### Pytest Plugins
```bash
pip install pytest-cov pytest-mock pytest-xdist pytest-html
```

### Code Quality
```bash
# Linting
flake8 sigma_nex/
pylint sigma_nex/

# Type checking
mypy sigma_nex/

# Security scanning
bandit -r sigma_nex/
```

## 📈 Test Reporting

### HTML Report
```bash
pytest --cov=sigma_nex --cov-report=html
# Genera htmlcov/index.html
```

### Coverage Badge
```markdown
![Coverage](https://img.shields.io/badge/Coverage-60%25-yellow?style=for-the-badge)
```

### Performance Metrics
- **Average test time**: <2s per test
- **Total suite time**: <60s
- **Memory usage**: <500MB durante test

## 🔄 Test Best Practices

### 1. Test Pyramid
- **70% Unit Tests**: Logica business core
- **20% Integration Tests**: Interazioni tra moduli  
- **10% E2E Tests**: Workflow completi

### 2. Test Scenarios
- **Happy Path**: Scenari di successo
- **Edge Cases**: Casi limite e boundary
- **Error Handling**: Gestione errori e eccezioni
- **Performance**: Load testing e stress testing

### 3. Test Environment
```yaml
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --strict-markers --disable-warnings
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    security: marks tests as security tests
```

## 🚨 Emergency Testing

### Critical Path Testing
```bash
# Test componenti critici prima del deploy
pytest tests/test_runner.py tests/test_security.py -v
```

### Smoke Testing
```bash
# Test base per verificare che il sistema sia funzionante
pytest tests/test_cli.py::test_basic_cli tests/test_server.py::test_health_check
```

---

**Autore**: Martin Sebastian  
**Versione**: 0.2.1  
**Ultimo aggiornamento**: 23 Settembre 2025