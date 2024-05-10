from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from coola import objects_are_allclose
from jinja2 import Template

from flamme.section import DataFrameSummarySection
from flamme.section.frame_summary import prepare_type_name

NoneType = type(None)


@pytest.fixture()
def dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "col1": np.array([1.2, 4.2, np.nan, 2.2, 1, 2.2]),
            "col2": np.array([1, 1, 0, 1, 1, 1]),
            "col3": np.array(["A", "B", None, np.nan, "C", "B"]),
        }
    )


def test_dataframe_summary_section_frame(dataframe: pd.DataFrame) -> None:
    assert DataFrameSummarySection(dataframe).frame is dataframe


@pytest.mark.parametrize("top", [0, 1, 2])
def test_dataframe_summary_section_top(dataframe: pd.DataFrame, top: int) -> None:
    assert DataFrameSummarySection(dataframe, top=top).top == top


def test_dataframe_summary_section_top_incorrect(dataframe: pd.DataFrame) -> None:
    with pytest.raises(ValueError, match=r"Incorrect top value \(-1\). top must be positive"):
        DataFrameSummarySection(dataframe, top=-1)


def test_dataframe_summary_section_get_columns(dataframe: pd.DataFrame) -> None:
    assert DataFrameSummarySection(dataframe).get_columns() == ("col1", "col2", "col3")


def test_dataframe_summary_section_get_columns_empty() -> None:
    assert DataFrameSummarySection(pd.DataFrame({})).get_columns() == ()


def test_dataframe_summary_section_get_null_count(dataframe: pd.DataFrame) -> None:
    assert DataFrameSummarySection(dataframe).get_null_count() == (1, 0, 2)


def test_dataframe_summary_section_get_null_count_empty() -> None:
    assert DataFrameSummarySection(pd.DataFrame({})).get_null_count() == ()


def test_dataframe_summary_section_get_nunique(dataframe: pd.DataFrame) -> None:
    assert DataFrameSummarySection(dataframe).get_nunique() == (5, 2, 5)


def test_dataframe_summary_section_get_nunique_empty() -> None:
    assert DataFrameSummarySection(pd.DataFrame({})).get_nunique() == ()


def test_dataframe_summary_section_get_column_types(dataframe: pd.DataFrame) -> None:
    assert DataFrameSummarySection(dataframe).get_column_types() == (
        {float},
        {int},
        {float, str, NoneType},
    )


def test_dataframe_summary_section_get_column_types_empty() -> None:
    assert DataFrameSummarySection(pd.DataFrame({})).get_column_types() == ()


def test_dataframe_summary_section_get_most_frequent_values(dataframe: pd.DataFrame) -> None:
    assert objects_are_allclose(
        DataFrameSummarySection(dataframe).get_most_frequent_values(),
        (
            ((2.2, 2), (1.2, 1), (4.2, 1), (np.nan, 1), (1.0, 1)),
            ((1, 5), (0, 1)),
            (("B", 2), ("A", 1), (None, 1), (np.nan, 1), ("C", 1)),
        ),
        equal_nan=True,
    )


def test_dataframe_summary_section_get_most_frequent_values_empty() -> None:
    assert DataFrameSummarySection(pd.DataFrame({})).get_most_frequent_values() == ()


def test_dataframe_summary_section_get_statistics(dataframe: pd.DataFrame) -> None:
    assert DataFrameSummarySection(dataframe).get_statistics() == {
        "columns": ("col1", "col2", "col3"),
        "null_count": (1, 0, 2),
        "nunique": (5, 2, 5),
        "column_types": ({float}, {int}, {float, str, NoneType}),
    }


def test_dataframe_summary_section_get_statistics_empty() -> None:
    assert DataFrameSummarySection(pd.DataFrame({})).get_statistics() == {
        "columns": (),
        "null_count": (),
        "nunique": (),
        "column_types": (),
    }


def test_column_temporal_null_value_section_render_html_body(dataframe: pd.DataFrame) -> None:
    section = DataFrameSummarySection(dataframe)
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_column_temporal_null_value_section_render_html_body_args(dataframe: pd.DataFrame) -> None:
    section = DataFrameSummarySection(dataframe)
    assert isinstance(
        Template(section.render_html_body(number="1.", tags=["meow"], depth=1)).render(), str
    )


def test_column_temporal_null_value_section_render_html_body_empty_rows() -> None:
    section = DataFrameSummarySection(pd.DataFrame({"col1": [], "col2": [], "col3": []}))
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_column_temporal_null_value_section_render_html_body_empty() -> None:
    section = DataFrameSummarySection(pd.DataFrame({}))
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_column_temporal_null_value_section_render_html_toc(dataframe: pd.DataFrame) -> None:
    section = DataFrameSummarySection(dataframe)
    assert isinstance(Template(section.render_html_toc()).render(), str)


def test_column_temporal_null_value_section_render_html_toc_args(dataframe: pd.DataFrame) -> None:
    section = DataFrameSummarySection(dataframe)
    assert isinstance(
        Template(section.render_html_toc(number="1.", tags=["meow"], depth=1)).render(), str
    )


#######################################
#     Tests for prepare_type_name     #
#######################################


@pytest.mark.parametrize(
    ("typ", "name"),
    [
        (float, "float"),
        (int, "int"),
        (str, "str"),
        (NoneType, "NoneType"),
        (pd.Timestamp, "pandas.Timestamp"),
        (np.ndarray, "numpy.ndarray"),
    ],
)
def test_prepare_type_name(typ: type, name: str) -> None:
    assert prepare_type_name(typ) == name
