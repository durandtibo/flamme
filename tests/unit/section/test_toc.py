from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from coola import objects_are_equal
from jinja2 import Template

from flamme.section import DuplicatedRowSection, TableOfContentSection


@pytest.fixture()
def dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "col1": np.array([1.2, 4.2, 4.2, 2.2]),
            "col2": np.array([1, 1, 1, 1]),
            "col3": np.array([1, 2, 2, 2]),
        }
    )


###########################################
#     Tests for TableOfContentSection     #
###########################################


def test_table_of_content_section_str(dataframe: pd.DataFrame) -> None:
    assert str(TableOfContentSection(DuplicatedRowSection(frame=dataframe))).startswith(
        "TableOfContentSection("
    )


def test_table_of_content_section_get_statistics(dataframe: pd.DataFrame) -> None:
    section = TableOfContentSection(DuplicatedRowSection(frame=dataframe))
    assert objects_are_equal(section.get_statistics(), {"num_rows": 4, "num_unique_rows": 3})


def test_table_of_content_section_get_statistics_columns(dataframe: pd.DataFrame) -> None:
    section = TableOfContentSection(DuplicatedRowSection(frame=dataframe, columns=["col2", "col3"]))
    assert objects_are_equal(section.get_statistics(), {"num_rows": 4, "num_unique_rows": 2})


def test_table_of_content_section_get_statistics_empty_row() -> None:
    section = TableOfContentSection(
        DuplicatedRowSection(frame=pd.DataFrame({"col1": [], "col2": []}))
    )
    assert objects_are_equal(section.get_statistics(), {"num_rows": 0, "num_unique_rows": 0})


def test_table_of_content_section_get_statistics_empty_column() -> None:
    section = TableOfContentSection(DuplicatedRowSection(frame=pd.DataFrame({})))
    assert objects_are_equal(section.get_statistics(), {"num_rows": 0, "num_unique_rows": 0})


def test_table_of_content_section_render_html_body(dataframe: pd.DataFrame) -> None:
    section = TableOfContentSection(DuplicatedRowSection(frame=dataframe))
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_table_of_content_section_render_html_body_empty_row() -> None:
    section = TableOfContentSection(
        DuplicatedRowSection(
            frame=pd.DataFrame({"col1": [], "col2": []}),
        )
    )
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_table_of_content_section_render_html_body_empty_column() -> None:
    section = TableOfContentSection(DuplicatedRowSection(frame=pd.DataFrame({})))
    assert isinstance(Template(section.render_html_body()).render(), str)


def test_table_of_content_section_render_html_body_args(
    dataframe: pd.DataFrame,
) -> None:
    section = TableOfContentSection(DuplicatedRowSection(frame=dataframe))
    assert isinstance(
        Template(section.render_html_body(number="1.", tags=["meow"], depth=1)).render(), str
    )


def test_table_of_content_section_render_html_toc(dataframe: pd.DataFrame) -> None:
    section = TableOfContentSection(DuplicatedRowSection(frame=dataframe))
    assert isinstance(Template(section.render_html_toc()).render(), str)


def test_table_of_content_section_render_html_toc_args(
    dataframe: pd.DataFrame,
) -> None:
    section = TableOfContentSection(DuplicatedRowSection(frame=dataframe))
    assert isinstance(
        Template(section.render_html_toc(number="1.", tags=["meow"], depth=1)).render(), str
    )
