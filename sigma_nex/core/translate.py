"""
SIGMA-NEX Translation Module

Optimized translation with lazy loading and path management.
"""

import importlib
import re
import threading
from pathlib import Path
from typing import Dict, Optional, Tuple

# Lazy imports to improve startup time
MarianMTModel = None
MarianTokenizer = None
_transformers_available = None

# Expose get_config at module scope so tests can patch
try:
    # Local import to avoid heavy dependencies at import time
    from ..config import get_config as get_config  # type: ignore[no-redef]
except Exception:
    # In testing scenarios this will be patched
    get_config = None  # type: ignore


def _check_transformers():
    """Check if transformers is available and import if needed."""
    global MarianMTModel, MarianTokenizer, _transformers_available

    if _transformers_available is None:
        try:
            tfm = importlib.import_module("transformers")
            MarianMTModel = getattr(tfm, "MarianMTModel")
            MarianTokenizer = getattr(tfm, "MarianTokenizer")
            _transformers_available = True
        except Exception:
            _transformers_available = False
            print("[WARNING] transformers not available. Translation disabled.")

    return _transformers_available


def _get_model_paths():
    """Get model paths using centralized configuration."""
    cfg = get_config() if callable(get_config) else None  # type: ignore[misc]
    base_path: Path
    if cfg is not None:
        base_path = cfg.get_path("translate_models", "sigma_nex/core/models/translate")
    else:
        base_path = Path("sigma_nex/core/models/translate")

    return {"it-en": base_path / "it-en", "en-it": base_path / "en-it"}


# Thread-safe model cache
_lock = threading.Lock()
_models: Dict[str, Tuple] = {}


def _load_model(direction: str) -> Optional[Tuple]:
    """Load translation model with thread safety and error handling.

    Note: Always check the on-disk path before returning a cached model to
    make tests deterministic when paths are patched.
    """
    if not _check_transformers():
        return None

    # Always validate model path first (before cache) so patched paths are honored
    try:
        paths = _get_model_paths()
        model_path = paths.get(direction)
    except Exception:
        model_path = None

    if not model_path or not getattr(model_path, "exists", lambda: False)():
        print(f"[WARNING] Translation model not found at {model_path}")
        return None

    with _lock:
        if direction not in _models:
            try:
                print(f"Loading translation model: {direction}")
                assert MarianTokenizer is not None, "MarianTokenizer not available"
                assert MarianMTModel is not None, "MarianMTModel not available"
                tokenizer = MarianTokenizer.from_pretrained(str(model_path))
                model = MarianMTModel.from_pretrained(str(model_path))
                _models[direction] = (tokenizer, model)
                print(f"[SUCCESS] Translation model loaded: {direction}")
            except Exception as e:
                print(f"[ERROR] Loading translation model {direction}: {e}")
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
    sentences = re.split(r"(?<=[.!?]) +", text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        test_chunk = (current_chunk + " " + sentence).strip()
        try:
            if len(tokenizer(test_chunk)["input_ids"]) < max_tokens:
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
            print(f"[WARNING] Translation error for chunk: {e}")
            translated_chunks.append(chunk)  # Fallback to original

    return " ".join(translated_chunks)


def translate_it_to_en(text: str) -> str:
    """Translate Italian text to English."""
    if not text or not text.strip():
        return text

    model_data = _load_model("it-en")
    if not model_data:
        print("[WARNING] Italian to English translation unavailable")
        return text

    tokenizer, model = model_data

    try:
        # Check if text is short enough for direct translation
        if len(tokenizer(text)["input_ids"]) < 500:
            batch = tokenizer([text], return_tensors="pt", padding=True)
            gen = model.generate(**batch)
            return tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
        else:
            return _chunk_translate(text, tokenizer, model, 500)
    except Exception as e:
        print(f"[ERROR] Translation error (IT->EN): {e}")
        return text


def translate_en_to_it(text: str) -> str:
    """Translate English text to Italian."""
    if not text or not text.strip():
        return text

    model_data = _load_model("en-it")
    if not model_data:
        print("[WARNING] English to Italian translation unavailable")
        return text

    tokenizer, model = model_data

    try:
        if len(tokenizer(text)["input_ids"]) < 500:
            batch = tokenizer([text], return_tensors="pt", padding=True)
            gen = model.generate(**batch)
            return tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
        else:
            return _chunk_translate(text, tokenizer, model, 500)
    except Exception as e:
        print(f"[ERROR] Translation error (EN->IT): {e}")
        return text


def is_translation_available() -> bool:
    """Check if translation functionality is available."""
    return _check_transformers()


def preload_models() -> None:
    """Preload translation models for better performance."""
    if not _check_transformers():
        return

    print("Preloading translation models...")
    _load_model("it-en")
    _load_model("en-it")
    print("[SUCCESS] Translation models preloaded")
