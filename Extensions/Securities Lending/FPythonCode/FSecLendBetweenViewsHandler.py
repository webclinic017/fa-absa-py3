""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendBetweenViewsHandler.py"
"""--------------------------------------------------------------------------
MODULE
    FSecLendBetweenViewHandler

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Handlers between the views.

-----------------------------------------------------------------------------"""
import acm
from FHandler import Handler
from FEvent import EventCallback 
from FSecLendEvents import (OnClientViewCounterpartySelected, 
                            OnClientViewCounterpartyChangedFromOrderCapture,
                            OnInventoryViewInventoryChangedFromOrderCapture, 
                            OnInventoryViewInstrumentsSelected)


class SecLendBetweenOrderAndClientHandler(Handler):
    
    INSTANCES = []
    
    COUNTERPARTY = None
    
    def __init__(self, dispatcher):
        self.INSTANCES.append(self)
        super(SecLendBetweenOrderAndClientHandler, self).__init__(dispatcher)
        
    @EventCallback
    def OnOrderCaptureCounterpartyChanged(self, event):
        SecLendBetweenOrderAndClientHandler.COUNTERPARTY = event.Counterparty()
        for instance in self.INSTANCES:
            if event.Counterparty():
                instance.SendEvent(OnClientViewCounterpartyChangedFromOrderCapture(self, event.Counterparty()))
                instance.SendEvent(OnClientViewCounterpartySelected(self, event.Counterparty()))
    
    def HandleViewDestroyed(self, view):
        if view.ClassName() == 'TradeProgramView':
            self._ClearCandidateTrades()
        self.INSTANCES.remove(self)
        

class SecLendBetweenOrderAndInventoryHandler(Handler):
    
    INSTANCES = []
    
    INSTRUMENT = None
    
    def __init__(self, dispatcher):
        self.INSTANCES.append(self)
        super(SecLendBetweenOrderAndInventoryHandler, self).__init__(dispatcher)
        
    @EventCallback
    def OnOrderCaptureInstrumentChanged(self, event):
        SecLendBetweenOrderAndInventoryHandler.INSTRUMENT = event.Instrument()
        for instance in self.INSTANCES:
            if event.Instrument():
                instance.SendEvent(OnInventoryViewInventoryChangedFromOrderCapture(self, event.Instrument()))
                instance.SendEvent(OnInventoryViewInstrumentsSelected(self, event.Instrument()))
    
    def HandleViewDestroyed(self, view):
        if view.ClassName() == 'TradeProgramView':
            self._ClearCandidateTrades()
        self.INSTANCES.remove(self)