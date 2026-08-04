# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw
import protoerror
import serializeraw
import utilo

import decider_bib.order
import decider_bib.serialize
import decider_bib.table
import decider_bib.utils
import decider_ref.listdiff


def work(
    bibtable: str,
    titlepage: str,
    pdfinfo: str,
    docinfo: iamraw.DocInfo,
) -> protoerror.ResultType:
    driver = create_driver(bibtable, titlepage, pdfinfo, docinfo)
    result = protoerror.run(
        modulename=__name__,
        driver=driver,
    )
    return result


def create_driver(table: str, titlepage: str, pdfinfo: str, docinfo: str):
    bibliography = decider_bib.serialize.load_bibliography_reference(table)
    if utilo.exists(titlepage):
        titlepage = serializeraw.load_titlepage(titlepage)
    else:
        titlepage = iamraw.TitlePage()
    pages = serializeraw.load_pdfinfo(pdfinfo)
    pages = pages.pages if pages else None
    # TODO: USE CONTENT SECTION LENGTH INSTEAD OF PAGES. THIS IMPROVES
    # JUDGEMENT OF THESIS WITH LONG APPENDIX
    driver = protoerror.driver(
        bibliography=bibliography,
        titlepage=titlepage,
        pages=pages,
        docinfo=docinfo,
    )
    return driver


SOLUTION_6000 = """\
Quellenverzeichnis ist nicht alphabetisch sortiert

Sortieren Sie das Quellenverzeichnis.

{{advice}}

{elemente/literaturverzeichnis}
"""


def check_6000_not_sorted_alphabetically(linter: callable, driver):
    references: iamraw.BibliographyReferences = driver.bibliography.references
    if all_labeled(references):
        # Labeled bibs with [1] [2] are always sorted
        utilo.debug('all bibs are labeled skip order check 6000')
        return
    if not all_authors_valid(references):
        utilo.error('could not parse all authors, skip 6000')
        return
    current = list(references)
    expected = decider_bib.order.theissen_sort(current)
    if current == expected:
        return
    location = pagelocation(current[0])
    # TODO: CHECK REPRESENTATION
    current = [decider_bib.utils.format_bibline(item) for item in current]
    expected = [decider_bib.utils.format_bibline(item) for item in expected]
    advice = decider_ref.listdiff.diffview(expected, current)
    linter(
        advice=advice,
        location=location,
    )


def all_authors_valid(references: iamraw.BibliographyReferences) -> bool:
    result = True
    for item in references:
        if item.authors:
            continue
        utilo.error(f'could not parse all bib refs: {item}')
        result = False
    return result


def all_labeled(references: iamraw.BibliographyReferences) -> bool:
    if not references:
        return False
    ref, noref = utilo.partition(
        key=lambda x: utilo.isint(x.reference),
        items=references,
    )
    if not noref:
        return True
    rate = utilo.rate_sum(len(ref), len(noref))
    if rate >= 0.75:
        # TODO: HOLY VALUE
        return True
    return False


SOLUTION_6005 = """\
Quellenverzeichnis veraltet

Die ausgewählten Quellen scheinen nicht dem aktuellen Stand der \
Forschung zu entsprechen. Überprüfen Sie ob durch weitere Recherche \
aktuelle Paper/Publikationen zum Thema gefunden werden können.
"""


def check_6006_bibs_too_old(linter: callable, driver):
    references: iamraw.BibliographyReferences = driver.bibliography.references
    if not references:
        return
    if not decider_bib.table.too_old(references):
        return
    location = pagelocation(references[0])
    linter(location=location)


SOLUTION_6006 = """\
Anzahl der Quellen zu gering

Die Anzahl der Quellen({{count}}) scheint für den Umfang der Arbeit \
zu gering zu sein. Halten Sie Rücksprache mit Ihrem wissenschaftlichen \
Betreuer.
"""


def check_6006_too_few_bibs(linter: callable, driver):
    references: iamraw.BibliographyReferences = driver.bibliography.references
    if not references:
        return
    if not driver.titlepage:
        return
    thesis = driver.titlepage.thesis.typ if driver.titlepage.thesis else None
    if not decider_bib.table.too_few(
            references=references,
            pages=driver.pages,
            thesis=thesis,
    ):
        return
    location = pagelocation(references[0])
    linter(location=location, count=len(references))


SOLUTION_6007 = """\
Anzahl der Quellen zu hoch

Die Anzahl {{count}} der Quellen erscheint für den Umfang der Arbeit zu \
hoch. Das Quellenverzeichnis darf nur Quellen enthalten die im Text \
zitiert/verwendet werden.
"""


def check_6007_too_many_bibs(linter: callable, driver):
    references: iamraw.BibliographyReferences = driver.bibliography.references
    if not references:
        return
    if not driver.titlepage:
        return
    thesis = driver.titlepage.thesis.typ if driver.titlepage.thesis else None
    if not decider_bib.table.too_many(
            references=references,
            pages=driver.pages,
            thesis=thesis,
    ):
        return
    location = pagelocation(references[0])
    linter(location=location, count=len(references))


SOLUTION_6010 = """\
Quellenangabe: Klammern überprüfen

Öffnende und schließende Klammern in „{{source}}“ sind nicht \
ausbalanciert: {{brackets}}.
"""


def check_6010_unbalanced_brackets(linter: callable, driver):
    references: iamraw.BibliographyReferences = driver.bibliography.references
    for reference in references:
        raw = reference.raw
        for pair in ('[]', '()'):
            if raw.count(pair[0]) == raw.count(pair[1]):
                continue
            linter(
                brackets=pair,
                source=raw,
                location=pagelocation(reference),
            )


SOLUTION_6011 = """\
Quellenangabe: Tippfehler erkannt

Tippfehler „{{typo}}“ in Quellenangabe „{{bib}}“ erkannt.
"""


def check_6011_typo(linter: callable, driver):
    references: iamraw.BibliographyReferences = driver.bibliography.references
    for reference in references:
        raw = reference.raw
        for typo in TYPOS:
            matched = re.search(typo, raw)
            if not matched:
                continue
            linter(
                typo=utilo.extract_match(matched),
                bib=raw,
                location=pagelocation(reference),
            )


TYPOS = (
    r':\)',
    ' : ',
    r'(\)\:[\w\d])',
)

SOLUTION_6020 = """\
Quellenangabe überprüfen

Stil der Quellenangabe **{{bibraw}}** weicht ab.
"""


def check_6020_bib_differs(linter: callable, driver):
    references: iamraw.BibliographyReferences = driver.bibliography.references
    invalid = decider_bib.table.invalid_references(references)
    for reference in invalid:
        raw = reference.raw
        linter(
            bibraw=raw,
            location=pagelocation(reference),
        )


def pagelocation(item) -> iamraw.Location:
    pagenumber = protoerror.OVERVIEW
    if item.raw_pdfpage is not None:
        pagenumber = iamraw.Location.from_page(item.raw_pdfpage)
    return pagenumber
