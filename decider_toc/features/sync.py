# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import iamraw
import protocol
import serializeraw
import utila


def work(
        tableofcontent: str,
        outlines: str,
        headlines: str,
        headlines_oneline: str,
) -> protocol.ResultType:
    tableofcontent: iamraw.Toc = serializeraw.load_toc(tableofcontent)
    outlines = serializeraw.load_toc(outlines)
    headlines = load_headlines(headlines, headlines_oneline)

    driver = protocol.driver(
        toc=tableofcontent,
        outlines=outlines,
        headlines=headlines,
    )

    result = protocol.run(__name__, driver=driver)
    return result


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

Die im Inhaltsverzeichnis verzeichneten Kapitelüberschriften weichen von
dem im Dokument enthaltenen Überschriften ab. Akutallisieren Sie das
Inhaltsverzeichnis.

Folgende Überschriften sind nicht im Inhaltsverzeichnis enthalten:

{{missing}}
"""


def check_1330_toc_document_sync(linter, driver):
    toc = driver.toc
    if not toc:
        utila.error('no toc')
        return
    headlines = driver.headlines
    if not headlines:
        utila.error('no headlines given')
        return
    headlines = iamraw.headlines_totoc(headlines)
    toc_firstpage = min([item.raw_location for item in toc])

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
    missing = utila.NEWLINE.join([f'* {item}' for item in missing])
    linter(location=iamraw.Location.from_page(toc_firstpage), missing=missing)


def not_missing(items: list) -> list:
    skip = {
        'inhalt',
        'inhaltsverzeichnis',
        'table of content',
        'table of contents',
    }
    return [item for item in items if item.lower() not in skip]
