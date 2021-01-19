#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila


# TODO: MOVE TO PROTOCOL
def select(items, selected=None):
    if isinstance(selected, int):
        selected = [selected]
    content = [item.content for item in items]
    flatten = utila.flatten(content)
    ids = [item.msgid for item in flatten]
    if selected:
        ids = [item for item in ids if item in selected]
    return ids
