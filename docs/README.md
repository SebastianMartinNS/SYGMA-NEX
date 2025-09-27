<div align="center">

![SIGMA-NEX Logo](../assets/logo.jpg)

# Documentazione SIGMA-NEX

Benvenuto nella documentazione completa di SIGMA-NEX, il Sistema di Intelligenza Artificiale Autonomo per la Sopravvivenza Offline-First.

</div>

## Indice

- [Quick Start](#quick-start)
- [Guide](#guide)
- [API Reference](#api-reference)
- [Architettura](#architettura)
- [Configurazione](#configurazione)
- [Testing](#testing)
- [Contribuire](#contribuire)
- [Sicurezza](#sicurezza)

## Quick Start

### Installazione Rapida

```bash
# Metodo 1: Sorgente (attuale)
git clone https://github.com/SebastianMartinNS/SYGMA-NEX.git
cd SYGMA-NEX
pip install -e .

# Metodo 2: Docker (in sviluppo)
git clone https://github.com/SebastianMartinNS/SYGMA-NEX.git
cd SYGMA-NEX
pip install -e .
```

### Primo Utilizzo

```bash
# Verifica installazione
sigma self-check

# Modalità interattiva
sigma start

# Avvia server API
sigma server

# Interfaccia grafica
sigma gui

# Aggiornamento sistema
sigma update --check-only  # Solo controllo
sigma update               # Aggiorna alla versione più recente

# Esecuzione come modulo
python -m sigma_nex --help
```

## Guide

### Guide Utente

1. **[Guida Installazione](installation.md)** - Installazione dettagliata per tutti i sistemi operativi
2. **[Configurazione Base](guides/configuration.md)** - Configurazione iniziale e personalizzazione
3. **[Utilizzo CLI](guides/cli-guide.md)** - Guida completa all'interfaccia a riga di comando
4. **[Utilizzo GUI](guides/gui-guide.md)** - Guida all'interfaccia grafica
5. **[API Usage](guides/api-usage.md)** - Come utilizzare l'API REST
6. **[Troubleshooting](guides/troubleshooting.md)** - Risoluzione problemi comuni

### Guide Sviluppatore

1. **[Development Setup](development.md)** - Configurazione ambiente di sviluppo
2. **[Architecture Overview](architecture/overview.md)** - Panoramica dell'architettura del sistema
3. **[Contributing Guidelines](../CONTRIBUTING.md)** - Come contribuire al progetto
4. **[Testing Guide](testing.md)** - Guida completa al testing
5. **[Security Guidelines](architecture/security-dev.md)** - Linee guida per lo sviluppo sicuro

### Guide Deployment

1. **[Docker Deployment](deployment.md)** - Deploy con Docker e Docker Compose
2. **[Production Setup](guides/production.md)** - Configurazione per produzione
3. **[Monitoring](guides/monitoring.md)** - Monitoraggio e logging
4. **[Backup & Recovery](guides/backup.md)** - Strategie di backup e recovery

## API Reference

### Core Components

- **[Runner API](api/runner.md)** - Core engine per l'elaborazione query
- **[Context API](api/context.md)** - Gestione contesto e prompt building
- **[Retriever API](api/retriever.md)** - Sistema di ricerca semantica
- **[Translation API](api/translation.md)** - Servizi di traduzione multilingue

### Interfaces

- **[CLI Reference](api/cli.md)** - Riferimento completo comandi CLI
- **[REST API](api.md)** - Documentazione endpoint REST
- **[GUI Components](api/gui.md)** - Componenti dell'interfaccia grafica

### Utilities

- **[Configuration](config/config.md)** - Sistema di configurazione
- **[Security Utils](api/security.md)** - Utilità di sicurezza
- **[Validation](api/validation.md)** - Sistema di validazione input

## Architettura

### Panoramica del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     SIGMA-NEX ECOSYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    CLI      │  │    GUI      │  │    API      │         │
│  │ Interface   │  │ Interface   │  │   Server    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │               CORE ENGINE                          │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │   │
│  │  │ Runner  │  │Context  │  │Retriever│  │Translate│ │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │             AI MODELS & DATA                        │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │   │
│  │  │ Ollama  │  │ FAISS   │  │MarianMT │             │ │   │
│  │  │(Mistral)│  │ Index   │  │Models   │             │ │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns

- **[Architectural Patterns](architecture/patterns.md)** - Pattern architetturali utilizzati
- **[Data Flow](architecture/data-flow.md)** - Flusso dei dati nel sistema
- **[Component Interaction](architecture/components.md)** - Interazione tra componenti
- **[Security Architecture](architecture/security.md)** - Architettura di sicurezza

## Configurazione

### File di Configurazione

Il sistema SIGMA-NEX utilizza un file `config.yaml` per la configurazione:

```yaml
# Configurazione modello AI
model_name: "mistral"
temperature: 0.7
max_tokens: 2048

# Sistema
debug: false
retrieval_enabled: true
max_history: 100

# Sicurezza
security_mode: "enabled"
encryption_enabled: true

# Traduzione
translation_enabled: true
source_language: "auto"
target_language: "it"
```

### Configurazioni Avanzate

- **[Advanced Configuration](config/advanced.md)** - Configurazioni avanzate
- **[Environment Variables](config/environment.md)** - Variabili d'ambiente
- **[Authentication Setup](config/authentication.md)** - Configurazione autenticazione
- **[Production Config](config/production.md)** - Configurazione per produzione
- **[Performance Tuning](config/performance.md)** - Ottimizzazione performance

## Testing

### Framework di Testing

SIGMA-NEX utilizza pytest come framework di testing principale:

- **Coverage target**: >95%
- **Test types**: Unit, Integration, E2E, Performance, Security
- **CI/CD**: GitHub Actions con test automatici

### Esecuzione Test

```bash
# Tutti i test
pytest

# Con coverage
pytest --cov=sigma_nex --cov-report=html

# Test specifici
pytest tests/unit/test_runner.py -v
```

Per maggiori dettagli, consulta la [Guida Testing completa](testing.md).

## Contribuire

SIGMA-NEX è un progetto open source e accoglie contributi dalla comunità:

### Come Contribuire

1. **Fork** del repository
2. **Crea** un branch per la tua feature (`git checkout -b feature/amazing-feature`)
3. **Commit** delle modifiche (`git commit -m 'Add amazing feature'`)
4. **Push** al branch (`git push origin feature/amazing-feature`)
5. **Apri** una Pull Request

### Linee Guida

- Segui il [Codice di Condotta](../CODE_OF_CONDUCT.md)
- Leggi le [Linee Guida per Contributi](../CONTRIBUTING.md)
- Scrivi test per il nuovo codice
- Mantieni la documentazione aggiornata

## Sicurezza

### Politica di Sicurezza

SIGMA-NEX prende seriamente la sicurezza. Per segnalazioni di vulnerabilità:

- **Email**: rootedlab6@gmail.com
- **Policy completa**: [SECURITY.md](../SECURITY.md)

### Best Practices

- Sistema completamente offline per default
- Input sanitization e validazione
- Crittografia dei dati sensibili
- Audit logging completo

## Struttura Documentazione

```
docs/
├── README.md                 # Questo file - Panoramica generale
├── api.md                   # API Reference base
├── development.md           # Guida sviluppo
├── deployment.md            # Guida deployment
├── testing.md              # Guida testing
├── installation.md         # Guida installazione dettagliata
├── api/                    # API Reference dettagliata
│   ├── runner.md           # Core Runner API
│   ├── context.md          # Context Management API
│   ├── retriever.md        # Retrieval System API
│   ├── translation.md      # Translation Service API
│   └── cli.md              # CLI Reference completa
├── guides/                 # Guide dettagliate
│   ├── cli-guide.md        # Guida CLI completa
│   ├── gui-guide.md        # Guida interfaccia grafica
│   ├── api-usage.md        # Utilizzo API REST
│   ├── configuration.md    # Configurazione del sistema
│   └── troubleshooting.md  # Risoluzione problemi
├── architecture/           # Documentazione architettura
│   └── overview.md         # Panoramica architetturale
└── config/                 # Configurazione
    ├── config.md           # Reference configurazione
    └── security.md         # Configurazione sicurezza
```

## Link Utili

- **[Repository GitHub](https://github.com/SebastianMartinNS/SYGMA-NEX)**
- **[Issues](https://github.com/SebastianMartinNS/SYGMA-NEX/issues)**
- **[Discussions](https://github.com/SebastianMartinNS/SYGMA-NEX/discussions)**
- **[Releases](https://github.com/SebastianMartinNS/SYGMA-NEX/releases)**
- **[Wiki](https://github.com/SebastianMartinNS/SYGMA-NEX/wiki)**

## Supporto

Hai bisogno di aiuto? Ecco come contattarci:

- **Bug Reports**: [GitHub Issues](https://github.com/SebastianMartinNS/SYGMA-NEX/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/SebastianMartinNS/SYGMA-NEX/discussions)
- **Email**: rootedlab6@gmail.com
- **Community**: [Discord Server](#) (coming soon)

---

<div align="center">

**SIGMA-NEX - Sopravvivenza Intelligente Offline-First**

*Documentazione aggiornata al 24 Settembre 2025*

</div>
