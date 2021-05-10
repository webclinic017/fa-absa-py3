""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FPublicBuySideOMSInterface.py"
"""--------------------------------------------------------------------------
MODULE
    FPublicBuySideOMSInterface

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    API to create orders programatically within Buy side OMS based on an instrument and a position.
    Example:
    
    instrument = acm.FInstrument['MyInstrument']
    positionDict = {'Portfolio':acm.FPhysicalPortfolio['MyPortfolio'],
                    'Acquirer':acm.FParty['MyFund'],
                    'OptKey1':'Strategy1'}

    order = GetOrder(instrument)
    order.Price(100)
    order.Quantity(1000)
    order.BuyOrSell('Buy')
    AddPositionReference(order, positionDict)
    FOrderUtils.SetSalesState(order, 'Inactive')
    orderProgram = CreateOrderProgram('New OP', [order])
    SendOrderProgram(orderProgram)
    
-----------------------------------------------------------------------------"""

import FOrderUtils
import FTradeToOrder

def GetOrder(instrument, currency=None):
    """ Takes an instrument and optionally a currency and returns a blank order on 
        the Internal market. If no currency is passed the instrument currency is used. """
    market = FOrderUtils.GetPrimaryMarket()
    FOrderUtils.Connect(market)
    currency = currency or instrument.Currency()
    order = FOrderUtils.CreateSalesOrder(instrument, currency, market)
    return order
    
def AddPositionReference(order, positionDict):
    """ Adds position details on the order that determines where the fills will be created.
        Takes a dicionary with trade attribute as keys and the related object as values. 
        Example: {'Portfolio', myPortfolio} """
    customArchive = FTradeToOrder.GetOrCreateCustomArchive(positionDict)
    FTradeToOrder.SetPositionReference(order, customArchive.Oid())

def CreateOrderProgram(name, orders=None):
    """ Creates an order program and adds the orders if possible. """
    market = FOrderUtils.GetPrimaryMarket()
    orderProgram = FOrderUtils.CreateOrderProgram(name, market)
    for order in orders or []:
        orderProgram.AddSalesOrder(order)
    return orderProgram
    
def SendOrderProgram(orderProgram, listener=None):
    """ Sends the order program and adds a listener that subscribes to the result of sending.
        The default listener will print whether it was successfully sent or not. """
    listener = listener or FOrderUtils.OrderProgramSenderListener(orderProgram)
    FOrderUtils.OrderProgramSender(orderProgram, listener).SendAsync()
