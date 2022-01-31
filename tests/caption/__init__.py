# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utilatest

import decider_cap
import decider_cap.cli

# pylint:disable=C0103
run = functools.partial(
    utilatest.run_command,
    main=decider_cap.cli.main,
    process=decider_cap.PROCESS,
    success=True,
)
fail = functools.partial(
    utilatest.run_command,
    main=decider_cap.cli.main,
    process=decider_cap.PROCESS,
    success=False,
)
