# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BibliographyReference
=====================

Sorting
-------

Theissen
~~~~~~~~

We sort by family name and as tiebreaker by year.
If no name is given, we use `o. V. = ohne Verfasser` instead.
If no year is given, we sort it after the items with year.

Publication without a person as authors, Siemens for example, arg
treated as normal author but there must (Hrsg.) added.

# TODO: ADD OTHER SORTING AS THEISSEN recommends
"""

import iamraw
import utila


def theissen_sort(items):
    """We sort by family name and as tiebraker by year. If no name is
    given, we use `o. V. = ohne Verfasser` instead. If no year is given,
    we sort it after the items with year(INF year)."""
    # sort by year
    items = sorted(
        items,
        key=lambda x: utila.INF if x.year in ('no year', None) else x.year,
    )
    # sort by author name
    items = sorted(items, key=author)
    return items


def author(item: iamraw.BibliographyReference) -> str:
    if not item.authors:
        return 'o. V.'
    if item.author:
        # Person
        return utila.replace(item.author).lower()
    # NoPerson
    return item.authors[0].raw.lower()
