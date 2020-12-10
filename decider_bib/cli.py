#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import decider_bib
import decider_ref

DESCRIPTION = ''

USER = 'user'
DEVELOPER = 'developer'

WORKPLAN = [
    utila.create_step(
        'order',
        [
            utila.ResultFile('detector', 'bibliography_detected'),
        ],
        (USER, DEVELOPER),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_ref.ROOT,
        featurepackage='decider_bib.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_bib.PROCESS,
            version=decider_ref.__version__,
        ),
    )
