# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import serializeraw
import utila


def load_bibliography_reference(path) -> list:
    loaded = serializeraw.load_bibliography_reference(path)
    if not loaded:
        return []
    with contextlib.suppress(AttributeError):
        # TODO: REMOVE LATER
        if isinstance(loaded[0], list):
            loaded = utila.flatten(loaded)
    return loaded
