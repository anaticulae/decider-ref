# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import indagator.path
import pytest
import utilotest

import bibliography_.order
import bibliography_.serialize


@pytest.mark.xfail(reason='broken bib')
@utilotest.requires(hoverpower.BACHELOR063_PDF)
def test_order_bib_bachelor63_theissen():
    source = hoverpower.link(hoverpower.BACHELOR063_PDF)
    table = indagator.path.bibliography_detected(source)
    bibliography = bibliography_.serialize.load_bibliography_reference(table)
    theissen = bibliography_.order.theissen_sort(bibliography)
    assert theissen == bibliography
