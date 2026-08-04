# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import docref.biblio.parser
import iamraw
import protoerror
import serializeraw
import utilo

import decider_bib.reference
import decider_bib.serialize
import decider_bib.utils


def work(  # pylint:disable=W0613
    bibtable: str,
    docreference: str,
    headlines: str,
    text: str,
    sections: str,
    docinfo: iamraw.DocInfo,
    pages: tuple = None,
) -> protoerror.ResultType:
    driver = create_driver(**locals())
    if driver.bibliography.references:  # pylint:disable=E1101
        result = protoerror.run(
            modulename=__name__,
            driver=driver,
            document=docinfo,
        )
    else:
        utilo.error('no bib table parsed: skip decider_bib:label')
        result = protoerror.RESULT_EMPTY
    return result


def create_driver(
    bibtable: str,
    docreference: str,
    headlines: str,
    text: str,
    sections: str,
    docinfo: iamraw.DocInfo,
    pages: tuple = None,
):
    bibliography = decider_bib.serialize.load_bibliography_reference(bibtable)
    docreference = serializeraw.load_docref(docreference, pages=pages)
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    sections = serializeraw.load_sections(sections, pages=pages)
    text = serializeraw.load_text(text, headlines=headlines, pages=pages)
    nobibs = nobibpages(sections)
    # create driver
    result = protoerror.driver(
        bibliography=bibliography,
        bibtextref=docreference,
        text=text,
        nobibs=nobibs,
        docinfo=docinfo,
    )
    return result


def nobibpages(sections: iamraw.sections.Sections) -> set:
    """Determine pages which are not bib-table pages."""
    end = sections[-1].end + 1
    collected = set()
    for part in sections:
        for item in part:
            if not isinstance(item, iamraw.sections.Bibliography):
                continue
            for page in range(int(item.start), int(item.end + 1)):
                collected.add(page)
    result = {item for item in range(end) if item not in collected}
    return result


def missing_bibtable_reference(bibtable) -> bool:
    if not bibtable:
        return True
    if len(bibtable) < 10:
        utilo.error(f'too few bib entry: {len(bibtable)}')
        return True
    invalid_reference = [item for item in bibtable if not item.reference]
    rate = len(invalid_reference) / len(bibtable)
    if rate > 0.2:
        utilo.error(f'too many invalid bib references: {rate}')
        return True
    return False


SOLUTION_6050 = """\
Quelle nicht gefunden

Die Referenz **{{reference}}** fehlt im Quellenverzeichnis.
"""


def check_6050_ref_in_table(linter: callable, driver):
    if missing_bibtable_reference(driver.bibliography.references):
        utilo.log('disable 6050')
        return
    plains = references_plain(driver.bibtextref, driver.text)
    for reference, plain in zip(driver.bibtextref, plains):
        if reference.page not in driver.nobibs:
            # bib table page
            continue
        location = iamraw.Location.from_sentence(
            sentence=reference.sentence,
            page=reference.page,
        )
        for mark, item in zip(reference.marked, plain):  # pylint:disable=W0612
            # verify that reference exists
            inside = decider_bib.reference.inside(
                reference=item,
                table=driver.bibliography.references,
            )
            if inside:
                # reference found
                continue
            if inside is None:
                # Could not parse bib label. Do not inform user about
                # missing reference when we are not able to parse the
                # reference.
                continue
            linter(location=location, reference=item)


SOLUTION_6051 = """\
Quelle überflüssig

Die Quelle **{{source}}** wird im Text nicht verwendet.
"""


def check_6051_table_in_text(linter: callable, driver):
    insentence = insentence_reference(driver.text, driver.bibtextref)
    source = list(driver.bibliography.references)
    for item in source:
        if item.reference:
            continue
        utilo.debug(f'None-Reference: {item}')
    not_required = [
        item for item in source
        if not decider_bib.reference.reference_inside(item, insentence)
    ]
    for item in not_required:
        location = iamraw.Location.from_page(item.raw_pdfpage)
        source = item.reference
        if not source:
            # skip None-Reference
            continue
        linter(
            location=location,
            source=source,
        )


def insentence_reference(text, bibliography) -> set:
    """Prepare references which are located inside sentences."""
    insentence_ref = references_plain(bibliography, text)
    insentence_ref = utilo.flat(insentence_ref)
    result = set()
    for item in insentence_ref:
        parsed = docref.biblio.parser.parse(item)
        if not parsed:
            utilo.error(f'could not parse: {item}')
            continue
        # TODO: SUPPORT MORE THAN ONE REFERENCE IN A SENTENCE?
        reference = parsed[0].reference
        if utilo.isint(reference):
            # convert to valid [10]-intext reference
            reference = f'[{reference}]'
        result.add(reference)
    return result


SOLUTION_6061 = """\
Seitenangabe fehlt

Der Quellenverweis **{{reference}}** enthält keine Seitenangabe.
"""


def check_6061_bib_ref_no_page(linter: callable, driver):
    plains = references_plain(driver.bibtextref, driver.text)
    for reference, plain in zip(driver.bibtextref, plains):
        if reference.page not in driver.nobibs:
            # bib table page
            continue
        location = iamraw.Location.from_sentence(
            sentence=reference.sentence,
            page=reference.page,
        )
        for mark, item in zip(reference.marked, plain):  # pylint:disable=W0612
            if decider_bib.reference.has_page(item):
                continue
            linter(
                location=location,
                reference=item,
            )


SOLUTION_6062 = """\
Seitenangabe unkonkret

Die Seitenzahl **{{reference}}** sollte durch die konkrete Seitenzahl \
ersetzt werden.
"""


def check_6062_bib_ref_inaccurate_page(linter: callable, driver):
    plains = references_plain(driver.bibtextref, driver.text)
    for reference, plain in zip(driver.bibtextref, plains):
        location = iamraw.Location.from_sentence(
            sentence=reference.sentence,
            page=reference.page,
        )
        for mark, item in zip(reference.marked, plain):  # pylint:disable=W0612
            if decider_bib.reference.precise(item):
                continue
            linter(
                location=location,
                reference=item,
            )


MISSING_PAGENUMBER_RATE_MIN = configos.HV_PERCENT_PLUS(default=20)

SOLUTION_I6063 = """\
Empfehlung: Quellenangaben konkretisieren

Es wird empfohlen sämtlichen Quellen eine Seitenangabe zuzufügen.
"""


def check_6063_bib_ref_add_pagination(linter: callable, driver):
    """Add hint to add page numbers.

    If there are too many lintings, disable this lintings.
    """
    baselinter: protoerror.Linter = linter.func.__self__
    pagenumber_missing = baselinter.count_findings(msgid=6061)
    if pagenumber_missing < 30:
        return
    intext_ref = len(driver.bibtextref)
    rate = pagenumber_missing / intext_ref
    if rate < MISSING_PAGENUMBER_RATE_MIN:
        return
    linter(location=protoerror.OVERVIEW)

    def disable_6061(findings):
        return [item for item in findings if item.msgid != 6061]

    baselinter.check_findings(disable_6061)


SOLUTION_6070 = """\
Label vereinfachen

Vereinfachen Sie das Label und entfernen Sie unnötige Klammern.

Erkannt: ([WA12])
Besser: [WAS12]

Erkannt: ([HA15], S. 40)
Besser: [HA15, S. 40]
"""

SPECIAL_COUNT_ACTIVE_MIN = configos.HV_INT_PLUS(default=5)


def check_6070_bib_ref_too_complicated(linter: callable, driver):
    plains = references_plain(driver.bibtextref, driver.text)
    collected = []
    for _, plain in zip(driver.bibtextref, plains):
        collected.extend(plain)
    if not collected:
        return
    special = [
        item for item in collected
        if item.startswith('([') and item.endswith(')')
    ]
    if len(special) < SPECIAL_COUNT_ACTIVE_MIN:
        return
    # TODO: ADD HINT FOR EVERY FINDING?
    linter(location=protoerror.OVERVIEW)


def references_plain(references, text) -> list:
    result = []
    sentences = decider_bib.utils.sentence_lookup(text)
    for ref in references:
        page, sentenceid, marked = ref.page, ref.sentence, ref.marked
        selected = decider_bib.utils.sentence_plain(  # pylint:disable=E1101
            sentences[page][sentenceid],
            marks=marked,
        )
        result.append(selected)
    return result
