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


def test_rules_bachelor63_regression(testdir, monkeypatch):
    """Ensure to handle roman numbers correctly. Before this regression
    test, roman page number converter fails when running --rules. Bug is
    fixed in lower level API by upgrading."""
    source = power.link(power.BACHELOR063_PDF)
    tests.toc.run(f'-i {source} --rules', monkeypatch=monkeypatch)

    findings = protocol.findings_from_path(testdir.tmpdir)
    findings = protocol.select(findings, pages=7, msgid=1360)
    assert len(findings) == 2  # VALIDATE LATER
