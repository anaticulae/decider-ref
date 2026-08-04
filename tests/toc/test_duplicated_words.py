# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilotest

import decider_toc.duplicated


@pytest.mark.xfail(reason='check later')
@utilotest.requires(hoverpower.MASTER098_PDF)
def test_duplicated_words_master098():
    source = hoverpower.link(hoverpower.MASTER098_PDF)
    toc = serializeraw.load_toc(source)
    assert toc
    validated = decider_toc.duplicated.validate(toc)
    assert len(validated) == 1  # TODO: VALIDATE LATER


@pytest.mark.xfail(reason='check later')
@utilotest.requires(hoverpower.DISS406_PDF)
def test_duplicated_words_diss406():
    source = hoverpower.link(hoverpower.DISS406_PDF)
    toc = serializeraw.load_toc(source)
    assert toc
    validated = decider_toc.duplicated.validate(toc)
    # DUPLICATES_COUNT_MIN dependent
    assert len(validated) == 3  # NOT VALIDATED
