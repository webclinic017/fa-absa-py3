""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExampleInstrumentPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExampleInstrumentPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
-------------------------------------------------------------------------------------------------------"""


import acm
from FPanel import Panel
from FEvent import EventCallback, OnInstrumentsSelected


class ExampleInstrumentPanel(Panel):

    def __init__(self):
        super(ExampleInstrumentPanel, self).__init__()
        self._insCtrl = None

    def OnInsSelected(self, *args):
        insId = self._insCtrl.GetData()
        event = OnInstrumentsSelected(self, insId)
        self.SendEvent(event)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.AddPopuplist('ins', 'Instrument', 40, 40)
        b.EndBox()
        return b

    def InitControls(self, layout):
        self._insCtrl = layout.GetControl('ins')
        self._insCtrl.Populate(acm.FStock.Select(None))
        self._insCtrl.AddCallback('Changed', self.OnInsSelected, None)
