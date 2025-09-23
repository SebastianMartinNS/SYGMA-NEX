"""
SIGMA-NEX Translation Module

Optimized translation with lazy loading and path management.
"""

import threading
import re
from typing import Dict, Tuple, Optional
from pathlib import Path

# Lazy imports to improve startup time
MarianMTModel = None
MarianTokenizer = None
_transformers_available = None


def _check_transformers():
    """Check if transformers is available and import if needed."""
    global MarianMTModel, MarianTokenizer, _transformers_available
    
    if _transformers_available is None:
        try:
            from transformers import MarianMTModel as _MarianMTModel
            from transformers import MarianTokenizer as _MarianTokenizer
            MarianMTModel = _MarianMTModel
            MarianTokenizer = _MarianTokenizer
            _transformers_available = True
        except ImportError:
            _transformers_available = False
            print("⚠️ Warning: transformers not available. Translation disabled.")
    
    return _transformers_available


def _get_model_paths():
    """Get model paths using centralized configuration."""
    from ..config import get_config
    config = get_config()
    
    base_path = config.get_path('translate_models', 'sigma_nex/core/models/translate')
    return {
        'it-en': base_path / "it-en",
        'en-it': base_path / "en-it"
    }


# Thread-safe model cache
_lock = threading.Lock()
_models: Dict[str, Tuple] = {}


def _load_model(direction: str) -> Optional[Tuple]:
    """Load translation model with thread safety and error handling."""
    if not _check_transformers():
        return None
    
    with _lock:
        if direction not in _models:
            try:
                paths = _get_model_paths()
                model_path = paths.get(direction)
                
                if not model_path or not model_path.exists():
                    print(f"⚠️ Warning: Translation model not found at {model_path}")
                    return None
                
                print(f"🔄 Loading translation model: {direction}")
                tokenizer = MarianTokenizer.from_pretrained(str(model_path))
                model = MarianMTModel.from_pretrained(str(model_path))
                _models[direction] = (tokenizer, model)
                print(f"✅ Translation model loaded: {direction}")
                
            except Exception as e:
                print(f"❌ Error loading translation model {direction}: {e}")
                return None
                
    return _models.get(direction)


def _chunk_translate(text: str, tokenizer, model, max_tokens: int = 500) -> str:
    """
    Split text into chunks and translate each chunk separately.
    
    Args:
        text: Text to translate
        tokenizer: Tokenizer instance
        model: Model instance
        max_tokens: Maximum tokens per chunk
        
    Returns:
        Translated text
    """
    # Split into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        test_chunk = (current_chunk + " " + sentence).strip()
        try:
            if len(tokenizer(test_chunk)['input_ids']) < max_tokens:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        except Exception:
            # Fallback to character-based chunking
            if len(current_chunk) + len(sentence) < max_tokens * 4:  # Rough estimate
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())

    # Translate chunks
    translated_chunks = []
    for chunk in chunks:
        try:
            batch = tokenizer([chunk], return_tensors="pt", padding=True)
            gen = model.generate(**batch)
            result = tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
            translated_chunks.append(result)
        except Exception as e:
            print(f"⚠️ Translation error for chunk: {e}")
            translated_chunks.append(chunk)  # Fallback to original
    
    return " ".join(translated_chunks)


def translate_it_to_en(text: str) -> str:
    """Translate Italian text to English."""
    if not text or not text.strip():
        return text
    
    model_data = _load_model('it-en')
    if not model_data:
        print("⚠️ Italian to English translation unavailable")
        return text
    
    tokenizer, model = model_data
    
    try:
        # Check if text is short enough for direct translation
        if len(tokenizer(text)['input_ids']) < 500:
            batch = tokenizer([text], return_tensors="pt", padding=True)
            gen = model.generate(**batch)
            return tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
        else:
            return _chunk_translate(text, tokenizer, model, 500)
    except Exception as e:
        print(f"❌ Translation error (IT->EN): {e}")
        return text


def translate_en_to_it(text: str) -> str:
    """Translate English text to Italian."""
    if not text or not text.strip():
        return text
    
    model_data = _load_model('en-it')
    if not model_data:
        print("⚠️ English to Italian translation unavailable")
        return text
    
    tokenizer, model = model_data
    
    try:
        if len(tokenizer(text)['input_ids']) < 500:
            batch = tokenizer([text], return_tensors="pt", padding=True)
            gen = model.generate(**batch)
            return tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
        else:
            return _chunk_translate(text, tokenizer, model, 500)
    except Exception as e:
        print(f"❌ Translation error (EN->IT): {e}")
        return text


def is_translation_available() -> bool:
    """Check if translation functionality is available."""
    return _check_transformers()


def preload_models() -> None:
    """Preload translation models for better performance."""
    if not _check_transformers():
        return
    
    print("🔄 Preloading translation models...")
    _load_model('it-en')
    _load_model('en-it')
    print("✅ Translation models preloaded")
