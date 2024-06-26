r"""Implement an analyzer that generates a section about the most
frequent values in a given columns."""

from __future__ import annotations

__all__ = ["MostFrequentValuesAnalyzer"]

import logging
from collections import Counter
from typing import TYPE_CHECKING

from flamme.analyzer.base import BaseAnalyzer
from flamme.section import EmptySection, MostFrequentValuesSection

if TYPE_CHECKING:
    import pandas as pd

logger = logging.getLogger(__name__)


class MostFrequentValuesAnalyzer(BaseAnalyzer):
    r"""Implement a most frequent values analyzer for a given column.

    Args:
        column: The column to analyze.
        dropna: If ``True``, the NaN values are not included in the
            analysis.
        top: The maximum number of values to show.

    Example usage:

    ```pycon

    >>> import numpy as np
    >>> import pandas as pd
    >>> from flamme.analyzer import MostFrequentValuesAnalyzer
    >>> analyzer = MostFrequentValuesAnalyzer(column="str")
    >>> analyzer
    MostFrequentValuesAnalyzer(column=str, dropna=False, top=100)
    >>> frame = pd.DataFrame({"col": np.array([np.nan, 1, 0, 1])})
    >>> section = analyzer.analyze(frame)

    ```
    """

    def __init__(self, column: str, dropna: bool = False, top: int = 100) -> None:
        self._column = column
        self._dropna = bool(dropna)
        self._top = top

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(column={self._column}, "
            f"dropna={self._dropna}, top={self._top:,})"
        )

    def analyze(self, frame: pd.DataFrame) -> MostFrequentValuesSection | EmptySection:
        logger.info(f"Analyzing the most frequent values of {self._column}")
        if self._column not in frame:
            logger.info(
                f"Skipping most frequent values analysis of column {self._column} "
                f"because it is not in the DataFrame: {sorted(frame.columns)}"
            )
            return EmptySection()
        return MostFrequentValuesSection(
            counter=Counter(frame[self._column].value_counts(dropna=self._dropna).to_dict()),
            column=self._column,
            top=self._top,
        )
