# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import utila
import utilatest

import decider_toc
import decider_toc.features.complexity
import tests.toc


def test_decider_toc_cli_help(mp):
    tests.toc.run('--help', mp=mp)


@utilatest.hasprog(decider_toc.PROCESS)
def test_decider_toc_nomonkey_cli_help():
    utila.run(f'{decider_toc.PROCESS} --help')


@utilatest.requires(power.MASTER099_PDF)
def test_toc_cli_master99_headline_too_long(td, mp):
    source = power.link(power.MASTER099_PDF)
    tests.toc.run(f'-i {source}', mp=mp)

    findings = protocol.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1382)) == 1


@utilatest.requires(power.MASTER099_PDF)
def test_toc_cli_master99_chapter_too_long(td, mp):
    source = power.link(power.MASTER099_PDF)
    tests.toc.run(f'-i {source}', mp=mp)

    findings = protocol.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1370)) == 4


@utilatest.requires(power.MASTER098_PDF)
def test_toc_cli_master98_chapter_too_short(td, mp):
    source = power.link(power.MASTER098_PDF)
    with mp.context() as context:
        context.setattr(
            decider_toc.features.complexity,
            'CHAPTER_LENGTH_CHECKER_MIN',
            0.0,
        )
        tests.toc.run(f'-i {source}', mp=mp)
    findings = protocol.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1371)) == 1


@utilatest.requires(power.BACHELOR076_PDF)
def test_toc_cli_bachelor76_legal_inside_toc(td, mp):
    source = power.link(power.BACHELOR076_PDF)
    tests.toc.run(f'-i {source} --rules', mp=mp)

    findings = protocol.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1365)) == 1


@utilatest.requires(power.BACHELOR076_PDF)
def test_toc_cli_bachelor76_roman_page_numbers(td, mp):
    """Regression test to verify that roman page numbers does not break
    page distance computation etc."""
    source = power.link(power.BACHELOR076_PDF)
    tests.toc.run(f'-i {source}', mp=mp)
    findings = protocol.findings_from_path(td.tmpdir)
    assert findings
