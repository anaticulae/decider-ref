# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import serializeraw
import utilatest

import decider_abb

run, fail = utilatest.create_cli_runner(decider_abb)


def run_table(source, mp, td, msgid=None, pages=None):
    utilatest.fixture_requires(source)
    source = power.link(source)
    utilatest.fixture_requires(source)
    cmd = f'-i {source} --table'
    run(cmd, mp=mp)
    path = decider_abb.path.decider_abb_table_user(td.tmpdir)
    result = protocol.select_findings(
        serializeraw.load_findings(path),
        msgid=msgid,
    )
    if pages is not None:
        result = protocol.select_pages(result, pages)
    return result
