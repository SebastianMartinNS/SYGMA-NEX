# SIGMA-NEX API Reference

## Overview

SIGMA-NEX provides a RESTful API for interacting with the cognitive agent. The API is built with FastAPI and provides endpoints for querying the agent, managing logs, and system health checks.

## Base URL

When running locally:
```
http://localhost:8000
```

## Authentication

Currently, the API uses IP-based filtering for administrative endpoints. Only localhost (127.0.0.1) can access sensitive endpoints like logs.

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
  "version": "0.2.1"
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

## Medical Integration

The API automatically detects medical-related queries and provides enhanced responses using specialized medical models when available.

**Medical Keywords Detected:**
- medicina, disinfettante, ferita, primo soccorso
- antibiotico, kit medico, antiseptico, benda
- farmaco, antidolorifico, ustione, medicazione
- And many more...

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

- Blocklist functionality for users/chats
- Request logging with OSINT data collection
- IP-based access control for sensitive endpoints
- No rate limiting currently implemented

## Starting the Server

```bash
# Using CLI
sigma server --host 0.0.0.0 --port 8000

# Using uvicorn directly
uvicorn sigma_nex.server:app --host 0.0.0.0 --port 8000

# Using Python module
python -m sigma_nex.server --port 8000
```