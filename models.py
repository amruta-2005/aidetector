from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Incident(db.Model):
    """Incident model for tracking security events"""
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.String(50), unique=True, nullable=False)
    incident_type = db.Column(db.String(50), nullable=False)  # phishing, deepfake, prompt_injection, credential_stuffing
    severity = db.Column(db.String(20), nullable=False)  # Critical, High, Medium, Low
    status = db.Column(db.String(20), nullable=False)  # BLOCKED, FLAGGED, INVESTIGATING, MITIGATED, QUARANTINED, MONITORED, CONTAINED, RESOLVED
    source = db.Column(db.String(255))
    target = db.Column(db.String(255))
    description = db.Column(db.Text)
    details = db.Column(db.JSON)
    risk_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'incident_type': self.incident_type,
            'severity': self.severity,
            'status': self.status,
            'source': self.source,
            'target': self.target,
            'description': self.description,
            'details': self.details,
            'risk_score': self.risk_score,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }

class Asset(db.Model):
    """Asset model for tracking critical organizational resources"""
    __tablename__ = 'assets'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(255), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)  # domain, email, account, ip_range
    asset_value = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(50))  # critical, vip, standard
    description = db.Column(db.Text)
    exposure_status = db.Column(db.String(20), default='secure')  # secure, monitored, exposed, critical
    exposure_details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_name': self.asset_name,
            'asset_type': self.asset_type,
            'asset_value': self.asset_value,
            'category': self.category,
            'description': self.description,
            'exposure_status': self.exposure_status,
            'exposure_details': self.exposure_details,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class User(db.Model):
    """User model for access control"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Admin, Analyst, Viewer, API Service
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    is_online = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'is_online': self.is_online,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AnalysisResult(db.Model):
    """Analysis results cache for emails, URLs, files"""
    __tablename__ = 'analysis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_type = db.Column(db.String(50), nullable=False)  # email, url, file, audio
    input_hash = db.Column(db.String(255), unique=True, nullable=False)
    input_data = db.Column(db.Text)
    result = db.Column(db.JSON)
    risk_score = db.Column(db.Float)
    ai_probability = db.Column(db.Float)  # Probability this is AI-generated
    key_indicators = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'analysis_type': self.analysis_type,
            'input_hash': self.input_hash,
            'result': self.result,
            'risk_score': self.risk_score,
            'ai_probability': self.ai_probability,
            'key_indicators': self.key_indicators,
            'created_at': self.created_at.isoformat()
        }

class AuditLog(db.Model):
    """Audit log for tracking user actions"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(255), nullable=False)
    resource = db.Column(db.String(255))
    details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource': self.resource,
            'details': self.details,
            'created_at': self.created_at.isoformat()
        }
