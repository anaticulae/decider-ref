# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol
import serializeraw
import utila


def create_driver(captions: str, pages: tuple = None):
    if utila.exists(captions):
        captions = serializeraw.load_captions(captions, pages=pages)
    else:
        captions = []
    flat = utila.flatten_content(captions)
    figures = [item for item in flat if item.typ == iamraw.CaptionType.FIGURE]
    codes = [item for item in flat if item.typ == iamraw.CaptionType.CODE]
    tables = [item for item in flat if item.typ == iamraw.CaptionType.TABLE]
    result = protocol.driver(
        captions=captions,
        codes=codes,
        figures=figures,
        tables=tables,
    )
    return result
