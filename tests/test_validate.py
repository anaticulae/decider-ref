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
import tests.toc

ARCHIVE = utila.join(decider_ref.ROOT, 'tests/expected', exist=True)


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR037_PDF, 'bachelor037', id='bachelor037'),
    pytest.param(power.BACHELOR067_PDF, 'bachelor067', id='bachelor067'),
    pytest.param(power.BACHELOR076_PDF, 'bachelor076', id='bachelor076'),
    pytest.param(power.BACHELOR090_PDF, 'bachelor090', id='bachelor090'),
    pytest.param(power.BACHELOR128_PDF, 'bachelor128', id='bachelor128'),
    pytest.param(power.DISS143_PDF, 'diss143', id='diss143'),
    pytest.param(power.MASTER072_PDF, 'master072', id='master072'),
    pytest.param(power.MASTER098_PDF, 'master098', id='master098'),
    pytest.param(power.MASTER116_PDF, 'master116', id='master116'),
])
@utilatest.nightly
def test_validate_huge(source, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=':',
        expected=expected,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
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

    def run_extraction(self, cmd, monkeypatch):  # pylint:disable=W0613,R0201
        tests.abbreviation.run(cmd, monkeypatch=monkeypatch)
        tests.bibliography.run(cmd, monkeypatch=monkeypatch)
        tests.caption.run(cmd, monkeypatch=monkeypatch)
        tests.toc.run(cmd, monkeypatch=monkeypatch)
