# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import konradus
import protoerror
import serializeraw
import utilo

import decider_ref.listdiff


def work(
    abbrev: str,
    intext: str,
    pages: tuple = None,
) -> protoerror.ResultType:
    driver = create_driver(
        abbrev,
        intext,
        pages=pages,
    )
    result = protoerror.run(
        __name__,
        driver,
    )
    return result


def create_driver(abbrev: str, intext: str, pages: tuple = None):
    if utilo.exists(abbrev):
        table = serializeraw.load_abbreviation_table(abbrev)
    else:
        table = iamraw.AbbreviationResult()
    intext = serializeraw.load_text_abbreviations(intext, pages=pages)
    driver = protoerror.driver(
        abbrevtable=table,
        intext=intext,
    )
    return driver


SOLUTION_15010 = """\
Abkürzungsverzeichnis nicht alphabetisch sortiert

Sortieren Sie das Abkürzungsverzeichnis.

{{advice}}

{elemente/abkuerzungsverzeichnis#alphabetische-sortierung}
"""


def check_15010_not_sorted_alphabetically(linter: callable, driver):
    abbreviations: iamraw.AbbreviationResult = driver.abbrevtable
    current = list(abbreviations)
    expected = sorted(
        abbreviations,
        key=lambda x: utilo.alphabetically(x.short),
    )
    if current == expected:
        # well sorted
        return
    location = pagelocation(current[0])
    # prepare viewable format
    current = [format_abbreviation_line(item) for item in current]
    expected = [format_abbreviation_line(item) for item in expected]
    advice = decider_ref.listdiff.diffview(expected, current)
    linter(
        advice=advice,
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
    abbreviations: iamraw.AbbreviationResult = driver.abbrevtable
    for item in abbreviations:
        name = item.short.lower()
        if name not in konradus.ABBREVIATION_LOWER:
            continue
        linter(
            abbreviation=item.short,
            location=pagelocation(item),
        )


SOLUTION_R15016 = """\
Abkürzung nicht vorhanden

Die Abkürzung **{{abbrev}}** ist nicht im Abkürzungsverzeichnis aufgeführt.

{elemente/abkuerzungsverzeichnis#abkurzungsverzeichnis}
"""


def check_15016_abbreviation_missing(linter: callable, driver):
    abbreviations: iamraw.AbbreviationResult = driver.abbrevtable
    if len(abbreviations) == 0:  # pylint:disable=compare-to-zero
        protoerror.skip_method('no abbreviation table')
        return
    references = utilo.flatten_content(driver.intext)
    references = [
        item for item in references
        if item.short.lower() not in konradus.ABBREVIATION_LOWER
    ]
    single = utilo.Single()
    collected = [
        item for item in references if not single.contains(item.short.lower())
    ]
    pdfpage = abbreviations.pdfpages[0]
    location = iamraw.Location.from_page(page=pdfpage)
    for item in collected:
        if abbreviations.short_inside(item.short):
            continue
        linter(
            abbrev=item.short,
            location=location,
        )


def format_abbreviation_line(item) -> str:
    return f' * {item.short} {item.description}'


def pagelocation(item) -> iamraw.Location:
    pagenumber = protoerror.OVERVIEW
    if item.position:
        pagenumber = iamraw.Location.from_page(item.position.page)
    return pagenumber
