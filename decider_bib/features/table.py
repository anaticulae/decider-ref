# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import iamraw
import protocol
import utila

import decider_bib.order
import decider_bib.serialize
import decider_bib.utils


def work(table: str) -> typing.Tuple[str, str]:
    bibliography = decider_bib.serialize.load_bibliography_reference(table)
    driver = protocol.driver(bibliography=bibliography)
    linter = protocol.from_module(__name__)
    linting(linter, driver)
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(linter: protocol.Linter, driver):
    location = iamraw.Location.from_page(0)
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        call = functools.partial(
            linter.add_finding,
            msgid=checker.msgid,
            location=location,
        )
        checker(call, driver)


SOLUTION_6000 = """\
Quellenverzeichnis ist nicht alphabetisch sortiert

Sortieren Sie das Quellenverzeichnis.

Gefunden:
---------
{{current}}

Erwartet:
---------
{{expected}}

{elemente/literaturverzeichnis}
"""


def check_6000_not_sorted_alphabetically(linter: callable, driver):
    references: iamraw.BibliographyReferences = driver.bibliography
    current = [item for item in references]
    expected = decider_bib.order.theissen_sort(current)

    if current == expected:
        return

    # TODO: CHECK REPRESENTATION
    current = [decider_bib.utils.format_bibline(item) for item in current]
    expected = [decider_bib.utils.format_bibline(item) for item in expected]

    linter(
        current=utila.NEWLINE.join(current),
        expected=utila.NEWLINE.join(expected),
    )
