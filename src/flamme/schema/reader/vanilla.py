r"""Contain the implementation of a simple ingestor."""

from __future__ import annotations

__all__ = ["SchemaReader"]

from typing import TYPE_CHECKING

import pyarrow as pa

from flamme.schema.reader.base import BaseSchemaReader

if TYPE_CHECKING:
    from pandas import DataFrame


class SchemaReader(BaseSchemaReader):
    r"""Implement a simple DataFrame ingestor.

    Args:
        df: Specifies the DataFrame to ingest.

    Example usage:

    ```pycon
    >>> import pandas as pd
    >>> from flamme.schema.reader import SchemaReader
    >>> reader = SchemaReader(
    ...     df=pd.DataFrame(
    ...         {
    ...             "col1": [1, 2, 3, 4, 5],
    ...             "col2": [1.1, 2.2, 3.3, 4.4, 5.5],
    ...             "col4": ["a", "b", "c", "d", "e"],
    ...         }
    ...     )
    ... )
    >>> reader
    SchemaReader(shape=(5, 3))
    >>> schema = reader.read()
    >>> schema
    col1: int64
    col2: double
    col4: string
    ...

    ```
    """

    def __init__(self, df: DataFrame) -> None:
        self._df = df

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(shape={self._df.shape})"

    def read(self) -> pa.Schema:
        return pa.Schema.from_pandas(self._df)
