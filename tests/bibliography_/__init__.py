# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utila
import utilatest

import decider_bibliography
import decider_bibliography.cli

# pylint:disable=C0103
run = functools.partial(
    utilatest.run_command,
    main=decider_bibliography.cli.main,
    process=decider_bibliography.PROCESS,
    success=True,
)
fail = functools.partial(
    utilatest.run_command,
    main=decider_bibliography.cli.main,
    process=decider_bibliography.PROCESS,
    success=False,
)
