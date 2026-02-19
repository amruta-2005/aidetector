# GenAI Defense - Backend Setup Guide

Complete guide to setting up and running the Flask backend for the GenAI Defense AI-powered fraud detection system.

## Quick Start (5 minutes)

### Windows
```bash
# 1. Install and setup
install_backend.bat

# 2. Run the server
run_server.bat

# 3. Open browser to http://localhost:5000
```

### macOS / Linux
```bash
# 1. Install and setup
bash install_backend.sh

# 2. Run the server
bash run_server.sh

# 3. Open browser to http://localhost:5000
```

## Manual Setup

### Prerequisites
- **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
- **pip** - Usually included with Python
- **Git** (optional) - For version control

### Step-by-Step Installation

#### 1. Navigate to Project Directory
```bash
cd aidetector
```

#### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask - Web framework
- SQLAlchemy - Database ORM
- Flask-CORS - API access
- And other required packages

#### 4. Configure Environment Variables

Create or edit `.env` file:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///aidetector.db
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=mistral
LOG_LEVEL=DEBUG
```

#### 5. Run the Server

**With auto-reload (development):**
```bash
python app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

#### 6. Test the Backend

Open browser to:
- **Dashboard:** http://localhost:5000
- **API Health:** http://localhost:5000/api/health
- **API Docs:** See below for endpoint references

## Project Structure

```
aidetector/
├── app.py                  # Main Flask application with routes
├── config.py               # Configuration settings
├── models.py               # SQLAlchemy database models
├── services.py             # Analysis services (email, URL, audio, etc.)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (gitignored)
├── aidetector.db          # SQLite database (auto-created)
│
├── install_backend.bat    # Windows setup script
├── install_backend.sh     # macOS/Linux setup script
├── run_server.bat         # Windows run script
├── run_server.sh          # macOS/Linux run script
│
├── README.md              # Main project documentation
├── BACKEND_SETUP.md       # This file
├── DATABASE_SCHEMA.md     # Database documentation
│
├── index.html             # Dashboard
├── [other HTML pages...]  # Analysis pages
│
├── css/
│   └── styles.css         # UI styling
│
└── js/
    ├── app.js             # Dashboard scripts
    ├── content.js         # Email analysis
    ├── phishing.js        # URL analysis
    ├── [other scripts...]
```

## Backend Architecture

### Layers

1. **Routes Layer (`app.py`)**
   - Flask endpoints
   - Request/response handling
   - HTTP status codes

2. **Services Layer (`services.py`)**
   - Business logic for each analysis type
   - Mock ML model implementations
   - Data transformation

3. **Models Layer (`models.py`)**
   - SQLAlchemy ORM models
   - Database schema definitions
   - Relationships between entities

4. **Data Layer**
   - SQLite database
   - Automatic migrations on startup
   - Initial data seeding

### Data Flow

```
Frontend (HTML/JavaScript)
    ↓
Flask Route Handler
    ↓
Service Method (analysis logic)
    ↓
Database Model (storage)
    ↓
SQLite Database
    ↓
Response back to Frontend
```

## API Overview

### Core Endpoints

#### Dashboard
```
GET /api/dashboard/stats
GET /api/dashboard/incidents-feed
```

#### Analysis Services
```
POST /api/analyze/email
POST /api/analyze/email/check-exposure
POST /api/analyze/url
POST /api/analyze/file
POST /api/analyze/audio
```

#### Incident Management
```
GET /api/incidents
POST /api/incidents
GET /api/incidents/<id>
PUT /api/incidents/<id>
GET /api/incidents/stats
```

#### Asset Management
```
GET /api/assets
POST /api/assets
GET /api/assets/stats
```

#### User Management
```
GET /api/users
POST /api/users
GET /api/users/stats
```

#### Dark Web Monitoring
```
GET /api/darkweb/exposure/<email>
GET /api/darkweb/stats
```

For complete API documentation, see the endpoint comments in `app.py`.

## Database

### SQLite Setup

Database is automatically created on first run at: `aidetector.db`

### Models

1. **Incident** - Security events and alerts
2. **Asset** - Critical organizational resources
3. **User** - User accounts and access control
4. **AnalysisResult** - Cached analysis results
5. **AuditLog** - Action audit trail

See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) for detailed schema documentation.

## Analysis Services

### EmailAnalysisService
Detects AI-generated phishing emails with risk scoring:
- Generic greeting detection
- Urgency tactic identification
- Credential harvesting patterns
- Sender spoofing detection
- Dark web credential exposure checking

**Example:**
```python
from services import EmailAnalysisService

result = EmailAnalysisService.analyze_email({
    'from': 'noreply@paypal-verify.net',
    'subject': 'Verify Your Account',
    'body': 'Click here to confirm...'
})
# Returns: {risk_score, ai_probability, indicators, is_phishing, threat_level}
```

### URLAnalysisService
Analyzes URLs for phishing and spoofing:
- Typosquatting detection
- Domain age analysis
- SSL certificate validation
- Suspicious pattern recognition

### FileAnalysisService
Malware and pharming analysis:
- Executable signature detection
- Macro obfuscation detection
- VirusTotal integration (mock)
- Behavioral analysis

### AudioAnalysisService
Deepfake voice detection:
- MFCC feature extraction (mock)
- Synthesis artifact detection
- Call metadata analysis

### PromptInjectionService
Tests LLM guardrails:
- Dangerous pattern detection
- Attack success rate tracking
- Data leak detection

### DarkWebService
Monitors dark web for exposure:
- Credential leak tracking
- Forum intelligence
- Asset watchlist monitoring

### RiskScoringService
Calculates overall risk posture

## Frontend Integration

### Connecting Frontend to Backend

The frontend JavaScript files automatically connect to the backend:

```javascript
const API_URL = 'http://localhost:5000/api';

// Example: Analyze email
fetch(`${API_URL}/analyze/email`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        from: 'sender@domain.com',
        subject: 'Test',
        body: 'Test body'
    })
})
.then(r => r.json())
.then(data => {
    console.log('Risk Score:', data.risk_score);
    console.log('AI Probability:', data.ai_probability);
});
```

### Fallback to Mock Data

If backend is not running, all pages gracefully fall back to mock data and local processing.

## Local LLM Integration (Ollama)

### Setup Ollama

1. **Download & Install**
   - Visit https://ollama.ai
   - Download for your OS

2. **Pull a Model**
   ```bash
   ollama pull mistral
   ```

3. **Run Ollama in Background**
   ```bash
   ollama serve
   ```
   (Runs on http://localhost:11434)

4. **Update Backend Config**
   - Set `OLLAMA_API_URL=http://localhost:11434` in `.env`
   - Set `OLLAMA_MODEL=mistral` (or your chosen model)

5. **Test Connection**
   ```bash
   curl http://localhost:11434/api/tags
   ```

### Available Models

```bash
# Small, fast (7B parameters)
ollama pull mistral

# Larger, more capable (7B parameters)
ollama pull llama2

# Custom fine-tuned models
ollama create mymodel -f ./Modelfile
```

## Environment Variables

Key configuration options:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | development or production | development |
| `FLASK_DEBUG` | Enable debug mode | True |
| `SECRET_KEY` | Session encryption key | (generated) |
| `DATABASE_URL` | SQLite database path | sqlite:///aidetector.db |
| `OLLAMA_API_URL` | Ollama server URL | http://localhost:11434 |
| `OLLAMA_MODEL` | Default model name | mistral |
| `LOG_LEVEL` | DEBUG, INFO, WARNING, ERROR | DEBUG |

## Troubleshooting

### Port 5000 Already in Use

```bash
# Option 1: Use different port (modify app.py)
python app.py --port 8000

# Option 2: Kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Database Errors

```bash
# Delete and recreate database
rm aidetector.db
python app.py
```

### Module Not Found Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check virtual environment is activated
# Windows: you should see (venv) in prompt
# macOS/Linux: same
```

### Ollama Connection Failed

```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve

# Check OLLAMA_API_URL in .env
```

### CORS Errors

If frontend can't connect to backend:
- Ensure backend is running on http://localhost:5000
- Flask-CORS is enabled (see `app.py`)
- Check browser console for actual error

## Performance Optimization

### Caching
- Analysis results are cached by input hash
- Prevents re-processing identical requests

### Database Indexing
- Incidents indexed on `created_at` and `status`
- Queries optimized for fast filtering

### Model Loading
- LLM models loaded once on startup
- Remains in memory for fast inference

## Security Considerations

1. **Change SECRET_KEY in Production**
   - Set to a strong random value
   - Never commit to version control

2. **Use Environment File**
   - `.env` file is gitignored
   - Store all secrets there

3. **CORS in Production**
   - Restrict to specific domains
   - Don't allow all origins (*)

4. **Database**
   - SQLite fine for development
   - Use PostgreSQL for production
   - Enable encryption at rest

5. **API Authentication**
   - Consider adding API key authentication
   - Implement rate limiting
   - Add request logging

## Deployment

### Development Server (Current)
```bash
python app.py
```
- Good for testing/development
- Auto-reloads on code changes
- Not suitable for production

### Production Server

Use production WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or with environment file:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --env-file .env app:app
```

### Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t aidetector-backend .
docker run -p 5000:5000 aidetector-backend
```

## Support & Next Steps

### Immediate Tasks
- [ ] Install backend dependencies
- [ ] Start Flask server
- [ ] Access dashboard at http://localhost:5000
- [ ] Test API endpoints

### Optional Enhancements
- [ ] Install Ollama for real LLM
- [ ] Add real dark web monitoring
- [ ] Integrate actual malware analysis APIs
- [ ] Add user authentication
- [ ] Deploy to production

### Documentation
- [README.md](README.md) - Main project documentation
- [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) - Database details
- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review console logs: `FLASK_DEBUG=True` shows detailed errors
3. Check `.env` configuration
4. Verify all dependencies installed: `pip list`

---

**Last Updated:** February 2026
**Version:** 1.0.0
