""" Compiled: 2017-11-06 12:31:15 """

#__src_file__ = "extensions/ConvertiblePricingAndRisk/etc/FDeltaNukeUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FDeltaNukeUtils -

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from FAMValuationUtils import FXRateValueFromInstrument
from FExerciseEventFunctions import ValidMandatoryConversionEventsSorted
from FLogger import FLogger
from math import isnan

SAVE_NUKE_PARAMS_IN_PRICE_ENTRY = 'SaveNukeParamsInPriceEntry'
logger = FLogger('DeltaNuke')


def IsNaN(value):
    if type(value) == float:
        if isnan(value):
            return True
    return False
        
def SaveNukeParametersInPriceEntrySetting():
    context = acm.GetDefaultContext()
    qS = [ext for ext in context.GetAllExtensions('FParameters', 'FObject', True, True) if ext.StringKey() == SAVE_NUKE_PARAMS_IN_PRICE_ENTRY]
    try:
        val = bool(str(qS[0].AtString('Enabled')).strip() == 'True')
    except Exception:
        val = True
        logger.error('Could not interpret value for the global quote setting %s. Proceeding using default value "%s"' % (SAVE_NUKE_PARAMS_IN_PRICE_ENTRY, val))
    return val        


class DeltaNukeUtils(object):

    NUKE_MARKET_NAME                = "deltaNukeMarket"
    BASE_BID_PRICE                  = "Delta Nuke Base Bid Price"
    BASE_ASK_PRICE                  = "Delta Nuke Base Ask Price"
    BASE_FX_RATE                    = "Delta Nuke Base Fx Rate"
    BASE_UND_PRICE                  = "Delta Nuke Base Underlying Price"
    BASE_DELTA                      = "Delta Nuke Base Delta"
    FALLBACK_DELTA                  = "Delta Nuke Fallback Delta"

    @staticmethod
    def nukeMarket():
        extensionContext = acm.GetDefaultContext()
        nukeMarketName = DeltaNukeUtils.NUKE_MARKET_NAME
        try:
            marketName = [ext for ext in extensionContext.GetAllExtensions('FExtensionValue', 'FObject', True, True, '', '', False)
                           if ext.StringKey() == nukeMarketName][0].Value()
        except Exception:
            logger.ELOG("Unable to find nuke market %s\n" % nukeMarketName)
            return None
        else:   
            return acm.FMarketPlace[marketName]

    @staticmethod
    def matchingInstrumentPrice(prices, market, currency, day = None):
        for price in prices:
            if (price.Market() == market) and (price.Currency() == currency) and (None == day or price.Day() == day):
                return price
        return None
        
    @staticmethod
    def getNukePrice(instrument):
        nukeMarket = DeltaNukeUtils.nukeMarket()
        foundPrice = DeltaNukeUtils.matchingInstrumentPrice(instrument.Prices(),\
                                nukeMarket, instrument.Currency())
        if foundPrice:
            price = foundPrice.Clone()
        else:
            logger.debug("Price record not found - creating new.\n")
            price = acm.FPrice()
            price.Instrument(instrument)
            price.Currency(instrument.Currency())
            price.Market(nukeMarket)
        price.Day(acm.Time.DateToday())
        return (foundPrice, price)

class SaveDeltaNukeParametersPrice(object):

    def __init__(self, data):
        if SaveNukeParametersInPriceEntrySetting():
            self._SaveParams(data)
        else:
            logger.info("FParameter %s is set to False. Nuke parameter not saved"%SAVE_NUKE_PARAMS_IN_PRICE_ENTRY)

    def _SaveParams(self, data):
        currentInstrument = None
        currentPriceRecord = None
        for (column_id, instrument, value) in data:
            if instrument.IsKindOf("FConvertible"):
                if instrument != currentInstrument:
                    if currentPriceRecord:
                        self._Save(currentPriceRecord)
                    currentInstrument = instrument
                if column_id in self.valid_keys:
                    (foundprice, newPrice) = DeltaNukeUtils.getNukePrice(instrument)
                    if foundprice:
                        currentPriceRecord = foundprice
                    else:
                        currentPriceRecord = newPrice
                    if value != None and not IsNaN(value):
                        self.valid_columns[column_id](currentPriceRecord, value)
                else:
                    continue
            else:
                logger.error("Verify that all instruments are convertibles.")
                continue
        if currentPriceRecord:
            self._Save(currentPriceRecord)

    def _Save(self, obj):
        try:
            obj.Commit()
        except Exception as e:
            logger.error('Failed to save nuke parameters. Reason: %s' % str(e))
        else:
            logger.info("Saved nuke parameter values.")
            
    def save_stock_price(priceRecord, value):
        # pylint: disable-msg=E1101,E0213
        priceRecord.Settle(value)

    def save_bid_price(priceRecord, value):
        # pylint: disable-msg=E1101,E0213    
        priceRecord.Last(value)

    def save_delta(priceRecord, value):
        # pylint: disable-msg=E1101,E0213    
        priceRecord.Low(value)

    def save_FX(priceRecord, value):
        # pylint: disable-msg=E1101,E0213   
        priceRecord.Bid(FXRateValueFromInstrument(priceRecord.Instrument(), value))

    def save_ask_price(priceRecord, value):
        # pylint: disable-msg=E1101,E0213    
        priceRecord.Ask(value)
        
    def save_fallback_delta(priceRecord, value):
        # pylint: disable-msg=E1101,E0213    
        priceRecord.High(value)

    valid_columns = {DeltaNukeUtils.BASE_UND_PRICE: save_stock_price,
                     DeltaNukeUtils.BASE_ASK_PRICE: save_ask_price,
                     DeltaNukeUtils.BASE_BID_PRICE: save_bid_price,
                     DeltaNukeUtils.BASE_DELTA: save_delta,
                     DeltaNukeUtils.BASE_FX_RATE: save_FX,
                     DeltaNukeUtils.FALLBACK_DELTA: save_fallback_delta,}

    valid_keys = valid_columns.keys()

class SelectedNukeParameter(object):

    def __call__(self):
        return self.data

    def __init__(self, cells):
        if isinstance(cells, [].__class__):
            self.data = cells
        else:
            self.data = []
            for cell in cells:
                if hasattr(cell, 'IsKindOf') and cell.IsKindOf(acm.FGridCellInfo):
                    cell_data = SelectedNukeParameter.get_cell_data(cell)
                    if cell_data:
                        evaluator = cell.Evaluator()
                        if hasattr(evaluator, 'IsSimulated') and evaluator.IsSimulated():
                            evaluator.RemoveSimulation()
                        self.data.append(cell_data)
                else:
                    raise TypeError("Attempt to extract cell data from unknown data type %s." % type(cell))

    @classmethod
    def get_cell_data(cls, cell):
        row = cell.RowObject()
        if not hasattr(row, "Instrument"):
            return
        instrument = row.Instrument().Originator()
        column_id = str(cell.Column().ColumnId())
        value = cell.Value()
        if column_id in SaveDeltaNukeParametersPrice.valid_keys:
            return column_id, instrument, value
        else:
            return


def save_nuke_params(eii):
    if eii.Parameter('sheet'):
        cells = eii.Parameter('sheet').Selection().SelectedCells()
    else:
        cells = eii.ExtensionObject().ActiveSheet().Selection().SelectedCells()
    SaveDeltaNukeParametersPrice(SelectedNukeParameter(cells)())
    
def ConvertibleIsMonisValued(convertible):
    return convertible.ValuationGrpChlItem().Name() == "Monis"
        
def ConversionRatioAdjustment(convertible):
    mandatoryEvents = ValidMandatoryConversionEventsSorted(convertible.ExerciseEvents(), acm.Time.DateValueDay(), convertible.EndDate())
    return convertible.ConversionRatio() if bool(mandatoryEvents) else 1.0
        
def ConvertibleIsUnexpired(cb):    
    return cb.IsKindOf('FConvertible') and not cb.IsExpired()

'''
To activate a button for saving nuke parameters, add FMenuExtension:
FTradingSheet:Save Nuke Parameter =
  Function=FDeltaNukeUtils.save_nuke_params
  MenuType=GridCell
  SheetProcessingMode=Local
  Standard=Yes
'''
