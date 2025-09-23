@echo off
REM Crea ambiente virtuale (se non esiste)
python -m venv venv

echo.
echo Attivazione ambiente virtuale:
echo -------------------------------------------
echo Esegui questo comando nella shell:
echo venv\Scripts\activate
echo -------------------------------------------

REM Attendi che l'utente abbia attivato l'ambiente
pause

REM Installa pacchetti necessari
pip install --upgrade pip
pip install transformers sentencepiece torch

echo.
echo -------------------------------------------
echo AMBIENTE VIRTUALE CREATO E PACCHETTI INSTALLATI!
echo Ora puoi lanciare i tuoi script in questo ambiente.
echo -------------------------------------------
pause
