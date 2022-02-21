# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import utilatest

import decider_toc.features.basic
import tests.toc


@utilatest.requires(power.DOCU035_PDF, folder='notoc')
def test_toc_extraction_no_toc():
    expected_failures = [1300, 1301]
    source = power.link(power.DOCU035_PDF, folder='notoc')
    failures = tests.toc.lint(source, decider_toc.features.basic)
    assert failures == expected_failures, str(failures)


@utilatest.requires(power.BACHELOR067_PDF)
def test_toc_duplicated_level_bachelor067():
    """\
    1 Einführung
    1 Quellcode/Skripte(Auszüge)
    2 Vorstellung und Architektur übersicht von Spark
    2 Konfigurationen
    """
    source = power.link(power.BACHELOR067_PDF)
    linted = tests.toc.linter(
        source,
        decider_toc.features.basic,
        msgids=1310,
    )
    assert len(linted) in (5, 6)


def lint(path: str, module):
    toc = tests.toc.tableofcontent(path)
    linter = protocol.from_module(module.__name__)
    driver = protocol.driver(
        toc=toc,
        outlines=None,
    )
    linter.run(driver=driver)
    result = linter.result(unique=False)
    failures = sorted(item.msgid for item in result)
    return failures
