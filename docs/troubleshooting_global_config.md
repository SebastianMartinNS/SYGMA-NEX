# Risoluzione Problemi - Uso Globale di SIGMA-NEX

## Problema: Perdita del Contesto quando si esegue `sigma` da directory diverse

### Sintomi
- Quando esegui `sigma` da una directory diversa dalla root del progetto, ricevi errori come:
  - "Config file not found"
  - "Framework data not available"
  - "Cannot load data files"

### Causa
SIGMA-NEX cerca i file di configurazione (`config.yaml`), dati (`data/`) e altri file necessari a partire dalla directory corrente. Quando esegui il comando da una directory diversa, non riesce a trovarli.

### Soluzioni

#### Soluzione 1: Configurazione Globale Automatica (Raccomandata)

```bash
# Installa la configurazione globale
sigma install-config

# Imposta la variabile d'ambiente (Windows PowerShell)
$env:SIGMA_NEX_ROOT = "C:\Users\tuonome\AppData\Roaming\sigma-nex"

# Oppure (Windows CMD)
set SIGMA_NEX_ROOT=C:\Users\tuonome\AppData\Roaming\sigma-nex

# Oppure (Linux/macOS)
export SIGMA_NEX_ROOT="$HOME/.config/sigma-nex"
```

#### Soluzione 2: Script Automatico

**Windows:**
```cmd
.\scripts\setup_global_windows.bat
```

**Linux/macOS:**
```bash
./scripts/setup_global_unix.sh
```

#### Soluzione 3: Variabile d'Ambiente Permanente

**Windows (PowerShell - utente corrente):**
```powershell
[Environment]::SetEnvironmentVariable("SIGMA_NEX_ROOT", "C:\Users\tuonome\AppData\Roaming\sigma-nex", "User")
```

**Windows (Variabili di Sistema):**
1. Apri "Variabili d'ambiente"
2. Aggiungi nuova variabile:
   - Nome: `SIGMA_NEX_ROOT`
   - Valore: `C:\Users\tuonome\AppData\Roaming\sigma-nex`

**Linux/macOS (permanente):**
Aggiungi al tuo `~/.bashrc`, `~/.zshrc`, o `~/.profile`:
```bash
export SIGMA_NEX_ROOT="$HOME/.config/sigma-nex"
```

### Verifica della Soluzione

1. **Testa da una directory diversa:**
   ```bash
   cd /path/to/other/directory
   sigma self-check
   ```

2. **Verifica la variabile d'ambiente:**
   ```bash
   # Windows
   echo $env:SIGMA_NEX_ROOT
   
   # Linux/macOS
   echo $SIGMA_NEX_ROOT
   ```

3. **Controlla i file copiati:**
   ```bash
   # Windows
   dir "$env:SIGMA_NEX_ROOT"
   
   # Linux/macOS
   ls -la "$SIGMA_NEX_ROOT"
   ```

### Rimozione della Configurazione Globale

Se vuoi rimuovere la configurazione globale:

```bash
# Rimuove i file di configurazione globale
sigma install-config --uninstall

# Rimuove la variabile d'ambiente (Windows PowerShell)
Remove-Item Env:\SIGMA_NEX_ROOT

# Rimuove la variabile d'ambiente (Linux/macOS)
unset SIGMA_NEX_ROOT
```

### Ordine di Ricerca dei File di Configurazione

SIGMA-NEX cerca i file di configurazione nel seguente ordine:

1. **Variabile d'ambiente `SIGMA_NEX_ROOT`** (se impostata)
2. **Directory corrente e parent** (cammina verso l'alto fino a 10 livelli)
3. **Directory del pacchetto** (relativa al file del modulo)
4. **Directory di configurazione utente:**
   - Windows: `%USERPROFILE%\AppData\Roaming\sigma-nex`
   - Linux/macOS: `~/.config/sigma-nex`
5. **Posizioni comuni di installazione:**
   - `~/.sigma-nex`
   - `/opt/sigma-nex` (Linux)
   - `C:\Program Files\sigma-nex` (Windows)
6. **Fallback:** Directory del progetto relativa al file di codice

### Note Importanti

- **Riavvio del terminale:** Dopo aver impostato le variabili d'ambiente permanenti, riavvia il terminale
- **Aggiornamenti:** Se aggiorni i file di configurazione nel progetto originale, riesegui `sigma install-config` per sincronizzare
- **Spazio su disco:** La configurazione globale occupa circa 10-50 MB (dipende dalla dimensione del framework)

### Troubleshooting Avanzato

**Problema:** "SIGMA_NEX_ROOT impostato ma i file non vengono trovati"
- Verifica che la directory esista: `Test-Path $env:SIGMA_NEX_ROOT` (Windows)
- Controlla i permessi di lettura sulla directory
- Verifica che `config.yaml` sia presente nella directory

**Problema:** "Variabile d'ambiente non persiste"
- Windows: Usa `setx` invece di `set` per rendere permanente la variabile
- Linux/macOS: Assicurati di aver aggiunto l'export al file di profilo corretto

**Problema:** "Conflitti tra configurazioni"
- Elimina eventuali configurazioni locali nella directory corrente
- Usa `sigma install-config --uninstall` e reinstalla