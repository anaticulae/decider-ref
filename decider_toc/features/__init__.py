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
    magic_pages: str = None,
):
    if utila.exists(toc):
        toc: iamraw.Toc = serializeraw.load_toc(toc)
    else:
        toc: iamraw.Toc = iamraw.Toc()
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
    if utila.exists(magic_pages):
        magic_pages_reverse = serializeraw.load_pagenumbers_magic(magic_pages)
        magic_pages_reverse = utila.dict_reverse(magic_pages_reverse)
    else:
        magic_pages_reverse = None
    result = protocol.driver(
        docinfo=docinfo,
        headlines=headlines,
        outlines=outlines,
        sections=sections,
        toc=toc,
        magic_pages_reverse=PageReverse(magic_pages_reverse),
    )
    return result


class PageReverse:

    def __init__(self, pages: dict = None):
        self.pages = pages if pages else dict()

    def __call__(self, userpage: int):
        if userpage is None:
            utila.error('could not reverse None, use OVERVIEW')
            return protocol.OVERVIEW
        try:
            return self.pages[userpage]
        except KeyError:
            utila.error(f'could not reverse: {userpage}, use OVERVIEW')
            return protocol.OVERVIEW
