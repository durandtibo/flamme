from __future__ import annotations

import pandas as pd
import pyarrow as pa
from pandas.testing import assert_frame_equal

from flamme.transformer.dataframe import ToNumeric

###################################################
#     Tests for ToNumericDataFrameTransformer     #
###################################################


def test_to_numeric_dataframe_transformer_str() -> None:
    assert (
        str(ToNumeric(columns=["col1", "col3"]))
        == "ToNumericDataFrameTransformer(columns=('col1', 'col3'))"
    )


def test_to_numeric_dataframe_transformer_str_kwargs() -> None:
    assert (
        str(ToNumeric(columns=["col1", "col3"], errors="ignore"))
        == "ToNumericDataFrameTransformer(columns=('col1', 'col3'), errors=ignore)"
    )


def test_to_numeric_dataframe_transformer_transform() -> None:
    frame = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["1", "2", "3", "4", "5"],
            "col4": ["a", "b", "c", "d", "e"],
        }
    )
    transformer = ToNumeric(columns=["col1", "col3"])
    out = transformer.transform(frame)
    assert_frame_equal(
        out,
        pd.DataFrame(
            {
                "col1": [1, 2, 3, 4, 5],
                "col2": ["1", "2", "3", "4", "5"],
                "col3": [1, 2, 3, 4, 5],
                "col4": ["a", "b", "c", "d", "e"],
            }
        ),
    )


def test_to_numeric_dataframe_transformer_transform_kwargs() -> None:
    frame = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["1", "2", "3", "4", "a5"],
            "col4": ["a", "b", "c", "d", "e"],
        }
    )
    transformer = ToNumeric(columns=["col1", "col3"], errors="coerce")
    out = transformer.transform(frame)
    assert_frame_equal(
        out,
        pd.DataFrame(
            {
                "col1": [1, 2, 3, 4, 5],
                "col2": ["1", "2", "3", "4", "5"],
                "col3": [1, 2, 3, 4, float("nan")],
                "col4": ["a", "b", "c", "d", "e"],
            }
        ),
    )


def test_to_numeric_dataframe_transformer_from_schema() -> None:
    frame = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["1", "2", "3", "4", "5"],
            "col4": ["a", "b", "c", "d", "e"],
        }
    )
    transformer = ToNumeric.from_schema(
        schema=pa.schema([("col1", pa.int64()), ("col2", pa.string()), ("col3", pa.float64())])
    )
    out = transformer.transform(frame)
    assert_frame_equal(
        out,
        pd.DataFrame(
            {
                "col1": [1, 2, 3, 4, 5],
                "col2": ["1", "2", "3", "4", "5"],
                "col3": [1, 2, 3, 4, 5],
                "col4": ["a", "b", "c", "d", "e"],
            }
        ),
    )


def test_to_numeric_dataframe_transformer_from_schema_kwargs() -> None:
    frame = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["1", "2", "3", "4", "a5"],
            "col4": ["a", "b", "c", "d", "e"],
        }
    )
    transformer = ToNumeric.from_schema(
        schema=pa.schema([("col1", pa.int64()), ("col2", pa.string()), ("col3", pa.float64())]),
        errors="coerce",
    )
    out = transformer.transform(frame)
    assert_frame_equal(
        out,
        pd.DataFrame(
            {
                "col1": [1, 2, 3, 4, 5],
                "col2": ["1", "2", "3", "4", "5"],
                "col3": [1, 2, 3, 4, float("nan")],
                "col4": ["a", "b", "c", "d", "e"],
            }
        ),
    )