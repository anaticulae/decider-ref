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
import tests
import tests.bibliography


def run_label(source, mp, td, msgid=None, pages=None):
    utilatest.fixture_requires(source)
    source = power.link(source)
    utilatest.fixture_requires(source)
    cmd = f'-i {source} --label'
    tests.bibliography.run(cmd, mp=mp)
    path = decider_bib.path.decider_bib_label_user(td.tmpdir)
    result = protocol.select_findings(
        serializeraw.load_findings(path),
        msgid=msgid,
    )
    if pages is not None:
        result = protocol.select_pages(result, pages)
    return result


@pytest.mark.xfail(reason='bib table included')
def test_bib_no_page_master116(td, mp):
    nopages = run_label(power.MASTER116_PDF, mp, td, {6061})
    expected_intext = 82
    expected_in_tof = 14  # duplication as a result out of text
    expected = expected_intext + expected_in_tof
    assert len(nopages) == expected  # VALIDTED


def test_bib_no_page_master98(td, mp):
    nopages = run_label(power.MASTER098_PDF, mp, td, {6061})
    assert len(nopages) in (10, 9)  # TODO: VALIDATE LATER


def test_bib_page_number_unprecise(td, mp):
    unprecise = run_label(power.MASTER116_PDF, mp, td, {6062})
    assert len(unprecise) in (2, 3)  # TODO: VALIDATE LATER


@pytest.mark.xfail(reason='enable later')
def test_bib_label_exists(td, mp):
    missing = run_label(power.MASTER116_PDF, mp, td, {6050})
    # all reference in text are located in bib table
    assert not missing


@pytest.mark.xfail(reason='improve sentence parser')
def test_bib_source_not_required(td, mp):
    notrequired = run_label(power.MASTER116_PDF, mp, td, {6051})
    assert not notrequired  # TODO: VALIDATE LATER


def test_bib_label_improvement(td, mp):
    improvement = run_label(power.MASTER091B_PDF, mp, td, {6070})
    assert improvement


@pytest.mark.xfail(reason='???')
def test_regression_bachelor75(td, mp):
    """Do not fail on [10]-pattern lookup."""
    linting = run_label(power.BACHELOR075_PDF, mp, td, {6061})
    assert len(linting) == 21  # NOT VALIDATED


@pytest.mark.xfail(reason='software integration')
def test_label_bib_ref_missing(td, mp):
    """No missing intext bib reference."""
    linting = run_label(power.BACHELOR075_PDF, mp, td, {6050})
    assert not linting


@pytest.mark.xfail(reason='investigate later')
def test_label_bib_not_required(td, mp):
    """All bib entrees are required."""
    linting = run_label(power.BACHELOR075_PDF, mp, td, {6051})
    assert not linting


def test_regression_bachelor90(td, mp):
    """As a result of invalid bib parsing, the linter produces some
    false postive errors.

    This tests ensures that bib parsing and bib reference parsing is
    aligned together. If an error occurs, check this parsing.
    """
    error = run_label(power.MASTER091B_PDF, mp, td, {6050})
    assert not error


@utilatest.requires(power.BACHELOR056_PDF)
def test_bib_source_not_found_bachelor56_page6(td, mp):
    """(Vgl. Borkenstein: 1.13) was parsed not correctly and therefore
    detected as missing reference. After improving label parser, this
    behavior is fixed."""
    bibliography = tests.bibliography.load_bib_table(power.BACHELOR056_PDF)
    assert bibliography, 'require bib table to run verification'
    notrequired = run_label(
        power.BACHELOR056_PDF,
        mp,
        td,
        msgid={6050},
        pages=6,
    )
    assert not notrequired


@pytest.mark.xfail(reason='enable later')
def test_diss143_numbered_label_6050(td, mp):
    error = run_label(power.DISS143_PDF, mp, td, {6050})
    assert not error


def test_diss143_add_pagination_hint(td, mp):
    hint = run_label(power.DISS143_PDF, mp, td, {6063})
    assert len(hint) == 1


@pytest.mark.xfail(reason='enable later')
def test_reg_bib_not_required_diss172(td, mp):
    """All bib entrees are required? TODO: VERIFY"""
    # TODO: NOT READY YET
    linting = run_label(power.DISS172_PDF, mp, td, {6051})
    assert not linting
