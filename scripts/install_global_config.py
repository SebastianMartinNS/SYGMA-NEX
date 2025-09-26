#!/usr/bin/env python3
"""Global configuration installer for SIGMA-NEX."""

import os
import shutil
import sys
from pathlib import Path


def install_global_config():
    """Install global configuration files."""

    if os.name == 'nt':
        global_config_dir = Path.home() / "AppData" / "Roaming" / "sigma-nex"
    else:
        global_config_dir = Path.home() / ".config" / "sigma-nex"

    global_config_dir.mkdir(parents=True, exist_ok=True)
    print("Installing global config to: {}".format(global_config_dir))

    return global_config_dir


def uninstall_global_config():
    """Remove global configuration files."""
    if os.name == 'nt':
        global_config_dir = Path.home() / "AppData" / "Roaming" / "sigma-nex"
    else:
        global_config_dir = Path.home() / ".config" / "sigma-nex"

    if global_config_dir.exists():
        response = input("Remove {}? (y/N): ".format(global_config_dir))
        if response.lower().startswith('y'):
            shutil.rmtree(global_config_dir)
            print("Config removed from: {}".format(global_config_dir))
        else:
            print("Operation cancelled")
    else:
        print("No global config found in: {}".format(global_config_dir))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_global_config()
    else:
        install_global_config()
