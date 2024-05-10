from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from coola import objects_are_equal
from pandas.testing import assert_frame_equal

from flamme.analyzer import ColumnTemporalNullValueAnalyzer
from flamme.section import ColumnTemporalNullValueSection, EmptySection

#####################################################
#     Tests for ColumnTemporalNullValueAnalyzer     #
#####################################################


def test_column_temporal_null_value_analyzer_str() -> None:
    assert str(
        ColumnTemporalNullValueAnalyzer(column="col", dt_column="datetime", period="M")
    ).startswith("ColumnTemporalNullValueAnalyzer(")


def test_column_temporal_null_value_analyzer_frame() -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(
        pd.DataFrame(
            {
                "col": np.array([1.2, 4.2, np.nan, 2.2]),
                "datetime": pd.to_datetime(
                    ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
                ),
            }
        )
    )
    assert_frame_equal(
        section.frame,
        pd.DataFrame(
            {
                "col": np.array([1.2, 4.2, np.nan, 2.2]),
                "datetime": pd.to_datetime(
                    ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
                ),
            }
        ),
    )


@pytest.mark.parametrize("column", ["col1", "col2"])
def test_column_temporal_null_value_analyzer_column(column: str) -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column=column, dt_column="datetime", period="M"
    ).analyze(
        pd.DataFrame(
            {
                "col1": np.array([1.2, 4.2, np.nan, 2.2]),
                "col2": np.array([1, 2, 3, 4]),
                "datetime": pd.to_datetime(
                    ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
                ),
            }
        )
    )
    assert section.column == column


@pytest.mark.parametrize("dt_column", ["datetime", "date"])
def test_column_temporal_null_value_analyzer_dt_column(dt_column: str) -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column="col", dt_column=dt_column, period="M"
    ).analyze(
        pd.DataFrame(
            {
                "col": np.array([1.2, 4.2, np.nan, 2.2]),
                "datetime": pd.to_datetime(
                    ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
                ),
                "date": pd.to_datetime(["2021-01-03", "2021-02-03", "2021-03-03", "2021-04-03"]),
            }
        )
    )
    assert section.dt_column == dt_column


@pytest.mark.parametrize("period", ["M", "D"])
def test_column_temporal_null_value_analyzer_period(period: str) -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column="col", dt_column="datetime", period=period
    ).analyze(
        pd.DataFrame(
            {
                "col": np.array([1.2, 4.2, np.nan, 2.2]),
                "datetime": pd.to_datetime(
                    ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
                ),
            }
        )
    )
    assert section.period == period


@pytest.mark.parametrize("figsize", [(7, 3), (1.5, 1.5)])
def test_column_temporal_null_value_analyzer_figsize(figsize: tuple[int, int]) -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column="col", dt_column="datetime", period="M", figsize=figsize
    ).analyze(
        pd.DataFrame(
            {
                "col": np.array([1.2, 4.2, np.nan, 2.2]),
                "datetime": pd.to_datetime(
                    ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
                ),
            }
        )
    )
    assert section.figsize == figsize


def test_column_temporal_null_value_analyzer_figsize_default() -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(
        pd.DataFrame(
            {
                "col": np.array([1.2, 4.2, np.nan, 2.2]),
                "datetime": pd.to_datetime(
                    ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
                ),
            }
        )
    )
    assert section.figsize is None


def test_column_temporal_null_value_analyzer_get_statistics() -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(
        pd.DataFrame(
            {
                "col": np.array([1.2, 4.2, np.nan, 2.2]),
                "datetime": pd.to_datetime(
                    ["2020-01-03", "2020-02-03", "2020-03-03", "2020-04-03"]
                ),
            }
        )
    )
    assert isinstance(section, ColumnTemporalNullValueSection)
    assert objects_are_equal(section.get_statistics(), {})


def test_column_temporal_null_value_analyzer_get_statistics_empty_rows() -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(pd.DataFrame({"col": [], "datetime": []}))
    assert isinstance(section, ColumnTemporalNullValueSection)
    assert objects_are_equal(section.get_statistics(), {})


def test_column_temporal_null_value_analyzer_get_statistics_missing_column() -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(pd.DataFrame({}))
    assert isinstance(section, EmptySection)
    assert objects_are_equal(section.get_statistics(), {})


def test_column_temporal_null_value_analyzer_get_statistics_missing_dt_column() -> None:
    section = ColumnTemporalNullValueAnalyzer(
        column="col", dt_column="datetime", period="M"
    ).analyze(pd.DataFrame({"col": []}))
    assert isinstance(section, EmptySection)
    assert objects_are_equal(section.get_statistics(), {})
