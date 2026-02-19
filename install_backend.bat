@echo off
REM GenAI Defense - Backend Setup Script for Windows
echo.
echo =========================================
echo GenAI Defense - Backend Installation
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [✓] Python found
echo.

REM Create virtual environment
echo [*] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [✓] Virtual environment created
echo.

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip

echo [✓] Pip upgraded
echo.

REM Install dependencies
echo [*] Installing dependencies from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [✓] Dependencies installed
echo.

REM Create .env if it doesn't exist
if not exist .env (
    echo [*] Creating .env configuration file...
    (
        echo FLASK_ENV=development
        echo FLASK_DEBUG=True
        echo SECRET_KEY=dev-key-change-in-production
        echo DATABASE_URL=sqlite:///aidetector.db
        echo OLLAMA_API_URL=http://localhost:11434
        echo OLLAMA_MODEL=mistral
        echo LOG_LEVEL=DEBUG
    ) > .env
    echo [✓] .env file created
) else (
    echo [✓] .env file already exists
)

echo.
echo =========================================
echo Installation Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Run the backend server:
echo    python app.py
echo.
echo 2. Open in browser:
echo    http://localhost:5000
echo.
echo 3. Optional - Install Ollama for local LLM:
echo    Download from https://ollama.ai
echo    Run: ollama pull mistral
echo    Then run: ollama serve
echo.
echo =========================================
echo.
pause
