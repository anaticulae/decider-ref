# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_cap
import tests.caption


def test_cap_cli_help(monkeypatch):
    tests.caption.run('--help', monkeypatch=monkeypatch)


def test_cap_nomonkey_cli_help():
    utila.run(f'{decider_cap.PROCESS} --help')
