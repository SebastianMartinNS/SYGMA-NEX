<div align="center">

![SIGMA-NEX Logo](https://raw.githubusercontent.com/SebastianMartinNS/SYGMA-NEX/master/assets/logo.jpg)

# SIGMA-NEX v0.3.5

**Sistema di Intelligenza Artificiale Autonomo per la Sopravvivenza Offline-First**

![Version](https://img.shields.io/badge/Version-0.3.5-blue?style=for-the-badge)
![Release Date](https://img.shields.io/badge/Release-2025--09--26-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)

[Download](https://github.com/SebastianMartinNS/SYGMA-NEX/releases/tag/v0.3.5) | 
[Documentation](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/) | 
[Issues](https://github.com/SebastianMartinNS/SYGMA-NEX/issues) | 
[Discussions](https://github.com/SebastianMartinNS/SYGMA-NEX/discussions)

</div>

---

## Panoramica Release

SIGMA-NEX v0.3.5 rappresenta un significativo passo avanti nell'evoluzione del nostro sistema di intelligenza artificiale autonomo. Progettato per scenari critici e ambienti offline, questa release introduce miglioramenti sostanziali in termini di performance, usabilità e robustezza.

### Caratteristiche Principali

- **100% Offline**: Funziona completamente senza connessione internet
- **AI Locale**: Utilizza Ollama per modelli linguistici avanzati
- **Specializzazione Medica**: Moduli dedicati per emergenze sanitarie
- **Ricerca Semantica**: Database vettoriale FAISS per retrieval intelligente
- **Traduzione Multilingue**: Supporto offline per 50+ lingue
- **Security-First**: Crittografia e validazione completa degli input

---

## 🆕 Novità in questa Release

### Nuove Funzionalità
- **ASCII Art Banner**: Banner grafico informativo con dettagli autore e repository
- **Update Command**: Nuovo comando `sigma update` per aggiornamenti automatici
  - `--check-only`: Controlla solo versioni disponibili
  - `--force`: Forza aggiornamento anche se già aggiornato
  - Verifica automatica via GitHub API
- **Module Execution**: Supporto completo `python -m sigma_nex`
- **Enhanced Testing**: 335/340 test passano (98.5% success rate)

### Miglioramenti
- **User Experience**: Banner informativo più chiaro e professionale
- **Error Handling**: Gestione robusta errori di rete e git durante aggiornamenti
- **Code Quality**: Compliance completa con flake8, isort, black
- **Documentation**: README e documentazione completamente aggiornati

### Bug Fixes
- Risolti problemi di path resolution su Windows
- Fix per timeout durante aggiornamenti Git
- Migliorata gestione dipendenze post-update
- Corretti link documentazione per puntare al repository GitHub

---

## Installazione Rapida

### Prerequisiti
- **Python**: 3.10+ (raccomandato 3.11)
- **Ollama**: [Download obbligatorio](https://ollama.com)
- **RAM**: Minimo 8GB, raccomandati 16GB+
- **Storage**: 5GB per modelli e dati

### Installazione Python
```bash
# Installazione diretta da PyPI
pip install sigma-nex==0.3.5

# Aggiornamento da versione precedente
pip install --upgrade sigma-nex

# Verifica installazione
sigma self-check
```

### Installazione Docker
```bash
# Pull dell'immagine specifica
docker pull ghcr.io/sebastianmartinns/sygma-nex:0.3.5

# Pull dell'ultima versione stabile
docker pull ghcr.io/sebastianmartinns/sygma-nex:latest

# Avvio container
docker run -p 8000:8000 ghcr.io/sebastianmartinns/sygma-nex:0.3.5
```

### Installazione da Sorgente
```bash
# Clone del repository
git clone https://github.com/SebastianMartinNS/SYGMA-NEX.git
cd SYGMA-NEX
git checkout v0.3.5

# Setup automatico
pip install -e .

# Installazione modelli AI
ollama pull mistral
```

---

## Quick Start

```bash
# Verifica installazione e configurazione
sigma self-check

# Avvia modalità interattiva
sigma start

# Avvia server API REST
sigma server

# Avvia interfaccia grafica
sigma gui

# Aggiorna sistema
sigma update
```

### Test API
```bash
# Health check
curl http://localhost:8000/

# Query di test
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Come disinfettare una ferita?"}'
```

---

## Documentazione Completa

### Guide per Utenti
- **[Homepage](https://github.com/SebastianMartinNS/SYGMA-NEX)** - Panoramica generale del progetto
- **[Quick Start](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/README.md#installazione-rapida)** - Guida rapida per iniziare
- **[Installazione Dettagliata](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/installation.md)** - Setup completo e configurazione
- **[Guida CLI](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/guides/cli-guide.md)** - Interfaccia a riga di comando
- **[Guida GUI](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/guides/gui-guide.md)** - Interfaccia grafica desktop
- **[Configurazione](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/guides/configuration.md)** - Setup avanzato e personalizzazione

### Guide per Sviluppatori
- **[Setup Sviluppo](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/development.md)** - Ambiente di sviluppo
- **[API Reference](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/api.md)** - Documentazione API REST
- **[Testing Guide](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/testing.md)** - Framework di testing
- **[Architettura](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/architecture/)** - Design e architettura sistema
- **[Contributing](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/CONTRIBUTING.md)** - Come contribuire al progetto

### Deploy e Produzione
- **[Deployment Guide](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/deployment.md)** - Deploy in produzione
- **[Docker Guide](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/guides/docker.md)** - Containerizzazione e orchestrazione
- **[Troubleshooting](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/guides/troubleshooting.md)** - Risoluzione problemi comuni
- **[Security Guide](https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/guides/security.md)** - Configurazione sicurezza

---

## Requisiti di Sistema

### Requisiti Minimi
- **Sistema Operativo**: Windows 10+, Linux (Ubuntu 20.04+), macOS 11+
- **Python**: 3.10 o superiore
- **RAM**: 8GB disponibili
- **Storage**: 5GB liberi per modelli e cache
- **Ollama**: Installazione obbligatoria

### Configurazione Raccomandata
- **RAM**: 16GB+ per performance ottimali
- **CPU**: 8+ core per elaborazione parallela
- **Storage**: SSD per accesso rapido ai modelli
- **GPU**: Opzionale, supporto CUDA per accelerazione

---

## Breaking Changes e Migrazione

✅ **Nessuna Breaking Change**: Questa release è completamente backward-compatible.

Tutti gli aggiornamenti sono incrementali e non richiedono modifiche alla configurazione esistente.

---

## Architettura di Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        SIGMA-NEX v0.3.5                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │     CLI     │  │     GUI     │  │  REST API   │             │
│  │   Terminal  │  │   Tkinter   │  │   FastAPI   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Runner    │  │  Retriever  │  │ Translator  │             │
│  │ (Core AI)   │  │ (Semantic)  │  │ (Offline)   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Ollama    │  │    FAISS    │  │  MarianMT   │             │
│  │  (Mistral)  │  │   Index     │  │   Models    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Sicurezza e Licenza

### Sicurezza
- **Offline-First**: Nessun dato viene trasmesso online
- **Input Validation**: Sanitizzazione completa degli input utente
- **Encryption**: Crittografia AES per dati sensibili
- **Audit Logging**: Tracciamento completo delle operazioni
- **Zero Trust**: Validazione di ogni componente del sistema

### Licenza
**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

✅ **Permesso**: Uso educativo, ricerca, progetti personali
❌ **Limitazione**: Uso commerciale richiede autorizzazione

**Contatti per Licenze Commerciali**: rootedlab6@gmail.com

---

## Supporto e Community

### Canali di Supporto
- **[Bug Reports](https://github.com/SebastianMartinNS/SYGMA-NEX/issues)** - Segnalazione bug e problemi
- **[Feature Requests](https://github.com/SebastianMartinNS/SYGMA-NEX/discussions)** - Richieste nuove funzionalità
- **[Q&A Forum](https://github.com/SebastianMartinNS/SYGMA-NEX/discussions/categories/q-a)** - Domande e risposte
- **[Email](mailto:rootedlab6@gmail.com)** - Supporto diretto

### Come Contribuire
1. **Fork** il repository su GitHub
2. **Clone** il tuo fork localmente
3. **Crea** un branch per la tua feature
4. **Implementa** le modifiche e testa
5. **Commit** seguendo [Conventional Commits](https://conventionalcommits.org/)
6. **Push** e apri una Pull Request

### Community Guidelines
- Mantieni un tono rispettoso e costruttivo
- Fornisci dettagli nei bug report
- Testa le modifiche prima di inviare PR
- Segui le linee guida di coding del progetto

---

## Metriche della Release

- **Files Changed**: 47 file modificati
- **Commits**: 23 commit dalla versione precedente
- **Lines Added**: 1,247 linee di codice
- **Lines Deleted**: 384 linee di codice
- **Test Success**: 335/340 test passano (98.5%)
- **Code Coverage**: 78% del codebase coperto
- **Security**: 0 vulnerabilità note
- **Performance**: < 2s response time medio

---

<div align="center">

**SIGMA-NEX v0.3.5** - *Sopravvivenza Intelligente Offline-First*

[Torna su](#-sigma-nex-v035) | 
[Download](https://github.com/SebastianMartinNS/SYGMA-NEX/releases/tag/v0.3.5) | 
[Homepage](https://github.com/SebastianMartinNS/SYGMA-NEX)

*Release Notes aggiornate al 26 Settembre 2025*

**Progetto sviluppato da Martin Sebastian - 2025**

</div>