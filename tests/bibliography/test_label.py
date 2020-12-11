# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import serializeraw

import decider_bib
import tests.bibliography


def run_label(source, monkeypatch, testdir, msgid=None):
    source = power.link(source)
    cmd = f'-i {source} --label'
    tests.bibliography.run(cmd, monkeypatch=monkeypatch)
    path = decider_bib.path.decider_bib_label_user(testdir.tmpdir)
    result = protocol.select_findings(
        serializeraw.load_findings(path),
        msgid=msgid,
    )
    return result


def test_bib_no_page(testdir, monkeypatch):
    nopages = run_label(power.MASTER116_PDF, monkeypatch, testdir, {6061})
    assert len(nopages) == 71  #TODO: VALIDATE LATER


def test_bib_page_number_unprecise(testdir, monkeypatch):
    unprecise = run_label(power.MASTER116_PDF, monkeypatch, testdir, {6062})
    assert len(unprecise) == 3  #TODO: VALIDATE LATER
