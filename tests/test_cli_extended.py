import sys
import builtins
import pytest
from click.testing import CliRunner
from unittest.mock import patch
import json

from sigma_nex import cli


def test_cli_help():
    runner = CliRunner()
    res = runner.invoke(cli.main, ["--help"])
    assert res.exit_code == 0


def test_cli_self_check(monkeypatch):
    # Mock Runner.self_check so it doesn't call external tools
    class DummyRunner:
        def __init__(self, *a, **k):
            pass
        def self_check(self):
            return None
    monkeypatch.setattr(cli, "Runner", DummyRunner)

    runner = CliRunner()
    res = runner.invoke(cli.main, ["self-check"])
    assert res.exit_code == 0


@patch('sigma_nex.server.SigmaServer', side_effect=ImportError('missing'))
def test_cli_server_command_import_guard(mock_server):
    runner = CliRunner()
    res = runner.invoke(cli.main, ["server"])  # should print error and exit 0
    assert res.exit_code == 0
    assert "dipendenze del server" in res.output.lower()


def test_cli_start_command(monkeypatch):
    # Mock Runner.interactive
    class DummyRunner:
        def __init__(self, *a, **k):
            pass
        def interactive(self):
            pass
    monkeypatch.setattr(cli, "Runner", DummyRunner)

    runner = CliRunner()
    res = runner.invoke(cli.main, ["start"])
    assert res.exit_code == 0


def test_cli_load_framework_command(monkeypatch):
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create a test JSON file with modules
        test_data = {"modules": ["module1", "module2", "module3"]}
        with open('test.json', 'w') as f:
            json.dump(test_data, f)
        res = runner.invoke(cli.main, ["load-framework", "test.json"])
        assert res.exit_code == 0
        assert "3" in res.output


def test_cli_load_framework_command_invalid_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create invalid JSON file
        with open('invalid.json', 'w') as f:
            f.write('invalid json')
        res = runner.invoke(cli.main, ["load-framework", "invalid.json"])
        assert res.exit_code == 0  # CLI doesn't fail on load error
        assert "Errore caricamento" in res.output


def test_cli_self_heal_command(monkeypatch):
    # Mock Runner.self_heal_file
    class DummyRunner:
        def __init__(self, *a, **k):
            pass
        def self_heal_file(self, file):
            return "Healed!"
    monkeypatch.setattr(cli, "Runner", DummyRunner)

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test.py', 'w') as f:
            f.write('print("test")')
        res = runner.invoke(cli.main, ["self-heal", "test.py"])
        assert res.exit_code == 0
        assert "Healed!" in res.output


@patch('sigma_nex.gui.main')
def test_cli_gui_command_success(mock_gui_main):
    mock_gui_main.return_value = None

    runner = CliRunner()
    res = runner.invoke(cli.main, ["gui"])
    assert res.exit_code == 0
    mock_gui_main.assert_called_once()


@patch('sigma_nex.server.SigmaServer')
def test_cli_server_command_success(mock_server_class):
    # Mock the SigmaServer class
    mock_server_instance = mock_server_class.return_value
    mock_server_instance.run.return_value = None

    runner = CliRunner()
    res = runner.invoke(cli.main, ["server"])
    assert res.exit_code == 0
    assert "avvio server" in res.output.lower()
    mock_server_class.assert_called_once()
    mock_server_instance.run.assert_called_once()
