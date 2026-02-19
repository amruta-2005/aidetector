#!/bin/bash

# Quick start script for GenAI Defense Backend on macOS/Linux

echo ""
echo "====================================="
echo "GenAI Defense - Server Startup"
echo "====================================="
echo ""

# Activate virtual environment
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
    echo "[✓] Virtual environment activated"
else
    echo "ERROR: Virtual environment not found"
    echo "Please run install_backend.sh first"
    exit 1
fi

echo ""

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Flask not installed"
    echo "Please run install_backend.sh first"
    exit 1
fi

echo "[✓] All dependencies ready"
echo ""
echo "Starting Flask server..."
echo ""
echo "====================================="
echo "Server running at:"
echo "   http://localhost:5000"
echo ""
echo "Dashboard: http://localhost:5000/"
echo "API Health: http://localhost:5000/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "====================================="
echo ""

python3 app.py
