#!/usr/bin/env python3
"""
GenAI Defense - Quick Reference & Testing Script

Run this script to verify the backend is properly configured.
Usage: python test_backend.py
"""

import sys
import subprocess
import json
import os
from pathlib import Path

def check_python_version():
    """Verify Python 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Found: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} OK")
    return True

def check_imports():
    """Verify required packages installed"""
    required = ['flask', 'flask_sqlalchemy', 'flask_cors', 'dotenv']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('_', '-'))
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} NOT installed")
            missing.append(package)
    
    return len(missing) == 0

def check_files():
    """Verify required files exist"""
    required_files = [
        'app.py',
        'config.py',
        'models.py',
        'services.py',
        'requirements.txt',
        '.env',
        'README.md',
        'BACKEND_SETUP.md'
    ]
    
    all_exist = True
    for f in required_files:
        if Path(f).exists():
            print(f"✅ {f} found")
        else:
            print(f"❌ {f} MISSING")
            all_exist = False
    
    return all_exist

def show_quick_commands():
    """Display quick reference commands"""
    print("\n" + "="*50)
    print("QUICK REFERENCE - Common Commands")
    print("="*50)
    
    commands = {
        "Setup Backend": [
            "bash install_backend.sh       (macOS/Linux)",
            "install_backend.bat          (Windows)"
        ],
        "Start Server": [
            "bash run_server.sh           (macOS/Linux)",
            "run_server.bat               (Windows)",
            "python app.py                (Direct)"
        ],
        "Access System": [
            "http://localhost:5000        (Dashboard)",
            "http://localhost:5000/api/health  (API Health)"
        ],
        "Manage Database": [
            "rm aidetector.db             (Reset database)",
            "sqlite3 aidetector.db        (Open SQLite shell)"
        ],
        "Check Logs": [
            "FLASK_DEBUG=True python app.py  (Verbose output)"
        ]
    }
    
    for section, items in commands.items():
        print(f"\n{section}:")
        for item in items:
            print(f"  $ {item}")

def main():
    print("\n" + "="*50)
    print("GenAI Defense - Backend Verification")
    print("="*50)
    print()
    
    print("🔍 System Checks\n")
    
    checks = [
        ("Python Version", check_python_version()),
        ("Required Packages", check_imports()),
        ("Required Files", check_files()),
    ]
    
    all_passed = all(result for _, result in checks)
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ All checks passed!")
    else:
        print("❌ Some checks failed. See above.")
    print("="*50)
    
    show_quick_commands()
    
    print("\n" + "="*50)
    print("📚 Documentation")
    print("="*50)
    print("""
Getting Started:
  1. Read: README.md
  2. Setup: BACKEND_SETUP.md
  3. Database: DATABASE_SCHEMA.md
  4. Summary: BACKEND_IMPLEMENTATION_SUMMARY.md

Install & Run:
  bash install_backend.sh
  bash run_server.sh

Test API:
  curl http://localhost:5000/api/health

Access Dashboard:
  Open http://localhost:5000 in browser
""")
    print("="*50)

if __name__ == '__main__':
    main()\n"
