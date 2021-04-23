import acm
import traceback
import pickle
import TradeCreationCustomization

from RFQUtils import Misc
from DealPackageUtil import SalesTradingInteraction
from TradeCreationUtil import TABTradeCreationSetting, TradeCreationUtil
from SalesTradingCustomizations import DefaultSalesAcquirer

# Quote Request Roles
TRADING = 1
SALES = 2
ROLE = {TRADING : 'Trading', SALES : 'Sales'}

# Sides
INTERNAL = 1
CLIENT = 2

# Deal Source Id Types
ORDER = 1
VIRTUALORDER = 2
DEALVERIFICATION = 3
QUOTE = 4
SALES_ORDER = 6

# Deal Attributes Systems
def get_bit(byteval, idx):
    return ((byteval&(1<<idx))!=0);
    
SHAPE_FINAL_DEST_BIT = 19
SHAPE_FINAL_SOURCE_BIT = 18
SHAPE_PL_DEST_BIT = 17
SHAPE_PL_SOURCE_BIT = 16

# Deal Reason
SHAPE = 10
REPORTDEAL_FILL = 23

# Deal Type
DEAL_TYPE = {ORDER : 'ORDER', QUOTE : 'QUOTE'}

def ExtractDictFromSalesTradingInfoString(freeText):
    return pickle.loads(freeText.szFreeText())

def CreateExtendedDataSubDict(imObject):
    extendedDataDict = acm.FDictionary()
    if imObject:
        for freeText in imObject.TNPFREETEXT:
            extendedDataName = Caching.FreeText(freeText.dwFieldId())
            if extendedDataName == 'SalesTradingInfo':
                salesTradingInfoDict = ExtractDictFromSalesTradingInfoString(freeText)
                extendedDataDict.AddAll(salesTradingInfoDict)
            else:
                extendedDataDict.AtPut(Caching.FreeText(freeText.dwFieldId()), freeText.szFreeText())
    return extendedDataDict

class Logging(object):

    _log = None

    @classmethod
    def LogObject(cls, log='*READING*'):
        if log == '*READING*':
            return cls._log
        else:
            cls._log = log

    @classmethod
    def Warning(cls, text):
        cls._log.warning(text)

    @classmethod
    def Error(cls, text):
        cls._log.error(text)

    @classmethod
    def Info(cls, text):
        cls._log.info(text)

    @classmethod
    def Success(cls, text):
        cls._log.success(text)

class Caching(object):

    _externalCaches = {}

    @classmethod
    def SetExternalCaches(cls, externalCaches):
        cls._externalCaches = externalCaches

    @classmethod
    def FreeTextCache(cls):
        return cls._externalCaches.get('FreeText')

    @classmethod
    def OrderCache(cls):
        return cls._externalCaches.get('Order')

    @classmethod
    def QuoteRequestCache(cls):
        return cls._externalCaches.get('QuoteRequest')

    @classmethod
    def Order(cls, salesOrderId):
        orderCache = cls.OrderCache()
        return orderCache.get(salesOrderId)

    @classmethod
    def QuoteRequest(cls, quoteRequestId):
        quoteRequestCache = cls.QuoteRequestCache()
        return quoteRequestCache.get(quoteRequestId)

    @classmethod
    def FreeText(cls, fieldId):
        freeTextCache = cls.FreeTextCache()
        return freeTextCache.get(fieldId)

    @classmethod
    def Cache(cls):
        if 'objectCache' not in globals():
            global objectCache
            objectCache = {}
        return objectCache

    @classmethod
    def LocalCache(cls, masterId):
        if masterId:
            return cls.Cache().setdefault(masterId, {})
        else:
            raise Exception('MasterId must be specified to obtain local cache.')

    @classmethod
    def InitLocalCache(cls, masterId):
        if masterId:
            localCache = cls.LocalCache(masterId)
            if len(localCache) == 0:
                localCache['extendedDataDict'] = acm.FDictionary()
                localCache['deals'] = {}

    @classmethod
    def ClearLocalCache(cls, masterId):
        del cls.Cache()[masterId]

    @classmethod
    def DealPairs(cls):
        return cls.Cache().setdefault('dealPairs', {})

    @classmethod
    def DealPair(cls, deal):
        dealPairId = deal.DealPairId()
        dealPairsDict = Caching.DealPairs()
        return dealPairsDict.setdefault(dealPairId, {})

    @classmethod
    def ClearDealPairCache(cls, deal):
        del cls.DealPairs()[deal.DealPairId()]

    @classmethod
    def UpdateDealPairCache(cls, deal):
        dealPair = cls.DealPair(deal)
        dealPair[deal.OrderOrQuote()] = deal

    @classmethod
    def CacheDeal(cls, masterId, deal):
        localCache = cls.LocalCache(masterId)
        dealCache = localCache['deals']
        dealDict = dealCache.setdefault(deal.SourceName(), {})
        dealDict[DEAL_TYPE[deal.OrderOrQuote()]] = deal

    @classmethod
    def ClientDeals(cls, masterId):
        localCache = cls.LocalCache(masterId)
        dealCache = localCache['deals']
        return dealCache[SalesTradingInteraction.SALES_NAME]

    @classmethod
    def InternalDeals(cls, masterId):
        localCache = cls.LocalCache(masterId)
        dealCache = localCache['deals']
        internalDeals = dealCache.copy()
        del internalDeals[SalesTradingInteraction.SALES_NAME]
        return internalDeals

    @classmethod
    def IsCached(cls, masterId, deal):
        localCache = cls.LocalCache(masterId)
        dealCache = localCache['deals']
        dealDict = dealCache.setdefault(deal.SourceName(), {})
        return dealDict.get(deal.OrderOrQuote()) is not None

    @classmethod
    def AllDealsFound(cls, masterId):
        localCache = cls.LocalCache(masterId)
        dealCache = localCache['deals']
        numberOfComponents = cls.NumberOfComponents(masterId)
        allDealsFound = numberOfComponents is not None
        if allDealsFound:
            allDealsFound = len(dealCache) == (cls.NumberOfComponents(masterId) + 1)
            if allDealsFound:
                for componentName, deals in dealCache.items():
                    if len(deals) != 2:
                        allDealsFound = False
                        break
        return allDealsFound

    @classmethod
    def ExtendedDataDict(cls, masterId):
        localCache = cls.LocalCache(masterId)
        return localCache['extendedDataDict']

    @classmethod
    def UpdateExtendedDataDict(cls, masterId, deal):
        name = ''
        if masterId:
            extendedDataDict = cls.ExtendedDataDict(masterId)
            if deal.IsRFQDeal():
                quoteRequestDict = CreateExtendedDataSubDict(deal.TnpQuoteRequest())
                name = quoteRequestDict.At('name')
                extendedDataDict.AtPut(name, quoteRequestDict)
                extendedDataDict.AtPut(name + ' Quote', CreateExtendedDataSubDict(deal.TnpQuote()))
            elif deal.IsSalesOrderDeal():
                name = SalesTradingInteraction.SALES_NAME
                extendedDataDict.AtPut(name, CreateExtendedDataSubDict(deal.TnpOrder()))
        return name
    
    @classmethod
    def NumberOfComponents(cls, masterId):
        numberOfComponents = None
        extendedDataDict = cls.ExtendedDataDict(masterId)
        salesComponentDict = extendedDataDict.At(SalesTradingInteraction.SALES_NAME)
        if salesComponentDict:
            numberOfComponents = salesComponentDict.At('numberOfComponents')
        return numberOfComponents
        
    @classmethod
    def InvestmentDecider(cls, masterId):
        localCache = cls.LocalCache(masterId)
        return localCache.get('investmentDecider')

    @classmethod
    def Client(cls, masterId):
        localCache = cls.LocalCache(masterId)
        return localCache.get('client')

    @classmethod
    def UpdateInvestmentDecider(cls, masterId, investmentDecider):
        localCache = cls.LocalCache(masterId)
        localCache['investmentDecider'] = investmentDecider

    @classmethod
    def UpdateClient(cls, masterId, client):
        localCache = cls.LocalCache(masterId)
        localCache['client'] = client

class TradeCreationHookArgument(object):

    def __init__(self, clientTrades, internalTrades, extendedDataDict, isFromSalesOrder):
        self._clientTrades = clientTrades
        self._internalTrades = internalTrades
        self._extendedDataDict = extendedDataDict
        self._isFromSalesOrder = isFromSalesOrder

    def ClientTrades(self):
        return self._clientTrades

    def InternalTrades(self):
        return self._internalTrades

    def ExtendedDataDict(self):
        return self._extendedDataDict

    def IsFromSalesOrder(self):
        return self._isFromSalesOrder

    def LogObject(self):
        return Logging.LogObject()

    def Info(self, text):
        Logging.Info(text)

    def Warning(self, text):
        Logging.Warning(text)

    def Error(self, text):
        Logging.Error(text)

    def Success(self, text):
        Logging.Success(text)

class DealWrapperBase(object):

    def __init__(self, AMBTrade, tnpDeal, TnpConst):
        self._AMBTrade = AMBTrade
        self._tnpDeal = tnpDeal
        self._tnpConst = TnpConst
        self.InitLocalCache()
        self.UpdateExtendedDataDict()
        self.CreateAndUpdateAcmTrade()
        self.ValidateAcmTrade()
    
    def AMBTrade(self):
        return self._AMBTrade

    def TnpDeal(self):
        return self._tnpDeal

    def TnpQuoteRequest(self):
        return None

    def TnpQuote(self):
        return None

    def TnpOrder(self):
        return None

    def TnpConst(self):
        return self._tnpConst

    def TnpDealType(self):
        return self.TnpDeal().dwSourceIdType()

    def AcmTrade(self):
        return self._acmTrade

    def AcmTradeDecorator(self):
        return self._acmTrdDeco
    
    def MasterId(self):
        return None

    def AccountId(self):
        return self.TnpDeal().ReferenceData.szAccountId()

    def CustomerId(self):
        return None

    def DealPairId(self):
        return self.TnpDeal().TNPDEALPAIRID.szDealPairId()

    def IsSalesOrderDeal(self):
        return False

    def IsRFQDeal(self):
        return False

    def Side(self):
        return None

    def OrderOrQuote(self):
        return None

    def IsOrderDeal(self):
        return self.OrderOrQuote() == ORDER

    def IsQuoteDeal(self):
        return self.OrderOrQuote() == QUOTE

    def IsClientOrderDeal(self):
        return self.Side() == CLIENT and self.OrderOrQuote() == ORDER

    def IsClientQuoteDeal(self):
        return self.Side() == CLIENT and self.OrderOrQuote() == QUOTE

    def IsInternalOrderDeal(self):
        return self.Side() == INTERNAL and self.OrderOrQuote() == ORDER

    def IsInternalQuoteDeal(self):
        return self.Side() == INTERNAL and self.OrderOrQuote() == QUOTE

    def IsInternalDeal(self):
        return self.Side() == INTERNAL

    def ClientId(self):
        return None

    def Client(self):
        return acm.FParty[self.ClientId()] if self.ClientId() else None

    def Counterparty(self):
        if self.IsClientQuoteDeal():
            cptyName = self.ClientId()
        else:
            cptyName = self.TnpDeal().szCounterpartyCompanyId()
        return acm.FParty[cptyName] if cptyName else None

    def InvestmentDecider(self):
        return Misc.GetInvestmentDeciderObject(self.Client(), self.InvestmentDecisionMakerId())
    
    def InitLocalCache(self):
        Caching.InitLocalCache(self.MasterId())
    
    def UpdateExtendedDataDict(self):
        sourceName = Caching.UpdateExtendedDataDict(self.MasterId(), self)
        self.SourceName(sourceName)
    
    def Twin(self):
        dealPair = Caching.DealPair(self)
        twin = dealPair.get(ORDER if self.IsQuoteDeal() else QUOTE)
        return twin

    def SetTradeQuantity(self):
        # Should actually be done in trade_generic.py in the TAB
        TnpConst = self.TnpConst()
        dQuantity = float(self.TnpDeal().dQuantity())
        instrument = self.AcmTrade().Instrument()
        direction = self.TnpDeal().dwBidOrAsk()
        quantity = 0
        if instrument and instrument.IsSwap() and instrument.SwapType() != 'Float/Float':
            if direction == TnpConst.TNP_ASK:
                quantity = dQuantity if instrument.RecLeg().IsFixedLeg() else -dQuantity
            elif direction == TnpConst.TNP_BID:
                quantity = -dQuantity if instrument.RecLeg().IsFixedLeg() else dQuantity
        else:
            quantity = -dQuantity if direction==TnpConst.TNP_ASK else dQuantity
        self.AcmTradeDecorator().Quantity(quantity)

    def SetPortfolioAndAcquirer(self):
        self.SetPortfolio()
        self.SetAcquirer()

    def SetPortfolio(self):
        portfolio = acm.FPhysicalPortfolio[self.AccountId()] if self.AccountId() else None
        if portfolio:
            self.AcmTradeDecorator().Portfolio(portfolio)
        else:
            if self.IsClientQuoteDeal():
                Logging.Warning("Cannot set sales portfolio: No accoundId on tnpDeal and no default sales portfolio specified.")
            elif self.IsInternalDeal():
                Logging.Warning("Cannot set trader portfolio: No default quote or own order account specified.")
    
    def SetAcquirer(self):
        acquirer = None
        portfolio = self.AcmTrade().Portfolio()
        if portfolio:
            owner = portfolio.PortfolioOwner()
        defaultSalesAcquirer = DefaultSalesAcquirer(portfolio)
        if self.IsClientQuoteDeal():
            acquirer = defaultSalesAcquirer if defaultSalesAcquirer else owner
        else:
            acquirer = owner
        if acquirer:
            self.AcmTradeDecorator().Acquirer(acquirer)
        else:
            if self.IsClientQuoteDeal():
                Logging.Warning("Cannot set sales acquirer: No default acquirer specified and sales portfolio '%s' has no owner." % portfolio.Name() if portfolio else portfolio)
            elif self.IsInternalDeal():
                Logging.Warning("Cannot set trader acquirer: Portfolio '%s' has no owner." % portfolio.Name())
        return acquirer

    def SetCounterparty(self):
        self.AcmTradeDecorator().Counterparty(self.Counterparty())

    def SetTrader(self):
        traderName = self.TnpDeal().szOriginalBrokerId()
        trader = acm.FUser[traderName] if traderName else None
        self.AcmTradeDecorator().Trader(trader)

    def SetStatus(self):
        self.AcmTradeDecorator().Status('FO Confirmed')

    def CreateAndUpdateAcmTrade(self):
        self.CreateAcmTrade()
        self.UpdateAcmTrade()
    
    def ValidateAcmTrade(self):
        if not self.AcmTrade().Instrument():
            raise Exception('TNP-ADM mapping failed. The FTrade created from the AMBA message has no instrument.')

    def CreateAcmTrade(self):
        self._acmTrade = acm.AMBAMessage.CreateObjectFromMessage(str(self.AMBTrade()))
        self._acmTrdDeco = acm.FBusinessLogicDecorator.WrapObject(self._acmTrade)

    def UpdateAcmTrade(self):
        trade = self.AcmTrade()
        trdDeco = self.AcmTradeDecorator()
        trdDeco.TradeTime(trade.TradeTime()) # TODO to set value day, what should value day be?
        self.SetTradeQuantity()
        self.SetPortfolioAndAcquirer()
        self.SetCounterparty()
        self.SetTrader()
        self.SetStatus() 

class SalesOrderDeal(DealWrapperBase):

    def IsSalesOrderDeal(self):
        return True
    
    def MasterId(self):
        return self.SalesOrderId()

    def TnpOrder(self):
        return Caching.Order(self.SalesOrderId())
    
    def SourceName(self, sourceName = '*NoInput*'):
        if sourceName == '*NoInput*':
            return SalesTradingInteraction.SALES_NAME if self.Side() == CLIENT else SalesTradingInteraction.MAIN_TRADING_COMPONENT_NAME

    def InvestmentDecisionMakerId(self):
        investmentDecisionMakerId = None
        if self.TnpOrder() and self.ClientId():
            investmentDecisionMakerId = self.TnpOrder().TNPINVESTMENTDECISIONMAKERID.szInvestmentDecisionMakerId() 
        return investmentDecisionMakerId

    def Side(self):
        return INTERNAL if self.TnpDealType() == DEALVERIFICATION else CLIENT

    def OrderOrQuote(self):
        dealType = self.TnpDealType()
        if dealType == DEALVERIFICATION:
            orderOrQuote = ORDER if self.TnpDeal().TNPCUSTOMERID.szCustomerId() else QUOTE
        else:
            orderOrQuote = ORDER if dealType == SALES_ORDER else QUOTE
        return orderOrQuote

    def SalesOrderId(self):
        salesOrderId = None
        tnpDeal = self.TnpDeal()
        if self.IsClientOrderDeal():
            salesOrderId = tnpDeal.szSourceId()
        elif self.IsInternalOrderDeal():
            salesOrderId = tnpDeal.TNPDEALTOSHAPEINFO.szSalesOrderId()
        if not salesOrderId:
            twin = self.Twin()
            if twin:
                salesOrderId = twin.SalesOrderId()
        return salesOrderId

    def ClientId(self):
        clientId = None
        if not self.IsInternalQuoteDeal():
            clientId = self.TnpDeal().TNPCUSTOMERID.szCustomerId()
        return clientId

class RFQDeal(DealWrapperBase):

    def IsRFQDeal(self):
        return True
    
    def MasterId(self):
        return self.CustomerRequestId()
    
    def SourceName(self, sourceName = '*NoInput*'):
        if sourceName == '*NoInput*':
            return self._sourceName
        else:
            self._sourceName = sourceName

    def TnpQuoteRequest(self):
        return Caching.QuoteRequest(self.QuoteRequestId())

    def TnpQuote(self):
        return self.TnpQuoteRequest().TNPQUOTEREQUESTANSWER.TNPQUOTE

    def QuoteRequestId(self):
        tnpQuoteRequestId = self.TnpDeal().TNPQUOTEREQUESTID
        return tnpQuoteRequestId.szQuoteRequestId() if tnpQuoteRequestId else None

    def QuoteRequestRole(self):
        return self.TnpQuoteRequest().TNPQUOTEREQUESTROLE.dwQuoteRequestRole()

    def CustomerRequestId(self):
        return self.TnpDeal().TNPCUSTOMERREQUESTID.szCustomerRequestId()

    def ClientId(self):
        clientId = None
        if self.IsClientQuoteDeal():
            clientId = self.TnpQuoteRequest().TNPCUSTOMERID.szCustomerId()
        return clientId

    def InvestmentDecisionMakerId(self):
        return self.TnpQuoteRequest().TNPINVESTMENTDECISIONMAKERID.szInvestmentDecisionMakerId()
        
    def Side(self):
        return CLIENT if self.SourceName() == SalesTradingInteraction.SALES_NAME else INTERNAL #CLIENT if self.QuoteRequestRole() == SALES else INTERNAL

    def OrderOrQuote(self):
        return self.TnpDealType()

    def UpdateAcmTrade(self):
        DealWrapperBase.UpdateAcmTrade(self)
        self.SetQuoteRequestIdAddInfo()

    def SetQuoteRequestIdAddInfo(self):
        TradeCreationUtil.SetAddInfoOnTrades([self.AcmTrade()], 'QuoteRequestId', self.QuoteRequestId())       
        
class DealHandler(object):
    def __init__(self, currentDeal):
        self._currentDeal = currentDeal
    
    def UpdateClient(self):
        if self.MasterId():
            client = self.CurrentDeal().Client()
            if client:
                Caching.UpdateClient(self.MasterId(), client)

    def UpdateInvestmentDecider(self):
        if self.MasterId():
            investmentDecider = self.CurrentDeal().InvestmentDecider()
            if investmentDecider:
                Caching.UpdateInvestmentDecider(self.MasterId(), investmentDecider) 

    def UpdateRegulatoryInfo(self):
        deal = self.ClientQuoteDeal()
        trade = deal.AcmTrade()
        regInfo = trade.RegulatoryInfo()
        regInfo.TheirOrganisation(Caching.Client(self.MasterId()))
        regInfo.TheirInvestmentDecider(Caching.InvestmentDecider(self.MasterId()))
    
    def UpdateSalesOrderIdAddInfos(self):
        internalTrades = self.InternalTrades()[SalesTradingInteraction.MAIN_TRADING_COMPONENT_NAME]
        allTrades = list(self.ClientTrades().values()) + list(internalTrades.values())
        if self.MasterId():
            TradeCreationUtil.SetAddInfoOnTrades(allTrades, 'SalesOrderId', self.MasterId())
    
    def UpdateSalesOrderClientQuoteDealPortfolio(self):
        # Must unforunately be done since the client quote trade Account is hardcoded in the autoshaper registry
        self.ClientTrades()[DEAL_TYPE[QUOTE]].Portfolio(self.CurrentDeal().TnpOrder().ReferenceData.szAccountId())
    
    def UpdateSalesOrderInternalTradePrices(self):
        # Must unforunately be done since the internal trades have the wrong price for multiple partial fill sales orders
        isAsk = self.ClientQuoteDeal().AcmTrade().Quantity() < 0.0
        sign = 1 if isAsk else -1
        priceDiff = sign * float(self.ExtendedDataDict().At(SalesTradingInteraction.SALES_NAME).At('Shape Price Margin'))
        traderPrice = self.ClientQuoteDeal().AcmTrade().Price() - priceDiff
        for k, trade in self.InternalTrades()[SalesTradingInteraction.MAIN_TRADING_COMPONENT_NAME].items():
            trade.Price(traderPrice)
        
    def CurrentDeal(self):
        return self._currentDeal

    def CanExtractMasterId(self):
        return self.MasterId() != '' and self.MasterId() is not None

    def MasterId(self):
        return self.CurrentDeal().MasterId()

    def CacheDeal(self, deal):
        Caching.CacheDeal(self.MasterId(), deal)

    def IsCached(self, deal):
        Caching.IsCached(self.MasterId(), deal)

    def UpdateDealPairCache(self):
        Caching.UpdateDealPairCache(self.CurrentDeal())

    def AllDealsFound(self):
        allDealsFound = False
        if self.MasterId():
            allDealsFound = Caching.AllDealsFound(self.MasterId())
        return allDealsFound

    def ClearDealPairCache(self):
        Caching.ClearDealPairCache(self.CurrentDeal())

    def ClearCache(self):
        Caching.ClearLocalCache(self.MasterId())

    def ClientTrades(self):
        clientDeals = Caching.ClientDeals(self.MasterId())
        order = DEAL_TYPE[ORDER]
        quote = DEAL_TYPE[QUOTE]
        return {order : clientDeals[order].AcmTrade(), quote : clientDeals[quote].AcmTrade()}

    def ClientQuoteDeal(self):
        clientDeals = Caching.ClientDeals(self.MasterId())
        return clientDeals[DEAL_TYPE[QUOTE]]

    def InternalTrades(self):
        internalDeals = Caching.InternalDeals(self.MasterId())
        order = DEAL_TYPE[ORDER]
        quote = DEAL_TYPE[QUOTE]
        internalTrades = {}
        for componentName, deals in internalDeals.items():
            internalTrades[componentName] = {order : deals[order].AcmTrade(), quote : deals[quote].AcmTrade()}
        return internalTrades

    def ExtendedDataDict(self):
        return Caching.ExtendedDataDict(self.MasterId())

    def Commit(self, artifactsToCommit):
        acm.BeginTransaction()
        try:
            for artifact in artifactsToCommit:
                artifact.Commit()
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            raise Exception(traceback.format_exc() + ": Failed to commit transaction: '%s'" % e)

    def PreTradeCreationHook(self):
        self.UpdateRegulatoryInfo()
        if self.CurrentDeal().IsSalesOrderDeal():
            self.UpdateSalesOrderIdAddInfos()
            self.UpdateSalesOrderClientQuoteDealPortfolio()
            self.UpdateSalesOrderInternalTradePrices()

    def CallTradeCreationHook(self):
        self.PreTradeCreationHook()
        hookArgument = TradeCreationHookArgument(self.ClientTrades(), self.InternalTrades(), self.ExtendedDataDict(), self.CurrentDeal().IsSalesOrderDeal())
        artifactsToCommit = TradeCreationCustomization.TradeCreation(hookArgument)
        return artifactsToCommit

    def CollectDeal(self):
        self.UpdateClient()
        self.UpdateInvestmentDecider()
        if self.CurrentDeal().IsRFQDeal():
            self.CollectRFQDeal()
        elif self.CurrentDeal().IsSalesOrderDeal():
            self.CollectSalesOrderDeal()

    def CollectRFQDeal(self):
        self.CacheDeal(self.CurrentDeal())

    def CollectSalesOrderDeal(self):
        self.UpdateDealPairCache()
        if self.CanExtractMasterId():
            self.CacheDeal(self.CurrentDeal())
            twin = self.CurrentDeal().Twin() # The SalesOrderId can always be extracted from one of the trades in each of the two deal pairs
            if twin and not self.IsCached(twin):
                self.CacheDeal(twin)
                self.ClearDealPairCache()

    def CreateTrades(self):
        artifactsToCommit = self.CallTradeCreationHook()
        self.Commit(artifactsToCommit)
        self.ClearCache()

class DealHandlerCreation(object):

    @classmethod
    def IsFromRFQ(cls, tnpDeal):
        isFromRFQ = False
        if tnpDeal.TNPQUOTEREQUESTID and tnpDeal.dwSourceIdType() in [ORDER, QUOTE]:
            isFromRFQ = True
        return isFromRFQ

    @classmethod
    def IsFromSalesOrder(cls, tnpDeal):
        isFromOrder = False
        dealType = tnpDeal.dwSourceIdType()
        dealAttribute = tnpDeal.afDealAttributesSystem()
        dealReason = tnpDeal.TNPDEALREASON.dwDealReason()
        
        if dealType == DEALVERIFICATION and dealReason == REPORTDEAL_FILL:
            isFromOrder = True
        elif dealType == VIRTUALORDER and dealReason == SHAPE:
            isFromOrder = get_bit(dealAttribute, SHAPE_FINAL_SOURCE_BIT) | get_bit(dealAttribute, SHAPE_PL_SOURCE_BIT) | get_bit(dealAttribute, SHAPE_PL_DEST_BIT)
        elif dealType == SALES_ORDER and dealReason == SHAPE:
            isFromOrder = get_bit(dealAttribute, SHAPE_FINAL_DEST_BIT)
        return isFromOrder

    @classmethod
    def IsRelevant(cls, tnpDeal):
        isRelevant = True
        dealType = tnpDeal.dwSourceIdType()
        dealAttribute = tnpDeal.afDealAttributesSystem()
        dealReason = tnpDeal.TNPDEALREASON.dwDealReason()
        if dealType == VIRTUALORDER and dealReason == SHAPE:
            isRelevant = not (get_bit(dealAttribute, SHAPE_PL_SOURCE_BIT) | get_bit(dealAttribute, SHAPE_PL_DEST_BIT))
        return isRelevant

    @classmethod
    def New(cls, AMBTrade, tnpDeal, TnpConst):
        dealHandler = None
        deal = None
        if cls.IsFromSalesOrder(tnpDeal) and cls.IsRelevant(tnpDeal):
            deal = SalesOrderDeal(AMBTrade, tnpDeal, TnpConst) 
        elif cls.IsFromRFQ(tnpDeal):
            deal = RFQDeal(AMBTrade, tnpDeal, TnpConst)
        if deal:
            dealHandler = DealHandler(deal)
        return dealHandler

def TradeCreation(AMBTrade, tnpDeal, externalCaches, TnpConst, log, *args):
    tradesCreated = False
    try:
        Logging.LogObject(log)
        Caching.SetExternalCaches(externalCaches)
        dealHandler = DealHandlerCreation.New(AMBTrade, tnpDeal, TnpConst)
        if dealHandler:
            dealHandler.CollectDeal()
            if dealHandler.AllDealsFound():
                dealHandler.CreateTrades()
                tradesCreated = True
        return tradesCreated
    except Exception as e:
        raise Exception('Trade creation failed: ' + traceback.format_exc())
