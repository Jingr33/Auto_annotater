# Test Suite

This directory contains the comprehensive test suite for the Auto Annotater application.

## Structure

```
tests/
├── unit/                    # Unit tests for individual modules
│   ├── test_bbox_annotation.py
│   ├── test_polygon_annotation.py
│   ├── test_annotation_parser.py
│   ├── test_enums.py
│   ├── test_configs.py
│   ├── test_dataset_validator.py
│   ├── test_data_manager.py
│   ├── test_frame_dto.py
│   ├── test_errors.py
│   ├── test_registry.py
│   └── test_cli_argument_parser.py
├── integration/             # Integration tests for module interactions
│   ├── testDataManagerIntegration.py
│   ├── test_pipeline_manager.py
│   └── test_api.py
├── e2e/                     # End-to-end tests for full workflows
│   ├── test_dataset_workflow.py
│   └── test_full_pipeline.py
├── fixtures/                # Test fixtures and shared data
├── conftest.py              # Pytest fixtures and configuration
└── README.md                # This file
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# E2E tests only
pytest tests/e2e/
```

### Run specific test files
```bash
pytest tests/unit/test_bbox_annotation.py
```

### Run tests with markers
```bash
# Run only slow tests
pytest -m slow

# Run only integration tests
pytest -m integration

# Run only e2e tests
pytest -m e2e
```

### Run tests with verbose output
```bash
pytest -v
```

### Run tests and show coverage
```bash
pytest --cov=src/backend
```

## Test Categories

### Unit Tests
- Test individual classes and functions in isolation
- Fast execution, no external dependencies
- Mock external dependencies when necessary

### Integration Tests
- Test interactions between multiple modules
- Test API endpoints and database operations
- May require temporary directories for file operations

### E2E Tests
- Test complete user workflows
- May require external resources (models, servers)
- Some tests are marked with `@pytest.mark.skip` if they require external dependencies

## Writing Tests

### Test File Naming
- Test files should be named `test_<module_name>.py`
- Test functions should be named `test_<description>.py`

### Test Function Naming
- Test functions should be named `test_<what_is_being_tested>`
- Use descriptive names that explain the test purpose

### Fixtures
- Use pytest fixtures for common setup/teardown
- Fixtures are defined in `conftest.py`
- Use `@pytest.fixture` decorator

### Assertions
- Use plain `assert` statements
- pytest provides detailed assertion failure messages

### Markers
- Use `@pytest.mark.slow` for slow tests
- Use `@pytest.mark.integration` for integration tests
- Use `@pytest.mark.e2e` for end-to-end tests
- Use `@pytest.mark.skip(reason="...")` to skip tests

## Dependencies

- pytest
- pytest-asyncio (for async tests)
- pytest-cov (for coverage reports)

Install test dependencies:
```bash
pip install pytest pytest-asyncio pytest-cov
```
