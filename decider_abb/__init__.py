# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Analyzer
=====================

* verify order/sorted
* check obvious abbrevation and give advice to delete abbreviation

TODO: INFORM ABOUT NOT USED ABBREVIATION
TODO: VERIFY FIRST USAGE
"""

import configo

import decider_abb.path
import decider_ref

__version__ = decider_ref.__version__

ROOT = decider_ref.ROOT
PROCESS = 'decider_abbrev'

configo.cloud_lookup(PROCESS)
