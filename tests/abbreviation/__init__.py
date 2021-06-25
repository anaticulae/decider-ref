# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import protocol
import serializeraw
import utilatest

import decider_abb
import decider_abb.cli

# pylint:disable=C0103
run = functools.partial(
    utilatest.run_command,
    main=decider_abb.cli.main,
    process=decider_abb.PROCESS,
    success=True,
)
fail = functools.partial(
    utilatest.run_command,
    main=decider_abb.cli.main,
    process=decider_abb.PROCESS,
    success=False,
)


def run_table(source, monkeypatch, testdir, msgid=None, pages=None):
    source = power.link(source)
    utilatest.fixture_requires(source)
    cmd = f'-i {source} --table'
    run(cmd, monkeypatch=monkeypatch)
    path = decider_abb.path.decider_abb_table_user(testdir.tmpdir)
    result = protocol.select_findings(
        serializeraw.load_findings(path),
        msgid=msgid,
    )
    if pages is not None:
        result = protocol.select_pages(result, pages)
    return result
