'''----------------------------------------------------------------------------------------------------------
MODULE                  :       NOP_Calculation
PROJECT                 :       NOP Reporting
PURPOSE                 :       This module contains functions specifically for NOP.
DEPARTMENT AND DESK     :       Market Risk
REQUASTER               :       Rishaan Ramnarain
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXXXXXX
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2013-09-06      XXXXXXXXXX      Heinrich Cronje                 Initial Implementation
2017-04-19      XXXXXXXXXX      Bhavik Mistry                   underlyingRate changed to use custom ABSA 
                                                                column 'Underlying Spot OTC' - Core column 
                                                                does not return consistenly

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    get_NOP_Notional_Amount: This functions calculates the NOP Nominal amount of the trade. Currency Options trades
                            take the underlying currency rate and the underlying price into consideration.
    get_NOP_FX_TPL_DELTA_CASH: This functions calculated the FX TPL DELTA CASH. If the date is detween the expiry date
                                and the settlement date, only the Cash is returned.
'''

import acm, ael
import SAGEN_IT_TM_Column_Calculation as Utils

def get_NOP_Notional_Amount(temp, object_id, currency, date, trade_nominal, *rest):
    nop_Notional_Amount = 0
    
    try:
        date = ael.date(date)
    except:
        date = date
    
    if object_id:
        trade = acm.FTrade[object_id]
        
    if trade:
        tradeCurr = trade.Currency().Name()
        instrument = trade.Instrument()
        legs = instrument.Legs()
        
        if instrument.InsType() == 'Curr':
            nop_Notional_Amount = trade.Premium()
        
        if instrument.InsType() in ['Deposit', 'TotalReturnSwap']:
            trade_nominal = trade.Nominal()

        if len(legs) == 0:
            underlyingRate = Utils.get_TM_Column_Calculation(None, 'Default', 'FTradeSheet', trade.Oid(), 'Trade', 'Underlying Spot OTC', tradeCurr, 0, None, None)
            rateConversion = 1
            if instrument.InsType() == 'Option':
                underlyingInst = instrument.Underlying()
                if underlyingInst.InsType() == 'Curr':
                    ael_TrdCurr = ael.Instrument[tradeCurr]
                    rate = ael_TrdCurr.used_price(date, underlyingInst.Currency().Name())
                    if rate != 0:
                        rateConversion = 1/rate
            
            nop_Notional_Amount = trade_nominal * underlyingRate * rateConversion
        else:
            nop_Notional_Amount = trade_nominal

    return nop_Notional_Amount

def get_NOP_FX_TPL_DELTA_CASH(temp, sheetType, objectId, objectType, reportingCurr, vectorColumn, instype, undInstype, repDay, cash, *rest):
    context = 'Default'
    startDate = None
    endDate = None
    columnId = 'Portfolio FX Tpl Delta Cash'
    if instype == 'Option' and undInstype == 'Curr':
        if objectType == 'Trade':
            try:
                repDay = ael.date(repDay)
            except:
                repDay = repDay
                
            acmTrade = acm.FTrade[objectId]
            acmInstrument = acmTrade.Instrument()
            if ael.date(repDay) > ael.date(acmInstrument.ExpiryDate()[:10]) and ael.date(repDay) <= ael.date(acmInstrument.SettlementDate()):
                return cash
            else:
                return Utils.get_TM_Column_Calculation(temp, context, sheetType, objectId, objectType, columnId, reportingCurr, vectorColumn, startDate, endDate)
    else:
        return Utils.get_TM_Column_Calculation(temp, context, sheetType, objectId, objectType, columnId, reportingCurr, vectorColumn, startDate, endDate)

#print get_NOP_FX_TPL_DELTA_CASH(None, 'FTradeSheet', 25688267, 'Trade', 'AUD', 1, 'Option', 'Curr', ael.date('2013-07-09'), 0)
