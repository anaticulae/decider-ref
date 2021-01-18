# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import detector.path
import power
import utila
import utilatest

import decider_bib
import decider_bib.cli

# pylint:disable=C0103
run = functools.partial(
    utilatest.run_command,
    main=decider_bib.cli.main,
    process=decider_bib.PROCESS,
    success=True,
)
fail = functools.partial(
    utilatest.run_command,
    main=decider_bib.cli.main,
    process=decider_bib.PROCESS,
    success=False,
)


def load_bib_table(path: str):
    table = power.link(path)
    table = detector.path.bibliography_detected(table)
    bibliography = decider_bib.serialize.load_bibliography_reference(table)
    return bibliography
