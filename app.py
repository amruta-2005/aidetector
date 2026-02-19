import os
import logging
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
from config import config
from models import db, Incident, Asset, User, AnalysisResult, AuditLog
from services import (
    EmailAnalysisService,
    URLAnalysisService,
    FileAnalysisService,
    AudioAnalysisService,
    PromptInjectionService,
    DarkWebService,
    RiskScoringService
)

# Initialize Flask app
app = Flask(__name__, static_folder='', static_url_path='')
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])

# Initialize extensions
db.init_app(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ==================== Database Initialization ====================
@app.before_request
def init_db():
    """Initialize database on first request"""
    if not hasattr(app, 'db_initialized'):
        with app.app_context():
            db.create_all()
            # Seed initial data
            seed_database()
            app.db_initialized = True

def seed_database():
    """Seed database with initial data"""
    if User.query.first() is None:
        users = [
            User(username='alex_rivera', email='alex@company.com', role='Admin', is_online=True),
            User(username='sarah_chen', email='sarah@company.com', role='Analyst', is_online=True),
            User(username='michael_park', email='michael@company.com', role='Viewer', is_online=False),
        ]
        db.session.add_all(users)
    
    if Incident.query.first() is None:
        incidents = [
            Incident(
                incident_id='INC-2024-001245',
                incident_type='phishing',
                severity='Critical',
                status='BLOCKED',
                source='external_email',
                target='employees@company.com',
                description='AI-generated phishing email with credential harvesting',
                risk_score=88
            ),
            Incident(
                incident_id='INC-2024-001244',
                incident_type='deepfake',
                severity='Critical',
                status='FLAGGED',
                source='voip_network',
                target='finance_team',
                description='Deepfake audio impersonating CFO',
                risk_score=92
            ),
        ]
        db.session.add_all(incidents)
    
    if Asset.query.first() is None:
        assets = [
            Asset(asset_name='CISO Email', asset_type='email', asset_value='ciso@company.com', category='critical', exposure_status='exposed'),
            Asset(asset_name='API Production', asset_type='domain', asset_value='api.company.com', category='critical', exposure_status='monitored'),
            Asset(asset_name='CEO Account', asset_type='account', asset_value='ceo_account', category='vip', exposure_status='secure'),
        ]
        db.session.add_all(assets)
    
    db.session.commit()

# ==================== Static Files ====================
@app.route('/')
def index():
    """Serve index.html"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    """Serve static files"""
    try:
        return send_from_directory('.', filename)
    except:
        return send_from_directory('.', 'index.html')

# ==================== API Routes ====================

# ========== Dashboard API ==========
@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    stats = RiskScoringService.calculate_risk_posture()
    return jsonify(stats)

@app.route('/api/dashboard/incidents-feed', methods=['GET'])
def get_incidents_feed():
    """Get recent incidents for dashboard feed"""
    incidents = Incident.query.order_by(Incident.created_at.desc()).limit(4).all()
    return jsonify([inc.to_dict() for inc in incidents])

# ========== Email Analysis API ==========
@app.route('/api/analyze/email', methods=['POST'])
def analyze_email():
    """Analyze email for phishing and AI-generation"""
    data = request.get_json()
    
    result = EmailAnalysisService.analyze_email(data)
    
    # Store in database
    analysis = AnalysisResult(
        analysis_type='email',
        input_hash=hash(str(data)),
        input_data=str(data)[:500],
        result=result,
        risk_score=result['risk_score'],
        ai_probability=result['ai_probability'],
        key_indicators=result['indicators']
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result)

@app.route('/api/analyze/email/check-exposure', methods=['POST'])
def check_email_exposure():
    """Check if email is exposed in dark web leaks"""
    data = request.get_json()
    email = data.get('email', '')
    
    result = EmailAnalysisService.check_credential_exposure(email)
    return jsonify(result)

# ========== URL Analysis API ==========
@app.route('/api/analyze/url', methods=['POST'])
def analyze_url():
    """Analyze URL for phishing and spoofing"""
    data = request.get_json()
    url = data.get('url', '')
    
    result = URLAnalysisService.analyze_url(url)
    
    # Store in database
    analysis = AnalysisResult(
        analysis_type='url',
        input_hash=hash(url),
        input_data=url,
        result=result,
        risk_score=result['phishing_risk_score']
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result)

# ========== File Analysis API ==========
@app.route('/api/analyze/file', methods=['POST'])
def analyze_file():
    """Analyze file for malware"""
    data = request.get_json()
    filename = data.get('filename', '')
    file_hash = data.get('hash', '')
    
    result = FileAnalysisService.analyze_file(filename, file_hash)
    
    # Store in database
    analysis = AnalysisResult(
        analysis_type='file',
        input_hash=file_hash,
        input_data=filename,
        result=result,
        risk_score=result['risk_score']
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result)

# ========== Audio Analysis API ==========
@app.route('/api/analyze/audio', methods=['POST'])
def analyze_audio():
    """Analyze audio for deepfake detection"""
    data = request.get_json()
    
    result = AudioAnalysisService.analyze_audio(data)
    
    # Store in database
    analysis = AnalysisResult(
        analysis_type='audio',
        input_hash=hash(str(data)),
        input_data='audio_analysis',
        result=result,
        ai_probability=result['synthetic_probability']
    )
    db.session.add(analysis)
    db.session.commit()
    
    return jsonify(result)

# ========== Model Sandbox API ==========
@app.route('/api/models/test-injection', methods=['POST'])
def test_prompt_injection():
    """Test prompt injection against LLM"""
    data = request.get_json()
    
    result = PromptInjectionService.test_prompt_injection(
        data.get('prompt', ''),
        data.get('model', 'mistral'),
        data.get('attack_type', 'jailbreaking')
    )
    
    return jsonify(result)

@app.route('/api/models/list', methods=['GET'])
def list_models():
    """List available local models"""
    models = [
        {'name': 'Mistral-7B', 'size': '3.2 GB', 'purpose': 'Phishing Detection', 'status': 'active'},
        {'name': 'LLaMA2-7B', 'size': '6.8 GB', 'purpose': 'Content Analysis', 'status': 'active'},
        {'name': 'Fine-tuned Detector', 'size': '1.4 GB', 'purpose': 'AI Text Detection', 'status': 'active'},
        {'name': 'MFCC Audio Model', 'size': '0.9 GB', 'purpose': 'Deepfake Detection', 'status': 'active'},
    ]
    return jsonify(models)

# ========== Incidents API ==========
@app.route('/api/incidents', methods=['GET'])
def get_incidents():
    """Get all incidents with filtering"""
    incident_type = request.args.get('type')
    severity = request.args.get('severity')
    status = request.args.get('status')
    
    query = Incident.query
    
    if incident_type:
        query = query.filter_by(incident_type=incident_type)
    if severity:
        query = query.filter_by(severity=severity)
    if status:
        query = query.filter_by(status=status)
    
    incidents = query.order_by(Incident.created_at.desc()).all()
    return jsonify([inc.to_dict() for inc in incidents])

@app.route('/api/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    """Get specific incident details"""
    incident = Incident.query.get_or_404(incident_id)
    return jsonify(incident.to_dict())

@app.route('/api/incidents', methods=['POST'])
def create_incident():
    """Create new incident"""
    data = request.get_json()
    
    incident = Incident(
        incident_id=data.get('incident_id'),
        incident_type=data.get('incident_type'),
        severity=data.get('severity', 'Medium'),
        status=data.get('status', 'INVESTIGATING'),
        source=data.get('source'),
        target=data.get('target'),
        description=data.get('description'),
        details=data.get('details'),
        risk_score=data.get('risk_score', 0)
    )
    
    db.session.add(incident)
    db.session.commit()
    
    return jsonify(incident.to_dict()), 201

@app.route('/api/incidents/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    """Update incident status"""
    incident = Incident.query.get_or_404(incident_id)
    data = request.get_json()
    
    incident.status = data.get('status', incident.status)
    incident.description = data.get('description', incident.description)
    incident.updated_at = datetime.utcnow()
    
    if data.get('status') == 'RESOLVED':
        incident.resolved_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify(incident.to_dict())

@app.route('/api/incidents/stats', methods=['GET'])
def get_incidents_stats():
    """Get incident statistics"""
    total = Incident.query.count()
    critical = Incident.query.filter_by(severity='Critical').count()
    active = Incident.query.filter(Incident.status.in_(['BLOCKED', 'FLAGGED', 'INVESTIGATING'])).count()
    resolved = Incident.query.filter_by(status='RESOLVED').count()
    
    sla_compliance = 94.3 if resolved > 0 else 0
    
    return jsonify({
        'total': total,
        'critical': critical,
        'active': active,
        'resolved': resolved,
        'sla_compliance': sla_compliance,
        'mttr_hours': 4.2
    })

# ========== Assets API ==========
@app.route('/api/assets', methods=['GET'])
def get_assets():
    """Get all assets"""
    assets = Asset.query.all()
    return jsonify([asset.to_dict() for asset in assets])

@app.route('/api/assets/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    """Get specific asset"""
    asset = Asset.query.get_or_404(asset_id)
    return jsonify(asset.to_dict())

@app.route('/api/assets', methods=['POST'])
def create_asset():
    """Create new asset"""
    data = request.get_json()
    
    asset = Asset(
        asset_name=data.get('asset_name'),
        asset_type=data.get('asset_type'),
        asset_value=data.get('asset_value'),
        category=data.get('category'),
        description=data.get('description'),
        exposure_status=data.get('exposure_status', 'secure')
    )
    
    db.session.add(asset)
    db.session.commit()
    
    return jsonify(asset.to_dict()), 201

@app.route('/api/assets/stats', methods=['GET'])
def get_assets_stats():
    """Get asset statistics"""
    total = Asset.query.count()
    exposed = Asset.query.filter_by(exposure_status='exposed').count()
    by_type = {
        'domains': Asset.query.filter_by(asset_type='domain').count(),
        'accounts': Asset.query.filter_by(asset_type='account').count(),
        'emails': Asset.query.filter_by(asset_type='email').count(),
        'ip_ranges': Asset.query.filter_by(asset_type='ip_range').count(),
    }
    
    return jsonify({
        'total': total,
        'exposed': exposed,
        'critical_vip': Asset.query.filter_by(category='critical').count(),
        'by_type': by_type
    })

# ========== Dark Web API ==========
@app.route('/api/darkweb/exposure/<email>', methods=['GET'])
def get_darkweb_exposure(email):
    """Get dark web exposure for email"""
    result = DarkWebService.get_credential_exposure(email)
    return jsonify(result)

@app.route('/api/darkweb/stats', methods=['GET'])
def get_darkweb_stats():
    """Get dark web monitoring statistics"""
    return jsonify({
        'total_exposed_credentials': 2481,
        'forum_mentions': 842,
        'sources': {
            'BreachForums': 342,
            'Exploit.in': 289,
            'Paste Sites': 156
        },
        'geographic_hotspots': 4,
        'genai_fraud_datasets': {
            'synthetic_profiles': 5_200_000,
            'phishing_templates': 1847
        }
    })

# ========== Users API ==========
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.get_json()
    
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        role=data.get('role', 'Viewer'),
        status=data.get('status', 'active')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Log action
    audit_log = AuditLog(
        user_id=user.id,
        action='User account created',
        resource=user.username
    )
    db.session.add(audit_log)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.username = data.get('username', user.username)
    user.role = data.get('role', user.role)
    user.status = data.get('status', user.status)
    user.is_online = data.get('is_online', user.is_online)
    
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/api/users/stats', methods=['GET'])
def get_users_stats():
    """Get user statistics"""
    total = User.query.count()
    online = User.query.filter_by(is_online=True).count()
    by_role = {
        'Admin': User.query.filter_by(role='Admin').count(),
        'Analyst': User.query.filter_by(role='Analyst').count(),
        'Viewer': User.query.filter_by(role='Viewer').count(),
        'API Service': User.query.filter_by(role='API Service').count(),
    }
    
    return jsonify({
        'total': total,
        'online': online,
        'by_role': by_role
    })

# ========== Threat Intelligence API ==========
@app.route('/api/threat-intel/campaigns', methods=['GET'])
def get_threat_campaigns():
    """Get active threat campaigns"""
    campaigns = [
        {
            'name': 'Operation Phantom',
            'wave': 3,
            'vector': 'AI-generated phishing emails',
            'targets_affected': 1247,
            'status': 'Active'
        },
        {
            'name': 'Deepfake Banking Extortion',
            'wave': 2,
            'vector': 'Voice synthesis attacks on finance teams',
            'targets_affected': 89,
            'status': 'Active'
        },
        {
            'name': 'Ransomware Polymorph',
            'wave': 5,
            'vector': 'AI-obfuscated malware payloads',
            'targets_affected': 345,
            'status': 'Active'
        }
    ]
    return jsonify(campaigns)

@app.route('/api/threat-intel/actors', methods=['GET'])
def get_threat_actors():
    """Get known threat actors"""
    actors = [
        {'name': 'APT-28/Fancy Bear', 'attribution': 'Russian', 'specialization': 'Phishing'},
        {'name': 'LockBit Affiliates', 'attribution': 'eCrime', 'specialization': 'Ransomware'},
        {'name': 'Unknown eCrime', 'attribution': 'Unknown', 'specialization': 'Credential Theft'},
        {'name': 'Chinese PLA Units', 'attribution': 'Chinese', 'specialization': 'Data Exfiltration'}
    ]
    return jsonify(actors)

@app.route('/api/threat-intel/emerging-techniques', methods=['GET'])
def get_emerging_techniques():
    """Get emerging fraud techniques"""
    techniques = [
        {'technique': 'Hybrid deepfake+VoIP attacks', 'increase': '+34%', 'severity': 'critical'},
        {'technique': 'Automated jailbreak kits', 'increase': '+89%', 'severity': 'critical'},
        {'technique': 'Cookie-stealing phishing', 'increase': '+156%', 'severity': 'high'}
    ]
    return jsonify(techniques)

# ========== Forensic Reporting API ==========
@app.route('/api/forensics/metrics', methods=['GET'])
def get_forensics_metrics():
    """Get forensic reporting metrics"""
    return jsonify({
        'prevented_loss': '$2.4M',
        'period_days': 30,
        'trend': '+22%',
        'total_incidents': 1247,
        'fraud_breakdown': {
            'phishing_blocked': 456,
            'credentials_found': 241,
            'malware_detonated': 189,
            'deepfakes_detected': 34
        },
        'roi': {
            'loss_prevented': '$2.4M',
            'hours_saved': 847,
            'uptime': '99.87%'
        }
    })

@app.route('/api/forensics/case-reports', methods=['GET'])
def get_case_reports():
    """Get case reports"""
    reports = [
        {
            'case_id': 'OP-PHANTOM-2025',
            'name': 'Operation Phishing Tide',
            'loss_prevented': '$1.2M',
            'status': 'Closed'
        },
        {
            'case_id': 'DW-BREACH-2025',
            'name': 'Dark Web Breach Response',
            'loss_prevented': '$840K',
            'status': 'Closed'
        },
        {
            'case_id': 'MODEL-JAX-2025',
            'name': 'Model Jailbreak Prevention',
            'loss_prevented': '$360K',
            'status': 'Closed'
        }
    ]
    return jsonify(reports)

# ========== Audit Logging API ==========
@app.route('/api/audit-logs', methods=['GET'])
def get_audit_logs():
    """Get audit logs"""
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(20).all()
    return jsonify([log.to_dict() for log in logs])

@app.route('/api/audit-logs', methods=['POST'])
def log_action():
    """Log user action"""
    data = request.get_json()
    
    log = AuditLog(
        user_id=data.get('user_id'),
        action=data.get('action'),
        resource=data.get('resource'),
        details=data.get('details')
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify(log.to_dict()), 201

# ========== Error Handlers ==========
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ========== Health Check ==========
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
