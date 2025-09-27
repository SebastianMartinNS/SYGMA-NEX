# SIGMA-NEX CLI Guide

## Overview

La Command Line Interface (CLI) di SIGMA-NEX fornisce accesso completo a tutte le funzionalità del sistema tramite terminale.

## Getting Started

### Basic Setup

```bash
# Verifica installazione
sigma --version

# Check sistema
sigma self-check

# Mostra help generale
sigma --help
```

### First Query

```bash
# Avvia modalità interattiva
sigma start

# Avvia server API
sigma server

# Avvia interfaccia grafica
sigma gui
```

## Interactive Mode

### Starting Interactive Session

```bash
# Modalità interattiva standard
sigma start

# Con configurazione personalizzata
sigma start --config config.production.yaml
```

### Interactive Commands

Nella modalità interattiva sono disponibili comandi speciali:

```
>> help                    # Mostra aiuto
>> history                 # Mostra cronologia
>> clear                   # Pulisci schermo
>> exit                    # Esci
```

### Example Interactive Session

```
$ sigma start
🤖 SIGMA-NEX Interactive Mode
Type 'help' for commands, 'exit' to quit

>> Come disinfettare una ferita?

🏥 Per disinfettare correttamente una ferita:

1. **Lavaggio mani**: Lavati le mani con sapone antibatterico
2. **Pulizia ferita**: Rimuovi delicatamente sporco e detriti
3. **Disinfettante**: Applica:
   - Acqua ossigenata (3%)
   - Clorexidina (0.5%)
   - Alcol etilico (70%)
4. **Copertura**: Applica benda sterile

**ATTENZIONE**: Se la ferita è profonda o non smette di sanguinare,
consulta immediatamente un medico.

>> history
1. Come disinfettare una ferita?

>> exit
Arrivederci!
```

## Server Management

### Starting the Server

```bash
# Server base
sigma server

# Server con configurazione custom
sigma server --host 0.0.0.0 --port 8080
```

### Server Authentication

```bash
# Login per comandi protetti
sigma login

# Logout
sigma logout
```

## Data Management

### Framework Loading

```bash
# Carica file Framework_SIGMA.json
sigma load-framework --path /path/to/Framework_SIGMA.json
```

## System Management

### Self Check

```bash
# Verifica sistema e dipendenze
sigma self-check
```

### Self Heal

```bash
# Analizza e migliora codice Python
sigma self-heal --file script.py
```

### Update

```bash
# Aggiorna SIGMA-NEX dal repository
sigma update
```

### Global Configuration

```bash
# Installa configurazione globale
sigma install-config

# Rimuovi configurazione globale
sigma install-config --uninstall
```

## GUI Interface

### Starting GUI

```bash
# Avvia interfaccia grafica
sigma gui
```

## Authentication System

### Login Process

```bash
# Login con credenziali
sigma login --username dev --password your_password

# Login con environment variables
export SIGMA_DEV_PASSWORD=your_password
sigma login --username dev
```

### Session Management

Le sessioni sono gestite automaticamente con timeout di sicurezza e supporto multi-sessione limitato.

## Configuration Examples

### Development Setup

```bash
# Setup ambiente sviluppo
sigma self-check
sigma start  # Test modalità interattiva
```

### Production Setup

```bash
# Setup produzione con autenticazione
sigma login --username admin
sigma server --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Common Issues

```bash
# Sistema non risponde
sigma self-check

# Problemi autenticazione
sigma login  # Riprova login

# Aggiorna se necessario
sigma update
```

### Debug Mode

```bash
# Esegui comandi con debug
SIGMA_DEBUG=1 sigma self-check
```

## Tips and Best Practices

### Productivity Tips

```bash
# Alias utili
alias sq='sigma start'
alias sserver='sigma server'
alias scheck='sigma self-check'
```

### Security Best Practices

```bash
# Usa sempre autenticazione per comandi protetti
sigma login --username admin

# Non condividere session tokens
# Configura environment variables per password sicure
```

### Integration Workflows

```bash
#!/bin/bash
# workflow.sh - Script di automazione SIGMA-NEX

# Verifica sistema
sigma self-check

# Avvia servizi
sigma server &
SERVER_PID=$!

# Esegui operazioni
# ... operazioni automatizzate ...

# Cleanup
kill $SERVER_PID
```

## Getting Help

```bash
# Help generale
sigma --help

# Help per comando specifico
sigma server --help
sigma login --help
```

## Available Commands

### Core Commands
- `sigma start` - Modalità interattiva
- `sigma server` - Avvia server API
- `sigma gui` - Interfaccia grafica

### Authentication
- `sigma login` - Login al sistema
- `sigma logout` - Logout dal sistema

### System Management
- `sigma self-check` - Verifica sistema
- `sigma self-heal` - Analisi codice
- `sigma update` - Aggiornamento sistema
- `sigma install-config` - Configurazione globale

### Data Operations
- `sigma load-framework` - Caricamento framework

## Configuration Files

### Main Configuration
- `config.yaml` - Configurazione principale
- Environment variables per credenziali sicure

### Global Configuration
- `SIGMA_NEX_ROOT` - Directory root globale
- Session files in directory temporanea

## Security Features

### Authentication Levels
- **Public**: Accesso limitato (disabilitato per sicurezza)
- **User**: Query base (disabilitato per sicurezza)
- **Dev**: Sviluppo e testing
- **Admin**: Accesso completo

### Session Security
- Token sicuri generati casualmente
- Timeout automatico sessioni
- Limite sessioni concorrenti
- Lockout dopo tentativi falliti

## Performance Optimization

### Memory Management
- Gestione efficiente history con deque
- Cleanup automatico file temporanei
- Limits configurabili per risorse

### Caching
- Cache modelli e configurazioni
- Session persistence ottimizzata
- File locking per concorrenza sicura
