from __future__ import annotations

import pandas as pd
from pandas.testing import assert_frame_equal

from flamme.transformer.dataframe import Sequential, StripString, ToNumeric

####################################################
#     Tests for SequentialDataFrameTransformer     #
####################################################


def test_sequential_dataframe_transformer_str() -> None:
    assert str(
        Sequential(
            [
                StripString(columns=["col1", "col3"]),
                ToNumeric(columns=["col1", "col2"]),
            ]
        )
    ).startswith("SequentialDataFrameTransformer(")


def test_sequential_dataframe_transformer_str_empty() -> None:
    assert str(Sequential([])) == "SequentialDataFrameTransformer()"


def test_sequential_dataframe_transformer_transform_1() -> None:
    frame = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, "  "],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["a ", " b", "  c  ", "d", "e"],
            "col4": ["a ", " b", "  c  ", "d", "e"],
        }
    )
    transformer = Sequential([ToNumeric(columns=["col1", "col2"], errors="coerce")])
    frame = transformer.transform(frame)
    assert_frame_equal(
        frame,
        pd.DataFrame(
            {
                "col1": [1.0, 2.0, 3.0, 4.0, float("nan")],
                "col2": [1, 2, 3, 4, 5],
                "col3": ["a ", " b", "  c  ", "d", "e"],
                "col4": ["a ", " b", "  c  ", "d", "e"],
            }
        ),
    )


def test_sequential_dataframe_transformer_transform_2() -> None:
    frame = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, "  "],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["a ", " b", "  c  ", "d", "e"],
            "col4": ["a ", " b", "  c  ", "d", "e"],
        }
    )
    transformer = Sequential(
        [
            StripString(columns=["col1", "col3"]),
            ToNumeric(columns=["col1", "col2"]),
        ]
    )
    frame = transformer.transform(frame)
    assert_frame_equal(
        frame,
        pd.DataFrame(
            {
                "col1": [1.0, 2.0, 3.0, 4.0, float("nan")],
                "col2": [1, 2, 3, 4, 5],
                "col3": ["a", "b", "c", "d", "e"],
                "col4": ["a ", " b", "  c  ", "d", "e"],
            }
        ),
    )
