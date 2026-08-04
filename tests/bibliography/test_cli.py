# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utilatest

import decider_bib
import tests.bibliography


def test_decider_bib_cli_help(mp):
    tests.bibliography.run('--help', mp=mp)


@utilatest.hasprog(decider_bib.PROCESS)
def test_decider_bib_nomonkey_cli_help():
    utila.run(f'{decider_bib.PROCESS} --help')
