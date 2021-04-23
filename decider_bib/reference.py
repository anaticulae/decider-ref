# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import docref.bibliography.parser
import iamraw
import utila


def has_page(item) -> bool:
    """\
    >>> has_page('[TCL18 S.14]')
    True
    >>> has_page('[ABC13]')
    False
    >>> has_page('([We05], S. 48)')
    True
    """
    parsed = docref.bibliography.parser.parse(item)
    if not parsed:
        # simple backup strategy
        return 'S.' in item or 'Seite' in item
    return parsed[0].page is not None


def precise(item) -> bool:
    if ' ff ' in item:
        return False
    if 'ff.' in item:
        return False
    if ' ff' in item:
        return False
    return True


def inside(reference: str, table: iamraw.BibliographyReferences) -> bool:
    parsed = docref.bibliography.parser.parse(reference)
    if not parsed:
        utila.error(f'could not parse: {reference}, skip insidecheck')
        return None
    assert len(parsed) == 1, str(parsed)
    parsed = parsed[0]
    if parsed.reference:
        for item in table:
            if item.reference is not None:
                # TODO: VALIDATE WHY
                continue
            utila.error(f'invalid reference: {item}')
        table = {item.reference.lower() for item in table if item.reference}
        return parsed.reference.lower() in table
    if parsed.reference is None:
        # TODO: ADD AUTHOR CHECK
        utila.error(f'could not determine .reference in: {reference}, '
                    'skip insidecheck')
        return None
    return False
