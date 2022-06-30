# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import tests.abbreviation


def test_abbrev_bachelor028_intable(testdir, monkeypatch):
    """Bachelor028 does not contain any ref table therefore we do not
    expect any linting here."""
    linted = tests.abbreviation.run_table(
        power.BACHELOR028_PDF,
        monkeypatch,
        testdir,
        msgid=15016,
    )
    assert not linted
