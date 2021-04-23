""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendUtils.py"

from __future__ import print_function
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendUtils

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Security loan utility functions.

------------------------------------------------------------------------------------------------"""
import acm
import traceback

import FUxCore
import itertools
import math
import time
from datetime import datetime
from functools import wraps

from DealPackageDevKit import CommandActionBase
from DealPackageUtil import IsFObject
from FLogger import FLogger
from FParameterSettings import ParameterSettingsCreator
from FSecLendDealUtils import SecurityLoanCreator
from ACMPyUtils import Transaction

TreeSpecificationForObject = acm.GetFunction('TreeSpecificationForObject', 1)

_SETTINGS = ParameterSettingsCreator.FromRootParameter('SecLendSettings')


def BenchmarkLogger():
    # info: 1, debug: 2
    level = 2 if _SETTINGS.BenchmarkingLogging() else 1
    b_logger = FLogger.GetLogger(name='SLOMS Benchmarker:')
    b_logger.Reinitialize(level=level)
    return b_logger


def Logger():
    LEVELS = {'info': 1, 'debug': 2, 'error': 3}
    logLevel = _SETTINGS.SLOMSLogger()
    level = logLevel.lower() if logLevel else 'info'
    LOGGER = FLogger.GetLogger(name='SLOMS')
    LOGGER.Reinitialize(
        level=LEVELS.get(level))
    return LOGGER


benchmark_logger = BenchmarkLogger()
logger = Logger()

class CalculationSpaceCollectionCache():
    # Util class for reusing Calculation Space Collection
    
    _spaceCollection = None
    _spaces = set()

    @classmethod
    def _GetCollection(cls):
        if not cls._spaceCollection:
            spaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
            cls._spaceCollection = spaceCollection
        return cls._spaceCollection
    
    @classmethod
    def GetSpace(cls, sheetClass, context):
        space = cls._GetCollection().GetSpace(sheetClass, context)
        cls._spaces.add(space)
        return space
    
    @classmethod    
    def Clear(cls):
        _spaceCollection.Clear()
        _spaces.clear()


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        if args:
            benchmark_logger.debug("{} - {}:{} {} -> {}".format(
            args, function.__module__, function.func_name," " * 10, t1 - t0))
        else:
            benchmark_logger.debug("{}:{} {} -> {}".format(
            function.__module__, function.func_name, " " * 10, t1 - t0))
        return result

    return function_timer


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# ----------------------------------------------------------------------------------------------
#  Security loan deal/instrument helper functions

def AbsoluteQuantity(trade):
    quantity = trade.Quantity()
    if IsFObject(trade.Instrument(), acm.FSecurityLoan):
        quantity = trade.FaceValue()
    return abs(quantity)

class ActionCommandActionBase(CommandActionBase):
    ATTRIBUTE_NAME = 'action_attribute_name'

    def Applicable(self):
        return self.ATTRIBUTE_NAME in self.DealPackage().GetAttributes()

    def Enabled(self):
        return self.DealPackage().GetAttributeMetaData(self.ATTRIBUTE_NAME, 'enabled')()

    def Invoke(self):
        actionFn = self.DealPackage().GetAttribute(self.ATTRIBUTE_NAME)
        if actionFn:
            actionFn()


def Decorated(obj):
    if not hasattr(obj, 'DecoratedObject'):
        return acm.FBusinessLogicDecorator.WrapObject(obj)
    return obj


def GetAllMasterSecurityLoans():
    query = acm.CreateFASQLQuery(acm.FSecurityLoan, 'AND')
    query.AddAttrNode('ProductTypeChlItem.Name', 'EQUAL', 'Master Security Loan')
    return query.Select()


def GetMasterSecurityLoan(instrument):
    if instrument:
        try:
            if instrument.IsKindOf(acm.FSecurityLoan):
                if instrument.ProductTypeChlItem() and \
                        instrument.ProductTypeChlItem().Name() == "Master Security Loan":
                    return instrument
                else:
                    instrument = instrument.Underlying()
            return acm.FSecurityLoan.Select01('underlying = {0} and productTypeChlItem = "{1}"'.format(
                instrument.Originator().Oid(), "Master Security Loan"), None)
        except AttributeError as ex:
            print("AttributeError occurred: {}".format(ex))
        except Exception as ex:
            logger.error(
                "GetMasterSecurityLoan Error: {}. More than one master security loan instrument found using this instrument: {}".format(
                    ex, instrument.Originator().Name()))
    return None


def GetTradableSecurities():
    return [ins.Underlying() for ins in GetAllMasterSecurityLoans()]

    
def CommitTrades(trades, chunkSize=50):
    for chuned_trades in [trades[x:x+chunkSize] for x in range(0, len(trades), chunkSize)]:
        with Transaction():
            for trade in chuned_trades:
                if trade.Instrument().IsInfant():
                    trade.Instrument().Commit()
                trade.Commit()

# ----------------------------------------------------------------------------------------------
#  Function for creating an availability trade
def CreateMasterSecurityLoan(underlying,
                             quantity=1,
                             status='Legally Confirmed',
                             acquirer=None,
                             counterparty=None,
                             portfolio=None,
                             valueday=None):
    master = GetMasterSecurityLoan(underlying)
    if master:
        trade = SecurityLoanCreator.CreateMasterSecurityLoanTrade(
            master,
            quantity=quantity,
            acquirer=acquirer,
            counterparty=counterparty,
            status=status,
            portfolio=portfolio,
            valueday=valueday)
        return trade
    return None

def GetSecurityLoanInstances(instrument):
    if instrument:
        if instrument.IsKindOf(acm.FSecurityLoan):
            if not instrument.ProductTypeChlItem() or \
                    instrument.ProductTypeChlItem().Name() != "Master Security Loan":
                return instrument
            instrument = instrument.Underlying()
        if not instrument.IsInfant():
            query = 'underlying={0} and productTypeChlItem <> "Master Security Loan"'.format(instrument.Oid())
            return acm.FSecurityLoan.Select(query)
    return []


def HasRemainingNominal(trade):
    return RemainingNominal(trade) != 0


def IsSameDirection(trade, quantity):
    return bool((int(quantity) ^ int(trade.Quantity())) >= 0)


def RemainingNominal(trade):
    return sum((t.FaceValue() for t in trade.Instrument().OriginalOrSelf().Trades()))


def SetSource(trade, source):
    if trade and acm.FMarketPlace[source]:
        trade.Market(source)

def IncludeExpiredTill():
    return str(_SETTINGS.IncludeExpiredTill())

def ActiveLoansBaseQuery():
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    query.AddAttrNodeEnum('Instrument.InsType', 'SecurityLoan')
    ExpiryDate = query.AddOpNode('AND')
    ExpiryDate.AddAttrNode('Instrument.ExpiryDate', 'GREATER_EQUAL', _SETTINGS.IncludeExpiredTill())
    ExpiryDate.AddAttrNode('Instrument.ExpiryDate', 'LESS_EQUAL', None)
    OpenEnd = query.AddOpNode('AND')
    OpenEnd.Not(True)
    OpenEnd.AddAttrNode('Instrument.OpenEnd',"EQUAL" ,"Terminated")
    return query


def SetDefaultRate(trade, destributed=False):
    """
    This function calculate a suggested fee for the security loan
    based on an extension attribute Security Loan Suggested Fee

    calc_space_coll = acm.Calculations().CreateCalculationSpaceCollection(acm.FStoredCalculationEnvironment["Limpro"])
    calc_space = calc_space_coll.GetSpace(
            acm.FTradeSheet, acm.GetDefaultContext().Name(),
            None, destributed)
    print "calculating..."
    calculation = calc_space.CreateCalculation(trade, 'Security Loan Suggested Fee', None)
    rate = calculation.Value().Number() if calculation.Value() else None
    print "rate:",rate
    :param trade:
    :return: double
    """
    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
    rate = calc_space.CreateCalculation(trade, 'Security Loan Suggested Fee')
    try:
        rate = (float(rate.Value()) or 0)
        if not rate or math.isnan(rate):
            rate = 0
    except Exception as e:
        print("SetDefaultRate error:", e)
        rate = 0
    SetSecurityLoanRate(trade, rate)
    return rate

def SetSecurityLoanRate(tradeOrInstrument, rate):
    """"slower?"""
    try:
        if tradeOrInstrument.Instrument().ProductTypeChlItem() and \
                tradeOrInstrument.Instrument().ProductTypeChlItem().Name() == "Rebate Security Loan":
            leg = Decorated(tradeOrInstrument.Instrument().FirstReceiveLeg())
        else:
            leg = Decorated(tradeOrInstrument.Instrument().FirstPayLeg())
        leg.GenerateSpreadFixings(True)
        leg.GenerateCashFlows(0.0)
        leg.Leg().StartingFee(rate)
    except Exception as e:
        print(traceback.format_exc())


def GetSecurityLoanRate(trade):
    if trade.Instrument().ProductTypeChlItem() and \
            trade.Instrument().ProductTypeChlItem().Name() == "Rebate Security Loan":
        leg = trade.Instrument().FirstReceiveLeg()
    else:
        leg = trade.Instrument().FirstPayLeg()
    return leg.StartingFee() if leg and not math.isnan(leg.StartingFee()) else None

def SetTradeQuantity(trade, quantity):
    if quantity:
        trade = Decorated(trade)
        trade.Quantity = quantity


def GetUnderlying(underlyingOrSecurityLoan):
    if underlyingOrSecurityLoan:
        if underlyingOrSecurityLoan.IsKindOf(acm.FSecurityLoan):
            return underlyingOrSecurityLoan.Underlying()
        else:
            return underlyingOrSecurityLoan


def CreateInstrument(underlyingOrSecurityLoan, **kwargs):
    underlying = GetUnderlying(underlyingOrSecurityLoan)
    if underlying:
        return SecurityLoanCreator.CreateInstrument(underlying=underlying, **kwargs)


def TradeFromInstrument(underying, **kwargs):
    loan = CreateInstrument(underying, **kwargs)
    return SecurityLoanCreator.CreateTrade(loan) if loan else None


def LoanType(trade):
    if trade.Type() == 'Normal':
        return 'New'
    elif trade.Type() == 'Closing':
        return 'Return'
    elif trade.Type() == 'Adjust':
        return 'Increase'
    else:
        return ''

def IsAvailabilityTrade(trade):
    return trade.TradeCategory() == 'Collateral' and IsMasterSecLoan(trade.Instrument())


def IsMasterSecLoan(ins):
    return (ins.IsKindOf(acm.FSecurityLoan) and
            ins.ProductTypeChlItem() and
            ins.ProductTypeChlItem().Name() == 'Master Security Loan')


def TimeToExpiration(trade, _timer=None):
    validityTime = trade.AddInfoValue("SBL_OrderExpiryTime")
    if validityTime:
        timeNow = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
        return max(int(validityTime - timeNow), 0)


def TradesFromObject(obj):
    # Returns all returnable security loan trades for the passed sheet object
    if IsFObject(obj, acm.FCollection):
        trades = (TradesFromObject(o) for o in obj)
        return {t for t in itertools.chain.from_iterable(trades) if t}
    elif IsFObject(obj, acm.FTrade) and IsFObject(obj.Instrument(), acm.FSecurityLoan):
        # counterparty = FSecLendHooks.ClientCounterparty(acm.User())
        # if FSecLendHooks.IsValidForReturn(obj, counterparty):
        return [obj]
    elif IsFObject(obj, acm.FTradeRow):
        return TradesFromObject(obj.Trade())
    elif IsFObject(obj, acm.FSecurityLoan):
        return TradesFromObject(obj.Trades())
    elif IsFObject(obj, acm.FInstrument):
        return TradesFromObject(GetSecurityLoanInstances(obj))
    elif IsFObject(obj, acm.FTreeSpecification):
        trades = TradesFromObject(obj.Constraints()) if obj.Constraints() else []
        return trades or TradesFromObject(obj.OriginObject())
    elif IsFObject(obj, acm.FTreeConstraints):
        return (TradesFromObject(obj.ConstraintSourceObject()) or
                TradesFromObject(obj.ConstraintDenominatorObject()) or
                TradesFromObject(obj.FlatValues().Last()) if obj.FlatValues() else [])
    return []


# ----------------------------------------------------------------------------------------------
#  Averaging function for distribued calculations

def AverageRateAggregation(subResults, includePositive, includeNegative):
    try:
        if subResults.Size() == 0:
            return None
        totalSize = 0.0
        totalWeightedRate = 0.0
        for subResult in subResults:
            pairOrPairs = subResult.At('result')
            if pairOrPairs is None:
                return None
            for pair in acm.GetFunction('arrayAny', 1)(pairOrPairs):
                if isinstance(pair, acm._pyClass("FPair")):
                    try:
                        rate = float(pair.First())
                        posSize = float(pair.Second())
                    except:
                        continue
                    if posSize > 0 and includePositive:
                        totalWeightedRate += rate * abs(posSize)
                        totalSize += abs(posSize)
                    elif posSize < 0 and includeNegative:
                        totalWeightedRate += rate * abs(posSize)
                        totalSize += abs(posSize)
        return totalWeightedRate / totalSize if totalSize != 0.0 else None
    except StandardError as e:
        return str(e)


# ----------------------------------------------------------------------------------------------
#  Workbench helper functions

def AddQueryAttrNodeList(query, attr, values, notNode = False):
    values = list(values)
    if query and values:
        node = query.AddOpNode('OR')
        node.Not(notNode)
        for value in itertools.islice(values, 50):
            node.AddAttrNode(attr, 'EQUAL', value)
        return query


def ColumnValuesFromExtensionattribute(FObject, ext_name, sheet='FTradeSheet'):
    # Returns a dictionery: ColId -> Value

    ext = acm.GetDefaultContext().GetExtension('FExtensionAttribute', sheet, ext_name)
    if not ext:
        return {"Error": "Missing FExtensionAttribute {0} for {1}".format(ext_name, sheet)}

    extensionValue = str(ext.Value()).split('"')[1]
    resultDict = {}
    calcSpace = acm.FCalculationSpace(sheet)
    for c in extensionValue.split('.'):
        columnId = c.strip('; ')
        calc = calcSpace.CreateCalculation(FObject, columnId)
        try:
            resultDict[columnId] = calc.FormattedValue()
        except RuntimeError:
            resultDict[columnId] = "#"

    return resultDict


# ----------------------------------------------------------------------------------------------
#  Inventory view helper class/functions

ASK_VOLUME_BIT = 3


def hasAskVolume(price):
    return bool(price.Bits() & (1 << ASK_VOLUME_BIT))


# ----------------------------------------------------------------------------------------------
#  Column dependent on query helper class/functions
def CreatePortfolioOfQuery(query):
    asqlPortfolio = acm.FASQLPortfolio(query)
    return asqlPortfolio


# ----------------------------------------------------------------------------------------------
#  Parameters

def GetDefaultPortfolioForExternalAvailability():
    """The default portfolio that represents the external availability."""
    return acm.FPhysicalPortfolio[_SETTINGS.ExternalAvailabilityDefaultPortfolio()]


def GetAvailabilityCompoundPortfolio():
    """The compound portfolio that represents the availability (Internal+Trading)."""
    return acm.FPhysicalPortfolio[_SETTINGS.AvailabilityCompoundPortfolio()]


def GetDefaultPortfolioForInternalAvailability():
    """The default portfolio that represents the internal availability."""
    return acm.FPhysicalPortfolio[_SETTINGS.InternalAvailabilityDefaultPortfolio()]


# ----------------------------------------------------------------------------------------------
#  Helper functions for portfolio pricing
def CreatePortfolioPricingLoan(underlying, startDate, endDate, fee):
    secLoan = SecurityLoanCreator.CreateInstrument(underlying=underlying,
                                                   legStartDate=startDate,
                                                   legEndDate=endDate,
                                                   openEnd="None",
                                                   generateSpreadFixings=False)
    leg = secLoan.FirstFixedLeg()
    leg.FixedRate = fee;
    secLoan.ExpiryDate = secLoan.EndDate()
    leg.GenerateCashFlows(0.0)
    return secLoan


# ----------------------------------------------------------------------------------------------
#  Helper function for column Security Loan Theoretical Profit And Loss

def ReplaceNumericValueWithSuggestedFee(dv, valuationdate, suggestedFee):
    try:
        if dv:
            if acm.Time.DateDifference(dv.DateTime(), valuationdate) >= 0:
                return acm.GetFunction('replaceNumericValue', 2)(dv, suggestedFee)
            return dv
    except Exception as e:
        return acm.Math.NotANumber()


# ----------------------------------------------------------------------------------------------
#  Helper function to check if EnableShowDropDonOnKeyDown is published in the current build.

def IsShowDropDownKey():
    if acm.FUxControl.GetMethod('EnableShowDropDownOnKeyDown', 1):
        return True
    else:
        return False


# ----------------------------------------------------------------------------------------------
#  Helper function to get counterparties. Used in Client View.

def getCounterparties():
    partyQry = acm.CreateFASQLQuery('FParty', 'AND')
    partyQry.AddAttrNodeBool('NotTrading', False)
    typeNode = partyQry.AddOpNode('OR')
    typeNode.AddAttrNode('Type', 'EQUAL', 'Counterparty')
    typeNode.AddAttrNode('Type', 'EQUAL', 'Client')
    parties = partyQry.Select()
    return parties


def getTradeTooltip(_validity_attr, _toolTipfieldSize = None):
    trade_tooltip = ""
    exceeds_length = False
    for attr in _validity_attr:
        if not _validity_attr[attr]:
            new_tooltip = trade_tooltip + '{} missing\n'.format(attr)
            if _toolTipfieldSize is None or len(new_tooltip) < (_toolTipfieldSize - 4):
                trade_tooltip = new_tooltip
            else:
                exceeds_length = True
    if exceeds_length:
        trade_tooltip += "..."
    return trade_tooltip

# ----------------------------------------------------------------------------------------------
#  Provider class for ASQL portfolios. Send in a query and a query folder to GetOrCreateFromQuery

class ASQLPortfolioProvider(object):

    cache = dict()

    def GetOrCreateFromQuery(self, queryOrQueryFolder):
        key = self._Hash(queryOrQueryFolder)
        portfolio = self.cache.get(key, None)
        if portfolio is None:
            portfolio = self.CreateFromQuery(queryOrQueryFolder, key)
        return portfolio

    def CreateFromQuery(self, queryOrQueryFolder, key):
        portfolio = acm.FASQLPortfolio(queryOrQueryFolder)
        self.cache[key] = portfolio
        return portfolio

    @classmethod
    def _Hash(cls, obj):
        if type(obj) is acm._pyClass("FASQLQueryFolder"):
            return cls._Hash(obj.AsqlQuery()) + obj.Name()
        elif type(obj) is acm._pyClass("FASQLQuery"):
            queryResult = obj.Select_Triggered()
            return ''.join(str(s.SQL()) for s in queryResult.SubResults())
        else:
            return obj


def GetAvailabilityQueryPortfolio(portfolioName, instrumentName):
    query = ActiveLoansBaseQuery()
    portNode = query.AddOpNode('OR')
    portNode.AddAttrNode('Portfolio.Name', 'EQUAL', portfolioName)
    undNode = query.AddOpNode('OR')
    undNode.AddAttrNode('Instrument.Underlying.Name', 'EQUAL', instrumentName)
    queryFolder = acm.FASQLQueryFolder()
    queryFolder.Name = instrumentName
    queryFolder.AsqlQuery = query
    return ASQLPortfolioProvider().GetOrCreateFromQuery(queryFolder)
    
def GetAvailabilityRowObject(portfolioName, instrumentName):
    queryFolder = GetAvailabilityQueryPortfolio(portfolioName, instrumentName)
    treeSpec = TreeSpecificationForObject(queryFolder)
    treeSpec.Grouper(acm.FUnderlyingGrouper())

    cs = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    cs.InsertItem(treeSpec)
    cs.Refresh()
    return cs.RowTreeIterator().FirstChild().Tree().Item()


# ----------------------------------------------------------------------------------------------
#  An information dialog

class InformationDialog(FUxCore.LayoutDialog):
    def __init__(self, caption, text, width, height):
        self.m_caption = caption
        self.m_text = text
        self.m_width = width
        self.m_height = height
        self.m_fuxDlg = None
        self.m_okBtn = None
        self.m_textBox = None
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_okBtn = layout.GetControl("ok")
        self.m_textBox = layout.GetControl("textBox")
        
        self.m_textBox.Editable(False)
        self.m_textBox.SetData(self.m_text)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddText('textBox', self.m_width, self.m_height, -1, -1)   
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.  EndBox()
        b.EndBox()
        return b

