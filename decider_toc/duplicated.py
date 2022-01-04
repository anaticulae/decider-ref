# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
>>> inside('Einleitung', 'EINLEITUNG UND PROBLEMSTELLUNG')
True

Regression tests:
=================

do not fail on special regex character `)`
>>> inside('Kupfer I)', 'EINLEITUNG')
False
"""
import collections
import re

import configo
import german
import iamraw
import knlp
import konrad

import decider_toc.utils


def validate(toc: iamraw.Toc) -> decider_toc.utils.InvalidTocItems:
    flatten = decider_toc.utils.flat(toc)
    lines = []
    for item in flatten:
        words = german.split_words(item.title, validate_sentences=False)
        words = konrad.remove_marks(words)
        lines.append(words)
    result = []
    duplication = duplicates(lines)
    for invalid in duplication:
        finding = [
            index for index, line in enumerate(flatten)
            if inside(invalid[0], line.title)
        ]
        if not finding:
            continue
        result.append((invalid, finding))
    return result


INSIDE = r"""
    (^|\W)
    %s
    (\W|$)
"""


def inside(item, container) -> bool:
    """\
    >>> inside('lebens', 'Heutige Lebens- und Arbeitswelt')
    True
    >>> inside('EMS', 'EINLEITUNG UND PROBLEMSTELLUNG')
    False
    >>> inside('PROBLEMSTELLUNG', 'EINLEITUNG UND PROBLEMSTELLUNG')
    True
    """
    item = re.escape(item)
    searched = re.search(
        INSIDE % item,
        container,
        flags=re.VERBOSE | re.IGNORECASE,
    )
    if searched is not None:
        return True
    return False


DUPLICATES_COUNT_MIN = configo.HolyTable(items=(
    (0, 5),
    (20, 5),
    (40, 10),
))


def duplicates(lines):
    duplicated_count_min = DUPLICATES_COUNT_MIN(len(lines))
    counter = collections.Counter()
    for line in lines:
        for index in range(len(line)):
            for words in range(index + 1, len(line) + 1):
                tokens = line[index:words]
                if len(tokens) == 1 and tokens[0].lower() in knlp.STOPWORDS:
                    # lower: handle UND correctly
                    continue
                sub = ' '.join(tokens)
                counter[sub] += 1
    most_common = counter.most_common(n=100)
    result = [item for item in most_common if item[1] >= duplicated_count_min]
    result = remove_duplicates(result)
    # filter again, if after merging a subgroup is not completly covered
    # by parent group.
    result = [item for item in result if item[1] >= duplicated_count_min]
    return result


def remove_duplicates(items):
    """Remove items which are part of a bigger parent/father item.

    >>> remove_duplicates([('Industrie', 6), ('Industrie 4.0', 6), ('4.0', 6)])
    [('Industrie 4.0', 6)]
    >>> remove_duplicates([('Industrie', 8), ('Industrie 4.0', 6), ('4.0', 6)])
    [('Industrie 4.0', 6), ('Industrie', 2)]
    """
    if not items:
        return []
    # longest items first
    todo = sorted(items, key=lambda x: x[0], reverse=True)
    result, todo = [todo[0]], todo[1:]
    for current in todo:
        candiate, count = current
        for item in result:
            if count > 0 and candiate in item[0]:
                if count <= item[1]:
                    count -= item[1]
                    # father can completely cover children
                    break
                # father is not huge enough, other fathers are
                # required to cover children completely
                count -= item[1]
        else:
            if count > 0:
                # some words are left, no all can be covered in fathers,
                # children becomes a father itself
                result.append((candiate, count))
    return result
