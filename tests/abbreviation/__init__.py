# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import serializeraw
import utilotest

import decider_abb

run, fail = utilotest.create_cli_runner(decider_abb)


def run_table(source, mp, td, msgid=None, pages=None):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    utilotest.fixture_requires(source)
    cmd = f'-i {source} --table'
    run(cmd, mp=mp)
    path = decider_abb.path.decider_abb_table_user(td.tmpdir)
    result = protoerror.select_findings(
        serializeraw.load_findings(path),
        msgid=msgid,
    )
    if pages is not None:
        result = protoerror.select_pages(result, pages)
    return result
