# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_abb
import tests.abbreviation


def test_decider_abbr_cli_help(monkeypatch):
    tests.abbreviation.run('--help', monkeypatch=monkeypatch)


def test_decider_abbr_nomonkey_cli_help():
    utila.run(f'{decider_abb.PROCESS} --help')
