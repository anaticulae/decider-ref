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

import abbreviation_

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
        root=abbreviation_.ROOT,
        features='abbreviation.features',
    )
    utilo.featurepack(
        workplan=WORKPLAN,
        root=abbreviation_.ROOT,
        featurepackage='abbreviation_.features',
        config=utilo.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=abbreviation_.PROCESS,
            pages=True,
            version=abbreviation_.__version__,
        ),
    )
