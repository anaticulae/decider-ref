#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import re

import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(ROOT, 'README.md'), encoding='utf8') as fp:
    README = fp.read()

with open(os.path.join(ROOT, 'decider_ref/__init__.py'), encoding='utf8') as fp:
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(os.path.join(ROOT, "requirements.txt"), encoding='utf8') as fp:
    REQUIRES = [line for line in fp.readlines() if line and '#' not in line]

if __name__ == "__main__":
    # allow ssetup.py to run from another directory
    os.chdir(ROOT)
    setuptools.setup(
        author='Helmut Konrad Fahrendholz',
        author_email='info@checkitweg.de',
        description='checker',
        install_requires=REQUIRES,
        long_description=README,
        name='decider_ref',
        platforms='any',
        url='https://dev.package.checkitweg.de/reference',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
        packages=[
            'decider_abb',
            'decider_abb.features',
            'decider_bib',
            'decider_bib.features',
            'decider_cap',
            'decider_cap.features',
            'decider_ref',
            'decider_toc',
            'decider_toc.features',
        ],
        entry_points={
            'console_scripts': [
                'decider_abbreviation = decider_abb.cli:main',
                'decider_bibliography = decider_bib.cli:main',
                'decider_caption = decider_cap.cli:main',
                'decider_toc = decider_toc.cli:main',
            ],
        },
    )
