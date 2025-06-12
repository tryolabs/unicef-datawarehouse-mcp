from typing import Any

import pandas as pd


def build_df_from_json(json_data: dict[str, Any]) -> pd.DataFrame:
    """Build a CSV DataFrame from SDMX-JSON data.

    Args:
        json_data: JSON data from API response

    Returns:
        DataFrame containing the requested data
    """
    data_structure = json_data["structure"]

    # Get dimension and attribute definitions upfront
    dimensions = {
        "observation": [d["id"] for d in data_structure["dimensions"]["observation"]],
        "series": [d["id"] for d in data_structure["dimensions"]["series"]],
    }
    attributes = {
        "observation": [a["id"] for a in data_structure["attributes"]["observation"]],
        "series": [a["id"] for a in data_structure["attributes"]["series"]],
    }

    # Create lookup dictionaries for faster value retrieval
    value_lookups = {
        ("dimensions", "observation"): {
            (i, val_pos): val["id"]
            for i, dim in enumerate(data_structure["dimensions"]["observation"])
            for val_pos, val in enumerate(dim["values"])
        },
        ("dimensions", "series"): {
            (i, val_pos): val["id"]
            for i, dim in enumerate(data_structure["dimensions"]["series"])
            for val_pos, val in enumerate(dim["values"])
        },
        ("attributes", "observation"): {
            (i, val_pos): val["id"]
            for i, attr in enumerate(data_structure["attributes"]["observation"])
            for val_pos, val in enumerate(attr["values"])
        },
        ("attributes", "series"): {
            (i, val_pos): val["id"]
            for i, attr in enumerate(data_structure["attributes"]["series"])
            for val_pos, val in enumerate(attr["values"])
        },
    }
    data = json_data["dataSets"][0]["series"]
    # Process all series at once using list comprehension
    rows = [
        (
            # Observation dimensions
            get_values(
                [int(x) for x in obs_dims.split(":")],
                "dimensions",
                "observation",
                value_lookups,
            )
            + [None] * (len(dimensions["observation"]) - len(obs_dims.split(":")))
            +
            # Series dimensions
            get_values(
                [int(x) for x in series_id.split(":")],
                "dimensions",
                "series",
                value_lookups,
            )
            + [None] * (len(dimensions["series"]) - len(series_id.split(":")))
            +
            # Observation attributes
            get_values(obs_attrs[1:], "attributes", "observation", value_lookups)
            +
            # Series attributes
            get_values(series_data["attributes"], "attributes", "series", value_lookups)
            + [None] * (len(attributes["series"]) - len(series_data["attributes"]))
            +
            # Observation value
            [obs_attrs[0]]
        )
        for series_id, series_data in data.items()
        if "observations" in series_data and "attributes" in series_data
        for obs_dims, obs_attrs in series_data["observations"].items()
    ]

    column_names = (
        dimensions["observation"]
        + dimensions["series"]
        + attributes["observation"]
        + attributes["series"]
        + ["OBS_VALUE"]
    )

    return pd.DataFrame(rows, columns=column_names)


def get_values(
    ids: list[int],
    structure_type: str,
    dimension_type: str,
    value_lookups: dict[tuple[str, str], dict[tuple[int, int], str]],
) -> list[str | None]:
    """Get values from lookup dictionary based on IDs and structure type.

    Args:
        ids: List of integer IDs to look up
        structure_type: Type of structure ('dimensions' or 'attributes')
        dimension_type: Type of dimension ('observation' or 'series')
        value_lookups: Dictionary containing lookup mappings

    Returns:
        List of values corresponding to the provided IDs
    """
    lookup = value_lookups[(structure_type, dimension_type)]
    return [lookup.get((i, id_val)) for i, id_val in enumerate(ids)]
