# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import serializeraw
import utila


def create_driver(captions: str, pages: tuple = None):
    if utila.exists(captions):
        captions = serializeraw.load_captions(captions, pages=pages)
    else:
        captions = []
    result = protocol.driver(captions=captions)
    return result
