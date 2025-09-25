#!/usr/bin/env python3
"""
Script per installare la configurazione globale di SIGMA-NEX.

Questo script copia i file di configurazione e dati necessari in una
posizione globale accessibile da qualsiasi directory.
"""

import os
import shutil
import sys
from pathlib import Path


def install_global_config():
    """Installa i file di configurazione globali."""
    
    # Determina il percorso root del progetto
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Percorso di destinazione per i file globali
    if os.name == 'nt':  # Windows
        global_config_dir = Path.home() / "AppData" / "Roaming" / "sigma-nex"
    else:  # Unix/Linux/MacOS
        global_config_dir = Path.home() / ".config" / "sigma-nex"
    
    print(f"📁 Installazione configurazione globale in: {global_config_dir}")
    
    # Crea la directory se non esiste
    global_config_dir.mkdir(parents=True, exist_ok=True)
    
    # File da copiare
    files_to_copy = [
        ("config.yaml", "config.yaml"),
        ("data", "data"),
        ("logs", "logs"),
    ]
    
    for src_name, dst_name in files_to_copy:
        src_path = project_root / src_name
        dst_path = global_config_dir / dst_name
        
        if src_path.exists():
            if src_path.is_file():
                print(f"📄 Copiando {src_name}...")
                shutil.copy2(src_path, dst_path)
            elif src_path.is_dir():
                print(f"📁 Copiando directory {src_name}...")
                if dst_path.exists():
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
        else:
            print(f"⚠️  File/directory non trovato: {src_path}")
    
    # Crea un file di ambiente per Windows
    if os.name == 'nt':
        env_file = global_config_dir / "set_env.bat"
        with open(env_file, 'w') as f:
            f.write(f"@echo off\n")
            f.write(f"set SIGMA_NEX_ROOT={global_config_dir}\n")
            f.write(f"echo Variabile ambiente SIGMA_NEX_ROOT impostata a: %SIGMA_NEX_ROOT%\n")
        print(f"📝 Creato script ambiente: {env_file}")
        print(f"   Esegui: {env_file}")
    
    # Crea un file di ambiente per Unix
    else:
        env_file = global_config_dir / "set_env.sh"
        with open(env_file, 'w') as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"export SIGMA_NEX_ROOT='{global_config_dir}'\n")
            f.write(f"echo 'Variabile ambiente SIGMA_NEX_ROOT impostata a: $SIGMA_NEX_ROOT'\n")
        os.chmod(env_file, 0o755)
        print(f"📝 Creato script ambiente: {env_file}")
        print(f"   Esegui: source {env_file}")
    
    print(f"\n✅ Installazione completata!")
    print(f"🎯 Per usare SIGMA-NEX da qualsiasi directory:")
    print(f"   1. Imposta la variabile ambiente SIGMA_NEX_ROOT={global_config_dir}")
    print(f"   2. Oppure esegui lo script di ambiente creato")
    print(f"   3. Ora puoi usare 'sigma' da qualsiasi directory")
    
    return global_config_dir


def uninstall_global_config():
    """Rimuove i file di configurazione globali."""
    
    if os.name == 'nt':  # Windows
        global_config_dir = Path.home() / "AppData" / "Roaming" / "sigma-nex"
    else:  # Unix/Linux/MacOS
        global_config_dir = Path.home() / ".config" / "sigma-nex"
    
    if global_config_dir.exists():
        response = input(f"🗑️  Rimuovere {global_config_dir}? (y/N): ")
        if response.lower().startswith('y'):
            shutil.rmtree(global_config_dir)
            print(f"✅ Configurazione globale rimossa da: {global_config_dir}")
        else:
            print("❌ Operazione annullata")
    else:
        print(f"ℹ️  Nessuna configurazione globale trovata in: {global_config_dir}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall_global_config()
    else:
        install_global_config()