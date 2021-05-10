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

import tests.toc


def test_toc_style_bachelor76_duplicated_words(testdir, monkeypatch):
    duplicated = run_style(power.BACHELOR076_PDF, 1380, testdir, monkeypatch)
    assert len(duplicated) == 1, str(duplicated)
    assert 'Industrie 4.0' in duplicated[0].solution.description


def test_toc_style_bachelor51_duplicated_words(testdir, monkeypatch):
    """Skip `EMS` detection in `1 EINLEITUNG UND PROBLEMSTELLUNG`."""
    duplicated = run_style(power.BACHELOR051_PDF, 1380, testdir, monkeypatch)
    description = duplicated[0].solution.description
    assert 'wird 5 mal in' in description


def run_style(source, msgid, testdir, monkeypatch):
    source = power.link(source)
    tests.toc.run(f'-i {source} --style', monkeypatch=monkeypatch)

    findings = protocol.findings_from_path(testdir.tmpdir)
    findings = findings[0].content

    selected = protocol.select_findings(findings, msgid=msgid)
    return selected
