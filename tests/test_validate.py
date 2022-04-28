# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import protocol
import pytest
import utila
import utilatest

import decider_ref
import tests.abbreviation
import tests.bibliography
import tests.caption
import tests.conftest
import tests.toc

ARCHIVE = utila.join(decider_ref.ROOT, 'tests/expected', exist=True)
TODO = [
    source[0] if isinstance(source, tuple) else source
    for source in tests.conftest.RESOURCES
]
TODO = [pytest.param(source, id=utila.file_name(source)) for source in TODO]


@utilatest.nightly
@pytest.mark.parametrize('source', TODO)
def test_validate_huge(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=':',
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                self.run_extraction,
                monkeypatch=monkeypatch,
            ),
            step=None,
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
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

    def run_extraction(self, cmd, monkeypatch):  # pylint:disable=W0613,R0201
        tests.abbreviation.run(cmd, monkeypatch=monkeypatch)
        tests.bibliography.run(cmd, monkeypatch=monkeypatch)
        tests.caption.run(cmd, monkeypatch=monkeypatch)
        tests.toc.run(cmd, monkeypatch=monkeypatch)
