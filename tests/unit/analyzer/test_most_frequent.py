from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from coola import objects_are_allclose, objects_are_equal

from flamme.analyzer import MostFrequentValuesAnalyzer
from flamme.section import EmptySection, MostFrequentValuesSection


@pytest.fixture()
def dataframe() -> pd.DataFrame:
    return pd.DataFrame({"col": np.array([1, 42, np.nan, 22, 1, 2, 1, np.nan])})


################################################
#     Tests for MostFrequentValuesAnalyzer     #
################################################


def test_most_frequent_values_analyzer_str() -> None:
    assert str(MostFrequentValuesAnalyzer(column="col")).startswith("MostFrequentValuesAnalyzer(")


def test_most_frequent_values_analyzer_get_statistics(dataframe: pd.DataFrame) -> None:
    section = MostFrequentValuesAnalyzer(column="col").analyze(dataframe)
    assert isinstance(section, MostFrequentValuesSection)
    assert objects_are_allclose(
        section.get_statistics(),
        {"most_common": [(1.0, 3), (float("nan"), 2), (42.0, 1), (22.0, 1), (2.0, 1)]},
        equal_nan=True,
    )


def test_most_frequent_values_analyzer_get_statistics_dropna_true(dataframe: pd.DataFrame) -> None:
    section = MostFrequentValuesAnalyzer(column="col", dropna=True).analyze(dataframe)
    assert isinstance(section, MostFrequentValuesSection)
    assert objects_are_equal(
        section.get_statistics(), {"most_common": [(1.0, 3), (42.0, 1), (22.0, 1), (2.0, 1)]}
    )


def test_most_frequent_values_analyzer_get_statistics_empty_no_row() -> None:
    section = MostFrequentValuesAnalyzer(column="col").analyze(pd.DataFrame({"col": np.array([])}))
    assert isinstance(section, MostFrequentValuesSection)
    assert objects_are_equal(section.get_statistics(), {"most_common": []})


def test_most_frequent_values_analyzer_get_statistics_empty_no_column() -> None:
    section = MostFrequentValuesAnalyzer(column="col").analyze(pd.DataFrame({}))
    assert isinstance(section, EmptySection)
    assert objects_are_equal(section.get_statistics(), {})
