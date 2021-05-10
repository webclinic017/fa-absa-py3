""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSLimitMethods.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSLimitMethods

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

PARAGRAPH_SYMBOL = chr(0xa7)

def ParentOrSelf(limit):
    if limit.Parent() is not None:
        return limit.Parent()
    else:
        return limit

def UCITSParagraphName(limit):
    parentOrSelf = ParentOrSelf(limit)
    splitName = parentOrSelf.Name().split(PARAGRAPH_SYMBOL)
    try:
        return PARAGRAPH_SYMBOL + splitName[1]
    except Exception:
        pass
    return limit.Name()