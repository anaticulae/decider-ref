# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import serializeraw
import utilotest

import decider_bib
import tests.bibliography


def run_table(source, mp, td, msgid=None):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    cmd = f'-i {source} --table'
    tests.bibliography.run(cmd, mp=mp)
    path = decider_bib.path.decider_bib_table_user(td.tmpdir)
    result = protoerror.select_findings(
        serializeraw.load_findings(path),
        msgid=msgid,
    )
    return result


def test_bib_sorting_master98(td, mp):
    unsorted_bib = run_table(hoverpower.MASTER098_PDF, mp, td, {6000})
    assert len(unsorted_bib) == 1


def test_bib_bachelor75_regression_table(td, mp):
    """Do not fail when parsing empty authors."""
    run_table(hoverpower.BACHELOR075_PDF, mp, td)


def test_bib_bachelor75_regression_bib_sort(td, mp):
    """Bib table is ??not?? sorted correctly.

    In the current state this check is disabled cause of not fully
    parsed bibs.
    """
    findings = run_table(hoverpower.BACHELOR075_PDF, mp, td, {6000})
    assert not findings
    # TODO: VERIFY ORDER AND DETECTED MISS SORTING OF BIB


def test_bib_order107_unbalanced_brackets(td, mp):
    unbalacend_brackets = run_table(
        hoverpower.ORDER107_PDF,
        mp,
        td,
        {6010},
    )
    # 1. (1983]: Gliederung und Benummerung in Texten.
    # 2. (Zugriff: 22.04.07
    # reduce to 2 after having common message
    assert len(unbalacend_brackets) == 3


def test_bib_master127_typos(td, mp):
    typo_detected = run_table(
        hoverpower.MASTER127_PDF,
        mp,
        td,
        {6011},
    )
    assert len(typo_detected) in {5, 7}


def test_bib_sorting_master116(td, mp):
    unsorted_bib = run_table(hoverpower.MASTER116_PDF, mp, td, {6000})
    assert not unsorted_bib  # TODO: VALIDATE LATER


def test_bib_master083_differs(td, mp):
    """Detect bib entrees which differ from style of other bibs."""
    detected = run_table(
        hoverpower.MASTER083_PDF,
        mp,
        td,
        {6020},
    )
    # TODO: IMPROVE AND CLARIFY DIFFER CHECKER
    assert len(detected) in {2, 4, 5}  # TODO: NOT VALIDATED


def test_bib_table_bachelor241_too_few_bibs(td, mp):
    detected = run_table(
        hoverpower.BACHELOR241_PDF,
        mp,
        td,
        {6006},
    )
    assert len(detected) == 1


def test_bib_table_diss266_too_many_bibs(td, mp):
    detected = run_table(
        hoverpower.DISS266_PDF,
        mp,
        td,
        {6007},
    )
    assert len(detected) == 1


def test_bib_sorted_diss172(td, mp):
    detected = run_table(
        hoverpower.DISS172_PDF,
        mp,
        td,
        {6000},
    )
    assert not detected
