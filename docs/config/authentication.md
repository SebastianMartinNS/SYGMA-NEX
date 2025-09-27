# Configurazione Autenticazione SIGMA-NEX

## Variabili d'Ambiente Richieste

Il sistema richiede due variabili d'ambiente per l'autenticazione sicura:

### SIGMA_DEV_PASSWORD
- **Scopo**: Password per l'utente sviluppatore
- **Permessi**: Accesso completo tranne funzioni amministrative
- **Utilizzo**: Per sviluppo, testing e manutenzione

### SIGMA_ADMIN_PASSWORD
- **Scopo**: Password per l'utente amministratore
- **Permessi**: Accesso completo a tutte le funzioni
- **Utilizzo**: Per configurazione e gestione avanzata

## Come Impostare le Variabili

### Windows (Temporaneo - Sessione Corrente)
```cmd
set SIGMA_DEV_PASSWORD=your_secure_dev_password
set SIGMA_ADMIN_PASSWORD=your_secure_admin_password
```

### Windows (Permanente - Sistema)
```cmd
setx SIGMA_DEV_PASSWORD "your_secure_dev_password" /M
setx SIGMA_ADMIN_PASSWORD "your_secure_admin_password" /M
```

### Linux/macOS (Temporaneo)
```bash
export SIGMA_DEV_PASSWORD=your_secure_dev_password
export SIGMA_ADMIN_PASSWORD=your_secure_admin_password
```

### Linux/macOS (Permanente)
Aggiungi al file `~/.bashrc` o `~/.zshrc`:
```bash
export SIGMA_DEV_PASSWORD=your_secure_dev_password
export SIGMA_ADMIN_PASSWORD=your_secure_admin_password
```

## Sicurezza delle Password

### Requisiti Minimi
- Lunghezza minima: 8 caratteri
- Caratteri misti: lettere maiuscole, minuscole, numeri, simboli
- Non usare: password comuni, date di nascita, nomi

### Esempi Sicuri
```bash
export SIGMA_DEV_PASSWORD="YourSecureDevPassword123!"
export SIGMA_ADMIN_PASSWORD="YourSecureAdminPassword456!"
```

## Verifica Configurazione

Testa che le variabili siano impostate correttamente:

```bash
# Windows
echo %SIGMA_DEV_PASSWORD%
echo %SIGMA_ADMIN_PASSWORD%

# Linux/macOS
echo $SIGMA_DEV_PASSWORD
echo $SIGMA_ADMIN_PASSWORD
```

## Cosa Deve Fare Chi Clona il Repository

### 1. Dopo il Clone
```bash
git clone https://github.com/SebastianMartinNS/SYGMA-NEX.git
cd SYGMA-NEX
```

### 2. Installazione Dipendenze
```bash
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 3. Configurazione Ambiente Virtuale
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 4. Impostazione Variabili d'Ambiente
Segui le istruzioni sopra per impostare `SIGMA_DEV_PASSWORD` e `SIGMA_ADMIN_PASSWORD`.

### 5. Verifica Installazione
```bash
# Test autenticazione
python -c "
from sigma_nex.auth import login_cli
import os

# Verifica variabili
print('DEV password set:', bool(os.getenv('SIGMA_DEV_PASSWORD')))
print('ADMIN password set:', bool(os.getenv('SIGMA_ADMIN_PASSWORD')))

# Test login se variabili impostate
if os.getenv('SIGMA_DEV_PASSWORD'):
    success, token, error = login_cli('dev', os.getenv('SIGMA_DEV_PASSWORD'))
    print('Dev login test:', success)
if os.getenv('SIGMA_ADMIN_PASSWORD'):
    success, token, error = login_cli('admin', os.getenv('SIGMA_ADMIN_PASSWORD'))
    print('Admin login test:', success)
"
```

### 6. Esecuzione Test
```bash
pytest tests/unit/test_auth_realistic.py -v
```

## Note di Sicurezza

- **Mai committare** le password nel codice o nei file di configurazione
- **Usare password diverse** per ambiente di sviluppo e produzione
- **Ruotare regolarmente** le password
- **Non condividere** le credenziali con altri sviluppatori
- **Usare un password manager** per gestire le credenziali sicure

## Troubleshooting

### Errore: "Environment variable SIGMA_DEV_PASSWORD not set"
- Verifica che la variabile sia impostata correttamente
- Riavvia il terminale se impostata permanentemente
- Controlla maiuscole/minuscole nel nome della variabile

### Errore: "Invalid credentials"
- Verifica che la password corrisponda esattamente al valore della variabile
- Controlla che non ci siano spazi extra

### Test Falliti
- Assicurati che l'ambiente virtuale sia attivato
- Verifica che tutte le dipendenze siano installate
- Controlla che le variabili d'ambiente siano accessibili dal processo Python</content>
<parameter name="filePath">c:\Users\senti\OneDrive\Desktop\sigma_nex_interactive\docs\config\authentication.md
