# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import konrad
import protocol
import serializeraw
import utila


def work(abbreviation: str) -> protocol.ResultType:
    abbreviation = serializeraw.load_abbreviation_table(abbreviation)
    driver = protocol.driver(abbrtable=abbreviation)

    result = protocol.run(__name__, driver)
    return result


SOLUTION_15010 = """\
Abkürzungsverzeichnis nicht alphabetisch sortiert

Sortieren Sie das Abkürzungsverzeichnis.

Gefunden:
---------
{{current}}

Erwartet:
---------
{{expected}}

{elemente/abkuerzungsverzeichnis#alphabetische-sortierung}
"""


def check_15010_not_sorted_alphabetically(linter: callable, driver):
    abbreviations: iamraw.AbbreviationResult = driver.abbrtable
    current = [item for item in abbreviations]
    expected = sorted(
        abbreviations,
        key=lambda x: utila.alphabetically(x.short),
    )

    if current == expected:
        return

    location = pagelocation(current[0])

    # TODO: CHECK REPRESENTATION
    current = [format_abbreviation_line(item) for item in current]
    expected = [format_abbreviation_line(item) for item in expected]

    linter(
        current=utila.NEWLINE.join(current),
        expected=utila.NEWLINE.join(expected),
        location=location,
    )


SOLUTION_R15015 = """\
Allgemein gültige Abkürzung

Die Abkürzung {{abbreviation}} kann als allgemein gültig angenommen werden und \
muss nicht separat aufgeführt werden. Entfernen Sie die Abkürzung um die \
Übersichtlichkeit des Abkürzungsverzeichnisses zu erhöhen.

{elemente/abkuerzungsverzeichnis#abkurzungsverzeichnis}
"""


def check_15015_abbreviation_not_required(linter: callable, driver):
    """Inform user to remove common abbreviation (exists in DUDEN)."""
    abbreviations: iamraw.AbbreviationResult = driver.abbrtable
    for item in abbreviations:
        name = item.short.lower()
        if name not in konrad.ABBREVIATION_LOWER:
            continue
        linter(
            abbreviation=item.short,
            location=pagelocation(item),
        )


def format_abbreviation_line(item) -> str:
    return f' * {item.short} {item.description}'


def pagelocation(item) -> iamraw.Location:
    pagenumber = protocol.OVERVIEW
    if item.position:
        pagenumber = iamraw.Location.from_page(item.position.page)
    return pagenumber
