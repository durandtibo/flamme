from __future__ import annotations

import logging
from unittest.mock import patch

import pytest

from flamme.utils.logging import configure_logging


@pytest.fixture(autouse=True)
def _reset_logging() -> None:
    logging.basicConfig()


#######################################
#     Tests for configure_logging     #
#######################################


def test_configure_logging() -> None:
    configure_logging()


@pytest.mark.parametrize("level", [logging.INFO, logging.WARNING, logging.ERROR])
def test_configure_logging_level(level: int) -> None:
    with patch("flamme.utils.logging.logging.basicConfig") as bc:
        configure_logging(level)
        assert bc.call_args.kwargs["level"] == level
