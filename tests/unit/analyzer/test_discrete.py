from __future__ import annotations

import numpy as np
import pandas as pd
from coola import objects_are_equal
from pandas import DataFrame
from pytest import fixture

from flamme.analyzer import (
    DiscreteDistributionAnalyzer,
    TemporalDiscreteDistributionAnalyzer,
)
from flamme.section import (
    DiscreteDistributionSection,
    EmptySection,
    TemporalDiscreteDistributionSection,
)

##################################################
#     Tests for DiscreteDistributionAnalyzer     #
##################################################


def test_discrete_distribution_analyzer_str() -> None:
    assert str(DiscreteDistributionAnalyzer(column="col")).startswith(
        "DiscreteDistributionAnalyzer("
    )


def test_discrete_distribution_analyzer_get_statistics() -> None:
    section = DiscreteDistributionAnalyzer(column="int").analyze(
        DataFrame(
            {
                "float": np.array([1.2, 4.2, np.nan, 2.2]),
                "int": np.array([np.nan, 1, 0, 1]),
                "str": np.array(["A", "B", None, np.nan]),
            }
        )
    )
    assert isinstance(section, DiscreteDistributionSection)
    stats = section.get_statistics()
    assert stats["nunique"] == 3
    assert stats["total"] == 4


def test_discrete_distribution_analyzer_get_statistics_dropna_true() -> None:
    section = DiscreteDistributionAnalyzer(column="int", dropna=True).analyze(
        DataFrame(
            {
                "float": np.array([1.2, 4.2, np.nan, 2.2]),
                "int": np.array([np.nan, 1, 0, 1]),
                "str": np.array(["A", "B", None, np.nan]),
            }
        )
    )
    assert isinstance(section, DiscreteDistributionSection)
    assert objects_are_equal(
        section.get_statistics(),
        {"most_common": [(1.0, 2), (0.0, 1)], "nunique": 2, "total": 3},
    )


def test_discrete_distribution_analyzer_get_statistics_empty_no_row() -> None:
    section = DiscreteDistributionAnalyzer(column="int").analyze(
        DataFrame({"float": np.array([]), "int": np.array([]), "str": np.array([])})
    )
    assert isinstance(section, DiscreteDistributionSection)
    assert objects_are_equal(
        section.get_statistics(), {"most_common": [], "nunique": 0, "total": 0}
    )


def test_discrete_distribution_analyzer_get_statistics_empty_no_column() -> None:
    section = DiscreteDistributionAnalyzer(column="col").analyze(DataFrame({}))
    assert isinstance(section, EmptySection)
    assert objects_are_equal(section.get_statistics(), {})


##########################################################
#     Tests for TemporalDiscreteDistributionAnalyzer     #
##########################################################


@fixture
def dataframe() -> DataFrame:
    return DataFrame(
        {
            "col": np.array([1, 42, np.nan, 22]),
            "datetime": pd.to_datetime(["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]),
        }
    )


def test_temporal_discrete_distribution_analyzer_str() -> None:
    assert str(
        TemporalDiscreteDistributionAnalyzer(column="col", dt_column="datetime", period="M")
    ).startswith("TemporalDiscreteDistributionAnalyzer(")


def test_temporal_discrete_distribution_analyzer_column(dataframe: DataFrame) -> None:
    section = TemporalDiscreteDistributionAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(dataframe)
    assert isinstance(section, TemporalDiscreteDistributionSection)
    assert section.column == "col"


def test_temporal_discrete_distribution_analyzer_dt_column(dataframe: DataFrame) -> None:
    section = TemporalDiscreteDistributionAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(dataframe)
    assert isinstance(section, TemporalDiscreteDistributionSection)
    assert section.dt_column == "datetime"


def test_temporal_discrete_distribution_analyzer_period(dataframe: DataFrame) -> None:
    section = TemporalDiscreteDistributionAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(dataframe)
    assert isinstance(section, TemporalDiscreteDistributionSection)
    assert section.period == "M"


def test_temporal_discrete_distribution_analyzer_get_statistics(dataframe: DataFrame) -> None:
    section = TemporalDiscreteDistributionAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(dataframe)
    assert isinstance(section, TemporalDiscreteDistributionSection)
    assert objects_are_equal(section.get_statistics(), {})


def test_temporal_discrete_distribution_analyzer_get_statistics_empty() -> None:
    section = TemporalDiscreteDistributionAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(DataFrame({"col": [], "int": [], "str": [], "datetime": []}))
    assert isinstance(section, TemporalDiscreteDistributionSection)
    assert objects_are_equal(section.get_statistics(), {})


def test_temporal_discrete_distribution_analyzer_get_statistics_missing_column() -> None:
    section = TemporalDiscreteDistributionAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(DataFrame({"datetime": []}))
    assert isinstance(section, EmptySection)
    assert objects_are_equal(section.get_statistics(), {})


def test_temporal_discrete_distribution_analyzer_get_statistics_missing_dt_column() -> None:
    section = TemporalDiscreteDistributionAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(DataFrame({"col": []}))
    assert isinstance(section, EmptySection)
    assert objects_are_equal(section.get_statistics(), {})
