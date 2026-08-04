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

import configos
import iamraw
import protoerror
import utilo

import decider_toc.features


def work(toc: str,
         outlines: str,
         headlines: str = None) -> protoerror.ResultType:
    driver = decider_toc.features.create_driver(
        toc,
        outlines,
        headlines=headlines,
    )
    result = protoerror.run(__name__, driver=driver)
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
    linter(location=protoerror.OVERVIEW)


SOLUTION_1301 = """\
PDF enthält keine Navigation

TODO: ADD LINK TO TECHNIK

{elemente/inhaltsverzeichnis}
"""


def check_1301_outlines_existence(linter, driver):
    outlines = driver.outlines
    if outlines:
        return
    linter(location=protoerror.OVERVIEW)


SOLUTION_1305 = """\
Überschrift ohne Inhalt

Die Überschrift {{headline}} ist so allgemein, dass Sie nur eine geringe \
bzw. keine Information aufweist.

Denken Sie über eine konkretere Überschrift nach, die der Leserin in der \
Orientierung in der Arbeit weiter hilft.

{elemente/inhaltsverzeichnis}
"""


def check_1305_headlines_without_sense(linter, driver):
    if not driver.headlines:
        return
    headlines = utilo.flat(driver.headlines)
    for item in headlines:
        title = item.title.lower()
        if not title in NO_CONTENT:
            continue
        # TODO: USE PDFPAGE LATER
        location = iamraw.Location.from_page(item.page)
        linter(
            headline=item.title,
            location=location,
        )


NO_CONTENT = utilo.splitlines("""
ALLGEMEINES
ALLGEMEIN
SONSTIGES
ÜBERBLICK
""")

SOLUTION_1310 = """\
Inhaltsverzeichnis inkonsistent

Mehrdeutige Bereichsnummber:
* {{first}}
* {{second}}
"""

SHORTEN_LEGNTH_MAX = configos.HV_INT_PLUS(default=30)


def check_1310_duplicated_level(linter, driver):
    headlines = driver.headlines
    if not headlines:
        return
    headlines = utilo.flat(headlines)
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
            first=utilo.shrink(first, maxlength=SHORTEN_LEGNTH_MAX),
            second=utilo.shrink(second, maxlength=SHORTEN_LEGNTH_MAX),
            location=protoerror.OVERVIEW,
        )


SOLUTION_R1315 = """\
Inhaltsverzeichnis Stil überdenken

Sie verwenden das Abstufungsprinzip. Durch Verwendung des Linienprinzips \
ist eine eindeutigere Struktur möglich.

{elemente/inhaltsverzeichnis}
"""


def check_1315_stepped_toc(linter, driver):
    toc: iamraw.Toc = driver.toc
    if not toc:
        return
    if toc.style != iamraw.TocStyle.STEPPED:
        return
    linter(location=protoerror.OVERVIEW)
