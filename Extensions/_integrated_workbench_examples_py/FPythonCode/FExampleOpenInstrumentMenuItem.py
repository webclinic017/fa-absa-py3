""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/IntegratedWorkbenchExamples/etc/FExampleOpenInstrumentMenuItem.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExampleOpenInstrumentMenuItem

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Implements an IntegratedWorkbenchMenuItem only applicable for ExampleView2 using a custom handler
-------------------------------------------------------------------------------------------------------"""

from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
import acm

class ExampleOpenInstrumentMenuItem(IntegratedWorkbenchMenuItem):

    def __init__(self, extObj):
        super(ExampleOpenInstrumentMenuItem, self).__init__(extObj,
                                                            view='ExampleView2')
        self.handler = self._Handler('ExampleInstrumentHandler')

    def GetLastSelectedInstrument(self):
        return self._Handler('ExampleInstrumentHandler').LastInstrumentSelected()

    def Invoke(self, eii):
        acm.StartApplication('Instrument Definition', self.GetLastSelectedInstrument())

    def EnabledFunction(self):
        return bool(self.GetLastSelectedInstrument())

def CreateExampleOpenInstrumentMenuItem(eii):
    return ExampleOpenInstrumentMenuItem(eii)
