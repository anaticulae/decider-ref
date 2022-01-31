# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_abb

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'table',
        [
            utila.ResultFile('groupme', 'abbreviation_abbreviation'),
        ],
        output=protocol.ResultDefault,
    ),
]


def main():
    hook = protocol.integrate(
        root=decider_abb.ROOT,
        features='decider_abb.features',
    )
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_abb.ROOT,
        featurepackage='decider_abb.features',
        config=utila.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_abb.PROCESS,
            version=decider_abb.__version__,
        ),
    )
