# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import elementae
import germania
import iamraw
import konradus

import decider_toc.utils

WORD_COUNT_MAX = configos.HV_INT_PLUS(default=12)


def validate(toc: iamraw.Toc) -> decider_toc.utils.InvalidTocItems:
    flatten = elementae.toc_flat(toc)

    lines = []
    for index, item in enumerate(flatten):
        words = germania.split_words(item.title, validate_sentences=False)
        words = konradus.remove_marks(words)
        linelength = len(words)
        if linelength > WORD_COUNT_MAX:
            lines.append((index, item.title, linelength, item.raw_location))
    return lines
