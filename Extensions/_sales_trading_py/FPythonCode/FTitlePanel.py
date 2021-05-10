""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FTitlePanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FTitlePanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm

from FPanel import Panel
from FEvent import EventCallback

class TitlePanel(Panel):

    NAME = 'nameCtrl'

    def __init__(self):
        Panel.__init__(self)
        self._nameCtrl = None

    def InitControls(self, layout):
        self._nameCtrl = layout.GetControl(self.NAME)
        self._nameCtrl.SetFont('', 14, True, False)
        self._nameCtrl.SetData('')

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.  BeginHorzBox('None', '')
        b.AddLabel(self.NAME, '', 1000, -1)
        b.  EndBox()
        return b

    def Selected(self, event):
        obj = event.First() or ''
        self._nameCtrl.SetData(obj)

class BondTitlePanel(TitlePanel):

    def __init__(self):
        TitlePanel.__init__(self)

    @EventCallback
    def CTSBondsSelected(self, event):
        self.Selected(event)


class ClientTitlePanel(TitlePanel):

    def __init__(self):
        TitlePanel.__init__(self)

    @EventCallback
    def CTSClientNavigationChanged(self, event):
        self.Selected(event)


class MarketMakingTitlePanel(TitlePanel):

    def __init__(self):
        TitlePanel.__init__(self)

    @EventCallback
    def CTSMarketMakerQuoteSelected(self, event):
        self.Selected(event)
