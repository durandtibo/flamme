from __future__ import annotations

import pandas as pd
from pandas.testing import assert_frame_equal

from flamme.transformer.df import StripString

#####################################################
#     Tests for StripStringDataFrameTransformer     #
#####################################################


def test_strip_str_dataframe_transformer_str() -> None:
    assert (
        str(StripString(columns=["col1", "col3"]))
        == "StripStringDataFrameTransformer(columns=('col1', 'col3'))"
    )


def test_strip_str_dataframe_transformer_transform() -> None:
    dataframe = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, "  "],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["a ", " b", "  c  ", "d", "e"],
            "col4": ["a ", " b", "  c  ", "d", "e"],
        }
    )
    transformer = StripString(columns=["col1", "col3"])
    dataframe = transformer.transform(dataframe)
    assert_frame_equal(
        dataframe,
        pd.DataFrame(
            {
                "col1": [1, 2, 3, 4, ""],
                "col2": ["1", "2", "3", "4", "5"],
                "col3": ["a", "b", "c", "d", "e"],
                "col4": ["a ", " b", "  c  ", "d", "e"],
            }
        ),
    )


def test_strip_str_dataframe_transformer_transform_none() -> None:
    dataframe = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, "  ", None, 42, 4.2],
            "col2": ["1", "2", "3", "4", "5", None, 42, 4.2],
            "col3": ["a ", " b", "  c  ", "d", "e", None, 42, 4.2],
            "col4": ["a ", " b", "  c  ", "d", "e", None, 42, 4.2],
        }
    )
    transformer = StripString(columns=["col1", "col3"])
    dataframe = transformer.transform(dataframe)
    assert_frame_equal(
        dataframe,
        pd.DataFrame(
            {
                "col1": [1, 2, 3, 4, "", None, 42, 4.2],
                "col2": ["1", "2", "3", "4", "5", None, 42, 4.2],
                "col3": ["a", "b", "c", "d", "e", None, 42, 4.2],
                "col4": ["a ", " b", "  c  ", "d", "e", None, 42, 4.2],
            }
        ),
    )


def test_strip_str_dataframe_transformer_transform_empty() -> None:
    dataframe = pd.DataFrame({})
    transformer = StripString(columns=[])
    dataframe = transformer.transform(dataframe)
    assert_frame_equal(dataframe, pd.DataFrame({}))
