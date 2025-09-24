# Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 11+, Ubuntu 18.04+
- **Python**: 3.10 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **Network**: Internet connection for initial setup

### Recommended Requirements
- **RAM**: 32GB for optimal performance
- **Storage**: SSD with 20GB+ free space
- **CPU**: Multi-core processor (4+ cores)
- **GPU**: NVIDIA GPU with CUDA support (optional)

## Installation Methods

### Method 1: Source Installation (Current)

```bash
# Clone repository
git clone https://github.com/SebastianMartinNS/SYGMA-NEX.git
cd SYGMA-NEX

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

## Platform-Specific Instructions

### Windows Installation

#### Prerequisites
```powershell
# Install Python 3.10+
winget install Python.Python.3.11

# Install Git
winget install Git.Git

# Install Visual C++ Redistributable
winget install Microsoft.VCRedist.2015+.x64
```

#### Installation Steps
```powershell
# Open PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install SIGMA-NEX
pip install sigma-nex

# Setup Windows service (optional)
sigma setup service --install
```

#### Windows-Specific Configuration
```yaml
# config.yaml - Windows paths
paths:
  data_dir: "C:\\ProgramData\\SigmaNex\\data"
  log_dir: "C:\\ProgramData\\SigmaNex\\logs"
  temp_dir: "C:\\Temp\\SigmaNex"

# Windows service settings
service:
  name: "SigmaNex"
  display_name: "SIGMA-NEX AI Agent"
  start_type: "auto"
```

### macOS Installation

#### Prerequisites
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install Git
brew install git
```

#### Installation Steps
```bash
# Install SIGMA-NEX
pip3 install sigma-nex

# Setup macOS service (optional)
sigma setup service --install --user
```

#### macOS-Specific Configuration
```yaml
# config.yaml - macOS paths
paths:
  data_dir: "~/Library/Application Support/SigmaNex"
  log_dir: "~/Library/Logs/SigmaNex"
  temp_dir: "/tmp/SigmaNex"

# LaunchAgent settings
service:
  plist_path: "~/Library/LaunchAgents/com.sigma-nex.agent.plist"
  auto_start: true
```

### Linux Installation

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install dependencies
sudo apt install python3.11 python3.11-venv python3-pip git curl

# Install SIGMA-NEX
pip3 install sigma-nex

# Setup systemd service (optional)
sudo sigma setup service --install --system
```

#### CentOS/RHEL/Fedora
```bash
# Install dependencies
sudo dnf install python3.11 python3-pip git curl

# Install SIGMA-NEX
pip3 install sigma-nex
```

#### Arch Linux
```bash
# Install dependencies
sudo pacman -S python python-pip git curl

# Install SIGMA-NEX
pip install sigma-nex
```

## Dependency Installation

### Core Dependencies

SIGMA-NEX will automatically install core dependencies:
- `click`: CLI framework
- `pyyaml`: Configuration management
- `torch`: PyTorch for ML models
- `transformers`: Hugging Face transformers
- `faiss-cpu`: Vector similarity search
- `cryptography`: Security features
- `fastapi`: Web API framework
- `uvicorn`: ASGI server
- `pydantic`: Data validation
- `requests`: HTTP client
- `customtkinter`: Modern GUI framework
- `sentence-transformers`: Sentence embeddings

### AI Model Dependencies

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh  # Linux/Mac
# or download from https://ollama.com/download    # Windows

# Pull required models
ollama pull mistral
```

### Development Dependencies

```bash
# Development tools
pip install pytest pytest-cov pytest-mock pytest-asyncio coverage black isort flake8
```

## Configuration Setup

### Initial Configuration

```bash
# Generate default configuration
sigma config init

# Edit configuration
sigma config edit

# Validate configuration
sigma config validate
```

### Basic Configuration File

```yaml
# ~/.sigma-nex/config.yaml
model_name: "mistral"
temperature: 0.7
max_tokens: 2048
debug: false
retrieval_enabled: true
max_history: 100

# Paths
data_dir: "~/.sigma-nex/data"
log_dir: "~/.sigma-nex/logs"

# Server settings
server:
  host: "127.0.0.1"
  port: 8000
  workers: 1

# Security
security:
  encryption_enabled: true
  rate_limiting: false
  audit_logging: true
```

## Post-Installation Setup

### Verify Installation

```bash
# Check version
sigma --version

# System health check
sigma self-check

# Test basic functionality
sigma ask "Test query"
```

### Download Additional Data

```bash
# Download medical frameworks
sigma data download medical

# Build search index
sigma index build

# Setup translation models
sigma translate setup
```

### Initial Data Import

```bash
# Import medical documents
sigma data import medical_docs/ --type medical

# Import FAQs
sigma data import faq.json --type faq

# Build initial index
sigma index rebuild
```

## Service Setup

### Linux Systemd Service

```bash
# Install service
sudo sigma setup service --install --system

# Enable auto-start
sudo systemctl enable sigma-nex

# Start service
sudo systemctl start sigma-nex

# Check status
sudo systemctl status sigma-nex
```

### Windows Service

```powershell
# Install as Windows service
sigma setup service --install

# Start service
sc start SigmaNex

# Check status
sc query SigmaNex
```

### Docker Service

```yaml
# docker-compose.yml
version: '3.8'
services:
  sigma-nex:
    image: ghcr.io/sebastianmartinns/sygma-nex:latest
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./config.yaml:/app/config.yaml
    restart: unless-stopped
    environment:
      - SIGMA_CONFIG=/app/config.yaml
```

## Troubleshooting Installation

### Common Issues

#### Python Version Issues
```bash
# Check Python version
python --version

# Install specific Python version
pyenv install 3.11.0
pyenv global 3.11.0
```

#### Dependency Conflicts
```bash
# Create clean virtual environment
python -m venv fresh_venv
source fresh_venv/bin/activate
pip install --upgrade pip
pip install sigma-nex
```

#### Permission Issues
```bash
# Fix permissions (Linux/Mac)
sudo chown -R $USER:$USER ~/.sigma-nex/

# Windows equivalent
icacls C:\Users\%USERNAME%\.sigma-nex /grant %USERNAME%:F /T
```

#### Ollama Connection Issues
```bash
# Check Ollama status
ollama list

# Restart Ollama service
sudo systemctl restart ollama  # Linux
brew services restart ollama   # macOS
```

### Log Analysis

```bash
# Check installation logs
sigma logs show --level INFO --grep "install"

# System diagnostics
sigma diagnose --full

# Component status
sigma status --detailed
```

## Upgrade Instructions

### Upgrade SIGMA-NEX

```bash
# Backup current installation
sigma backup create pre-upgrade-backup.tar.gz

# Upgrade to latest version
pip install --upgrade sigma-nex

# Migrate configuration if needed
sigma config migrate

# Verify upgrade
sigma self-check
```

### Rollback Instructions

```bash
# Install specific version
pip install sigma-nex==0.2.0

# Restore from backup
sigma backup restore pre-upgrade-backup.tar.gz
```

## Next Steps

After successful installation:

1. **[Basic Configuration](configuration.md)** - Configure SIGMA-NEX for your needs
2. **[CLI Guide](../guides/cli-guide.md)** - Learn command-line usage
3. **[GUI Guide](../guides/gui-guide.md)** - Explore the graphical interface
4. **[API Usage](../guides/api-usage.md)** - Integrate with the REST API
5. **[Testing Guide](../TESTING.md)** - Verify your installation

## Support

For installation issues:
- **Documentation**: https://github.com/SebastianMartinNS/SYGMA-NEX/wiki
- **Issues**: https://github.com/SebastianMartinNS/SYGMA-NEX/issues
- **Email**: rootedlab6@gmail.com