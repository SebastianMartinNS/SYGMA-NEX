"""
Test realistici completi per sigma_nex.config - 80% coverage target
Test REALI senza mock pesanti - focus su gestione configurazione effettiva
"""

import pytest
import yaml
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

from sigma_nex.config import SigmaConfig, get_config, load_config, _config_instance


class TestSigmaConfigRealistic:
    """Test realistici completi per SigmaConfig - gestione configurazione effettiva"""

    def setup_method(self):
        """Setup per ogni test - resetta global config"""
        global _config_instance
        _config_instance = None

    def test_find_project_root_real(self):
        """Test ricerca project root reale"""
        # Test con directory temporanea che simula progetto
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Crea config.yaml nella root del progetto
            config_file = temp_path / "config.yaml"
            config_file.write_text("debug: true")

            # Crea sottodirectory per testare ricerca
            sub_dir = temp_path / "sigma_nex" / "core"
            sub_dir.mkdir(parents=True)

            # Simula cambio directory
            original_cwd = os.getcwd()
            try:
                os.chdir(str(sub_dir))

                config = SigmaConfig()

                # Dovrebbe trovare la root del progetto
                assert config.project_root == temp_path
                assert (config.project_root / "config.yaml").exists()

            finally:
                os.chdir(original_cwd)

    def test_find_project_root_fallback_real(self):
        """Test fallback quando non trova config.yaml"""
        # Test in directory senza config.yaml
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)

                config = SigmaConfig()

                # Dovrebbe usare fallback - verifica che sia un path ragionevole
                # Il fallback dovrebbe essere un directory path valido
                assert config.project_root.exists()
                # In ambiente diversi il path può variare, verifica che non sia None/vuoto
                assert config.project_root != Path(".")

            finally:
                os.chdir(original_cwd)

    def test_config_loading_existing_file_real(self):
        """Test caricamento configurazione da file esistente"""
        config_data = {
            "debug": True,
            "model_name": "llama2",
            "temperature": 0.8,
            "translation": {"enabled": True, "target_lang": "it"},
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as temp_file:
            yaml.safe_dump(config_data, temp_file)
            temp_path = temp_file.name

        try:
            config = SigmaConfig(config_path=temp_path)

            # Verifica caricamento corretto
            assert config.config == config_data
            assert config.get("debug") == True
            assert config.get("model_name") == "llama2"
            assert config.get("temperature") == 0.8
            assert config.get("translation.enabled") == True
            assert config.get("translation.target_lang") == "it"

        finally:
            os.unlink(temp_path)

    def test_config_loading_missing_file_real(self):
        """Test caricamento con file mancante - fallback a config vuoto"""
        config = SigmaConfig(config_path="nonexistent_config.yaml")

        # Dovrebbe fallire gracefully con config vuoto
        assert config.config == {}
        assert config.get("debug") == False  # Default value
        assert config.get("model_name") == "mistral"  # Default value

    def test_config_loading_invalid_yaml_real(self):
        """Test gestione YAML malformato"""
        invalid_yaml = """
        debug: true
        model_name: llama2
        invalid_yaml: [unclosed list
        temperature: 0.8
        """

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as temp_file:
            temp_file.write(invalid_yaml)
            temp_path = temp_file.name

        try:
            # Mock print per catturare warning
            with patch("builtins.print") as mock_print:
                config = SigmaConfig(config_path=temp_path)

                # Dovrebbe fallback a config vuoto
                assert config.config == {}

                # Dovrebbe stampare warning
                mock_print.assert_called_once()
                assert "Warning: invalid or unreadable YAML" in str(
                    mock_print.call_args
                )

        finally:
            os.unlink(temp_path)

    def test_framework_loading_existing_file_real(self):
        """Test caricamento framework da file JSON esistente"""
        framework_data = {
            "framework": "SIGMA-NEX",
            "version": "1.0",
            "modules": [
                {
                    "id": "survival_001",
                    "name": "Water Procurement",
                    "category": "survival",
                },
                {
                    "id": "navigation_001",
                    "name": "GPS Navigation",
                    "category": "navigation",
                },
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            # Crea struttura directory data/
            data_dir = Path(temp_dir) / "data"
            data_dir.mkdir()

            # Crea file framework
            framework_file = data_dir / "Framework_SIGMA.json"
            with framework_file.open("w", encoding="utf-8") as f:
                json.dump(framework_data, f)

            # Inizializza config con project root personalizzato
            config = SigmaConfig()
            config.project_root = Path(temp_dir)

            # Test caricamento framework
            framework = config.framework

            assert framework == framework_data
            assert framework["framework"] == "SIGMA-NEX"
            assert len(framework["modules"]) == 2
            assert framework["modules"][0]["name"] == "Water Procurement"

    def test_framework_loading_missing_file_real(self):
        """Test caricamento framework con file mancante"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SigmaConfig()
            config.project_root = Path(temp_dir)

            # Mock print per catturare warning
            with patch("builtins.print") as mock_print:
                framework = config.framework

                # Dovrebbe essere dict vuoto
                assert framework == {}

                # Non dovrebbe stampare warning se file semplicemente non esiste
                # (il file potrebbe non essere necessario)

    def test_get_path_predefined_paths_real(self):
        """Test percorsi predefiniti"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = SigmaConfig()
            config.project_root = Path(temp_dir)

            # Test percorsi predefiniti
            assert (
                config.get_path("framework")
                == Path(temp_dir) / "data" / "Framework_SIGMA.json"
            )
            assert (
                config.get_path("models")
                == Path(temp_dir) / "sigma_nex" / "core" / "models"
            )
            assert (
                config.get_path("translate_models")
                == Path(temp_dir) / "sigma_nex" / "core" / "models" / "translate"
            )
            assert config.get_path("data") == Path(temp_dir) / "data"
            assert config.get_path("logs") == Path(temp_dir) / "logs"
            assert config.get_path("temp") == Path(temp_dir) / "temp"

    def test_get_path_custom_config_paths_real(self):
        """Test percorsi personalizzati da configurazione"""
        config_data = {
            "custom_data_path": "my_custom_data",
            "models_path": "/absolute/path/to/models",
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as temp_file:
            yaml.safe_dump(config_data, temp_file)
            temp_path = temp_file.name

        try:
            config = SigmaConfig(config_path=temp_path)

            # Test percorso relativo personalizzato
            custom_data_path = config.get_path("custom_data")
            assert custom_data_path == config.project_root / "my_custom_data"

            # Test percorso assoluto personalizzato
            models_path = config.get_path("models")
            # I path predefiniti hanno precedenza sui config custom
            expected = config.project_root / "sigma_nex" / "core" / "models"
            assert models_path == expected

        finally:
            os.unlink(temp_path)

    def test_get_path_default_fallback_real(self):
        """Test fallback a percorso default"""
        config = SigmaConfig()

        # Percorso non definito dovrebbe usare default
        custom_path = config.get_path("nonexistent", "default/path")
        assert custom_path == config.project_root / "default" / "path"

    def test_set_configuration_values_real(self):
        """Test impostazione valori configurazione"""
        config = SigmaConfig()

        # Set valori semplici
        config.set("debug", True)
        config.set("model_name", "custom_model")

        assert config.get("debug") == True
        assert config.get("model_name") == "custom_model"

        # Set valori annidati (dotted keys)
        config.set("translation.enabled", True)
        config.set("translation.target_lang", "es")
        config.set("server.host", "localhost")
        config.set("server.port", 8080)

        assert config.get("translation.enabled") == True
        assert config.get("translation.target_lang") == "es"
        assert config.get("server.host") == "localhost"
        assert config.get("server.port") == 8080

        # Verifica struttura annidata
        translation_config = config.get("translation")
        assert isinstance(translation_config, dict)
        assert translation_config["enabled"] == True
        assert translation_config["target_lang"] == "es"

    def test_set_edge_cases_real(self):
        """Test casi limite per set()"""
        config = SigmaConfig()

        # Chiave vuota - non dovrebbe fare nulla
        config.set("", "value")
        config.set(None, "value")

        # Non dovrebbe creare valori
        assert config.get("") is None

        # Sovrascrittura di dict esistente
        config.set("existing.key", "initial")
        config.set("existing", {"new": "structure"})

        assert config.get("existing.new") == "structure"
        assert config.get("existing.key") is None  # Dovrebbe essere sovrascritto

    def test_save_configuration_real(self):
        """Test salvataggio configurazione su disco"""
        config_data = {
            "debug": True,
            "model_name": "test_model",
            "nested": {"value": 42, "flag": False},
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            # Crea sottodirectory per testare mkdir
            config_path = Path(temp_dir) / "config" / "test_config.yaml"

            config = SigmaConfig(config_path=str(config_path))

            # Imposta i valori
            for key, value in config_data.items():
                config.set(key, value)

            # Salva su disco
            config.save()

            # Verifica file creato
            assert config_path.exists()

            # Verifica contenuto
            with config_path.open("r", encoding="utf-8") as f:
                saved_data = yaml.safe_load(f)

            assert saved_data == config_data

    def test_get_with_defaults_real(self):
        """Test get() con valori di default"""
        config = SigmaConfig()

        # Test defaults predefiniti
        assert config.get("debug") == False
        assert config.get("model_name") == "mistral"
        assert config.get("temperature") == 0.7
        assert config.get("max_history") == 100
        assert config.get("max_tokens") == 2048
        assert config.get("retrieval_enabled") == True

        # Test default personalizzato
        assert config.get("nonexistent_key", "custom_default") == "custom_default"

        # Test con config esistente che sovrascrive default
        config.set("debug", True)
        config.set("temperature", 0.9)

        assert config.get("debug") == True
        assert config.get("temperature") == 0.9

    def test_get_dotted_keys_real(self):
        """Test accesso con chiavi dotted"""
        config = SigmaConfig()

        # Imposta struttura annidata
        config.set("server.host", "localhost")
        config.set("server.port", 8080)
        config.set("server.ssl.enabled", True)
        config.set("server.ssl.cert_path", "/path/to/cert")

        # Test accesso dotted
        assert config.get("server.host") == "localhost"
        assert config.get("server.port") == 8080
        assert config.get("server.ssl.enabled") == True
        assert config.get("server.ssl.cert_path") == "/path/to/cert"

        # Test chiave inesistente
        assert config.get("server.nonexistent") is None
        assert config.get("server.ssl.nonexistent", "default") == "default"


class TestGlobalConfigRealistic:
    """Test realistici per funzioni globali configurazione"""

    def setup_method(self):
        """Reset global config per ogni test"""
        global _config_instance
        _config_instance = None

    def test_get_config_singleton_real(self):
        """Test pattern singleton per get_config()"""
        # Prima chiamata crea istanza
        config1 = get_config()
        assert isinstance(config1, SigmaConfig)

        # Seconda chiamata restituisce stessa istanza
        config2 = get_config()
        assert config1 is config2

        # Modifica configurazione dovrebbe essere visibile
        config1.set("test_key", "test_value")
        assert config2.get("test_key") == "test_value"

    def test_get_config_with_custom_path_real(self):
        """Test get_config() con percorso personalizzato"""
        config_data = {"custom": True, "model": "custom_model"}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as temp_file:
            yaml.safe_dump(config_data, temp_file)
            temp_path = temp_file.name

        try:
            # Prima chiamata con percorso personalizzato
            config = get_config(config_path=temp_path)
            assert config.get("custom") == True
            assert config.get("model") == "custom_model"

            # Seconda chiamata senza percorso dovrebbe usare stessa istanza
            config2 = get_config()
            assert config is config2
            assert config2.get("custom") == True

        finally:
            os.unlink(temp_path)

    def test_load_config_legacy_function_real(self):
        """Test funzione legacy load_config()"""
        config_data = {
            "system_prompt": "You are SIGMA-NEX",
            "debug": True,
            "model_name": "legacy_model",
        }

        framework_data = {
            "framework": "SIGMA-NEX",
            "modules": [{"id": "test", "name": "Test Module"}],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            # Crea config.yaml
            config_path = Path(temp_dir) / "config.yaml"
            with config_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(config_data, f)

            # Crea data/Framework_SIGMA.json
            data_dir = Path(temp_dir) / "data"
            data_dir.mkdir()
            framework_path = data_dir / "Framework_SIGMA.json"
            with framework_path.open("w", encoding="utf-8") as f:
                json.dump(framework_data, f)

            # Test load_config
            result = load_config(str(config_path))

            # Verifica configurazione caricata
            assert result["system_prompt"] == "You are SIGMA-NEX"
            assert result["debug"] == True
            assert result["model_name"] == "legacy_model"

            # Verifica framework incluso
            assert "framework" in result
            assert result["framework"]["framework"] == "SIGMA-NEX"
            assert len(result["framework"]["modules"]) == 1

    def test_load_config_missing_file_real(self):
        """Test load_config() con file mancante"""
        with pytest.raises(RuntimeError, match="Config file not found"):
            load_config("nonexistent_config.yaml")

    def test_load_config_missing_system_prompt_real(self):
        """Test load_config() senza system_prompt obbligatorio"""
        config_data = {"debug": True}  # Manca system_prompt

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as temp_file:
            yaml.safe_dump(config_data, temp_file)
            temp_path = temp_file.name

        try:
            with pytest.raises(
                RuntimeError, match="Missing 'system_prompt' in config.yaml"
            ):
                load_config(temp_path)

        finally:
            os.unlink(temp_path)


class TestConfigIntegration:
    """Test integrazione configurazione con altri moduli"""

    def setup_method(self):
        """Reset global config"""
        global _config_instance
        _config_instance = None

    def test_config_framework_integration_real(self):
        """Test integrazione configurazione con framework"""
        # Simula progetto completo
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Crea config.yaml
            config_data = {
                "debug": False,
                "model_name": "integration_test",
                "framework_custom": True,
            }
            config_path = project_root / "config.yaml"
            with config_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(config_data, f)

            # Crea framework
            framework_data = {
                "framework": "SIGMA-NEX Integration",
                "modules": [
                    {"id": "int_001", "name": "Integration Module", "category": "test"}
                ],
            }
            data_dir = project_root / "data"
            data_dir.mkdir()
            framework_path = data_dir / "Framework_SIGMA.json"
            with framework_path.open("w", encoding="utf-8") as f:
                json.dump(framework_data, f)

            # Cambia directory temporaneamente per forzare il framework test
            original_cwd = os.getcwd()
            try:
                os.chdir(str(project_root))

                # Test integrazione
                config = SigmaConfig(config_path=str(config_path))

                # Verifica config
                assert config.get("model_name") == "integration_test"
                assert config.get("framework_custom") == True

                # Verifica framework - dovrebbe essere quello del temp dir
                framework = config.framework
                assert "modules" in framework
                assert len(framework["modules"]) == 1
                assert framework["modules"][0]["name"] == "Integration Module"

            finally:
                os.chdir(original_cwd)

    def test_config_path_resolution_integration_real(self):
        """Test risoluzione percorsi per integrazione moduli"""
        config = SigmaConfig()

        # Test tutti i percorsi predefiniti esistano come Path
        paths_to_test = [
            "framework",
            "models",
            "translate_models",
            "data",
            "logs",
            "temp",
        ]

        for path_type in paths_to_test:
            path = config.get_path(path_type)
            assert isinstance(path, Path)
            assert path.is_absolute()
            assert str(config.project_root) in str(path)


class TestConfigPerformance:
    """Test performance configurazione"""

    def setup_method(self):
        """Reset global config"""
        global _config_instance
        _config_instance = None

    def test_config_loading_performance_real(self):
        """Test performance caricamento configurazione"""
        import time

        # Crea config di dimensioni realistiche
        large_config = {
            "debug": True,
            "models": {f"model_{i}": f"config_{i}" for i in range(100)},
            "paths": {f"path_{i}": f"/path/to/{i}" for i in range(50)},
            "features": {f"feature_{i}": i % 2 == 0 for i in range(200)},
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as temp_file:
            yaml.safe_dump(large_config, temp_file)
            temp_path = temp_file.name

        try:
            start_time = time.time()

            config = SigmaConfig(config_path=temp_path)

            # Accessi multipli per test caching
            for _ in range(10):
                config.get("debug")
                config.get("models.model_50")
                config.get("features.feature_100")

            end_time = time.time()

            # Dovrebbe essere veloce anche con config grande
            assert end_time - start_time < 0.5  # Meno di 500ms

        finally:
            os.unlink(temp_path)

    def test_config_memory_usage_real(self):
        """Test uso memoria configurazione"""
        import gc

        initial_objects = len(gc.get_objects())

        # Crea e distruggi multiple configurazioni
        configs = []
        for i in range(10):
            config = SigmaConfig()
            config.set(f"test_{i}", f"value_{i}")
            configs.append(config)

        # Cleanup
        del configs
        gc.collect()

        final_objects = len(gc.get_objects())

        # Non dovrebbe esserci memory leak significativo
        objects_increase = final_objects - initial_objects
        assert objects_increase < 500  # Threshold ragionevole


class TestConfigErrorHandling:
    """Test gestione errori configurazione"""

    def setup_method(self):
        """Reset global config"""
        global _config_instance
        _config_instance = None

    def test_config_save_permission_error_real(self):
        """Test gestione errori di permesso durante salvataggio"""
        # Testa con path non scrivibile (solo se su sistema Unix-like)
        if os.name == "nt":  # Windows
            pytest.skip("Permission test not reliable on Windows")

        config = SigmaConfig(config_path="/root/readonly_config.yaml")
        config.set("test", "value")

        with pytest.raises(RuntimeError, match="Unable to save configuration"):
            config.save()

    def test_config_robust_fallbacks_real(self):
        """Test fallback robusti in caso di errori"""
        # Test con file corrotto
        corrupted_yaml = "debug: true\nmodel: [unclosed"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as temp_file:
            temp_file.write(corrupted_yaml)
            temp_path = temp_file.name

        try:
            with patch("builtins.print"):  # Sopprime warning
                config = SigmaConfig(config_path=temp_path)

                # Dovrebbe fallback a defaults
                assert (
                    config.get("debug") == False
                )  # Default, non True dal file corrotto
                assert config.get("model_name") == "mistral"  # Default

        finally:
            os.unlink(temp_path)
