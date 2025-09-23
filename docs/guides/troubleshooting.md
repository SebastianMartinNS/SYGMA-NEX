# 🔧 Troubleshooting Guide

## Quick Diagnostics

### System Health Check

```bash
# Complete system check
sigma self-check

# Detailed system status
sigma status --detailed

# Component-specific checks
sigma status ollama
sigma status index
sigma status models
```

### Common Issues Quick Fix

```bash
# Reset to working state
sigma setup clean && sigma setup init

# Rebuild search index
sigma index rebuild --force

# Update all models
sigma models update --all

# Clear all caches
sigma cache clear --all
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
# Reduce model size or increase system RAM
sigma config set max_tokens 1024
sigma config set temperature 0.7
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

# Update SIGMA-NEX config
sigma config set ollama.host localhost
sigma config set ollama.port 11434
sigma config set ollama.timeout 120

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
sigma ask "Test query" --debug

# Check model configuration
sigma config show | grep -A5 model

# Verify model version
ollama show mistral
```

**Solutions**:
```bash
# Adjust model parameters
sigma config set temperature 0.7    # Reduce for more focused responses
sigma config set top_p 0.9          # Adjust nucleus sampling
sigma config set max_tokens 2048    # Increase for longer responses

# Try different model
sigma config set model_name llama2
ollama pull llama2

# Reset system prompt
sigma config set system_prompt default
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
sigma status --resources

# Profile performance
sigma profile --duration 60
```

**Solutions**:
```bash
# Reduce memory usage
sigma config set max_history 50
sigma config set retrieval_top_k 3
sigma config set embedding_batch_size 16

# Clear caches
sigma cache clear
rm -rf ~/.sigma-nex/cache/*

# Optimize index
sigma index optimize

# Restart with limited workers
sigma server --workers 1
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

# For Windows display scaling
sigma gui --scale-factor 1.0
```

### GUI Performance Issues

**Symptoms**:
- Slow response in GUI
- Freezing during queries
- High CPU usage

**Solutions**:
```bash
# Enable hardware acceleration
sigma config set gui.hardware_acceleration true

# Reduce UI effects
sigma config set gui.animations false
sigma config set gui.transparency false

# Optimize thread usage
sigma config set gui.worker_threads 2
```

## Search and Retrieval Issues

### Index Problems

**Symptoms**:
- "Index not found" errors
- Poor search results
- Search returning no results

**Diagnostics**:
```bash
# Check index status
sigma index stats

# Verify index files
ls -la ~/.sigma-nex/data/
file ~/.sigma-nex/data/moduli.index

# Test search manually
sigma search "test query" --debug
```

**Solutions**:
```bash
# Rebuild index
sigma index rebuild --force

# Re-import data
sigma data import data/ --format json --rebuild

# Check data integrity
sigma data verify

# Update embeddings model
sigma config set embedding.model "all-MiniLM-L6-v2"
```

### Poor Search Quality

**Symptoms**:
- Irrelevant search results
- Missing relevant documents
- Inconsistent results

**Solutions**:
```bash
# Adjust search parameters
sigma config set retrieval_top_k 10
sigma config set similarity_threshold 0.6

# Update embedding model
sigma models update embeddings

# Reprocess documents with better chunking
sigma data reprocess --chunk-size 512 --overlap 50
```

## API and Server Issues

### Server Won't Start

**Symptoms**:
- "Port already in use" error
- Server crashes on startup
- Cannot bind to address

**Diagnostics**:
```bash
# Check port usage
netstat -tlnp | grep 8000        # Linux
netstat -an | findstr 8000       # Windows
lsof -i :8000                    # macOS

# Test server manually
sigma server --debug --port 8001
```

**Solutions**:
```bash
# Kill process using port
sudo kill -9 $(lsof -t -i:8000)  # Unix
netstat -ano | findstr :8000     # Windows (find PID, then taskkill)

# Use different port
sigma server --port 8001

# Configure different host
sigma server --host 127.0.0.1 --port 8000
```

### API Errors

**Symptoms**:
- HTTP 500 errors
- Connection timeouts
- Malformed responses

**Diagnostics**:
```bash
# Test API manually
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}'

# Check server logs
sigma logs tail --server

# Debug API calls
sigma server --debug --log-level DEBUG
```

**Solutions**:
```bash
# Restart server
sigma server restart

# Clear server cache
sigma cache clear --server

# Update server configuration
sigma config set server.timeout 60
sigma config set server.workers 2
```

## Translation Issues

### Translation Not Working

**Symptoms**:
- "Translation model not found"
- Poor translation quality
- Translation errors

**Diagnostics**:
```bash
# Test translation manually
sigma translate test --source en --target it --text "Hello"

# Check translation models
ls -la ~/.cache/huggingface/transformers/

# Verify language support
sigma translate languages
```

**Solutions**:
```bash
# Download translation models
sigma translate setup --languages en,es,fr,de

# Clear translation cache
rm -rf ~/.cache/huggingface/

# Update translation configuration
sigma config set translation.model "Helsinki-NLP/opus-mt"
sigma config set translation.cache_size 1000
```

## Configuration Issues

### Config File Problems

**Symptoms**:
- "Config file not found"
- YAML parsing errors
- Invalid configuration values

**Diagnostics**:
```bash
# Validate configuration
sigma config validate

# Show effective configuration
sigma config show --resolved

# Check config file location
sigma config show --sources
```

**Solutions**:
```bash
# Create default config
sigma config init --force

# Fix YAML syntax
# Use online YAML validator or:
python -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Reset to defaults
sigma config reset --confirm
```

### Environment Variables

**Symptoms**:
- Config not loading from environment
- Environment variables ignored
- Inconsistent behavior

**Solutions**:
```bash
# Check environment variables
env | grep SIGMA

# Set environment variables correctly
export SIGMA_CONFIG="/path/to/config.yaml"
export SIGMA_DEBUG="true"
export SIGMA_LOG_LEVEL="DEBUG"

# Windows equivalent
set SIGMA_CONFIG=C:\path\to\config.yaml
setx SIGMA_DEBUG true
```

## Logging and Debugging

### Enable Debug Mode

```bash
# Enable debug globally
sigma config set debug true
sigma config set log_level DEBUG

# Debug specific component
sigma --debug ask "test query"
sigma server --debug --reload

# Trace execution
SIGMA_TRACE=1 sigma ask "test query"
```

### Log Analysis

```bash
# View recent logs
sigma logs show --last 100

# Filter by level
sigma logs show --level ERROR

# Search logs
sigma logs search "error" --last 24h

# Follow logs in real-time
sigma logs tail -f

# Export logs for analysis
sigma logs export --format json --output debug-logs.json
```

### Debug Information Collection

```bash
# Collect debug information
sigma diagnose --full --output debug-info.json

# System information
sigma status --detailed --json

# Performance profiling
sigma profile --duration 60 --output profile.json
```

## Getting Help

### Documentation

```bash
# Open documentation
sigma docs open

# Command-specific help
sigma ask --help
sigma server --help

# Configuration reference
sigma config help
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

2. **Configuration**:
   ```bash
   sigma config show --anonymized
   ```

3. **Debug Logs**:
   ```bash
   sigma logs export --level DEBUG --last 1h
   ```

4. **Error Details**:
   - Exact error message
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### Performance Issues

For performance problems, provide:

```bash
# System resources
sigma status --resources

# Performance profile
sigma profile --duration 300

# Memory analysis
sigma memory analyze

# Query timing
time sigma ask "test query"
```

This troubleshooting guide covers the most common issues. For specific problems not covered here, please consult the documentation or contact support.