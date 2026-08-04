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
import pytest
import utilotest

import tests


@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_toc_bachelor90_toc_document_sync(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR090_PDF)
    tests.toc.run(f'-i {source} --sync', mp=mp)

    findings = protoerror.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1330)) == 1


@pytest.mark.xfail(reason='broken headlines parser')
@utilotest.requires(hoverpower.BACHELOR037_PDF)
def test_toc_bachelor37_toc_document_sync(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR037_PDF)
    tests.toc.run(f'-i {source} --sync', mp=mp)

    findings = protoerror.findings_from_path(td.tmpdir)
    assert len(tests.select(findings, 1330)) == 1

    description = findings[0].content[0].solution.description
    assert '* Methode3' in description
    assert '* Datenanalyse / Statistik' in description
    assert '* Inhalt' not in description
