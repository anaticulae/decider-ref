# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Sync
====

TOC - Outlines
TOC - Content

Verify:
    - level
    - text
    - page number

TODO: ADD SOLUTION TO COMPARE TOC AND OUTLINES
"""

import os

import elementae
import elementae.headline.lookup
import iamraw
import protoerror
import serializeraw
import utilo


def work(
    toc: str,
    outlines: str,
    headlines: str,
    headlines_oneline: str,
) -> protoerror.ResultType:
    driver = create_driver(
        toc,
        outlines,
        headlines,
        headlines_oneline,
    )
    result = protoerror.run(
        __name__,
        driver=driver,
    )
    return result


def create_driver(toc, outlines, headlines, headlines_oneline):
    if utilo.exists(toc):
        toc: iamraw.Toc = serializeraw.load_toc(toc)
    else:
        toc: iamraw.Toc = iamraw.Toc()
    if utilo.exists(outlines):
        outlines = serializeraw.load_toc(outlines)
    else:
        outlines = None
    if utilo.exists(headlines):
        headlines = load_headlines(headlines, headlines_oneline)
    else:
        headlines = None
    driver = protoerror.driver(
        toc=toc,
        outlines=outlines,
        headlines=headlines,
    )
    return driver


def load_headlines(normal: str, oneline: str):
    headlines, headlines_oneline = [], []
    if os.path.exists(normal):
        headlines = serializeraw.load_headlines(normal)
    if os.path.exists(oneline):
        headlines_oneline = serializeraw.load_headlines(oneline)

    if len(headlines) > len(headlines_oneline):
        return headlines
    return headlines_oneline


SOLUTION_1330 = """\
Inhaltsverzeichnis nicht aktuell

Die im Inhaltsverzeichnis verzeichneten Kapitelüberschriften weichen von \
dem im Dokument enthaltenen Überschriften ab. Akutallisieren Sie das \
Inhaltsverzeichnis.

Folgende Überschriften sind nicht im Inhaltsverzeichnis enthalten:

{{missing}}
"""


def check_1330_toc_document_sync(linter, driver):
    toc = driver.toc
    if not toc:
        utilo.error('no toc')
        return
    headlines = driver.headlines
    if not headlines:
        utilo.error('no headlines given')
        return
    headlines = iamraw.headlines_totoc(headlines)
    toc_firstpage = min((item.raw_location for item in toc))
    toc = elementae.toc_flat(toc)
    headlines = elementae.toc_flat(headlines)  # pylint:disable=R0204
    # TODO: ADD BETTER TOC SYNC TO COMPARE CORRECT LEVEL
    # TODO: RENAME VARIABLES
    # compare first level
    toc_firstlevel = [item.title for item in toc]
    document_firstlevel = [item.title for item in headlines]
    if toc_firstlevel == document_firstlevel:
        # all first level headlines in toc are equal to detected headlines
        # in document
        return
    missing = [
        item for item in document_firstlevel if item not in toc_firstlevel
    ]
    # It is not required to have headline `Inhaltsverzeichnis` in table of
    # content.
    # TODO: Add logging?
    missing = not_missing(missing)
    if not missing:
        return
    missing = utilo.NEWLINE.join([f'* {item}' for item in missing])
    linter(location=iamraw.Location.from_page(toc_firstpage), missing=missing)


def not_missing(items: list) -> list:
    return [
        item for item in items
        if not utilo.verysimilar(item, expected=elementae.headline.lookup.TOC)
    ]
