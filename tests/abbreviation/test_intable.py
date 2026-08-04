# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower

import tests.abbreviation


def test_abbrev_bachelor028_intable(td, mp):
    """Bachelor028 does not contain any ref table therefore we do not
    expect any linting here."""
    linted = tests.abbreviation.run_table(
        hoverpower.BACHELOR028_PDF,
        mp,
        td,
        msgid=15016,
    )
    assert not linted
