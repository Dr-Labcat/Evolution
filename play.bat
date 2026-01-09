@echo off
cd /d "%~dp0"

IF NOT EXIST ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment. Make sure Python is installed and in PATH.
        pause
        exit /b
    )

    IF EXIST requirements.txt (
        echo Installing dependencies...
        .venv\Scripts\pip.exe install -r requirements.txt
    ) ELSE (
        echo No requirements.txt found. Skipping installation.
    )
)

.venv\Scripts\python.exe main.py
pause
