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

import decider_cap.basic
import decider_cap.driver


def work(
    captions: str,
    docinfo: iamraw.DocInfo,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = decider_cap.driver.create_driver(
        captions,
        pages=pages,
    )
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


SOLUTION_6201 = """\
Unterschriften der Abbildungen falsch numeriert

{{advice}}
"""

SOLUTION_6202 = """\
Unterschriften der Tabellen falsch numeriert

{{advice}}
"""

SOLUTION_6203 = """\
Unterschriften der Codes falsch numeriert

{{advice}}
"""


def check_6201_order_figures(linter: callable, driver):
    decider_cap.basic.check_order(driver.figures, linter)


def check_6202_order_tables(linter: callable, driver):
    decider_cap.basic.check_order(driver.tables, linter)


def check_6203_order_codes(linter: callable, driver):
    decider_cap.basic.check_order(driver.codes, linter)


SOLUTION_6205 = """\
Unterschrift endet nicht mit einem Punkt

{{text}}
"""
SOLUTION_6206 = SOLUTION_6205
SOLUTION_6207 = SOLUTION_6205


def check_6205_dotted_figures(linter: callable, driver):
    decider_cap.basic.check_dotted(driver.figures, linter)


def check_6206_dotted_tables(linter: callable, driver):
    decider_cap.basic.check_dotted(driver.tables, linter)


def check_6207_dotted_codes(linter: callable, driver):
    decider_cap.basic.check_dotted(driver.codes, linter)


SOLUTION_6210 = """\
Unterschrift startet nicht mit einem Großbuchstaben

{{text}}
"""
SOLUTION_6211 = SOLUTION_6210
SOLUTION_6212 = SOLUTION_6210


def check_6210_upper_figures(linter: callable, driver):
    decider_cap.basic.check_upper(driver.figures, linter)


def check_6211_upper_tables(linter: callable, driver):
    decider_cap.basic.check_upper(driver.tables, linter)


def check_6212_upper_codes(linter: callable, driver):
    decider_cap.basic.check_upper(driver.codes, linter)


SOLUTION_6220 = """\
Unterschrift zu lang

Die Unterschrift **{{text}}** ist zu lang und sollte verkürzt \
werden.
"""
SOLUTION_6221 = SOLUTION_6220
SOLUTION_6222 = SOLUTION_6220


def check_6220_length_figures(linter: callable, driver):
    decider_cap.basic.check_length(driver.figures, linter)


def check_6221_length_tables(linter: callable, driver):
    decider_cap.basic.check_length(driver.tables, linter)


def check_6222_length_codes(linter: callable, driver):
    decider_cap.basic.check_length(driver.codes, linter)
