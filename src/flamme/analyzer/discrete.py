from __future__ import annotations

__all__ = ["DiscreteDistributionAnalyzer"]

from collections import Counter

from pandas import DataFrame, Series

from flamme.analyzer.base import BaseAnalyzer
from flamme.section import DiscreteDistributionSection


class DiscreteDistributionAnalyzer(BaseAnalyzer):
    r"""Implements a discrete distribution analyzer.

    Args:
    ----
        column (str): Specifies the column to analyze.
        dropna (bool, optional): If ``True``, the NaN values are not
            included in the analysis. Default: ``False``
        max_rows (int, optional): Specifies the maximum number of rows
            to show in the table. Default: ``20``
    """

    def __init__(self, column: str, dropna: bool = False, max_rows: int = 20) -> None:
        self._column = column
        self._dropna = bool(dropna)
        self._max_rows = max_rows

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(column={self._column}, "
            f"dropna={self._dropna}, max_rows={self._max_rows})"
        )

    def analyze(self, df: DataFrame) -> DiscreteDistributionSection:
        series = Series()
        if self._column in df:
            series = df[self._column]
        return DiscreteDistributionSection(
            counter=Counter(series.value_counts(dropna=self._dropna).to_dict()),
            null_values=series.isnull().sum(),
            column=self._column,
            max_rows=self._max_rows,
        )
