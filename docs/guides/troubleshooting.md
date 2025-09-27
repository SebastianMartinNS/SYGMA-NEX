# 🔧 Troubleshooting Guide

## Quick Diagnostics

### System Health Check

```bash
# Complete system check
sigma self-check

# Detailed system status
sigma self-check

# Component-specific checks
# Check Ollama: ollama list
# Check data: verify data/ directory
# Check models: ollama ps
```

### Common Issues Quick Fix

```bash
# Reset to working state
# Clean cache and temp files manually
# Reinitialize configuration

# Rebuild search index
# Verify data integrity manually

# Update all models
ollama pull mistral

# Clear all caches
# Remove temp files manually
```

## Installation Issues

### Python Version Problems

**Symptoms**: 
- "Python version not supported"
- Import errors on startup
- Syntax errors in code

**Solutions**:
```bash
# Check Python version
python --version

# Install correct Python version
pyenv install 3.11.0
pyenv global 3.11.0

# Reinstall SIGMA-NEX
pip uninstall sigma-nex
pip install sigma-nex
```

### Dependency Conflicts

**Symptoms**:
- Package import errors
- Version conflicts during installation
- Missing dependencies

**Solutions**:
```bash
# Create clean environment
python -m venv fresh_env
source fresh_env/bin/activate  # Linux/Mac
fresh_env\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip

# Install with no cache
pip install --no-cache-dir sigma-nex

# Fix specific conflicts
pip install --force-reinstall package-name
```

### Permission Issues

**Symptoms**:
- "Permission denied" errors
- Cannot create files/directories
- Config files not accessible

**Solutions**:
```bash
# Linux/Mac - Fix permissions
sudo chown -R $USER:$USER ~/.sigma-nex/
chmod -R 755 ~/.sigma-nex/

# Windows - Fix permissions
icacls C:\Users\%USERNAME%\.sigma-nex /grant %USERNAME%:F /T

# Run as administrator (Windows)
# Right-click PowerShell -> "Run as Administrator"
```

## Ollama Connection Issues

### Ollama Not Found

**Symptoms**:
- "Ollama not found" error
- Connection refused errors
- Model loading failures

**Diagnostics**:
```bash
# Check if Ollama is installed
which ollama
ollama --version

# Check Ollama service status
systemctl status ollama          # Linux
brew services list | grep ollama # macOS
```

**Solutions**:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh  # Linux/Mac
# Windows: Download from https://ollama.com/download

# Start Ollama service
sudo systemctl start ollama      # Linux
brew services start ollama       # macOS
ollama serve                     # Manual start

# Verify installation
ollama list
ollama pull mistral
```

### Model Loading Issues

**Symptoms**:
- "Model not found" errors
- Slow model loading
- Out of memory errors

**Diagnostics**:
```bash
# List available models
ollama list

# Check model details
ollama show mistral

# Monitor resource usage
ollama ps
htop  # or Task Manager on Windows
```

**Solutions**:
```bash
# Download missing models
ollama pull mistral
ollama pull medllama2

# Remove and reinstall model
ollama rm mistral
ollama pull mistral

# For memory issues
# Reduce model parameters in config.yaml:
# max_tokens: 1024
# temperature: 0.7
```

### Network Connectivity

**Symptoms**:
- Connection timeouts
- "Cannot connect to Ollama" errors
- Intermittent failures

**Diagnostics**:
```bash
# Test Ollama connection
curl http://localhost:11434/api/version

# Check network configuration
netstat -tlnp | grep 11434
ss -tlnp | grep 11434

# Test with different host/port
curl http://127.0.0.1:11434/api/version
```

**Solutions**:
```bash
# Configure Ollama host/port
export OLLAMA_HOST=0.0.0.0:11434

# Update SIGMA-NEX config in config.yaml:
# ollama:
#   host: localhost
#   port: 11434
#   timeout: 120

# Restart services
sudo systemctl restart ollama
sigma server restart
```

## Model and AI Issues

### Poor Response Quality

**Symptoms**:
- Irrelevant or nonsensical responses
- Repetitive outputs
- Off-topic answers

**Diagnostics**:
```bash
# Test with simple query
sigma start

# Check system health
sigma self-check
```

### Memory and Performance Issues

**Symptoms**:
- Slow response times
- Out of memory errors
- System freezing

**Diagnostics**:
```bash
# Monitor system resources
htop                           # Linux/Mac
Get-Process | Sort-Object CPU  # Windows PowerShell

# Check SIGMA-NEX memory usage
# Monitor process memory manually

# Profile performance
# Use system monitoring tools
```

**Solutions**:
```bash
# Restart system
# Check available memory
# Close other applications if needed
```

## GUI Issues

### GUI Won't Start

**Symptoms**:
- "tkinter not found" error
- GUI crashes on startup
- Blank or missing window

**Diagnostics**:
```bash
# Test tkinter installation
python -c "import tkinter; print('tkinter OK')"

# Test CustomTkinter
python -c "import customtkinter; print('CustomTkinter OK')"

# Check display settings (Linux)
echo $DISPLAY
xhost +localhost
```

**Solutions**:
```bash
# Install tkinter (Linux)
sudo apt-get install python3-tk     # Ubuntu/Debian
sudo yum install tkinter             # CentOS/RHEL

# Reinstall CustomTkinter
pip uninstall customtkinter
pip install customtkinter

# For Linux display issues
export DISPLAY=:0
xhost +localhost
```

### GUI Performance Issues

**Symptoms**:
- Slow response in GUI
- Freezing during queries
- High CPU usage

**Solutions**:
```bash
# Enable hardware acceleration
# Reduce UI effects
# Optimize thread usage
```

## Getting Help

### Documentation

```bash
# Check system health for diagnostics
sigma self-check
```

### Support Channels

- **GitHub Issues**: https://github.com/SebastianMartinNS/SYGMA-NEX/issues
- **Discussions**: https://github.com/SebastianMartinNS/SYGMA-NEX/discussions
- **Email Support**: rootedlab6@gmail.com
- **Emergency**: rootedlab6@gmail.com

### Bug Reports

When reporting bugs, include:

1. **System Information**:
   ```bash
   sigma --version
   python --version
   uname -a  # Linux/Mac
   systeminfo  # Windows
   ```

2. **Error Details**:
   - Exact error message
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### Performance Issues

For performance problems, provide system resource information and timing data.

This troubleshooting guide covers the most common issues. For specific problems not covered here, please consult the documentation or contact support.
