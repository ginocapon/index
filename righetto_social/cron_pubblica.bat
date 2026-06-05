@echo off
cd /d "%~dp0"
python verifica_meta.py
if errorlevel 1 exit /b 1
python publish_from_agenda.py --modo cron
exit /b %errorlevel%
