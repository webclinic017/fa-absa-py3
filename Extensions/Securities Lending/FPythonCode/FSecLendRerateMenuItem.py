""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendRerateMenuItem.py"

"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendRerateMenuItem

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
     Menu Item for Rerate functionality making use of FSecLendDealUtils.

------------------------------------------------------------------------------------------------"""

from FIntegratedWorkbenchMenuItem import IntegratedWorkbenchMenuItem
import acm
from FEvent import EventCallback, CreateEvent, BaseEvent
from FWorkbenchObserver import WorkbenchObserver
from FSecLendEvents import OnRerateButtonClicked
from FIntegratedWorkbench import GetHandler
from FSecLendInventoryPositionHandler import SecLendInventoryPositionHandler

class RerateMenuItem(IntegratedWorkbenchMenuItem):

    def __init__(self, eii):
        super(self.__class__, self).__init__(eii, None)
        self._frame = eii
        self._observer = None
        self._isVisible = False
      
    def Invoke(self, eii):
        selection = self._frame.ActiveSheet().Selection()
        self.SendEvent(OnRerateButtonClicked(self, selection.SelectedRowObjects()))
        

    def Dispatcher(self):
        return self.View().Dispatcher()
        
    def Enabled(self):
        if self._observer is None:
            self._observer = WorkbenchObserver(self.Dispatcher(), self)
        return self.View() and self.View().Name() in ("SecLendPortfolioView", "SecLendClientView", "SecLendInventoryView")
        
    def SendEvent(self, event):
        self._observer.SendEvent(event)
        
    def Checked(self):
        try:
            return self._frame.IsDockWindowVisible('SecLendReratePanel')
        except:
            return False
            
    
def Rerate(eii):
    return RerateMenuItem(eii)


