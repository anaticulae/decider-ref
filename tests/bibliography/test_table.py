# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
