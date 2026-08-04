# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import utilo

import decider_toc

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'basic',
        [
            utilo.ResultFile('reftable', 'toc_toc'),
            utilo.ResultFile('rawmaker', 'outlines_outlines'),
            utilo.ResultFile('words', 'headlines_headlines', optional=True),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'complexity',
        [
            utilo.ResultFile('reftable', 'toc_toc'),
            utilo.ResultFile('groupme', 'pagenumbers_magic'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'rules',
        [
            utilo.ResultFile('reftable', 'toc_toc'),
            utilo.ResultFile('sections', 'section_result'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'style',
        [
            utilo.ResultFile('reftable', 'toc_toc'),
        ],
        protoerror.ResultDefault,
    ),
    utilo.create_step(
        'sync',
        [
            utilo.ResultFile('reftable', 'toc_toc'),
            utilo.ResultFile('rawmaker', 'outlines_outlines'),
            utilo.ResultFile('words', 'headlines_headlines', optional=True),
            utilo.ResultFile('words', 'headlines_oneline', optional=True),
        ],
        protoerror.ResultDefault,
    ),
]


def main():
    hook = protoerror.integrate(
        root=decider_toc.ROOT,
        features='decider_toc.features',
    )
    docinfo = protoerror.integrate_docinfo()
    utilo.featurepack(
        workplan=WORKPLAN,
        root=decider_toc.ROOT,
        featurepackage='decider_toc.features',
        config=utilo.FeaturePackConfig(
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
