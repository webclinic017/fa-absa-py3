""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FTradeToOrder.py"
"""--------------------------------------------------------------------------
MODULE
    FTradeToOrder

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Module with utility functions for creating orders based on trades.
-----------------------------------------------------------------------------"""

import hashlib
import acm
import FDifferences
import FAssetManagementUtils
import FOrderUtils
from FLogger import FLogger
from FParameterSettings import ParameterSettingsCreator

SETTINGS = ParameterSettingsCreator.FromRootParameter('BSOMSSettings')

def Logger():
    LEVELS = {'info': 1, 'debug': 2, 'error': 3}
    logLevel = SETTINGS.Log()
    level = logLevel.lower() if logLevel else 'info'
    LOGGER = FLogger.GetLogger(name='BSOMS')
    LOGGER.Reinitialize(
        level=LEVELS.get(level),
        logToConsole=1)
    return LOGGER

LOGGER = Logger()

#----------------------------------------------------------------------------
#                  Create Orders from Trades utils
#----------------------------------------------------------------------------

def OrderProcessTypeInfoFromTrade(trade):
    if trade.IsFxSpot():
        info = FOrderUtils.CreateOrderProcessTypeInfo(acm.FFxSpotOrderProcessType(), trade.ValueDay())
    elif trade.IsFxForward():
        info = FOrderUtils.CreateOrderProcessTypeInfo(acm.FFxForwardOrderProcessType(), trade.ValueDay())
    elif trade.IsFxSwapNearLeg():
        info = FOrderUtils.CreateOrderProcessTypeInfo(acm.FFxSwapOrderProcessType(), trade.ValueDay(), 'Near')
    elif trade.IsFxSwapFarLeg():
        info = FOrderUtils.CreateOrderProcessTypeInfo(acm.FFxSwapOrderProcessType(), trade.ValueDay(), 'Far')
    return info

def LinkFxSwapOrder(nearOrder, farOrder):
    virtualOrderHandler = acm.Trading.CreateFxSwapOrder(FOrderUtils.TradingSession(), nearOrder.MarketPlace())
    virtualOrderHandler.AddOrder(nearOrder)
    virtualOrderHandler.AddOrder(farOrder)
    return virtualOrderHandler

def CreateSalesOrderFromTrade(trade, internalMarket=None):
    order = FOrderUtils.CreateSalesOrder(trade.Instrument(), trade.Currency(), internalMarket)
    order.Quantity(abs(trade.Quantity()))
    if trade.Price() > 0:
        order.Price(trade.Price())
    else:
        order.PriceCondition('Unlimited')
    order.BuyOrSell(trade.BoughtAsString())
    if trade.Instrument().InsType() == 'Curr':
        order.OrderProcessTypeInfo(OrderProcessTypeInfoFromTrade(trade))
    return order

def CallOrderCreationHook(order, trade):
    functionPath = SETTINGS.OrderHook()
    FAssetManagementUtils.CallFunction(functionPath, order, trade)

def CreateOrderWithPositionReferenceFromTrade(trade, market, salesState=None):
    order = CreateSalesOrderFromTrade(trade, market)
    SetPositionReferenceFromTrade(order, trade)
    CallOrderCreationHook(order, trade)
    FOrderUtils.SetSalesState(order, salesState)
    return order

def CreateOrderProgramFromTrades(trades, name, salesState=None):
    market = FOrderUtils.GetPrimaryMarket()
    orderProgram = FOrderUtils.CreateOrderProgram(name, market)
    for trade in trades:
        if trade.IsFxSwap():
            if trade.IsFxSwapFarLeg():
                nearOrder = CreateOrderWithPositionReferenceFromTrade(trade.ConnectedTrade(), market, salesState)
                farOrder = CreateOrderWithPositionReferenceFromTrade(trade, market, salesState)
                #virtualOrderHandler = LinkFxSwapOrder(nearOrder, farOrder)
                orderProgram.AddSalesOrder(nearOrder)
                orderProgram.AddSalesOrder(farOrder)
        else:
            order = CreateOrderWithPositionReferenceFromTrade(trade, market, salesState)
            orderProgram.AddSalesOrder(order)
    return orderProgram

#----------------------------------------------------------------------------
#                        Position Attributes on order
#----------------------------------------------------------------------------

def SetPositionReference(order, reference):
    try:
        order.SetExtendedData('Position Reference', reference)
    except AttributeError:
        raise Exception('Extended data with label "Position Reference" not found. '
                            'Reserved FreeTextField "Position Reference" must be activated on Internal Market')

def SetPositionReferenceFromTrade(order, trade):
    reference = CustomArchive(trade).Oid()
    SetPositionReference(order, reference)
    
def FilterOutPropeties(attributes):
    attributesToInclude = list(SETTINGS.AttributesToInclude())
    return {k:v for k, v in attributes.iteritems() if k in attributesToInclude}

def CustomArchiveName(archive):
    h = hashlib.md5()
    h.update(str(archive.Text()))
    return h.hexdigest()

def GetCustomArchive(name):
    try:
        return acm.FCustomArchive.Select('name="{0}" and subType="OMS" and user="0"'.format(name))[0]
    except IndexError:
        return None

def GetOrCreateCustomArchive(attributes):
    archive = acm.FCustomArchive()
    archive.ToArchive('attributes', attributes)
    archive.SubType('OMS')
    name = CustomArchiveName(archive)
    existingArchive = GetCustomArchive(name)
    if existingArchive:
        return existingArchive
    else:
        archive.Name(name)
        archive.AutoUser(False)
        archive.Commit()
        return archive

def CustomArchive(trade):
    attributes = FDifferences.Attributes(trade)
    attributes.update(FDifferences.AdditionalInfoAttributes(trade))
    attributes = FilterOutPropeties(attributes)
    return GetOrCreateCustomArchive(attributes)

def PositionAttributes(order):
    oid = order.ExtendedData().Position_Reference()
    attributes = acm.FCustomArchive[oid].FromArchive('attributes')
    return attributes

def Portfolio(order):
    try:
        return PositionAttributes(order).At('Portfolio')
    except Exception:
        return None
