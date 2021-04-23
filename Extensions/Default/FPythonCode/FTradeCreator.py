""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FTradeCreator.py"
"""--------------------------------------------------------------------------
MODULE
    FTradeCreator

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Trade creators and quantity calculator and convenience methods
-----------------------------------------------------------------------------"""

import acm
import math
import FSheetUtils
from FAssetManagementUtils import GetLogger

SPACE_COLLECTION = acm.Calculations().CreateCalculationSpaceCollection()

def GetCalcSpace(sheet):
    return SPACE_COLLECTION.GetSpace(sheet, acm.GetDefaultContext())

class TradeCreator(object):
       
    def __init__(self, inputDict):   
        self.inputDict = inputDict
               
    def CreateTrade(self):
        trade = acm.FTrade()
        self.SetProperties(trade, self.inputDict)
        return trade
    
    @staticmethod
    def SetProperties(trade, inputDict):
        for name, value in inputDict.iteritems():
            if 'AdditionalInfo' in name:
                name = name.split('.')[1]
                try:
                    setattr(trade.AdditionalInfo(), name, value)
                except (AttributeError, TypeError) as e:
                    GetLogger().debug(e)
            else:
                if 'OptKey' in name:
                    name, value = GetTradeKey(name, value)
                try:
                    setattr(trade, name, value)
                except (AttributeError, TypeError) as e:
                    GetLogger().debug(e)

class DecoratedTradeCreator(TradeCreator):

    PRICE_COLUMN_ID = 'Suggested Mark-to-Market Price'

    def CreateTrade(self):
        tradeDecorator = acm.FBusinessLogicDecorator.WrapObject(acm.FTrade())
        self._SetDefaultValues(tradeDecorator)
        self.SetProperties(tradeDecorator, self.inputDict)
        return tradeDecorator.DecoratedObject()

    def _SetDefaultValues(self, trade):
        # When using acm.DealCapturing.CreateNewTrade() simulating the trade does not work 
        trade.Instrument(self.inputDict['Instrument'])
        trade.Currency(trade.Instrument().Currency())
        trade.Status('Simulated')
        trade.Trader(acm.User())
        trade.TradeTime(acm.Time.TimeNow())
        if 'Price' not in self.inputDict:
            trade.Price(self.Price(trade.Instrument()))

    @classmethod
    def Price(cls, instrument, priceColumn=PRICE_COLUMN_ID):
        try:
            space = GetCalcSpace('FDealSheet')
            price = float(space.CalculateValue(instrument, priceColumn))
            if math.isnan(price):
                raise Exception
            return price
        except Exception:
            MSG = ('No valid price found for instrument {0}. '
                   'Trade price will not be set.'.format(instrument.Name()))
            GetLogger().warn(MSG)

class TradeFromTMPositionCreator(DecoratedTradeCreator):
    
    def __init__(self, positionObj, instrument=None):
        self._instrument = instrument
        self._positionObj = positionObj
        inputDict = self._CreateInputDict()
        super(TradeFromTMPositionCreator, self).__init__(inputDict)
        
    def _CreateInputDict(self):
        inputDict = dict()
        self._AddInstrument(inputDict)
        self._AddPortfolio(inputDict)
        self._AddProperties(inputDict)
        return inputDict
    
    @classmethod
    def PortfolioFromTop(cls, positionObj):
        raise NotImplementedError
        
    @classmethod
    def Portfolio(cls, positionObj):
        raise NotImplementedError
        
    @classmethod
    def Instrument(cls, positionObj):
        raise NotImplementedError
    
    def _AddInstrument(self, inputDict):
        inputDict['Instrument'] = self._instrument or self.Instrument(self._positionObj)
    
    def _AddPortfolio(self, inputDict):
        inputDict['Portfolio'] = self.Portfolio(self._positionObj)
        
    def _AddProperties(self, inputDict):
        for prop, value in self.PropertiesFromGrouper(self._positionObj) or []:
            inputDict[prop] = value
    
    @staticmethod
    def _PortfolioFromFilter(aFilter):
        for _op, _lb, field, _cond, value, _rb in aFilter.FilterCondition():
            if str(field) == 'Portfolio':
                return acm.FPhysicalPortfolio[str(value)]
                
    @classmethod
    def _PortfolioFromQuery(cls, portfolio):
        query = portfolio.QueryCopy()
        if query:
            portfolios = []
            for attr, value in cls._AsqlAttrsAndValues(query):
                if str(attr) == 'Portfolio.Name':
                    portfolios.append(value)
            if len(portfolios) == 1: #Only one portfolio in query
                try:
                    return acm.FPhysicalPortfolio.Select01(
                            'name like {0}'.format(portfolios[0]), '')
                except Exception:
                    pass
    
    @classmethod
    def _PhysicalPortfolio(cls, portfolio):
        if portfolio.IsKindOf(acm.FASQLPortfolio):
            return cls._PortfolioFromQuery(portfolio)
        elif portfolio.IsKindOf(acm.FTradeSelection):
            return cls._PortfolioFromFilter(portfolio)
        elif portfolio.IsKindOf(acm.FPhysicalPortfolio) and not portfolio.IsKindOf(acm.FCompoundPortfolio):
            return portfolio
        else:
            GetLogger().debug('No valid physical portfolio found for {0}.'.format(portfolio.StringKey()))
    
    @staticmethod
    def _GrouperList(grouper):
        try:
            groupers = []
            if grouper and grouper.IsKindOf(acm.FChainedGrouper):
                for grp in grouper.Groupers():
                    groupers.append(grp)
            else:
                groupers.append(grouper)
            return [grp for grp in groupers if not grp.IsKindOf(acm.FSubportfolioGrouper)]
        except AttributeError:
            pass
    
    @classmethod
    def _PropertiesFromGrouper(cls, grouper, groupingValues):
        try:
            groupers = cls._GrouperList(grouper)
            if groupingValues:
                for i, groupingValue in enumerate(groupingValues):
                    propertyName = cls._Property(groupers[i])
                    yield propertyName, groupingValue
        except (AttributeError, IndexError) as e:
            GetLogger().debug(e)
    
    @staticmethod
    def _Property(grouper):
        PREFIX = 'Trade.'
        if grouper.IsKindOf(acm.FAttributeGrouper):
            method = grouper.Method().AsString()
            if PREFIX in method:
                try:
                    _none, propertyName = method.split(PREFIX)
                    return propertyName
                except ValueError:
                    pass
        return str(grouper.Label() or grouper.DisplayName())

    @staticmethod
    def _AsqlAttrsAndValues(query):
        def GetNodes(node, nodes=None):
            nodes = [] if nodes is None else nodes
            if hasattr(node, 'AsqlNodes') and node.AsqlNodes():
                for n in node.AsqlNodes():
                    GetNodes(n, nodes)
            if node and node.IsKindOf(acm.FASQLNode):
                nodes.append(node)
            return nodes
        attributeNodes = (n for n in GetNodes(query) if
                          n.IsKindOf(acm.FASQLAttrNode))
        for node in attributeNodes:
            yield (node.AsqlAttribute().AttributeString(), node.AsqlValue())
    
class TradeFromTreeSpecCreator(TradeFromTMPositionCreator):

    def __init__(self, treeSpec, instrument=None):
        super(TradeFromTreeSpecCreator, self).__init__(treeSpec, instrument)
    
    @classmethod
    def PortfolioFromTop(cls, treeSpec):
        return cls._PhysicalPortfolio(treeSpec.OriginObject())

    @classmethod
    def Portfolio(cls, treeSpec):
        return cls.PortfolioFromTop(treeSpec) or cls.PropertyFromGrouper(treeSpec, 'Portfolio')
    
    @classmethod
    def PropertyFromGrouper(cls, treeSpec, property):
        for prop, value in cls.PropertiesFromGrouper(treeSpec):
            if prop == property:
                return value
    
    @classmethod
    def PropertiesFromGrouper(cls, treeSpec):
        if treeSpec.Constraints():
            groupingValues = treeSpec.Constraints().FlatValues()
            grouper = treeSpec.Grouper()
            return cls._PropertiesFromGrouper(grouper, groupingValues)
        else:
            return []
        
    @classmethod
    def Instrument(cls, treeSpec):
        return treeSpec.Constraints().ConstraintDenominatorObject()
    
class FXTradeFromTreeSpecCreator(TradeFromTreeSpecCreator):
    
    SPOTPROCESS_BIT = 4096
    FORWARDPROCESS_BIT = 8192
    
    def __init__(self, treeSpec, instrument=None):
        super(FXTradeFromTreeSpecCreator, self).__init__(treeSpec, instrument)
        self._DefaultValues()
    
    def _DefaultValues(self):
        currencyPair = self.CurrencyPair()
        if currencyPair:
            date = currencyPair.SpotDate(acm.Time.DateNow())
            self.inputDict['Instrument'] = currencyPair.Currency1()
            self.inputDict['Currency'] = currencyPair.Currency2()
            self.SetValueDay(currencyPair, date)
            self.SetTradeProcess(date)
            self.SetPrice(currencyPair)
                            
    def SetValueDay(self, currencyPair, date):
        try:
            if not self.inputDict['ValueDay']:
                self.inputDict['ValueDay'] = date
        except KeyError:
            self.inputDict['ValueDay'] = date
            
    def SetTradeProcess(self, date):
        if self.inputDict['ValueDay'] > date:
            self.inputDict['TradeProcess'] = self.FORWARDPROCESS_BIT
        else:
            self.inputDict['TradeProcess'] = self.SPOTPROCESS_BIT
    
    def SetPrice(self, currencyPair):
        if 'Price' not in self.inputDict:
            curr1 = currencyPair.Currency1()
            curr2 = currencyPair.Currency2()
            fxRate = self.GetFXPrice(curr1, curr2, self.inputDict['ValueDay'])
            self.inputDict['Price'] = fxRate
        
    def CurrencyPair(self):
        denominatorObject = self._treeSpec.Constraints().ConstraintDenominatorObject()
        if denominatorObject.IsKindOf(acm.FFxRate):
            currencyPair = denominatorObject.CurrencyPair()
            return currencyPair
    
    @classmethod      
    def GetFXPrice(cls, curr1, curr2, date):
        cs = cls.CalculationSpace()
        return float(curr1.Calculation().FXRate(cs, curr2, date))
    
    @staticmethod
    def CalculationSpace():
        context = acm.GetDefaultContext()
        return acm.Calculations().CreateStandardCalculationsSpaceCollection(context)

class TradeFromRowCreator(TradeFromTMPositionCreator):

    def __init__(self, row, instrument=None):
        super(TradeFromRowCreator, self).__init__(row, instrument)
    
    @classmethod
    def PortfolioFromTop(cls, row):
        return cls._PhysicalPortfolio(row.Portfolio())

    @classmethod
    def Portfolio(cls, row):
        return cls.PortfolioFromTop(row) or cls.PropertyFromGrouper(row, 'Portfolio')
    
    @classmethod
    def PropertyFromGrouper(cls, row, property):
        for prop, value in cls.PropertiesFromGrouper(row):
            if prop == property:
                return value
    
    @classmethod
    def PropertiesFromGrouper(cls, row):
        groupingValues = row.Grouping().GroupingValues()
        grouper = FSheetUtils.TopRow(row).Grouping().Grouper()
        return cls._PropertiesFromGrouper(grouper, groupingValues)
    
    @staticmethod
    def Instrument(row):
        return row.Instrument() if hasattr(row, 'Instrument') else None
        
def GetTradeKey(name, value):
    if isinstance(value, acm._pyClass(acm.FChoiceList)):
        return name, value
    name = name.split('.')[0]
    def _getDefaultList():
        QUERY = 'list="MASTER" and name="Trade Keys"'
        tradeKeys = acm.FChoiceList.Select01(QUERY, '')
        index = int(name[-1])-1
        try:
            return tradeKeys.Choices().At(index).Name()
        except Exception:
            return tradeKeys.Choices().At(0).Name()

    def _getADMMappedList():
        QUERY = 'list="MASTER" and name="ADM Choicelist Mappings"'
        admMappedList = acm.FChoiceList.Select01(QUERY, '')
        for i, choice in enumerate(admMappedList.Choices()):
            if choice.Name().startswith('Trade.'+name.lower()):
                return admMappedList.Choices().At(i).Description()
        return _getDefaultList()

    listName = _getADMMappedList()
    try:
        query = 'list="{0}" and name="{1}"'.format(listName, value)
        return name, acm.FChoiceList.Select01(query, '')
    except Exception:
        MSG = ('Failed to get ChoiceList {0}.'.format(value))
        GetLogger().warn(MSG)    