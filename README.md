# UNICEF Data Warehouse MCP

This is the project for the MCP server for the UNICEF Data Warehouse.

## Development

### Dependencies

Dependencies are managed with [uv](https://docs.astral.sh/uv/).

To install the dependencies, run:

```bash
uv sync
```

### Running the server

To run the server, run:

```bash
mcp dev datawarehouse_mcp/server.py
```

### Running the tests

To run the tests, run:

```bash
uv run tests/test_server.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
