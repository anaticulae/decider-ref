#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import protocol
import utila

import decider_bib
import decider_ref

DESCRIPTION = ''

USER = 'user'
DEVELOPER = 'developer'

WORKPLAN = [
    utila.create_step(
        'label',
        [
            utila.ResultFile('detector', 'bibliography_detected'),
            utila.ResultFile('docref', 'bibliography_parsed'),
            utila.ResultFile('words', 'headlines_headlines'),
            utila.ResultFile('words', 'sentences_sentences'),
            utila.ResultFile('sections', 'section_result'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'table',
        [
            utila.ResultFile('detector', 'bibliography_detected'),
            utila.ResultFile('detector', 'titlepage_detected'),
            utila.File('pdfinfo'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        name='plot',
        inputs=[
            utila.ResultFile('detector', 'bibliography_detected'),
        ],
        output=[
            ('year_histogram', 'png'),
        ],
    ),
]


def main():
    hook = protocol.integrate(
        root=decider_ref.ROOT,
        features='decider_bib.features',
    )
    docinfo = protocol.integrate_docinfo()
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_ref.ROOT,
        featurepackage='decider_bib.features',
        config=utila.FeaturePackConfig(
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
