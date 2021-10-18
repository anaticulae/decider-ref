# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

MAX_AUTHOR_LENGTH = configo.HV_INT_PLUS(default=60)


def invalid_references(
    references: iamraw.BibliographyReferences,
) -> iamraw.BibliographyReferences:
    result = []
    for reference in references:
        if not reference.authors:
            utila.error(f'no authors: {reference}')
            continue
        if max(author_length(reference.authors)) < MAX_AUTHOR_LENGTH:
            continue
        result.append(reference)
    return result


def author_length(authors):
    return [len(item.raw) for item in authors]


def too_old(references: iamraw.BibliographyReferences) -> bool:  # pylint:disable=W0613
    return False


BIBLIOGRAPHY_RANGE_UPPER = configo.HolyTable([
    (0, 50),
    (30, 40),
    (50, 50),
    (70, 70),
    (100, 100),
    (200, 180),
    (300, 250),
    (500, 400),
])


def too_many(  # pylint:disable=W0613
    references: iamraw.BibliographyReferences,
    pages: int,
    thesis: iamraw.DocumentType,
) -> bool:
    if not pages:
        return False
    reference_count = len(references)
    upper = BIBLIOGRAPHY_RANGE_UPPER(pages)
    return reference_count > upper


BIBLIOGRAPHY_RANGE_LOWER = configo.HolyTable([
    (0, 15),
    (30, 15),
    (50, 25),
    (70, 30),
    (100, 40),
    (200, 50),
    (300, 70),
])


def too_few(  # pylint:disable=W0613
    references: iamraw.BibliographyReferences,
    pages: int,
    thesis: iamraw.DocumentType,
) -> bool:
    if not pages:
        return False
    reference_count = len(references)
    lower = BIBLIOGRAPHY_RANGE_LOWER(pages)
    return reference_count < lower
