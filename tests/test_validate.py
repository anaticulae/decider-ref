# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import protoerror
import pytest
import utilo
import utilotest

import decider_ref
import tests.abbreviation
import tests.bibliography
import tests.caption
import tests.conftest
import tests.toc

ARCHIVE = utilo.join(decider_ref.ROOT, 'tests/expected', exist=True)
TODO = [
    source[0] if isinstance(source, tuple) else source
    for source in tests.conftest.RESOURCES
]
TODO = [pytest.param(source, id=utilo.file_name(source)) for source in TODO]


@utilotest.nightly
@pytest.mark.parametrize('source', TODO)
def test_validate_huge(source, td, mp):
    utilotest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=':',
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, pages, workdir, mp):
        super().__init__(
            program=functools.partial(
                self.run_extraction,
                mp=mp,
            ),
            step=None,
            pages=pages,
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
        )
        self.headlines = hoverpower.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        return protoerror.findings_from_path(path)

    def raw(self, value) -> str:
        findings = utilo.flatten_content(value)
        findings = [
            f'{str(item.msgid).zfill(5)} {str(item.location)} {item.solution.title}'
            for item in findings
        ]
        findings = sorted(findings, key=utilo.alphabetically)
        result = utilo.NEWLINE.join(findings)
        return result

    def run_extraction(self, cmd, mp):  # pylint:disable=W0613,R0201
        tests.abbreviation.run(cmd, mp=mp)
        tests.bibliography.run(cmd, mp=mp)
        tests.caption.run(cmd, mp=mp)
        tests.toc.run(cmd, mp=mp)
