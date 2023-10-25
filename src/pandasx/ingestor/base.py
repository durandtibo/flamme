from __future__ import annotations

__all__ = ["BaseIngestor"]

import logging
from abc import ABC
from typing import TypeVar

from objectory import AbstractFactory
from pandas import DataFrame

logger = logging.getLogger(__name__)


T = TypeVar("T")


class BaseIngestor(ABC, metaclass=AbstractFactory):
    r"""Defines the base class to implement a DataFrame ingestor.

    Example usage:

    .. code-block:: pycon

        >>> from pandasx.ingestor import ParquetIngestor
        >>> ingestor = ParquetIngestor(path="/path/to/df.parquet")
        >>> df = ingestor.ingest()
    """

    def ingest(self) -> DataFrame:
        r"""Ingests a DataFrame.

        Returns:
            ``pandas.DataFrame``: The ingested DataFrame.

        Example usage:

        .. code-block:: pycon

            >>> from pandasx.ingestor import ParquetIngestor
            >>> ingestor = ParquetIngestor(path="/path/to/df.parquet")
            >>> df = ingestor.ingest()
        """
