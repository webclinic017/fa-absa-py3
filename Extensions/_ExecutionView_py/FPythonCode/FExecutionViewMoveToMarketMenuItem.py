""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ExecutionView/etc/FExecutionViewMoveToMarketMenuItem.py"
"""--------------------------------------------------------------------------
MODULE
    FExectionViewMoveToMarketMenuItem

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Functionality for creating buttons for quickly moving sales orders to
    an external market. To use this functionality, it is necessary to:
    
    1) Create an FMenuExtension:

        FUiTrdMgrFrame:MyMoveButton =
          CreateFunction=MyMoveButton.CreateMenuItem
          DisplayName=Move To My Market
          MenuType=Application
          ParentMenu=
      
    2) Create an FPythonCode file MyMoveButton with a function CreateMenuItem.
       This function should create a MoveToMarketMenuItem object with the name
       of the market you wish the button to be connected to as an input.
    
        FObject:MyMoveButton

        from FExecutionViewMoveToMarketMenuItem import MoveToMarketMenuItem

        def CreateMenuItem(frame):
            return MoveToMarketMenuItem(frame, "Market Place Name")
            
    3) From the order sheet, the menu button can be added and customized with a location, icon, tool-tip 
       etc. by using the "Ribbon Designer"

-----------------------------------------------------------------------------"""


import acm
import FOrderUtils
from FExecutionViewMenuItem import ExecutionViewMenuItem
from FExecutionViewUtils import logger

class MoveToMarketMenuItem(ExecutionViewMenuItem):

    OWN = "Own"

    def __init__(self, eii, marketName):
        super(self.__class__, self).__init__(eii)
        self._market = acm.FMarketPlace[marketName]
        if not self._market:
            logger.error('Could not find any market %s'%str(marketName))
        
    def Enabled(self):
        if self._market:
            orderHandlers = self.SelectedSalesOrderHandlers()
            if orderHandlers:
                return not (False in [self.OrderEnabledForMarket(orderHandler) for orderHandler in orderHandlers])
        return False

    def OrderEnabledForMarket(self, orderHandler):
        try:
            tradingInterface = FOrderUtils.ExistingTradingInterface(orderHandler.Instrument(), self._market, orderHandler.TradingInterface().Currency())
            return self._market.IsConnected() and bool(tradingInterface)
        except AttributeError as e:
            return False

        
    def InvokeAsynch(self, eii):
        if self.ValidateOrderStates(self._SelectedSalesOrders()):
            self.MoveOrdersToMarket()
        
    def MoveOrdersToMarket(self):
        for orderHandler in self.SelectedSalesOrderHandlers():
            self.MoveOrderToMarket(orderHandler)
            
    def MoveOrderToMarket(self, orderHandler):
        moveOrderHandler = self.CreateMoveOrder(orderHandler)
        self.InitializeMoveOrder(orderHandler, moveOrderHandler)
        FOrderUtils.OrderSender(moveOrderHandler).SendOrder()
       
    def CreateMoveOrder(self, orderHandler):
        return FOrderUtils.CreateMoveOrder(orderHandler, self._market)
        
    def InitializeMoveOrder(self, originalOrderHandler, moveOrderHandler):
        """ This is where we specify the move order from the sales order. Override this method in subclass to change behaviour """
        moveOrderHandler.Quantity = originalOrderHandler.Balance()
        moveOrderHandler.Price = originalOrderHandler.Price()
        moveOrderHandler.MarketAccount = self.MarketAccount()
    
    def MarketAccount(self):    
        return self.OWN


def MoveToFIXMarketMenuItem(frame):
    return MoveToMarketMenuItem(frame, "FIX")
