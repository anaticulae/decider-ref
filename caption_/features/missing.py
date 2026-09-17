# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import iamraw
import protoerror
import serializeraw
import utilo


def work(
    captionx: str,
    coderox: str,
    tablerox: str,
    figureox: str,
    pages: tuple,
) -> protoerror.ResultType:
    driver = create_driver(
        caption=captionx,
        codero=coderox,
        figureo=figureox,
        tablero=tablerox,
        pages=pages,
    )
    result = protoerror.run(
        modulename=__name__,
        driver=driver,
    )
    return result


SOLUTION_6300 = """\
Abbildung: Unterschrift fehlt

Es wurde keine Unterschrift erkannt.
"""
SOLUTION_6301 = """\
Quellcode: Unterschrift fehlt

Es wurde keine Unterschrift erkannt.
"""
SOLUTION_6302 = """\
Tabelle: Unterschrift fehlt

Es wurde keine Unterschrift erkannt.
"""
SOLUTION_I6303 = """\
Empfehlung: Unterschriften verwenden

Im Dokument werden keine Bild-, Tabellen- oder Quellcodeunterschriften \
verwendet.
"""


def check_6300_missing_figure_caption(linter: callable, driver):
    missing('figureo', 6300, driver, linter)


def check_6301_missing_codero_caption(linter: callable, driver):
    missing('codero', 6301, driver, linter)


def check_6302_missing_tablero_caption(linter: callable, driver):
    missing('tablero', 6302, driver, linter)


NO_CAPTION_COUNT_MIN = configos.HV_INT_PLUS(default=10)

NO_CAPTION_RATE_MIN = configos.HV_PERCENT_PLUS(default=70)


def check_6303_no_caption(linter: callable, driver):
    baselinter: protoerror.Linter = linter.func.__self__
    missing_caption = baselinter.count_findings(msgid=6300)
    missing_caption += baselinter.count_findings(msgid=6301)
    missing_caption += baselinter.count_findings(msgid=6302)
    elementae = sum(
        len(item) for item in (
            driver.codero,
            driver.tablero,
            driver.figureo,
        ))
    if elementae < NO_CAPTION_COUNT_MIN:
        utilo.debug(f'too few elements: {elementae}, disable 6303')
        return
    rate = utilo.rate_rel(missing_caption, elementae)
    if rate < NO_CAPTION_RATE_MIN:
        return
    linter()


def missing(var, msgid: int, driver, linter):
    data = getattr(driver, var)
    if not data:
        utilo.debug(f'no {var}, skip {msgid}')
        return
    captions = {item.reference for item in driver.caption}
    for item in data:
        if item.identifier in captions:
            continue
        location = iamraw.Location.from_page(item.page)
        linter(location=location)


def create_driver(
    caption: str,
    codero: str,
    figureo: list,
    tablero: str,
    pages: tuple,
):
    if utilo.exists(caption):
        caption = serializeraw.load_captions(caption, pages=pages)
        caption = utilo.flatten_content(caption)
    else:
        caption = []
    if utilo.exists(codero):
        codero = serializeraw.load_codes(codero, pages=pages)
        codero = utilo.flatten_content(codero)
    else:
        codero = []
    if utilo.exists(figureo):
        figureo = serializeraw.load_figures(path=figureo)
    else:
        figureo = []
    if utilo.exists(tablero):
        tablero = serializeraw.load_tables(tablero, pages=pages)
        tablero = utilo.flatten_content(tablero)
    else:
        tablero = []
    result = protoerror.driver(
        codero=codero,
        figureo=figureo,
        tablero=tablero,
        caption=caption,
    )
    return result
