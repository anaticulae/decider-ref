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
import utilatest

import decider_toc.features.complexity
import tests.toc


@utilatest.requires(power.BACHELOR063_PDF)
def test_bachelor63_regression_complexity(testdir, monkeypatch):
    """Do not mix roman and arabic numbers in toc length computation.
    TODO: HANDLE ROMAN NUMBERS
    """
    source = power.link(power.BACHELOR063_PDF)
    with monkeypatch.context() as context:
        context.setattr(
            decider_toc.features.complexity,
            'CHAPTER_LENGTH_CHECKER_MIN',
            0.0,
        )
        tests.toc.run(f'-i {source} --complexity', monkeypatch=monkeypatch)
    findings = protocol.findings_from_path(testdir.tmpdir)
    findings = protocol.select_pages(findings, pages=(6, 7))
    assert findings  # count is not important


@utilatest.requires(power.MASTER116_PDF)
def test_toc_decider_toc_complexity_regression():
    """1351 fails with converting ROMAN number to int. In the future
    this will be resolved with ROMAN-number to pdf-page converter."""
    source = power.link(power.MASTER116_PDF)
    tests.toc.lint(source, decider_toc.features.complexity)


def test_decider_toc_complexity_bachelor128_regression():
    """Page 4 is the page of table of content."""
    source = power.link(power.BACHELOR128_PDF)
    findings = tests.toc.linter(source, decider_toc.features.complexity)
    findings = [item for item in findings if item.location.page == 4]
    assert len(findings) == 2
