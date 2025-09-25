"""
SIGMA-NEX Configuration and Path Management

Centralized path management and configuration for the SIGMA-NEX project.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class SigmaConfig:
    """Centralized configuration manager for SIGMA-NEX."""

    def __init__(self, config_path: Optional[str] = None):
        self.project_root = self._find_project_root()
        self.config_path = (
            Path(config_path) if config_path else (self.project_root / "config.yaml")
        )
        self._config = None
        self._framework = None

    def _find_project_root(self) -> Path:
        """Find the project root directory safely."""
        # Try walking up from CWD for a limited number of levels
        current = Path.cwd()
        for _ in range(10):
            if (current / "config.yaml").exists():
                return current
            if current == current.parent:
                break
            current = current.parent
        # Fallback to repository root (two levels up from this file)
        return Path(__file__).parent.parent.parent

    @property
    def config(self) -> Dict[str, Any]:
        """Get configuration, loading it if necessary."""
        if self._config is None:
            self._load_config()
        return self._config

    def _load_config(self) -> None:
        """Load configuration from YAML file with graceful fallbacks."""
        try:
            if not Path(self.config_path).exists():
                # Missing config file: fall back to empty config (defaults will apply)
                self._config = {}
                return

            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                self._config = data if isinstance(data, dict) else {}
        except Exception:
            # Invalid YAML or other IO issues: fall back to empty config
            print(f"⚠️ Warning: invalid or unreadable YAML at {self.config_path}")
            self._config = {}

    @property
    def framework(self) -> Dict[str, Any]:
        """Get framework data, loading it if necessary."""
        if self._framework is None:
            self._load_framework()
        return self._framework

    def _load_framework(self) -> None:
        """Load framework from JSON file."""
        framework_path = self.get_path("framework", "data/Framework_SIGMA.json")

        self._framework = {}
        try:
            if framework_path.exists():
                with open(framework_path, "r", encoding="utf-8") as f:
                    self._framework = json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Cannot load framework from {framework_path}: {e}")

    def get_path(self, path_type: str, default_relative: str = "") -> Path:
        """Get a path for a specific resource type."""
        paths = {
            "framework": self.project_root / "data" / "Framework_SIGMA.json",
            "models": self.project_root / "sigma_nex" / "core" / "models",
            "translate_models": self.project_root
            / "sigma_nex"
            / "core"
            / "models"
            / "translate",
            "data": self.project_root / "data",
            "logs": self.project_root / "logs",
            "temp": self.project_root / "temp",
        }

        if path_type in paths:
            return paths[path_type]

        # Custom path from config
        custom_path = self.config.get(f"{path_type}_path")
        if custom_path:
            path = Path(custom_path)
            return path if path.is_absolute() else self.project_root / path

        # Default fallback
        return self.project_root / default_relative

    # --- lightweight mutation helpers used by tests ---
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dotted keys, creating nested dicts."""
        cfg = self.config  # ensure loaded
        if not isinstance(key, str) or not key:
            return
        parts = key.split(".")
        cur = cfg
        for part in parts[:-1]:
            if part not in cur or not isinstance(cur[part], dict):
                cur[part] = {}
            cur = cur[part]
        cur[parts[-1]] = value

    def save(self) -> None:
        """Persist current configuration to disk, creating parent dirs."""
        try:
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(self.config, f, sort_keys=False, allow_unicode=True)
        except Exception as e:
            raise RuntimeError(f"Unable to save configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with dotted-key support and sensible defaults."""
        # Default values for common configuration keys
        defaults = {
            "debug": False,
            "model_name": "mistral",
            "temperature": 0.7,
            "max_history": 100,
            "max_tokens": 2048,
            "retrieval_enabled": True,
        }

        if default is None and key in defaults:
            default = defaults[key]

        cfg = self.config
        # Support dotted key access (e.g., "translation.enabled")
        if isinstance(key, str) and "." in key:
            parts = key.split(".")
            cur: Any = cfg
            for part in parts:
                if isinstance(cur, dict) and part in cur:
                    cur = cur[part]
                else:
                    return default
            return cur

        return cfg.get(key, default)


# Global configuration instance
_config_instance = None


def get_config(config_path: Optional[str] = None) -> SigmaConfig:
    """Get the global configuration instance.

    If a config_path is provided, (re)initialize the singleton with that path.
    """
    global _config_instance
    if _config_instance is None or config_path is not None:
        _config_instance = SigmaConfig(config_path=config_path)
    return _config_instance


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Legacy function for backward compatibility.
    """
    if config_path is None:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        config_path = os.path.join(root_dir, "config.yaml")

    if not os.path.exists(config_path):
        raise RuntimeError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    if "system_prompt" not in cfg:
        raise RuntimeError("Missing 'system_prompt' in config.yaml")

    # Load framework
    framework_path = cfg.get(
        "framework_path",
        os.path.join(os.path.dirname(config_path), "data", "Framework_SIGMA.json"),
    )
    framework = {}
    try:
        if os.path.exists(framework_path):
            with open(framework_path, "r", encoding="utf-8") as ff:
                framework = json.load(ff)
    except Exception as e:
        print(
            f"⚠️ Warning: Cannot load framework from {framework_path}: {e}", flush=True
        )

    cfg["framework"] = framework
    return cfg
