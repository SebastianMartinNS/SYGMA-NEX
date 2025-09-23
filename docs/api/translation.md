# Translation API Reference

## Overview

The Translation module provides multilingual support for SIGMA-NEX using MarianMT models for high-quality offline translation.

## Class: Translator

```python
from sigma_nex.core.translate import Translator

translator = Translator(config)
```

### Methods

#### `translate(text: str, target_lang: str = 'it', source_lang: str = 'auto') -> str`

Translate text between languages.

**Parameters:**
- `text` (str): Text to translate
- `target_lang` (str): Target language code (default: 'it')
- `source_lang` (str): Source language code (default: 'auto')

**Returns:**
- `str`: Translated text

**Example:**
```python
translator = Translator(config)
italian_text = translator.translate("How to treat a wound?", target_lang='it')
print(italian_text)  # "Come trattare una ferita?"
```

#### `detect_language(text: str) -> str`

Detect the language of input text.

**Parameters:**
- `text` (str): Text to analyze

**Returns:**
- `str`: Detected language code

#### `is_translation_needed(text: str, target_lang: str = 'it') -> bool`

Check if translation is needed for the given text.

**Parameters:**
- `text` (str): Input text
- `target_lang` (str): Target language

**Returns:**
- `bool`: True if translation is needed

#### `get_supported_languages() -> List[str]`

Get list of supported language codes.

**Returns:**
- `List[str]`: List of supported language codes

## Supported Languages

### Language Codes

```python
SUPPORTED_LANGUAGES = {
    'it': 'Italian',      # Primary language
    'en': 'English',      # International
    'es': 'Spanish',      # Medical literature
    'fr': 'French',       # Medical terminology
    'de': 'German',       # Scientific papers
    'pt': 'Portuguese',   # Medical research
    'ru': 'Russian',      # Emergency situations
    'ar': 'Arabic',       # Middle East support
    'zh': 'Chinese',      # Asian languages
    'ja': 'Japanese'      # Technical documentation
}
```

### Medical Language Support

Special handling for medical terminology:
- **Preserves medical terms**: Drug names, symptoms, procedures
- **Context-aware translation**: Medical vs. general context
- **Terminology consistency**: Standardized medical vocabulary
- **Dosage preservation**: Maintains medication dosages and units

## MarianMT Models

### Model Architecture

SIGMA-NEX uses Facebook's MarianMT models:
- **Opus-MT**: High-quality translation models
- **Medical-tuned**: Specialized for medical content
- **Offline capable**: No internet required
- **Fast inference**: Optimized for real-time translation

### Model Loading

```python
from transformers import MarianMTModel, MarianTokenizer

def load_translation_model(source_lang: str, target_lang: str):
    """Load MarianMT model for language pair."""
    model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return model, tokenizer
    except OSError:
        # Fallback to multilingual model
        return load_multilingual_model()
```

### Model Caching

```python
from functools import lru_cache

@lru_cache(maxsize=10)
def get_cached_model(source_lang: str, target_lang: str):
    """Cache frequently used translation models."""
    return load_translation_model(source_lang, target_lang)
```

## Translation Pipeline

### Text Preprocessing

```python
def preprocess_for_translation(text: str) -> str:
    """Prepare text for optimal translation."""
    # Preserve medical terms and measurements
    text = preserve_medical_entities(text)
    
    # Normalize punctuation
    text = normalize_punctuation(text)
    
    # Handle special characters
    text = handle_special_chars(text)
    
    return text
```

### Medical Entity Preservation

```python
def preserve_medical_entities(text: str) -> str:
    """Preserve medical terms during translation."""
    medical_patterns = [
        r'\d+(?:\.\d+)?\s*(?:mg|ml|g|kg|l)',  # Dosages
        r'[A-Z][a-z]+(?:-[A-Z][a-z]+)*',      # Drug names
        r'COVID-19|SARS-CoV-2|HIV|AIDS',      # Diseases
        r'\b(?:ICD|CPT|SNOMED)\b\d+',         # Medical codes
    ]
    
    preserved = {}
    for i, pattern in enumerate(medical_patterns):
        matches = re.findall(pattern, text)
        for match in matches:
            placeholder = f"__MEDICAL_ENTITY_{i}_{len(preserved)}__"
            preserved[placeholder] = match
            text = text.replace(match, placeholder, 1)
    
    return text, preserved
```

### Post-processing

```python
def postprocess_translation(text: str, preserved_entities: dict) -> str:
    """Restore preserved entities after translation."""
    for placeholder, original in preserved_entities.items():
        text = text.replace(placeholder, original)
    
    # Fix common translation artifacts
    text = fix_medical_terminology(text)
    text = fix_punctuation_spacing(text)
    
    return text
```

## Language Detection

### Automatic Detection

```python
from langdetect import detect, LangDetectException

def detect_language_robust(text: str) -> str:
    """Robust language detection with fallbacks."""
    try:
        # Primary detection
        detected = detect(text)
        
        # Validate against supported languages
        if detected in SUPPORTED_LANGUAGES:
            return detected
        
        # Fallback to character-based detection
        return detect_by_character_distribution(text)
        
    except LangDetectException:
        # Medical text heuristics
        return detect_medical_language(text)
```

### Medical Text Detection

```python
def detect_medical_language(text: str) -> str:
    """Detect language for medical texts."""
    medical_keywords = {
        'it': ['dolore', 'ferita', 'medicina', 'sintomo'],
        'en': ['pain', 'wound', 'medicine', 'symptom'],
        'es': ['dolor', 'herida', 'medicina', 'síntoma'],
        'fr': ['douleur', 'blessure', 'médecine', 'symptôme']
    }
    
    scores = {}
    for lang, keywords in medical_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text.lower())
        scores[lang] = score
    
    return max(scores, key=scores.get) if scores else 'en'
```

## Configuration

```yaml
translation:
  enabled: true                    # Enable translation
  default_source: "auto"          # Auto-detect source language
  default_target: "it"            # Default target language
  preserve_medical: true          # Preserve medical entities
  cache_models: true              # Cache translation models
  
models:
  base_model: "Helsinki-NLP/opus-mt"
  medical_model: "clinical-marian-mt"
  cache_size: 10                  # Number of cached models
  device: "cpu"                   # cpu or cuda
  
quality:
  min_confidence: 0.8             # Minimum translation confidence
  fallback_enabled: true          # Enable fallback translation
  review_threshold: 0.9           # Human review threshold
```

## Quality Assurance

### Translation Confidence

```python
def calculate_confidence(source: str, translation: str, model) -> float:
    """Calculate translation confidence score."""
    # Back-translation check
    back_translation = reverse_translate(translation, model)
    similarity = calculate_similarity(source, back_translation)
    
    # Model confidence
    model_confidence = get_model_confidence(model, source, translation)
    
    # Medical term preservation check
    medical_preservation = check_medical_preservation(source, translation)
    
    return (similarity * 0.4 + model_confidence * 0.4 + medical_preservation * 0.2)
```

### Medical Accuracy Validation

```python
def validate_medical_translation(source: str, translation: str) -> bool:
    """Validate medical translation accuracy."""
    # Check critical medical terms
    critical_terms = extract_critical_medical_terms(source)
    preserved_terms = check_term_preservation(critical_terms, translation)
    
    # Validate dosages and measurements
    dosages_valid = validate_dosage_translation(source, translation)
    
    # Check contraindication preservation
    contraindications_valid = validate_contraindications(source, translation)
    
    return all([preserved_terms, dosages_valid, contraindications_valid])
```

## Integration Examples

### Real-time Translation

```python
async def translate_realtime(text: str, target_lang: str = 'it') -> str:
    """Asynchronous real-time translation."""
    # Quick language detection
    source_lang = detect_language(text)
    
    if source_lang == target_lang:
        return text
    
    # Translate with caching
    cache_key = f"{source_lang}:{target_lang}:{hash(text)}"
    cached_result = translation_cache.get(cache_key)
    
    if cached_result:
        return cached_result
    
    # Perform translation
    result = await asyncio.to_thread(
        translator.translate, 
        text, 
        target_lang, 
        source_lang
    )
    
    # Cache result
    translation_cache[cache_key] = result
    return result
```

### Medical Emergency Translation

```python
def emergency_translate(text: str, target_lang: str = 'it') -> str:
    """Priority translation for medical emergencies."""
    # Fast-track detection for emergency keywords
    emergency_keywords = ['emergency', 'urgente', 'pain', 'bleeding']
    is_emergency = any(keyword in text.lower() for keyword in emergency_keywords)
    
    if is_emergency:
        # Use fast, cached models
        return fast_translate(text, target_lang)
    
    # Regular translation pipeline
    return translator.translate(text, target_lang)
```

### Multi-language Support

```python
def multilingual_response(query: str, user_lang: str = 'auto') -> dict:
    """Generate response in multiple languages."""
    # Detect query language
    if user_lang == 'auto':
        user_lang = translator.detect_language(query)
    
    # Generate response in Italian (primary)
    italian_response = runner.process_query(
        translator.translate(query, 'it')
    )
    
    # Translate response to user's language
    user_response = translator.translate(italian_response, user_lang)
    
    return {
        'query_language': user_lang,
        'response': user_response,
        'original_response': italian_response
    }
```