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
import utila
import utilatest

import tests.toc


@utilatest.requires(power.DISS406_PDF)
def test_toc_diff406(td, mp):
    source = power.link(power.DISS406_PDF)
    tests.toc.run(f'-i {source}', mp=mp)
    findings = protocol.findings_from_path(td.tmpdir)
    findings = utila.flatten_content(findings)
    assert findings
    # After supporting S. 120 as page numbers 1360 should not occurrs anymore
    assert not protocol.select_findings(findings, msgid=1360)
