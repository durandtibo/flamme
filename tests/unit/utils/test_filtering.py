from __future__ import annotations

from decimal import Decimal

import pandas as pd

from flamme.utils.filtering import (
    find_columns_decimal,
    find_columns_str,
    find_columns_type,
)

#######################################
#     Tests for find_columns_type     #
#######################################


def test_find_columns_type_str() -> None:
    dataframe = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["1", "2", "3", "4", "5"],
            "col4": ["a", "b", "c", "d", "e"],
        }
    )
    assert find_columns_type(dataframe, str) == ("col2", "col3", "col4")


def test_find_columns_type_int() -> None:
    dataframe = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["1", "2", "3", "4", "5"],
            "col4": ["a", "b", "c", "d", "e"],
        }
    )
    assert find_columns_type(dataframe, int) == ("col1",)


def test_find_columns_type_float() -> None:
    dataframe = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["1", "2", "3", "4", "5"],
            "col4": ["a", "b", "c", "d", "e"],
        }
    )
    assert find_columns_type(dataframe, float) == ()


def test_find_columns_type_empty() -> None:
    assert find_columns_type(pd.DataFrame({}), str) == ()


##########################################
#     Tests for find_columns_decimal     #
##########################################


def test_find_columns_decimal() -> None:
    dataframe = pd.DataFrame(
        {
            "col1": [1, 2, 3, Decimal(4), Decimal(5)],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["1", Decimal(2), "3", "4", "5"],
            "col4": ["a", "b", "c", "d", "e"],
        }
    )
    assert find_columns_decimal(dataframe) == ("col1", "col3")


def test_find_columns_decimal_empty() -> None:
    assert find_columns_decimal(pd.DataFrame({})) == ()


######################################
#     Tests for find_columns_str     #
######################################


def test_find_columns_str() -> None:
    dataframe = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["1", "2", "3", "4", "5"],
            "col3": ["1", "2", "3", "4", "5"],
            "col4": ["a", "b", "c", "d", "e"],
        }
    )
    assert find_columns_str(dataframe) == ("col2", "col3", "col4")


def test_find_columns_str_empty() -> None:
    assert find_columns_str(pd.DataFrame({})) == ()
