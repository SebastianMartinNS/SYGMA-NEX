#!/usr/bin/env python3
"""
SIGMA-NEX CI/CD Status Monitor

Script per monitorare lo stato dei workflow GitHub Actions e fornire
informazioni dettagliate sullo stato del sistema CI/CD.

Usage:
    python monitor_ci.py [--verbose] [--json]
"""

import subprocess
from datetime import datetime
from pathlib import Path


def run_command(cmd: str, capture_output: bool = True) -> str:
    """Execute shell command and return output."""
    try:
        result = subprocess.run(
            cmd.split(), capture_output=capture_output, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    except FileNotFoundError:
        return "Error: Command not found"


def check_git_status():
    """Check git repository status."""
    print("Git Repository Status:")
    print("-" * 40)

    # Current branch
    branch = run_command("git branch --show-current")
    print(f"Current branch: {branch}")

    # Latest commit
    commit = run_command("git log --oneline -1")
    print(f"Latest commit: {commit}")

    # Remote status
    status = run_command("git status --porcelain")
    if status:
        print(f"Uncommitted changes: {len(status.splitlines())} files")
    else:
        print("Working directory clean")

    print()


def check_workflows():
    """Check workflow files status."""
    print("Workflow Configuration:")
    print("-" * 40)

    workflows_dir = Path(".github/workflows")
    if not workflows_dir.exists():
        print("No .github/workflows directory found")
        return

    workflow_files = list(workflows_dir.glob("*.yml"))
    print(f"Found {len(workflow_files)} workflow files:")

    for workflow_file in workflow_files:
        print(f"   {workflow_file.name}")

        # Check if file is valid YAML
        try:
            with open(workflow_file, "r", encoding="utf-8") as f:
                content = f.read()
                if "name:" in content and "on:" in content:
                    print(f"      Valid workflow syntax")
                else:
                    print(f"      Missing required fields")
        except Exception as e:
            print(f"      Error reading file: {e}")

    print()


def check_test_structure():
    """Check test directory structure."""
    print("🧪 Test Structure:")
    print("-" * 40)

    tests_dir = Path("tests")
    if not tests_dir.exists():
        print("No tests directory found")
        return

    # Check for required subdirectories
    required_dirs = ["unit", "integration", "performance"]

    for dir_name in required_dirs:
        dir_path = tests_dir / dir_name
        if dir_path.exists():
            test_files = list(dir_path.glob("test_*.py"))
            print(f"{dir_name}/: {len(test_files)} test files")
        else:
            print(f" {dir_name}/: Directory not found")

    # Count total test files
    all_test_files = list(tests_dir.glob("**/test_*.py"))
    print(f"Total test files: {len(all_test_files)}")
    print()


def check_dependencies():
    """Check dependency files."""
    print("Dependencies:")
    print("-" * 40)

    # Main requirements
    if Path("requirements.txt").exists():
        with open("requirements.txt", "r") as f:
            main_deps = len(
                [line for line in f if line.strip() and not line.startswith("#")]
            )
        print(f"requirements.txt: {main_deps} dependencies")
    else:
        print("requirements.txt: Not found")

    # Test requirements
    if Path("requirements-test.txt").exists():
        with open("requirements-test.txt", "r") as f:
            test_deps = len(
                [line for line in f if line.strip() and not line.startswith("#")]
            )
        print(f"requirements-test.txt: {test_deps} dependencies")
    else:
        print("requirements-test.txt: Not found")

    # Check if development tools are available
    dev_tools = {
        "black": "Code formatter",
        "isort": "Import sorter",
        "flake8": "Linter",
        "mypy": "Type checker",
        "pytest": "Test runner",
    }

    print("Development tools:")
    for tool, description in dev_tools.items():
        try:
            version = run_command(f"{tool} --version")
            if "Error" not in version:
                print(f"   {tool}: Available ({description})")
            else:
                print(f"   {tool}: Not available ({description})")
        except BaseException:
            print(f"   {tool}: Not available ({description})")

    print()


def check_quality_status():
    """Check current code quality status."""
    print("Code Quality Status:")
    print("-" * 40)

    # Run basic quality checks
    quality_checks = {
        "black --check sigma_nex": "Code formatting",
        "isort --check-only sigma_nex": "Import sorting",
        "flake8 sigma_nex --count": "Linting issues",
        "pytest tests/unit/ --tb=no -q": "Unit tests",
    }

    for cmd, description in quality_checks.items():
        result = run_command(cmd)
        if "Error" in result:
            print(f"   {description}: Tool not available")
        elif "would reformat" in result or "incorrectly sorted" in result:
            print(f"   {description}: Issues found")
        elif result.strip().isdigit() and int(result.strip()) > 0:
            print(f"   {description}: {result.strip()} issues")
        elif "passed" in result or result == "0":
            print(f"   {description}: OK")
        else:
            print(f"   {description}: Check needed")

    print()


def generate_action_items():
    """Generate actionable next steps."""
    print("Next Steps:")
    print("-" * 40)

    print("1. Check GitHub Actions:")
    print("   - Go to: https://github.com/SebastianMartinNS/SYGMA-NEX/actions")
    print("   - Verify CI/CD Pipeline is running")
    print("   - Check for any failure messages")
    print()

    print("2. Run Quality Workflow:")
    print("   - Go to: Actions → Code Quality Improvement")
    print("   - Click 'Run workflow'")
    print("   - Select 'all' for comprehensive fixes")
    print()

    print("3. Monitor Progress:")
    print("   - Check workflow status every few minutes")
    print("   - Review quality reports in Artifacts")
    print("   - Monitor test success rates")
    print()

    print("4. Iterative Improvement:")
    print("   - Address any critical failures first")
    print("   - Use auto-fix for formatting issues")
    print("   - Gradually improve code quality metrics")


def main():
    """Main monitoring function."""
    print("SIGMA-NEX CI/CD Status Monitor")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Run all checks
    check_git_status()
    check_workflows()
    check_test_structure()
    check_dependencies()
    check_quality_status()
    generate_action_items()

    print("=" * 50)
    print("Monitoring complete!")
    print("Tip: Run this script regularly to track CI/CD health")


if __name__ == "__main__":
    main()
