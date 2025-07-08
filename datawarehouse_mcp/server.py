from typing import Any

from config import config
from exceptions import DataWarehouseAPIError
from handlers import (
    handle_get_all_indicators_for_dataflow,
    handle_get_available_dataflows,
    handle_get_data_for_dataflow,
)
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Data Warehouse MCP", host=config.server.host, port=config.server.port)

from logging_config import get_logger  # noqa: E402

logger = get_logger(__name__)


@mcp.tool()
def get_available_dataflows() -> dict[str, str | dict[str, Any]]:
    """Get the available dataflows and their descriptions.

    Returns:
        Dictionary containing available dataflows and input arguments.
    """
    logger.info("Getting available dataflows")
    available_dataflows = handle_get_available_dataflows()
    logger.info("Returning available dataflows")
    return {
        "available_dataflows": available_dataflows,
        "input_arguments": {},
    }


@mcp.tool()
def get_all_indicators_for_dataflow(
    dataflow_id: str,
) -> dict[str, str | dict[str, str]]:
    """Get all indicators for the dataflow.

    Args:
        dataflow_id: Dataflow ID to get indicators for

    Returns:
        Dictionary containing indicators info and input arguments.
    """
    logger.info("Getting all indicators for dataflow %s", dataflow_id)
    if dataflow_id == "":
        msg = "Dataflow ID is required"
        logger.error(msg)
        raise DataWarehouseAPIError(msg)

    indicators_info = handle_get_all_indicators_for_dataflow(dataflow_id)
    logger.info("Returning indicators info for dataflow %s", dataflow_id)
    return {
        "all_indicators": indicators_info,
        "input_arguments": {"dataflow_id": dataflow_id},
    }


@mcp.tool()
def get_data_for_dataflow(
    dataflow_id: str,
    ref_areas: str,
    indicators: str,
    year: int | None = None,
) -> dict[str, str | dict[str, str]]:
    """Get data for a specific dataflow.

    Returns all available data that matches the criteria.
    If the year is not found, it will return all data for that country and indicator.

    Args:
        dataflow_id: Dataflow ID to get data for
        ref_areas: Plus-separated string of ISO-3 codes to filter by.
        indicators: Plus-separated string of indicator codes to retrieve.
        year: The year of the data to retrieve.

    Returns:
        Dictionary containing data and input arguments.
    """
    logger.info("Getting data for dataflow %s", dataflow_id)
    if dataflow_id == "":
        msg = "Dataflow ID is required"
        logger.error(msg)
        raise DataWarehouseAPIError(msg)

    data = handle_get_data_for_dataflow(
        dataflow_id=dataflow_id,
        ref_areas=ref_areas,
        indicators=indicators,
        year=year,
    )
    logger.info("Returning data for dataflow %s", dataflow_id)
    return {
        "data": data.to_string(max_rows=None, max_cols=None),  # type: ignore[misc]
        "input_arguments": {
            "dataflow_id": dataflow_id,
            "ref_areas": ref_areas,
            "indicators": indicators,
            "year": str(year) if year is not None else "",
        },
    }


if __name__ == "__main__":
    logger.info("🚀 Starting server... ")

    logger.info(
        'Check "http://localhost:%s/%s" for the server status',
        config.server.port,
        config.server.transport,
    )

    mcp.run(config.server.transport)
