#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

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
            utila.ResultFile('words', 'word_result'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'table',
        [
            utila.ResultFile('detector', 'bibliography_detected'),
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
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_ref.ROOT,
        featurepackage='decider_bib.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_bib.PROCESS,
            version=decider_ref.__version__,
        ),
    )
