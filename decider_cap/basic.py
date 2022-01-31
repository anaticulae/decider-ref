# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

import decider_ref.listdiff


def captions_sort(captions: list) -> list:
    captions = sorted(captions, key=lambda x: number(x.number))
    return captions


def number(value: str) -> int:
    try:
        value = int(value)
    except (ValueError, TypeError):
        value = -1
    return value


def check_order(captions, linter):
    if not captions:
        return
    expected = captions_sort(captions)
    current = captions
    if expected == current:
        return
    expected = [item.raw[0:75] for item in expected]
    current = [item.raw[0:75] for item in current]
    advice = decider_ref.listdiff.diffview(expected, current)
    linter(advice=advice)


def isdotted(captions) -> bool:
    if not captions:
        return False
    if len(captions) < 5:
        return False
    dotted, notdotted = utila.partition(
        key=lambda x: x.raw.strip()[-1] == '.',
        items=captions,
    )
    if not notdotted:
        return True
    rate = len(dotted) / len(captions)
    if rate < 0.8:  # TODO: HOLY VALUE
        return False
    return True


def check_dotted(captions, linter):
    if not isdotted(captions):
        return
    for item in captions:
        raw = item.raw.strip()
        if raw[-1] == '.':
            continue
        location = iamraw.Location.from_page(item.pdfpage)
        linter(
            text=raw,
            location=location,
        )
