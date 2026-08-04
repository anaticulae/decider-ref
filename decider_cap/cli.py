# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import utilo

import decider_cap
import decider_ref

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        name='basic',
        inputs=[
            utilo.ResultFile('caption', 'result_result'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        name='style',
        inputs=[
            utilo.ResultFile('caption', 'result_result'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        name='missing',
        inputs=[
            utilo.ResultFile('caption', 'result_result'),
            utilo.ResultFile('codero', 'result_result', optional=True),
            utilo.ResultFile('tablero', 'result_result', optional=True),
            utilo.ResultFile(
                'rawmaker',
                'images_images',
                ext=None,
                optional=True,
            ),
        ],
        output=protoerror.ResultDefault,
    ),
]


def main():
    hook = protoerror.integrate(
        root=decider_ref.ROOT,
        features='decider_cap.features',
    )
    docinfo = protoerror.integrate_docinfo()
    utilo.featurepack(
        workplan=WORKPLAN,
        root=decider_ref.ROOT,
        featurepackage='decider_cap.features',
        config=utilo.FeaturePackConfig(
            cli_hook=[
                docinfo,
                hook,
            ],
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_cap.PROCESS,
            pages=True,
            version=decider_ref.__version__,
        ),
    )
