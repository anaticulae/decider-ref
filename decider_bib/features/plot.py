# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import painter
import utila

import decider_bib.order
import decider_bib.serialize


def work(table: str) -> bytes:
    bibliography = decider_bib.serialize.load_bibliography_reference(table)

    rendered = render_year_overview(bibliography)
    return rendered


def render_year_overview(bibliography, year_min=1970, year_max=2025) -> bytes:
    year = [item.year for item in bibliography]
    year = [item for item in year if utila.isnumber(item)]
    # filter invalid years
    year = [item for item in year if year_min <= item < year_max]
    # TODO: DISPLAY EXCLUDES YEAR
    # TODO: DISPLAY VERY OLD YEARS ON THE BORDER OF THE IMAGE
    year, counted = count(year)
    rendered = painter.bar_render(
        x=year,
        y=counted,
        width=15.0,
        height=0.75 * golden(15.0),
        grid=True,
        title='Bibliographie',
        xlabel='Jahr',
        ylabel='Anzahl',
    )
    raw = painter.png(rendered)
    return raw


def golden(longest: float) -> float:
    # TODO: REPLACE WITH UTILA
    return longest / 1.618


def count(items) -> tuple:
    counter = collections.defaultdict(int)
    for item in items:
        counter[item] += 1
    first, second = [], []
    for key in sorted(counter.keys()):
        first.append(key)
        second.append(counter[key])
    return first, second
