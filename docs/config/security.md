# 🛡️ Security Configuration

## Security Overview

SIGMA-NEX implements a comprehensive security framework designed to protect sensitive medical data and ensure system integrity in offline environments.

## Security Configuration

### Core Security Settings

```yaml
# config.yaml - Security section
security:
  # === ENCRYPTION ===
  encryption:
    enabled: true                    # Enable encryption at rest
    algorithm: "AES-256-GCM"        # Encryption algorithm
    key_rotation_hours: 24          # Key rotation interval
    backup_keys: 3                  # Number of backup keys
    
  # === ACCESS CONTROL ===
  access_control:
    enabled: true                   # Enable access control
    default_deny: true              # Default deny policy
    ip_whitelist:                   # Allowed IP addresses
      - "127.0.0.1"
      - "192.168.0.0/16"
      - "10.0.0.0/8"
    ip_blacklist: []                # Blocked IP addresses
    
  # === RATE LIMITING ===
  rate_limiting:
    enabled: true                   # Enable rate limiting
    requests_per_minute: 60         # Max requests per minute
    requests_per_hour: 1000         # Max requests per hour
    burst_size: 10                  # Burst capacity
    
  # === AUDIT & LOGGING ===
  audit:
    enabled: true                   # Enable audit logging
    log_queries: true               # Log user queries
    log_responses: false            # Don't log responses (privacy)
    anonymize_personal: true        # Anonymize personal data
    retention_days: 90              # Log retention period
    
  # === INPUT VALIDATION ===
  validation:
    enabled: true                   # Enable input validation
    max_query_length: 10000         # Max query length
    blocked_patterns:               # Blocked regex patterns
      - "(?i)(select|drop|delete|insert|update)\\s"
      - "(?i)(<script|javascript:)"
      - "(?i)(\\.\\.[\\/\\\\])"
    sanitize_html: true             # Strip HTML tags
    
  # === MEDICAL DATA PROTECTION ===
  medical:
    anonymize_patient_data: true    # Anonymize patient references
    mask_sensitive_info: true       # Mask SSN, phone numbers
    medical_audit: true             # Enhanced medical audit
    hipaa_compliance: true          # HIPAA compliance mode
```

### Environment Variables

```bash
# Security environment variables
export SIGMA_ENCRYPTION_KEY="your-32-char-encryption-key-here-12345"
export SIGMA_SALT="your-salt-value-here"
export SIGMA_SECRET_KEY="your-secret-key-for-sessions"

# Security features
export SIGMA_SECURITY_MODE="strict"
export SIGMA_AUDIT_LEVEL="high"
export SIGMA_ANONYMIZE_LOGS="true"

# Access control
export SIGMA_ALLOWED_IPS="127.0.0.1,192.168.1.0/24"
export SIGMA_RATE_LIMIT="100"
```

## Encryption Configuration

### Data Encryption

```yaml
encryption:
  # At-rest encryption
  data_encryption:
    enabled: true
    key_file: "~/.sigma-nex/keys/data.key"
    cipher: "AES-256-GCM"
    key_derivation: "PBKDF2"
    iterations: 100000
    
  # In-transit encryption
  transport_encryption:
    enabled: true
    tls_version: "1.3"
    cert_file: "/etc/ssl/sigma-nex.crt"
    key_file: "/etc/ssl/sigma-nex.key"
    ca_file: "/etc/ssl/ca.crt"
    
  # Memory encryption
  memory_encryption:
    enabled: true
    secure_delete: true
    memory_limit: "1GB"
```

### Key Management

```python
# Key management example
from sigma_nex.security import KeyManager

km = KeyManager()

# Generate new encryption key
key = km.generate_key()

# Store key securely
km.store_key("data_encryption", key)

# Rotate keys
km.rotate_key("data_encryption")

# Backup keys
km.backup_keys("/secure/backup/location")
```

## Access Control

### IP-Based Access Control

```yaml
access_control:
  ip_filtering:
    enabled: true
    mode: "whitelist"               # whitelist or blacklist
    
    whitelist:
      - "127.0.0.1"                # Localhost
      - "192.168.0.0/16"           # Private network
      - "10.0.0.0/8"               # Corporate network
      
    blacklist:
      - "0.0.0.0/0"                # Block all (for blacklist mode)
      
  geo_blocking:
    enabled: false                  # Geographic filtering
    allowed_countries: ["IT", "US", "CA"]
    blocked_countries: ["CN", "RU"]
```

### Role-Based Access Control (Planned)

```yaml
rbac:
  enabled: false                    # Future feature
  roles:
    admin:
      permissions: ["*"]
    medical_staff:
      permissions: ["query", "medical_data", "emergency"]
    user:
      permissions: ["query"]
      
  users:
    - username: "admin"
      role: "admin"
      password_hash: "hashed_password"
    - username: "doctor1"
      role: "medical_staff"
      mfa_required: true
```

## Input Validation & Sanitization

### Query Validation

```yaml
validation:
  query_validation:
    enabled: true
    max_length: 10000               # Maximum query length
    min_length: 1                   # Minimum query length
    
    blocked_patterns:
      # SQL injection prevention
      - "(?i)(select|drop|delete|insert|update|union|exec)\\s"
      # XSS prevention
      - "(?i)(<script|javascript:|onload=|onclick=)"
      # Path traversal prevention
      - "(?i)(\\.\\.[\\/\\\\]|\\.[\\/\\\\]etc[\\/\\\\])"
      # Command injection prevention
      - "(?i)(;|\\||&|`|\\$\\(|\\$\\{)"
      
    allowed_patterns:
      # Medical terms are always allowed
      - "(?i)(symptoms?|treatment|medication|dosage)"
      
  response_filtering:
    enabled: true
    remove_sensitive: true          # Remove sensitive information
    medical_disclaimer: true        # Add medical disclaimers
```

### Sanitization Functions

```python
from sigma_nex.security.validation import sanitize_input

def process_query(raw_query: str) -> str:
    """Process and sanitize user query."""
    
    # Basic sanitization
    sanitized = sanitize_input(raw_query)
    
    # Medical-specific validation
    if is_medical_query(sanitized):
        sanitized = medical_sanitize(sanitized)
    
    # Length validation
    if len(sanitized) > MAX_QUERY_LENGTH:
        raise ValueError("Query too long")
        
    return sanitized
```

## Audit and Logging

### Audit Configuration

```yaml
audit:
  general:
    enabled: true
    log_level: "INFO"
    format: "json"
    destination: "file"             # file, syslog, database
    
  medical_audit:
    enabled: true
    enhanced_logging: true
    anonymize_patient_data: true
    require_justification: false    # Future feature
    
  security_events:
    failed_logins: true
    rate_limit_exceeded: true
    blocked_queries: true
    encryption_events: true
    
  log_rotation:
    enabled: true
    max_size: "100MB"
    backup_count: 10
    compression: true
```

### Audit Log Format

```json
{
  "timestamp": "2024-09-23T10:30:00Z",
  "event_type": "query_processed",
  "user_id": "anonymous_12345",
  "session_id": "sess_abcdef",
  "ip_address": "192.168.1.100",
  "query_hash": "sha256_hash_of_query",
  "query_type": "medical",
  "processing_time": 1.23,
  "model_used": "mistral",
  "retrieval_used": true,
  "security_level": "high",
  "anonymized": true,
  "compliance": {
    "hipaa": true,
    "gdpr": true
  }
}
```

## Medical Data Protection

### HIPAA Compliance

```yaml
hipaa_compliance:
  enabled: true
  
  # Minimum necessary standard
  data_minimization: true
  access_logging: true
  
  # Administrative safeguards
  assigned_security_responsibility: true
  workforce_training: true
  access_management: true
  
  # Physical safeguards
  facility_access_controls: true
  workstation_use: true
  media_controls: true
  
  # Technical safeguards
  access_control: true
  audit_controls: true
  integrity: true
  transmission_security: true
```

### Data Anonymization

```python
from sigma_nex.security.anonymization import anonymize_medical_data

def anonymize_query(query: str) -> str:
    """Anonymize medical query for logging."""
    
    # Remove personal identifiers
    query = remove_names(query)
    query = remove_ssn(query)
    query = remove_phone_numbers(query)
    query = remove_addresses(query)
    
    # Replace with placeholders
    query = replace_ages_with_ranges(query)
    query = replace_dates_with_relative(query)
    
    return query
```

## Security Monitoring

### Real-time Monitoring

```yaml
monitoring:
  security_monitoring:
    enabled: true
    real_time_alerts: true
    
    alerts:
      failed_authentication: true
      rate_limit_exceeded: true
      suspicious_queries: true
      encryption_failures: true
      
    thresholds:
      failed_login_threshold: 5
      query_rate_threshold: 100
      error_rate_threshold: 10
      
  intrusion_detection:
    enabled: true
    pattern_matching: true
    anomaly_detection: true
    behavioral_analysis: true
```

### Security Metrics

```python
# Security metrics collection
from prometheus_client import Counter, Histogram

security_events = Counter('sigma_security_events_total', 
                         'Security events', ['event_type'])

query_validation_time = Histogram('sigma_query_validation_seconds',
                                 'Time spent validating queries')

encryption_operations = Counter('sigma_encryption_operations_total',
                               'Encryption operations', ['operation'])
```

## Incident Response

### Security Incident Configuration

```yaml
incident_response:
  enabled: true
  
  automatic_responses:
    block_suspicious_ip: true
    rate_limit_aggressive: true
    alert_administrators: true
    
  escalation:
    level_1_threshold: 10           # Suspicious events
    level_2_threshold: 50           # Potential attack
    level_3_threshold: 100          # Active attack
    
  notification:
    email_alerts: true
    sms_alerts: false
    webhook_alerts: true
    
  quarantine:
    enabled: true
    automatic_quarantine: true
    quarantine_duration: 3600       # 1 hour
```

### Backup Security

```yaml
backup_security:
  encryption:
    enabled: true
    separate_key: true
    
  verification:
    integrity_checks: true
    regular_testing: true
    
  storage:
    offline_backups: true
    geographic_distribution: true
    access_control: true
```

## Compliance

### Regulatory Compliance

```yaml
compliance:
  standards:
    hipaa: true                     # Health Insurance Portability
    gdpr: true                      # General Data Protection Regulation
    iso27001: true                  # Information Security Management
    
  audit_requirements:
    regular_assessments: true
    penetration_testing: true
    vulnerability_scanning: true
    
  documentation:
    security_policies: true
    incident_procedures: true
    training_materials: true
```

## Security Best Practices

### Development Security

1. **Secure Coding**:
   - Input validation at all entry points
   - Output encoding for all outputs
   - Principle of least privilege
   - Defense in depth

2. **Testing**:
   - Security unit tests
   - Penetration testing
   - Vulnerability assessments
   - Code security scanning

3. **Dependencies**:
   - Regular security updates
   - Vulnerability scanning
   - Secure package sources
   - License compliance

### Operational Security

1. **Infrastructure**:
   - Network segmentation
   - Firewall configuration
   - Regular security updates
   - Monitoring and alerting

2. **Data Protection**:
   - Encryption at rest and in transit
   - Secure key management
   - Regular backups
   - Data retention policies

3. **Access Management**:
   - Strong authentication
   - Role-based access control
   - Regular access reviews
   - Session management

For security support:
- **Security Team**: rootedlab6@gmail.com
- **Incident Response**: rootedlab6@gmail.com
- **Vulnerability Reports**: rootedlab6@gmail.com
