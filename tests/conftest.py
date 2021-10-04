# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import writers

import decider_ref

PACKAGE = decider_ref.PACKAGE
power.setup(decider_ref.ROOT)

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

WORKER = 6

RESOURCES = [
    power.DISS143_PDF,
    (power.MASTER116_PDF, '0:50,75:115'),
    (power.MASTER098_PDF, '0:10,43:65,88:97'),
    power.BACHELOR076_PDF,
    power.MASTER072_PDF,
    power.BACHELOR090_PDF,
    (power.BACHELOR128_PDF, '0:70'),
    power.BACHELOR037_PDF,
    (power.BACHELOR056_PDF, '0:15,49:55'),
    (power.BACHELOR063_PDF, '0:20,59'),
    (power.BACHELOR051_PDF, '0:10,40:52'),
    (power.MASTER091B_PDF, '0:20,81:91'),
    (power.TECH024_PDF, '0:15'),
    (power.MASTER099_PDF, '0:10'),
    (power.MASTER127_PDF, '121:126'),
    (power.MASTER083_PDF, '75:82'),
    (power.ORDER107_PDF, '104:110'),
    (power.MASTER078_PDF, '0:10'),
    (power.BACHELOR075_PDF, '15:25,70:74'),
    (power.BACHELOR241_PDF, '0:10,235:242'),
    (power.DISS266_PDF, '0:10,214:246'),
]

RESOURCES_NOTOC = [
    (power.DOCU035_PDF, ':'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        files=resources,
        destination=power.generated(),
        full=True,
        base=power.REPOSITORY,
        worker=WORKER,
        pages=':',
    )


def extract_notoc(resources):
    genex.extract_removepages(
        resources,
        removepages='1:5',
        folder='notoc',
        groupme=True,
    )


def install():
    # generate docs after project is installed properly
    writers.generate()
