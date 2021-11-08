# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_toc

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'basic',
        [
            utila.ResultFile('groupme', 'toc_toc'),
            utila.ResultFile('rawmaker', 'outlines_outlines'),
        ],
        ('user', 'developer'),
    ),
    utila.create_step(
        'complexity',
        [
            utila.ResultFile('groupme', 'toc_toc'),
        ],
        ('user', 'developer'),
    ),
    utila.create_step(
        'rules',
        [
            utila.ResultFile('groupme', 'toc_toc'),
        ],
        ('user', 'developer'),
    ),
    utila.create_step(
        'style',
        [
            utila.ResultFile('groupme', 'toc_toc'),
        ],
        ('user', 'developer'),
    ),
    utila.create_step(
        'sync',
        [
            utila.ResultFile('groupme', 'toc_toc'),
            utila.ResultFile('rawmaker', 'outlines_outlines'),
            utila.ResultFile('words', 'headlines_headlines', optional=True),
            utila.ResultFile('words', 'headlines_oneline', optional=True),
        ],
        ('user', 'developer'),
    ),
]


def main():
    hook = protocol.integrate(
        root=decider_toc.ROOT,
        features='decider_toc.features',
    )
    docinfo = protocol.integrate_docinfo()
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_toc.ROOT,
        featurepackage='decider_toc.features',
        config=utila.FeaturePackConfig(
            cli_hook=[
                docinfo,
                hook,
            ],
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_toc.PROCESS,
            pages=True,
            version=decider_toc.__version__,
        ),
    )
