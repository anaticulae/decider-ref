# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protoerror
import utilo

import caption_.driver


def work(
    captions: str,
    docinfo: iamraw.DocInfo,
    pages: tuple = None,
) -> protoerror.ResultType:
    driver = caption_.driver.create_driver(
        captions,
        pages=pages,
    )
    result = protoerror.run(
        modulename=__name__,
        driver=driver,
        document=docinfo,
    )
    return result


SOLUTION_6250 = """\
Unterschrift auf nächster Seite

Die Unterschrift **{{text}}** befindet sich nicht auf einer Seite mit \
dem beschriebenen Objekt.

# TODO: ADD TECHNIQUE HINT
"""


def check_6250_overlap(linter: callable, driver):
    for item in utilo.flatten_content(driver.captions):
        if not item.overlap:
            continue
        linter(
            text=item.raw,
            location=iamraw.Location.from_page(item.pdfpage),
        )
