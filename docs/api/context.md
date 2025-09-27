# Context API Reference

## Overview

The Context module manages conversation context, prompt building, and history management for SIGMA-NEX.

## Class: ContextBuilder

```python
from sigma_nex.core.context import ContextBuilder

context_builder = ContextBuilder(config)
```

### Methods

#### `build_prompt(query: str, history: List[str] = None, system_prompt: str = None) -> str`

Build a complete prompt for the AI model.

**Parameters:**
- `query` (str): Current user query
- `history` (List[str], optional): Conversation history
- `system_prompt` (str, optional): Override default system prompt

**Returns:**
- `str`: Complete formatted prompt

**Example:**
```python
builder = ContextBuilder(config)
prompt = builder.build_prompt(
    query="Come trattare una ferita?",
    history=["Ciao", "Salve! Come posso aiutarti?"]
)
```

#### `add_to_history(query: str, response: str)`

Add a query-response pair to conversation history.

**Parameters:**
- `query` (str): User's question
- `response` (str): AI's response

#### `clear_history()`

Clear all conversation history.

#### `get_history() -> List[Dict[str, str]]`

Get the current conversation history.

**Returns:**
- `List[Dict[str, str]]`: History as list of query-response pairs

## System Prompts

### Default System Prompt

The default system prompt configures SIGMA-NEX for:
- **Medical Emergency Support**: Prioritizes life-saving information
- **Offline Operation**: Works without internet connectivity
- **Italian Language**: Primary language with multilingual support
- **Safety First**: Always emphasizes professional medical consultation

### Medical System Prompt

Enhanced prompt for medical queries:
- **Emergency Protocols**: Structured emergency response
- **Drug Information**: Medication interactions and contraindications
- **Symptom Assessment**: Systematic symptom evaluation
- **First Aid**: Step-by-step first aid procedures

### Security System Prompt

Security-focused prompt for sensitive operations:
- **Input Validation**: Enhanced input sanitization
- **Privacy Protection**: Data anonymization
- **Audit Requirements**: Detailed logging
- **Access Control**: Permission-based responses

## Context Management

### History Truncation

```python
# Automatic history management
max_history = config.get('max_history', 100)
if len(history) > max_history:
    # Keep recent history and system-critical exchanges
    history = truncate_intelligent(history, max_history)
```

### Context Compression

For long conversations, the context builder implements intelligent compression:
- **Summarization**: Old exchanges are summarized
- **Key Retention**: Important medical/safety info preserved
- **Progressive Compression**: Gradual detail reduction

### Memory Optimization

```python
# Memory-efficient context building
def build_efficient_context(query, history, max_tokens=4096):
    context = system_prompt
    
    # Add recent history first (LIFO)
    for exchange in reversed(history[-10:]):
        candidate = f"{context}\n{exchange}"
        if count_tokens(candidate) > max_tokens:
            break
        context = candidate
    
    # Always add current query
    return f"{context}\nUtente: {query}\nAI:"
```

## Prompt Templates

### Standard Template
```
Sistema: {system_prompt}

Cronologia:
{history}

Utente: {query}
AI:
```

### Medical Template
```
SISTEMA MEDICO SIGMA-NEX - MODALITÀ EMERGENZA

Protocollo: {emergency_level}
Situazione: {medical_context}
Cronologia: {medical_history}

QUERY MEDICA: {query}

RISPOSTA STRUTTURATA:
1. URGENZA:
2. AZIONI IMMEDIATE:
3. INFORMAZIONI CLINICHE:
4. RACCOMANDAZIONI:
```

### Security Template
```
MODALITÀ SICUREZZA ATTIVA
Livello di accesso: {security_level}
Audit ID: {audit_id}

Query validata: {sanitized_query}
Contesto autorizzato: {authorized_context}

Risposta:
```

## Configuration Options

```yaml
context:
  max_history: 100              # Maximum conversation length
  max_tokens: 4096             # Maximum context tokens
  compression_enabled: true    # Enable intelligent compression
  medical_mode: false          # Medical emergency mode
  security_mode: false         # Enhanced security mode
  
prompts:
  system_prompt: "custom/path/to/prompt.txt"
  medical_prompt: "custom/medical_prompt.txt"
  emergency_prompt: "custom/emergency_prompt.txt"
```

## Integration Examples

### With Retriever
```python
from sigma_nex.core.context import ContextBuilder
from sigma_nex.core.retriever import Retriever

context_builder = ContextBuilder(config)
retriever = Retriever(config)

# Enhance context with retrieved information
def build_enhanced_context(query, history):
    # Get relevant documents
    docs = retriever.retrieve(query, top_k=3)
    
    # Build base context
    context = context_builder.build_prompt(query, history)
    
    # Add retrieved information
    if docs:
        context += f"\n\nINFORMAZIONI RILEVANTI:\n{docs}"
    
    return context
```

### Medical Context Enhancement
```python
def build_medical_context(query, symptoms, patient_history):
    """Build specialized medical context."""
    medical_context = {
        'emergency_level': assess_emergency_level(symptoms),
        'medical_context': extract_medical_entities(query),
        'medical_history': format_medical_history(patient_history)
    }
    
    return context_builder.build_medical_prompt(query, medical_context)
```
