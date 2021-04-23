""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FTnpUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FTnpUtils

    (c) Copyright 2016 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Module with utility functions for getting information from TNP messages
    and accessing data from TAB
-----------------------------------------------------------------------------"""

import acm

class TnpDependecies(object):
    """ Used for Dependency Injection to access TNPConst, logger and caches in TAB 
        which also allows for unit testing without running TAB """ 
   
    TNP_CONST = None
    LOG = None
    ORDER_CACHE = None
    ORDER_BOOK_CACHE = None
    ORDER_PROGRAM_CACHE = None
    DEAL_CACHE = None
    
    @classmethod
    def Initialize(cls, tnpConst, log, orderCache, orderBookCache, orderProgramCache, dealCache):
        cls.TNP_CONST = tnpConst
        cls.LOG = log
        cls.ORDER_CACHE = orderCache
        cls.ORDER_BOOK_CACHE = orderBookCache
        cls.ORDER_PROGRAM_CACHE = orderProgramCache
        cls.DEAL_CACHE = dealCache
    
    @classmethod
    def IsInitialized(cls):
        if (cls.TNP_CONST is not None 
                and cls.LOG is not None
                and cls.ORDER_CACHE is not None
                and cls.ORDER_BOOK_CACHE is not None
                and cls.ORDER_PROGRAM_CACHE is not None
                and cls.DEAL_CACHE is not None):
            return True
        else:
            return False

# ------------------------------------ TNP Order ------------------------------------

TNP_POSITION_REFERENCE = 131078

def AllCachedOrders():
    return TnpDependecies.ORDER_CACHE.values()
    
def GetTNPOrder(orderId):
    return TnpDependecies.ORDER_CACHE.get(orderId)

def FindTradeFromOrder(tnpOrder):
    return acm.FTrade[tnpOrder.szOrderId()]

def FindFillsForOrder(tnpOrder):
    query = 'orderUuid = {0}'.format(tnpOrder.szOrderId())
    return acm.FTrade.Select(query)

def PositionReferenceForOrder(tnpOrder):
    try:
        return GetFreeTextField(tnpOrder, TNP_POSITION_REFERENCE)
    except AttributeError:
        return None

def IsBulkOrder(tnpOrder):
    try:
        return TnpDependecies.TNP_CONST.TNP_OR_BULK_ORDER in unpack(tnpOrder.TNPORDERROLE.dwOrderRole()) 
    except StandardError:
        return False

def IsSalesOrder(tnpOrder):
    return TnpDependecies.TNP_CONST.TNP_ORDER_AF_SYSTEM_SALES_ORDER in unpack(tnpOrder.afOrderAttributesSystem())
   
def IsStandardSalesOrder(tnpOrder):
    return IsSalesOrder(tnpOrder) and not IsBulkOrder(tnpOrder)

def IsDeleteOrderCausedByOrderProgramRemoved(tnpOrder):
    return tnpOrder.dwDeleteReason() == TnpDependecies.TNP_CONST.TNP_DR_ORDER_PROGRAM_REMOVED

def IsPartOfOrderProgram(tnpOrder):
    return bool(tnpOrder.TNPORDERPROGRAMID.szOrderProgramId())

def GetOrderProgramForOrder(tnpOrder):
    return TnpDependecies.ORDER_PROGRAM_CACHE.get(tnpOrder.TNPORDERPROGRAMID.szOrderProgramId())

def IsOrderDone(tnpOrder):
    return tnpOrder.TNPSALESORDERSTATE.dwSalesOrderState() in [TnpDependecies.TNP_CONST.TNP_SOS_CANCELLED, 
                                                               TnpDependecies.TNP_CONST.TNP_SOS_DONE_SALES_ORDER, 
                                                               TnpDependecies.TNP_CONST.TNP_SOS_COMPLETED]
    
def TradedQuantity(tnpOrder):
    return tnpOrder.dTradedQuantity()
    
def QuantityToShape(tnpOrder):
    try:
        return tnpOrder.TNPDEALSTOSHAPEQUANTITY.dDealsToShapeQuantity() or 0.0
    except StandardError:
        return 0.0

def IsFxOrder(tnpOrder):
    try:
        return tnpOrder.TNPORDERPROCESSTYPE.dwOrderProcessType() in [TnpDependecies.TNP_CONST.TNP_OPT_FX_SPOT,
                                                              TnpDependecies.TNP_CONST.TNP_OPT_FX_FORWARD,
                                                              TnpDependecies.TNP_CONST.TNP_OPT_FX_SWAP]
        
    except StandardError:
        return False

def IsFxSpotOrder(tnpOrder):
    try:
        return tnpOrder.TNPORDERPROCESSTYPE.dwOrderProcessType() in [TnpDependecies.TNP_CONST.TNP_OPT_FX_SPOT]
    except StandardError:
        return False

def IsFxForwardOrder(tnpOrder):
    try:
        return tnpOrder.TNPORDERPROCESSTYPE.dwOrderProcessType() in [TnpDependecies.TNP_CONST.TNP_OPT_FX_FORWARD]
    except StandardError:
        return False

def IsFxSwapOrder(tnpOrder):
    try:
        return tnpOrder.TNPORDERPROCESSTYPE.dwOrderProcessType() in [TnpDependecies.TNP_CONST.TNP_OPT_FX_SWAP]
    except StandardError:
        return False
               
def FxValueDay(tnpOrder):
    try:
        return tnpOrder.TNPORDERPROCESSTYPE.TNPVALUEDATE.szValueDate()
    except StandardError:
        return acm.Time.DateToday()

def OrderProcessType(tnpOrder):
    PROCESSTYPES = {1:'FXSpot',2:'FXForward', 3:'FXSwap'}
    try:
        return PROCESSTYPES[tnpOrder.TNPORDERPROCESSTYPE.dwOrderProcessType()]
    except StandardError:
        return None
    
    
# ------------------------------------ TNP Deal ------------------------------------

TNP_PREFERRED_COUNTERPARTY_BROKER = 131073

def Counterparty(tnpDeal):
    try:
        return GetFreeTextField(tnpDeal, TNP_PREFERRED_COUNTERPARTY_BROKER)
    except AttributeError:
        return None

def FindTradeFromDeal(tnpDeal):
    return acm.FTrade[tnpDeal.szDealId()]

def IsBulkDeal(tnpDeal):
    return IsBulkOrder(OriginatingSalesOrder(tnpDeal))
  
def IsAllocatedDeal(tnpDeal):
    return tnpDeal.TNPDEALREASON.dwDealReason() == TnpDependecies.TNP_CONST.TNP_DRN_DISTRIBUTEDEAL

def IsPartOfAllocation(tnpDeal):
    return IsBulkDeal(tnpDeal) or IsAllocatedDeal(tnpDeal)
    
def FindPreviousDeals(tnpDeal):
    deals = [tnpDeal]
    try:
        deals.extend(FindPreviousDeals(TnpDependecies.DEAL_CACHE[tnpDeal.szExternalDealId()]))
    except KeyError:
        pass
    return deals

def OriginatingBulkDeal(tnpDeal):
    firstDeal = FindPreviousDeals(tnpDeal)[-1]
    return firstDeal if IsBulkDeal(firstDeal) else None

def OriginatingSalesOrder(tnpDeal):
    return GetTNPOrder(tnpDeal.TNPDEALTOSHAPEINFO.szSalesOrderId())

def IsDealFromMarket(tnpDeal):
    return tnpDeal.TNPDEALREASON.dwDealReason() in [TnpDependecies.TNP_CONST.TNP_DRN_ONE_TO_ONE_DEAL, 
                                                    TnpDependecies.TNP_CONST.TNP_DRN_MOVEORDER_FILL,
                                                    TnpDependecies.TNP_CONST.TNP_DRN_MOVEORDER_ONE_TO_ONE_FILL]
def IsDistributedDeal(tnpDeal):
    return (tnpDeal.TNPDEALREASON.dwDealReason() == TnpDependecies.TNP_CONST.TNP_DRN_DISTRIBUTEDEAL and
            not tnpDeal.dwSourceIdType() == TnpDependecies.TNP_CONST.TNP_SIT_VIRTUALORDER)
            
def IsAutomatchedDeal(tnpDeal):
    return tnpDeal.TNPDEALREASON.dwDealReason() == TnpDependecies.TNP_CONST.TNP_DRN_AUTOMATCH 

def DealCausedByTrade(tnpDeal):
    return IsDealFromMarket(tnpDeal) or IsDistributedDeal(tnpDeal) or IsAutomatchedDeal(tnpDeal)

def IsDeleteDeal(tnpDeal):
    return tnpDeal.dwMCFlag() == TnpDependecies.TNP_CONST.TNP_MCFLAG_DELETEDEAL


# ------------------------------------ Util functions ------------------------------------

TNP_OB_NAME_TAB = 8388608

def AMBAMessageForObjects(objects, msgType=None):
    """ Returns an AMBA transaction messages containing all objects in the list. """
    if objects:
        generator = acm.FAMBAMessageGenerator()
        generator.AddFields('{{Trade,Quantity}, {Trade,Premium}}') #Include even if 0

        message = generator.Generate(objects[0]) #Start with first
        message.RemoveMessage(message.Messages()[0]) #Remove first to only keep header
        message.AtPutStrings('SOURCE', 'pt')
        if msgType:
            message.AtPutStrings('TYPE', msgType)
        transMsg = acm.FAMBAMessage()
        transMsg.Type('TRANSACTION')
      
        for obj in objects:
            msg = generator.Generate(obj).Messages()[0]
            transMsg.AddMessage(msg)
            
        message.AddMessage(transMsg)
        return message

def GetFreeTextField(tnpMessage, fieldId):
    for freeText in tnpMessage.TNPFREETEXT:
        if freeText.dwFieldId() == fieldId:
            return freeText.szFreeText()

def OrderBookName(tnpOrderBook):
    for name in tnpOrderBook.TNPORDERBOOKNAME:
        if name.dwNameType() == TNP_OB_NAME_TAB:
            return name.szName()
  
def TnpOrderBook(tnpOrder):
    cache = TnpDependecies.ORDER_BOOK_CACHE
    return cache.get(tnpOrder.szOrderBookId())

def IsOrderMessage(tnpMessage):
    try:
        return tnpMessage.name() in ['MCNEWORDER', 'MCMODIFYORDER', 'MCDELETEORDER']
    except RuntimeError:
        return 'TNPENTEREDORDER' in str(tnpMessage)
    
def IsDealMessage(tnpMessage):
    try:
        return tnpMessage.name()  == 'MCDEAL'
    except RuntimeError:
        return False

def DateTimeFromTnp(dt):
    ''' Removing the ms part of tnp-message '''
    time = acm.Time.LocalTimeAsUTCDays(dt[:4], dt[4:6], dt[6:8],
                                       dt[8:10], dt[10:12], dt[12:14], 0)
    return acm.Time.UtcToLocal(time)

def unpack(bitmask): 
    potential_bits = []
    x = 1
    while x <= bitmask:
        potential_bits.append(x)
        x *= 2
    bits = []
    for x in reversed(potential_bits):
        if x <= bitmask:
            bits.append(x)
            bitmask -= x
    return bits
