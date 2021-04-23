""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FCurrentActiveCandidateTrades.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FCurrentActiveCandidateTrades

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Handler that works as an interface between the events created by user actions in the 
    Portfolio Trading view and the CandidateTrades. The handler also distributes events to
    update the panels in the Portolio Trading view
-------------------------------------------------------------------------------------------------"""

from datetime import datetime

import acm
import FOrderUtils
from FPromise import AsynchronousCall
from FHandler import Handler
from FEvent import EventCallback, OnError, CreateEvent, BaseEvent
from FCandidateTrades import CandidateTrades, PlaceholderTrades
from FParameterSettings import ParameterSettingsCreator
from FIntegratedWorkbenchLogging import logger
from FTradeProgramEvents import(OnCandidateTradesChanged,
                                OnCandidateTradesCleared,
                                OnLimitsChecked,
                                )
try:
    from FTradeToOrder import CreateOrderProgramFromTrades
except ImportError:
    omsModuleInstalled = False
else:
    omsModuleInstalled = True

class CurrentActiveCandidateTrades(Handler):

    SETTINGS = ParameterSettingsCreator.FromRootParameter('TradeProgramSettings')

    def __init__(self, dispatcher):
        super(CurrentActiveCandidateTrades, self).__init__(dispatcher)
        self._candidateTradesIncluded = self.SETTINGS.IncludeCandidateTrades()
        self._candidateTrades = CandidateTrades(simulateTrades=self._candidateTradesIncluded)
        self._placeholderTrades = PlaceholderTrades(simulateTrades=self._candidateTradesIncluded)

    def CandidateTrades(self):
        return self._candidateTrades.Trades()
    
    def IncludeCandidateTrades(self):
        return self._candidateTradesIncluded

    @EventCallback
    def OnCandidateTradesCreated(self, event):
        self._candidateTrades.AddTrades(event.Action(), event.Trades())
        self.SendEvent(OnCandidateTradesChanged(self, self._candidateTrades))

    @EventCallback
    def OnPlaceholderTradesCreated(self, event):
        self._placeholderTrades.AddTrades(event.Action(), event.Trades())

    @EventCallback
    def OnIncludeCandidateChanged(self, _):
        self._candidateTradesIncluded = not self._candidateTradesIncluded
        self._candidateTrades.AlwaysSimulateTrades(self._candidateTradesIncluded)
        self.SendEvent(OnCandidateTradesChanged(self, self._candidateTrades))

    @EventCallback
    def OnTradeProgramActionInvoked(self, event):
        action = event.Action()
        self._candidateTrades.ClearAction(action)

    @EventCallback
    def OnTradeProgramActionCleared(self, _):
        self._ClearCandidateTrades()
      
    @EventCallback
    def OnOrdersCreatedFromCandidateTrades(self, _):
        try:
            assert omsModuleInstalled, 'Module "Buy Side OMS" is needed to create orders from candidate trades'
            name = acm.User().Name() + ' ' + datetime.now().strftime('%x %X')
            orderProgram = CreateOrderProgramFromTrades(self.CandidateTrades(), name, salesState='Inactive')
            FOrderUtils.OrderProgramSender(orderProgram, GetOrderProgramResultListener()(self)).SendAsync()
        except Exception as e:
            self.SendEvent(OnError(self, 'Information', e.message))

    def HandleViewDestroyed(self, view):
        if view.ClassName() == 'TradeProgramView':
            self._ClearCandidateTrades()

    def _ClearCandidateTrades(self):
        self._candidateTrades.ClearAll()
        self._placeholderTrades.ClearAll()
        self.SendEvent(OnCandidateTradesCleared(self))

def GetOrderProgramResultListener():
    if omsModuleInstalled:   
        class OrderProgramResultListener(FOrderUtils.OrderSenderListener):
        
            def __init__(self, handler):
                self._handler = handler
        
            def OnSuccess(self, orderProgram):
                self._handler._ClearCandidateTrades()
                event = CreateEvent('OnOrdersSuccessfullyCreated', BaseEvent, orderProgram)
                self._handler.SendEvent(event)
            
            @AsynchronousCall
            def HandleError(self, errorMessage):
                msg = 'Failed to send order: {0}'.format(errorMessage)
                self._handler.SendEvent(OnError(self._handler, 'Information', msg))
        return OrderProgramResultListener
    