#!/usr/bin/env python3
"""Test di debug per verificare problemi CLI"""

import json
import tempfile
from unittest.mock import patch
from click.testing import CliRunner
from sigma_nex.cli import main

def test_debug_load_framework():
    """Test debug per load-framework"""
    runner = CliRunner()
    
    test_data = {
        "framework": "SIGMA-NEX",
        "version": "1.0",
        "modules": [
            {
                "id": "survival_001",
                "name": "Water Procurement", 
                "category": "survival",
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as temp_file:
        json.dump(test_data, temp_file, indent=2)
        temp_path = temp_file.name
    
    try:
        # Test con patch per evitare banner Unicode
        with (
            patch("sigma_nex.cli.show_ascii_banner"),  # Disabilita banner
            patch("sigma_nex.cli.require_auth", lambda x: lambda f: f),
            patch("sigma_nex.data_loader.DataLoader.load", return_value=2),
        ):
            env = {"SIGMA_SESSION_TOKEN": "test_token"}
            result = runner.invoke(main, ["load-framework", "--path", temp_path], env=env)
            print(f"Exit code con patch: {result.exit_code}")
            print(f"Output (safe): {repr(result.output)}")
            if result.exception:
                print(f"Exception: {result.exception}")
                print(f"Exception type: {type(result.exception)}")
    
    except Exception as e:
        print(f"Error in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_debug_load_framework()