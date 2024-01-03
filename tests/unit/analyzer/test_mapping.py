from __future__ import annotations

import numpy as np
import pytest
from coola import objects_are_allclose
from pandas import DataFrame

from flamme.analyzer import (
    DataTypeAnalyzer,
    DuplicatedRowAnalyzer,
    MappingAnalyzer,
    NullValueAnalyzer,
)
from flamme.section import SectionDict

#####################################
#     Tests for MappingAnalyzer     #
#####################################


def test_mapping_analyzer_str() -> None:
    assert str(MappingAnalyzer({})).startswith("MappingAnalyzer(")


def test_mapping_analyzer_analyzers() -> None:
    analyzer = MappingAnalyzer(
        {
            "section1": NullValueAnalyzer(),
            "section2": DuplicatedRowAnalyzer(),
        }
    )
    assert isinstance(analyzer.analyzers, dict)
    assert len(analyzer.analyzers) == 2
    assert isinstance(analyzer.analyzers["section1"], NullValueAnalyzer)
    assert isinstance(analyzer.analyzers["section2"], DuplicatedRowAnalyzer)


def test_mapping_analyzer_get_statistics() -> None:
    section = MappingAnalyzer(
        {
            "section1": NullValueAnalyzer(),
            "section2": NullValueAnalyzer(),
        }
    ).analyze(
        DataFrame(
            {
                "float": np.array([1.2, 4.2, np.nan, 2.2]),
                "int": np.array([np.nan, 1, 0, 1]),
                "str": np.array(["A", "B", None, np.nan]),
            }
        )
    )
    assert isinstance(section, SectionDict)
    assert objects_are_allclose(
        section.get_statistics(),
        {
            "section1": {
                "columns": ("float", "int", "str"),
                "null_count": (1, 1, 2),
                "total_count": (4, 4, 4),
            },
            "section2": {
                "columns": ("float", "int", "str"),
                "null_count": (1, 1, 2),
                "total_count": (4, 4, 4),
            },
        },
    )


def test_mapping_analyzer_get_statistics_empty() -> None:
    section = MappingAnalyzer(
        {
            "section1": NullValueAnalyzer(),
            "section2": NullValueAnalyzer(),
        }
    ).analyze(
        DataFrame(
            {
                "float": np.array([]),
                "int": np.array([]),
                "str": np.array([]),
            }
        )
    )
    assert isinstance(section, SectionDict)
    assert objects_are_allclose(
        section.get_statistics(),
        {
            "section1": {
                "columns": ("float", "int", "str"),
                "null_count": (0, 0, 0),
                "total_count": (0, 0, 0),
            },
            "section2": {
                "columns": ("float", "int", "str"),
                "null_count": (0, 0, 0),
                "total_count": (0, 0, 0),
            },
        },
    )


@pytest.mark.parametrize("max_toc_depth", [0, 1, 2])
def test_mapping_analyzer_max_toc_depth(max_toc_depth: int) -> None:
    section = MappingAnalyzer(
        {
            "section1": NullValueAnalyzer(),
            "section2": NullValueAnalyzer(),
        },
        max_toc_depth=max_toc_depth,
    ).analyze(
        DataFrame(
            {
                "float": np.array([1.2, 4.2, np.nan, 2.2]),
                "int": np.array([np.nan, 1, 0, 1]),
                "str": np.array(["A", "B", None, np.nan]),
            }
        )
    )
    assert isinstance(section, SectionDict)
    assert section.max_toc_depth == max_toc_depth


def test_mapping_analyzer_add_analyzer() -> None:
    analyzer = MappingAnalyzer(
        {
            "section1": NullValueAnalyzer(),
            "section2": DuplicatedRowAnalyzer(),
        }
    )
    analyzer.add_analyzer("section3", DataTypeAnalyzer())
    assert isinstance(analyzer.analyzers, dict)
    assert len(analyzer.analyzers) == 3
    assert isinstance(analyzer.analyzers["section1"], NullValueAnalyzer)
    assert isinstance(analyzer.analyzers["section2"], DuplicatedRowAnalyzer)
    assert isinstance(analyzer.analyzers["section3"], DataTypeAnalyzer)


def test_mapping_analyzer_add_analyzer_replace_ok_false() -> None:
    analyzer = MappingAnalyzer(
        {
            "section1": NullValueAnalyzer(),
            "section2": DataTypeAnalyzer(),
        }
    )
    with pytest.raises(KeyError, match="`section2` is already used to register an analyzer."):
        analyzer.add_analyzer("section2", DuplicatedRowAnalyzer())


def test_mapping_analyzer_add_analyzer_replace_ok_true() -> None:
    analyzer = MappingAnalyzer(
        {
            "section1": NullValueAnalyzer(),
            "section2": DataTypeAnalyzer(),
        }
    )
    analyzer.add_analyzer("section2", DuplicatedRowAnalyzer(), replace_ok=True)
    assert isinstance(analyzer.analyzers, dict)
    assert len(analyzer.analyzers) == 2
    assert isinstance(analyzer.analyzers["section1"], NullValueAnalyzer)
    assert isinstance(analyzer.analyzers["section2"], DuplicatedRowAnalyzer)
