# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import groupme.path
import iamraw
import serializeraw
import utila
import utilatest

import decider_toc
import decider_toc.cli

# pylint:disable=C0103
run = functools.partial(
    utilatest.run_command,
    main=decider_toc.cli.main,
    process=decider_toc.PROCESS,
    success=True,
)
fail = functools.partial(
    utilatest.run_command,
    main=decider_toc.cli.main,
    process=decider_toc.PROCESS,
    success=False,
)


def tableofcontent(path: str) -> iamraw.Toc:
    path = groupme.path.toc(path)
    result = serializeraw.load_toc(path)
    return result
