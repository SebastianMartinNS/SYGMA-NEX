# Runner API Reference

## Overview

The Runner is the core execution engine of SIGMA-NEX, responsible for processing queries and managing the interaction with AI models.

## Class: Runner

```python
from sigma_nex.core.runner import Runner

runner = Runner(config=config_dict)
```

### Constructor

**Parameters:**
- `config` (dict): Configuration dictionary containing model settings

### Methods

#### `process_query(query: str, history: List[str] = None) -> str`

Process a user query and return the AI response.

**Parameters:**
- `query` (str): The user's question or command
- `history` (List[str], optional): Previous conversation history

**Returns:**
- `str`: The AI model's response

**Example:**
```python
runner = Runner({'model_name': 'mistral'})
response = runner.process_query("Come posso disinfettare una ferita?")
print(response)
```

#### `build_context(query: str, history: List[str] = None) -> str`

Build the complete context for the AI model including system prompt, history, and current query.

**Parameters:**
- `query` (str): Current user query
- `history` (List[str], optional): Conversation history

**Returns:**
- `str`: Complete formatted context

#### `self_heal() -> bool`

Attempt to recover from errors and restore normal operation.

**Returns:**
- `bool`: True if recovery successful, False otherwise

## Configuration Options

```yaml
# Ollama settings
model_name: "mistral"          # AI model to use
temperature: 0.7               # Response creativity (0.0-1.0)
max_tokens: 2048              # Maximum response length

# System behavior
debug: false                   # Enable debug logging
retrieval_enabled: true       # Enable semantic search
max_history: 100              # Maximum conversation history
```

## Error Handling

The Runner implements comprehensive error handling:

- **Model Connection Errors**: Automatic retry with exponential backoff
- **Timeout Errors**: Configurable timeout limits
- **Memory Errors**: Automatic history truncation
- **Invalid Input**: Input sanitization and validation

## Integration Examples

### CLI Integration
```python
from sigma_nex.core.runner import Runner
from sigma_nex.config import load_config

config = load_config()
runner = Runner(config)

while True:
    query = input(">> ")
    if query.lower() in ['exit', 'quit']:
        break
    response = runner.process_query(query)
    print(response)
```

### API Server Integration
```python
from fastapi import FastAPI
from sigma_nex.core.runner import Runner

app = FastAPI()
runner = Runner(config)

@app.post("/ask")
async def ask_question(query: str):
    response = runner.process_query(query)
    return {"response": response}
```

## Performance Considerations

- **Model Loading**: Models are loaded once at initialization
- **Context Caching**: Recent contexts are cached for faster responses
- **Memory Management**: Automatic cleanup of old history
- **Concurrent Requests**: Thread-safe for multiple simultaneous queries

## Security Features

- **Input Sanitization**: All inputs are validated and sanitized
- **Query Filtering**: Malicious queries are blocked
- **Rate Limiting**: Configurable request rate limits
- **Audit Logging**: All queries are logged for security analysis