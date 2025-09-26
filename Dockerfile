# Dockerfile per SIGMA-NEX
# Base image con Python 3.11
FROM python:3.11-slim as base

# Metadata
LABEL maintainer="Sebastian Martin <rootedlab6@gmail.com>"
LABEL version="0.3.5"
LABEL description="SIGMA-NEX - Sistema di Intelligenza Artificiale Autonomo per la Sopravvivenza Offline-First"

# Variabili di ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    curl \
    git \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crea utente non-root per sicurezza
RUN groupadd -r sigma && useradd -r -g sigma -m sigma

# Directory di lavoro
WORKDIR /app

# Copia requirements e installa dipendenze Python
COPY requirements.txt requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Development stage (per sviluppo locale)
FROM base as development

# Installa dipendenze di sviluppo
RUN pip install --no-cache-dir -r requirements-test.txt

# Installa Ollama con gestione errori
RUN curl -fsSL https://ollama.ai/install.sh | sh || echo "⚠️ Ollama installation failed, continuing without it"

# Copia tutto il codice sorgente
COPY --chown=sigma:sigma . .

# Installa il package in modalità development
RUN pip install -e .

# Cambia all'utente sigma
USER sigma

# Espone porte
EXPOSE 8000 11434

# Comando di default per development
CMD ["python", "-m", "sigma_nex", "server", "--host", "0.0.0.0", "--port", "8000"]

# Production stage (per deployment)
FROM base as production

# Copia solo il codice necessario
COPY --chown=sigma:sigma setup.py pyproject.toml README.md LICENSE CHANGELOG.md ./
COPY --chown=sigma:sigma sigma_nex/ ./sigma_nex/
COPY --chown=sigma:sigma data/ ./data/
COPY --chown=sigma:sigma config.yaml ./

# Installa il package
RUN pip install .

# Cambia all'utente sigma
USER sigma

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Espone porta
EXPOSE 8000

# Comando di default per production
CMD ["python", "-m", "sigma_nex", "server", "--host", "0.0.0.0", "--port", "8000"]

# Multi-arch build support
FROM production as final

# Copia script di entrypoint
COPY --chown=sigma:sigma docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["server"]