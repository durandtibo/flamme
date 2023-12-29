from __future__ import annotations

__all__ = ["valid_h_tag", "tags2id", "tags2title", "render_html_toc", "auto_yscale_continuous"]

from collections.abc import Sequence

import numpy as np

from flamme.utils.array import nonnan

GO_TO_TOP = '<a href="#">Go to top</a>'


def tags2id(tags: Sequence[str]) -> str:
    r"""Converts a sequence of tags to a string that can be used as ID in
    a HTML file.

    Args:
        tags (``Sequence``): Specifies the sequence of tags.

    Returns:
        str: The generated ID from the tags.
    """
    return "-".join(tags).replace(" ", "-").lower()


def tags2title(tags: Sequence[str]) -> str:
    r"""Converts a sequence of tags to a string that can be used as
    title.

    Args:
        tags (``Sequence``): Specifies the sequence of tags.

    Returns:
        str: The generated title from the tags.
    """
    return " | ".join(tags[::-1])


def valid_h_tag(index: int) -> int:
    r"""Computes a valid number of a h HTML tag.

    Args:
        index (int): Specifies the original value.

    Returns:
        int: A valid value.
    """
    return max(1, min(6, index))


def render_html_toc(
    number: str = "", tags: Sequence[str] = (), depth: int = 0, max_depth: int = 1
) -> str:
    r"""Renders the HTML table of content (TOC) associated to the
    section.

    Args:
        number (str, optional): Specifies the section number
            associated to the section. Default: ""
        tags (``Sequence``, optional): Specifies the tags
            associated to the section. Default: ``()``
        depth (int, optional): Specifies the depth in the report.
            Default: ``0``

    Returns:
        str: The HTML table of content associated to the section.
    """
    if depth >= max_depth:
        return ""
    tag = tags[-1] if tags else ""
    return f'<li><a href="#{tags2id(tags)}">{number} {tag}</a></li>'


def auto_yscale_continuous(array: np.ndarray, nbins: int | None) -> str:
    r"""Finds a good scale for y-axis based on the data distribution.

    Args:
        array: Specifies the data to use to find the scale.
        nbins: Specifies the number of bins in the histogram.

    Returns:
        The scale for y-axis.

    Example usage:

    ```pycon
    >>> import numpy as np
    >>> from flamme.section.utils import auto_yscale_continuous
    >>> auto_yscale_continuous(np.arange(100))
    linear

    ```
    """
    if nbins is None:
        nbins = 100
    array = nonnan(array)
    counts = np.histogram(array, bins=nbins)[0]
    nonzero_count = [c for c in counts if c > 0]
    if len(nonzero_count) <= 2 or (max(nonzero_count) / max(min(nonzero_count), 1)) < 50:
        return "linear"
    if np.nanmin(array) <= 0.0:
        return "symlog"
    return "log"
