# noqa: INP001
r"""Contain a demo example to generate a report."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from grizz.ingestor import Ingestor
from grizz.transformer import BaseTransformer, SequentialTransformer

from flamme import analyzer as fa
from flamme.reporter import BaseReporter, Reporter
from flamme.utils.logging import configure_logging

logger = logging.getLogger(__name__)

FIGSIZE = (14, 5)


def create_dataframe(nrows: int = 1000, ncols: int = 100) -> pd.DataFrame:
    r"""Create a DataFrame.

    Args:
        nrows: Specifies the number of rows.
        ncols: Specifies the number of columns.

    Returns:
        The generated DataFrame.
    """
    rng = np.random.default_rng(42)
    frame = pd.DataFrame(
        rng.normal(size=(nrows, ncols)), columns=[f"feature{i:04}" for i in range(ncols)]
    )
    mask = rng.choice([True, False], size=frame.shape, p=[0.2, 0.8])
    mask[mask.all(1), -1] = 0
    frame = frame.mask(mask)
    frame["datetime"] = pd.date_range("2018-01-01", periods=nrows, freq="H")
    return frame


def create_null_value_analyzer() -> fa.BaseAnalyzer:
    r"""Instantiate an analyzer about null values.

    Returns:
        The instantiated analyzer.
    """
    return fa.MappingAnalyzer(
        {
            "overall": fa.NullValueAnalyzer(figsize=FIGSIZE),
            "temporal": fa.TemporalNullValueAnalyzer(
                dt_column="datetime", period="M", figsize=FIGSIZE
            ),
            "monthly": fa.ColumnTemporalNullValueAnalyzer(
                dt_column="datetime", period="M", figsize=(7, 4)
            ),
            "weekly": fa.ColumnTemporalNullValueAnalyzer(dt_column="datetime", period="W"),
            "daily": fa.ColumnTemporalNullValueAnalyzer(
                dt_column="datetime", period="D", ncols=1, figsize=FIGSIZE
            ),
        }
    )


def create_continuous_column_analyzer(
    column: str,
    yscale: str = "linear",
    xmin: float | str | None = None,
    xmax: float | str | None = None,
) -> fa.BaseAnalyzer:
    r"""Instantiate an analyzer about continuous values for a given
    column.

    Args:
        column: Specifies the column to analyze.
        yscale: Specifies the y-axis scale.
        xmin: Specifies the minimum value of the range or its
            associated quantile.
        xmax: Specifies the maximum value of the range or its
            associated quantile.

    Returns:
        The instantiated analyzer.
    """
    return fa.MappingAnalyzer(
        {
            "overall": fa.ColumnContinuousAnalyzer(
                column=column,
                yscale=yscale,
                nbins=100,
                figsize=FIGSIZE,
                xmin=xmin,
                xmax=xmax,
            ),
            "monthly": fa.ColumnTemporalContinuousAnalyzer(
                column=column,
                dt_column="datetime",
                period="M",
                yscale=yscale,
                figsize=FIGSIZE,
            ),
            "weekly": fa.ColumnTemporalContinuousAnalyzer(
                column=column,
                dt_column="datetime",
                period="W",
                yscale=yscale,
                figsize=FIGSIZE,
            ),
            "daily": fa.ColumnTemporalContinuousAnalyzer(
                column=column,
                dt_column="datetime",
                period="D",
                yscale=yscale,
                figsize=FIGSIZE,
            ),
            "advanced": fa.ColumnContinuousAdvancedAnalyzer(
                column=column, yscale=yscale, nbins=100, figsize=FIGSIZE
            ),
            "most frequent": fa.MostFrequentValuesAnalyzer(column=column, top=10),
        },
        max_toc_depth=1,
    )


def create_analyzer() -> fa.BaseAnalyzer:
    r"""Instantiate an analyzer.

    Returns:
        The instantiated analyzer.
    """
    columns = fa.MappingAnalyzer({})
    return fa.MappingAnalyzer(
        {
            "summary": fa.DataFrameSummaryAnalyzer(),
            "monthly count": fa.TemporalRowCountAnalyzer(
                dt_column="datetime",
                period="M",
                figsize=FIGSIZE,
            ),
            "duplicate": fa.DuplicatedRowAnalyzer(),
            "column type": fa.DataTypeAnalyzer(),
            "null values": create_null_value_analyzer(),
            "columns": columns,
        }
    )


def create_transformer() -> BaseTransformer:
    r"""Instantiate a ``pandas.DataFrame`` transformer.

    Returns:
        The instantiated transformer.
    """
    return SequentialTransformer([])


def create_reporter() -> BaseReporter:
    r"""Instantiate a reporter.

    Returns:
        The instantiated reporter.
    """
    return Reporter(
        ingestor=Ingestor(frame=create_dataframe(nrows=10000, ncols=500)),
        transformer=create_transformer(),
        analyzer=create_analyzer(),
        report_path=Path.cwd().joinpath("tmp/report_large.html"),
    )


def main_report() -> None:
    r"""Define the main function to generate a report."""
    reporter = create_reporter()
    logger.info(f"reporter:\n{reporter}")
    reporter.compute()


if __name__ == "__main__":
    configure_logging(level=logging.INFO)
    main_report()
