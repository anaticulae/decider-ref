# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import writers

import decider_reference

PACKAGE = decider_reference.PACKAGE
power.setup(decider_reference.ROOT)

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

WORKER = 6

RESOURCES = [
    (power.MASTER116_PDF, '0:50,75:115'),
    (power.MASTER098_PDF, '0:10,43:65,88:97'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        files=resources + [power.REPOSITORY],
        destination=power.generated(),
        full=True,
        worker=WORKER,
    )


def install():
    # generate docs after project is installed properly
    writers.generate()
