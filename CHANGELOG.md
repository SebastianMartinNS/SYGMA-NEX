# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2025-09-24

### Added 
-  **Test Suite Completa**: 
- 🔧 **Files Management**: 
- ⚙️ **Configuration**: 

### Changed
-  **Documentazione**: 
-  **Test**: 
-  **Struttura**: Repository pulito e organizzato per produzione

### Removed
-  **File Obsoleti**: Test temporanei, script locali, configurazioni duplicate
-  **Test Deprecati**: test_basic.py, marian_test.py, test_server_medical.py
-  **Build Scripts**: build_index.py, setup_dev.bat, cleanup.bat
-  **Config Duplicati**: pytest-simple.ini, config.production.yaml

## [0.2.1] - 2024-12-22

### Added
- Comprehensive project reorganization and professionalization
- Professional README.md with badges, installation guide, and usage examples
- Complete API documentation in `docs/api.md`
- Development guide in `docs/development.md`
- Proper `pyproject.toml` configuration with modern Python packaging standards
- MIT License file
- `.gitignore` file with comprehensive exclusions
- New `sigma_nex.server` module with clean FastAPI implementation
- Development scripts in `scripts/` directory
- Batch files for easy Windows development setup
- Enhanced CLI with server and GUI commands
- Professional project structure with clear separation of concerns

### Changed
- Reorganized project structure for better maintainability
- Updated `requirements.txt` with proper versioning and missing dependencies
- Improved CLI interface with better help text and new commands
- Consolidated GUI functionality in `sigma_nex.gui` package
- Enhanced configuration management
- Updated setup.py to use modern packaging standards

### Removed
- Duplicate files (`sigma_api_server - Copia.py`, `sigma_api_server0.1.py`)
- Temporary files (`1234567890'ì+.txt`, `Nuovo Documento di testo.txt`)
- Old GUI files (`gui.pyw`, `gui_final_fixed.pyw`)
- Build artifacts (`build/`, `dist/`, `*.spec` files)
- Python cache files (`__pycache__/`)
- Patch files (`*.patch`)
- Executable files (`*.exe`)

### Fixed
- Import paths and module organization
- Dependency management and version specifications
- Project metadata and configuration
- Code structure and maintainability issues

### Security
- Added proper input validation patterns
- Implemented IP-based access control for sensitive endpoints
- Enhanced logging and monitoring capabilities

---

## [Unreleased] - 2025-01-XX

### Added
- ✨ **Professional Documentation Suite**: Complete GitHub documentation overhaul
  - Comprehensive README.md with architecture diagrams and usage examples
  - CONTRIBUTING.md with detailed contribution guidelines
  - CODE_OF_CONDUCT.md for community standards
  - SECURITY.md for responsible disclosure policy
- 🔧 **Enhanced VS Code Tasks**: Updated tasks.json for proper venv usage
- 📦 **Sentence Transformers**: Added sentence-transformers to runtime dependencies
- 🔄 **SigmaConfig Migration**: Migrated CLI from legacy load_config to SigmaConfig class
- 🚫 **Retrieval Off Mode**: Implemented configurable retrieval disable via config.yaml
- 🏗️ **Improved Build System**: Enhanced pyproject.toml with modern packaging standards

### Changed
- 📚 **Documentation Overhaul**: Complete rewrite of project documentation for professional presentation
- ⚙️ **Configuration System**: Enhanced SigmaConfig with retrieval_enabled flag
- 🧪 **Test Suite Updates**: Updated test cases to reflect new context building behavior
- 🔨 **Development Tools**: Improved task configurations for better developer experience

### Fixed
- 🐛 **Context Building Logic**: Fixed prompt building to conditionally include knowledge sections
- ✅ **Test Compatibility**: Updated tests to match new retrieval behavior
- 🔧 **Build Configuration**: Fixed VS Code task configurations for venv usage

### Security
- 🔒 **Enhanced Security Documentation**: Added comprehensive security policy and disclosure guidelines
- 🛡️ **Input Validation**: Improved input sanitization in context building
- 📊 **Audit Trail**: Better logging for security-relevant operations

---

## Previous Versions

### [0.2.0] - Previous Release
- Initial working version with GUI, CLI, and API server
- Basic Ollama integration
- Translation functionality with MarianMT
- Medical query enhancement

### [0.1.0] - Initial Release
- Basic CLI functionality
- Core SIGMA-NEX agent implementation
- Initial configuration system
