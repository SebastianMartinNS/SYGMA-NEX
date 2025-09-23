# 🚀 SIGMA-NEX Deployment Guide

## Panoramica

Guida completa per il deployment di SIGMA-NEX in ambienti di produzione, sviluppo e testing.

## 🐳 Docker Deployment (Raccomandato)

### Production Deployment
```bash
# Clone repository
git clone https://github.com/SebastianMartinNS/SYGMA-NEX.git
cd SYGMA-NEX

# Build e deploy
docker-compose up -d

# Verifica salute del sistema
curl http://localhost:8000/
```

### Development Deployment
```bash
# Usa configurazione di sviluppo
docker-compose -f docker-compose.dev.yml up
```

### Configuration Files
```yaml
# docker-compose.yml (Production)
version: '3.8'
services:
  sigma-nex:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 🖥️ Traditional Deployment

### System Requirements
- **OS**: Ubuntu 20.04+, Windows 10+, macOS 11+
- **Python**: 3.10+
- **RAM**: Minimo 8GB, raccomandati 16GB+
- **Storage**: 10GB spazio libero
- **Network**: Accesso localhost per Ollama

### Installation Steps
```bash
# 1. Clone repository
git clone https://github.com/SebastianMartinNS/SYGMA-NEX.git
cd SYGMA-NEX

# 2. Setup Python environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 5. Download models
ollama pull mistral
ollama pull medllama2

# 6. Verify installation
sigma self-check
```

## ⚙️ Configuration

### Environment Variables
```bash
# Production settings
export SIGMA_ENV=production
export SIGMA_LOG_LEVEL=INFO
export SIGMA_MODEL_NAME=mistral
export SIGMA_MAX_HISTORY=100
export SIGMA_RETRIEVAL_ENABLED=true
```

### Config Files
```yaml
# config.production.yaml
model_name: "mistral"
temperature: 0.7
max_tokens: 2048
debug: false
retrieval_enabled: true
max_history: 100
log_level: "INFO"

security:
  encryption_enabled: true
  rate_limiting: true
  audit_logging: true
  ip_whitelist: ["127.0.0.1", "192.168.0.0/16"]

ollama:
  host: "localhost"
  port: 11434
  timeout: 120
```

### Secrets Management
```bash
# Usa environment variables per secrets
export SIGMA_ENCRYPTION_KEY="your-32-char-key-here"
export SIGMA_API_KEY="your-api-key-here"
export SIGMA_DB_PASSWORD="your-db-password"
```

## 🌐 Cloud Deployment

### AWS Deployment
```yaml
# docker-compose.aws.yml
version: '3.8'
services:
  sigma-nex:
    image: sigma-nex:latest
    ports:
      - "80:8000"
    environment:
      - AWS_REGION=us-east-1
      - LOG_GROUP=sigma-nex-logs
    volumes:
      - /opt/sigma-nex/data:/app/data
      - /var/log/sigma-nex:/app/logs
```

### Azure Container Instances
```bash
# Deploy to Azure
az container create \
  --resource-group sigma-nex-rg \
  --name sigma-nex \
  --image sigma-nex:latest \
  --dns-name-label sigma-nex \
  --ports 8000 \
  --environment-variables ENVIRONMENT=production
```

### Google Cloud Run
```yaml
# cloudbuild.yaml
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/sigma-nex', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/sigma-nex']
- name: 'gcr.io/cloud-builders/gcloud'
  args:
  - 'run'
  - 'deploy'
  - 'sigma-nex'
  - '--image'
  - 'gcr.io/$PROJECT_ID/sigma-nex'
  - '--region'
  - 'us-central1'
  - '--platform'
  - 'managed'
```

## 🔧 Service Management

### Systemd Service (Linux)
```ini
# /etc/systemd/system/sigma-nex.service
[Unit]
Description=SIGMA-NEX AI Agent
After=network.target

[Service]
Type=simple
User=sigma-nex
WorkingDirectory=/opt/sigma-nex
Environment=PATH=/opt/sigma-nex/venv/bin
ExecStart=/opt/sigma-nex/venv/bin/sigma server --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable sigma-nex
sudo systemctl start sigma-nex
sudo systemctl status sigma-nex
```

### Windows Service
```batch
# install-service.bat
sc create SigmaNex binPath= "C:\sigma-nex\venv\Scripts\sigma.exe server --host 0.0.0.0 --port 8000"
sc config SigmaNex start= auto
sc start SigmaNex
```

## 📊 Monitoring

### Health Checks
```bash
# Basic health check
curl -f http://localhost:8000/ || exit 1

# Detailed health check
curl http://localhost:8000/health | jq '.status'
```

### Logging
```yaml
# logging.yaml
version: 1
formatters:
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  file:
    class: logging.handlers.RotatingFileHandler
    filename: /app/logs/sigma-nex.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
    formatter: detailed
  console:
    class: logging.StreamHandler
    formatter: detailed
loggers:
  sigma_nex:
    level: INFO
    handlers: [file, console]
    propagate: false
```

### Metrics Collection
```python
# metrics.py
import time
import psutil
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter('sigma_requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('sigma_request_duration_seconds', 'Request latency')
SYSTEM_MEMORY = Gauge('sigma_memory_usage_bytes', 'Memory usage')
```

## 🔒 Security Deployment

### SSL/TLS Configuration
```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name sigma-nex.example.com;
    
    ssl_certificate /etc/ssl/certs/sigma-nex.crt;
    ssl_certificate_key /etc/ssl/private/sigma-nex.key;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Firewall Rules
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8000/tcp  # SIGMA-NEX (interno)
sudo ufw enable

# iptables
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --dport 8000 -s 127.0.0.1 -j ACCEPT
```

### Container Security
```dockerfile
# Dockerfile security best practices
FROM python:3.11-slim AS base

# Create non-root user
RUN adduser --disabled-password --gecos '' sigma-nex

# Set security options
USER sigma-nex
WORKDIR /app

# Copy and install dependencies
COPY --chown=sigma-nex:sigma-nex requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=sigma-nex:sigma-nex . .

# Security scan
RUN pip install safety && safety check

EXPOSE 8000
CMD ["sigma", "server", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 Performance Optimization

### Production Settings
```yaml
# config.production.yaml
performance:
  workers: 4                    # CPU cores
  worker_connections: 1000      # Max connections per worker
  keepalive_timeout: 65        # Keep connections alive
  max_requests: 1000           # Requests per worker before restart
  preload_models: true         # Load models at startup
  
caching:
  enabled: true
  redis_url: "redis://localhost:6379"
  ttl: 3600                    # Cache TTL in seconds
  
database:
  pool_size: 20                # Connection pool size
  max_overflow: 30             # Max overflow connections
```

### Resource Limits
```yaml
# docker-compose.yml
services:
  sigma-nex:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

## 🔄 Backup and Recovery

### Data Backup
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/sigma-nex"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup data and configuration
tar -czf $BACKUP_DIR/sigma-nex-data-$DATE.tar.gz \
  /opt/sigma-nex/data/ \
  /opt/sigma-nex/config.yaml \
  /opt/sigma-nex/logs/

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Database Backup
```bash
# backup-db.sh
pg_dump sigma_nex > /backups/sigma-nex-db-$(date +%Y%m%d).sql
```

### Recovery Procedure
```bash
# restore.sh
BACKUP_FILE=$1
if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: $0 <backup_file>"
  exit 1
fi

# Stop service
sudo systemctl stop sigma-nex

# Restore data
tar -xzf $BACKUP_FILE -C /

# Restart service
sudo systemctl start sigma-nex
```

## 🚨 Troubleshooting

### Common Issues

#### Ollama Connection Failed
```bash
# Check Ollama status
systemctl status ollama

# Restart Ollama
sudo systemctl restart ollama

# Check models
ollama list
```

#### Memory Issues
```bash
# Check memory usage
free -h
docker stats sigma-nex

# Optimize memory
echo 3 > /proc/sys/vm/drop_caches
```

#### Port Conflicts
```bash
# Find process using port
lsof -i :8000
netstat -tulpn | grep :8000

# Kill process
kill -9 <PID>
```

### Log Analysis
```bash
# View logs
tail -f /app/logs/sigma-nex.log

# Search errors
grep -i error /app/logs/sigma-nex.log

# Analyze access patterns
awk '{print $1}' /app/logs/access.log | sort | uniq -c | sort -nr
```

## 📞 Support

### Deployment Support
- **Email**: deployment@sigma-nex.org
- **Documentation**: https://github.com/SebastianMartinNS/SYGMA-NEX/wiki
- **Issues**: https://github.com/SebastianMartinNS/SYGMA-NEX/issues

### Emergency Contacts
- **Critical Issues**: emergency@sigma-nex.org
- **Security Issues**: security@sigma-nex.org
- **24/7 Support**: +1-xxx-xxx-xxxx (Enterprise only)

---

**Autore**: Martin Sebastian  
**Versione**: 0.2.1  
**Ultimo aggiornamento**: 23 Settembre 2025