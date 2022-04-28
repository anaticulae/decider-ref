# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol
import serializeraw
import utila


def work(
    captionx: str,
    coderox: str,
    tablerox: str,
    figureox: str,
    pages: tuple,
) -> protocol.ResultType:
    driver = create_driver(
        caption=captionx,
        codero=coderox,
        figureo=figureox,
        tablero=tablerox,
        pages=pages,
    )
    result = protocol.run(
        modulename=__name__,
        driver=driver,
    )
    return result


SOLUTION_6300 = """\
Unterschrift fehlt

Es wurde keine Unterschrift erkannt.
"""
SOLUTION_6301 = SOLUTION_6300
SOLUTION_6302 = SOLUTION_6300


def check_6300_missing_figure_caption(linter: callable, driver):
    if not driver.figureo:
        utila.debug('no figures, skip 6300')
        return
    captions = {item.reference for item in driver.caption}
    for figure in driver.figureo:
        if figure.identifier in captions:
            continue
        location = iamraw.Location.from_page(figure.page)
        linter(location=location)


def check_6301_missing_codero_caption(linter: callable, driver):
    if not driver.codero:
        utila.debug('no codero, skip 6301')
        return
    captions = {item.reference for item in driver.caption}
    for codero in driver.codero:
        if codero.identifier in captions:
            continue
        location = iamraw.Location.from_page(codero.page)
        linter(location=location)


def check_6302_missing_tablero_caption(linter: callable, driver):
    if not driver.tablero:
        utila.debug('no tablero, skip 6302')
        return
    captions = {item.reference for item in driver.caption}
    for tablero in driver.tablero:
        if tablero.identifier in captions:
            continue
        location = iamraw.Location.from_page(tablero.page)
        linter(location=location)


def create_driver(
    caption: str,
    codero: str,
    figureo: list,
    tablero: str,
    pages: tuple,
):
    if utila.exists(caption):
        caption = serializeraw.load_captions(caption, pages=pages)
        caption = utila.flatten_content(caption)
    else:
        caption = []
    if utila.exists(codero):
        codero = serializeraw.load_codes(codero, pages=pages)
        codero = utila.flatten_content(codero)
    else:
        codero = []
    if utila.exists(figureo):
        figureo = serializeraw.load_figures(path=figureo)
    else:
        figureo = []
    if utila.exists(tablero):
        tablero = serializeraw.load_tables(tablero, pages=pages)
        tablero = utila.flatten_content(tablero)
    else:
        tablero = []
    result = protocol.driver(
        codero=codero,
        figureo=figureo,
        tablero=tablero,
        caption=caption,
    )
    return result
