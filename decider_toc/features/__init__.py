# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol
import serializeraw


def create_driver(toc: str, outlines: str = None):
    toc: iamraw.Toc = serializeraw.load_toc(toc)
    if outlines:
        outlines = serializeraw.load_toc(outlines)
    driver = protocol.driver(toc=toc, outlines=outlines)
    return driver
