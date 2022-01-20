# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol
import serializeraw
import utila


def create_driver(
    toc: str,
    outlines: str = None,
    headlines: str = None,
    docinfo: iamraw.DocInfo = None,
    sections: str = None,
):
    toc: iamraw.Toc = serializeraw.load_toc(toc)
    if utila.exists(headlines):
        outlines = serializeraw.load_toc(outlines)
    else:
        outlines = None
    if utila.exists(headlines):
        headlines = serializeraw.load_headlines(headlines)
    else:
        headlines = None
    if utila.exists(sections):
        sections = serializeraw.load_sections(sections)
    else:
        sections = None
    result = protocol.driver(
        docinfo=docinfo,
        headlines=headlines,
        outlines=outlines,
        sections=sections,
        toc=toc,
    )
    return result
