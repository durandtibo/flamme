from __future__ import annotations

import polars as pl
import pyarrow as pa
import pytest
from coola import objects_are_equal

from flamme.schema.reader import SchemaReader


@pytest.fixture(scope="module")
def frame() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["a", "b", "c", "d", "e"],
            "col3": [1.2, 2.2, 3.2, 4.2, 5.2],
        }
    )


##################################
#     Tests for SchemaReader     #
##################################


def test_schema_reader_str(frame: pl.DataFrame) -> None:
    assert str(SchemaReader(frame)).startswith("SchemaReader(")


def test_schema_reader_read(frame: pl.DataFrame) -> None:
    schema = SchemaReader(frame).read()
    assert objects_are_equal(
        schema,
        pa.schema(
            [
                ("col1", pa.int64()),
                ("col2", pa.large_string()),
                ("col3", pa.float64()),
            ]
        ),
    )
