#!/usr/bin/env python3
"""Global configuration installer for SIGMA-NEX."""

import os
import shutil
import sys
from pathlib import Path


def print_banner():
    """Print the SIGMA-NEX ASCII banner."""
    banner = """
================================================================================
 ███████╗██╗ ██████╗ ███╗   ███╗ █████╗       ███╗   ██╗███████╗██╗  ██╗
 ██╔════╝██║██╔════╝ ████╗ ████║██╔══██╗      ████╗  ██║██╔════╝╚██╗██╔╝
 ███████╗██║██║  ███╗██╔████╔██║███████║█████╗██╔██╗ ██║█████╗   ╚███╔╝
 ╚════██║██║██║   ██║██║╚██╔╝██║██╔══██║╚════╝██║╚██╗██║██╔══╝   ██╔██╗
 ███████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║      ██║ ╚████║███████╗██╔╝ ██╗
 ╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝      ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝

                GLOBAL CONFIGURATION INSTALLER
================================================================================
"""
    print(banner)


def get_config_files():
    """Get list of configuration files to install."""
    config_files = [
        "config.yaml",
        "pytest.ini",
        "pyproject.toml"
    ]
    return [Path(f) for f in config_files if Path(f).exists()]


def install_global_config():
    """Install global configuration files."""
    print_banner()
    print("SIGMA-NEX Global Configuration Installer")
    print("=" * 50)

    # Determine config directory
    if os.name == 'nt':
        global_config_dir = Path.home() / "AppData" / "Roaming" / "sigma-nex"
    else:
        global_config_dir = Path.home() / ".config" / "sigma-nex"

    print(f"[INFO] Directory configurazione globale: {global_config_dir}")

    # Create directory
    try:
        global_config_dir.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Directory creata: {global_config_dir}")
    except Exception as e:
        print(f"[ERROR] Impossibile creare directory: {e}")
        return False

    # Get config files to install
    config_files = get_config_files()
    if not config_files:
        print("[WARNING] Nessun file di configurazione trovato nella directory corrente")
        return False

    print(f"[INFO] File di configurazione da installare: {len(config_files)}")

    # Install files
    installed = 0
    for config_file in config_files:
        dest = global_config_dir / config_file.name
        try:
            shutil.copy2(config_file, dest)
            print(f"[OK] Installato: {config_file.name} -> {dest}")
            installed += 1
        except Exception as e:
            print(f"[ERROR] Installazione fallita {config_file.name}: {e}")

    if installed > 0:
        print(f"\n[SUCCESS] Installati {installed} file(s) di configurazione globale")
        print(f"\nConfigurazione disponibile in: {global_config_dir}")
        return True
    else:
        print("\n[ERROR] Nessun file installato")
        return False


def uninstall_global_config():
    """Remove global configuration files."""
    print_banner()
    print("SIGMA-NEX Global Configuration Uninstaller")
    print("=" * 50)

    if os.name == 'nt':
        global_config_dir = Path.home() / "AppData" / "Roaming" / "sigma-nex"
    else:
        global_config_dir = Path.home() / ".config" / "sigma-nex"

    print(f"[INFO] Directory configurazione: {global_config_dir}")

    if global_config_dir.exists():
        print(f"\nDirectory trovata: {global_config_dir}")
        try:
            # Show contents
            contents = list(global_config_dir.glob("*"))
            if contents:
                print("Contenuto:")
                for item in contents:
                    print(f"  - {item.name}")
            else:
                print("  (vuota)")

            response = input(f"\nRimuovere la directory {global_config_dir}? (y/N): ")
            if response.lower().startswith('y'):
                shutil.rmtree(global_config_dir)
                print(f"[OK] Configurazione rimossa da: {global_config_dir}")
                return True
            else:
                print("[INFO] Operazione annullata")
                return False
        except Exception as e:
            print(f"[ERROR] Rimozione fallita: {e}")
            return False
    else:
        print(f"[INFO] Nessuna configurazione globale trovata in: {global_config_dir}")
        return False


def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        success = uninstall_global_config()
    else:
        success = install_global_config()

    if success:
        print("\n" + "=" * 80)
        print("                    OPERAZIONE COMPLETATA")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("                    OPERAZIONE FALLITA")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
