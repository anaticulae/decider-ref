# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import iamraw
import protoerror
import utilo

import decider_abb.features.table
import tests.abbreviation


def test_abbrev_sorted_bachelor37(td, mp):
    # TODO: ADJUST TABLE PAGE LOADER
    linted = tests.abbreviation.run_table(
        hoverpower.BACHELOR037_PDF,
        mp,
        td,
        msgid=15010,
    )
    assert len(linted) == 1


def test_abbrev_table_sorted():
    table = iamraw.AbbreviationResult()
    for item in ['Alpha', 'Beta', 'Gamma', 'helm']:
        table.append(iamraw.Abbreviation(item))
    driver = protoerror.driver(abbrevtable=table)

    linter = protoerror.Linter()
    decider_abb.features.table.check_15010_not_sorted_alphabetically(
        linter.add_finding,
        driver,
    )
    assert linter.findings == []


def abbreviation_linter(method):
    linter = protoerror.from_module(decider_abb.features.table)
    location = iamraw.Location.from_page(5)
    msgid = vars(method)['msgid']
    call = functools.partial(
        linter.add_finding,
        msgid=msgid,
        location=location,
    )
    linter.add_finding = call
    return linter


EXAMPLE = [
    ('Beta', 'Dies ist ein Parmeter'),
    ('Alpha', 'Dies ist noch ein Parmeter'),
    ('helm', 'H * l * m * n'),
    ('Gamma', 'require more'),
]


def test_abbrev_table_unsorted():
    table = iamraw.AbbreviationResult()
    for short, description in EXAMPLE:
        table.append(iamraw.Abbreviation(
            short=short,
            description=description,
        ))
    driver = protoerror.driver(abbrevtable=table)

    linter = abbreviation_linter(
        decider_abb.features.table.check_15010_not_sorted_alphabetically)
    decider_abb.features.table.check_15010_not_sorted_alphabetically(
        linter.add_finding,
        driver,
    )
    assert len(linter.findings) == 1, str(linter.findings)

    description = linter.findings[0].solution.description
    assert utilo.istemplate_replaced(description), description
