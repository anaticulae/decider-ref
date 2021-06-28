# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import protocol
import pytest
import serializeraw
import utilatest

import decider_toc.features
import decider_toc.features.complexity as dtfc
import decider_toc.features.rules as dtfr
import decider_toc.level
import tests

TECHNICAL24_INVALID_CHILDREN = 1
TECHNICAL24_INVALID_CHILDREN_TO_LONG = 1
TECHNICAL24_TOO_DEEP = 14


@utilatest.requires(power.TECH024_PDF)
def test_toc_invalid_children(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(decider_toc.level, 'MAX_TOC_DEEPNESS', 2)
        failures = lint(power.link(power.TECH024_PDF), dtfr)
    failures = len(failures)
    assert failures == TECHNICAL24_INVALID_CHILDREN, str(failures)


@pytest.mark.xfail(reason='result finding unique reduces 15 to 9')
@utilatest.requires(power.TECH024_PDF)
def test_toc_to_deep(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(decider_toc.level, 'MAX_TOC_DEEPNESS', 2)
        failures = lint(power.link(power.TECH024_PDF), dtfc)
    failures = len([item for item in failures if item in (1351, 1382)])
    expected = sum([
        TECHNICAL24_INVALID_CHILDREN_TO_LONG,
        TECHNICAL24_TOO_DEEP,
    ])
    assert failures == expected, str(failures)


def master78_too_few_children(invalid):
    assert invalid[0].title == 'Grundsätzliche Anforderungen'
    assert invalid[1].title == 'Anbindung der Bussysteme'
    assert invalid[2].title == 'Auswahl passender Busgeräte'


@pytest.mark.parametrize('source, invalids, validate', [
    pytest.param(
        power.link(power.TECH024_PDF),
        TECHNICAL24_INVALID_CHILDREN,
        None,
        id='technical24',
    ),
    pytest.param(
        power.link(power.MASTER078_PDF),
        3,
        master78_too_few_children,
        id='master78',
    ),
    pytest.param(
        power.link(power.MASTER072_PDF),
        0,
        None,
        id='master72',
    ),
])
@utilatest.requires(power.TECH024_PDF)
@utilatest.requires(power.MASTER072_PDF)
@utilatest.requires(power.MASTER078_PDF)
def test_toc_too_few_children(source, invalids, validate):
    toc = tests.toc.tableofcontent(source)
    validated = decider_toc.level.validate_children(toc)
    assert len(validated) == invalids, str(len(validated))
    if not validate:
        return
    validate(validated)


# yapf:disable
@pytest.mark.parametrize('source, too_deep', [
    pytest.param(power.link(power.TECH024_PDF), TECHNICAL24_TOO_DEEP, id='technical24'),
    pytest.param(power.link(power.MASTER072_PDF), 6, id='master72'),
])
# yapf:enable
@utilatest.requires(power.TECH024_PDF)
@utilatest.requires(power.MASTER072_PDF)
def test_toc_validate_deepness(source, too_deep):
    toc = tests.toc.tableofcontent(source)
    maxdeep = 2
    validated = decider_toc.level.validate_deepness(toc, maxdeep=maxdeep)
    # `too_deep` items with 1.2.3
    assert len(validated) == too_deep


def lint(path: str, module):
    driver = decider_toc.features.create_driver(toc=path)
    location = iamraw.Location.from_page(1)
    dumped = protocol.run(
        module.__name__,
        driver=driver,
        location=location,
    )
    result = serializeraw.load_findings(dumped[0]) + serializeraw.load_findings(
        dumped[1])
    failures = sorted(item.msgid for item in result)
    return failures
