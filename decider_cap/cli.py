# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_cap
import decider_ref

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        name='basic',
        inputs=[
            utila.ResultFile('caption', 'result_result'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        name='style',
        inputs=[
            utila.ResultFile('caption', 'result_result'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        name='missing',
        inputs=[
            utila.ResultFile('caption', 'result_result'),
            utila.ResultFile('codero', 'result_result', optional=True),
            utila.ResultFile('tablero', 'result_result', optional=True),
            utila.ResultFile(
                'rawmaker',
                'images_images',
                ext=None,
                optional=True,
            ),
        ],
        output=protocol.ResultDefault,
    ),
]


def main():
    hook = protocol.integrate(
        root=decider_ref.ROOT,
        features='decider_cap.features',
    )
    docinfo = protocol.integrate_docinfo()
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_ref.ROOT,
        featurepackage='decider_cap.features',
        config=utila.FeaturePackConfig(
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
