@echo off
REM Quick start script for GenAI Defense Backend on Windows
echo.
echo ===================================
echo GenAI Defense - Server Startup
echo ===================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [✓] Virtual environment activated
) else (
    echo ERROR: Virtual environment not found
    echo Please run install_backend.bat first
    pause
    exit /b 1
)

echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Flask not installed
    echo Please run install_backend.bat first
    pause
    exit /b 1
)

echo [✓] All dependencies ready
echo.
echo Starting Flask server...
echo.
echo ===================================
echo Server running at:
echo   http://localhost:5000
echo.
echo Dashboard: http://localhost:5000/
echo API Health: http://localhost:5000/api/health
echo.
echo Press Ctrl+C to stop the server
echo ===================================
echo.

python app.py
