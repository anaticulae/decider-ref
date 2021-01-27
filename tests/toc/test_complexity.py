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


def test_bachelor63_regression_complexity(testdir, monkeypatch):
    """Do not mix roman and arabic numbers in toc length computation.
    TODO: HANDLE ROMAN NUMBERS
    """
    source = power.link(power.BACHELOR063_PDF)
    tests.toc.run(f'-i {source} --complexity', monkeypatch=monkeypatch)

    findings = protocol.findings_from_path(testdir.tmpdir)
    findings = protocol.select_pages(findings, pages=(6, 7))
    assert findings  # count is not important
