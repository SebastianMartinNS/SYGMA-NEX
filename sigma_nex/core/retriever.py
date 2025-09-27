# sigma_nex/core/retriever.py
import json
import os
import time
from typing import List

# Lazy/optional imports to avoid heavy dependencies during import time
try:  # faiss is optional in CI; tests may mock it
    import faiss  # type: ignore
except Exception:  # pragma: no cover
    faiss = None  # type: ignore

try:  # sentence-transformers is large; allow absence in tests
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover
    SentenceTransformer = None  # type: ignore

# Percorsi file
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Framework_SIGMA.json")
INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "moduli.index")
MAPPING_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "moduli.mapping.json")
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "sigma_nex",
    "core",
    "models",
    "paraphrase-MiniLM-L6-v2",
)

# Global model cache (loaded lazily)
_model = None
# Backward-compat global used by tests to patch
model = None
# FAISS index cache
_cached_index = None
_cached_texts = None
_index_cache_time = 0.0
INDEX_CACHE_TTL = 3600  # 1 hour cache


def _get_model():
    """Return a sentence transformer model, loading it lazily.

    Falls back to a lightweight stub that returns zero vectors if the real
    dependency or local files are unavailable. This keeps unit tests decoupled
    from heavyweight downloads.
    """
    global _model
    if _model is not None:
        return _model

    if SentenceTransformer is None:

        class _Stub:
            def encode(self, texts, convert_to_numpy=True):
                import numpy as _np  # local import to avoid hard dependency

                # Return deterministic zero embeddings with small dim
                arr = _np.zeros((len(texts), 8), dtype=_np.float32)
                return arr

        _model = _Stub()
        print("[WARNING] Using stub embeddings model - semantic search disabled")
        print("[INFO] Install sentence-transformers for full functionality:")
        print("       pip install sentence-transformers")
        return _model

    try:
        _model = SentenceTransformer(MODEL_PATH)
        print("[INFO] Loaded local embedding model from cache")
        return _model
    except Exception:
        try:
            _model = SentenceTransformer("all-MiniLM-L6-v2")
            print("[INFO] Loaded default embedding model: all-MiniLM-L6-v2")
            return _model
        except Exception:
            # Fallback to stub if local model not present
            class _Stub:
                def encode(self, texts, convert_to_numpy=True):
                    import numpy as _np

                    return _np.zeros((len(texts), 8), dtype=_np.float32)

            _model = _Stub()
            print("[WARNING] Using stub embeddings model - semantic search disabled")
            print("[INFO] Install sentence-transformers for full functionality:")
            print("       pip install sentence-transformers")
            return _model


class Retriever:
    """Retriever class for semantic search using FAISS."""

    def __init__(self, index_path: str, model_name: str):
        """
        Initialize the retriever.

        Args:
            index_path: Path to the FAISS index file
            model_name: Name of the sentence transformer model
        """
        self.index_path = index_path
        self.model_name = model_name
        # Use global model if present (tests may patch it); otherwise lazy load
        self.model = model if model is not None else _get_model()

    def search(self, query: str, k: int = 3):
        """
        Search for relevant documents.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant documents
        """
        return search_moduli(query, k)


def get_moduli() -> List[dict]:
    """
    Carica e restituisce la lista dei moduli di sopravvivenza dal file JSON.
    """
    try:
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("modules", [])
    except Exception as e:
        print(f"[ERRORE RETRIEVER] Impossibile caricare i moduli: {e}")
        return []


def build_index():
    """
    Costruisce l'indice vettoriale FAISS a partire dai moduli presenti nel JSON
    e salva l'indice FAISS e la mappatura testuale.
    """
    moduli = get_moduli()
    if not moduli:
        print("[ERRORE] Nessun modulo disponibile nel framework.")
        return

    texts = [f"{mod['nome']} :: {mod['descrizione']}" for mod in moduli]
    # Prefer patched global model if available
    mdl = model if model is not None else _get_model()
    try:
        embeddings = mdl.encode(texts, convert_to_numpy=True)
    except Exception as e:
        print(f"[ERRORE] Impossibile generare embedding: {e}")
        return

    if faiss is None:
        print("[ERRORE] FAISS non disponibile.")
        return

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)

    with open(MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Indice FAISS costruito con {len(moduli)} moduli.")


def search_moduli(query: str, k: int = 3):
    """
    Esegue una ricerca semantica tra i moduli usando FAISS e restituisce
    le descrizioni più rilevanti dalla mappatura testuale.
    Utilizza cache per migliorare le performance.
    """
    global _cached_index, _cached_texts, _index_cache_time

    try:
        if faiss is None:
            raise RuntimeError("FAISS non disponibile")

        current_time = time.time()

        # Check if cache is valid
        if _cached_index is None or _cached_texts is None or current_time - _index_cache_time > INDEX_CACHE_TTL:

            # Load and cache index and texts
            _cached_index = faiss.read_index(INDEX_PATH)

            with open(MAPPING_PATH, encoding="utf-8") as f:
                _cached_texts = json.load(f)

            _index_cache_time = current_time
            print("[INFO] FAISS index cached for improved performance")

        if not _cached_texts:
            print("[ERRORE FAISS] Mappatura moduli vuota o malformata.")
            return []

        # Prefer patched global model if available
        mdl = model if model is not None else _get_model()
        query_vec = mdl.encode([query], convert_to_numpy=True)
        _D, indices = _cached_index.search(query_vec, k)

        return [_cached_texts[i] for i in indices[0]]

    except Exception as e:
        print(f"[ERRORE FAISS] Ricerca fallita: {e}")
        return []
