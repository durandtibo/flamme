from __future__ import annotations

from datetime import datetime, timezone

import matplotlib.pyplot as plt
import polars as pl
import pytest
from coola import objects_are_allclose
from jinja2 import Template
from polars.testing import assert_frame_equal

from flamme.section import TemporalNullValueSection
from flamme.section.null_temp import (
    create_section_template,
    create_temporal_null_figure,
    create_temporal_null_table,
    create_temporal_null_table_row,
)


@pytest.fixture()
def dataframe() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "col1": [None, float("nan"), 0.0, 1.0],
            "col2": [None, 1, 0, None],
            "datetime": [
                datetime(year=2020, month=1, day=3, tzinfo=timezone.utc),
                datetime(year=2020, month=2, day=3, tzinfo=timezone.utc),
                datetime(year=2020, month=3, day=3, tzinfo=timezone.utc),
                datetime(year=2020, month=4, day=3, tzinfo=timezone.utc),
            ],
        },
        schema={
            "col1": pl.Float64,
            "col2": pl.Int64,
            "datetime": pl.Datetime(time_unit="us", time_zone="UTC"),
        },
    )


@pytest.fixture()
def dataframe_empty() -> pl.DataFrame:
    return pl.DataFrame(
        {"col1": [], "col2": [], "datetime": []},
        schema={
            "col1": pl.Float64,
            "col2": pl.Int64,
            "datetime": pl.Datetime(time_unit="us", time_zone="UTC"),
        },
    )


##############################################
#     Tests for TemporalNullValueSection     #
##############################################


def test_temporal_null_value_section_str(dataframe: pl.DataFrame) -> None:
    assert str(
        TemporalNullValueSection(
            frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
        )
    ).startswith("TemporalNullValueSection(")


def test_temporal_null_value_section_frame(dataframe: pl.DataFrame) -> None:
    section = TemporalNullValueSection(
        frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
    )
    assert_frame_equal(section.frame, dataframe)


def test_temporal_null_value_section_columns(dataframe: pl.DataFrame) -> None:
    section = TemporalNullValueSection(
        frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
    )
    assert section.columns == ("col1", "col2")


@pytest.mark.parametrize("dt_column", ["datetime", "date"])
def test_temporal_null_value_section_dt_column(dt_column: str, dataframe: pl.DataFrame) -> None:
    section = TemporalNullValueSection(
        frame=dataframe.with_columns(pl.col("datetime").alias("date")),
        columns=["col1", "col2"],
        dt_column=dt_column,
        period="1mo",
    )
    assert section.dt_column == dt_column


@pytest.mark.parametrize("period", ["1mo", "D"])
def test_temporal_null_value_section_period(dataframe: pl.DataFrame, period: str) -> None:
    section = TemporalNullValueSection(
        frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period=period
    )
    assert section.period == period


@pytest.mark.parametrize("figsize", [(7, 3), (1.5, 1.5)])
def test_temporal_null_value_section_figsize(
    dataframe: pl.DataFrame, figsize: tuple[int, int]
) -> None:
    section = TemporalNullValueSection(
        frame=dataframe,
        columns=["col1", "col2"],
        dt_column="datetime",
        period="1mo",
        figsize=figsize,
    )
    assert section.figsize == figsize


def test_temporal_null_value_section_figsize_default(dataframe: pl.DataFrame) -> None:
    section = TemporalNullValueSection(
        frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
    )
    assert section.figsize is None


def test_temporal_null_value_section_missing_dt_column(dataframe: pl.DataFrame) -> None:
    with pytest.raises(
        ValueError, match=r"Datetime column my_datetime is not in the DataFrame \(columns:"
    ):
        TemporalNullValueSection(
            frame=dataframe, columns=["col1", "col2"], dt_column="my_datetime", period="1mo"
        )


def test_temporal_null_value_section_get_statistics(dataframe: pl.DataFrame) -> None:
    section = TemporalNullValueSection(
        frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
    )
    assert objects_are_allclose(section.get_statistics(), {})


def test_temporal_null_value_section_get_statistics_empty_row(
    dataframe_empty: pl.DataFrame,
) -> None:
    section = TemporalNullValueSection(
        frame=dataframe_empty,
        columns=["col1", "col2"],
        dt_column="datetime",
        period="1mo",
    )
    assert objects_are_allclose(section.get_statistics(), {})


def test_temporal_null_value_section_render_html_body(dataframe: pl.DataFrame) -> None:
    section = TemporalNullValueSection(
        frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
    )
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_temporal_null_value_section_render_html_body_args(dataframe: pl.DataFrame) -> None:
    section = TemporalNullValueSection(
        frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
    )
    assert isinstance(
        Template(section.render_html_body(number="1.", tags=["meow"], depth=1)).render(), str
    )


def test_temporal_null_value_section_render_html_body_empty_rows(
    dataframe_empty: pl.DataFrame,
) -> None:
    section = TemporalNullValueSection(
        frame=dataframe_empty,
        columns=["col1", "col2"],
        dt_column="datetime",
        period="1mo",
    )
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_temporal_null_value_section_render_html_toc(dataframe: pl.DataFrame) -> None:
    section = TemporalNullValueSection(
        frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
    )
    assert isinstance(Template(section.render_html_toc()).render(), str)


def test_temporal_null_value_section_render_html_toc_args(dataframe: pl.DataFrame) -> None:
    section = TemporalNullValueSection(
        frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
    )
    assert isinstance(
        Template(section.render_html_toc(number="1.", tags=["meow"], depth=1)).render(), str
    )


#############################################
#     Tests for create_section_template     #
#############################################


def test_create_section_template() -> None:
    assert isinstance(create_section_template(), str)


################################################
#    Tests for create_temporal_null_figure     #
################################################


def test_create_temporal_null_figure(dataframe: pl.DataFrame) -> None:
    assert isinstance(
        create_temporal_null_figure(
            frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
        ),
        plt.Figure,
    )


def test_create_temporal_null_figure_empty(dataframe_empty: pl.DataFrame) -> None:
    assert isinstance(
        create_temporal_null_figure(
            frame=dataframe_empty,
            columns=["col1", "col2"],
            dt_column="datetime",
            period="1mo",
        ),
        plt.Figure,
    )


###############################################
#    Tests for create_temporal_null_table     #
###############################################


def test_create_temporal_null_table(dataframe: pl.DataFrame) -> None:
    assert isinstance(
        create_temporal_null_table(
            frame=dataframe, columns=["col1", "col2"], dt_column="datetime", period="1mo"
        ),
        str,
    )


def test_create_temporal_null_table_empty(dataframe_empty: pl.DataFrame) -> None:
    assert isinstance(
        create_temporal_null_table(
            frame=dataframe_empty,
            columns=["col1", "col2"],
            dt_column="datetime",
            period="1mo",
        ),
        str,
    )


###################################################
#    Tests for create_temporal_null_table_row     #
###################################################


def test_create_temporal_null_table_row() -> None:
    assert isinstance(create_temporal_null_table_row(label="meow", num_nulls=5, total=42), str)
