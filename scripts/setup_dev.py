#!/usr/bin/env python3
"""
SIGMA-NEX Development Setup Script

Sets up the development environment for SIGMA-NEX.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"{description}...")
    try:
        subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def check_prerequisites():
    """Check if required tools are installed."""
    print("Checking prerequisites...")

    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required")
        return False
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"  # noqa: E501
    print(f"✅ Python {version}")

    # Check if Ollama is installed
    try:
        subprocess.run(["ollama", "--version"], check=True, capture_output=True)
        print("✅ Ollama is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Ollama not found. Please install from https://ollama.com")

    return True


def setup_virtual_environment():
    """Set up Python virtual environment."""
    venv_path = Path("venv")

    if venv_path.exists():
        print("Virtual environment already exists")
        return True

    return run_command(f"{sys.executable} -m venv venv", "Creating virtual environment")


def install_dependencies():
    """Install project dependencies."""
    venv_pip = "venv\\Scripts\\pip" if os.name == "nt" else "venv/bin/pip"

    commands = [
        (f"{venv_pip} install --upgrade pip", "Upgrading pip"),
        (f"{venv_pip} install -e .", "Installing SIGMA-NEX in development mode"),
        (f"{venv_pip} install -e .[dev]", "Installing development dependencies"),
    ]

    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False

    return True


def setup_pre_commit():
    """Set up pre-commit hooks."""
    venv_python = "venv\\Scripts\\python" if os.name == "nt" else "venv/bin/python"

    commands = [
        (f"{venv_python} -m pip install pre-commit", "Installing pre-commit"),
        (
            (
                "venv\\Scripts\\pre-commit install"
                if os.name == "nt"
                else "venv/bin/pre-commit install"
            ),
            "Setting up pre-commit hooks",
        ),
    ]

    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False

    return True


def pull_ollama_models():
    """Pull required Ollama models."""
    models = ["mistral", "medllama2"]

    for model in models:
        print(f"Pulling Ollama model: {model}")
        try:
            subprocess.run(["ollama", "pull", model], check=True)
            print(f"✅ Model {model} downloaded successfully")
        except subprocess.CalledProcessError:
            print(
                f"⚠️  Could not download model {model}. "
                "You may need to install it manually."
            )
        except FileNotFoundError:
            print("⚠️  Ollama not found. Skipping model download.")
            break


def create_dev_config():
    """Create development configuration files."""
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# SIGMA-NEX Development Environment Variables
SIGMA_DEBUG=true
SIGMA_LOG_LEVEL=DEBUG
SIGMA_API_HOST=127.0.0.1
SIGMA_API_PORT=8000
"""
        env_file.write_text(env_content)
        print("✅ Created .env file")

    # Create development config
    dev_config = Path("config.dev.yaml")
    if not dev_config.exists():
        dev_content = """model_name: "mistral"
debug: true
log_level: "DEBUG"
system_prompt: |
  Sei SIGMA-NEX in modalità sviluppo. Fornisci risposte dettagliate e
  includi informazioni di debug quando richiesto.
"""
        dev_config.write_text(dev_content)
        print("✅ Created development config")


def main():
    """Main setup function."""
    print("SIGMA-NEX Development Setup")
    print("=" * 40)

    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please install required tools.")
        return 1

    steps = [
        setup_virtual_environment,
        install_dependencies,
        setup_pre_commit,
        create_dev_config,
    ]

    for step in steps:
        if not step():
            print(f"\n❌ Setup failed at step: {step.__name__}")
            return 1

    # Optional step - doesn't fail setup if it doesn't work
    pull_ollama_models()

    print("\nDevelopment environment setup completed!")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    if os.name == "nt":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run tests: pytest")
    print("3. Start development: sigma start")
    print("4. Check the docs/ folder for more information")

    return 0


if __name__ == "__main__":
    sys.exit(main())
