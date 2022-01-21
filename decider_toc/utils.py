# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import german
import iamraw
import iamraw.toc
import utila


class InvalidTocItems(collections.UserList):  # pylint:disable=too-many-ancestors
    pass


def flat(toc: iamraw.Toc):
    """Remove nested order and deliver a top down list of pages and
    sections."""
    result = []

    def godown(item: iamraw.toc.TocLinkMixin):
        result.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)

    return result


def toc_lang(toc: iamraw.Toc) -> iamraw.Language:
    flats = flat(toc)
    joined = utila.NEWLINE.join([item.raw for item in flats])
    result = german.lang(joined).language
    return result
