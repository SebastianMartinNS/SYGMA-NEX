# 🔧 Configuration Reference

## Overview

This document provides a comprehensive reference for all SIGMA-NEX configuration options.

## Core Configuration

### Model Settings

```yaml
# AI Model Configuration
model_name: "mistral"              # Primary AI model
temperature: 0.7                   # Response creativity (0.0-1.0)
max_tokens: 2048                   # Maximum response length
context_window: 4096               # Context window size
top_p: 0.9                         # Nucleus sampling
top_k: 40                          # Top-k sampling
repeat_penalty: 1.1                # Repetition penalty

# Medical Model Configuration  
medical_model: "medllama2"         # Specialized medical model
medical_temperature: 0.3           # Conservative temperature for medical
medical_max_tokens: 4096           # Longer responses for medical
emergency_model: "medllama2"       # Emergency protocol model
```

### System Settings

```yaml
# System Behavior
debug: false                       # Enable debug mode
log_level: "INFO"                  # Logging level
max_history: 100                   # Conversation history limit
auto_save: true                    # Auto-save conversations
startup_check: true                # System check on startup
self_healing: true                 # Auto-recovery features

# Performance Settings
workers: 1                         # Number of worker processes
max_concurrent: 10                 # Max concurrent requests
request_timeout: 30                # Request timeout (seconds)
memory_limit: "2GB"                # Memory usage limit
cache_size: 1000                   # Cache size (entries)
```

## Retrieval Configuration

### FAISS Settings

```yaml
retrieval:
  enabled: true                    # Enable semantic search
  engine: "faiss"                  # Search engine (faiss, simple)
  top_k: 5                         # Number of results
  similarity_threshold: 0.7        # Minimum similarity score
  
  # FAISS Configuration
  faiss:
    index_type: "flat"             # flat, ivf, hnsw
    dimension: 384                 # Embedding dimension
    nlist: 100                     # Number of clusters (IVF)
    nprobe: 10                     # Search clusters (IVF)
    ef_construction: 40            # HNSW construction
    ef_search: 16                  # HNSW search
    M: 16                          # HNSW connections
    
  # Embedding Configuration
  embeddings:
    model: "all-MiniLM-L6-v2"      # Embedding model
    batch_size: 32                 # Encoding batch size
    cache_embeddings: true         # Cache embeddings
    normalize: true                # Normalize vectors
```

### Search Enhancement

```yaml
# Search Optimization
search:
  boost_medical: 1.5               # Boost medical content
  boost_emergency: 2.0             # Boost emergency content
  recency_boost: 0.1               # Boost recent documents
  length_penalty: 0.05             # Penalty for long documents
  
  # Query Enhancement
  query_expansion: true            # Expand queries with synonyms
  medical_synonyms: true           # Use medical synonym expansion
  spell_correction: true           # Auto-correct spelling
  stemming: true                   # Enable stemming
```

## Translation Configuration

### Language Settings

```yaml
translation:
  enabled: true                    # Enable translation
  default_source: "auto"           # Auto-detect source language
  default_target: "it"             # Default target language
  preserve_medical: true           # Preserve medical terms
  
  # Supported Languages
  languages:
    - "it"    # Italian (primary)
    - "en"    # English
    - "es"    # Spanish
    - "fr"    # French
    - "de"    # German
    - "pt"    # Portuguese
    - "ru"    # Russian
    - "ar"    # Arabic
    - "zh"    # Chinese
    - "ja"    # Japanese
    
  # Model Configuration
  models:
    base_model: "Helsinki-NLP/opus-mt"
    medical_model: "clinical-marian-mt"
    fallback_model: "google-translate"  # External fallback
    
  # Quality Settings
  quality:
    min_confidence: 0.8            # Minimum translation confidence
    back_translation: true         # Verify with back-translation
    medical_validation: true       # Validate medical translations
```

## Security Configuration

### Encryption Settings

```yaml
security:
  encryption:
    enabled: true                  # Enable encryption
    algorithm: "AES-256-GCM"       # Encryption algorithm
    key_length: 32                 # Key length in bytes
    key_rotation: 86400            # Key rotation interval (seconds)
    secure_delete: true            # Secure memory deletion
    
  # Access Control
  access_control:
    enabled: true                  # Enable access control
    default_deny: true             # Default deny policy
    ip_whitelist:                  # Allowed IP addresses
      - "127.0.0.1"
      - "192.168.0.0/16"
    session_timeout: 3600          # Session timeout (seconds)
    
  # Input Validation
  validation:
    max_query_length: 10000        # Maximum query length
    blocked_patterns:              # Blocked regex patterns
      - "(?i)(select|drop|delete)\\s"
      - "(?i)(<script|javascript:)"
    sanitize_html: true            # Strip HTML tags
    validate_encoding: true        # Validate text encoding
```

### Audit Configuration

```yaml
# Audit and Logging
audit:
  enabled: true                    # Enable audit logging
  log_queries: true                # Log user queries
  log_responses: false             # Log AI responses (privacy)
  anonymize_personal: true         # Anonymize personal data
  retention_days: 90               # Log retention period
  
  # Medical Audit
  medical_audit:
    enabled: true                  # Enhanced medical audit
    log_patient_data: false        # Log patient information
    anonymize_medical: true        # Anonymize medical data
    require_justification: false   # Require query justification
    
  # Compliance
  compliance:
    hipaa: true                    # HIPAA compliance mode
    gdpr: true                     # GDPR compliance mode
    iso27001: true                 # ISO 27001 compliance
```

## Server Configuration

### HTTP Server Settings

```yaml
server:
  host: "127.0.0.1"                # Bind host
  port: 8000                       # Bind port
  workers: 1                       # Number of workers
  timeout: 30                      # Request timeout
  keepalive: 65                    # Keep-alive timeout
  max_requests: 1000               # Requests per worker
  
  # SSL/TLS Configuration
  ssl:
    enabled: false                 # Enable SSL
    cert_file: "/path/to/cert.pem"
    key_file: "/path/to/key.pem"
    ca_file: "/path/to/ca.pem"
    ssl_version: "TLSv1.3"
    
  # CORS Configuration
  cors:
    enabled: true                  # Enable CORS
    allowed_origins:               # Allowed origins
      - "http://localhost:3000"
      - "https://your-domain.com"
    allowed_methods: ["GET", "POST"]
    allowed_headers: ["Content-Type", "Authorization"]
    max_age: 600                   # Preflight cache time
```

### Rate Limiting

```yaml
# Rate Limiting Configuration
rate_limiting:
  enabled: true                    # Enable rate limiting
  storage: "memory"                # memory, redis
  redis_url: "redis://localhost:6379"
  
  # Rate Limits
  limits:
    global: "1000/hour"            # Global rate limit
    per_ip: "100/hour"             # Per IP rate limit
    per_user: "60/minute"          # Per user rate limit
    
  # Endpoint-Specific Limits
  endpoints:
    "/ask": "60/minute"
    "/batch": "10/minute"
    "/emergency": "unlimited"      # No limit for emergencies
    
  # Burst Configuration
  burst:
    enabled: true                  # Enable burst capacity
    size: 10                       # Burst size
    refill_rate: 1                 # Refill rate per second
```

## Path Configuration

### Directory Structure

```yaml
paths:
  # Base Directories
  base_dir: "~/.sigma-nex"         # Base directory
  data_dir: "~/.sigma-nex/data"    # Data directory
  log_dir: "~/.sigma-nex/logs"     # Log directory
  cache_dir: "~/.sigma-nex/cache"  # Cache directory
  temp_dir: "/tmp/sigma-nex"       # Temporary directory
  
  # Data Files
  index_file: "data/moduli.index"  # FAISS index file
  mapping_file: "data/moduli.mapping.json"
  config_file: "config.yaml"      # Configuration file
  
  # Models
  models_dir: "models"             # Models directory
  embeddings_cache: "cache/embeddings"
  translations_cache: "cache/translations"
  
  # Logs
  main_log: "logs/sigma-nex.log"
  audit_log: "logs/audit.log"
  error_log: "logs/error.log"
  access_log: "logs/access.log"
```

## Ollama Configuration

### Connection Settings

```yaml
ollama:
  host: "localhost"                # Ollama host
  port: 11434                      # Ollama port
  timeout: 120                     # Connection timeout
  retry_attempts: 3                # Retry attempts
  retry_delay: 1                   # Retry delay (seconds)
  
  # Model Management
  auto_pull: true                  # Auto-pull missing models
  model_timeout: 300               # Model load timeout
  keep_alive: 600                  # Model keep-alive time
  
  # Performance
  num_ctx: 4096                    # Context size
  num_predict: 2048                # Prediction length
  num_thread: 8                    # CPU threads
  num_gpu: 1                       # GPU count
  
  # Memory Management
  mlock: false                     # Lock model in memory
  numa: false                      # NUMA awareness
  low_vram: false                  # Low VRAM mode
```

## GUI Configuration

### Interface Settings

```yaml
gui:
  # Appearance
  theme: "dark"                    # dark, light, auto
  font_family: "Segoe UI"          # Font family
  font_size: 12                    # Font size
  scaling: 1.0                     # UI scaling factor
  
  # Window Settings
  window_size: [800, 600]          # Default window size
  min_size: [600, 400]             # Minimum window size
  max_size: [1920, 1080]           # Maximum window size
  resizable: true                  # Allow window resize
  
  # Chat Interface
  chat:
    message_spacing: 10            # Message spacing
    max_messages: 1000             # Max displayed messages
    auto_scroll: true              # Auto-scroll to bottom
    timestamp_visible: true        # Show timestamps
    word_wrap: true                # Enable word wrap
    
  # Behavior
  behavior:
    auto_save: true                # Auto-save conversations
    confirm_exit: true             # Confirm on exit
    minimize_to_tray: false        # Minimize to system tray
    check_updates: true            # Check for updates
```

### Medical Interface

```yaml
# Medical-Specific GUI Settings
medical_gui:
  emergency_button: true           # Show emergency button
  medical_mode: true               # Enable medical interface
  quick_actions: true              # Show quick action buttons
  
  # Emergency Settings
  emergency:
    auto_activate: true            # Auto-activate on emergency keywords
    priority_display: true         # Priority visual indicators
    protocol_shortcuts: true       # Quick protocol access
    
  # Medical Tools
  tools:
    calculator: true               # Medical calculators
    drug_database: true            # Drug information
    reference_guides: true         # Medical references
    protocol_access: true          # Emergency protocols
```

## Logging Configuration

### Log Levels and Formats

```yaml
logging:
  version: 1
  disable_existing_loggers: false
  
  # Formatters
  formatters:
    standard:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
      datefmt: '%Y-%m-%d %H:%M:%S'
      
    detailed:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
      
    json:
      format: '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}'
      
    medical:
      format: '[MEDICAL] %(asctime)s - %(levelname)s - %(message)s'
      
  # Handlers
  handlers:
    console:
      class: logging.StreamHandler
      level: INFO
      formatter: standard
      stream: ext://sys.stdout
      
    file:
      class: logging.handlers.RotatingFileHandler
      level: DEBUG
      formatter: detailed
      filename: ~/.sigma-nex/logs/sigma-nex.log
      maxBytes: 10485760            # 10MB
      backupCount: 5
      encoding: utf-8
      
    audit:
      class: logging.handlers.RotatingFileHandler
      level: INFO
      formatter: json
      filename: ~/.sigma-nex/logs/audit.log
      maxBytes: 52428800            # 50MB
      backupCount: 10
      
    medical:
      class: logging.handlers.RotatingFileHandler
      level: INFO
      formatter: medical
      filename: ~/.sigma-nex/logs/medical.log
      maxBytes: 20971520            # 20MB
      backupCount: 7
      
  # Loggers
  loggers:
    sigma_nex:
      level: INFO
      handlers: [console, file]
      propagate: false
      
    sigma_nex.audit:
      level: INFO
      handlers: [audit]
      propagate: false
      
    sigma_nex.medical:
      level: INFO
      handlers: [medical, audit]
      propagate: false
      
    sigma_nex.security:
      level: WARNING
      handlers: [file, audit]
      propagate: false
```

## Performance Configuration

### Optimization Settings

```yaml
performance:
  # Memory Management
  memory:
    max_memory: "4GB"              # Maximum memory usage
    gc_threshold: 0.8              # Garbage collection threshold
    cache_size: 1000               # Cache size (entries)
    preload_models: true           # Preload models at startup
    
  # Threading
  threading:
    max_workers: 8                 # Maximum worker threads
    thread_pool_size: 4            # Thread pool size
    async_enabled: true            # Enable async processing
    
  # Caching
  caching:
    enabled: true                  # Enable caching
    backend: "memory"              # memory, redis, file
    ttl: 3600                      # Cache TTL (seconds)
    max_size: 1000                 # Max cache entries
    
  # Database
  database:
    pool_size: 20                  # Connection pool size
    max_overflow: 30               # Max overflow connections
    pool_timeout: 30               # Pool timeout
    pool_recycle: 3600             # Pool recycle time
```

## Environment-Specific Configurations

### Development Configuration

```yaml
# config.dev.yaml
extends: "config.yaml"             # Extend base config

# Override for development
debug: true
log_level: "DEBUG"
auto_reload: true

server:
  workers: 1
  timeout: 120
  
security:
  encryption_enabled: false
  audit_logging: false
  
performance:
  cache_size: 100
  preload_models: false
```

### Production Configuration

```yaml
# config.production.yaml
extends: "config.yaml"

# Production overrides
debug: false
log_level: "INFO"

server:
  workers: 4
  timeout: 60
  
security:
  encryption_enabled: true
  audit_logging: true
  rate_limiting_enabled: true
  
performance:
  cache_size: 5000
  preload_models: true
  max_memory: "8GB"
  
monitoring:
  enabled: true
  metrics_enabled: true
  health_checks: true
```

### Testing Configuration

```yaml
# config.test.yaml
extends: "config.yaml"

# Test overrides
debug: true
log_level: "DEBUG"

# Use test data
paths:
  data_dir: "test_data"
  
# Disable external services
ollama:
  enabled: false
  
translation:
  enabled: false
  
# Fast settings for tests
retrieval:
  top_k: 1
  
performance:
  cache_size: 10
```

## Configuration Validation

### Schema Definition

```yaml
# Configuration schema for validation
schema:
  type: object
  required: [model_name, server]
  properties:
    model_name:
      type: string
      enum: [mistral, llama2, medllama2]
      
    temperature:
      type: number
      minimum: 0.0
      maximum: 2.0
      
    server:
      type: object
      required: [host, port]
      properties:
        host:
          type: string
          format: hostname
        port:
          type: integer
          minimum: 1
          maximum: 65535
```

### Validation Commands

```bash
# Validate current configuration
sigma config validate

# Validate specific file
sigma config validate --file config.production.yaml

# Check configuration schema
sigma config schema

# Show configuration with validation
sigma config show --validate
```

For configuration support:
- **Configuration Guide**: https://docs.sigma-nex.org/config
- **Schema Reference**: https://schema.sigma-nex.org
- **Examples**: https://github.com/SebastianMartinNS/SYGMA-NEX/tree/master/examples/config
- **Support**: rootedlab6@gmail.com