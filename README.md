# GenAI Defense - AI Fraud Detection System

A comprehensive, offline-first fraud detection system that identifies AI-generated phishing, deepfake attacks, and AI model vulnerabilities using locally-hosted language models and custom detectors.

## Features

- **AI-Generated Phishing Detection** - Identify emails crafted by AI with risk scoring
- **Deepfake Audio Detection** - Detect AI-synthesized voice used in fraud calls
- **Prompt Injection Testing** - Test LLM guardrails against jailbreak attempts
- **Attachment Malware Analysis** - Sandbox file detonation with behavioral analysis
- **URL Phishing Analysis** - Domain spoofing and SSL certificate validation
- **Dark Web Monitoring** - Credential exposure tracking across underground forums
- **Incident Management** - Comprehensive incident tracking with SLA monitoring
- **Asset Inventory** - Critical asset exposure monitoring
- **User Management** - Role-based access control (RBAC)
- **Forensic Reporting** - Financial impact and ROI tracking

## Architecture

### Frontend
- **HTML5/CSS3/JavaScript** - Pure vanilla stack, no frameworks
- **Responsive Design** - Works on desktop and tablet
- **Real-time Visualizations** - Canvas charts and live data updates
- **Modular Page Structure** - 15 pages for different fraud detection capabilities

### Backend
- **Python Flask** - RESTful API server
- **SQLite Database** - Local incident and asset storage
- **Offline Architecture** - No cloud dependencies
- **Integrations:**
  - Ollama - Local LLM inference (Mistral, LLaMA2)
  - Hugging Face Transformers - NLP models
  - librosa - Audio analysis (MFCC)

### Data Flow
```
Frontend (HTML/JS) 
    ↓
Flask REST API (Port 5000)
    ↓
SQLite Database
    ↓
Analysis Services (EmailAnalysisService, etc.)
    ↓
Local LLM (Ollama) / ML Models
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda
- Optional: Ollama (for local LLM support)

### Setup Steps

1. **Clone/Download the project**
```bash
cd aidetector
```

2. **Create virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set environment variables**
Create or edit `.env` file:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///aidetector.db
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

5. **Initialize database** (automatic on first run)
```bash
# Database will be created on app startup
```

6. **Run the application**
```bash
python app.py
```

7. **Access the dashboard**
Open browser to: `http://localhost:5000`

## API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Overall security posture
- `GET /api/dashboard/incidents-feed` - Recent incidents

### Analysis Endpoints
- `POST /api/analyze/email` - Analyze email for AI phishing
- `POST /api/analyze/email/check-exposure` - Check dark web leaks
- `POST /api/analyze/url` - Analyze URL for spoofing
- `POST /api/analyze/file` - Analyze file for malware
- `POST /api/analyze/audio` - Detect deepfake audio

### Incidents
- `GET /api/incidents` - List incidents (with filtering)
- `POST /api/incidents` - Create new incident
- `GET /api/incidents/<id>` - Get incident details
- `PUT /api/incidents/<id>` - Update incident status
- `GET /api/incidents/stats` - Incident statistics

### Assets
- `GET /api/assets` - List critical assets
- `POST /api/assets` - Add new asset
- `GET /api/assets/stats` - Asset statistics

### Users & Access Control
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/users/stats` - User statistics
- `GET /api/audit-logs` - Audit trail

### Threat Intelligence
- `GET /api/threat-intel/campaigns` - Active threat campaigns
- `GET /api/threat-intel/actors` - Known threat actors
- `GET /api/threat-intel/emerging-techniques` - New attack vectors

### Dark Web
- `GET /api/darkweb/exposure/<email>` - Email exposure check
- `GET /api/darkweb/stats` - Dark web monitoring stats

### Models
- `GET /api/models/list` - Available local models
- `POST /api/models/test-injection` - Test prompt injection

### Forensics & Reporting
- `GET /api/forensics/metrics` - Financial impact metrics
- `GET /api/forensics/case-reports` - Case summaries

### System
- `GET /api/health` - Health check

## Configuration

### Adding Local LLM Support

1. **Install Ollama**
   - Download from https://ollama.ai
   - Pull model: `ollama pull mistral`

2. **Run Ollama**
   ```bash
   ollama serve
   ```
   (Ollama will run on `http://localhost:11434` by default)

3. **Update environment**
   - Set `OLLAMA_API_URL` in `.env`
   - Set `OLLAMA_MODEL` to desired model (mistral, llama2, etc.)

### Model Configuration

Access Model Configuration page (`/model-config.html`) to:
- Monitor VRAM and resource usage
- View active models and their performance
- Manage training datasets
- Adjust temperature and token limits
- Configure content filtering

## API Integration in Frontend

Example: Analyzing an email from JavaScript

```javascript
// From js/content.js
function analyzeContent() {
    const emailData = {
        from: 'noreply@paypal-verify.net',
        to: 'user@company.com',
        subject: 'Urgent: Verify Your Account',
        body: 'Click here to confirm your identity immediately'
    };
    
    fetch('/api/analyze/email', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(emailData)
    })
    .then(r => r.json())
    .then(data => {
        console.log('Risk Score:', data.risk_score);
        console.log('AI Probability:', data.ai_probability);
        console.log('Indicators:', data.indicators);
    });
}
```

## Database Schema

### Incidents Table
```sql
- id (int, primary key)
- incident_id (string, unique)
- incident_type (string)
- severity (string)
- status (string)
- source (string)
- target (string)
- description (text)
- risk_score (float)
- created_at (datetime)
- updated_at (datetime)
- resolved_at (datetime)
```

### Assets Table
```sql
- id (int, primary key)
- asset_name (string)
- asset_type (string)
- asset_value (string, unique)
- category (string)
- exposure_status (string)
- created_at (datetime)
```

### Users Table
```sql
- id (int, primary key)
- username (string, unique)
- email (string, unique)
- role (string)
- status (string)
- is_online (boolean)
- last_login (datetime)
- created_at (datetime)
```

### Analysis Results Table
```sql
- id (int, primary key)
- analysis_type (string)
- input_hash (string, unique)
- result (json)
- risk_score (float)
- ai_probability (float)
- created_at (datetime)
```

## Security Considerations

1. **Offline Operation** - No cloud calls, all processing local
2. **Data Privacy** - No sensitive data stored in database (anonymized features only)
3. **Access Control** - Role-based permissions (Admin, Analyst, Viewer, API Service)
4. **Audit Logging** - All privileged actions logged
5. **Environment Secrets** - Store sensitive configs in `.env` (not in version control)

## Performance Optimization

- **Model Caching** - LLM models cached in memory during server lifetime
- **Result Caching** - Analysis results cached by input hash to avoid re-processing
- **Database Indexing** - Incident queries optimized with created_at index
- **Frontend** - Lazy loading of JavaScript, CSS minification ready

## Troubleshooting

### Port Already in Use
```bash
# Use different port
python app.py --port 8000
```

### Database Locked
```bash
# Delete database and reinitialize
rm aidetector.db
python app.py
```

### Ollama Connection Failed
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### Missing Dependencies
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt
```

## File Structure

```
aidetector/
├── app.py                      # Flask application & routes
├── config.py                   # Configuration management
├── models.py                   # Database models
├── services.py                 # Analysis services
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── aidetector.db              # SQLite database (auto-created)
├── index.html                  # Dashboard
├── content-inspector.html       # Email analysis
├── phishing-tester.html         # URL analysis
├── attachment-sandbox.html      # File analysis
├── model-sandbox.html           # Prompt injection testing
├── incidents.html               # Incident tracking
├── dark-web.html                # Dark web monitoring
├── deepfake-audio.html          # Audio analysis
├── model-config.html            # LLM configuration
├── asset-inventory.html         # Asset tracking
├── forensic-reporting.html      # Financial reporting
├── user-management.html         # RBAC management
├── threat-intel.html            # Campaign tracking
├── css/
│   └── styles.css              # Styling
└── js/
    ├── app.js                  # Dashboard scripts
    ├── nav.js                  # Navigation
    ├── content.js              # Email analysis
    ├── phishing.js             # URL analysis
    ├── attachment.js           # File upload
    ├── sandbox.js              # Model testing
    ├── incidents.js            # Incident management
    ├── audio.js                # Audio visualization
    └── darkweb.js              # Dark web data
```

## Next Steps & Future Enhancements

- [ ] Docker containerization for easy deployment
- [ ] Real Ollama/Hugging Face model integration
- [ ] Advanced MFCC audio deepfake detection
- [ ] Real dark web crawler integration
- [ ] Machine learning model retraining pipeline
- [ ] Automated threat feed ingestion
- [ ] Multi-tenant support
- [ ] Advanced reporting with PDF export
- [ ] Real-time WebSocket incident streaming
- [ ] Integration with SIEM systems (Splunk, ELK)

## Support & Contributing

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

## License

This project is provided as-is for fraud detection and cybersecurity research purposes.

---

**Last Updated:** February 2026
**Current Version:** 1.0.0

Protype Link:
https://drive.google.com/file/d/1vywrVZ8jD7Mtg6tv1gPxCoavB0zEha4A/view?usp=sharing
