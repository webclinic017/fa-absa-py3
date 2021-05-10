""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExampleCounterpartyPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExampleCounterpartyPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Implements a simple panel displaying the counterparty name of the currently selected trade
-------------------------------------------------------------------------------------------------------"""


import acm
from FPanel import Panel
from FEvent import EventCallback

class ExampleCounterpartyPanel(Panel):

    def __init__(self):
        super(ExampleCounterpartyPanel, self).__init__()
        self._nameControl = None

    @EventCallback
    def OnExampleTradesSelected(self, event):
        if event.Objects():
            counterparty = event.Objects().First().Trade().Counterparty()
            self._nameControl.SetData(counterparty or '')

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None', '')
        b.AddLabel('name', '', 1000, -1)
        b.EndBox()
        return b

    def InitControls(self, layout):
        self._nameControl = layout.GetControl('name')
        self._nameControl.SetFont('', 14, True, False)
        self._nameControl.SetData('')
