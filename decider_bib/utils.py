# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import re

import german
import konrad
import utila

LABEL = r'\[\d+\]'


def format_bibline(item) -> str:
    if item.reference and not re.match(LABEL, str(item.reference)):
        # convert to string to avoid failing when reference is parsed as
        # int or something. Later, this will not be a problem, cause we
        # have only valid parsings.
        return str(item.reference)
    title = utila.shrink(item.title, maxlength=20)
    return f' * {item.author} {item.year} {title}'


# TODO: REMOVE LATER
def sentences(texts, numbers: bool = False):
    number, current = 0, None
    for chunk in texts:
        for section in chunk.content:
            for page, sentence in zip(section.pages, section.content):
                if not numbers:
                    yield page, sentence
                else:
                    if current != page:
                        number = 0
                        current = page
                    else:
                        number += 1
                    yield page, number, sentence


def sentence_lookup(text) -> dict:
    lookup = collections.defaultdict(list)
    for page, sentence in sentences(text):
        lookup[page].append(sentence)
    return dict(lookup)


def sentence_plain(sentence, marks) -> list:
    result = []
    splitted = german.word_tokenize(sentence, validate_sentences=False)
    for start, end in marks:
        selected = [splitted[item] for item in utila.rtuple(start, end)]
        selected = selection_plain(selected)
        result.append(selected)
    return result


def selection_plain(items: list) -> str:
    items = [konrad.mark2str(item) for item in items]
    raw = ' '.join(items)
    raw = raw.replace('( ', '(')
    raw = raw.replace('[ ', '[')
    raw = raw.replace(' )', ')')
    raw = raw.replace(' ]', ']')
    raw = raw.replace(' ,', ',')
    raw = raw.replace(' ; ', '; ')
    raw = raw.replace(' - ', '-')
    raw = raw.replace(' : ', ': ')
    return raw
