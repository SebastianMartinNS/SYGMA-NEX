#!/usr/bin/env python3
"""
SIGMA-NEX Project Cleanup Script

Removes temporary files, build artifacts, and cache directories.
"""

import glob
import os
import shutil


def remove_patterns(patterns, root_dir="."):
    """Remove files matching patterns."""
    removed = []
    for pattern in patterns:
        matches = glob.glob(os.path.join(root_dir, pattern), recursive=True)
        for match in matches:
            try:
                if os.path.isdir(match):
                    shutil.rmtree(match)
                    print(f"Removed directory: {match}")
                else:
                    os.remove(match)
                    print(f"Removed file: {match}")
                removed.append(match)
            except Exception as e:
                print(f"⚠️  Could not remove {match}: {e}")
    return removed


def main():
    """Main cleanup function."""
    print("🧹 Starting SIGMA-NEX project cleanup...")

    # Patterns to remove
    cleanup_patterns = [
        # Python cache
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        # Build artifacts
        "build",
        "dist",
        "*.egg-info",
        "*.spec",
        # Temporary files
        "*.tmp",
        "*.temp",
        "*.patch",
        "*.log",
        # OS specific
        ".DS_Store",
        "Thumbs.db",
        # Editor files
        "*.swp",
        "*.swo",
        "*~",
        # Project specific
        "*- Copia.*",
        "*0.1.*",
        "*2.*",
        "*.exe",
        "*.zip",
    ]

    removed = remove_patterns(cleanup_patterns)

    print(f"\n✅ Cleanup completed! Removed {len(removed)} items.")
    print("\nProject is now clean and organized!")


if __name__ == "__main__":
    main()
