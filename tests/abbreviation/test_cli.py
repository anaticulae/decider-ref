# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo
import utilotest

import abbreviation_
import tests.abbreviation


def test_decider_abbr_cli_help(mp):
    tests.abbreviation.run('--help', mp=mp)


@utilotest.hasprog(abbreviation_.PROCESS)
def test_decider_abbr_nomonkey_cli_help():
    utilo.run(f'{abbreviation_.PROCESS} --help')
