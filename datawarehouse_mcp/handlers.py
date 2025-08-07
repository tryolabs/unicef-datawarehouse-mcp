import urllib.parse
from logging import getLogger

import pandas as pd
import requests
from constants import BASE_URL
from exceptions import DataWarehouseAPIError
from sdmx_parser import build_df_from_json

logger = getLogger(__name__)


def handle_get_available_dataflows() -> str:
    """Get information about available dataflows.

    Returns:
        String containing descriptions of available dataflows and their purposes
    """
    info_on_dataflows = """
    - CCRI: Climate Risk Index - Hazards, health risks, vulnerability factors
    - CHLD_PVTY: Child Poverty - Measures poverty levels, deprivation rates, income ratios, etc.
    - CME: Child Mortality - Tracks mortality rates and deaths across age groups 0-24 years
    - CME_CAUSE_OF_DEATH: Child Mortality by Cause of Death
    - DM: Demography - Population statistics, age groups, fertility, life expectancy, etc.
    - EDUCATION: Education data like literacy rates, completion rates, out-of-school rates, etc.
    - HIV_AIDS: HIV prevention, treatment and transmission stats
    - IMMUNISATION: Vaccination coverage rates for BCG, DTP, polio, measles and other key vaccines
    - NUTRITION: Key nutrition indicators like stunting, wasting, breastfeeding, anemia and diet
    - PT_CM: Child Marriage, tracks early marriage rates, related outcomes and socioeconomic factors
    """
    return info_on_dataflows


def handle_get_all_indicators_for_dataflow(dataflow_id: str) -> dict[str, str]:
    """Get information on indicators for a specific dataflow.

    Args:
        dataflow_id: Dataflow ID to get indicators information for

    Returns:
        Dictionary mapping indicator IDs to their names
    """
    logger.info("Getting indicators info for dataflow %s", dataflow_id)
    try:
        url = urllib.parse.urljoin(BASE_URL, f"data/{dataflow_id}/All?format=sdmx-json")
        data = requests.get(url, timeout=200).json()
        data_structure = data["data"]["structure"]
        indicators_info = {
            val["id"]: val["name"]
            for i, attr in enumerate(data_structure["dimensions"]["series"])
            for _, val in enumerate(attr["values"])
            if i == 1
        }

    except (requests.RequestException, ValueError, KeyError) as e:
        logger.exception("Error getting indicators info for dataflow %s", dataflow_id)
        raise DataWarehouseAPIError(str(e)) from e

    logger.info("Returning indicators info for dataflow %s", dataflow_id)
    return indicators_info


def handle_get_data_for_dataflow(
    dataflow_id: str,
    ref_areas: str,
    indicators: str,
    year: int | None = None,
) -> pd.DataFrame:
    """Get data for a specific dataflow.

    Returns all available data that matches the criteria.
    If the year is not found, it will return all data for that country and indicator.

    Args:
        dataflow_id: Dataflow ID to get data for
        ref_areas: Plus-separated string of ISO-3 codes to filter by.
        indicators: Plus-separated string of indicator codes to retrieve.
        year: The year of the data to retrieve.

    Returns:
        pd.DataFrame: DataFrame containing the requested data
    """
    logger.info("Getting data for dataflow %s", dataflow_id)
    try:
        url = urllib.parse.urljoin(
            BASE_URL,
            f"data/{dataflow_id}/{ref_areas}.{indicators}?format=sdmx-json",
        )

        data = requests.get(url, timeout=200).json()

        if "errors" in data:
            logger.error("Error getting data for dataflow %s", dataflow_id)
            raise DataWarehouseAPIError(str(data["errors"]))

        data = build_df_from_json(data["data"])
    except (requests.RequestException, ValueError, KeyError) as e:
        logger.exception("Error getting data for dataflow %s", dataflow_id)
        raise DataWarehouseAPIError(str(e)) from e

    if year is not None and str(year) in data["TIME_PERIOD"].unique():
        logger.info("Filtering data for year %s", year)
        data = data[data["TIME_PERIOD"] == str(year)]

    return data
