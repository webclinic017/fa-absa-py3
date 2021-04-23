""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ConvertibleMarketMaking/etc/FCMMSaveNukeParameters.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCMMSaveNukeParameters

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

from contextlib import contextmanager

from FAssetManagementUtils import logger
from FDeltaNukeUtils import SaveDeltaNukeParametersPrice, DeltaNukeUtils, SaveNukeParametersInPriceEntrySetting, IsNaN
from FCMMDataSourceListener import ValueInvoker


PROPOSED_BID_PRICE              = "Proposed Bid Price"
PROPOSED_ASK_PRICE              = "Proposed Ask Price"
UNDERLYING_SPOT                 = "Portfolio Underlying Future Method Price"
FX_RATE                         = "Formatted Underlying FX Rate"
CB_PARITY                       = "CB Parity"
BASE_BID_PRICE                  = "Base Bid Price"
BASE_ASK_PRICE                  = "Base Ask Price"
BASE_FX_RATE                    = "Formatted Base FX Rate"
BASE_UND_PRICE                  = "Base Und Price"
BASE_DELTA                      = "Base Delta"
FALLBACK_DELTA                  = "Delta Nuke Fallback Delta"
PARITY_BASED_QUOTING            = "Parity Based Quoting"

LIVE_COLUMNS = (PROPOSED_BID_PRICE, PROPOSED_ASK_PRICE, UNDERLYING_SPOT, FX_RATE, FALLBACK_DELTA)

BASE_PRICE_COLUMNS = (BASE_BID_PRICE, BASE_ASK_PRICE)

NUKE_COLUMNS  = (BASE_BID_PRICE, BASE_ASK_PRICE, BASE_UND_PRICE, \
                 BASE_FX_RATE, BASE_DELTA)
                 
PROPOSED_QUOTE_COLUMNS = (PROPOSED_BID_PRICE, PROPOSED_ASK_PRICE)

PARITY_COLUMNS = (PARITY_BASED_QUOTING, CB_PARITY)

REBASE_COLUMNS  = LIVE_COLUMNS + PARITY_COLUMNS


DELTA_NUKE_MAP = {BASE_BID_PRICE: DeltaNukeUtils.BASE_BID_PRICE, \
                BASE_ASK_PRICE: DeltaNukeUtils.BASE_ASK_PRICE, \
                BASE_UND_PRICE: DeltaNukeUtils.BASE_UND_PRICE, \
                BASE_FX_RATE: DeltaNukeUtils.BASE_FX_RATE, \
                BASE_DELTA: DeltaNukeUtils.BASE_DELTA}


def RowObject(eii):
    button = eii.Parameter("ClickedButton")
    rowObject = button.RowObject() if button and button.RowObject().IsKindOf('FQuoteLevelRow') else None
    return rowObject

''' Save Quote Settings '''

@contextmanager
def SwitchSaveQuoteParameter(dataSpace, newVal):
    dataSource = dataSpace.GetDataSource('Save Quote Parameter', 0)
    old_val = dataSource.Get()
    dataSource.Set(newVal)
    yield
    dataSource.Set(old_val)
    
class QuoteParametersHandler(object):
    
    def __init__(self, quoteController):
        self._quoteController = quoteController
    
    def QuoteController(self):
        return self._quoteController
    
    def OrderBook(self):
        return self.QuoteController().OrderBook()
    
    def SaveQuoteSettings(self):
        dataSpace = self.QuoteController().DataSpace()
        with SwitchSaveQuoteParameter(dataSpace, True):
            logger.info("Saving settings for orderbook: %s" % self.OrderBook().Name())
        return 

''' Save Nuke parameters '''

def FilteredRowObject(rowObject):
    return rowObject if rowObject.IsKindOf('FQuoteLevelRow') else None
    
def FilteredRowObjects(eii):
    return filter(FilteredRowObject, eii.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects().AsList())

def SaveNukeParameters(eii):
    rowObjects = FilteredRowObjects(eii) 
    saveNukeParamsInPriceEntry = SaveNukeParametersInPriceEntrySetting()
    for rowObject in rowObjects:
        SaveNukeParametersAsynchronous(rowObject, NUKE_COLUMNS, saveNukeParamsInPriceEntry)

class NukeParameterHandler(object):

    def __init__(self, rowObject, readColumns):
        self.rowObject = rowObject
        self.quoteController = rowObject.QuoteController()
        ValueInvoker(self.quoteController, readColumns, self.AsynchCallBack)
        
    def RowObject(self):
        return self.rowObject
        
    def Instrument(self):
        return self.OrderBook().Instrument()
    
    def OrderBook(self):
        return self.quoteController.OrderBook()
        
    def GetValue(self, values, key):
        return values.get(key)

    def UseDeltaNukePriceEntry(self):
        raise NotImplementedError
        
    def DeltaNukeColumnId(self, quoteColumn):
        return DELTA_NUKE_MAP.get(quoteColumn)
        
    def DataSourceAt(self, col_id):
        return self.quoteController.DataSpace().GetDataSource(col_id, 0)
        
    def AsynchCallBack(self, values):
        raise NotImplementedError

    def CreateSaveNukeParameterInput(self, column_id, value):
        return (self.DeltaNukeColumnId(column_id), self.Instrument(), value)  
   
class SaveNukeParametersAsynchronous(NukeParameterHandler):

    def __init__(self, rowObject, columns, saveNukeParamsInPriceEntry):
        self._saveNukeParamsInPriceEntry = saveNukeParamsInPriceEntry        
        NukeParameterHandler.__init__(self, rowObject, columns)
        
    def AsynchCallBack(self, values):
        QuoteParametersHandler(self.quoteController).SaveQuoteSettings()
        if self.UseDeltaNukePriceEntry():
            SaveDeltaNukeParametersPrice(self.SaveNukeParametersInput(values))
            logger.info("Saving nuke parameters for instrument: %s in price table succeeded" % self.RowObject().Instrument().Name())            
            
    def UseDeltaNukePriceEntry(self):
        return self._saveNukeParamsInPriceEntry        
        
    def SaveNukeParametersInput(self, values):
        return [self.CreateSaveNukeParameterInput(key, values[key]) for key in values]
        
''' Rebase nuke'''

def RebaseDeltaNuke(eii):
    rowObject = RowObject(eii)
    saveNukeParamsInPriceEntry = SaveNukeParametersInPriceEntrySetting()
    if rowObject:
        RebaseNukeParametersAsynchronous(rowObject, REBASE_COLUMNS, saveNukeParamsInPriceEntry)

class RebaseNukeParametersAsynchronous(NukeParameterHandler):

    def __init__(self, rowObject, columns, saveNukeParamsInPriceEntry):
        self._saveNukeParamsInPriceEntry = saveNukeParamsInPriceEntry        
        NukeParameterHandler.__init__(self, rowObject, columns)
    
    def AsynchCallBack(self, values):
        rebaseValues = self.RebasedValues(values)
        QuoteParametersHandler(self.quoteController).SaveQuoteSettings()
        self.UnsimulateProposedQuotes()
        if self.UseDeltaNukePriceEntry():
            SaveDeltaNukeParametersPrice(rebaseValues)
   
    def GetLiveValues(self, values):
        return [self.GetValue(values, col_id) for col_id in LIVE_COLUMNS]
        
    def UseDeltaNukePriceEntry(self):
        return self._saveNukeParamsInPriceEntry        
         
    def RebasedValues(self, values):
        live_values = self.GetLiveValues(values)
        base_values_dict = {NUKE_COLUMNS[i]: live_values[i] for i in range(len(NUKE_COLUMNS)) if live_values[i]}
        return self._SetAndReturnRebasedValues(base_values_dict)
        
    def _SetAndReturnRebasedValues(self, val_dict):
        base_values = []
        for key in val_dict.keys():
            val = val_dict[key]
            self.DataSourceAt(key).Set( val )
            base_values.append( self.CreateSaveNukeParameterInput(key, val) )
        return base_values
        
    def UnsimulateProposedQuotes(self):
        for col_id in PROPOSED_QUOTE_COLUMNS:
            self.DataSourceAt(col_id).Set("")

''' Tick prices '''

def TickBasePrices(eii, up):
    rowObject = RowObject(eii)
    saveNukeParamsInPriceEntry = SaveNukeParametersInPriceEntrySetting()
    if rowObject:
        TickBasePricesAsynchronous(rowObject, up, BASE_PRICE_COLUMNS, saveNukeParamsInPriceEntry)
            
def TickProposedQuotePrice(eii, quoteSide, up):
    rowObject = RowObject(eii)
    if rowObject:
        TickProposedBidOrAskPriceAsynchronous(rowObject, quoteSide, up, PROPOSED_QUOTE_COLUMNS)

class TickPricesBase(NukeParameterHandler):

    def __init__(self, rowObject, up, columns):
        self._up = up
        NukeParameterHandler.__init__(self, rowObject, columns)

    def GetTickedValue(self, value):
        tickList=self.OrderBook().TickSizeList()
        if not tickList:
            raise StandardError('Orderbook %s has no tick list.' % self.OrderBook().Name())
        tickSize=tickList.TickSizeAt(value)
        if self._up:
            newVal = value + tickSize
        else:
            newVal = value - tickSize
        return newVal

class TickBasePricesAsynchronous(TickPricesBase):

    def __init__(self, rowObject, up, columns, saveQuoteSettingsInPriceEntry):
        self._saveNukeParamsInPriceEntry = saveQuoteSettingsInPriceEntry        
        TickPricesBase.__init__(self, rowObject, up, columns)

    def TickBasePrice(self, col_id, value):
        newVal = self.GetTickedValue(value)
        self.DataSourceAt(col_id).Set(newVal)
        return self.CreateSaveNukeParameterInput(col_id, newVal)
    
    def TickQuoteSettings(self, values):
        return [self.TickBasePrice(col_id, self.GetValue(values, col_id)) for col_id in values]
        
    def UseDeltaNukePriceEntry(self):
        return self._saveNukeParamsInPriceEntry        
    
    def AsynchCallBack(self, values):
        base_values = self.TickQuoteSettings(values)
        QuoteParametersHandler(self.quoteController).SaveQuoteSettings()
        if self.UseDeltaNukePriceEntry():
            SaveDeltaNukeParametersPrice(base_values)
    
class TickProposedBidOrAskPriceAsynchronous(TickPricesBase):

    def __init__(self, rowObject, quoteSide, up, columns):
        self._quoteSide = quoteSide
        TickPricesBase.__init__(self, rowObject, up, columns)
        
    def QuoteSide(self):
        return self._quoteSide
        
    def AsynchCallBack(self, values):
        target = PROPOSED_BID_PRICE if self.QuoteSide() == 'Bid' else PROPOSED_ASK_PRICE
        value = self.GetTickedValue(self.GetValue(values, target))
        self.DataSourceAt(target).Set(value)


''' Input hooks '''

def SetBaseFXRate(rowObj, column, calc, value, action):
    quoteController = rowObj.QuoteController()
    dataSpace = quoteController.DataSpace()
    base_fx = dataSpace.GetDataSource("Base FX Rate", 0)
    if str(action) == 'insert':
        base_fx_unformatted = dataSpace.GetDataSource("Unformatted Base FX Rate", 0)
        base_fx.Set( base_fx_unformatted.Get() )
    elif str(action) == 'remove':
        base_fx.Set("")
    return 0

def SetSpreadBiasFactor(rowObj, column, calc, value, action):
    quoteController = rowObj.QuoteController()
    dataSpace = quoteController.DataSpace()
    spreadBiasFactor = dataSpace.GetDataSource('Spread Bias Factor', 0)
    if value == 'Bid': 
        spreadBiasFactor.Set(0.0)
    elif value == 'Bid/Ask': 
        spreadBiasFactor.Set(0.5)
    elif value == 'Ask': 
        spreadBiasFactor.Set(1.0)
    return 0

def SetNukeSpreadSettings(rowObj, column, calc, value, action):
    quoteController = rowObj.QuoteController()
    dataSpace = quoteController.DataSpace()
    absSpread = dataSpace.GetDataSource('Absolute Spread', 0)
    spreadBiasFactor = dataSpace.GetDataSource('Spread Bias Factor', 0)
    newSpread = 0.0
    if value == 'Vega Nuke':
        baseBid = dataSpace.GetDataSource('Base Bid Price', 0)
        baseAsk = dataSpace.GetDataSource('Base Ask Price', 0)
        newSpread = baseAsk.Get() - baseBid.Get() 
    spreadBiasFactor.Set( 0.5 )
    if not IsNaN(newSpread):
        absSpread.Set( newSpread )
    return 0

