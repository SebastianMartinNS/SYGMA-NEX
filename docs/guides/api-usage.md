# 🌐 SIGMA-NEX API Usage Guide

## Overview

L'API REST di SIGMA-NEX fornisce accesso programmatico a tutte le funzionalità del sistema, consentendo l'integrazione con applicazioni esterne, sistemi ospedalieri e dispositivi medici.

## Getting Started

### Starting the API Server

```bash
# Server base
sigma server

# Server con configurazione custom
sigma server --host 0.0.0.0 --port 8080

# Server per produzione
sigma server --workers 4 --config production.yaml

# Server con SSL
sigma server --ssl-cert cert.pem --ssl-key key.pem
```

### Testing API Connection

```bash
# Health check
curl http://localhost:8000/

# Expected response
{
  "status": "ok",
  "info": "SIGMA-NEX API con logging, OSINT e blocklist attivi",
  "version": "0.2.1"
}
```

## Core Endpoints

### POST /ask - Query AI Agent

**Description**: Invia una domanda all'agente AI e ricevi una risposta elaborata.

**Request**:
```http
POST /ask
Content-Type: application/json

{
  "question": "Come disinfettare una ferita?",
  "history": [
    "Ciao",
    "Salve! Come posso aiutarti?"
  ],
  "user_id": 123,
  "chat_id": 456,
  "username": "medic1",
  "context": {
    "medical_priority": true,
    "emergency": false,
    "patient_age": 35,
    "patient_gender": "M"
  }
}
```

**Response**:
```json
{
  "response": "🏥 Per disinfettare correttamente una ferita:\n\n1. **Lavaggio mani**: Lavati le mani con sapone antibatterico\n2. **Pulizia ferita**: Rimuovi delicatamente sporco e detriti\n3. **Disinfettante**: Applica:\n   - Acqua ossigenata (3%)\n   - Clorexidina (0.5%)\n   - Alcol etilico (70%)\n4. **Copertura**: Applica benda sterile\n\n⚠️ **ATTENZIONE**: Se la ferita è profonda o non smette di sanguinare, consulta immediatamente un medico.",
  "metadata": {
    "processing_time": 1.234,
    "model_used": "mistral",
    "retrieval_used": true,
    "medical_context": true,
    "confidence": 0.95
  }
}
```

### GET / - Health Check

**Description**: Verifica lo stato del sistema.

**Response**:
```json
{
  "status": "ok",
  "info": "SIGMA-NEX API active",
  "version": "0.2.1",
  "components": {
    "ollama": "connected",
    "retrieval": "active",
    "translation": "available"
  },
  "uptime": 3600,
  "timestamp": "2024-09-23T10:30:00Z"
}
```

### GET /logs - System Logs (Admin Only)

**Description**: Recupera i log del sistema (solo da localhost).

**Parameters**:
- `last` (optional): Numero di entry recenti (default: 50)
- `level` (optional): Livello di log (DEBUG, INFO, WARNING, ERROR)
- `since` (optional): Timestamp ISO 8601

**Request**:
```http
GET /logs?last=100&level=INFO&since=2024-09-23T00:00:00Z
```

**Response**:
```json
[
  {
    "timestamp": "2024-09-23T10:30:00Z",
    "level": "INFO",
    "user_id": 123,
    "question_hash": "sha256...",
    "response_length": 256,
    "ip": "127.0.0.1",
    "processing_time": 1.23,
    "model": "mistral",
    "medical": true
  }
]
```

### GET /logfile - Download Logs (Admin Only)

**Description**: Scarica il file di log completo.

**Response**: File di testo con tutti i log del sistema.

## Advanced Endpoints

### POST /batch - Batch Processing

**Description**: Processa multiple query in una singola richiesta.

**Request**:
```json
{
  "queries": [
    {
      "id": "q1",
      "question": "Sintomi dell'infarto",
      "priority": "high"
    },
    {
      "id": "q2", 
      "question": "Dosaggio ibuprofene adulti",
      "priority": "normal"
    }
  ],
  "user_id": 123,
  "batch_options": {
    "parallel": true,
    "timeout": 30
  }
}
```

**Response**:
```json
{
  "results": [
    {
      "id": "q1",
      "response": "🚨 SINTOMI INFARTO MIOCARDICO...",
      "status": "success",
      "processing_time": 2.1
    },
    {
      "id": "q2",
      "response": "💊 DOSAGGIO IBUPROFENE...",
      "status": "success", 
      "processing_time": 1.8
    }
  ],
  "total_time": 2.3,
  "success_count": 2,
  "error_count": 0
}
```

### GET /models - Available Models

**Description**: Lista dei modelli AI disponibili.

**Response**:
```json
{
  "models": [
    {
      "name": "mistral",
      "type": "general",
      "status": "loaded",
      "size": "4.1GB",
      "capabilities": ["text", "medical"]
    },
    {
      "name": "medllama2",
      "type": "medical",
      "status": "available",
      "size": "7.3GB", 
      "capabilities": ["medical", "emergency"]
    }
  ],
  "active_model": "mistral"
}
```

### POST /search - Semantic Search

**Description**: Ricerca semantica nei documenti indicizzati.

**Request**:
```json
{
  "query": "primo soccorso ustioni",
  "top_k": 5,
  "filters": {
    "category": "emergency",
    "language": "it"
  }
}
```

**Response**:
```json
{
  "results": [
    {
      "text": "Trattamento ustioni di primo grado...",
      "score": 0.92,
      "source": "emergency_protocols.pdf",
      "category": "emergency"
    }
  ],
  "total_results": 5,
  "processing_time": 0.45
}
```

### POST /translate - Translation Service

**Description**: Traduce testo tra lingue supportate.

**Request**:
```json
{
  "text": "How to treat a burn?",
  "source_lang": "en",
  "target_lang": "it",
  "preserve_medical": true
}
```

**Response**:
```json
{
  "translated_text": "Come trattare un'ustione?",
  "source_language": "en",
  "target_language": "it",
  "confidence": 0.98,
  "medical_terms_preserved": ["burn"]
}
```

## Medical-Specific Endpoints

### POST /emergency - Emergency Protocols

**Description**: Accesso rapido ai protocolli di emergenza.

**Request**:
```json
{
  "emergency_type": "cardiac_arrest",
  "patient_info": {
    "age": 45,
    "gender": "M",
    "conscious": false
  },
  "location": "hospital"
}
```

**Response**:
```json
{
  "protocol": {
    "name": "Basic Life Support - Adult",
    "steps": [
      {
        "step": 1,
        "action": "Check responsiveness",
        "description": "Tap shoulders and shout 'Are you okay?'",
        "duration": "5 seconds"
      },
      {
        "step": 2,
        "action": "Call for help",
        "description": "Call 112 and request AED",
        "duration": "immediate"
      }
    ]
  },
  "priority": "critical",
  "estimated_time": "immediate"
}
```

### POST /drug-check - Drug Information

**Description**: Verifica informazioni su farmaci e interazioni.

**Request**:
```json
{
  "drugs": ["ibuprofene", "paracetamolo"],
  "patient": {
    "age": 65,
    "weight": 70,
    "allergies": ["penicillina"],
    "conditions": ["ipertensione"]
  }
}
```

**Response**:
```json
{
  "interactions": [
    {
      "drug1": "ibuprofene",
      "drug2": "paracetamolo", 
      "severity": "minor",
      "description": "Nessuna interazione significativa"
    }
  ],
  "dosage_recommendations": {
    "ibuprofene": "400mg ogni 6-8 ore, max 1200mg/die",
    "paracetamolo": "500-1000mg ogni 4-6 ore, max 3000mg/die"
  },
  "warnings": [
    "Monitorare funzione renale con ibuprofene"
  ]
}
```

## Authentication & Authorization

### API Key Authentication (Planned)

```http
POST /ask
Authorization: Bearer your-api-key-here
Content-Type: application/json

{
  "question": "Medical query"
}
```

### JWT Token Authentication (Planned)

```http
POST /auth/login
Content-Type: application/json

{
  "username": "medic1",
  "password": "secure_password"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_token_here"
}
```

## Error Handling

### Standard Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid query format",
    "details": {
      "field": "question",
      "issue": "Question cannot be empty"
    },
    "timestamp": "2024-09-23T10:30:00Z",
    "request_id": "req_12345"
  }
}
```

### HTTP Status Codes

| Code | Description | Common Causes |
|------|-------------|---------------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid JSON, missing required fields |
| 401 | Unauthorized | Invalid API key or token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Endpoint not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error, model unavailable |
| 503 | Service Unavailable | System maintenance, Ollama down |

### Error Categories

```python
# Error types and handling
ERROR_CODES = {
    "VALIDATION_ERROR": 400,
    "AUTHENTICATION_ERROR": 401,
    "AUTHORIZATION_ERROR": 403,
    "RATE_LIMIT_ERROR": 429,
    "MODEL_ERROR": 500,
    "SYSTEM_ERROR": 500,
    "TIMEOUT_ERROR": 504
}
```

## Rate Limiting

### Default Limits

```yaml
rate_limiting:
  enabled: true
  rules:
    - path: "/ask"
      limit: "60/minute"
      burst: 10
    - path: "/batch"
      limit: "10/minute"
      burst: 2
    - path: "/emergency"
      limit: "unlimited"  # No limit for emergencies
```

### Rate Limit Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1695456000
X-RateLimit-Retry-After: 60
```

## SDK and Client Libraries

### Python SDK

```python
from sigma_nex import SigmaNexClient

# Initialize client
client = SigmaNexClient(
    base_url="http://localhost:8000",
    api_key="your-api-key"  # When authentication is enabled
)

# Simple query
response = client.ask("Come misurare la pressione?")
print(response.text)

# Medical priority query
response = client.ask(
    "Dolore al petto acuto",
    medical_priority=True,
    user_id=123
)

# Batch processing
responses = client.batch([
    "Sintomi infarto",
    "Primo soccorso ustioni",
    "Dosaggio aspirina"
])

# Emergency protocol
protocol = client.emergency("cardiac_arrest", patient_age=45)
```

### JavaScript SDK

```javascript
import { SigmaNexClient } from 'sigma-nex-js';

const client = new SigmaNexClient({
  baseURL: 'http://localhost:8000',
  apiKey: 'your-api-key'
});

// Simple query
const response = await client.ask('Come disinfettare una ferita?');
console.log(response.data.response);

// Medical query with context
const medicalResponse = await client.ask('Dosaggio ibuprofene', {
  context: {
    patientAge: 35,
    patientWeight: 70,
    medicalPriority: true
  }
});

// Emergency protocol
const emergency = await client.emergency('cardiac_arrest', {
  patientAge: 45,
  conscious: false
});
```

### cURL Examples

```bash
# Basic query
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Come trattare una ferita?",
    "user_id": 123
  }'

# Medical priority query
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Dolore al petto acuto",
    "context": {
      "medical_priority": true,
      "emergency": true
    }
  }'

# Batch processing
curl -X POST http://localhost:8000/batch \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      {"id": "q1", "question": "Sintomi infarto"},
      {"id": "q2", "question": "Primo soccorso"}
    ]
  }'
```

## Integration Examples

### Hospital Information System

```python
class HospitalIntegration:
    def __init__(self):
        self.sigma_client = SigmaNexClient("http://sigma-nex:8000")
        self.his_client = HISClient()
    
    def patient_consultation(self, patient_id: str, symptoms: str):
        # Get patient data from HIS
        patient = self.his_client.get_patient(patient_id)
        
        # Query SIGMA-NEX with patient context
        response = self.sigma_client.ask(
            f"Paziente {patient.age} anni, sintomi: {symptoms}",
            context={
                "patient_age": patient.age,
                "patient_gender": patient.gender,
                "medical_history": patient.history,
                "current_medications": patient.medications
            }
        )
        
        # Log consultation in HIS
        self.his_client.log_consultation(
            patient_id=patient_id,
            ai_consultation=response.text,
            timestamp=datetime.now()
        )
        
        return response.text
```

### Emergency Department Integration

```python
class EmergencyDepartment:
    def __init__(self):
        self.sigma_client = SigmaNexClient("http://sigma-nex:8000")
    
    def triage_assessment(self, symptoms: str, vital_signs: dict):
        # Emergency triage with SIGMA-NEX
        response = self.sigma_client.ask(
            f"Triage: {symptoms}",
            context={
                "emergency": True,
                "vital_signs": vital_signs,
                "location": "emergency_department"
            }
        )
        
        # Determine triage level
        triage_level = self.extract_triage_level(response.text)
        
        return {
            "triage_level": triage_level,
            "ai_assessment": response.text,
            "recommendations": self.extract_recommendations(response.text)
        }
```

### Mobile App Integration

```javascript
// React Native example
import { SigmaNexClient } from 'sigma-nex-js';

const MedicalAssistantApp = () => {
  const [client] = useState(new SigmaNexClient({
    baseURL: 'https://your-sigma-nex-server.com',
    timeout: 30000
  }));

  const askMedicalQuestion = async (question) => {
    try {
      const response = await client.ask(question, {
        context: {
          mobile_app: true,
          user_location: await getUserLocation(),
          medical_priority: true
        }
      });
      
      return response.data.response;
    } catch (error) {
      console.error('Medical query failed:', error);
      return 'Errore nella consultazione. Riprova o contatta un medico.';
    }
  };

  return (
    <MedicalChat onQuestion={askMedicalQuestion} />
  );
};
```

## Monitoring and Analytics

### API Metrics

```python
# Prometheus metrics for API monitoring
from prometheus_client import Counter, Histogram

api_requests = Counter('sigma_api_requests_total', 
                      'API requests', ['endpoint', 'method', 'status'])

request_duration = Histogram('sigma_api_request_duration_seconds',
                           'Request duration', ['endpoint'])

medical_queries = Counter('sigma_medical_queries_total',
                         'Medical queries', ['type', 'priority'])
```

### Health Monitoring

```bash
# API health check script
#!/bin/bash
ENDPOINT="http://localhost:8000"

# Basic health check
curl -f $ENDPOINT/ || exit 1

# Functional test
RESPONSE=$(curl -s -X POST $ENDPOINT/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "test"}')

if [[ $RESPONSE == *"response"* ]]; then
  echo "✅ API functional test passed"
else
  echo "❌ API functional test failed"
  exit 1
fi
```

## Security Considerations

### Input Validation

All API endpoints implement comprehensive input validation:

- **Query Length**: Maximum 10,000 characters
- **SQL Injection**: Pattern-based filtering
- **XSS Prevention**: HTML sanitization
- **Path Traversal**: File path validation
- **Medical Context**: Medical query validation

### Data Privacy

- **Query Logging**: Configurable query logging
- **Anonymization**: Automatic PII removal
- **Audit Trail**: Comprehensive access logging
- **HIPAA Compliance**: Medical data protection
- **Encryption**: TLS for data in transit

### Network Security

```yaml
# Security configuration
security:
  cors:
    enabled: true
    allowed_origins: ["https://your-domain.com"]
    allowed_methods: ["GET", "POST"]
    
  rate_limiting:
    enabled: true
    redis_url: "redis://localhost:6379"
    
  ip_filtering:
    whitelist: ["192.168.0.0/16"]
    blacklist: []
```

## Troubleshooting API Issues

### Common Problems

#### Connection Issues

```bash
# Test API connectivity
curl -v http://localhost:8000/

# Check server status
sigma status --server

# View server logs
sigma logs tail --server
```

#### Performance Issues

```bash
# Monitor API performance
curl -w "@curl-format.txt" http://localhost:8000/ask

# Where curl-format.txt contains:
#     time_namelookup:  %{time_namelookup}\n
#     time_connect:     %{time_connect}\n
#     time_appconnect:  %{time_appconnect}\n
#     time_pretransfer: %{time_pretransfer}\n
#     time_redirect:    %{time_redirect}\n
#     time_starttransfer: %{time_starttransfer}\n
#                    ----------\n
#     time_total:       %{time_total}\n
```

#### Error Diagnosis

```python
# API client with error handling
import requests

def robust_api_call(question: str):
    try:
        response = requests.post(
            "http://localhost:8000/ask",
            json={"question": question},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        return {"error": "Request timeout - try again"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API server"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
```

For API support and documentation:
- **API Documentation**: https://api.sigma-nex.org/docs
- **SDK Documentation**: https://sdk.sigma-nex.org
- **API Support**: rootedlab6@gmail.com
- **Integration Help**: rootedlab6@gmail.com