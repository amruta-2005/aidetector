# GenAI Defense - Database Schema

Complete documentation of the SQLite database schema for the GenAI Defense system.

## Overview

**Database Type:** SQLite
**File Location:** `aidetector.db`
**Created On:** First backend startup
**Tables:** 5 main tables + relationships

## Tables

### 1. incidents

Stores security incidents and alerts detected by the system.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | INTEGER | PRIMARY KEY | Unique incident identifier |
| incident_id | VARCHAR(50) | UNIQUE, NOT NULL | Human-readable ID (e.g., INC-2024-001245) |
| incident_type | VARCHAR(50) | NOT NULL | phishing, deepfake, prompt_injection, credential_stuffing, malware |
| severity | VARCHAR(20) | NOT NULL | Critical, High, Medium, Low |
| status | VARCHAR(20) | NOT NULL | BLOCKED, FLAGGED, INVESTIGATING, MITIGATED, QUARANTINED, MONITORED, CONTAINED, RESOLVED |
| source | VARCHAR(255) | NULL | Origin of incident (email, URL, file, audio, etc.) |
| target | VARCHAR(255) | NULL | What was targeted/affected |
| description | TEXT | NULL | Detailed description |
| details | JSON | NULL | Structured incident metadata |
| risk_score | FLOAT | DEFAULT 0.0 | Risk score (0-100) |
| created_at | DATETIME | DEFAULT NOW | Timestamp when incident detected |
| updated_at | DATETIME | DEFAULT NOW | Last update timestamp |
| resolved_at | DATETIME | NULL | When incident was resolved |

**Indexes:** created_at, status, severity

**Example Record:**
```json
{
    "id": 1,
    "incident_id": "INC-2024-001245",
    "incident_type": "phishing",
    "severity": "Critical",
    "status": "BLOCKED",
    "source": "external_email",
    "target": "employees@company.com",
    "description": "AI-generated phishing with credential harvesting",
    "details": {
        "ai_probability": 88,
        "indicators": ["urgency_manipulation", "generic_greeting"],
        "detected_by": "EmailAnalysisService"
    },
    "risk_score": 88.0,
    "created_at": "2024-12-15T14:22:15",
    "updated_at": "2024-12-15T14:22:15",
    "resolved_at": null
}
```

---

### 2. assets

Tracks critical organizational resources monitored for exposure.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | INTEGER | PRIMARY KEY | Unique asset identifier |
| asset_name | VARCHAR(255) | NOT NULL | Display name (e.g., "CEO Email") |
| asset_type | VARCHAR(50) | NOT NULL | domain, email, account, ip_range |
| asset_value | VARCHAR(255) | UNIQUE, NOT NULL | Actual value (e.g., ceo@company.com) |
| category | VARCHAR(50) | NULL | critical, vip, standard |
| description | TEXT | NULL | Additional details |
| exposure_status | VARCHAR(20) | DEFAULT 'secure' | secure, monitored, exposed, critical |
| exposure_details | JSON | NULL | Details about exposure |
| created_at | DATETIME | DEFAULT NOW | Created timestamp |
| updated_at | DATETIME | DEFAULT NOW | Updated timestamp |

**Indexes:** asset_type, exposure_status, asset_value

**Example Record:**
```json
{
    "id": 1,
    "asset_name": "CISO Email",
    "asset_type": "email",
    "asset_value": "ciso@company.com",
    "category": "critical",
    "description": "Chief Information Security Officer email",
    "exposure_status": "exposed",
    "exposure_details": {
        "leaked_in": ["LinkedIn", "Adobe"],
        "dark_web_mentions": 12,
        "last_seen": "2024-12-14"
    },
    "created_at": "2024-12-01T10:00:00",
    "updated_at": "2024-12-15T09:30:00"
}
```

---

### 3. users

User accounts and access control information.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | INTEGER | PRIMARY KEY | Unique user identifier |
| username | VARCHAR(100) | UNIQUE, NOT NULL | Login username |
| email | VARCHAR(100) | UNIQUE, NOT NULL | User email address |
| role | VARCHAR(50) | NOT NULL | Admin, Analyst, Viewer, API Service |
| status | VARCHAR(20) | DEFAULT 'active' | active, inactive, suspended |
| is_online | BOOLEAN | DEFAULT False | Current online status |
| last_login | DATETIME | NULL | Last login timestamp |
| created_at | DATETIME | DEFAULT NOW | Account creation timestamp |
| updated_at | DATETIME | DEFAULT NOW | Last modification timestamp |

**Indexes:** username, email, role

**Example Record:**
```json
{
    "id": 1,
    "username": "alex_rivera",
    "email": "alex@company.com",
    "role": "Admin",
    "status": "active",
    "is_online": true,
    "last_login": "2024-12-15T09:15:00",
    "created_at": "2024-06-01T10:00:00",
    "updated_at": "2024-12-15T09:15:00"
}
```

**Available Roles:**
- **Admin** - Full system access, configuration
- **Analyst** - View, analyze, test sandboxes, manage incidents
- **Viewer** - Read-only access to dashboards and reports
- **API Service** - Automated API access for integrations

---

### 4. analysis_results

Cache of previous analysis results for quick retrieval.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | INTEGER | PRIMARY KEY | Unique result identifier |
| analysis_type | VARCHAR(50) | NOT NULL | email, url, file, audio |
| input_hash | VARCHAR(255) | UNIQUE, NOT NULL | Hash of input for deduplication |
| input_data | TEXT | NULL | Original input (truncated) |
| result | JSON | NOT NULL | Complete analysis result |
| risk_score | FLOAT | NULL | Calculated risk score |
| ai_probability | FLOAT | NULL | Probability of AI generation |
| key_indicators | JSON | NULL | Important findings |
| created_at | DATETIME | DEFAULT NOW | Analysis timestamp |

**Indexes:** analysis_type, input_hash, risk_score

**Example Record:**
```json
{
    "id": 1,
    "analysis_type": "email",
    "input_hash": "3d4f7e9a8b2c1d5f",
    "input_data": "From: noreply@paypal-verify.net...",
    "result": {
        "risk_score": 88,
        "ai_probability": 88,
        "is_phishing": true,
        "threat_level": "critical",
        "indicators": [
            "urgency_manipulation",
            "generic_greeting",
            "credential_request"
        ]
    },
    "risk_score": 88.0,
    "ai_probability": 88.0,
    "key_indicators": [
        "urgency_manipulation",
        "generic_greeting"
    ],
    "created_at": "2024-12-15T14:22:15"
}
```

---

### 5. audit_logs

Audit trail of user actions for compliance and security investigation.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | INTEGER | PRIMARY KEY | Unique log entry ID |
| user_id | INTEGER | FOREIGN KEY (users.id) | User who performed action |
| action | VARCHAR(255) | NOT NULL | Action description |
| resource | VARCHAR(255) | NULL | What was acted upon |
| details | JSON | NULL | Additional context |
| created_at | DATETIME | DEFAULT NOW | When action occurred |

**Indexes:** user_id, action, created_at

**Example Records:**
```json
{
    "id": 1,
    "user_id": 1,
    "action": "Incident status updated",
    "resource": "INC-2024-001245",
    "details": {
        "old_status": "FLAGGED",
        "new_status": "RESOLVED",
        "reason": "False positive confirmed"
    },
    "created_at": "2024-12-15T15:30:00"
},
{
    "id": 2,
    "user_id": 1,
    "action": "Model configuration changed",
    "resource": "mistral-7b",
    "details": {
        "temperature": 0.7,
        "max_tokens": 2048
    },
    "created_at": "2024-12-15T14:45:00"
},
{
    "id": 3,
    "user_id": 2,
    "action": "Security scan executed",
    "resource": "full_system_scan",
    "details": {
        "duration_seconds": 3600,
        "incidents_found": 12
    },
    "created_at": "2024-12-15T13:00:00"
}
```

---

## Relationships

### User → AuditLog (One-to-Many)
- One user can have many audit log entries
- Foreign key: `audit_logs.user_id` → `users.id`

---

## Query Examples

### Get Critical Incidents
```sql
SELECT * FROM incidents 
WHERE severity = 'Critical' 
  AND status != 'RESOLVED'
ORDER BY created_at DESC;
```

### Find Recently Exposed Assets
```sql
SELECT * FROM assets 
WHERE exposure_status IN ('exposed', 'critical')
ORDER BY updated_at DESC 
LIMIT 10;
```

### User Activity Report
```sql
SELECT users.username, COUNT(*) as action_count
FROM audit_logs
JOIN users ON audit_logs.user_id = users.id
WHERE audit_logs.created_at > datetime('now', '-30 days')
GROUP BY users.username
ORDER BY action_count DESC;
```

### Cache Hit Rate
```sql
SELECT 
    analysis_type,
    COUNT(*) as total_analyses,
    COUNT(DISTINCT input_hash) as unique_inputs,
    ROUND(100.0 * COUNT(*) / COUNT(DISTINCT input_hash), 2) as cache_hit_rate
FROM analysis_results
WHERE created_at > datetime('now', '-7 days')
GROUP BY analysis_type;
```

### Risk Posture Summary
```sql
SELECT 
    COUNT(*) as total_incidents,
    SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) as critical_count,
    SUM(CASE WHEN severity = 'High' THEN 1 ELSE 0 END) as high_count,
    AVG(risk_score) as avg_risk_score
FROM incidents
WHERE created_at > datetime('now', '-30 days');
```

---

## Data Management

### Backup

```bash
# Simple SQLite backup
cp aidetector.db aidetector.db.backup

# Or using sqlite3
sqlite3 aidetector.db ".backup aidetector.db.backup"
```

### Export to CSV

```bash
# Export incidents to CSV
sqlite3 aidetector.db \
  ".mode csv" \
  ".output incidents.csv" \
  "SELECT * FROM incidents LIMIT 1000;"
```

### Database Integrity Check

```bash
sqlite3 aidetector.db "PRAGMA integrity_check;"
```

### Optimize Database

```bash
sqlite3 aidetector.db "VACUUM;"
```

---

## Performance Considerations

### Current Indexes
- `incidents.created_at` - Fast timeline queries
- `incidents.status` - Quick status filtering
- `assets.asset_type` - Asset category queries
- `analysis_results.input_hash` - Cache lookups

### Retention Policy (Recommended)
```sql
-- Archive old incidents (> 1 year)
DELETE FROM incidents 
WHERE created_at < datetime('now', '-1 year')
  AND status = 'RESOLVED';

-- Trim analysis cache (> 3 months)
DELETE FROM analysis_results 
WHERE created_at < datetime('now', '-3 months');

-- Keep audit logs for 7 years (compliance)
-- No auto-deletion recommended
```

---

## Migration to PostgreSQL (Production)

For production deployment, consider PostgreSQL:

```python
# Update config.py
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/aidetector'

# Install driver
pip install psycopg2-binary

# Create database
createdb aidetector

# Run app - tables created automatically
python app.py
```

---

## SQLite Limitations & Solutions

| Limitation | Impact | Solution |
|-----------|--------|----------|
| Single writer | Concurrency issues | Use PostgreSQL for production |
| File-based locking | Potential corruption | Use journaling, regular backups |
| Limited query optimization | Slower complex queries | Add indexes, denormalize if needed |
| No built-in encryption | Data exposure risk | Encrypt filesystem or use PostgreSQL |

---

## Database Initialization

SQLite database is automatically created on first Flask startup:

```python
# From app.py
@app.before_request
def init_db():
    with app.app_context():
        db.create_all()
        seed_database()
```

Initial seed data includes:
- 3 sample users (Admin, Analyst, Viewer)
- 2 sample incidents
- 3 sample assets

---

## Troubleshooting

### Database Locked Error
```bash
# SQLite file is being accessed by another process
# Stop Flask and check for stale locks
rm -f aidetector.db-journal
```

### Corrupted Database
```bash
# Backup and recreate
cp aidetector.db aidetector.db.corrupt
rm aidetector.db
python app.py  # Creates fresh database
```

### Performance Issues
```sql
-- Check table sizes
SELECT 
    name,
    SUM(CASE WHEN typeof(name) = 'table' THEN 1 ELSE 0 END) as table_count,
    (SELECT COUNT(*) FROM incidents) as incidents_count
FROM sqlite_master;

-- Run VACUUM to optimize
VACUUM;
```

---

## Schema Diagram

```
┌─────────────────────┐
│      users          │
├─────────────────────┤
│ id (PK)             │
│ username (UNIQUE)   │
│ email (UNIQUE)      │
│ role                │
│ status              │
│ is_online           │
│ last_login          │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │ (1:N)
           │
           └──→ ┌──────────────────────┐
                │   audit_logs         │
                ├──────────────────────┤
                │ id (PK)              │
                │ user_id (FK)         │
                │ action               │
                │ resource             │
                │ details (JSON)       │
                │ created_at           │
                └──────────────────────┘

┌──────────────────────┐     ┌──────────────────────┐
│    incidents         │     │      assets          │
├──────────────────────┤     ├──────────────────────┤
│ id (PK)              │     │ id (PK)              │
│ incident_id (UNIQUE) │     │ asset_name           │
│ incident_type        │     │ asset_type           │
│ severity             │     │ asset_value (UNIQUE) │
│ status               │     │ category             │
│ source               │     │ exposure_status      │
│ target               │     │ exposure_details     │
│ description          │     │ created_at           │
│ details (JSON)       │     │ updated_at           │
│ risk_score           │     └──────────────────────┘
│ created_at           │
│ updated_at           │
│ resolved_at          │
└──────────────────────┘

┌──────────────────────────────┐
│    analysis_results          │
├──────────────────────────────┤
│ id (PK)                      │
│ analysis_type                │
│ input_hash (UNIQUE)          │
│ input_data                   │
│ result (JSON)                │
│ risk_score                   │
│ ai_probability               │
│ key_indicators (JSON)        │
│ created_at                   │
└──────────────────────────────┘
```

---

**Last Updated:** February 2026
**Version:** 1.0.0
