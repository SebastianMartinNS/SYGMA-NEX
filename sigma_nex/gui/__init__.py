"""
SIGMA-NEX GUI Main Module

Entry point for the graphical user interface of SIGMA-NEX.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .main_gui import SigmaNexGUI, launch_gui


def main():
    """Main entry point for SIGMA-NEX GUI."""
    print("🚀 Starting SIGMA-NEX GUI...")
    launch_gui()


if __name__ == "__main__":
    main()