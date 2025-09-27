# SIGMA-NEX API Reference

## Overview

SIGMA-NEX provides a RESTful API for interacting with the cognitive agent. The API is built with FastAPI and provides endpoints for querying the agent, managing logs, and system health checks.

## Base URL

When running locally:
```
http://localhost:8000
```

## Authentication

The API uses API key authentication for security. Configure API keys in your `config.yaml`:

```yaml
api_keys:
  - "your-api-key-1"
  - "your-api-key-2"
```

Include the API key in requests:

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Authorization: Bearer your-api-key-1" \
  -H "Content-Type: application/json" \
  -d '{"question": "Test question"}'
```

**Security Note**: Never commit API keys to version control. Use environment variables or secure configuration management.

For support and security issues, contact: rootedlab6@gmail.com

## Endpoints

### POST /ask

Query the SIGMA-NEX cognitive agent.

**Request Body:**
```json
{
  "question": "string",
  "history": ["string"],  // Optional
  "user_id": 123,         // Optional
  "chat_id": 456,         // Optional
  "username": "string"    // Optional
}
```

**Response:**
```json
{
  "response": "string"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Come posso disinfettare una ferita?",
    "user_id": 123
  }'
```

### GET /

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "info": "SIGMA-NEX API con logging, OSINT e blocklist attivi",
  "version": "0.3.1"
}
```

### GET /logs

Get recent system logs (localhost only).

**Parameters:**
- `last` (optional): Number of recent log entries to return (default: 50)

**Response:**
```json
[
  {
    "timestamp": "2024-01-01T12:00:00Z",
    "user_id": 123,
    "question": "example question",
    "response": "example response",
    "ip": "127.0.0.1",
    ...
  }
]
```

### GET /logfile

Download the complete log file (localhost only).

**Response:** Plain text file download

## Response Processing

The API processes queries through the SIGMA-NEX cognitive engine, which includes context management, semantic retrieval, and translation capabilities when needed.

## Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `400` - Bad Request
- `403` - Forbidden (for restricted endpoints)
- `404` - Not Found
- `500` - Internal Server Error

Error responses include details:
```json
{
  "detail": "Error description"
}
```

## Rate Limiting and Security

- Request logging and monitoring
- IP-based access control for sensitive endpoints
- Input validation and sanitization
- Secure communication protocols

## Starting the Server

```bash
# Using CLI
sigma server --host 0.0.0.0 --port 8000

# Using uvicorn directly
uvicorn sigma_nex.server:app --host 0.0.0.0 --port 8000

# Using Python module
python -m sigma_nex.server --port 8000
```
