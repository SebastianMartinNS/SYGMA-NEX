#!/bin/bash
# Script per impostare la configurazione globale di SIGMA-NEX su Linux/macOS

echo "🚀 Configurazione globale SIGMA-NEX"
echo

# Installa la configurazione globale
echo "📦 Installazione configurazione globale..."
sigma install-config
if [ $? -ne 0 ]; then
    echo "❌ Errore durante l'installazione"
    exit 1
fi

echo
echo "🔧 Impostazione variabile d'ambiente..."

# Percorso di configurazione globale
GLOBAL_CONFIG_DIR="$HOME/.config/sigma-nex"

# Determina il file di profilo della shell
if [ -f "$HOME/.zshrc" ]; then
    PROFILE_FILE="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    PROFILE_FILE="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    PROFILE_FILE="$HOME/.bash_profile"
else
    PROFILE_FILE="$HOME/.profile"
fi

# Verifica se la variabile è già impostata
if grep -q "SIGMA_NEX_ROOT" "$PROFILE_FILE" 2>/dev/null; then
    echo "⚠️  SIGMA_NEX_ROOT già presente in $PROFILE_FILE"
    echo "🔄 Aggiornamento del percorso..."
    # Rimuove la vecchia impostazione
    sed -i.bak '/SIGMA_NEX_ROOT/d' "$PROFILE_FILE"
fi

# Aggiunge la nuova variabile d'ambiente
echo "export SIGMA_NEX_ROOT='$GLOBAL_CONFIG_DIR'" >> "$PROFILE_FILE"

echo "✅ Variabile d'ambiente SIGMA_NEX_ROOT aggiunta a $PROFILE_FILE"
echo "📍 Percorso: $GLOBAL_CONFIG_DIR"
echo

# Imposta la variabile per la sessione corrente
export SIGMA_NEX_ROOT="$GLOBAL_CONFIG_DIR"

echo "🎯 Ora puoi usare 'sigma' da qualsiasi directory!"
echo "💡 Riavvia il terminale o esegui: source $PROFILE_FILE"
echo
echo "✨ Configurazione completata!"