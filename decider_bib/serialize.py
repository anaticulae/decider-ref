# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw
import serializeraw
import utila


def load_bibliography_reference(path) -> list:
    if not utila.exists(path):
        utila.debug(f'bib file does not exists: {path}')
        return iamraw.BibliographyTable()
    loaded = serializeraw.load_bibliography_reference(path)
    if not loaded:
        return iamraw.BibliographyTable()
    with contextlib.suppress(AttributeError):
        # TODO: REMOVE LATER
        if isinstance(loaded[0], list):
            loaded = utila.flat(loaded)
    if isinstance(loaded, list):
        # TODO: REMOVE AFTER UPGRADING
        loaded: iamraw.BibliographyTable = iamraw.BibliographyTable(
            references=loaded)
    return loaded
