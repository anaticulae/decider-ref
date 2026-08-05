# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elementae
import elementae.headline.lookup
import iamraw
import protoerror
import utilo

import decider_toc.features
import decider_toc.level as dtl


def work(toc: str, sections: str) -> protoerror.ResultType:
    driver = decider_toc.features.create_driver(
        toc=toc,
        sections=sections,
    )
    result = protoerror.run(
        __name__,
        driver=driver,
        location=protoerror.OVERVIEW,
    )
    return result


SOLUTION_1350 = """\
Kapitel enthält zu wenige Sektionen

Ein Kapitel oder eine Sektion benötigt mindestens zwei \
Teilüberschriften. Falls dies nicht moeglich ist, sollte das \
Unterkapitel in den Text eingeplegt werden.

{elemente/inhaltsverzeichnis#kapitelstruktur}
"""


def check_1350_toc_level_to_few_children(linter, driver):
    toc: iamraw.Toc = driver.toc
    level_result: dtl.TocValidationResult = dtl.validate(toc)
    for item in level_result.too_few_children:  # pylint:disable=E1133
        # TODO: REMOVE AFTER UPGRADING SERIALIZERAW
        try:
            location = iamraw.Location.from_page(int(item.page))
        except ValueError:
            # TODO: THINK ABOUT CONCEPT TO HANDLE ROMAN PAGE NUMBERS
            # TODO: INTRODUCE RAW LOCATION?
            utilo.error(f'could not convert roman page number: {item.page}')
            continue
        linter(location=location)


SOLUTION_1360 = """\
Inhaltsverzeichnis enthält nicht nur aufsteigende Seitenzahlen

Korrigieren Sie das Inhaltsverzeichnis bzw. die Seitenzahlen.

Zeile: {{text}}
Seite {{current}} folgt auf {{before}}.

{darstellung/seitenzahlen#anforderungen}
"""


def check_1360_toc_ascending_pages(linter, driver):
    toc: iamraw.Toc = driver.toc
    page_result: elementae.InvalidPages = elementae.validate_toc(toc)
    # TODO: ADD SPECIAL CASE FOR elementae.INVALID_ROMAN_NUMBER
    for item in page_result:
        location = iamraw.Location.from_page(item.raw_location)
        linter(
            current=item.current,
            before=item.before,
            text=item.text,
            location=location,
        )


SOLUTION_1365 = """\
Eidesstattliche Erklärung als Teil der Arbeit

Die Eidesstatttliche Erklärung ist kein Teil der Prüfungsleistung und \
wird somit nicht im Inhaltsverzeichnis aufgeführt und wird ebenfalls \
nicht bei der Seitenzählung berücksichtigt.

{elemente/erklaerung}
"""


def check_1365_toc_legal_inside_toc(linter, driver):
    toc: iamraw.Toc = driver.toc
    if not toc:
        return
    toc = elementae.toc_flat(toc)

    legal_intoc = [item for item in toc if islegal(item.title)]
    if not legal_intoc:
        return

    location = iamraw.Location.from_page(legal_intoc[0].raw_location)
    linter(location=location)

    if len(legal_intoc) >= 2:
        utilo.error(f'multiple legal toc detected {legal_intoc}')


LEGAL = elementae.headline.lookup.LEGAL


def islegal(item: str) -> bool:
    return utilo.similar(LEGAL, item, maxdiff=0.95)


SOLUTION_1366 = """\
Abstract an den Anfang

Das Abstrac/k???t dient zum ersten Kontakt des Lesenden. Daher bietet es \
sich an dies ganz an den Anfang der Arbeit zu stellen.

Falls die Prürfungsordnung dies anders sieht, bitte orientieren Sie sich \
an dieser.

{elemente/abstract}
"""


def check_1366_abstract_position(linter, driver):
    if not driver.sections:
        return
    sections = utilo.flat(driver.sections)
    # TODO: USE COUNT LATER
    abstract = utilo.select_type(sections, iamraw.Abstract)
    if not abstract:
        return
    abstract = abstract[0]
    # TODO: MAKE DOCUMENT LENGTH DEPEDENT
    # lastpage = sections[-1].end
    if abstract.start < 20:  # TODO: HOLY VALUE
        return
    location = iamraw.Location.from_page(abstract.start)
    linter(location=location)
