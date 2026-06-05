@echo off
REM Domenica (o manuale): genera bozze settimana successiva (12 sito + 2 notizie RSS)
cd /d "%~dp0"
python genera_bozze_settimanali.py
exit /b %errorlevel%
