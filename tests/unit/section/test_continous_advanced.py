from __future__ import annotations

import polars as pl
import pytest
from coola import objects_are_allclose
from jinja2 import Template
from matplotlib import pyplot as plt
from polars.testing import assert_series_equal

from flamme.section import ColumnContinuousAdvancedSection
from flamme.section.continuous_advanced import (
    create_histogram_range_figure,
    create_section_template,
)


@pytest.fixture()
def series() -> pl.Series:
    return pl.Series([None, *list(range(101)), None], dtype=pl.Int64)


@pytest.fixture()
def stats() -> dict:
    return {
        "count": 103,
        "num_nulls": 2,
        "num_non_nulls": 101,
        "nunique": 102,
        "mean": 50.0,
        "std": 29.154759474226502,
        "skewness": 0.0,
        "kurtosis": -1.2,
        "min": 0.0,
        "q001": 0.1,
        "q01": 1.0,
        "q05": 5.0,
        "q10": 10.0,
        "q25": 25.0,
        "median": 50.0,
        "q75": 75.0,
        "q90": 90.0,
        "q95": 95.0,
        "q99": 99.0,
        "q999": 99.9,
        "max": 100.0,
        ">0": 100,
        "<0": 0,
        "=0": 1,
    }


#####################################################
#     Tests for ColumnContinuousAdvancedSection     #
#####################################################


def test_column_continuous_advanced_section_str(series: pl.Series) -> None:
    assert str(ColumnContinuousAdvancedSection(series=series, column="col")).startswith(
        "ColumnContinuousAdvancedSection("
    )


def test_column_continuous_advanced_section_series(series: pl.Series) -> None:
    assert_series_equal(ColumnContinuousAdvancedSection(series=series, column="col").series, series)


def test_column_continuous_advanced_section_column(series: pl.Series) -> None:
    assert ColumnContinuousAdvancedSection(series=series, column="col").column == "col"


def test_column_continuous_advanced_section_yscale_default(series: pl.Series) -> None:
    assert ColumnContinuousAdvancedSection(series=series, column="col").yscale == "auto"


@pytest.mark.parametrize("yscale", ["log", "linear"])
def test_column_continuous_advanced_section_yscale(series: pl.Series, yscale: str) -> None:
    assert (
        ColumnContinuousAdvancedSection(series=series, column="col", yscale=yscale).yscale == yscale
    )


def test_column_continuous_advanced_section_nbins_default(series: pl.Series) -> None:
    assert ColumnContinuousAdvancedSection(series=series, column="col").nbins is None


@pytest.mark.parametrize("nbins", [1, 2, 4])
def test_column_continuous_advanced_section_nbins(series: pl.Series, nbins: int) -> None:
    assert ColumnContinuousAdvancedSection(series=series, column="col", nbins=nbins).nbins == nbins


def test_column_continuous_advanced_section_figsize_default(series: pl.Series) -> None:
    assert ColumnContinuousAdvancedSection(series=series, column="col").figsize is None


@pytest.mark.parametrize("figsize", [(7, 3), (1.5, 1.5)])
def test_column_continuous_advanced_section_figsize(
    series: pl.Series, figsize: tuple[float, float]
) -> None:
    assert (
        ColumnContinuousAdvancedSection(series=series, column="col", figsize=figsize).figsize
        == figsize
    )


def test_column_continuous_advanced_section_get_statistics(series: pl.Series, stats: dict) -> None:
    section = ColumnContinuousAdvancedSection(series=series, column="col")
    assert objects_are_allclose(section.get_statistics(), stats, atol=1e-2)


def test_column_continuous_advanced_section_get_statistics_empty_row() -> None:
    section = ColumnContinuousAdvancedSection(series=pl.Series([], dtype=pl.Int64), column="col")
    assert objects_are_allclose(
        section.get_statistics(),
        {
            "count": 0,
            "num_nulls": 0,
            "num_non_nulls": 0,
            "nunique": 0,
            "mean": float("nan"),
            "std": float("nan"),
            "skewness": float("nan"),
            "kurtosis": float("nan"),
            "min": float("nan"),
            "q001": float("nan"),
            "q01": float("nan"),
            "q05": float("nan"),
            "q10": float("nan"),
            "q25": float("nan"),
            "median": float("nan"),
            "q75": float("nan"),
            "q90": float("nan"),
            "q95": float("nan"),
            "q99": float("nan"),
            "q999": float("nan"),
            "max": float("nan"),
            ">0": 0,
            "<0": 0,
            "=0": 0,
        },
        equal_nan=True,
    )


def test_column_continuous_advanced_section_get_statistics_single_value() -> None:
    section = ColumnContinuousAdvancedSection(
        series=pl.Series(values=[1, 1, 1, 1, 1]), column="col"
    )
    assert objects_are_allclose(
        section.get_statistics(),
        {
            "count": 5,
            "num_nulls": 0,
            "num_non_nulls": 5,
            "nunique": 1,
            "mean": 1.0,
            "std": 0.0,
            "skewness": float("nan"),
            "kurtosis": float("nan"),
            "min": 1.0,
            "q001": 1.0,
            "q01": 1.0,
            "q05": 1.0,
            "q10": 1.0,
            "q25": 1.0,
            "median": 1.0,
            "q75": 1.0,
            "q90": 1.0,
            "q95": 1.0,
            "q99": 1.0,
            "q999": 1.0,
            "max": 1.0,
            ">0": 5,
            "<0": 0,
            "=0": 0,
        },
        equal_nan=True,
    )


def test_column_continuous_advanced_section_get_statistics_only_nans() -> None:
    section = ColumnContinuousAdvancedSection(
        series=pl.Series([None, None, None, None]), column="col"
    )
    assert objects_are_allclose(
        section.get_statistics(),
        {
            "count": 4,
            "num_nulls": 4,
            "num_non_nulls": 0,
            "nunique": 1,
            "mean": float("nan"),
            "std": float("nan"),
            "skewness": float("nan"),
            "kurtosis": float("nan"),
            "min": float("nan"),
            "q001": float("nan"),
            "q01": float("nan"),
            "q05": float("nan"),
            "q10": float("nan"),
            "q25": float("nan"),
            "median": float("nan"),
            "q75": float("nan"),
            "q90": float("nan"),
            "q95": float("nan"),
            "q99": float("nan"),
            "q999": float("nan"),
            "max": float("nan"),
            ">0": 0,
            "<0": 0,
            "=0": 0,
        },
        equal_nan=True,
    )


def test_column_continuous_advanced_section_render_html_body(series: pl.Series) -> None:
    section = ColumnContinuousAdvancedSection(series=series, column="col")
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_column_continuous_advanced_section_render_html_body_args(series: pl.Series) -> None:
    section = ColumnContinuousAdvancedSection(series=series, column="col")
    assert isinstance(
        Template(section.render_html_body(number="1.", tags=["meow"], depth=1)).render(), str
    )


def test_column_continuous_advanced_section_render_html_body_empty() -> None:
    section = ColumnContinuousAdvancedSection(
        series=pl.Series(values=[], dtype=pl.Int64), column="col"
    )
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_column_continuous_advanced_section_render_html_toc(series: pl.Series) -> None:
    section = ColumnContinuousAdvancedSection(series=series, column="col")
    assert isinstance(Template(section.render_html_toc()).render(), str)


def test_column_continuous_advanced_section_render_html_toc_args(series: pl.Series) -> None:
    section = ColumnContinuousAdvancedSection(series=series, column="col")
    assert isinstance(
        Template(section.render_html_toc(number="1.", tags=["meow"], depth=1)).render(), str
    )


#############################################
#     Tests for create_section_template     #
#############################################


def test_create_section_template() -> None:
    assert isinstance(create_section_template(), str)


##################################################
#    Tests for create_histogram_range_figure     #
##################################################


def test_create_histogram_range_figure(series: pl.Series) -> None:
    assert isinstance(create_histogram_range_figure(series=series, column="col"), plt.Figure)


@pytest.mark.parametrize("nbins", [1, 2, 4])
def test_create_histogram_range_figure_nbins(series: pl.Series, nbins: int) -> None:
    assert isinstance(
        create_histogram_range_figure(series=series, column="col", nbins=nbins), plt.Figure
    )


@pytest.mark.parametrize("yscale", ["linear", "log"])
def test_create_histogram_range_figure_yscale(series: pl.Series, yscale: str) -> None:
    assert isinstance(
        create_histogram_range_figure(series=series, column="col", yscale=yscale), plt.Figure
    )


@pytest.mark.parametrize("xmin", [1.0, "q0.1", None, "q1"])
def test_create_histogram_range_figure_xmin(series: pl.Series, xmin: float | str | None) -> None:
    assert isinstance(
        create_histogram_range_figure(series=series, column="col", xmin=xmin), plt.Figure
    )


@pytest.mark.parametrize("xmax", [100.0, "q0.9", None, "q0"])
def test_create_histogram_range_figure_xmax(series: pl.Series, xmax: float | str | None) -> None:
    assert isinstance(
        create_histogram_range_figure(series=series, column="col", xmax=xmax), plt.Figure
    )


@pytest.mark.parametrize("figsize", [(7, 3), (1.5, 1.5)])
def test_create_histogram_range_figure_figsize(
    series: pl.Series, figsize: tuple[float, float]
) -> None:
    assert isinstance(
        create_histogram_range_figure(series=series, column="col", figsize=figsize), plt.Figure
    )


def test_create_histogram_range_figure_empty() -> None:
    assert (
        create_histogram_range_figure(series=pl.Series([None, None], dtype=pl.Int64), column="col")
        is None
    )
