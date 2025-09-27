@echo off
REM setup_auth.bat - Script di configurazione autenticazione SIGMA-NEX per Windows
REM Questo script aiuta a configurare le variabili d'ambiente per l'autenticazione

echo ================================================================================
echo ███████╗██╗ ██████╗ ███╗   ███╗ █████╗       ███╗   ██╗███████╗██╗  ██╗
echo ██╔════╝██║██╔════╝ ████╗ ████║██╔══██╗      ████╗  ██║██╔════╝╚██╗██╔╝
echo ███████╗██║██║  ███╗██╔████╔██║███████║█████╗██╔██╗ ██║█████╗   ╚███╔╝
echo ╚════██║██║██║   ██║██║╚██╔╝██║██╔══██║╚════╝██║╚██╗██║██╔══╝   ██╔██╗
echo ███████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║      ██║ ╚████║███████╗██╔╝ ██╗
echo ╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝      ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
echo ================================================================================
echo.
echo               SIGMA-NEX Authentication Setup for Windows
echo               Developed by: Martin Sebastian | Email: rootedlab6@gmail.com
echo               Repository: https://github.com/SebastianMartinNS/SYGMA-NEX
echo.
echo ================================================================================
echo.

REM Verifica se siamo in ambiente virtuale
if defined VIRTUAL_ENV (
    echo [OK] Ambiente virtuale attivato: %VIRTUAL_ENV%
) else (
    echo [WARNING] Ambiente virtuale non rilevato. Assicurati di aver attivato il venv.
    echo          python -m venv venv ^&^& venv\Scripts\activate
    echo.
)

REM Verifica se le variabili sono già impostate
echo Verifica variabili ambiente attuali:
if defined SIGMA_DEV_PASSWORD (
    echo [OK] SIGMA_DEV_PASSWORD: IMPOSTATA
) else (
    echo [MISSING] SIGMA_DEV_PASSWORD: NON IMPOSTATA
)

if defined SIGMA_ADMIN_PASSWORD (
    echo [OK] SIGMA_ADMIN_PASSWORD: IMPOSTATA
) else (
    echo [MISSING] SIGMA_ADMIN_PASSWORD: NON IMPOSTATA
)
echo.

if defined SIGMA_ADMIN_PASSWORD (
    echo SIGMA_ADMIN_PASSWORD: IMPOSTATA
) else (
    echo SIGMA_ADMIN_PASSWORD: NON IMPOSTATA
)
echo.

set /p choice="Vuoi configurare le password ora? (y/N): "
if /i not "!choice!"=="y" if /i not "!choice!"=="Y" (
    echo Configurazione annullata.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo                    IMPORTANTE - REQUISITI PASSWORD SICURE
echo ================================================================================
echo Le password devono essere sicure con i seguenti requisiti:
echo - Minimo 8 caratteri
echo - Almeno una lettera maiuscola
echo - Almeno una lettera minuscola
echo - Almeno un numero
echo - Almeno un carattere speciale (!@#$%%^&*()-_=+[]{}|.<>?)
echo.
echo Non usare password comuni o prevedibili.
echo ================================================================================
echo.

REM Password dev
:dev_password
set /p "dev_pass=Inserisci password per utente DEV: "
if "%dev_pass%"=="" goto dev_password
call :strlen dev_pass_len "%dev_pass%"
if %dev_pass_len% lss 8 (
    echo [ERROR] Password troppo corta (minimo 8 caratteri)
    goto dev_password
)
set /p "dev_pass_confirm=Conferma password DEV: "
if not "%dev_pass%"=="%dev_pass_confirm%" (
    echo [ERROR] Le password non coincidono
    goto dev_password
)
echo [OK] Password DEV accettata

REM Password admin
:admin_password
set /p "admin_pass=Inserisci password per utente ADMIN: "
if "%admin_pass%"=="" goto admin_password
call :strlen admin_pass_len "%admin_pass%"
if %admin_pass_len% lss 8 (
    echo [ERROR] Password troppo corta (minimo 8 caratteri)
    goto admin_password
)
set /p "admin_pass_confirm=Conferma password ADMIN: "
if not "%admin_pass%"=="%admin_pass_confirm%" (
    echo [ERROR] Le password non coincidono
    goto admin_password
)
echo [OK] Password ADMIN accettata

REM Imposta le variabili
set SIGMA_DEV_PASSWORD=%dev_pass%
set SIGMA_ADMIN_PASSWORD=%admin_pass%

echo.
echo ================================================================================
echo                    CONFIGURAZIONE COMPLETATA
echo ================================================================================
echo [SUCCESS] Variabili ambiente impostate per questa sessione CMD
echo.

REM Test configurazione
echo === Test Configurazione ===
python -c "
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

echo.
echo ================================================================================
                    PROSSIMI PASSI
================================================================================
echo.
echo NOTA: Queste variabili sono valide solo per questa sessione CMD.
echo.
echo Per impostarle permanentemente:
echo.
echo 1. Comando per impostazione permanente nel sistema:
echo    setx SIGMA_DEV_PASSWORD "%dev_pass%" /M
echo    setx SIGMA_ADMIN_PASSWORD "%admin_pass%" /M
echo.
echo 2. Per impostarle solo per l'utente corrente:
echo    setx SIGMA_DEV_PASSWORD "%dev_pass%"
echo    setx SIGMA_ADMIN_PASSWORD "%admin_pass%"
echo.
echo 3. Verifica la documentazione completa in: docs\config\authentication.md
echo.
echo ================================================================================
pause
exit /b 0

:strlen <resultVar> <string>
setlocal enabledelayedexpansion
set "s=%~2#"
set "len=0"
for %%N in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
    if "!s:~%%N!" neq "" (
        set /a "len+=%%N"
        set "s=!s:~%%N!"
    )
)
endlocal & set "%~1=%len%"
goto :eof