""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FSearchPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FSearchPanel

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Panel that dispatches a search event when activated
-------------------------------------------------------------------------------------------------------"""

import acm
import FIntegratedWorkbenchUtils
from FPanel import Panel

class SearchPanel(Panel):

    def __init__(self):
        Panel.__init__(self)
        self._searchBox = None
        self._outgoingEvents = []
        if self.Settings().OutgoingEvents():
            self._outgoingEvents = FIntegratedWorkbenchUtils.GetAttributesInModule(
                self.Settings().OutgoingEvents())
    
    def InitSubscriptions(self):
        Panel.InitSubscriptions(self)
        self._searchBox.AddCallback('Activate', self._SearchActivated, None)   
       
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None', '')
        b.  AddInput('searchBox', 'Search')
        b.EndBox()
        return b
    
    def InitControls(self, layout):
        self._searchBox = layout.GetControl('searchBox')
    
    def _SearchActivated(self, cd=None, data=None):
        text = str(self._searchBox.GetData())
        if text:
            for outgoingEvent in self._outgoingEvents:
                event = outgoingEvent(self, text)
                self.SendEvent(event)