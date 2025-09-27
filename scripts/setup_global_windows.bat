@echo off
REM Script per impostare la configurazione globale di SIGMA-NEX su Windows

echo Configurazione globale SIGMA-NEX
echo.

REM Installa la configurazione globale
echo Installazione configurazione globale...
sigma install-config
if %ERRORLEVEL% neq 0 (
    echo Errore durante l'installazione
    pause
    exit /b 1
)

echo.
echo Impostazione variabile d'ambiente...

REM Imposta la variabile d'ambiente per l'utente corrente
set "GLOBAL_CONFIG_DIR=%USERPROFILE%\AppData\Roaming\sigma-nex"
setx SIGMA_NEX_ROOT "%GLOBAL_CONFIG_DIR%" >nul 2>&1

if %ERRORLEVEL% equ 0 (
    echo Variabile d'ambiente SIGMA_NEX_ROOT impostata con successo
    echo Percorso: %GLOBAL_CONFIG_DIR%
    echo.
    echo Ora puoi usare 'sigma' da qualsiasi directory!
    echo Riavvia il terminale per rendere effettive le modifiche
) else (
    echo Errore nell'impostazione della variabile d'ambiente
    echo Imposta manualmente SIGMA_NEX_ROOT=%GLOBAL_CONFIG_DIR%
)

echo.
echo Configurazione completata!
pause