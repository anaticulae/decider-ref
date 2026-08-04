# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import utilo
import utilotest

import decider_toc
import decider_toc.features.complexity
import tests.toc


def test_decider_toc_cli_help(mp):
    tests.toc.run('--help', mp=mp)


@utilotest.hasprog(decider_toc.PROCESS)
def test_decider_toc_nomonkey_cli_help():
    utilo.run(f'{decider_toc.PROCESS} --help')


@utilotest.requires(hoverpower.MASTER099_PDF)
def test_toc_cli_master99_headline_too_long(td, mp):
    source = hoverpower.link(hoverpower.MASTER099_PDF)
    tests.toc.run(f'-i {source}', mp=mp)

    findings = protoerror.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1382)) == 1


@utilotest.requires(hoverpower.MASTER099_PDF)
def test_toc_cli_master99_chapter_too_long(td, mp):
    source = hoverpower.link(hoverpower.MASTER099_PDF)
    tests.toc.run(f'-i {source}', mp=mp)

    findings = protoerror.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1370)) == 4


@utilotest.requires(hoverpower.MASTER098_PDF)
def test_toc_cli_master98_chapter_too_short(td, mp):
    source = hoverpower.link(hoverpower.MASTER098_PDF)
    with mp.context() as context:
        context.setattr(
            decider_toc.features.complexity,
            'CHAPTER_LENGTH_CHECKER_MIN',
            0.0,
        )
        tests.toc.run(f'-i {source}', mp=mp)
    findings = protoerror.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1371)) == 1


@utilotest.requires(hoverpower.BACHELOR076_PDF)
def test_toc_cli_bachelor76_legal_inside_toc(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR076_PDF)
    tests.toc.run(f'-i {source} --rules', mp=mp)

    findings = protoerror.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1365)) == 1


@utilotest.requires(hoverpower.BACHELOR076_PDF)
def test_toc_cli_bachelor76_roman_page_numbers(td, mp):
    """Regression test to verify that roman page numbers does not break
    page distance computation etc."""
    source = hoverpower.link(hoverpower.BACHELOR076_PDF)
    tests.toc.run(f'-i {source}', mp=mp)
    findings = protoerror.findings_from_path(td.tmpdir)
    assert findings
