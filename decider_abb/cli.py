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

DESCRIPTION = ''

DEFAULT = ('user', 'developer')

WORKPLAN = [
    utila.create_step(
        'table',
        [
            utila.ResultFile('groupme', 'abbreviation_abbreviation'),
        ],
        output=DEFAULT,
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_abb.ROOT,
        featurepackage='decider_abb.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_abb.PROCESS,
            version=decider_abb.__version__,
        ),
    )
