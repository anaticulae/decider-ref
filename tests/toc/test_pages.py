# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elements
import power
import utilatest

import tests


@utilatest.requires(power.TECH024_PDF)
def test_toc_pages_validate():
    toc = tests.toc.tableofcontent(power.link(power.TECH024_PDF))
    validated = elements.validate_toc(toc)
    assert validated == [], validated


@utilatest.requires(power.TECH024_PDF)
def test_toc_pages_validate_with_errors():
    toc = tests.toc.tableofcontent(power.link(power.TECH024_PDF))
    # introduce some errors
    toc.children[1].page = 10
    toc.children[5].page = 20
    validated = elements.validate_toc(toc)
    assert len(validated) == 2, validated
