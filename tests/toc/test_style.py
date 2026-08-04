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
import pytest
import utila
import utilatest

import decider_toc.duplicated
import tests.toc


def test_toc_style_bachelor76_duplicated_words(td, mp):
    duplicated = run_style(power.BACHELOR076_PDF, 1380, td, mp)
    assert len(duplicated) == 1, str(duplicated)
    assert 'Industrie 4.0' in duplicated[0].solution.description


def test_toc_style_bachelor51_duplicated_words(td, mp):
    """Skip `EMS` detection in `1 EINLEITUNG UND PROBLEMSTELLUNG`."""
    with mp.context() as context:
        # make this test config independent
        context.setattr(
            decider_toc.duplicated,
            'DUPLICATES_COUNT_MIN',
            lambda _: 5,
        )
        duplicated = run_style(
            power.BACHELOR051_PDF,
            1380,
            td,
            mp,
        )
    assert duplicated, 'check DUPLICATES_COUNT_MIN'
    description = duplicated[0].solution.description
    assert 'wird 5 mal in' in description


@pytest.mark.xfail(reason='???')
def test_toc_words_duplicated_master072(td, mp):
    """Ensure that subpattern arn't detected twice."""
    duplicated = run_style(power.MASTER072_PDF, 1380, td, mp)
    assert len(duplicated) == 2, str(duplicated)
    assert '„Social Web“' in duplicated[0].solution.description
    assert '„Social“' in duplicated[1].solution.description


def run_style(source, msgid, td, mp):
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.toc.run(f'-i {source} --style', mp=mp)
    # load findings
    findings = protocol.findings_from_path(td.tmpdir)
    findings = utila.flatten_content(findings)
    selected = protocol.select_findings(findings, msgid=msgid)
    return selected
