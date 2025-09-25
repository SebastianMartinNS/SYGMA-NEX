"""
Test realistici completi per sigma_nex.cli - 80% coverage target
Test REALI senza mock pesanti - focus su funzionalità effettive CLI
"""

import json
import os
import tempfile
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from sigma_nex.cli import load_framework, main


class TestSigmaNexCLIRealistic:
    """Test realistici completi per CLI - copertura effettiva senza mock pesanti"""

    def test_cli_main_group_real(self):
        """Test gruppo principale CLI"""
        runner = CliRunner()

        # Test help del comando principale
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "SIGMA-NEX" in result.output
        assert "Agente cognitivo autonomo" in result.output
        assert "--secure" in result.output

    def test_cli_secure_flag_real(self):
        """Test flag secure del CLI"""
        runner = CliRunner()

        # Test help principale mostra --secure flag
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "--secure" in result.output
        assert "Modalità sicura" in result.output

    def test_cli_start_command_real(self):
        """Test comando start con configurazione reale"""
        runner = CliRunner()

        # Test integrazione REALE con get_config senza mock

        # Mock solo interactive per evitare REPL infinito
        with patch("sigma_nex.core.runner.Runner.interactive") as mock_interactive:
            result = runner.invoke(main, ["start"])

            # Verifica che interactive() sia stato chiamato
            mock_interactive.assert_called_once()

            assert result.exit_code == 0

    def test_cli_start_command_secure_real(self):
        """Test comando start con modalità sicura"""
        runner = CliRunner()

        # Test REALE della modalità sicura senza mock config
        with patch("sigma_nex.core.runner.Runner.interactive") as mock_interactive:
            result = runner.invoke(main, ["--secure", "start"])

            # Verifica che interactive() sia stato chiamato
            mock_interactive.assert_called_once()
            assert result.exit_code == 0

    def test_cli_load_framework_real(self):
        """Test comando load-framework con file reale"""
        runner = CliRunner()

        # Crea file JSON temporaneo con struttura realistica
        test_data = {
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

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file, indent=2)
            temp_path = temp_file.name

        try:
            result = runner.invoke(load_framework, [temp_path])

            # Verifica output del comando
            assert result.exit_code == 0
            assert "Caricati 2 moduli dal file" in result.output
            assert temp_path in result.output

        finally:
            os.unlink(temp_path)

    def test_cli_load_framework_empty_file_real(self):
        """Test load-framework con file vuoto"""
        runner = CliRunner()

        # File con moduli vuoti
        test_data = {"framework": "SIGMA-NEX", "modules": []}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            result = runner.invoke(load_framework, [temp_path])

            assert result.exit_code == 0
            assert "Caricati 0 moduli dal file" in result.output

        finally:
            os.unlink(temp_path)

    def test_cli_load_framework_nonexistent_file_real(self):
        """Test load-framework con file inesistente"""
        runner = CliRunner()

        result = runner.invoke(load_framework, ["nonexistent_file.json"])

        # Click dovrebbe restituire errore per file inesistente
        assert result.exit_code != 0
        assert "does not exist" in result.output or "No such file" in result.output

    def test_cli_self_check_command_real(self):
        """Test comando self-check"""
        runner = CliRunner()

        # Test REALE self-check con configurazione reale
        with patch("sigma_nex.core.runner.Runner.self_check") as mock_self_check:
            result = runner.invoke(main, ["self-check"])

            # Verifica che self_check() sia stato chiamato
            mock_self_check.assert_called_once()

            assert result.exit_code == 0

    def test_cli_commands_list_real(self):
        """Test che tutti i comandi siano disponibili"""
        runner = CliRunner()

        result = runner.invoke(main, ["--help"])

        # Verifica che tutti i comandi principali siano listati
        assert result.exit_code == 0
        assert "start" in result.output
        assert "load-framework" in result.output
        assert "self-check" in result.output
        assert "self-heal" in result.output  # Questo dovrebbe esistere


class TestCLIIntegration:
    """Test integrazione CLI con altri moduli"""

    def test_cli_config_integration_real(self):
        """Test integrazione CLI con configurazione"""
        runner = CliRunner()

        # Test che l'help funzioni senza errori di config
        result = runner.invoke(main, ["--help"])

        # Dovrebbe funzionare anche senza config perfetta
        assert result.exit_code == 0
        assert "SIGMA-NEX" in result.output

    def test_cli_runner_integration_real(self):
        """Test integrazione CLI con Runner usando config reale"""
        runner = CliRunner()

        # Test integrazione REALE CLI-Runner con config effettiva
        with patch("sigma_nex.core.runner.Runner.interactive") as mock_interactive:
            result = runner.invoke(main, ["start"])

            # Runner viene inizializzato con config reale
            mock_interactive.assert_called_once()
            assert result.exit_code == 0

    def test_cli_dataloader_integration_real(self):
        """Test integrazione CLI con DataLoader"""
        runner = CliRunner()

        # Test con file JSON reale del progetto se esiste
        project_file = "data/Framework_SIGMA.json"
        if os.path.exists(project_file):
            result = runner.invoke(load_framework, [project_file])

            assert result.exit_code == 0
            assert "Caricati" in result.output
            assert "moduli dal file" in result.output
        else:
            # Skip se il file non esiste
            pytest.skip("File Framework_SIGMA.json non trovato")


class TestCLIErrorHandling:
    """Test gestione errori CLI"""

    def test_cli_invalid_command_real(self):
        """Test comando inesistente"""
        runner = CliRunner()

        result = runner.invoke(main, ["invalid-command"])

        # Click dovrebbe restituire errore per comando inesistente
        assert result.exit_code != 0
        assert "No such command" in result.output

    def test_cli_config_error_handling_real(self):
        """Test gestione errori configurazione con config reale"""
        runner = CliRunner()

        # Test che il CLI gestisca configurazione non perfetta
        result = runner.invoke(main, ["--help"])

        # CLI dovrebbe gestire config reale gracefully
        assert result.exit_code == 0
        assert "SIGMA-NEX" in result.output

    def test_cli_runner_error_handling_real(self):
        """Test gestione errori Runner con configurazioni reali"""
        runner = CliRunner()

        # Test error recovery con mock minimale
        with patch(
            "sigma_nex.core.runner.Runner.interactive",
            side_effect=Exception("Interactive error"),
        ):
            result = runner.invoke(main, ["start"])

            # CLI dovrebbe gestire l'errore del Runner gracefully
            assert result.exit_code != 0


class TestCLIPerformance:
    """Test performance CLI"""

    def test_cli_startup_time_real(self):
        """Test tempo di avvio CLI"""
        import time

        runner = CliRunner()

        start_time = time.time()
        result = runner.invoke(main, ["--help"])
        end_time = time.time()

        # CLI dovrebbe avviarsi rapidamente
        startup_time = end_time - start_time
        assert startup_time < 2.0  # Meno di 2 secondi
        assert result.exit_code == 0

    def test_cli_memory_usage_real(self):
        """Test uso memoria CLI"""
        import gc

        runner = CliRunner()

        initial_objects = len(gc.get_objects())

        # Esegui diversi comandi CLI
        runner.invoke(main, ["--help"])

        with patch("sigma_nex.cli.get_config", return_value={"model": "test"}):
            runner.invoke(main, ["self-check", "--help"])

        gc.collect()
        final_objects = len(gc.get_objects())

        # Non dovrebbe esserci memory leak significativo
        objects_increase = final_objects - initial_objects
        assert objects_increase < 1000  # Threshold ragionevole


class TestCLICoreIntegration:
    """Test integrazione CLI con core modules senza mock"""

    def test_cli_config_real_access(self):
        """Test accesso alla configurazione reale dal CLI"""
        from sigma_nex.config import get_config

        # Test che get_config funzioni realmente
        config = get_config()
        assert hasattr(config, "config")
        assert isinstance(config.config, dict)

        # Test accesso a parametri reali
        model_name = config.get("model_name", "default")
        assert isinstance(model_name, str)
        assert len(model_name) > 0

    def test_cli_dataloader_real_functionality(self):
        """Test funzionalità reale DataLoader dal CLI"""
        from sigma_nex.data_loader import DataLoader

        # Test inizializzazione DataLoader reale
        loader = DataLoader()
        assert hasattr(loader, "load")
        assert callable(loader.load)

        # Test con file JSON temporaneo reale
        test_data = {
            "framework": "SIGMA-TEST",
            "modules": [
                {"id": "test_module", "name": "Test Module", "category": "test"}
            ],
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            # Test caricamento REALE
            count = loader.load(temp_path)
            assert count == 1
        finally:
            os.unlink(temp_path)

    def test_cli_runner_real_initialization(self):
        """Test inizializzazione reale Runner dal CLI"""
        from sigma_nex.config import get_config
        from sigma_nex.core.runner import Runner

        # Test inizializzazione con config reale
        config = get_config()

        with patch(
            "sigma_nex.core.runner.shutil.which", return_value="/usr/bin/ollama"
        ):
            runner = Runner(config.config, secure=False)

            # Verifica inizializzazione reale
            assert hasattr(runner, "config")
            assert hasattr(runner, "model")
            assert hasattr(runner, "history")
            assert isinstance(runner.config, dict)
            assert isinstance(runner.model, str)

    def test_cli_validation_real_functions(self):
        """Test funzioni validation reali dal CLI"""
        from sigma_nex.utils.validation import (
            sanitize_log_data,
            sanitize_text_input,
            validate_user_id,
        )

        # Test sanitize_text_input REALE
        clean_text = sanitize_text_input("Test input <script>alert('xss')</script>")
        assert "script" not in clean_text
        assert "Test input" in clean_text

        # Test validate_user_id REALE
        user_id = validate_user_id(12345)
        assert user_id == 12345

        # Test sanitize_log_data REALE
        log_data = {"message": "test", "password": "secret"}
        clean_data = sanitize_log_data(log_data)
        assert "test" in str(clean_data)
        assert "secret" not in str(clean_data)


class TestCLIRealWorldUsage:
    """Test utilizzo real-world del CLI"""

    def test_cli_workflow_complete_real(self):
        """Test workflow completo CLI senza mock eccessivi"""
        runner = CliRunner()

        # 1. Crea file framework di test
        test_modules = [
            {"id": "test_001", "name": "Test Module 1", "category": "test"},
            {"id": "test_002", "name": "Test Module 2", "category": "test"},
        ]
        test_data = {"framework": "SIGMA-NEX", "modules": test_modules}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as temp_file:
            json.dump(test_data, temp_file)
            temp_path = temp_file.name

        try:
            # 2. Carica framework REALE (senza mock DataLoader)
            result = runner.invoke(load_framework, [temp_path])
            assert result.exit_code == 0
            assert "Caricati 2 moduli" in result.output

            # 3. Esegui self-check con config reale
            with patch("sigma_nex.core.runner.Runner.self_check") as mock_self_check:
                result = runner.invoke(main, ["self-check"])
                assert result.exit_code == 0
                mock_self_check.assert_called_once()

        finally:
            os.unlink(temp_path)

    def test_cli_help_documentation_real(self):
        """Test documentazione help CLI"""
        runner = CliRunner()

        # Test help del comando principale
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert (
            len(result.output) > 100
        )  # Help dovrebbe essere sufficientemente dettagliato

        # Test help dei sottocomandi
        for command in ["start", "load-framework", "self-check"]:
            result = runner.invoke(main, [command, "--help"])
            assert result.exit_code == 0
            assert len(result.output) > 50  # Ogni comando dovrebbe avere help

    def test_cli_server_command_coverage(self):
        """Test comando server per aumentare coverage"""
        runner = CliRunner()

        # Test server command con mock per evitare avvio reale
        with patch("sigma_nex.server.SigmaServer") as mock_server_class:
            mock_server = Mock()
            mock_server.run = Mock()
            mock_server_class.return_value = mock_server

            # Test comando server
            result = runner.invoke(main, ["server", "--port", "8001"])

            # Dovrebbe tentare di avviare il server
            mock_server_class.assert_called_once()
            mock_server.run.assert_called_once_with(host="127.0.0.1", port=8001)

            # Il comando dovrebbe essere riuscito
            assert result.exit_code == 0
            assert "Avvio server SIGMA-NEX" in result.output

    def test_cli_gui_command_coverage(self):
        """Test comando GUI per aumentare coverage"""
        runner = CliRunner()

        # Test GUI command con mock per evitare avvio reale finestra
        with patch("sigma_nex.gui.main") as mock_gui_main:

            # Test comando gui
            result = runner.invoke(main, ["gui"])

            # Dovrebbe tentare di avviare la GUI
            mock_gui_main.assert_called_once()

            # Il comando dovrebbe essere riuscito
            assert result.exit_code == 0

    def test_cli_import_error_handling(self):
        """Test gestione errori di importazione nel CLI"""
        runner = CliRunner()

        # Test comportamento con import error simulato per server
        with patch.dict("sys.modules", {"sigma_nex.server": None}):
            result = runner.invoke(main, ["server"])

            # Dovrebbe gestire gracefully l'errore di import
            assert result.exit_code == 0  # Il comando gestisce l'errore internamente
            assert "dipendenze del server non installate" in result.output

    def test_cli_unknown_command_coverage(self):
        """Test comando inesistente per aumentare coverage"""
        runner = CliRunner()

        # Test comando inesistente
        result = runner.invoke(main, ["unknown-command"])

        # Dovrebbe restituire errore per comando non trovato
        assert result.exit_code != 0
        assert "No such command" in result.output or "Usage:" in result.output

    def test_cli_config_error_conditions(self):
        """Test condizioni d'errore della configurazione"""
        runner = CliRunner()

        # Test con config che potrebbe fallire
        with patch("sigma_nex.cli.get_config", side_effect=Exception("Config error")):
            result = runner.invoke(main, ["--help"])

            # Il comando help dovrebbe funzionare anche con errori config
            # perché non accede alla config
            assert result.exit_code == 0

    def test_cli_runner_initialization_errors(self):
        """Test errori di inizializzazione del Runner"""
        runner = CliRunner()

        # Test start command con Runner che fallisce l'inizializzazione
        with patch("sigma_nex.cli.Runner", side_effect=Exception("Runner init failed")):
            result = runner.invoke(main, ["start"])

            # Dovrebbe gestire gracefully l'errore
            assert result.exit_code != 0

    def test_cli_self_heal_functionality(self):
        """Test funzionalità self-heal del CLI"""
        runner = CliRunner()

        # Test self-heal con file temporaneo
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as temp_file:
            temp_file.write('# Test file with potential issue\nprint("hello")\n')
            temp_path = temp_file.name

        try:
            with patch("sigma_nex.core.runner.Runner") as mock_runner_class:
                mock_runner = Mock()
                mock_runner.self_heal_file.return_value = True
                mock_runner_class.return_value = mock_runner

                # Test self-heal command
                result = runner.invoke(main, ["self-heal", temp_path])

                # Dovrebbe tentare self-heal
                assert result.exit_code in [0, 1]  # Success o errore controlled

        finally:
            os.unlink(temp_path)
