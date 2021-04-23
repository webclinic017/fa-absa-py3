""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FBookmarkMenuItem.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FBookmarkMenuItem

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm

from FBookmarks import FBookmarks
from FIntegratedWorkbenchUtils import IsKindOf
from FSalesTradingLogging import logger
from FParameterSettings import ParameterSettingsCreator
from FSalesTradingMenuItem import SalesTradingMenuItem

class BookmarkMenuItem(SalesTradingMenuItem):

    def __init__(self, extObj, view=None):
        super(BookmarkMenuItem, self).__init__(extObj, view=view)
        self._settings = ParameterSettingsCreator.FromRootParameter('ToggleBookmarkMenuItem')
        self.panels = [panel for panel in self._settings.Panels()]
        logger.debug("BookmarkMenuItem.__init__() Panels: %s Application: %s" % (self.panels, self._frame))

    def PanelObjectPair(self):
        for p in self.panels:
            dockWindow = self._frame.GetCustomDockWindow(p.Name())
            if dockWindow:
                custPanel = dockWindow.CustomLayoutPanel()
                obj = custPanel.SelectedObject()
                if IsKindOf(obj, acm.FObject):
                    return custPanel, obj
        return None, None

    def Checked(self):
        try:
            panel, obj = self.PanelObjectPair()
            if (panel != None) and (obj != None):
                return FBookmarks(panel.Settings().BookmarkKey()).IsIncluded(obj)
            else:
                return False
        except Exception as exc:
            logger.error("BookmarkMenuItem.Checked Exception:")
            logger.error(exc, exc_info=True)
            return False

    def Invoke(self, eii):
        try:
            panel, obj = self.PanelObjectPair()
            if (panel != None) and (obj != None):
                FBookmarks(panel.Settings().BookmarkKey()).Toggle(obj)
            else:
                logger.error("BookmarkMenuItem.Invoke() Unable to bookmark, no object selected")
        except Exception as exc:
            logger.error("BookmarkMenuItem.Invoke Exception:")
            logger.error(exc, exc_info=True)
