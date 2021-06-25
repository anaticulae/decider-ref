# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utilatest

import tests


@utilatest.requires(power.MASTER072_PDF)
def test_decider_bib_plot_bib_overview(testdir, monkeypatch):
    source = power.link(power.MASTER072_PDF)
    cmd = f'-i {source} --plot'
    tests.bibliography.run(cmd, monkeypatch=monkeypatch)
    assert os.path.exists('decider_bibliography__plot_year_histogram.png')
