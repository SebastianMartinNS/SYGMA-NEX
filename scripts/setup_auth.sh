#!/bin/bash
# setup_auth.sh - Script di configurazione autenticazione SIGMA-NEX
# Questo script aiuta a configurare le variabili d'ambiente per l'autenticazione

echo "================================================================================
███████╗██╗ ██████╗ ███╗   ███╗ █████╗       ███╗   ██╗███████╗██╗  ██╗
██╔════╝██║██╔════╝ ████╗ ████║██╔══██╗      ████╗  ██║██╔════╝╚██╗██╔╝
███████╗██║██║  ███╗██╔████╔██║███████║█████╗██╔██╗ ██║█████╗   ╚███╔╝
╚════██║██║██║   ██║██║╚██╔╝██║██╔══██║╚════╝██║╚██╗██║██╔══╝   ██╔██╗
███████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║      ██║ ╚████║███████╗██╔╝ ██╗
╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝      ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
================================================================================

              SIGMA-NEX Authentication Setup for Linux/macOS
              Developed by: Martin Sebastian | Email: rootedlab6@gmail.com
              Repository: https://github.com/SebastianMartinNS/SYGMA-NEX

================================================================================
"

# Verifica se siamo in ambiente virtuale
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "[OK] Ambiente virtuale attivato: $VIRTUAL_ENV"
else
    echo "[WARNING] Ambiente virtuale non rilevato. Assicurati di aver attivato il venv."
    echo "          python -m venv venv && source venv/bin/activate"
    echo ""
fi

# Verifica se le variabili sono già impostate
echo "Verifica variabili ambiente attuali:"
if [[ -n "$SIGMA_DEV_PASSWORD" ]]; then
    echo "[OK] SIGMA_DEV_PASSWORD: IMPOSTATA"
else
    echo "[MISSING] SIGMA_DEV_PASSWORD: NON IMPOSTATA"
fi

if [[ -n "$SIGMA_ADMIN_PASSWORD" ]]; then
    echo "[OK] SIGMA_ADMIN_PASSWORD: IMPOSTATA"
else
    echo "[MISSING] SIGMA_ADMIN_PASSWORD: NON IMPOSTATA"
fi
echo ""

# Richiedi configurazione
read -p "Vuoi configurare le password ora? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Configurazione annullata."
    exit 1
fi

echo ""
echo "================================================================================
                    IMPORTANTE - REQUISITI PASSWORD SICURE
================================================================================
Le password devono essere sicure con i seguenti requisiti:
- Minimo 8 caratteri
- Almeno una lettera maiuscola
- Almeno una lettera minuscola
- Almeno un numero
- Almeno un carattere speciale (!@#\$%^&*()-_=+[]{}|.<>?)

Non usare password comuni o prevedibili.
================================================================================
"

# Password dev
while true; do
    read -s -p "Inserisci password per utente DEV: " dev_pass
    echo
    if [[ ${#dev_pass} -lt 8 ]]; then
        echo "[ERROR] Password troppo corta (minimo 8 caratteri)"
        continue
    fi
    read -s -p "Conferma password DEV: " dev_pass_confirm
    echo
    if [[ "$dev_pass" != "$dev_pass_confirm" ]]; then
        echo "[ERROR] Le password non coincidono"
        continue
    fi
    echo "[OK] Password DEV accettata"
    break
done

# Password admin
while true; do
    read -s -p "Inserisci password per utente ADMIN: " admin_pass
    echo
    if [[ ${#admin_pass} -lt 8 ]]; then
        echo "[ERROR] Password troppo corta (minimo 8 caratteri)"
        continue
    fi
    read -s -p "Conferma password ADMIN: " admin_pass_confirm
    echo
    if [[ "$admin_pass" != "$admin_pass_confirm" ]]; then
        echo "[ERROR] Le password non coincidono"
        continue
    fi
    echo "[OK] Password ADMIN accettata"
    break
done

# Imposta le variabili
export SIGMA_DEV_PASSWORD="$dev_pass"
export SIGMA_ADMIN_PASSWORD="$admin_pass"

echo ""
echo "================================================================================
                    CONFIGURAZIONE COMPLETATA
================================================================================
[SUCCESS] Variabili ambiente impostate per questa sessione terminale
"

# Verifica configurazione
echo "=== Test Configurazione ==="
python3 -c "
import os
from sigma_nex.auth import login_cli

print('Variabili ambiente:')
print(f'  SIGMA_DEV_PASSWORD: {\"SET\" if os.getenv(\"SIGMA_DEV_PASSWORD\") else \"NOT SET\"}')
print(f'  SIGMA_ADMIN_PASSWORD: {\"SET\" if os.getenv(\"SIGMA_ADMIN_PASSWORD\") else \"NOT SET\"}')
print()

if os.getenv('SIGMA_DEV_PASSWORD'):
    success, token, error = login_cli('dev', os.getenv('SIGMA_DEV_PASSWORD'))
    print(f'Test login DEV: {\"SUCCESS\" if success else \"FAILED\"} - {error or \"OK\"}')

if os.getenv('SIGMA_ADMIN_PASSWORD'):
    success, token, error = login_cli('admin', os.getenv('SIGMA_ADMIN_PASSWORD'))
    print(f'Test login ADMIN: {\"SUCCESS\" if success else \"FAILED\"} - {error or \"OK\"}')
"

echo ""
echo "================================================================================
                    PROSSIMI PASSI
================================================================================
"
echo "NOTA: Queste variabili sono valide solo per questa sessione terminale."
echo ""
echo "Per impostarle permanentemente:"
echo ""
echo "1. Aggiungi al tuo ~/.bashrc o ~/.zshrc:"
echo "   export SIGMA_DEV_PASSWORD=\"$dev_pass\""
echo "   export SIGMA_ADMIN_PASSWORD=\"$admin_pass\""
echo ""
echo "2. Ricarica la configurazione:"
echo "   source ~/.bashrc  # o source ~/.zshrc"
echo ""
echo "3. Verifica la documentazione completa in: docs/config/authentication.md"