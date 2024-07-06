from __future__ import annotations

import polars as pl
from polars.testing import assert_frame_equal

from flamme.transformer.dataframe import StripString

#####################################################
#     Tests for StripStringDataFrameTransformer     #
#####################################################


def test_strip_str_dataframe_transformer_repr() -> None:
    assert repr(StripString(columns=["col1", "col3"])).startswith(
        "StripStringDataFrameTransformer(columns=('col1', 'col3'))"
    )


def test_strip_str_dataframe_transformer_str() -> None:
    assert str(StripString(columns=["col1", "col3"])).startswith(
        "StripStringDataFrameTransformer(columns=('col1', 'col3'))"
    )


def test_strip_str_dataframe_transformer_transform() -> None:
    frame = pl.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["a ", " b", "  c  ", "d", "e"],
            "col4": ["a ", " b", "  c  ", "d", "e"],
        }
    )
    transformer = StripString(columns=["col1", "col2", "col3"])
    out = transformer.transform(frame)
    assert_frame_equal(
        out,
        pl.DataFrame(
            {
                "col1": [1, 2, 3, 4, 5],
                "col2": ["1", "2", "3", "4", "5"],
                "col3": ["a", "b", "c", "d", "e"],
                "col4": ["a ", " b", "  c  ", "d", "e"],
            }
        ),
    )


def test_strip_str_dataframe_transformer_transform_none() -> None:
    frame = pl.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5, None],
            "col2": ["1", "2", "3", "4", "5", None],
            "col3": ["a ", " b", "  c  ", "d", "e", None],
            "col4": ["a ", " b", "  c  ", "d", "e", None],
        }
    )
    transformer = StripString(columns=["col2", "col3"])
    out = transformer.transform(frame)
    assert_frame_equal(
        out,
        pl.DataFrame(
            {
                "col1": [1, 2, 3, 4, 5, None],
                "col2": ["1", "2", "3", "4", "5", None],
                "col3": ["a", "b", "c", "d", "e", None],
                "col4": ["a ", " b", "  c  ", "d", "e", None],
            }
        ),
    )


def test_strip_str_dataframe_transformer_transform_empty() -> None:
    transformer = StripString(columns=[])
    out = transformer.transform(pl.DataFrame({}))
    assert_frame_equal(out, pl.DataFrame({}))


def test_strip_str_dataframe_transformer_transform_empty_row() -> None:
    frame = pl.DataFrame({"col": []}, schema={"col": pl.String})
    transformer = StripString(columns=["col"])
    out = transformer.transform(frame)
    assert_frame_equal(out, pl.DataFrame({"col": []}, schema={"col": pl.String}))
