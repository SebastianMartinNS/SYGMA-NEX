# 🚀 SIGMA-NEX CI/CD System

Questo documento descrive il sistema CI/CD professionale implementato per SIGMA-NEX.

## 📋 Overview

Il sistema CI/CD è composto da due workflow principali:

1. **🧪 CI/CD Pipeline** (`ci.yml`) - Pipeline principale per test e build
2. **🎯 Code Quality** (`quality.yml`) - Miglioramento graduale della qualità del codice

## 🧪 CI/CD Pipeline Principale

### Trigger
- Push su `master` e `develop`
- Pull Request verso `master` e `develop`
- Tag `v*` per release

### Jobs

#### 🔍 Pre-checks
- **Code Formatting**: Black (warnings only)
- **Import Sorting**: isort (warnings only)
- **Linting**: flake8 (warnings only)
- **Type Checking**: mypy (warnings only)
- **Security Scan**: Bandit (warnings only)
- **Vulnerability Check**: Safety (warnings only)

> ⚠️ **Nota**: I pre-check sono configurati come warnings per non bloccare lo sviluppo. Utilizzare il workflow Quality per miglioramenti.

#### 🧪 Tests
- **Unit Tests**: Test delle funzionalità core (`tests/unit/`)
- **Integration Tests**: Test di integrazione (`tests/integration/`)
- **Matrix Testing**: Python 3.10, 3.11, 3.12
- **Coverage**: Report automatico su Codecov

#### 🚀 Performance Tests
- **Benchmark Tests**: Test delle performance (`tests/performance/`)
- **Memory Usage**: Controllo uso memoria
- **Response Time**: Misurazione tempi di risposta

#### 🐳 Docker
- **Build**: Costruzione immagine Docker
- **Test**: Verifica funzionamento container
- **Push**: Pubblicazione su GitHub Container Registry (solo per branch principali)

#### 📄 Documentation
- **Build**: Generazione documentazione Sphinx
- **Deploy**: Pubblicazione su GitHub Pages (solo branch `master`)

#### 🏷️ Release (solo per tag)
- **Package Build**: Creazione pacchetti Python
- **GitHub Release**: Creazione release automatica
- **PyPI**: Pubblicazione pacchetto (richiede `PYPI_API_TOKEN`)

### 📊 Quality Gate

La pipeline ha un sistema di Quality Gate intelligente:

#### ✅ Criteri di Successo
- **Tests**: Tutti i test unitari devono passare
- **Docker**: Build deve completarsi con successo
- **Integration**: Test di integrazione devono passare

#### ⚠️ Warnings (non bloccanti)
- **Code Quality**: Problemi di formattazione/linting
- **Performance**: Test delle performance falliti
- **Security**: Vulnerability warnings

## 🎯 Code Quality Workflow

### Trigger
- **Manual**: Workflow dispatch con opzioni
- **Scheduled**: Lunedì alle 2:00 AM (settimanale)

### Funzionalità

#### 🔧 Assessment
- Analisi completa della qualità del codice
- Report dettagliato dei problemi
- Metriche di qualità

#### 🛠️ Auto-fix
- **Formatting**: Applicazione automatica Black
- **Imports**: Sorting automatico con isort
- **Basic Linting**: Fix automatico problemi base
- **Commit automatico**: Push delle correzioni

#### 📊 Metrics
- Statistiche dettagliate
- Tracking dei miglioramenti
- Report di qualità

### Utilizzo

```bash
# Manuale via GitHub UI
# 1. Vai su Actions → Code Quality Improvement
# 2. Clicca "Run workflow"
# 3. Seleziona il tipo di fix desiderato

# Oppure via CLI GitHub
gh workflow run quality.yml -f fix_type=all
```

## 🔧 Setup e Configurazione

### Secrets Richiesti

#### GitHub Repository Secrets
```bash
# Per pubblicazione PyPI (opzionale)
PYPI_API_TOKEN=pypi-token-here

# Per notifiche Discord (opzionale)
DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
```

### File di Configurazione

#### `requirements-test.txt`
```
# Test dependencies
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-benchmark>=4.0.0

# Code quality tools
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.5.0
bandit>=1.7.5
safety>=2.3.5
```

#### `pytest.ini`
```ini
[tool:pytest]
minversion = 7.0
addopts = -ra --strict-markers --cov=sigma_nex
testpaths = tests
markers =
    unit: unit tests
    integration: integration tests
    performance: performance tests
```

## 📈 Strategia di Miglioramento

### Fase 1: Stabilizzazione (Attuale)
- ✅ Pipeline CI/CD funzionante
- ✅ Test automatici
- ✅ Docker build
- ⚠️ Code quality warnings (non bloccanti)

### Fase 2: Qualità Graduale
- 🎯 Fix automatico problemi formattazione
- 🎯 Miglioramento import sorting
- 🎯 Risoluzione problemi linting base

### Fase 3: Excellence
- 🎯 Type annotations complete
- 🎯 100% test coverage
- 🎯 Zero security warnings
- 🎯 Performance optimizations

## 🚨 Troubleshooting

### Pipeline Fails

#### Test Failures
```bash
# Run tests locally
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
```

#### Docker Build Issues
```bash
# Test Docker build locally
docker build -t sigma-nex-test .
docker run --rm sigma-nex-test sigma self-check
```

#### Dependency Issues
```bash
# Update dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
pip install -e .
```

### Quality Issues

#### Format Code
```bash
# Fix formatting
black sigma_nex tests

# Fix imports
isort sigma_nex tests

# Check linting
flake8 sigma_nex tests --max-line-length=88
```

#### Run Quality Workflow
1. Vai su GitHub Actions
2. Seleziona "Code Quality Improvement"
3. Run workflow con opzione "all"

## 📞 Support

Per problemi con CI/CD:

1. **Check Actions**: Verifica i log in GitHub Actions
2. **Local Testing**: Replica il problema localmente
3. **Quality Workflow**: Usa il workflow di qualità per auto-fix
4. **Documentation**: Consulta questo README

## 🎯 Best Practices

### Commits
- Usa commit semantici: `feat:`, `fix:`, `docs:`, `style:`, ecc.
- Test localmente prima del push
- Mantieni commit atomici e focalizzati

### Pull Requests
- Aspetta che tutti i test passino
- Ignora warnings di code quality (verranno risolti gradualmente)
- Assicurati che la funzionalità core funzioni

### Releases
- Usa semantic versioning: `v1.0.0`, `v1.0.1`, ecc.
- Aggiorna CHANGELOG.md prima del tag
- Verifica che tutti i test passino prima del tag

---

**🚀 SIGMA-NEX - Sistema di CI/CD Professionale e Scalabile**