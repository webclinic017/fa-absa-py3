""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FBookmarkEventAdapter.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FBookmarkEventAdapter

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------"""

import acm
import FCTSUtils
from FCTSEvents import OnBookmark
from FHandler import Handler

from FSalesTradingLogging import logger


class BookmarkEventAdapter(Handler):

    def __init__(self, dispatcher):
        super(BookmarkEventAdapter, self).__init__(dispatcher)
        self._selectRes = None
        self._preferencesListener = None
        self.InitiateListening()

    def InitiateListening(self):

        self._preferencesListener = self._PreferencesListener(self)
        try:
            self._selectRes = FCTSUtils.GetUserPreferences()
        except RuntimeError:
            logger.info('Unable to find preferences for user {0}. '
                        'Bookmarks will not work'.format(acm.UserName()))
        else:
            self._selectRes.AddDependent(self._preferencesListener)

    def HandleViewDestroyed(self, _view):
        if self._selectRes:
            self._selectRes.RemoveDependent(self._preferencesListener)
            self._selectRes = None

    class _PreferencesListener(object):
        def __init__(self, parent):
            self._parent = parent

        def ServerUpdate(self, send, asp, params=None):
            if send.IsModified():
                try:
                    logger.debug("BookmarkEventAdapter._PreferencesListener()."
                                 "ServerUpdate() send: %s asp: %s " % (send.Class(), asp))
                    self._parent.SendEvent(OnBookmark(self._parent))
                except Exception as exc:
                    logger.error("BookmarkEventAdapter._PreferencesListener Exception:")
                    logger.error(exc, exc_info=True)
