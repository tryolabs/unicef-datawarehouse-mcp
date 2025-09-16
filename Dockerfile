FROM python:3.11-slim

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy the application code
COPY datawarehouse_mcp/ ./datawarehouse_mcp/


# Create a non-root user
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port (matches config.yaml)
EXPOSE 6000

# Health check (SSE endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:6000/sse', timeout=5)"

CMD ["uv", "run", "datawarehouse_mcp/server.py"]