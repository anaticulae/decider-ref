# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import pytest

import tests.caption


@pytest.mark.xfail(reason='duplicated caption parsing')
def test_caption_basic_diss172(testdir, monkeypatch):
    source = power.link(power.DISS172_PDF)
    tests.caption.run(
        f'-i {source} -o {testdir.tmpdir} --basic',
        monkeypatch=monkeypatch,
    )
    findings = protocol.findings_from_path(testdir.tmpdir)
    assert not findings
