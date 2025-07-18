# Tests Documentation

## Overview

The UNICEF Datawarehouse MCP project contains unit tests to ensure the reliability of MCP server functions for accessing and querying dataflow information from external data sources.

## Test Structure

### Test Files

- **`test_server.py`** - Tests MCP server functions for dataflow operations
- **`test_logger.py`** - Tests logging configuration and setup

### Test Categories

#### Unit Tests

- **Server Function Tests**: Testing dataflow retrieval, indicator queries, and data access
- **API Integration Tests**: Testing external API calls and data parsing
- **Error Handling Tests**: Testing exception handling and error responses

## Key Test Coverage

- ✅ `get_available_dataflows()` - Retrieves list of available dataflows
- ✅ `get_all_indicators_for_dataflow()` - Gets indicators for specific dataflow (e.g., GENDER dataflow)
- ✅ `get_data_for_dataflow()` - Retrieves actual data for dataflows
- ✅ Error handling for invalid dataflow IDs
- ✅ Logging configuration and setup
- ✅ Response format validation

## Running Tests

### Prerequisites

```bash
# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

### Run All Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=datawarehouse_mcp --cov-report=html

# Run specific test file
uv run pytest tests/test_server.py

# Run specific test class
uv run pytest tests/test_server.py::TestGetAvailableDataflows

# Run with verbose output
uv run pytest -v
```

## Test Configuration

Tests are configured via `pyproject.toml`:

- Test path: `tests/`
- Python path includes: `[".", "datawarehouse_mcp"]`
- Coverage excludes test files and `__init__.py`

## Notes

- Tests interact with real external APIs, so network connectivity is required
- Some tests validate against expected data structures that may change over time
- Error handling tests ensure graceful degradation when APIs are unavailable
