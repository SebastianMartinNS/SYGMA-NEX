# 🖥️ SIGMA-NEX CLI Guide

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
# Query semplice
sigma ask "Come misurare la pressione arteriosa?"

# Query con contesto
sigma ask "Che farmaco posso usare?" --context "Ho mal di testa"
```

## Interactive Mode

### Starting Interactive Session

```bash
# Modalità interattiva standard
sigma

# Con modello specifico
sigma --model mistral

# Con configurazione personalizzata
sigma --config config.production.yaml
```

### Interactive Commands

Nella modalità interattiva sono disponibili comandi speciali:

```
>> help                    # Mostra aiuto
>> history                 # Mostra cronologia
>> clear                   # Pulisci schermo
>> save conversation.txt   # Salva conversazione
>> load conversation.txt   # Carica conversazione
>> model mistral          # Cambia modello
>> exit                    # Esci
```

### Example Interactive Session

```
$ sigma
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

⚠️ **ATTENZIONE**: Se la ferita è profonda o non smette di sanguinare, 
consulta immediatamente un medico.

>> history
1. Come disinfettare una ferita?

>> save wound_care.txt
✅ Conversazione salvata in wound_care.txt

>> exit
👋 Arrivederci!
```

## Direct Queries

### Basic Queries

```bash
# Query diretta
sigma ask "Sintomi dell'infarto"

# Query con priorità medica
sigma ask "Dolore al petto acuto" --medical-priority

# Query con traduzione
sigma ask "How to treat a burn?" --translate-to it
```

### Advanced Queries

```bash
# Query con cronologia
sigma ask "Quale antibiotico?" --history "Ho una ferita infetta da 2 giorni"

# Query con contesto medico
sigma ask "Dosaggio ibuprofene" --context "Paziente 65 anni, 70kg"

# Query con formato output specifico
sigma ask "Protocollo RCP" --format structured
```

## Server Management

### Starting the Server

```bash
# Server base
sigma server

# Server con configurazione custom
sigma server --host 0.0.0.0 --port 8080

# Server in debug mode
sigma server --debug --reload

# Server production
sigma server --config production.yaml --workers 4
```

### Server Monitoring

```bash
# Status del server
curl http://localhost:8000/

# Health check dettagliato
sigma health --server

# Logs in tempo reale
sigma logs tail --server
```

## Data Management

### Index Operations

```bash
# Costruisci index da zero
sigma index build

# Aggiorna index esistente
sigma index update

# Ricostruisci forzando
sigma index rebuild --force

# Statistiche index
sigma index stats
```

### Data Import/Export

```bash
# Importa documenti medici
sigma data import medical_docs/ --format json

# Importa da database
sigma data import medical.db --type sqlite

# Esporta configurazione
sigma config export --format yaml
```

## Model Management

### Ollama Integration

```bash
# Lista modelli disponibili
sigma models list

# Scarica nuovo modello
sigma models pull medllama2

# Test modello
sigma models test mistral --query "Test di funzionamento"

# Rimuovi modello
sigma models remove old-model
```

### Model Configuration

```bash
# Configura modello default
sigma config set model_name mistral

# Configura temperatura
sigma config set temperature 0.7

# Mostra configurazione modelli
sigma models config
```

## Security and User Management

### Security Commands

```bash
# Scansione sicurezza
sigma security scan

# Audit completo
sigma security audit --output audit-report.json

# Verifica permessi
sigma security check

# Logs di sicurezza
sigma security logs --last 100
```

### User Management

```bash
# Crea utente
sigma users create medic1 --role medical

# Lista utenti
sigma users list

# Aggiorna permessi
sigma users update medic1 --permissions emergency,prescription

# Disabilita utente
sigma users disable medic1
```

## Monitoring and Diagnostics

### System Monitoring

```bash
# Status completo del sistema
sigma status --detailed

# Monitoring in tempo reale
sigma monitor --refresh 5 --metrics cpu,memory,requests

# Performance metrics
sigma metrics --period 1h
```

### Log Management

```bash
# Mostra logs recenti
sigma logs show --last 50

# Filtra per livello
sigma logs show --level ERROR

# Cerca nei logs
sigma logs search "medical query" --timeframe 24h

# Export logs
sigma logs export --format json --output logs-$(date +%Y%m%d).json
```

## Configuration Management

### Config Commands

```bash
# Mostra configurazione corrente
sigma config show

# Edita configurazione
sigma config edit

# Valida configurazione
sigma config validate

# Reset a default
sigma config reset
```

### Environment Setup

```bash
# Setup ambiente sviluppo
sigma setup dev

# Setup ambiente produzione
sigma setup production

# Verifica dipendenze
sigma setup check

# Pulizia cache
sigma setup clean
```

## Advanced Features

### Backup and Restore

```bash
# Crea backup completo
sigma backup create --output backup-$(date +%Y%m%d).tar.gz

# Lista backup disponibili
sigma backup list

# Ripristina da backup
sigma backup restore backup-20240901.tar.gz

# Verifica integrità backup
sigma backup verify backup-20240901.tar.gz
```

### Performance Tools

```bash
# Profiling performance
sigma profile start --duration 60

# Analisi memoria
sigma memory analyze

# Ottimizzazione automatica
sigma optimize --target performance

# Cache management
sigma cache stats
sigma cache clear
```

## Automation and Scripting

### Batch Processing

```bash
# Processa file di query
cat queries.txt | sigma batch --format json

# Script automatico
sigma script run daily-checks.sh

# Scheduled tasks
sigma schedule add "0 */6 * * *" "sigma index update"
```

### Integration Examples

```bash
#!/bin/bash
# medical-check.sh - Script di controllo medico automatico

# Verifica sistema
if ! sigma self-check --quiet; then
    echo "❌ Sistema non funzionante"
    exit 1
fi

# Query medica standard
RESPONSE=$(sigma ask "Protocolli emergenza attivi" --format json)

# Salva response
echo "$RESPONSE" > /var/log/medical-status.json

# Notifica se necessario
if echo "$RESPONSE" | grep -q "ALERT"; then
    sigma notify admin "Attenzione protocolli emergenza"
fi
```

## Troubleshooting

### Common Issues

```bash
# Modello non trovato
sigma models list          # Verifica modelli disponibili
sigma models pull mistral  # Scarica modello mancante

# Errori di connessione
sigma diagnose network     # Diagnosi rete
sigma status ollama        # Verifica Ollama

# Problemi permessi
sudo chown -R $USER ~/.sigma-nex/  # Fix permessi Linux
```

### Debug Mode

```bash
# Debug completo
sigma --debug --verbose ask "test query"

# Trace comandi
SIGMA_TRACE=1 sigma ask "debug test"

# Logs debug
sigma logs show --level DEBUG --tail
```

## Tips and Best Practices

### Productivity Tips

```bash
# Alias utili
alias sq='sigma ask'
alias slog='sigma logs tail'
alias sstatus='sigma status'

# Autocompletamento
eval "$(_SIGMA_COMPLETE=bash_source sigma)"  # Bash
eval "$(_SIGMA_COMPLETE=zsh_source sigma)"   # Zsh
```

### Medical Use Cases

```bash
# Emergenza rapida
sigma ask "RCP pediatrica" --priority high --format checklist

# Ricerca farmaci
sigma ask "Interazioni paracetamolo ibuprofene" --context "Paziente anziano"

# Protocolli ospedalieri
sigma ask "Protocollo sepsi" --format protocol --save protocols/
```

### Integration Workflows

```bash
# Pipeline medica completa
sigma data import latest-medical-db.json
sigma index rebuild
sigma models update
sigma server restart
sigma notify team "Sistema aggiornato"
```

## Configuration Examples

### Development Setup

```bash
# Configura per sviluppo
sigma config set debug true
sigma config set log_level DEBUG
sigma config set auto_reload true
sigma server --dev
```

### Production Setup

```bash
# Configura per produzione
sigma config set workers 4
sigma config set log_level INFO
sigma config set security.rate_limiting true
sigma config set monitoring.enabled true
```

## Getting Help

```bash
# Help generale
sigma --help

# Help per comando specifico
sigma ask --help
sigma server --help

# Documentazione online
sigma docs open

# Support
sigma support contact
```