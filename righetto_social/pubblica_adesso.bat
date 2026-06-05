@echo off
cd /d "%~dp0"
echo === Verifica Meta ===
python verifica_meta.py
if errorlevel 1 exit /b 1
echo.
echo === Pubblica (modo MANUALE: rispetta l'ora che hai messo in Agenda) ===
python publish_from_agenda.py --modo manuale %*
pause
