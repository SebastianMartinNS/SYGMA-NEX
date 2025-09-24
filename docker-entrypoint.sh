#!/bin/bash
# Docker entrypoint script per SIGMA-NEX

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logo ASCII
echo -e "${BLUE}"
cat << "EOF"
   ███████╗██╗ ██████╗ ███╗   ███╗ █████╗     ███╗   ██╗███████╗██╗  ██╗
   ██╔════╝██║██╔════╝ ████╗ ████║██╔══██╗    ████╗  ██║██╔════╝╚██╗██╔╝
   ███████╗██║██║  ███╗██╔████╔██║███████║    ██╔██╗ ██║█████╗   ╚███╔╝ 
   ╚════██║██║██║   ██║██║╚██╔╝██║██╔══██║    ██║╚██╗██║██╔══╝   ██╔██╗ 
   ███████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║    ██║ ╚████║███████╗██╔╝ ██╗
   ╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
EOF
echo -e "${NC}"

echo -e "${GREEN}SIGMA-NEX Container Starting...${NC}"
echo -e "${BLUE}   Sistema di Intelligenza Artificiale Autonomo${NC}"
echo -e "${BLUE}   per la Sopravvivenza Offline-First${NC}"
echo ""

# Funzione per logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verifica configurazione
check_config() {
    log_info "Verificando configurazione..."
    
    if [ ! -f "config.yaml" ]; then
        log_warn "File config.yaml non trovato, creando configurazione di default..."
        cat > config.yaml << EOF
model_name: "mistral"
temperature: 0.7
max_tokens: 2048
debug: false
retrieval_enabled: true
max_history: 100
translation_enabled: true

system_prompt: |
  Sei SIGMA-NEX, un agente cognitivo autonomo progettato per assistere in situazioni 
  di sopravvivenza e emergenza. Fornisci informazioni pratiche, concrete e sicure.
EOF
    fi
    
    log_info "✅ Configurazione verificata"
}

# Verifica dipendenze
check_dependencies() {
    log_info "Verificando dipendenze..."
    
    # Verifica Python packages
    python -c "import sigma_nex" 2>/dev/null || {
        log_error "SIGMA-NEX package non installato correttamente"
        exit 1
    }
    
    log_info "✅ Dipendenze verificate"
}

# Verifica Ollama (se richiesto)
check_ollama() {
    if [ "$ENABLE_OLLAMA" = "true" ]; then
        log_info "Verificando connessione Ollama..."
        
        OLLAMA_HOST=${OLLAMA_HOST:-"http://localhost:11434"}
        
        # Attendi che Ollama sia disponibile
        for i in {1..30}; do
            if curl -s "$OLLAMA_HOST/api/tags" >/dev/null 2>&1; then
                log_info "✅ Ollama connesso su $OLLAMA_HOST"
                return 0
            fi
            log_info "Attendendo Ollama... ($i/30)"
            sleep 2
        done
        
        log_warn "⚠️  Ollama non raggiungibile, continuando senza modelli locali"
    fi
}

# Inizializzazione dati
init_data() {
    log_info "Inizializzando dati..."
    
    # Crea directory necessarie
    mkdir -p logs data/cache
    
    # Verifica e crea indici FAISS se necessario
    if [ ! -f "data/moduli.index" ]; then
        log_info "Creando indici di ricerca..."
        python -c "
import os
os.environ['SIGMA_SKIP_OLLAMA'] = '1'
from sigma_nex.data_loader import initialize_index
initialize_index()
" 2>/dev/null || log_warn "Impossibile creare indici FAISS"
    fi
    
    log_info "✅ Dati inizializzati"
}

# Setup sicurezza
setup_security() {
    log_info "Configurando sicurezza..."
    
    # Imposta permessi file sensibili
    chmod 600 config.yaml 2>/dev/null || true
    chmod -R 755 data/ 2>/dev/null || true
    
    # Variabili di ambiente per sicurezza
    export SIGMA_SECURITY_MODE=${SIGMA_SECURITY_MODE:-"enabled"}
    export SIGMA_LOG_LEVEL=${SIGMA_LOG_LEVEL:-"INFO"}
    
    log_info "✅ Sicurezza configurata"
}

# Gestione segnali
cleanup() {
    log_info "Ricevuto segnale di terminazione, fermando SIGMA-NEX..."
    kill $PID 2>/dev/null || true
    wait $PID 2>/dev/null || true
    log_info "✅ SIGMA-NEX fermato correttamente"
    exit 0
}

# Registra gestori segnali
trap cleanup SIGTERM SIGINT SIGQUIT

# Main execution
main() {
    # Verifica se siamo in modalità help
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "SIGMA-NEX Docker Container"
        echo ""
        echo "Utilizzo:"
        echo "  docker run sigma-nex [comando] [opzioni]"
        echo ""
        echo "Comandi disponibili:"
        echo "  server          Avvia server API (default)"
        echo "  cli             Avvia modalità CLI interattiva"
        echo "  self-check      Verifica sistema"
        echo "  help            Mostra questo messaggio"
        echo ""
        echo "Variabili d'ambiente:"
        echo "  ENABLE_OLLAMA=true     Abilita controllo Ollama"
        echo "  OLLAMA_HOST=url        Host Ollama (default: http://localhost:11434)"
        echo "  SIGMA_LOG_LEVEL=level  Livello log (DEBUG,INFO,WARN,ERROR)"
        echo "  SIGMA_SECURITY_MODE    Modalità sicurezza (enabled/disabled)"
        echo ""
        exit 0
    fi
    
    # Esegui verifiche iniziali
    check_config
    check_dependencies
    check_ollama
    init_data
    setup_security
    
    # Determina comando da eseguire
    CMD="$1"
    shift || true
    
    case "$CMD" in
        "server"|"")
            log_info "Avviando SIGMA-NEX API Server..."
            exec sigma server --host 0.0.0.0 --port ${PORT:-8000} "$@" &
            ;;
        "cli")
            log_info "Avviando SIGMA-NEX CLI..."
            exec sigma start "$@" &
            ;;
        "self-check")
            log_info "Eseguendo self-check..."
            exec sigma self-check "$@"
            ;;
        "gui")
            log_error "❌ GUI non disponibile in container"
            exit 1
            ;;
        *)
            log_info "Eseguendo comando personalizzato: $CMD"
            exec sigma "$CMD" "$@" &
            ;;
    esac
    
    PID=$!
    log_info "✅ SIGMA-NEX avviato con PID $PID"
    
    # Attendi il processo principale
    wait $PID
}

# Avvia main con tutti gli argomenti
main "$@"