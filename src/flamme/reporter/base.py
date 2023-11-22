from __future__ import annotations

__all__ = ["BaseReporter", "is_reporter_config", "setup_reporter"]

import logging
from abc import ABC

from objectory import AbstractFactory
from objectory.utils import is_object_config

logger = logging.getLogger(__name__)


class BaseReporter(ABC, metaclass=AbstractFactory):
    r"""Defines the base class to preprocess a DataFrame.

    Example usage:

    .. code-block:: pycon

        >>> import pandas as pd
        >>> from flamme.reporter import ToNumericPreprocessor
        >>> reporter = ToNumericPreprocessor(columns=["col1", "col3"])
        >>> reporter
        ToNumericPreprocessor(columns=('col1', 'col3'))
        >>> df = pd.DataFrame(
        ...     {
        ...         "col1": [1, 2, 3, 4, 5],
        ...         "col2": ["1", "2", "3", "4", "5"],
        ...         "col3": ["1", "2", "3", "4", "5"],
        ...         "col4": ["a", "b", "c", "d", "e"],
        ...     }
        ... )
        >>> df.dtypes
        col1     int64
        col2    object
        col3    object
        col4    object
        dtype: object
        >>> df = reporter.preprocess(df)
        >>> df.dtypes
        col1     int64
        col2    object
        col3     int64
        col4    object
        dtype: object
    """

    def compute(self) -> None:
        r"""Computes the report.

        Example usage:

        .. code-block:: pycon

            >>> import pandas as pd
            >>> from flamme.reporter import ToNumericPreprocessor
            >>> reporter = ToNumericPreprocessor(columns=["col1", "col3"])
            >>> df = pd.DataFrame(
            ...     {
            ...         "col1": [1, 2, 3, 4, 5],
            ...         "col2": ["1", "2", "3", "4", "5"],
            ...         "col3": ["1", "2", "3", "4", "5"],
            ...         "col4": ["a", "b", "c", "d", "e"],
            ...     }
            ... )
            >>> df.dtypes
            col1     int64
            col2    object
            col3    object
            col4    object
            dtype: object
            >>> df = reporter.preprocess(df)
            >>> df.dtypes
            col1     int64
            col2    object
            col3     int64
            col4    object
            dtype: object
        """


def is_reporter_config(config: dict) -> bool:
    r"""Indicates if the input configuration is a configuration for a
    ``BaseReporter``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
    ----
        config (dict): Specifies the configuration to check.

    Returns:
    -------
        bool: ``True`` if the input configuration is a configuration
            for a ``BaseReporter`` object.

    Example usage:

    .. code-block:: pycon

        >>> from flamme.reporter import is_reporter_config
        >>> is_reporter_config(
        ...     {
        ...         "_target_": "flamme.reporter.ToNumericPreprocessor",
        ...         "columns": ["col1", "col3"],
        ...     }
        ... )
        True
    """
    return is_object_config(config, BaseReporter)


def setup_reporter(
    reporter: BaseReporter | dict,
) -> BaseReporter:
    r"""Sets up an reporter.

    The reporter is instantiated from its configuration
    by using the ``BaseReporter`` factory function.

    Args:
    ----
        reporter (``BaseReporter`` or dict): Specifies an
            reporter or its configuration.

    Returns:
    -------
        ``BaseReporter``: An instantiated reporter.

    Example usage:

    .. code-block:: pycon

        >>> from flamme.reporter import setup_reporter
        >>> reporter = setup_reporter(
        ...     {
        ...         "_target_": "flamme.reporter.ToNumericPreprocessor",
        ...         "columns": ["col1", "col3"],
        ...     }
        ... )
        >>> reporter
        ToNumericPreprocessor(columns=('col1', 'col3'))
    """
    if isinstance(reporter, dict):
        logger.info("Initializing an reporter from its configuration... ")
        reporter = BaseReporter.factory(**reporter)
    if not isinstance(reporter, BaseReporter):
        logger.warning(f"reporter is not a `BaseReporter` (received: {type(reporter)})")
    return reporter
