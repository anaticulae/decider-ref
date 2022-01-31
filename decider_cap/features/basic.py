# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import iamraw
import protocol
import utila

import decider_cap.driver


def work(
    captions: str,
    docinfo: iamraw.DocInfo,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = decider_cap.driver.create_driver(captions, pages=pages)
    result = protocol.run(
        modulename=__name__,
        driver=driver,
        document=docinfo,
    )
    return result


SOLUTION_6200 = """\
Unterschrift mehrfach verwendet

Die Unterschrift **{{line}}** wurde **{{count}}-mal** auf den Seiten \
{{pages}} erkannt. Überprüfen Sie ob dies korrekt ist.
"""


def check_6200_duplication(linter: callable, driver):
    collected = collections.defaultdict(list)
    for pagecaption in driver.captions:
        for caption in pagecaption.content:
            # TODO: DECIDE BETWEEN LABEL AND CAPTION TEXT
            collected[caption.text].append(pagecaption.page)
    for key, value in collected.items():
        if len(value) <= 1:
            continue
        pages = utila.from_tuple(utila.make_unique(value), ',')
        linter(
            line=key,
            count=len(value),
            pages=pages,
        )
