# 🔧 SIGMA-NEX Configuration Guide

## Overview

SIGMA-NEX utilizza un sistema di configurazione flessibile basato su file YAML che permette di personalizzare ogni aspetto del comportamento del sistema.

## Configuration Hierarchy

La configurazione segue una gerarchia specifica:

1. **Command line arguments** (priorità massima)
2. **Environment variables**
3. **User config file** (`~/.sigma-nex/config.yaml`)
4. **System config file** (`/etc/sigma-nex/config.yaml`)
5. **Default values** (priorità minima)

## Main Configuration File

### Location

```bash
# Linux/macOS
~/.sigma-nex/config.yaml

# Windows
%APPDATA%\SigmaNex\config.yaml

# Custom location
export SIGMA_CONFIG="/path/to/custom/config.yaml"
```

### Basic Structure

```yaml
# config.yaml - Configurazione principale SIGMA-NEX

# === MODELLO AI ===
model_name: "mistral"                # Modello Ollama da utilizzare
temperature: 0.7                     # Creatività risposte (0.0-1.0)
max_tokens: 2048                     # Lunghezza massima risposta
context_window: 4096                 # Finestra di contesto

# === SISTEMA ===
debug: false                         # Modalità debug
log_level: "INFO"                    # DEBUG, INFO, WARNING, ERROR
max_history: 100                     # Cronologia conversazioni
auto_save: true                      # Salvataggio automatico

# === RICERCA SEMANTICA ===
retrieval_enabled: true              # Abilita ricerca FAISS
retrieval_top_k: 5                   # Numero risultati
similarity_threshold: 0.7            # Soglia similarità

# === TRADUZIONE ===
translation_enabled: true            # Abilita traduzione
source_language: "auto"              # Rilevamento automatico
target_language: "it"                # Lingua target default
preserve_medical_terms: true         # Preserva terminologia medica

# === SICUREZZA ===
security:
  encryption_enabled: true           # Crittografia dati
  rate_limiting: false               # Limitazione rate
  audit_logging: true                # Log audit
  ip_whitelist: []                   # Lista IP autorizzati

# === SERVER ===
server:
  host: "127.0.0.1"                 # Host binding
  port: 8000                         # Porta
  workers: 1                         # Processi worker
  timeout: 30                        # Timeout richieste

# === PERCORSI ===
paths:
  data_dir: "~/.sigma-nex/data"      # Directory dati
  log_dir: "~/.sigma-nex/logs"       # Directory log
  cache_dir: "~/.sigma-nex/cache"    # Directory cache
  temp_dir: "/tmp/sigma-nex"         # Directory temporanea

# === OLLAMA ===
ollama:
  host: "localhost"                  # Host Ollama
  port: 11434                        # Porta Ollama
  timeout: 120                       # Timeout connessione
  retry_attempts: 3                  # Tentativi riconnessione

# === GUI ===
gui:
  theme: "dark"                      # dark, light, auto
  font_size: 12                      # Dimensione font
  window_size: [800, 600]            # Dimensioni finestra
  auto_scroll: true                  # Scroll automatico
```

## Environment Variables

### Core Variables

```bash
# Configurazione principale
export SIGMA_CONFIG="/path/to/config.yaml"
export SIGMA_MODEL="mistral"
export SIGMA_DEBUG="true"
export SIGMA_LOG_LEVEL="DEBUG"

# Server
export SIGMA_HOST="0.0.0.0"
export SIGMA_PORT="8080"
export SIGMA_WORKERS="4"

# Percorsi
export SIGMA_DATA_DIR="/var/lib/sigma-nex"
export SIGMA_LOG_DIR="/var/log/sigma-nex"
export SIGMA_CACHE_DIR="/tmp/sigma-nex"

# Ollama
export OLLAMA_HOST="localhost:11434"
export OLLAMA_TIMEOUT="120"

# Sicurezza
export SIGMA_ENCRYPTION_KEY="your-32-char-encryption-key-here"
export SIGMA_RATE_LIMIT="100"
export SIGMA_AUDIT_LOG="true"
```

### Medical-Specific Variables

```bash
# Configurazioni mediche
export SIGMA_MEDICAL_MODE="true"
export SIGMA_EMERGENCY_PRIORITY="high"
export SIGMA_MEDICAL_MODEL="medllama2"
export SIGMA_DRUG_DATABASE="/path/to/drugs.db"
```

## Profile Configurations

### Development Profile

```yaml
# config.dev.yaml
model_name: "mistral"
debug: true
log_level: "DEBUG"
auto_reload: true

server:
  host: "127.0.0.1"
  port: 8000
  workers: 1
  debug: true

security:
  encryption_enabled: false
  rate_limiting: false
  audit_logging: false

paths:
  data_dir: "./dev-data"
  log_dir: "./dev-logs"
```

### Production Profile

```yaml
# config.production.yaml
model_name: "mistral"
debug: false
log_level: "INFO"
auto_reload: false

server:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  timeout: 60

security:
  encryption_enabled: true
  rate_limiting: true
  audit_logging: true
  ip_whitelist: ["192.168.0.0/16", "10.0.0.0/8"]

monitoring:
  enabled: true
  metrics_endpoint: "/metrics"
  health_check_interval: 30

paths:
  data_dir: "/var/lib/sigma-nex"
  log_dir: "/var/log/sigma-nex"
  cache_dir: "/var/cache/sigma-nex"
```

### Medical Profile

```yaml
# config.medical.yaml
model_name: "medllama2"
temperature: 0.3                     # Più conservativo per medicina
max_tokens: 4096                     # Risposte più dettagliate

medical_mode: true
emergency_priority: true
drug_interaction_check: true

retrieval:
  medical_only: true                 # Solo documenti medici
  emergency_boost: 2.0               # Boost contenuti emergenza
  
security:
  medical_audit: true                # Audit medico completo
  anonymize_logs: true               # Anonimizza dati pazienti
  
system_prompts:
  default: "prompts/medical-system.txt"
  emergency: "prompts/emergency-system.txt"
```

## Advanced Configuration

### Model Configuration

```yaml
models:
  primary: "mistral"
  medical: "medllama2"
  translation: "opus-mt"
  
  settings:
    mistral:
      temperature: 0.7
      top_p: 0.9
      top_k: 40
      repeat_penalty: 1.1
      
    medllama2:
      temperature: 0.3
      top_p: 0.95
      medical_mode: true
      safety_filter: strict
```

### Retrieval Configuration

```yaml
retrieval:
  enabled: true
  engine: "faiss"                    # faiss, elasticsearch, simple
  
  faiss:
    index_type: "flat"               # flat, ivf, hnsw
    dimension: 384
    nlist: 100
    nprobe: 10
    
  embeddings:
    model: "all-MiniLM-L6-v2"
    batch_size: 32
    cache_size: 10000
    
  search:
    top_k: 5
    similarity_threshold: 0.7
    max_tokens: 2000
    boost_medical: 1.5
```

### Security Configuration

```yaml
security:
  # Encryption
  encryption:
    enabled: true
    algorithm: "AES-256-GCM"
    key_rotation: 86400              # 24 ore
    
  # Authentication
  auth:
    enabled: false                   # Per ora disabilitato
    provider: "local"                # local, ldap, oauth
    session_timeout: 3600
    
  # Rate Limiting
  rate_limiting:
    enabled: true
    requests_per_minute: 60
    burst_size: 10
    
  # Audit
  audit:
    enabled: true
    log_queries: true
    log_responses: false             # Privacy
    anonymize_personal: true
    retention_days: 90
```

### Logging Configuration

```yaml
logging:
  version: 1
  disable_existing_loggers: false
  
  formatters:
    standard:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    detailed:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    json:
      format: '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
      
  handlers:
    console:
      class: logging.StreamHandler
      level: INFO
      formatter: standard
      
    file:
      class: logging.handlers.RotatingFileHandler
      level: DEBUG
      formatter: detailed
      filename: ~/.sigma-nex/logs/sigma-nex.log
      maxBytes: 10485760              # 10MB
      backupCount: 5
      
    audit:
      class: logging.handlers.RotatingFileHandler
      level: INFO
      formatter: json
      filename: ~/.sigma-nex/logs/audit.log
      maxBytes: 52428800              # 50MB
      backupCount: 10
      
  loggers:
    sigma_nex:
      level: INFO
      handlers: [console, file]
      propagate: false
      
    sigma_nex.audit:
      level: INFO
      handlers: [audit]
      propagate: false
```

## Configuration Management

### Loading Configuration

```python
from sigma_nex.config import load_config

# Load with defaults
config = load_config()

# Load specific file
config = load_config("/path/to/config.yaml")

# Load with environment override
config = load_config(env_override=True)
```

### Configuration Validation

```bash
# Validate current config
# Validate YAML syntax manually

# Validate specific file
# Validate YAML syntax manually --file config.production.yaml

# Show configuration with sources
# Check config.yaml file --sources
```

### Dynamic Configuration

```python
# Runtime configuration updates
from sigma_nex.config import update_config

# Update single value
update_config("temperature", 0.8)

# Update nested value
update_config("server.workers", 6)

# Bulk update
update_config({
    "debug": True,
    "log_level": "DEBUG"
})
```

## Configuration Examples

### Minimal Configuration

```yaml
# config.minimal.yaml
model_name: "mistral"
debug: false
```

### High-Performance Configuration

```yaml
# config.performance.yaml
model_name: "mistral"
server:
  workers: 8
  timeout: 120
  
retrieval:
  enabled: true
  top_k: 10
  cache_size: 50000
  
caching:
  enabled: true
  redis_url: "redis://localhost:6379"
  ttl: 3600
```

### Secure Configuration

```yaml
# config.secure.yaml
security:
  encryption_enabled: true
  rate_limiting: true
  audit_logging: true
  ip_whitelist: ["127.0.0.1"]
  
logging:
  anonymize_personal: true
  retention_days: 30
  
server:
  ssl_cert: "/etc/ssl/sigma-nex.crt"
  ssl_key: "/etc/ssl/sigma-nex.key"
```

## Troubleshooting Configuration

### Common Issues

```bash
# Configuration not found
# Check config.yaml file                    # Check current config
# Create config.yaml manually                    # Create default config

# Invalid YAML syntax
# Validate YAML syntax manually               # Check for syntax errors

# Permission issues
sudo chown $USER ~/.sigma-nex/config.yaml
chmod 600 ~/.sigma-nex/config.yaml  # Secure permissions
```

### Debug Configuration

```bash
# Show effective configuration
# Check config.yaml file --resolved

# Show configuration sources
# Check config.yaml file --sources

# Test configuration
# Test configuration manually
```

## Migration Guide

### Upgrading Configuration

```bash
# Backup current config
cp ~/.sigma-nex/config.yaml ~/.sigma-nex/config.yaml.backup

# Migrate to new version
# Migrate configuration manually --from-version 0.1.0

# Validate after migration
# Validate YAML syntax manually
```

### Configuration Schema Changes

When upgrading SIGMA-NEX, configuration schema may change:

1. **Backup** existing configuration
2. **Review** migration notes in CHANGELOG
3. **Run** migration tool
4. **Validate** new configuration
5. **Test** functionality

For assistance with configuration:
- **Documentation**: https://github.com/SebastianMartinNS/SYGMA-NEX/blob/master/docs/guides/configuration.md
- **Examples**: https://github.com/SebastianMartinNS/SYGMA-NEX/tree/master/examples
- **Support**: rootedlab6@gmail.com
