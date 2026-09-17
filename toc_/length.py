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

import toc_.utils

WORD_COUNT_MAX = configos.HV_INT_PLUS(default=12)


def validate(tocc: iamraw.Toc) -> toc_.utils.InvalidTocItems:
    flatten = elementae.toc_flat(tocc)
    result = []
    for index, item in enumerate(flatten):
        words = germania.split_words(item.title, validate_sentences=False)
        words = konradus.remove_marks(words)
        linelength = len(words)
        if linelength > WORD_COUNT_MAX:
            result.append((index, item.title, linelength, item.raw_location))
    return result
