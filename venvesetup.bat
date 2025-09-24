@echo off
REM SIGMA-NEX v0.3.1 - Setup Automatico per Windows
REM Questo script configura automaticamente l'ambiente di sviluppo

echo ========================================
echo     SIGMA-NEX v0.3.1 Setup
echo ========================================
echo.

REM Controlla se Python e disponibile
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato nel PATH
    echo Installa Python 3.10+ da https://python.org
    pause
    exit /b 1
)

echo [1/5] Verifica Python...
python --version

REM Crea ambiente virtuale
echo.
echo [2/5] Creazione ambiente virtuale...
if exist venv (
    echo Ambiente virtuale esistente trovato
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERRORE: Creazione ambiente virtuale fallita
        pause
        exit /b 1
    )
)

REM Attiva ambiente virtuale
echo.
echo [3/5] Attivazione ambiente virtuale...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRORE: Attivazione ambiente virtuale fallita
    pause
    exit /b 1
)

REM Aggiorna pip
echo.
echo [4/5] Aggiornamento pip...
python -m pip install --upgrade pip

REM Installa dipendenze
echo.
echo [5/5] Installazione dipendenze...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRORE: Installazione dipendenze fallita
    pause
    exit /b 1
)

REM Installa in modalita sviluppo
echo.
echo Installazione SIGMA-NEX in modalita sviluppo...
pip install -e .
if errorlevel 1 (
    echo ERRORE: Installazione SIGMA-NEX fallita
    pause
    exit /b 1
)

echo.
echo ========================================
echo    INSTALLAZIONE COMPLETATA!
echo ========================================
echo.
echo Per iniziare:
echo   1. Installa Ollama: https://ollama.com
echo   2. Scarica modello: ollama pull mistral
echo   3. Testa il sistema: sigma self-check
echo   4. Avvia SIGMA-NEX: sigma start
echo.
echo Ambiente virtuale attivato automaticamente.
echo Per riattivarlo in futuro: venv\Scripts\activate.bat
echo.
pause