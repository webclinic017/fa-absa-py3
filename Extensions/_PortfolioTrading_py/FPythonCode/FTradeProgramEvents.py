""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FTradeProgramEvents.py"
"""-------------------------------------------------------------------------------------------------
MODULE
    FTradeProgramEvents

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Events for the Portfolio Trading view
-------------------------------------------------------------------------------------------------"""

from FEvent import BaseEvent, OnObjectsSelected


class TradeProgramEvent(BaseEvent):

    def __init__(self, sender, program):
        super(TradeProgramEvent, self).__init__(sender, program)

    def TradeProgram(self):
        return self._parameters

class OnOrdersCreatedFromCandidateTrades(BaseEvent):
    def __init__(self, sender):
        BaseEvent.__init__(self, sender, None)

class OnTradeProgramCleared(TradeProgramEvent):
    def __init__(self, sender):
        TradeProgramEvent.__init__(self, sender, None)

class OnConfirmTradeProgramSelected(TradeProgramEvent):
    def __init__(self, sender, program):
        TradeProgramEvent.__init__(self, sender, program)

class OnTradeProgramReset(TradeProgramEvent):
    def __init__(self, sender, program):
        TradeProgramEvent.__init__(self, sender, program)

class OnCreateOrders(TradeProgramEvent):
    def __init__(self, sender, program):
        super(OnCreateOrders, self).__init__(sender, program)

class OnSendOrdersToExecution(TradeProgramEvent):
    def __init__(self, sender, program):
        super(OnSendOrdersToExecution, self).__init__(sender, program)

class OnOrdersCreated(TradeProgramEvent):
    def __init__(self, sender, program):
        super(OnOrdersCreated, self).__init__(sender, program)



class OnSendOrders(BaseEvent):
    def __init__(self, sender, params):
        super(OnSendOrders, self).__init__(sender, params)

class OnDeleteOrders(BaseEvent):
    def __init__(self, sender, params):
        super(OnDeleteOrders, self).__init__(sender, params)


class OnLimitsChecked(BaseEvent):

    def __init__(self, sender, limitsResults):
        BaseEvent.__init__(self, sender, limitsResults)

    def LimitsResults(self):
        return self._parameters


class OnTradeProgramChanged(OnObjectsSelected):

    def __init__(self, sender, selection):
        OnObjectsSelected.__init__(self, sender, selection)

class OnActiveTradeProgramOrdersChanged(BaseEvent):

    def __init__(self, sender, tradeProgram, orders):
        super(OnActiveTradeProgramOrdersChanged, self).__init__(sender, tradeProgram)
        self._orders = orders

    def TradeProgram(self):
        return self._parameters

    def Orders(self):
        return self._orders

class OnIncludeCandidateChanged(BaseEvent):

    def __init__(self, sender, includeCandidate):
        BaseEvent.__init__(self, sender, includeCandidate)

    def IncludeCandidate(self):
        return self._parameters

class OnTradeProgramExport(BaseEvent):
    def __init__(self, sender, path):
        BaseEvent.__init__(self, sender, path)

    def Path(self):
        return self._parameters

class OnTradeProgramActionInvoked(BaseEvent):
    def __init__(self, sender, action):
        BaseEvent.__init__(self, sender, action)
        
    def Action(self):
        return self._parameters

class OnTradeProgramActionCleared(BaseEvent):
    pass

class OnMainSheetSelected(OnObjectsSelected):

    def __init__(self, sender, selection):
        OnObjectsSelected.__init__(self, sender, selection)
        self._selectionObject = selection

    def Selection(self):
        return self._selectionObject


class OnCandidateTradesCreated(BaseEvent):

    def __init__(self, sender, trades, action):
        self._trades = trades
        self._action = action
        super(OnCandidateTradesCreated, self).__init__(sender, (trades, action))

    def Trades(self):
        return self._trades
        
    def Action(self):
        return self._action

class OnPlaceholderTradesCreated(OnCandidateTradesCreated):
    pass
    
class OnCandidateTradesChanged(BaseEvent):

    def __init__(self, sender, candidateTrades):
        super(OnCandidateTradesChanged, self).__init__(sender, candidateTrades)

    def CandidateTrades(self):
        return self._parameters

class OnCandidateTradesCleared(BaseEvent):

    def __init__(self, sender):
        super(OnCandidateTradesCleared, self).__init__(sender, None)

    def CandidateTrades(self):
        return self._parameters
