# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
import writers
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import decider_ref

PACKAGE = decider_ref.PACKAGE
hoverpower.setup(decider_ref.ROOT)

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

RESOURCES = [
    (hoverpower.BACHELOR051_PDF, '0:10,40:52'),
    (hoverpower.BACHELOR056_PDF, '0:15,49:55'),
    (hoverpower.BACHELOR063_PDF, '0:20,59'),
    (hoverpower.BACHELOR075_PDF, '15:25,70:74'),
    (hoverpower.BACHELOR077_PDF, '0:20'),
    (hoverpower.BACHELOR128_PDF, '0:70'),
    (hoverpower.BACHELOR241_PDF, '0:10,235:242'),
    (hoverpower.DISS172_PDF, '100:172'),
    (hoverpower.DISS266_PDF, '0:10,214:246'),
    (hoverpower.DISS406_PDF, '3:12'),
    (hoverpower.MASTER049_PDF, '45:50'),
    (hoverpower.MASTER078_PDF, '0:10'),
    (hoverpower.MASTER083_PDF, '75:82'),
    (hoverpower.MASTER091B_PDF, '0:20,81:91'),
    (hoverpower.MASTER098_PDF, '0:10,43:65,88:97'),
    (hoverpower.MASTER099_PDF, '0:10'),
    (hoverpower.MASTER116_PDF, '0:50,75:115'),
    (hoverpower.MASTER127_PDF, '121:126'),
    (hoverpower.ORDER107_PDF, '104:110'),
    (hoverpower.TECH024_PDF, '0:15'),
    hoverpower.BACHELOR028_PDF,
    hoverpower.BACHELOR037_PDF,
    hoverpower.BACHELOR067_PDF,
    hoverpower.BACHELOR076_PDF,
    hoverpower.BACHELOR090_PDF,
    hoverpower.DISS143_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.TECH019_PDF,
]
WORKER = utilotest.worker_count(5, onci=len(RESOURCES))

RESOURCES_NOTOC = [
    (hoverpower.DOCU035_PDF, ':'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    gennex.extract(
        files=resources,
        full=True,
        base=hoverpower.REPOSITORY,
        worker=WORKER,
    )


def extract_notoc(resources):
    gennex.extract_removepages(
        resources,
        removepages='1:5',
        folder='notoc',
        cleanup=True,
        footnote=True,
        groupme=True,
        headnote=True,
        pagenumber=True,
        worker=len(resources),
    )


def install():
    # generate docs after project is installed properly
    writers.generate()
