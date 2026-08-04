# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import detector.path
import hoverpower
import pytest
import utilotest

import decider_bib.order
import decider_bib.path
import decider_bib.serialize


@pytest.mark.xfail(reason='broken bib')
@utilotest.requires(hoverpower.BACHELOR063_PDF)
def test_order_bib_bachelor63_theissen():
    source = hoverpower.link(hoverpower.BACHELOR063_PDF)
    table = detector.path.bibliography_detected(source)
    bibliography = decider_bib.serialize.load_bibliography_reference(table)
    theissen = decider_bib.order.theissen_sort(bibliography)
    assert theissen == bibliography
