# SIGMA-NEX Testing Documentation

## Overview

SIGMA-NEX now includes a comprehensive test suite that ensures code quality, performance, and reliability. The testing infrastructure follows modern Python testing best practices with pytest and includes coverage reporting.

## Test Structure

```
tests/
├── conftest.py          # Test configuration and fixtures
├── test_config.py       # Configuration system tests
├── test_validation.py   # Input validation tests
├── test_runner.py       # Core runner functionality tests
└── requirements-test.txt # Testing dependencies
```

## Running Tests

### Install Test Dependencies

```powershell
# Install test dependencies
pip install -r requirements-test.txt

# Or install development dependencies
pip install -e ".[dev]"
```

### Run All Tests

```powershell
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_config.py

# Run specific test class
pytest tests/test_config.py::TestSigmaConfig

# Run specific test method
pytest tests/test_config.py::TestSigmaConfig::test_config_initialization_default
```

### Coverage Reports

```powershell
# Generate HTML coverage report
pytest --cov=sigma_nex --cov-report=html

# Generate terminal coverage report
pytest --cov=sigma_nex --cov-report=term-missing

# Generate XML coverage report (for CI/CD)
pytest --cov=sigma_nex --cov-report=xml
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual components in isolation
- Mock external dependencies
- Fast execution time
- High coverage requirements

### Integration Tests (`@pytest.mark.integration`)
- Test component interactions
- Use real dependencies where appropriate
- Slower execution time
- Focus on end-to-end workflows

### API Tests (`@pytest.mark.api`)
- Test FastAPI server endpoints
- Test API security and validation
- Require Ollama service for full testing

### GUI Tests (`@pytest.mark.gui`)
- Test CustomTkinter interface components
- Mock user interactions
- Visual component validation

## Test Fixtures

### `test_config`
Provides a test configuration dictionary with safe defaults.

### `temp_project_dir`
Creates a temporary project directory with proper structure and test data files.

### `test_config_obj`
Returns a configured SigmaConfig instance for testing.

### `sample_history`, `sample_questions`
Provide realistic test data for conversation testing.

### `mock_ollama_server`
Mocks Ollama API responses for isolated testing.

## Test Examples

### Testing Configuration System
```python
def test_config_path_resolution(test_config_obj):
    config = test_config_obj
    data_path = config.get_path('data', 'data')
    assert data_path.name == 'data'
    assert data_path.is_absolute()
```

### Testing Input Validation
```python
def test_sanitize_script_tags():
    malicious = "<script>alert('xss')</script>Hello"
    result = sanitize_text_input(malicious)
    assert "<script>" not in result
    assert "Hello" in result
```

### Testing API Endpoints
```python
@patch('requests.post')
def test_process_query_successful(mock_post, test_config_obj):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Test response"}
    mock_post.return_value = mock_response
    
    runner = SigmaRunner(test_config_obj)
    result = runner.process_query("Test question")
    
    assert "response" in result
    assert result["response"] == "Test response"
```

## Security Testing

The test suite includes comprehensive security validation:

- **XSS Prevention**: Tests script tag sanitization
- **SQL Injection**: Tests database query sanitization
- **Path Traversal**: Tests file access security
- **Input Validation**: Tests all user input points
- **Log Sanitization**: Tests sensitive data removal

## Performance Testing

Performance tests ensure SIGMA-NEX maintains efficiency:

- **Memory Management**: Tests history deque limits
- **Response Times**: Measures query processing times
- **Resource Cleanup**: Tests temporary file management
- **Concurrent Requests**: Tests server load handling

## Continuous Integration

The test suite is designed for CI/CD integration:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    pip install -e ".[dev]"
    pytest --cov=sigma_nex --cov-report=xml
    
- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Coverage Goals

- **Minimum Coverage**: 80% overall
- **Critical Modules**: 90% coverage
  - `sigma_nex.config`
  - `sigma_nex.utils.validation`
  - `sigma_nex.core.runner`
- **Security Functions**: 100% coverage

## Writing New Tests

When adding new functionality:

1. **Create corresponding test file**: `test_[module_name].py`
2. **Follow naming conventions**: `test_[function_name]_[scenario]`
3. **Use appropriate markers**: `@pytest.mark.unit`, `@pytest.mark.integration`
4. **Mock external dependencies**: Use `unittest.mock` or `pytest-mock`
5. **Test error conditions**: Include negative test cases
6. **Update fixtures**: Add new test data to `conftest.py` if needed

## Debugging Tests

```powershell
# Run tests with debugger integration
pytest --pdb

# Run tests with detailed output
pytest -vvv --tb=long

# Run only failed tests from last run
pytest --lf

# Run tests matching pattern
pytest -k "test_config"

# Run tests with specific marker
pytest -m "unit"
```

## Test Data Management

Test data is automatically created and cleaned up:
- Temporary directories are created for each test
- Mock data files are generated as needed
- Cleanup happens automatically after test completion
- No manual test data management required

## Best Practices

1. **Isolation**: Each test should be independent
2. **Speed**: Unit tests should run quickly
3. **Clarity**: Test names should describe the scenario
4. **Coverage**: Aim for high code coverage
5. **Maintenance**: Keep tests updated with code changes
6. **Documentation**: Document complex test scenarios

## Troubleshooting

### Common Issues

**Import Errors**: Ensure project is installed in development mode:
```powershell
pip install -e .
```

**Missing Dependencies**: Install test requirements:
```powershell
pip install -r requirements-test.txt
```

**Path Issues**: Tests automatically handle path resolution using fixtures.

**Mock Failures**: Verify mock patches match actual import paths.

### Getting Help

- Check test output for detailed error messages
- Use `pytest --tb=long` for full tracebacks
- Verify test data in temporary directories
- Review fixture setup in `conftest.py`

The testing infrastructure ensures SIGMA-NEX maintains high quality standards while enabling confident development and deployment.