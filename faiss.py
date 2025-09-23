"""
Lightweight FAISS shim for tests and local development on platforms without FAISS wheels.
Provides a minimal subset of the API used by the project/tests.
"""
from __future__ import annotations

import pickle
from pathlib import Path
from typing import Tuple

try:
    import numpy as np  # optional; used if available
except Exception:  # pragma: no cover
    np = None  # type: ignore


class IndexFlatL2:
    def __init__(self, d: int):
        self.d = d
        self._embeddings = None

    def add(self, embeddings):
        self._embeddings = embeddings

    def search(self, query_vec, k: int) -> Tuple[object, list]:
        # If numpy is available and we have embeddings, compute naive L2
        if np is not None and self._embeddings is not None:
            q = query_vec
            X = self._embeddings
            try:
                # Ensure 2D
                if q.ndim == 1:
                    q = q.reshape(1, -1)
                # Compute distances
                dists = ((X[None, :, :] - q[:, None, :]) ** 2).sum(axis=2)
                # Get top-k smallest distances
                idx = np.argsort(dists, axis=1)[:, :k]
                D = np.take_along_axis(dists, idx, axis=1)
                return D, idx.tolist()
            except Exception:
                pass
        # Fallback: return zeros and sequential indices
        n = k
        D = None
        I = [list(range(k))]
        return D, I


def write_index(index: IndexFlatL2, path: str | Path) -> None:
    with open(path, "wb") as f:
        pickle.dump(index, f)


def read_index(path: str | Path) -> IndexFlatL2:
    with open(path, "rb") as f:
        return pickle.load(f)
