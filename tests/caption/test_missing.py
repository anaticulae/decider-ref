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
import utilatest

import tests.caption


@utilatest.requires(power.TECH019_PDF)
def test_caption_missing_some_tech019(td, mp):
    source = power.link(power.TECH019_PDF)
    tests.caption.run(
        f'-i {source} -o {td.tmpdir} --missing',
        mp=mp,
    )
    findings = protocol.findings_from_path(td.tmpdir)
    assert findings


@utilatest.requires(power.TECH019_PDF)
def test_caption_missing_all_caption_tech019(td, mp):
    source = power.link(power.TECH019_PDF)
    tests.caption.run(
        f'-i {source} -o {td.tmpdir} --missing',
        mp=mp,
    )
    findings = protocol.findings_from_path(td.tmpdir, msgid=6303)
    assert len(findings) == 1
    assert findings
