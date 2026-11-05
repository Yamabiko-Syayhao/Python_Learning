@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Project Python environment is missing.
    echo Run this command in the project folder: uv sync --locked
    pause
    exit /b 1
)
".venv\Scripts\python.exe" -B -c "import websockets" >nul 2>&1
if errorlevel 1 (
    echo Project dependency is missing or the Python environment is broken.
    echo Run this command in the project folder: uv sync --locked
    pause
    exit /b 1
)
echo Starting chat server. Keep this window open. Press Ctrl+C to stop.
".venv\Scripts\python.exe" -B -X utf8 -u serverCopy.py --open-browser
if errorlevel 1 (
    echo Startup failed. Check the error above and see README.md.
    pause
)
