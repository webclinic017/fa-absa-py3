""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSBookmarks.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSBookmarks

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from FBookmarkMenuItem import BookmarkMenuItem
from FSalesTradingLogging import logger

class _BondBookmarkMenuItem(BookmarkMenuItem):

    def __init__(self, extObj):
        BookmarkMenuItem.__init__(self, extObj)
        logger.debug("_BondBookmarkMenuItem.__init__()" )

    def EnabledFunction(self):
        if self.View().Name() in ['BondView', 'MarketMakerView']:
            return True


class _ClientBookmarkMenuItem(BookmarkMenuItem):

    def __init__(self, extObj):
        BookmarkMenuItem.__init__(self, extObj, view='ClientView')
        logger.debug("_ClientBookmarkMenuItem.__init__()" )


def CreateBondBookmarkMenuItem(eii):
    try:
        logger.debug("CreateBondBookmarkMenuItem()" )
        return _BondBookmarkMenuItem(eii)
    except Exception as stderr:
        logger.error("CreateBondBookmarkMenuItem() Exception:" )
        logger.error(stderr, exc_info=True)

def CreateClientBookmarkMenuItem(eii):
    try:
        logger.debug("CreateClientBookmarkMenuItem()" )
        return _ClientBookmarkMenuItem(eii)
    except Exception as stderr:
        logger.error("CreateClientBookmarkMenuItem() Exception:" )
        logger.error(stderr, exc_info=True)
