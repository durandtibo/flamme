r"""Contain the implementation of a section to analyze the most frequent
values for a given columns."""

from __future__ import annotations

__all__ = ["MostFrequentValuesSection"]

import logging
from typing import TYPE_CHECKING

from coola.utils import repr_indent, repr_mapping
from jinja2 import Template

from flamme.section.base import BaseSection
from flamme.section.utils import (
    GO_TO_TOP,
    render_html_toc,
    tags2id,
    tags2title,
    valid_h_tag,
)

if TYPE_CHECKING:
    from collections import Counter
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class MostFrequentValuesSection(BaseSection):
    r"""Implement a section that analyzes the most frequent values for a
    given columns.

    Args:
        counter: The counter with the number of occurrences
            for all values.
        column: The column name.
        top: The maximum number of values to show.

    Example usage:

    ```pycon

    >>> from collections import Counter
    >>> from flamme.section import MostFrequentValuesSection
    >>> section = MostFrequentValuesSection(
    ...     counter=Counter({"a": 4, "b": 2, "c": 6}), column="col"
    ... )
    >>> section
    MostFrequentValuesSection(
      (counter): Counter({'c': 6, 'a': 4, 'b': 2})
      (column): col
      (top): 100
      (total): 12
    )
    >>> section.get_statistics()
    {'most_common': [('c', 6), ('a', 4), ('b', 2)]}

    ```
    """

    def __init__(self, counter: Counter, column: str, top: int = 100) -> None:
        self._counter = counter
        self._column = column
        self._top = top

        self._total = sum(self._counter.values())

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping(
                {
                    "counter": self._counter,
                    "column": self._column,
                    "top": self._top,
                    "total": self._total,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def get_statistics(self) -> dict:
        return {"most_common": list(self._counter.most_common(self._top))}

    def render_html_body(self, number: str = "", tags: Sequence[str] = (), depth: int = 0) -> str:
        logger.info("Rendering the most frequent values section...")
        return Template(self._create_template()).render(
            {
                "go_to_top": GO_TO_TOP,
                "id": tags2id(tags),
                "depth": valid_h_tag(depth + 1),
                "title": tags2title(tags),
                "section": number,
                "table": self._create_table(),
                "column": self._column,
                "top": f"{self._top:,}",
            }
        )

    def render_html_toc(
        self, number: str = "", tags: Sequence[str] = (), depth: int = 0, max_depth: int = 1
    ) -> str:
        return render_html_toc(number=number, tags=tags, depth=depth, max_depth=max_depth)

    def _create_template(self) -> str:
        return """
<h{{depth}} id="{{id}}">{{section}} {{title}} </h{{depth}}>

{{go_to_top}}

<p style="margin-top: 1rem;">
This section analyzes the {{top}} most frequent values in <em>{{column}}</em>.

<ul>
  <li> <b>count</b>: is the number of occurrences of the value </li>
  <li> <b>percentage</b>: is the number of occurrences the value divided by the total number of occurrences </li>
  <li> <b>cumulative percentage</b>: is the sum of the percentage of occurrence for the value plus all the previous values in the table. </li>
</ul>

{{table}}
<p style="margin-top: 1rem;">
"""

    def _create_table(self) -> str:
        most_common = list(self._counter.most_common(self._top))
        rows = []
        cumcount = 0
        for value, count in most_common:
            cumcount += count
            rows.append(
                create_table_row(value=value, count=count, total=self._total, cumcount=cumcount)
            )
        return Template(
            """
<table class="table table-hover table-responsive w-auto" >
    <thead class="thead table-group-divider">
        <tr>
            <th>value</th>
            <th>count</th>
            <th>percentage (%)</th>
            <th>cumulative percentage (%)</th>
        </tr>
    </thead>
    <tbody class="tbody table-group-divider">
        {{rows}}
        <tr class="table-group-divider"></tr>
    </tbody>
</table>
"""
        ).render({"rows": "\n".join(rows)})


def create_table_row(value: str, count: int, total: int, cumcount: int) -> str:
    r"""Create the HTML code of a new table row.

    Args:
        value: Specifies a string representation of the value.
        count: The number of occurrences of the value.
        total: The total number of occurrences.
        cumcount: The cumulative number of occurrences.

    Returns:
        The HTML code of a row.
    """
    return Template(
        """<tr>
    <th>{{value}}</th>
    <td {{num_style}}>{{count}}</td>
    <td {{num_style}}>{{percentage}}</td>
    <td {{num_style}}>{{cum_percentage}}</td>
</tr>"""
    ).render(
        {
            "num_style": 'style="text-align: right;"',
            "value": value,
            "count": f"{count:,}",
            "percentage": f"{100 * count / total:.2f}",
            "cum_percentage": f"{100 * cumcount / total:.2f}",
        }
    )
