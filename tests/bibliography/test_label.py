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

import decider_bib
import tests
import tests.bibliography


def run_label(source, monkeypatch, testdir, msgid=None, pages=None):
    source = power.link(source)
    cmd = f'-i {source} --label'
    tests.bibliography.run(cmd, monkeypatch=monkeypatch)
    path = decider_bib.path.decider_bib_label_user(testdir.tmpdir)
    result = protocol.select_findings(
        serializeraw.load_findings(path),
        msgid=msgid,
    )
    if pages is not None:
        result = protocol.select_pages(result, pages)
    return result


def test_bib_no_page_master116(testdir, monkeypatch):
    nopages = run_label(power.MASTER116_PDF, monkeypatch, testdir, {6061})
    assert len(nopages) == 122  # TODO: VALIDATE LATER


@pytest.mark.xfail(reason='enable later')
def test_bib_no_page_master98(testdir, monkeypatch):
    nopages = run_label(power.MASTER098_PDF, monkeypatch, testdir, {6061})
    assert len(nopages) == 1  # TODO: VALIDATE LATER


def test_bib_page_number_unprecise(testdir, monkeypatch):
    unprecise = run_label(power.MASTER116_PDF, monkeypatch, testdir, {6062})
    assert len(unprecise) == 3  # TODO: VALIDATE LATER


def test_bib_label_exists(testdir, monkeypatch):
    missing = run_label(power.MASTER116_PDF, monkeypatch, testdir, {6050})
    # all reference in text are located in bib table
    assert not missing


def test_bib_source_not_required(testdir, monkeypatch):
    notrequired = run_label(power.MASTER116_PDF, monkeypatch, testdir, {6051})
    assert not notrequired  # TODO: VALIDATE LATER


def test_bib_source_not_found_bachelor56_page6(testdir, monkeypatch):
    """(Vgl. Borkenstein: 1.13) was parsed not correctly and therefore
    detected as missing reference. After improving label parser, this
    behavior is fixed."""
    bibliography = tests.bibliography.load_bib_table(power.BACHELOR056_PDF)
    assert bibliography, 'require bib table to run verification'
    notrequired = run_label(
        power.BACHELOR056_PDF,
        monkeypatch,
        testdir,
        msgid={6050},
        pages=6,
    )
    assert not notrequired
