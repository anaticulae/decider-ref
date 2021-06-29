# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

MAX_AUTHOR_LENGTH = 60  # TODO: HOLY VALUE


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
