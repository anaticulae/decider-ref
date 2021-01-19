# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import utila

import decider_toc
import tests.toc


def test_decider_toc_cli_help(monkeypatch):
    tests.toc.run('--help', monkeypatch=monkeypatch)


def test_decider_toc_nomonkey_cli_help():
    utila.run(f'{decider_toc.PROCESS} --help')


def test_toc_cli_master99_headline_too_long(testdir, monkeypatch):
    source = power.link(power.MASTER099_PDF)
    tests.toc.run(f'-i {source}', monkeypatch=monkeypatch)

    findings = protocol.findings_from_path(testdir.tmpdir)
    assert len(tests.select(findings, 1382)) == 1


def test_toc_cli_master99_chapter_too_long(testdir, monkeypatch):
    source = power.link(power.MASTER099_PDF)
    tests.toc.run(f'-i {source}', monkeypatch=monkeypatch)

    findings = protocol.findings_from_path(testdir.tmpdir)
    assert len(tests.select(findings, 1370)) == 4


def test_toc_cli_master98_chapter_too_short(testdir, monkeypatch):
    source = power.link(power.MASTER098_PDF)
    tests.toc.run(f'-i {source}', monkeypatch=monkeypatch)

    findings = protocol.findings_from_path(testdir.tmpdir)
    assert len(tests.select(findings, 1371)) == 1


def test_toc_cli_bachelor76_legal_inside_toc(testdir, monkeypatch):
    source = power.link(power.BACHELOR076_PDF)
    tests.toc.run(f'-i {source} --rules', monkeypatch=monkeypatch)

    findings = protocol.findings_from_path(testdir.tmpdir)
    assert len(tests.select(findings, 1365)) == 1


def test_toc_cli_bachelor76_roman_page_numbers(testdir, monkeypatch):
    """Regression test to verify that roman page numbers does not break
    page distance computation etc."""
    source = power.link(power.BACHELOR076_PDF)
    tests.toc.run(f'-i {source}', monkeypatch=monkeypatch)
    findings = protocol.findings_from_path(testdir.tmpdir)
    assert findings
