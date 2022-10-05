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
import utilatest

import decider_toc.features.complexity
import tests.toc


@utilatest.requires(power.BACHELOR063_PDF)
def test_bachelor63_regression_complexity(td, mp):
    """Do not mix roman and arabic numbers in toc length computation.
    TODO: HANDLE ROMAN NUMBERS
    """
    source = power.link(power.BACHELOR063_PDF)
    with mp.context() as context:
        context.setattr(
            decider_toc.features.complexity,
            'CHAPTER_LENGTH_CHECKER_MIN',
            0.0,
        )
        tests.toc.run(f'-i {source} --complexity', mp=mp)
    findings = protocol.findings_from_path(td.tmpdir)
    findings = protocol.select_pages(findings, pages=(6, 7))
    assert findings  # count is not important


@utilatest.requires(power.MASTER116_PDF)
def test_toc_decider_toc_complexity_regression():
    """1351 fails with converting ROMAN number to int. In the future
    this will be resolved with ROMAN-number to pdf-page converter."""
    source = power.link(power.MASTER116_PDF)
    tests.toc.lint(source, decider_toc.features.complexity)


@utilatest.requires(power.BACHELOR128_PDF)
def test_decider_toc_complexity_bachelor128_regression():
    """Page 4 is the page of table of content."""
    source = power.link(power.BACHELOR128_PDF)
    findings = tests.toc.linter(
        source,
        decider_toc.features.complexity,
        msgids=1351,
    )
    findings = [item for item in findings if item.location.page == 4]
    assert len(findings) == 2
    findings = tests.toc.linter(
        source,
        decider_toc.features.complexity,
        msgids=1370,
    )
    findings = [item for item in findings if item.location.page == 4]
    complexity_error = 3
    assert len(findings) == complexity_error
    msg = str(findings)
    # Das ´Projekt-Demenz-Arnsberg`
    assert msg.count('**7**') == 1
    # Verarbeitungen der Erkenntnisse
    # Auswertung der Interviewergebnisse
    assert msg.count('**16**') == 2


@utilatest.requires(power.BACHELOR077_PDF)
def test_toc_complexity_bachelor077_regression():
    source = power.link(power.BACHELOR077_PDF)
    findings = tests.toc.linter(
        source,
        decider_toc.features.complexity,
        msgids=1370,
    )
    assert len(findings) == 4
