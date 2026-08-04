# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protoerror
import serializeraw
import utilo
import utilotest

import decider_toc

run, fail = utilotest.create_cli_runner(decider_toc)


def tableofcontent(path: str) -> iamraw.Toc:
    path = iamraw.path.reftable_toc(path)
    if utilo.exists(path):
        result = serializeraw.load_toc(path)
    else:
        result = iamraw.Toc()
    return result


def lint(path: str, module):
    result = linter(path, module)
    failures = sorted(item.msgid for item in result)
    return failures


def linter(path: str, module, msgids=None):
    toc = tableofcontent(path)
    try:
        headlines = serializeraw.load_headlines(path)
    except FileNotFoundError:
        headlines = None
    driver = protoerror.driver(
        headlines=headlines,
        outlines=None,
        toc=toc,
        docinfo=None,
    )
    findings = protoerror.run(
        module.__name__,
        driver=driver,
    )
    result = serializeraw.load_findings(findings[0], msgids=msgids)
    return result
