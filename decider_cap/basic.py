# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def captions_sort(captions: list) -> list:
    captions = sorted(captions, key=lambda x: number(x.number))
    return captions


def number(value: str) -> int:
    try:
        value = int(value)
    except (ValueError, TypeError):
        value = -1
    return value
