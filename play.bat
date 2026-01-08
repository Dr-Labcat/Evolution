@echo off
REM Run the Russian Evolution game using the virtual environment

cd /d "%~dp0"
.venv\Scripts\python.exe main.py
pause
