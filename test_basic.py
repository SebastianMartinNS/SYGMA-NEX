"""
Basic test to verify core functionality without complex fixtures.
"""

import os
import sys
from pathlib import Path

# Add sigma_nex to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all core modules can be imported."""
    try:
        from sigma_nex import config, data_loader
        from sigma_nex.core import context, retriever, runner, translate
        from sigma_nex.utils import security, validation
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config_basic():
    """Test basic config functionality."""
    try:
        from sigma_nex.config import SigmaConfig
        
        # Change to project directory
        old_cwd = os.getcwd()
        os.chdir(project_root)
        
        try:
            config = SigmaConfig()
            print(f"✓ Config initialized")
            print(f"✓ Project root: {config.project_root}")
            print(f"✓ Debug mode: {config.get('debug', False)}")
            print(f"✓ Model name: {config.get('model_name', 'not-set')}")
            return True
        finally:
            os.chdir(old_cwd)
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False

def test_validation_basic():
    """Test basic validation functionality."""
    try:
        from sigma_nex.utils.validation import validate_query, sanitize_input
        
        # Test valid queries
        result = validate_query("Come costruire un riparo?", ["test"], is_medical=False)
        print(f"✓ Query validation: {result}")
        
        # Test sanitization
        clean = sanitize_input("Test <script>alert('xss')</script> input")
        print(f"✓ Input sanitization: '{clean}'")
        
        return True
    except Exception as e:
        print(f"✗ Validation error: {e}")
        return False

def test_data_loading():
    """Test data loading functionality."""
    try:
        from sigma_nex.data_loader import load_framework_data, load_faq_data
        
        framework_path = project_root / "data" / "Framework_SIGMA.json"
        faq_path = project_root / "data" / "faq_domande_critiche.json"
        
        if framework_path.exists():
            framework_data = load_framework_data(str(framework_path))
            print(f"✓ Framework data loaded: {len(framework_data)} modules")
        else:
            print("⚠ Framework data file not found")
        
        if faq_path.exists():
            faq_data = load_faq_data(str(faq_path))
            print(f"✓ FAQ data loaded: {len(faq_data)} items")
        else:
            print("⚠ FAQ data file not found")
        
        return True
    except Exception as e:
        print(f"✗ Data loading error: {e}")
        return False

def test_core_classes():
    """Test that core classes can be instantiated."""
    try:
        from sigma_nex.core.context import ContextManager
        from sigma_nex.core.retriever import SigmaRetriever
        from sigma_nex.core.runner import SigmaRunner
        
        # Test ContextManager
        context_mgr = ContextManager()
        print("✓ ContextManager instantiated")
        
        # Test SigmaRetriever
        retriever = SigmaRetriever()
        print("✓ SigmaRetriever instantiated")
        
        # Test SigmaRunner with basic params
        runner = SigmaRunner()
        print("✓ SigmaRunner instantiated")
        
        return True
    except Exception as e:
        print(f"✗ Core classes error: {e}")
        return False

if __name__ == "__main__":
    print("Running basic SIGMA-NEX functionality tests...\n")
    
    tests = [
        test_imports,
        test_config_basic, 
        test_validation_basic,
        test_data_loading,
        test_core_classes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\n--- {test.__name__} ---")
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All basic tests passed! Core functionality is working.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the output above for details.")
        sys.exit(1)