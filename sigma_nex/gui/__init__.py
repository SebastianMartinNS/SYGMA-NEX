"""
SIGMA-NEX GUI package.

This package intentionally avoids importing the heavy GUI module at import time.
"""

def main() -> None:
    """Lazy entry point for SIGMA-NEX GUI."""
    print("Starting SIGMA-NEX GUI...")
    from . import main_gui as _mg  # lazy import to allow tests to patch
    _mg.main()


__all__ = ["main"]


if __name__ == "__main__":
    main()