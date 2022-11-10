# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import protocol
import utila

import decider_toc.balance
import decider_toc.features
import decider_toc.length
import decider_toc.level


def work(
    toc: str,
    magic_pages: str,
    docinfo: iamraw.DocInfo = None,
) -> protocol.ResultType:
    driver = decider_toc.features.create_driver(
        toc=toc,
        docinfo=docinfo,
        magic_pages=magic_pages,
    )
    result = protocol.run(
        __name__,
        driver=driver,
        location=protocol.OVERVIEW,
        document=docinfo,
    )
    return result


def complex_document(document) -> bool:
    if not document:
        return False
    if not document.doctype:
        return False
    if document.doctype in (iamraw.DocumentType.DISS, iamraw.DocumentType.BOOK):
        return True
    return False


SOLUTION_1351 = """\
Gliederung zu komplex

Das Dokument weist eine zu detaillierte Untergliederung **{{tocline}}** auf. \
Eine zu feingliedrige Gliederung reduziert die Übersichtlichkeit und \
verhindert das schnelle Navigieren im Text.

Begrenzen Sie die Gliederung auf maximal 3 Sektionen.

{elemente/inhaltsverzeichnis#tiefe-der-gliederung}
"""


def check_1351_toc_level_to_deep(linter, driver):
    toc: iamraw.Toc = driver.toc
    if not toc.style:
        return
    if toc.style != iamraw.TocStyle.NUMBERED:
        return
    deep_max = decider_toc.level.TOC_DEEPNESS_DEFAULT_MAX
    if complex_document(driver.docinfo):
        deep_max = decider_toc.level.TOC_DEEPNESS_DISS_MAX
    level_result: 'TocValidationResult' = decider_toc.level.validate(
        toc=toc,
        maxdeep=deep_max,
    )
    for item in level_result.level_to_deep:  # pylint:disable=E1133
        tocline = tocline_shrink(item.raw)
        location = iamraw.Location.from_page(item.raw_location)
        linter(
            location=location,
            tocline=tocline,
        )


def tocline_shrink(raw: str) -> str:
    raw = raw.replace('..', '').replace('. .', '')
    raw = raw.strip('.')
    raw = utila.shrink(raw, maxlength=80)
    return raw


SOLUTION_1370 = """\
Abschnitt zu lang

Der Abschnitt **{{headline}}** ist im Vergleich zu den gleichranggigen \
Abschnitten ({{expected}}) zu lang (**{{current}}**).

Überdenken Sie die Abschnittseinteilung und überlegen Sie sich weitere \
Teilabschnitte einzuführen.

{aufbau_gliederung/absatz}
"""


def check_1370_section_too_long(linter, driver):
    toc: iamraw.Toc = driver.toc
    validate_chapter_length(
        linter,
        toc,
        level=2,
        expected=decider_toc.balance.TOO_LONG,
    )

    validate_chapter_length(
        linter,
        toc,
        level=3,
        expected=decider_toc.balance.TOO_LONG,
    )


SOLUTION_1371 = """\
Abschnitt zu kurz

Der Abschnitt „{{headline}}“ ist im Vergleich zu den gleichranggigen \
Abschnitten({{expected}}) zu kurz({{current}}). Überdenken Sie die \
Abschnittseinteilung und überlegen Sie sich Teilabschnitte zusammen zu \
führen.

{aufbau_gliederung/absatz}
"""


def check_1371_section_too_short(linter, driver):
    toc: iamraw.Toc = driver.toc
    validate_chapter_length(
        linter,
        toc,
        level=2,
        expected=decider_toc.balance.TOO_SHORT,
    )
    validate_chapter_length(
        linter,
        toc,
        level=3,
        expected=decider_toc.balance.TOO_SHORT,
    )


CHAPTER_LENGTH_CHECKER_MIN = configo.HV_FLOAT_PLUS(default=2.0)


def validate_chapter_length(linter, toc, level, expected):
    balanced = decider_toc.balance.judge(toc)
    level_x_balanced = utila.flat(getattr(balanced, f'level{level}'))
    flat = decider_toc.balance.data(toc)
    level_x = [item for item in flat if item.level == level]
    for line, judged in zip(level_x, level_x_balanced):
        if judged[0] != expected:
            continue
        if judged[0] is None:
            # check is disabled
            continue
        if judged[2] <= CHAPTER_LENGTH_CHECKER_MIN:
            continue
        location = iamraw.Location.from_page(line.pdfpage)
        title = line.title
        linter(
            location=location,
            headline=title,
            current=judged[1],
            expected=judged[2],
        )


# TODO: Link to article
SOLUTION_1382 = """\
Überschrift zu lang

Die Überschrift **{{title}}** ist zu lang und sollte verkürzt \
werden.
"""


def check_1382_toc_long_lines(linter, driver):
    toc: iamraw.Toc = driver.toc
    findings = decider_toc.length.validate(toc)
    for item in findings:
        title, raw_location = item[1], item[3]
        location = iamraw.Location.from_page(raw_location)
        linter(
            title=title,
            location=location,
        )
