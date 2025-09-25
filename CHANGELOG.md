# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] - 2025-09-25

### Changed
- **License Update**: Migrated from MIT License to Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
- **Commercial Restrictions**: Software now restricted to educational, research, and personal use only
- **Documentation Updates**: Updated README.md, AUTHORS.md, setup.py, and pyproject.toml to reflect new license
- **Attribution Requirements**: Added clear attribution requirements for any redistribution or derivative works

### Legal
- **Open Source Status**: Remains open source but with non-commercial restrictions
- **Commercial Licensing**: Commercial use now requires explicit written permission from copyright holder
- **Clear Terms**: Added professional license terms with warranty disclaimers and attribution requirements

## [0.3.2] - 2025-09-25

### Fixed
- **FAISS Compatibility**: Resolved NumPy 2.x compatibility issues, downgraded to NumPy 1.26.4
- **FAISS Index Rebuild**: Fixed dimension mismatch (8 vs 384) by rebuilding index with correct model
- **Unit Test Mocking**: Fixed test_retriever_realistic.py mock test with proper cache reset logic
- **Dependency Resolution**: Added missing SentencePiece library for translation functionality
- **Model Caching**: Implemented proper global model cache management in tests

### Changed
- **Test Coverage**: Achieved 328/333 tests passing (99.1% success rate)
- **Code Quality**: Applied black formatting, maintained clean code standards
- **Security Analysis**: Updated bandit security report with 8 low-severity findings
- **FAISS Operations**: Restored full semantic search functionality with 3-result validation

### Technical
- **Environment**: Python 3.11.3, FAISS 1.7.4, NumPy 1.26.4, SentenceTransformers 4.1.0
- **Coverage**: 84.92% test coverage across 14 source files (1811 LOC)
- **Security**: 8 low-severity issues identified, all related to subprocess usage (acceptable)
- **Performance**: FAISS semantic search operational, translation system verified

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

## [0.2.1] - 2025-XX-XX

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
-  **Professional Documentation Suite**: Complete GitHub documentation overhaul
  - Comprehensive README.md with architecture diagrams and usage examples
  - CONTRIBUTING.md with detailed contribution guidelines
  - CODE_OF_CONDUCT.md for community standards
  - SECURITY.md for responsible disclosure policy
-  **Enhanced VS Code Tasks**: Updated tasks.json for proper venv usage
-  **Sentence Transformers**: Added sentence-transformers to runtime dependencies
-  **SigmaConfig Migration**: Migrated CLI from legacy load_config to SigmaConfig class
-  **Retrieval Off Mode**: Implemented configurable retrieval disable via config.yaml
-  **Improved Build System**: Enhanced pyproject.toml with modern packaging standards

### Changed
-  **Documentation Overhaul**: Complete rewrite of project documentation for professional presentation
-  **Configuration System**: Enhanced SigmaConfig with retrieval_enabled flag
-  **Test Suite Updates**: Updated test cases to reflect new context building behavior
-  **Development Tools**: Improved task configurations for better developer experience

### Fixed
-  **Context Building Logic**: Fixed prompt building to conditionally include knowledge sections
-  **Test Compatibility**: Updated tests to match new retrieval behavior
-  **Build Configuration**: Fixed VS Code task configurations for venv usage

### Security
-  **Enhanced Security Documentation**: Added comprehensive security policy and disclosure guidelines
-  **Input Validation**: Improved input sanitization in context building
-  **Audit Trail**: Better logging for security-relevant operations

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
