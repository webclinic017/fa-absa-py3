"""----------------------------------------------------------------------------------------------------------
MODULE                  :       Trades booking automation
PURPOSE                 :       Automate trade booking for the Treasury and Money Markets Desks
DEPARTMENT AND DESK     :       Money Markets
REQUESTER               :       Lucille Joseph
DEVELOPER               :       Mighty Mkansi
CR NUMBER               :       
-------------------------------------------------------------------------------------------------------------

"""

import acm
from at_logging import getLogger

LOGGER = getLogger(__name__)


businessLogicHandler = acm.FBusinessLogicGUIDefault()
curr = acm.FCurrency['ZAR']
calendar = acm.FCalendar['ZAR Johannesburg']
today =acm.Time.DateToday()

def get_brigde_trade_nominal(instrument):
    context = acm.GetDefaultContext()
    sheet_type = 'FTradeSheet'
    calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type )
    value = calc_space.CalculateValue(instrument, 'Portfolio Position' )
    return abs(value)
    
def createClientTrade(trade, float_ref, rolling_period, reset_type, mirror_trade_portfolio, internal_trade_acquirer, 
                      mirror_trade_acquirer, internal_trade_portfolio, internal_trade_spread, status):
    trade_list =[]
        
    client_trade = trade
    client_instrument = client_trade.Instrument()
   
    internal_instrument = acm.FDeposit()
    
    internal_instrument.RegisterInStorage()
    internal_instrument = acm.FInstrumentLogicDecorator(internal_instrument, businessLogicHandler)       
   
    internal_instrument.ExpiryDate(client_instrument.ExpiryDate())
    internal_instrument.DayCountMethod(client_instrument.DayCountMethod())
    internal_instrument.ValuationGrpChlItem(client_instrument.ValuationGrpChlItem())
    
    internal_instrument.Quotation(acm.FQuotation['Pct of Nominal'])
    internal_instrument.QuoteType('Pct of Nominal')
      
    internal_instrument.OpenEnd('None') 
    internal_instrument.Currency(client_instrument.Currency())
    
    reset_period_count = rolling_period[0]
    
    if rolling_period[1] == 'm':
        reset_period_unit = 'Months'
    else:
        reset_period_unit = 'Days'        
            
    leg = internal_instrument.CreateLeg(1)
    leg.LegType('Float')
    leg.RollingPeriod(client_instrument.Legs()[0].RollingPeriod())
    leg.FloatRateReference (float_ref) 
    leg.Spread(internal_trade_spread) 
    leg.DayCountMethod(client_instrument.Legs()[0].DayCountMethod())
    leg.RollingPeriodBase(client_instrument.Legs()[0].RollingPeriodBase())
    leg.StartDate(client_instrument.Legs()[0].StartDate())
    leg.EndDate(client_instrument.ExpiryDate())
    leg.ResetDayOffset(0)
    leg.ResetPeriodCount(reset_period_count)
    leg.ResetPeriodUnit(reset_period_unit)
    leg.ResetType(reset_type)
    leg.ResetDayMethod('Following')
    leg.ResetCalendar(calendar)
    leg.Rounding('Normal')
    leg.Decimals(5)
    leg.FloatRateFactor(1)
       
    try:
        internal_instrument.Commit()
        LOGGER.info('Committed %s', internal_instrument.Name())
        
    except Exception as e:
        LOGGER.exception('Could not commit instrument: %s', e)       

    internal_trade = acm.FTrade()
    internal_trade = acm.FTradeLogicDecorator(internal_trade, businessLogicHandler)
    internal_trade.RegisterInStorage()
    
    if client_instrument:
        internal_trade.Instrument(internal_instrument)
        
        if len(client_instrument.Trades()) == 1:
            nominal = abs(client_trade.Nominal())
        else:
            nominal = get_brigde_trade_nominal(client_instrument)
        
        internal_trade.Nominal(nominal)
        internal_trade.Portfolio(internal_trade_portfolio)
        internal_trade.Acquirer(internal_trade_acquirer)
        internal_trade.Currency(client_trade.Currency())
        internal_trade.Counterparty(mirror_trade_acquirer)
        internal_trade.TradeTime(client_trade.TradeTime())
        internal_trade.AcquireDay(client_trade.AcquireDay())
        internal_trade.Price(100)
        internal_trade.Trader(acm.User())
        internal_trade.Status(status)
        internal_trade.AdditionalInfo().Funding_Instype('CL')
        
        if client_instrument.Legs()[0].LegType() == 'Float':
            profit_spread = round(float(client_instrument.Legs()[0].Spread()) - float(internal_trade_spread), 2)
        else:
            profit_spread = 0.0        
                        
        try:
            acm.BeginTransaction()
            
            internal_trade.TrxTrade(trade)
            internal_trade.GroupTrdnbr(trade.Oid())
            
            if trade.Status() in ('Simulated', 'FO Confirmed'):
                trade.GroupTrdnbr(trade.Oid())
                trade.AdditionalInfo().MM_Profit_Spread(profit_spread)                
                #trade.Status('FO Confirmed')
                trade.Commit()
                
            internal_trade.MirrorPortfolio(mirror_trade_portfolio)
            internal_trade.ValueDay(client_trade.ValueDay())
            
            internal_trade.Commit()            
            internal_trade.MirrorTrade().TrxTrade(trade)            
            internal_trade.Commit()
            trade_list.append(internal_trade)
            LOGGER.info('Commited internal trades %s , %s', internal_trade.Oid(), internal_trade.MirrorTrade().Oid()) 
            acm.CommitTransaction()
                     
        except Exception as e:            
            acm.AbortTransaction()            
            raise         
                    
        mirror_trade = internal_trade.MirrorTrade()
        mirror_trade.GroupTrdnbr(trade.Oid())
        internal_trade.GroupTrdnbr(trade.Oid())
        mirror_trade.AdditionalInfo().Funding_Instype('CD')
	
        try:
            mirror_trade.Commit()
            internal_trade.Commit()
            trade_list.append(mirror_trade)
        except Exception as e:
            raise
    else:
        LOGGER.info('Could not find internal instrument')
    
    return trade_list