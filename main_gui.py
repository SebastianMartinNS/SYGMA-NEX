"""
SIGMA-NEX Main GUI Entry Point

This file provides backward compatibility for the main GUI.
The main GUI implementation is now in sigma_nex.gui.main_gui.
"""

import sys
from pathlib import Path

# Add the sigma_nex package to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from sigma_nex.gui.main_gui import launch_gui

    if __name__ == "__main__":
        print("Starting SIGMA-NEX GUI...")
        print("Note: Consider using 'sigma gui' command instead")
        launch_gui()

except ImportError as e:
    print(f"❌ Error importing GUI: {e}")
    print("Please install dependencies: pip install customtkinter")
    input("Press Enter to exit...")
except Exception as e:
    print(f"❌ Error starting GUI: {e}")
    input("Press Enter to exit...")
