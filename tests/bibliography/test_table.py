# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import pytest
import serializeraw
import utilatest

import decider_bib
import tests.bibliography


def run_table(source, monkeypatch, testdir, msgid=None):
    source = power.link(source)
    utilatest.fixture_requires(source)
    cmd = f'-i {source} --table'
    tests.bibliography.run(cmd, monkeypatch=monkeypatch)
    path = decider_bib.path.decider_bib_table_user(testdir.tmpdir)
    result = protocol.select_findings(
        serializeraw.load_findings(path),
        msgid=msgid,
    )
    return result


def test_bib_sorting_master98(testdir, monkeypatch):
    unsorted_bib = run_table(power.MASTER098_PDF, monkeypatch, testdir, {6000})
    assert len(unsorted_bib) == 1


def test_bib_bachelor75_regression_table(testdir, monkeypatch):
    """Do not fail when parsing empty authors."""
    run_table(power.BACHELOR075_PDF, monkeypatch, testdir)


def test_bib_bachelor75_regression_bib_sort(testdir, monkeypatch):
    """Bib table is ??not?? sorted correctly.

    In the current state this check is disabled cause of not fully
    parsed bibs.
    """
    findings = run_table(power.BACHELOR075_PDF, monkeypatch, testdir, {6000})
    assert not findings
    # TODO: VERIFY ORDER AND DETECTED MISS SORTING OF BIB


def test_bib_order107_unbalanced_brackets(testdir, monkeypatch):
    unbalacend_brackets = run_table(
        power.ORDER107_PDF,
        monkeypatch,
        testdir,
        {6010},
    )
    # 1. (1983]: Gliederung und Benummerung in Texten.
    # 2. (Zugriff: 22.04.07
    # reduce to 2 after having common message
    assert len(unbalacend_brackets) == 3


def test_bib_master127_typos(testdir, monkeypatch):
    typo_detected = run_table(
        power.MASTER127_PDF,
        monkeypatch,
        testdir,
        {6011},
    )
    assert len(typo_detected) == 5


@pytest.mark.xfail(reason='improve bib parser')
def test_bib_sorting_master116(testdir, monkeypatch):
    unsorted_bib = run_table(power.MASTER116_PDF, monkeypatch, testdir, {6000})
    assert not unsorted_bib  # TODO: VALIDATE LATER


def test_bib_master083_differs(testdir, monkeypatch):
    """Detect bib entrees which differ from style of other bibs."""
    detected = run_table(
        power.MASTER083_PDF,
        monkeypatch,
        testdir,
        {6020},
    )
    # TODO: IMPROVE AND CLARIFY DIFFER CHECKER
    assert len(detected) in (2, 5)  # TODO: NOT VALIDATED


def test_bib_table_bachelor241_too_few_bibs(testdir, monkeypatch):
    detected = run_table(
        power.BACHELOR241_PDF,
        monkeypatch,
        testdir,
        {6006},
    )
    assert len(detected) == 1


def test_bib_table_diss266_too_many_bibs(testdir, monkeypatch):
    detected = run_table(
        power.DISS266_PDF,
        monkeypatch,
        testdir,
        {6007},
    )
    assert len(detected) == 1
