# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import utilo

import decider_abb

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'table',
        [
            utilo.ResultFile('reftable', 'abbrev_abbrev'),
            utilo.ResultFile('words', 'abbreviation_detected'),
        ],
        output=protoerror.ResultDefault,
    ),
]


def main():
    hook = protoerror.integrate(
        root=decider_abb.ROOT,
        features='decider_abb.features',
    )
    utilo.featurepack(
        workplan=WORKPLAN,
        root=decider_abb.ROOT,
        featurepackage='decider_abb.features',
        config=utilo.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_abb.PROCESS,
            pages=True,
            version=decider_abb.__version__,
        ),
    )
