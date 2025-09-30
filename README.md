# UNICEF Data Warehouse MCP Server

The UNICEF Data Warehouse MCP Server provides access to UNICEF's comprehensive statistical data repository through a Model Context Protocol (MCP) interface. This server enables natural language queries against UNICEF's vast collection of indicators covering child welfare, education, health, nutrition, and development metrics worldwide.

## Overview

This MCP server serves as the statistical data backend for the UNICEF Geosphere project, providing access to:

- **UNICEF Indicators**: Child mortality, education access, nutrition status, health coverage
- **Country Statistics**: Data for 195+ countries and territories
- **Time Series Data**: Historical trends spanning multiple decades
- **Disaggregated Data**: Breakdowns by age, gender, location, and socioeconomic status
- **Real-time Access**: Direct integration with UNICEF's data warehouse via SDMX protocol

## Features

### Core Capabilities

- **Dataflow Discovery**: Browse available statistical datasets and indicators
- **Indicator Querying**: Get detailed information about specific indicators
- **Filtered Data Retrieval**: Query data with country, time, and indicator filters
- **SDMX Integration**: Standards-compliant statistical data exchange
- **Metadata Access**: Rich descriptions of datasets, methodologies, and sources

### Statistical Coverage

- **Child Health**: Mortality rates, immunization coverage, malnutrition indicators
- **Education**: School enrollment, literacy rates, educational attainment
- **Child Protection**: Birth registration, child labor, violence against children
- **Water & Sanitation**: Access to clean water, sanitation facilities
- **Social Protection**: Cash transfers, social services coverage
- **Emergency Response**: Humanitarian indicators and crisis response metrics

## Technology Stack

- **FastMCP**: Model Context Protocol server framework
- **SDMX**: Statistical Data and Metadata eXchange standard
- **Pandas**: Data manipulation and analysis
- **Requests**: HTTP client for SDMX API integration

## Project Structure

```
datawarehouse_mcp/
├── server.py            # MCP server and tool definitions
├── handlers.py          # Tool implementation and data processing
├── sdmx_parser.py       # SDMX protocol parser and client
├── config.py            # Configuration and settings management
├── schemas.py           # Dataclasses-based models and types
├── constants.py         # Application constants
├── config.yaml          # Server configuration
├── logging_config.py    # Logging setup
├── dataflows.json       # Curated list of available dataflows
└── exceptions.py        # Custom exception definitions
```

## Installation

### Dependencies

```bash
# Install dependencies using uv
uv sync
```

## Configuration

The server requires minimal configuration as it connects to UNICEF's public SDMX endpoints.

### Server configuration

**`datawarehouse_mcp/config.yaml`**:

```yaml
server:
  host: "0.0.0.0" # Server bind address
  port: 6000 # Internal MCP port
  transport: "sse" # MCP transport protocol
```

The server is reachable only on the internal Docker network. The agent connects via `datawarehouse_mcp:6000/sse`.

## Available Tools

The MCP server exposes 3 primary tools for statistical data access:

### 1. Dataflow Discovery

#### `get_available_dataflows()`

Returns information about some available statistical datasets (dataflows).
Currently, not all dataflows in the Data Warehouse are available through the MCP server.

**Returns**: Dictionary containing:

- `available_dataflows`: Formatted string listing dataflow IDs with descriptions
- `input_arguments`: Empty (no parameters required)

### 2. Indicator Discovery

#### `get_all_indicators_for_dataflow(dataflow_id: str)`

Retrieves all available indicators for a specific dataflow.

**Parameters**:

- `dataflow_id` (required): Dataflow identifier from available dataflows

**Returns**: Dictionary containing:

- `all_indicators`: Dictionary mapping indicator codes to their names
- `input_arguments`: {"dataflow_id": dataflow_id}

### 3. Data Retrieval

#### `get_data_for_dataflow(dataflow_id: str, ref_areas: str, indicators: str, year: int | None = None)`

Queries specific data from the dataflow with filters.

**Parameters**:

- `dataflow_id` (required): Dataflow identifier
- `ref_areas` (required): Plus-separated ISO 3-letter country codes (e.g., "COL+ETH+URY" or "URY")
- `indicators` (required): Plus-separated indicator codes (e.g., "DM_BRTS+DM_DEATHS")
- `year` (optional): Year filter (e.g., 2020)

**Returns**: Dictionary containing:

- `data`: String representation of the resulting table
- `input_arguments`: Echo of the input parameters used

## Development

### Running the Server

```bash
# Development mode
mcp dev datawarehouse_mcp/server.py

# Production mode
uv run datawarehouse_mcp/server.py
```

### Testing

```bash
# Run all tests
uv run pytest

# Run specific tests
uv run pytest tests/test_server.py -v
```

### Development Setup

1. **Clone repository**
2. **Install dependencies**: `uv sync`
3. **Configure test environment**
4. **Run tests to verify SDMX connectivity**

## SDMX Integration

The server implements the SDMX (Statistical Data and Metadata eXchange) standard for accessing UNICEF's data warehouse:

### SDMX Limitations

- **Rate Limiting**: UNICEF SDMX API has usage limits
- **Data Freshness**: Indicators updated at different frequencies
- **Coverage Gaps**: Not all indicators available for all countries
- **Historical Data**: Some indicators have limited historical coverage

## Security

### Data Security

- **Public data**: All UNICEF indicators are publicly available
- **No service secrets**: This service requires no secrets or credentials to run
- **No authentication to SDMX**: SDMX endpoints used are public
- **Input Validation**: All parameters validated before SDMX requests
- **Client-side rate limiting**: Not implemented; adhere to API limits

## Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8 and use type hints
2. **Testing**: Add tests for new SDMX functionality
3. **Documentation**: Update tool descriptions and examples

### Adding New Tools

1. **Define tool** in `server.py` with `@mcp.tool()` decorator
2. **Implement handler** in `handlers.py`
3. **Add SDMX logic** in `sdmx_parser.py` if needed
4. **Write tests** in `tests/test_handlers.py`
5. **Update documentation** in README

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Submit issues on GitHub repository
- **SDMX Documentation**: [SDMX Official Specification](https://sdmx.org/)
- **UNICEF Data**: [UNICEF Data Portal](https://data.unicef.org/)
- **Technical Support**: Repository maintainers
