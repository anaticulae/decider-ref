# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import bibliography_


def decider_bib_label_user(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(path, bibliography_.PROCESS, 'label_user',
                               prefix)


def decider_bib_table_user(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(path, bibliography_.PROCESS, 'table_user',
                               prefix)
