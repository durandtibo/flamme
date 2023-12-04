from __future__ import annotations

from pathlib import Path

from pandas import DataFrame
from pytest import TempPathFactory, fixture

from flamme.analyzer import NullValueAnalyzer
from flamme.ingestor import ParquetIngestor
from flamme.preprocessor import SequentialPreprocessor
from flamme.reporter import Reporter


@fixture(scope="module")
def df_path(tmp_path_factory: TempPathFactory) -> Path:
    path = tmp_path_factory.mktemp("data").joinpath("df.parquet")
    df = DataFrame(
        {
            "col1": [1, 2, 3, 4, 5],
            "col2": ["a", "b", "c", "d", "e"],
            "col3": [1.2, 2.2, 3.2, 4.2, 5.2],
        }
    )
    df.to_parquet(path)
    return path


##############################
#     Tests for Reporter     #
##############################


def test_reporter_str(df_path: Path, tmp_path: Path) -> None:
    report_path = tmp_path.joinpath("report.html")
    assert str(
        Reporter(
            ingestor=ParquetIngestor(df_path),
            preprocessor=SequentialPreprocessor(preprocessors=[]),
            analyzer=NullValueAnalyzer(),
            report_path=report_path,
        )
    ).startswith("Reporter(")


def test_reporter_compute(df_path: Path, tmp_path: Path) -> None:
    report_path = tmp_path.joinpath("report.html")
    Reporter(
        ingestor=ParquetIngestor(df_path),
        preprocessor=SequentialPreprocessor(preprocessors=[]),
        analyzer=NullValueAnalyzer(),
        report_path=report_path,
    ).compute()
    assert report_path.is_file()
