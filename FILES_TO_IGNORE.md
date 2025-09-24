# Repository Cleanup - Files Rimossi per Versione Professionale

Questo documento elenca i file che sono stati rimossi dal repository per mantenere una struttura pulita e professionale.

## ✅ **File Rimossi - Completato**

### Script di Test Temporanei (RIMOSSI ✅)
- ~~`test_basic.py`~~ - Rimosso: file di test temporaneo
- ~~`marian_test.py`~~ - Rimosso: test sperimentale traduzione
- ~~`MARIANDWND.py`~~ - Rimosso: file di test non documentato
- ~~`faiss.py`~~ - Rimosso: script di test FAISS standalone
- ~~`text_translate.py`~~ - Rimosso: test traduzione temporaneo

### Script di Build/Setup Locali (RIMOSSI ✅)
- ~~`build_index.py`~~ - Rimosso: script build locale
- ~~`build_index1.py`~~ - Rimosso: script build duplicato
- ~~`setup_dev.bat`~~ - Rimosso: setup Windows locale  
- ~~`venvesetup.bat`~~ - Rimosso: setup venv locale
- ~~`cleanup.bat`~~ - Rimosso: script cleanup locale
- ~~`avvia_gui.bat`~~ - Rimosso: launcher Windows locale

### File di Coverage/Config Duplicati (RIMOSSI ✅)
- ~~`.coverage`~~ - Rimosso: file di coverage locale
- ~~`pytest-simple.ini`~~ - Rimosso: config pytest duplicata
- ~~`config.production.yaml`~~ - Rimosso: config non utilizzata
- ~~`.pre-commit-config.yaml`~~ - Rimosso: config pre-commit non necessaria

### File di Test Obsoleti (RIMOSSI ✅)
- ~~`tests/test_server_medical.py`~~ - Rimosso: test medico obsoleto
- ~~`tests/test_validation.py`~~ - Rimosso: sostituito con versione realistica

### File di Data Duplicati (RIMOSSI ✅)
- ~~`data/Framework_SIGMA1.json`~~ - Rimosso: dataset duplicato

## File di Output e Cache

### Report di Coverage
- `htmlcov/` (directory completa)
- `coverage.xml`
- `test_coverage_report.json`

### Log Files
- `logs/` (directory completa)
- `sigma_nex_api.log`
- `*.log`

### Cache Python
- `__pycache__/` (directory completa)
- `*.pyc`
- `*.pyo`
- `*.pyd`
- `sigma_nex.egg-info/` (directory completa)

## File di Configurazione Locale

### Ambienti Virtuali
- `venv/` (directory completa)
- `.venv/`
- `ENV/`

### File di Configurazione Sensibili
- `config.production.yaml` (se contiene dati sensibili)
- `.env`
- `.env.local`
- `.env.production`

## File Temporanei e di Sviluppo

### File Temporanei
- `temp/`
- `tmp/`
- `*.tmp`
- `*.bak`
- `*.patch`

### File di Backup
- `*.backup`
- `backup/`

### File Specifici del Progetto
- File con nomi non standard come:
  - `1234567890'ì+.txt`
  - `Nuovo Documento di testo.txt`
  - `*- Copia.py`
  - `*0.1.py`
  - `*2.py`

## File di Sistema

### Windows
- `Thumbs.db`
- `*.lnk`

### macOS
- `.DS_Store`
- `.DS_Store?`
- `._*`
- `.Spotlight-V100`
- `.Trashes`

### Linux
- `*~`
- `.directory`

## Dati e Indici

### Indici FAISS (Grandi file binari)
- `data/moduli.index`
- `data/moduli.mapping.json`
- `*.index`
- `*.faiss`

### Modelli ML (Se presenti)
- `models/`
- `checkpoints/`
- `*.bin`
- `*.safetensors`
- `*.pt`
- `*.pth`
- `sigma_nex/core/models/` (se contiene modelli binari)

## IDE e Editor

### Visual Studio Code
- `.vscode/` (settings locali)

### PyCharm/IntelliJ
- `.idea/`

### Vim/Emacs
- `*.swp`
- `*.swo`

## Note Importanti

1. **Il file .gitignore è già configurato** per ignorare automaticamente tutti questi file
2. **Verificare sempre** che non ci siano dati sensibili nei file di configurazione prima del commit
3. **I file di documentazione sono stati aggiornati** per riflettere lo stato attuale del progetto
4. **La documentazione è ora professionale** senza emoji eccessive
5. **La versione corrente è 0.2.1** come specificato in pyproject.toml

## Comando per Verificare Status Git

```bash
# Verifica lo status prima del commit
git status

# Verifica cosa sarà incluso nel commit
git add . --dry-run

# Verifica le differenze
git diff --cached
```

## File da Includere Assolutamente

I seguenti file DEVONO essere inclusi nel repository:

- `README.md` (aggiornato)
- `pyproject.toml`
- `requirements.txt`
- `requirements-test.txt`
- `sigma_nex/` (directory completa del codice)
- `tests/` (directory completa dei test)
- `docs/` (documentazione completa)
- `data/Framework_SIGMA.json` e `data/Framework_SIGMA1.json`
- `config.yaml` (configurazione base senza dati sensibili)
- `LICENSE`
- `CHANGELOG.md`
- `AUTHORS.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `scripts/` (se contiene script utili per gli utenti)
- `docker-compose.yml` e `docker-compose.dev.yml`
- `Dockerfile`
- `docker-entrypoint.sh`
- `.gitignore` (aggiornato)

Ultimo aggiornamento: 24 Settembre 2025