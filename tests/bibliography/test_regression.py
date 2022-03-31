# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import tests.bibliography


def test_empty_bib(testdir, monkeypatch):
    """Run decider with empty bib.

    Before this patch, loading data creates invalid data structure which
    produces an runtime error.
    """
    source = power.link(power.MASTER049_PDF)
    todo = 'create empty bib and remove master049 which is now detected correctly'
    assert not serializeraw.load_bibliography_reference(source), todo
    cmd = f'-i {source} -o {testdir.tmpdir}'
    tests.bibliography.run(cmd, monkeypatch=monkeypatch)
