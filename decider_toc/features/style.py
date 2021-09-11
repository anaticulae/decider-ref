# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol

import decider_toc.duplicated
import decider_toc.marks


def work(toc: str) -> protocol.ResultType:
    driver = decider_toc.features.create_driver(toc)
    try:
        pdflocation = driver.toc[0].raw_location  # pylint:disable=E1101
    except IndexError:
        pdflocation = protocol.OVERVIEW.page
    result = protocol.run(
        __name__,
        driver=driver,
        location=iamraw.Location.from_page(pdflocation),
    )
    return result


SOLUTION_1380 = """\
Worthäufung im Inhaltsverzeichnis

Das Wort „{{word}}“ wird {{count}} mal in den Zeilen {{lines}} benutzt. \
Überprüfen Sie Dokumentenstruktur oder variieren Sie gegebenenfalls \
dieses Wort um die Varianz der Sprache zu vergrößern.
"""


def check_1380_toc_duplicated_words(linter, driver):
    toc: iamraw.Toc = driver.toc
    findings = decider_toc.duplicated.validate(toc)
    for item in findings:
        (word, count), lines = item
        lines = ', '.join([f'{item}' for item in lines])
        # location = iamraw.Location.from_page(item.raw_location)
        linter(
            word=word,
            count=count,
            lines=lines,
        )


# TODO: ADD ARTICLE
SOLUTION_1383 = """\
Sektion enthält Fragestellung

Die Überschrift **{{title}}** ist als Frage formuliert.

Überschriften zeichnen sich durch Knappheit und Eindeutigkeit aus. Daher \
sollten diese substantivisch, kurz und prägnant und nicht als Teilsatz oder \
Fragesatz formuliert werden.
"""


def check_1383_toc_contains_question_mark(linter, driver):
    toc: iamraw.Toc = driver.toc
    findings = decider_toc.marks.validate_question_mark(toc)
    for item in findings:
        _, title, raw_location = item
        location = iamraw.Location.from_page(raw_location)
        linter(title=title, location=location)


# TODO: ADD ARTICLE
SOLUTION_1384 = """\
Sektion enthält Anführungszeichen

Die Überschrift **{{title}}** enhält Anführungszeichen. Dies \
deutet auf eine spezielle Bedeutung hin. Dies sollte vermieden werden, \
da Überschriften, kurz, prägnant und substantivisch formuliert sein sollen.

Überlegen Sie, wie die Sektion prägnanter und ohne spezielles Vorwissen \
verständlich wird.
"""


def check_1384_toc_contains_quotation_mark(linter, driver):
    toc: iamraw.Toc = driver.toc
    findings = decider_toc.marks.collect_quotation_marks(toc)
    for item in findings:
        _, title, raw_location = item
        location = iamraw.Location.from_page(raw_location)
        linter(title=title, location=location)
