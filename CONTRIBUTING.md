# Contributing to SIGMA-NEX

<div align="center">

![Contributing](https://img.shields.io/badge/Contributing-Guide-blue?style=for-the-badge)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)
![First Timers](https://img.shields.io/badge/first--timers--friendly-blue?style=for-the-badge)

**Grazie per il tuo interesse nel contribuire a SIGMA-NEX!**

</div>

---

## 📋 Indice

- [🚀 Come Iniziare](#-come-iniziare)
- [💡 Tipi di Contributi](#-tipi-di-contributi)
- [🔄 Processo di Sviluppo](#-processo-di-sviluppo)
- [📝 Standard di Codice](#-standard-di-codice)
- [🧪 Testing](#-testing)
- [📚 Documentazione](#-documentazione)
- [🔒 Sicurezza](#-sicurezza)
- [🎯 Linee Guida per le Pull Request](#-linee-guida-per-le-pull-request)

## 🚀 Come Iniziare

### 1. Preparazione Ambiente

```bash
# Fork e clona il repository
git clone https://github.com/YOUR_USERNAME/sigma-nex.git
cd sigma-nex

# Crea un branch per il tuo lavoro
git checkout -b feature/my-awesome-feature

# Setup ambiente di sviluppo
pip install -e ".[dev]"
pre-commit install
```

### 2. Verifica Setup

```bash
# Esegui test per verificare tutto funzioni
pytest

# Verifica linting
black --check sigma_nex/
flake8 sigma_nex/
```

### 3. Trova un Task

- 🔍 Controlla le [Issues](https://github.com/sigma-nex/sigma-nex/issues) con label `good first issue`
- 💡 Leggi le [Discussioni](https://github.com/sigma-nex/sigma-nex/discussions) per idee
- 🐛 Segnala bug o richiedi funzionalità

## 💡 Tipi di Contributi

### 🐛 Bug Fixes
- Correzioni di bug nel codice esistente
- Miglioramenti alla stabilità del sistema
- Fix di sicurezza

### ✨ Nuove Funzionalità
- Implementazione di nuove caratteristiche
- Miglioramenti all'interfaccia utente
- Estensioni dell'API

### 📚 Documentazione
- Miglioramenti alla documentazione
- Guide per l'utente
- Esempi di utilizzo

### 🧪 Testing
- Nuovi test case
- Miglioramenti alla copertura
- Test di integrazione

### 🔧 Tooling
- Miglioramenti al build system
- Nuovi script di automazione
- Configurazioni CI/CD

## 🔄 Processo di Sviluppo

### 1. Scegli un Task
- Assegna a te stesso l'issue su GitHub
- Discuti l'approccio nei commenti se necessario

### 2. Sviluppo (TDD - Test Driven Development)
```bash
# 1. Scrivi test prima del codice
# tests/test_my_feature.py
def test_my_new_feature():
    assert my_function() == expected_result

# 2. Implementa la funzionalità
# sigma_nex/my_feature.py
def my_function():
    return "implementation"

# 3. Verifica che i test passino
pytest tests/test_my_feature.py
```

### 3. Code Quality
```bash
# Formattazione automatica
black sigma_nex/
isort sigma_nex/

# Linting
flake8 sigma_nex/

# Type checking (opzionale)
mypy sigma_nex/
```

### 4. Commit
```bash
# Usa conventional commits
git add .
git commit -m "feat: add amazing new feature

- Add feature X
- Fix issue Y
- Update documentation Z"
```

### 5. Push e Pull Request
```bash
git push origin feature/my-awesome-feature
# Crea PR su GitHub
```

## 📝 Standard di Codice

### Python Style Guide
Seguiamo [PEP 8](https://pep8.org/) con alcune personalizzazioni:

- **Linee massime**: 88 caratteri (Black default)
- **Quotes**: Preferisci double quotes `"` per stringhe
- **Imports**: Organizzati con `isort`
- **Type Hints**: Richiesti per tutte le funzioni pubbliche

### Esempi di Codice

```python
# ✅ Bene
def process_query(query: str, user_id: Optional[int] = None) -> Dict[str, Any]:
    """Processa una query dell'utente.

    Args:
        query: La domanda dell'utente
        user_id: ID utente opzionale

    Returns:
        Dizionario con risposta e metadati
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")

    result = {
        "response": "Risposta elaborata",
        "timestamp": datetime.now(),
        "user_id": user_id
    }

    return result

# ❌ Male
def process_query(query,user_id=None):  # Manca spazi, type hints
    if not query:  # Non gestisce stringhe vuote correttamente
        return "error"
    return {"response":"ok"}  # Non documentato
```

### Naming Conventions

- **Classi**: `PascalCase` (es. `SigmaConfig`)
- **Funzioni**: `snake_case` (es. `process_query`)
- **Variabili**: `snake_case` (es. `user_input`)
- **Costanti**: `UPPER_CASE` (es. `MAX_TOKENS`)
- **File**: `snake_case.py` (es. `data_loader.py`)

## 🧪 Testing

### Requisiti di Testing
- **Coverage minima**: 95% per tutto il codice
- **Tipi di test**: Unit, Integration, E2E
- **Framework**: pytest con pytest-cov

### Struttura dei Test
```
tests/
├── __init__.py
├── conftest.py              # Configurazioni condivise
├── test_cli.py             # Test CLI
├── test_config.py          # Test configurazione
├── test_runner.py          # Test core engine
├── test_server.py         # Test API server
└── test_retriever.py       # Test ricerca semantica
```

### Scrivere Buoni Test

```python
import pytest
from sigma_nex.core.runner import Runner

class TestRunner:
    def test_process_query_success(self):
        """Test elaborazione query riuscita."""
        config = {"model_name": "mistral"}
        runner = Runner(config)

        result = runner.process_query("Test query")

        assert "response" in result
        assert isinstance(result["response"], str)
        assert result["processing_time"] > 0

    def test_process_query_empty_input(self):
        """Test gestione input vuoto."""
        config = {"model_name": "mistral"}
        runner = Runner(config)

        with pytest.raises(ValueError, match="Query cannot be empty"):
            runner.process_query("")

    @pytest.mark.parametrize("query,expected_contains", [
        ("acqua", "purificazione"),
        ("ferita", "disinfezione"),
        ("fuoco", "sicurezza")
    ])
    def test_medical_queries(self, query, expected_contains):
        """Test risposte a query mediche."""
        config = {"model_name": "mistral"}
        runner = Runner(config)

        result = runner.process_query(query)

        assert expected_contains.lower() in result["response"].lower()
```

### Eseguire i Test

```bash
# Tutti i test
pytest

# Test specifici
pytest tests/test_cli.py::TestCLI::test_start_command

# Con coverage
pytest --cov=sigma_nex --cov-report=html

# Test lenti solo
pytest -m slow

# Debug mode
pytest -v -s --pdb
```

## 📚 Documentazione

### Requisiti Documentazione
- **Docstrings**: Tutte le funzioni pubbliche devono avere docstring completa
- **Type Hints**: Richiesti per parametri e return values
- **Esempi**: Codice di esempio dove appropriato

### Formato Docstring

```python
def complex_function(
    param1: str,
    param2: Optional[int] = None,
    *,
    keyword_only: bool = False
) -> Dict[str, Any]:
    """Riepilogo breve e descrittivo della funzione.

    Descrizione più dettagliata se necessaria. Spiega cosa fa
    la funzione, eventuali side effects, e considerazioni importanti.

    Args:
        param1: Descrizione del primo parametro obbligatorio.
        param2: Descrizione del secondo parametro opzionale.
        keyword_only: Parametro solo keyword per...

    Returns:
        Descrizione di cosa viene restituito.

    Raises:
        ValueError: Quando l'input è invalido.
        ConnectionError: Quando non riesce a connettersi.

    Examples:
        >>> result = complex_function("test", param2=42)
        >>> print(result["status"])
        success

    Note:
        Considerazioni aggiuntive o avvertenze.
    """
```

### Aggiornamento Documentazione
- Aggiorna `README.md` per nuove funzionalità
- Aggiorna `docs/api.md` per nuovi endpoint
- Aggiorna `CHANGELOG.md` per ogni release

## 🔒 Sicurezza

### Considerazioni di Sicurezza
- **Input Validation**: Sempre valida e sanitizza input utente
- **No Secrets**: Non committare mai chiavi API o segreti
- **Dependencies**: Controlla regolarmente vulnerabilità
- **Access Control**: Implementa controlli appropriati

### Security Checklist
- [ ] Input sanitizzato e validato
- [ ] No SQL injection possibili
- [ ] No XSS in output web
- [ ] Headers di sicurezza appropriati
- [ ] Rate limiting implementato
- [ ] Logging sicuro (no dati sensibili)
- [ ] Dependencies aggiornate

### Segnalare Vulnerabilità
- **NON** aprire issue pubbliche per vulnerabilità di sicurezza
- Invia email a: rootedlab6@gmail.com
- Include dettagli completi e proof-of-concept

## 🎯 Linee Guida per le Pull Request

### Template PR
```markdown
## Descrizione
Breve descrizione delle modifiche.

## Tipo di Cambiamento
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 💥 Breaking change
- [ ] 📚 Documentation
- [ ] 🎨 Style
- [ ] 🔧 Refactoring

## Testing
- [ ] Test aggiunti/aggiornati
- [ ] Coverage >= 95%
- [ ] Test manuali effettuati

## Checklist
- [ ] Code style corretto (Black, isort)
- [ ] Linting passa (flake8)
- [ ] Documentazione aggiornata
- [ ] Breaking changes documentati
- [ ] Migration guide se necessario
```

### Review Process
1. **Automated Checks**: CI deve passare
2. **Code Review**: Almeno un maintainer deve approvare
3. **Testing**: Tutti i test devono passare
4. **Documentation**: Docs aggiornate se necessario

### Merge Requirements
- ✅ CI verde
- ✅ Approvazione di almeno 1 maintainer
- ✅ Tutti i test passano
- ✅ Nessun conflitto
- ✅ Branch aggiornato con main

## 🎉 Riconoscimenti

Grazie per contribuire a SIGMA-NEX! Il tuo lavoro aiuta a rendere l'AI offline-first più accessibile e sicura per tutti.

### Premi per Contributori
- 🏆 **First PR**: Badge "First Contributor"
- 🌟 **10 PRs**: Badge "Active Contributor"
- 👑 **50 PRs**: Badge "Core Contributor"
- 🐛 **Bug Hunter**: Per chi trova e fixa bug critici
- 📚 **Documentation Hero**: Per miglioramenti significativi alla docs

### Comunità
- 💬 [GitHub Discussions](https://github.com/sigma-nex/sigma-nex/discussions)
- 👥 [Discord Server](https://discord.gg/sigma-nex)
- 📧 Newsletter mensile per aggiornamenti

---

<div align="center">

**Domande?** [Apri una discussione](https://github.com/sigma-nex/sigma-nex/discussions) • **Problemi?** [Segnala un bug](https://github.com/sigma-nex/sigma-nex/issues)

</div>