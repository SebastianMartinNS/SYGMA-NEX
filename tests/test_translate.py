import pytest

from sigma_nex.core import translate as tr


def test_is_translation_available_handles_missing_transformers(monkeypatch):
    # Force _check_transformers to False
    monkeypatch.setattr(tr, "_transformers_available", False)
    assert tr.is_translation_available() is False


def test_preload_models_noop_when_unavailable(monkeypatch, capsys):
    monkeypatch.setattr(tr, "_transformers_available", False)
    tr.preload_models()
    # should not crash


def test_translate_functions_fallback_when_unavailable(monkeypatch):
    monkeypatch.setattr(tr, "_transformers_available", False)
    text = "Ciao mondo"
    assert tr.translate_it_to_en(text) == text
    assert tr.translate_en_to_it(text) == text


def test_chunk_translate_fallback(monkeypatch):
    # Simulate tokenizer/model errors to exercise fallback branches
    class DummyTok:
        def __call__(self, text):
            raise Exception("tokenizer-error")

    class DummyModel:
        pass

    # Long enough to trigger chunking logic
    text = "A. " * 600
    out = tr._chunk_translate(text, DummyTok(), DummyModel(), max_tokens=10)
    assert isinstance(out, str)
    assert len(out) > 0
