import pytest

from datawarehouse_mcp.exceptions import DataWarehouseAPIError
from datawarehouse_mcp.server import (
    get_all_indicators_for_dataflow,
    get_available_dataflows,
    get_data_for_dataflow,
)


class TestGetAvailableDataflows:
    """Test suite for get_available_dataflows tool."""

    def test_get_available_dataflows_success(self) -> None:
        """Test successful retrieval of available dataflows."""
        result = get_available_dataflows()

        assert result.get("available_dataflows", None) is not None
        assert result.get("input_arguments", None) == {}


class TestGetAllIndicatorsForDataflow:
    """Test suite for get_all_indicators_for_dataflow tool."""

    def test_get_all_indicators_success(self) -> None:
        """Test successful retrieval of indicators for a dataflow."""
        dataflow_id = "GENDER"
        expected_indicators = {
            "GN_PTNTY_LV_BNFTS": "Paternity leave benefits",
            "GN_MTNTY_LV_BNFTS": "Maternity leave benefits",
            "GN_LF_PTCPN": "Labour force participation rate",
            "GN_UNMPLY": "Labour force unemployment rate",
            "GN_IDX": "Social Institutions and Gender Index (SIGI)",
            "GN_ED_ATTN": "Educational attainment of the population (aged 25 years and older)",
            "GN_IT_MOB_OWN": "Proportion of individuals who own a mobile telephone",
            "GN_FB_BNK_ACCSS": (
                "Proportion of adolescents and adults (aged 15 years and older) "
                "with an account at a financial institution or mobile money service provider"
            ),
            "GN_TIMEUSE": "Time use",
            "GN_SG_LGL_GENEQEMP": (
                "Legal frameworks that promote, enforce, and monitor gender equality- "
                "Area 3: Employment and economic benefits"
            ),
        }

        result = get_all_indicators_for_dataflow(dataflow_id)

        assert result.get("all_indicators", None) is not None
        assert result.get("input_arguments", None) == {"dataflow_id": dataflow_id}
        assert result.get("all_indicators") == expected_indicators

    def test_get_all_indicators_empty_dataflow_id(self) -> None:
        """Test handling of empty dataflow ID."""
        dataflow_id = ""

        with pytest.raises(DataWarehouseAPIError):
            get_all_indicators_for_dataflow(dataflow_id)


class TestGetDataForDataflow:
    """Test suite for get_data_for_dataflow tool."""

    def test_get_data_success_with_year(self) -> None:
        """Test successful data retrieval with year specified."""
        dataflow_id = "DM"
        ref_areas = "URY"
        indicators = "DM_BRTS"
        year = 2020
        expected_result = (
            "TIME_PERIODREF_AREAINDICATORRESIDENCESEXAGEOBS_STATUSOBS_CONFCOVERAGE_TIME"
            "FREQ_COLLTIME_PERIOD_METHODDATA_SOURCEUNIT_MEASUREUNIT_MULTIPLIERSOURCE_LINK"
            "SERIES_FOOTNOTEOBS_FOOTNOTEOBS_VALUE702020URYDM_BRTS_T_T_TPREDNoneNoneNoneNone"
            "UnitedNations,DepartmentofEconomicandSocial Affairs, Population Division (2024). "
            "World Population Prospects 2024.PS3https://population.un.org/wpp/NoneNone35.383"
        )
        result = get_data_for_dataflow(dataflow_id, ref_areas, indicators, year)
        result["data"] = result["data"].replace("\n", "").replace(" ", "")
        assert result == {
            "data": str(expected_result).replace("\n", "").replace(" ", ""),
            "input_arguments": {
                "dataflow_id": dataflow_id,
                "ref_areas": ref_areas,
                "indicators": indicators,
                "year": str(year),
            },
        }

    def test_get_data_api_error(self) -> None:
        """Test handling of API errors during data retrieval."""
        dataflow_id = "INVALID"
        ref_areas = "XXX"
        indicators = "INVALID_IND"

        with pytest.raises(DataWarehouseAPIError):
            get_data_for_dataflow(dataflow_id, ref_areas, indicators)
