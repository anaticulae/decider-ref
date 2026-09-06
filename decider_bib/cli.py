#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import protoerror
import utilo

import decider_bib
import decider_ref

DESCRIPTION = ''

USER = 'user'
DEVELOPER = 'developer'

WORKPLAN = [
    utilo.create_step(
        'label',
        [
            utilo.ResultFile('detector', 'bibliography_detected'),
            utilo.ResultFile('docref', 'bibliography_parsed'),
            utilo.ResultFile('words', 'headlines_headlines'),
            utilo.ResultFile('words', 'sentences_sentences'),
            utilo.ResultFile('sections', 'section_result'),
        ],
        (USER, DEVELOPER),
    ),
    utilo.create_step(
        'table',
        [
            utilo.ResultFile('detector', 'bibliography_detected'),
            utilo.ResultFile('detector', 'titlepage_detected'),
            utilo.File('pdflog'),
        ],
        (USER, DEVELOPER),
    ),
    utilo.create_step(
        name='plot',
        inputs=[
            utilo.ResultFile('detector', 'bibliography_detected'),
        ],
        output=[
            ('year_histogram', 'png'),
        ],
    ),
]


def main():
    hook = protoerror.integrate(
        root=decider_ref.ROOT,
        features='decider_bib.features',
    )
    docinfo = protoerror.integrate_docinfo()
    utilo.featurepack(
        workplan=WORKPLAN,
        root=decider_ref.ROOT,
        featurepackage='decider_bib.features',
        config=utilo.FeaturePackConfig(
            cli_hook=[
                docinfo,
                hook,
            ],
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_bib.PROCESS,
            pages=True,
            version=decider_ref.__version__,
        ),
    )
