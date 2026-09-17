# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import indagator.path
import utilotest

import bibliography_
import bibliography_.serialize

run, fail = utilotest.create_cli_runner(bibliography_)


def load_bib_table(path: str):
    table = hoverpower.link(path)
    table = indagator.path.bibliography_detected(table)
    bibliography = bibliography_.serialize.load_bibliography_reference(table)
    return bibliography
