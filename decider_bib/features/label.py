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

import docref.bibliography.parser
import iamraw
import protocol
import serializeraw
import utila
import words.utils

import decider_bib.order
import decider_bib.reference
import decider_bib.serialize
import decider_bib.utils


def work(
        table: str,
        docreference: str,
        headlines: str,
        text: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    bibliography = decider_bib.serialize.load_bibliography_reference(table)
    text, docreference = load_docref(docreference, headlines, text, pages=pages)
    driver = protocol.driver(
        bibliography=bibliography,
        bibtextref=docreference,
        text=text,
    )
    linter = protocol.from_module(__name__)
    if bibliography:
        linting(linter, driver)
    else:
        utila.error('no bib table parsed: skip decider_bib:label')
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


def load_docref(
        docreference: str,
        headlines: str,
        text: str,
        pages: tuple = None,
) -> list:
    docreference = serializeraw.load_docref(docreference, pages=pages)
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    text = serializeraw.load_text(text, headlines=headlines, pages=pages)
    return text, docreference


SOLUTION_6050 = """\
Quelle nicht gefunden

Die Referenz **{{reference}}** fehlt im Quellenverzeichnis.
"""


def check_6050_ref_in_table(linter: callable, driver):
    plains = references_plain(driver.bibtextref, driver.text)
    for reference, plain in zip(driver.bibtextref, plains):
        location = iamraw.Location.from_sentence(
            sentence=reference.sentence,
            page=reference.page,
        )
        for mark, item in zip(reference.marked, plain):  # pylint:disable=W0612
            # verify that reference exists
            inside = decider_bib.reference.inside(
                reference=item,
                table=driver.bibliography,
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
    plains = references_plain(driver.bibtextref, driver.text)
    plains = utila.flatten(plains)
    plains = {
        docref.bibliography.parser.parse(item)[0].reference for item in plains
    }
    source = list(driver.bibliography)
    not_required = [item for item in source if item.reference not in plains]
    for item in not_required:
        location = iamraw.Location.from_page(page=0)
        linter(location=location, source=item.reference)


SOLUTION_6061 = """\
Seitenangabe fehlt

Der Quellenverweis **{{reference}}** enthält keine Seitenangabe.
"""


def check_6061_bib_ref_no_page(linter: callable, driver):
    plains = references_plain(driver.bibtextref, driver.text)
    for reference, plain in zip(driver.bibtextref, plains):
        location = iamraw.Location.from_sentence(
            sentence=reference.sentence,
            page=reference.page,
        )
        for mark, item in zip(reference.marked, plain):  # pylint:disable=W0612
            if decider_bib.reference.has_page(item):
                continue
            linter(location=location, reference=item)


SOLUTION_6062 = """\
Seitenangabe unkonkret

Die Seitenzahl **{{reference}}** sollte durch die konkrete Seitenzahl
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
            linter(location=location, reference=item)


def references_plain(references, text) -> list:
    result = []
    sentences = words.utils.sentence_lookup(text)
    for ref in references:
        page, sentenceid, marked = ref.page, ref.sentence, ref.marked
        selected = words.utils.sentence_plain(  # pylint:disable=E1101
            sentences[page][sentenceid],
            marks=marked,
        )
        result.append(selected)
    return result
