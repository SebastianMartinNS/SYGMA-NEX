# CLI Reference

## Overview

SIGMA-NEX provides a comprehensive command-line interface for all system operations, from basic queries to advanced administration.

## Installation and Setup

```bash
# Install SIGMA-NEX
pip install sigma-nex

# Verify installation
sigma --version

# Check system health
sigma self-check
```

## Basic Commands

### Interactive Mode

```bash
# Start interactive chat
sigma

# Start with specific model
sigma --model mistral

# Start with custom config
sigma --config config.production.yaml
```

### Direct Queries

```bash
# Ask a question directly
sigma ask "Come disinfettare una ferita?"

# Query with history context
sigma ask "Che antibiotico usare?" --history "Ho una ferita infetta"

# Medical priority mode
sigma ask "Dolore al petto" --medical-priority
```

## Server Commands

### Start Server

```bash
# Start API server
sigma server

# Custom host and port
sigma server --host 0.0.0.0 --port 8080

# Production mode
sigma server --config config.production.yaml --workers 4

# Debug mode
sigma server --debug --reload
```

### Server Options

```bash
sigma server [OPTIONS]

Options:
  --host TEXT          Host to bind (default: 127.0.0.1)
  --port INTEGER       Port to bind (default: 8000)
  --workers INTEGER    Number of worker processes
  --config PATH        Configuration file path
  --debug              Enable debug mode
  --reload             Auto-reload on code changes
  --ssl-cert PATH      SSL certificate file
  --ssl-key PATH       SSL private key file
```

## GUI Commands

### Start GUI

```bash
# Start graphical interface
sigma gui

# Start with specific theme
sigma gui --theme dark

# Start in fullscreen
sigma gui --fullscreen
```

## Data Management

### Index Operations

```bash
# Build search index
sigma index build

# Update existing index
sigma index update

# Rebuild from scratch
sigma index rebuild --force

# Show index statistics
sigma index stats
```

### Data Import

```bash
# Import documents
sigma data import documents/ --format json

# Import medical database
sigma data import medical.db --type medical

# Import with preprocessing
sigma data import raw_data/ --preprocess --chunk-size 512
```

## Configuration Commands

### Config Management

```bash
# Show current configuration
sigma config show

# Validate configuration
sigma config validate

# Create default config
sigma config init

# Edit configuration
sigma config edit
```

### Environment Setup

```bash
# Setup development environment
sigma setup dev

# Install models
sigma setup models --medical

# Check dependencies
sigma setup check

# Clean cache and temporary files
sigma setup clean
```

## Model Management

### Ollama Integration

```bash
# List available models
sigma models list

# Pull new model
sigma models pull llama2-medical

# Remove model
sigma models remove old-model

# Test model
sigma models test mistral --query "Test query"
```

### Translation Models

```bash
# Download translation models
sigma translate setup

# List translation languages
sigma translate languages

# Test translation
sigma translate test --source en --target it --text "Hello world"
```

## Security Commands

### User Management

```bash
# Create new user
sigma users create --username medic1 --role medical

# List users
sigma users list

# Update user permissions
sigma users update medic1 --add-permission emergency

# Disable user
sigma users disable medic1
```

### Security Audit

```bash
# Run security scan
sigma security scan

# Check permissions
sigma security check

# Generate audit report
sigma security audit --format json --output audit.json

# View security logs
sigma security logs --last 100
```

## Monitoring Commands

### System Monitoring

```bash
# Show system status
sigma status

# Monitor in real-time
sigma monitor --refresh 5

# Show performance metrics
sigma metrics

# Generate health report
sigma health --detailed
```

### Log Management

```bash
# View logs
sigma logs show

# Tail logs in real-time
sigma logs tail

# Filter logs by level
sigma logs show --level ERROR

# Export logs
sigma logs export --format json --output logs.json
```

## Advanced Commands

### Development Tools

```bash
# Run tests
sigma test

# Run tests with coverage
sigma test --coverage

# Code quality check
sigma lint

# Type checking
sigma typecheck
```

### Backup and Restore

```bash
# Create backup
sigma backup create --output backup.tar.gz

# List backups
sigma backup list

# Restore from backup
sigma backup restore backup.tar.gz

# Verify backup integrity
sigma backup verify backup.tar.gz
```

### Performance Tools

```bash
# Profile performance
sigma profile --duration 60

# Memory analysis
sigma memory analyze

# Optimize index
sigma optimize index

# Clear caches
sigma cache clear
```

## Command Options

### Global Options

```bash
--config PATH        Configuration file
--verbose, -v        Verbose output
--quiet, -q          Quiet mode
--help              Show help message
--version           Show version
--debug             Debug mode
--no-color          Disable colored output
```

### Output Formats

```bash
--format FORMAT     Output format (json, yaml, table, csv)
--output PATH       Output file path
--pretty            Pretty-print output
--compact           Compact output
```

## Configuration Files

### Priority Order

1. Command line options
2. Environment variables
3. User config file (`~/.sigma-nex/config.yaml`)
4. System config file (`/etc/sigma-nex/config.yaml`)
5. Default values

### Environment Variables

```bash
# Configuration
export SIGMA_CONFIG="/path/to/config.yaml"
export SIGMA_MODEL="mistral"
export SIGMA_DEBUG="true"

# Server settings
export SIGMA_HOST="0.0.0.0"
export SIGMA_PORT="8080"
export SIGMA_WORKERS="4"

# Paths
export SIGMA_DATA_DIR="/var/lib/sigma-nex"
export SIGMA_LOG_DIR="/var/log/sigma-nex"
export SIGMA_CACHE_DIR="/tmp/sigma-nex"
```

## Shell Completion

### Setup Bash Completion

```bash
# Add to ~/.bashrc
eval "$(_SIGMA_COMPLETE=bash_source sigma)"

# Or install system-wide
sigma --install-completion bash
```

### Zsh Completion

```bash
# Add to ~/.zshrc
eval "$(_SIGMA_COMPLETE=zsh_source sigma)"

# Or install system-wide
sigma --install-completion zsh
```

## Examples

### Basic Usage

```bash
# Simple question
sigma ask "Come misurare la pressione?"

# Medical emergency
sigma ask "Primo soccorso per shock anafilattico" --priority high

# Multi-language support
sigma ask "How to treat a burn?" --translate-to it
```

### Server Setup

```bash
# Development server
sigma server --debug --reload

# Production server with SSL
sigma server \
  --host 0.0.0.0 \
  --port 443 \
  --workers 4 \
  --ssl-cert cert.pem \
  --ssl-key key.pem \
  --config production.yaml
```

### Data Pipeline

```bash
# Complete data setup
sigma index build --source medical_docs/
sigma translate setup --languages en,es,fr
sigma models pull mistral medllama2
sigma server --config production.yaml
```

### Monitoring Setup

```bash
# Real-time monitoring
sigma monitor --metrics cpu,memory,requests &
sigma logs tail --filter ERROR &
sigma status --refresh 10
```

## Troubleshooting

### Common Issues

```bash
# Model not found
sigma models list  # Check available models
sigma models pull mistral  # Download missing model

# Permission errors
sigma config check  # Verify configuration
sudo chown -R $USER:$USER ~/.sigma-nex/  # Fix permissions

# Connection errors
sigma self-check  # Diagnose system
sigma status --detailed  # Check component status
```

### Debug Mode

```bash
# Enable verbose debugging
sigma --debug --verbose ask "test query"

# Check configuration
sigma config show --debug

# Trace command execution
SIGMA_TRACE=1 sigma ask "test"
```