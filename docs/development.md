# Development Guide

## Setup Development Environment

### Prerequisites

1. **Python 3.10+**
2. **Git**
3. **Ollama** installed and running
4. **VS Code** (recommended) with Python extension

### Initial Setup

```bash
# Clone repository
git clone https://github.com/SebastianMartinNS/SYGMA-NEX.git
cd SYGMA-NEX

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Project Structure

```
sigma-nex/
├── sigma_nex/              # Main package
│   ├── __init__.py
│   ├── cli.py             # Command-line interface
│   ├── config.py          # Configuration management
│   ├── data_loader.py     # Data loading utilities
│   ├── server.py          # FastAPI server
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   ├── context.py     # Context management
│   │   ├── retriever.py   # Information retrieval
│   │   ├── runner.py      # Main execution engine
│   │   └── translate.py   # Translation utilities
│   ├── gui/               # Graphical interface
│   │   ├── __init__.py
│   │   └── main_gui.py    # Main GUI application
│   └── utils/             # Utility modules
│       ├── __init__.py
│       └── security.py    # Security utilities
├── data/                  # Data files and frameworks
├── tests/                 # Test suite
├── docs/                  # Documentation
├── config.yaml           # Main configuration
├── requirements.txt       # Dependencies
├── pyproject.toml        # Project metadata
└── README.md             # Project overview
```

## Development Workflow

### Code Style

We use several tools to maintain code quality:

```bash
# Format code
black sigma_nex/
isort sigma_nex/

# Lint code
flake8 sigma_nex/

# Type checking (optional)
mypy sigma_nex/
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sigma_nex --cov-report=html

# Run specific test file
pytest tests/test_runner.py

# Run specific test
pytest tests/test_runner.py::test_specific_function
```

### Adding New Features

1. **Create a branch:**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Write tests first (TDD):**
   ```python
   # tests/test_my_feature.py
   def test_my_new_feature():
       # Test implementation
       pass
   ```

3. **Implement the feature:**
   ```python
   # sigma_nex/my_feature.py
   def my_new_function():
       # Implementation
       pass
   ```

4. **Update documentation:**
   - Add docstrings
   - Update README if needed
   - Add to API docs if applicable

5. **Test everything:**
   ```bash
   pytest
   black sigma_nex/
   flake8 sigma_nex/
   ```

6. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: add my new feature"
   git push origin feature/my-new-feature
   ```

### Core Components

#### Runner (sigma_nex/core/runner.py)

The main execution engine that handles:
- Ollama model interaction
- Progress tracking
- Self-healing capabilities
- Interactive REPL

#### Server (sigma_nex/server.py)

FastAPI-based API server featuring:
- Request/response handling
- Logging and monitoring
- Medical query integration
- Blocklist management

#### GUI (sigma_nex/gui/main_gui.py)

CustomTkinter-based interface providing:
- User-friendly interaction
- Real-time responses
- Command history

### Configuration

Configuration is managed through `config.yaml`:

```yaml
model_name: "mistral"
system_prompt: |
  Your system prompt here...
```

Access configuration in code:
```python
from sigma_nex.config import load_config

cfg = load_config()
model = cfg.get('model_name', 'mistral')
```

### Adding New CLI Commands

```python
# In sigma_nex/cli.py
@main.command()
@click.option('--my-option', help='My option help')
@click.pass_context
def my_command(ctx, my_option):
    """My command description."""
    # Implementation
    pass
```

### Adding New API Endpoints

```python
# In sigma_nex/server.py, within _setup_routes method
@self.app.get("/my-endpoint")
async def my_endpoint():
    """My endpoint description."""
    return {"message": "Hello"}
```

### Database Integration

Currently, SIGMA-NEX uses file-based storage. For database integration:

1. **Choose a database** (SQLite for local, PostgreSQL for production)
2. **Add dependencies:**
   ```toml
   # pyproject.toml
   dependencies = [
       "sqlalchemy>=2.0.0",
       "alembic>=1.12.0",
   ]
   ```
3. **Create models:**
   ```python
   # sigma_nex/models.py
   from sqlalchemy import Column, Integer, String
   from sqlalchemy.ext.declarative import declarative_base

   Base = declarative_base()

   class MyModel(Base):
       __tablename__ = "my_table"
       id = Column(Integer, primary_key=True)
       name = Column(String)
   ```

### Performance Optimization

- Use `asyncio` for I/O operations
- Implement caching for frequent queries
- Monitor memory usage with large models
- Profile with `cProfile` for bottlenecks

### Security Considerations

- Validate all user inputs
- Use environment variables for secrets
- Implement proper authentication for production
- Regular security audits with `bandit`

### Deployment

#### Development Deployment
```bash
# Start all services
sigma server &
sigma gui &
```

#### Production Deployment
```bash
# Use gunicorn for production
gunicorn sigma_nex.server:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Debugging

#### Common Issues

1. **Ollama not found:**
   ```bash
   which ollama  # Check if installed
   ollama list   # Check available models
   ```

2. **Translation models missing:**
   - Check `sigma_nex/core/models/translate/` directory
   - Download from HuggingFace if needed

3. **GUI not starting:**
   - Ensure `customtkinter` is installed
   - Check display settings on Linux

#### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Contributing Guidelines

1. **Follow PEP 8** style guidelines
2. **Write tests** for all new functionality
3. **Update documentation** for public APIs
4. **Use meaningful commit messages** (conventional commits)
5. **Keep PRs focused** and reasonably sized
6. **Review security implications** of changes

### Release Process

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md**
3. **Create release tag:**
   ```bash
   git tag -a v0.2.1 -m "Release v0.2.1"
   git push origin v0.2.1
   ```
4. **Build and publish:**
   ```bash
   python -m build
   twine upload dist/*
   ```

## Getting Help

- **GitHub Issues:** For bugs and feature requests
- **GitHub Discussions:** For questions and ideas
- **Email:** rootedlab6@gmail.com for direct contact

Happy coding!