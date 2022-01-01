# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
""".. _decider_features_toc:

Table of content
================
"""

import collections

import protocol
import utila

import decider_toc.features


def work(toc: str, outlines: str, headlines: str = None) -> protocol.ResultType:
    driver = decider_toc.features.create_driver(
        toc,
        outlines,
        headlines=headlines,
    )
    result = protocol.run(__name__, driver=driver)
    return result


# TODO: ADD SOLUTION_1300_MS to link how to create table of content in word
# TODO: ADD SOLUTION_1300_LATEX to link how to create table of content in LATEX

SOLUTION_1300 = """\
Dokument enthält kein Inhaltsverzeichnis

Fügen Sie ein Inhaltsverzeichnis zum Dokument hinzu.

TODO: ADD LINK TO TECHNIK

{elemente/inhaltsverzeichnis}
"""


def check_1300_toc_existence(linter, driver):
    toc = driver.toc
    if toc.children:
        return
    linter(location=protocol.OVERVIEW)


SOLUTION_1301 = """\
PDF enthält keine Navigation

TODO: ADD LINK TO TECHNIK

{elemente/inhaltsverzeichnis}
"""


def check_1301_outlines_existence(linter, driver):
    outlines = driver.outlines
    if outlines:
        return
    linter(location=protocol.OVERVIEW)


SOLUTION_1310 = """\
Inhaltsverzeichnis inkonsistent

Mehrdeutige Bereichsnummber:
* {{first}}
* {{second}}
"""


def check_1310_duplicated_level(linter, driver):
    headlines = driver.headlines
    if not headlines:
        return
    headlines = utila.flatten(headlines)
    duplicated = collections.defaultdict(list)
    for headline in headlines:
        key = headline.raw_level.strip() if headline.raw_level else None
        if not key:
            continue
        duplicated[key].append(headline)
    for pair in duplicated.values():
        if len(pair) == 1:
            continue
        first, second = pair[0].raw, pair[1].raw
        linter(
            first=shorten(first),
            second=shorten(second),
            location=protocol.OVERVIEW,
        )


def shorten(text, length_max: int = 30) -> str:
    """\
    >>> shorten('ABCDEFGHIJKLMNOPRSTUVWXYZ', length_max=20)
    'ABCDEFGHIJ [...] STUVWXYZ'
    """
    text = text.strip()
    if len(text) < length_max:
        return text
    text = text[0:length_max // 2] + ' [...] ' + text[length_max // 2 + 7:]
    return text
