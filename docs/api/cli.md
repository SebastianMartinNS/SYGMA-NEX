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

## Authentication Commands

### Login

```bash
# Login as public user
sigma login -u user

# Login as developer (requires SIGMA_DEV_PASSWORD env var)
sigma login -u dev

# Login as admin (requires SIGMA_ADMIN_PASSWORD env var)
sigma login -u admin

# Login with password prompt
sigma login -u dev -p
```

### Logout

```bash
# Logout and clear session
sigma logout
```

## Protected Commands

The following commands require authentication:

### Configuration Management

```bash
# Load framework (requires config permission)
sigma load-framework --path framework.json

# Self-heal code (requires config permission)
sigma self-heal --file script.py

# Install global config (requires admin permission)
sigma install-config

# Remove global config (requires admin permission)
sigma install-config --uninstall
```

### Server Management

```bash
# Start API server (requires admin permission)
sigma server --host 0.0.0.0 --port 8000
```

### GUI Management

```bash
# Start graphical interface (requires config permission)
sigma gui
```

### Update Management

```bash
# Update SIGMA-NEX (requires admin permission)
sigma update

# Check for updates without installing
sigma update --check-only
```

## Core Commands

### Interactive Mode

```bash
# Start interactive session
sigma start

# Start with custom config
sigma start --config config.production.yaml
```

### Server Commands

```bash
# Start API server
sigma server

# Custom host and port
sigma server --host 0.0.0.0 --port 8080
```

### GUI Commands

```bash
# Start graphical interface
sigma gui
```

### System Management

```bash
# System health check
sigma self-check

# Code analysis and healing
sigma self-heal --file script.py

# Update system
sigma update

# Install global configuration
sigma install-config

# Remove global configuration
sigma install-config --uninstall
```

### Data Management

```bash
# Load framework data
sigma load-framework --path /path/to/Framework_SIGMA.json
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
export SIGMA_DEBUG="true"

# Server settings
export SIGMA_HOST="0.0.0.0"
export SIGMA_PORT="8080"

# Authentication
export SIGMA_DEV_PASSWORD="your_secure_dev_password"
export SIGMA_ADMIN_PASSWORD="your_secure_admin_password"

# Paths
export SIGMA_DATA_DIR="/var/lib/sigma-nex"
export SIGMA_LOG_DIR="/var/log/sigma-nex"
```

## Examples

### Basic Usage

```bash
# Start interactive mode
sigma start

# Start server
sigma server --host 0.0.0.0 --port 8000

# Start GUI
sigma gui
```

### Authentication

```bash
# Login as developer
sigma login -u dev

# Login with password
sigma login -u admin -p

# Logout
sigma logout
```

### System Management

```bash
# Check system health
sigma self-check

# Analyze and improve code
sigma self-heal --file my_script.py

# Update system
sigma update

# Install global config
sigma install-config
```

### Data Operations

```bash
# Load framework
sigma load-framework --path Framework_SIGMA.json
```

## Troubleshooting

### Common Issues

```bash
# Permission errors
sudo chown -R $USER:$USER ~/.sigma-nex/  # Fix permissions

# Connection errors
sigma self-check  # Diagnose system
```

### Debug Mode

```bash
# Enable verbose debugging
sigma --debug --verbose start

# Check configuration
sigma --debug self-check
```
