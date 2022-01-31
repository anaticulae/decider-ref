# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import power
import protocol
import pytest
import utila
import utilatest

import decider_ref
import tests.abbreviation
import tests.bibliography
import tests.caption
import tests.toc

ARCHIVE = os.path.join(decider_ref.ROOT, 'tests/expected')
utila.exists_assert(ARCHIVE)


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR037_PDF, 'bachelor037', id='bachelor037'),
])
@utilatest.longrun
def test_validate_huge(source, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=':',
        expected=expected,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


def run_extraction(cmd, monkeypatch):  # pylint:disable=W0613
    tests.abbreviation.run(cmd, monkeypatch=monkeypatch)
    tests.bibliography.run(cmd, monkeypatch=monkeypatch)
    tests.caption.run(cmd, monkeypatch=monkeypatch)
    tests.toc.run(cmd, monkeypatch=monkeypatch)


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                run_extraction,
                monkeypatch=monkeypatch,
            ),
            step=None,
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.headlines = power.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        return protocol.findings_from_path(path)

    def raw(self, value) -> str:
        findings = utila.flatten_content(value)
        findings = [
            f'{str(item.msgid).zfill(5)} {item.location.raw().zfill(5)} {item.solution.title}'
            for item in findings
        ]
        findings = sorted(findings, key=utila.alphabetically)
        result = utila.NEWLINE.join(findings)
        return result
