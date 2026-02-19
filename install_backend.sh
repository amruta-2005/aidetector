#!/bin/bash

# GenAI Defense - Backend Setup Script for macOS/Linux

echo ""
echo "========================================="
echo "GenAI Defense - Backend Installation"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using:"
    echo "  macOS: brew install python3"
    echo "  Linux: apt-get install python3 python3-venv"
    exit 1
fi

echo "[✓] Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "[*] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[✓] Virtual environment created"
echo ""

# Upgrade pip
echo "[*] Upgrading pip..."
python3 -m pip install --upgrade pip

echo "[✓] Pip upgraded"
echo ""

# Install dependencies
echo "[*] Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[✓] Dependencies installed"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "[*] Creating .env configuration file..."
    cat > .env << EOF
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-key-change-in-production
DATABASE_URL=sqlite:///aidetector.db
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=mistral
LOG_LEVEL=DEBUG
EOF
    echo "[✓] .env file created"
else
    echo "[✓] .env file already exists"
fi

echo ""
echo "========================================="
echo "Installation Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the backend server:"
echo "   python app.py"
echo ""
echo "3. Open in browser:"
echo "   http://localhost:5000"
echo ""
echo "4. Optional - Install Ollama for local LLM:"
echo "   Download from https://ollama.ai"
echo "   Run: ollama pull mistral"
echo "   Then run: ollama serve"
echo ""
echo "========================================="
echo ""
chmod +x run_server.sh

