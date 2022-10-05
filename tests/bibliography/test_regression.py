# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila
import utilatest

import tests.bibliography


@utilatest.requires(power.MASTER049_PDF)
def test_empty_bib(td, mp):
    """Run decider with empty bib.

    Before this patch, loading data creates invalid data structure which
    produces an runtime error.
    """
    source = power.link(power.MASTER049_PDF)
    utila.copy_content(
        source,
        td.tmpdir,
        unlock=True,
    )
    empty = iamraw.BibliographyTable()
    dumped = serializeraw.dump_bibliography_reference(empty)
    utila.file_replace(
        td.tmpdir.join('bibliography__result_result.yaml'),
        content=dumped,
    )
    cmd = f'-i {td.tmpdir} -o {td.tmpdir}'
    tests.bibliography.run(cmd, mp=mp)
