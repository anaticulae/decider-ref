# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import tests.abbreviation


def test_abbreviation_sorted_bachelor37(testdir, monkeypatch):
    # TODO: ADJUST TABLE PAGE LOADER
    linted = tests.abbreviation.run_table(
        power.BACHELOR037_PDF,
        monkeypatch,
        testdir,
        msgid=15010,
    )
    assert len(linted) == 1
