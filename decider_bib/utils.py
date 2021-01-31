# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def format_bibline(item) -> str:
    if item.reference:
        # convert to string to avoid failing when reference is parsed as
        # int or something. Later, this will not be a problem, cause we
        # have only valid parsings.
        return str(item.reference)
    return f' * {item.author} {item.year} {item.title}'
