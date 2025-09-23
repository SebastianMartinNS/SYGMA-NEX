import pytest
from click.testing import CliRunner
from sigma_nex.cli import main

def test_help():
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
