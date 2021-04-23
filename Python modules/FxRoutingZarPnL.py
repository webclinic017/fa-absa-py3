''''
Developer : Mighty Mkansi 
FX Non ZAR PnL Trade constallation booking module
'''
import acm
import FXUtils
from at import TP_FX_SPOT, TP_FX_FORWARD, TP_SWAP_FAR_LEG, TP_SWAP_NEAR_LEG
from at_ael_variables import AelVariableHandler
from FxPricingUtils import CalculateTradeValueDayPnL

ZarCurr = acm.FCurrency['ZAR']
calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
FX_SALES_PORTS = acm.FCompoundPortfolio['FX_SALES'].SubPortfolios()

context = acm.GetDefaultContext()
sheet_type = 'FTradeSheet'
pnl_calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type )

today = acm.Time.DateToday()

'''================================================================================================
================================================================================================'''
ael_variables = AelVariableHandler()
ael_variables.add('TrdFilter',
    label='Trade Filter',
    cls='FTradeSelection',
    mandatory=False,
    multiple=True,
    default='ZarFxPnL')

ael_variables.add('fwdPortfolio',
    label='Forward Position Portfolio',
    collection=['FLO', 'FWT', 'AGG'],
    default='FLO')

ael_variables.add('spotPortfolio',
    label='Spot Position Portfolio',
    collection=['AGG', 'RND'],
    default='AGG')

ael_variables.add('spotTradeCounterparty',
    label='Spot Position Acquirer',
    collection=['FX SPOT', 'IRD DESK'],
    default='FX SPOT')

ael_variables.add('fwdTradeCounterparty',
    label='Forward Position Acquirer',
    collection=['FX SPOT', 'IRD DESK'],
    default='IRD DESK')

'''================================================================================================
================================================================================================'''
def GetZARRate(trade, date):      
    Currency2 = trade.Currency()
    CurrencyPair = ZarCurr.CurrencyPair(Currency2)
    ZARConversionRate = Currency2.Calculation().FXRate(calc_space, ZarCurr, date)    
    return ZARConversionRate.Number()

'''================================================================================================
================================================================================================'''
def getTradesInPosition(trade): 
    ins = trade.Instrument()
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    query.AddAttrNode('GroupTrdnbr.Oid', 'EQUAL', trade.Oid())
    connectedTrades = query.Select() 
    return connectedTrades

'''================================================================================================
================================================================================================'''
def SholdCreateZarPnlTrade(original_trade):
    if original_trade.Portfolio() in FX_SALES_PORTS:
        if  'ZAR' in [original_trade.CurrencyPair().Currency1().Name(), 
                        original_trade.CurrencyPair().Currency2().Name()]:
            return False       

    return True

'''================================================================================================
================================================================================================'''
def simulateFwdPoints(trade, fwd_date, spot_date):    
    Currency2 = trade.Currency()    
    currencyPair = ZarCurr.CurrencyPair(Currency2)   
    spot_date_today = currencyPair.SpotDate(today)
                
    timeToExpiry = acm.Time.DateDifference(fwd_date, spot_date) 
    date_period = '%sd'%str(timeToExpiry)
   
    simulateDate = acm.Time.DateAdjustPeriod(spot_date_today, date_period)
  
    fx_fwd = trade.Currency().Calculation().FXRate(calc_space, ZarCurr, spot_date_today).Number()  
    fx_today = trade.Currency().Calculation().FXRate(calc_space, ZarCurr, simulateDate).Number()   
    
    return  (fx_today - fx_fwd)
    
'''================================================================================================
================================================================================================'''
def CreateZarPnLTrade(trade, valueDay, portfolio, counterparty, price, zarPnl):
    if SholdCreateZarPnlTrade(trade):        
        if valueDay < acm.Time.TimeNow():
            time = valueDay
        else:
            time = acm.Time.TimeNow()  
        Currency2 = trade.Currency()
        currencyPair = ZarCurr.CurrencyPair(Currency2)   
        newTrade = acm.FTrade()
        newTrade.RegisterInStorage()
        newTrade.TradeTime( time)
        newTrade.AcquireDay(  valueDay )
        newTrade.ValueDay ( valueDay )
        newTrade.Instrument( currencyPair.Currency1() )
        newTrade.Currency( currencyPair.Currency2() ) 
            
        if trade.IsFxSpot() == True:
            newTrade.Acquirer(trade.Acquirer())
            newTrade.TradeProcess( TP_FX_SPOT )
        else:
            newTrade.Acquirer(trade.Acquirer())
            newTrade.TradeProcess( TP_FX_FORWARD )
        
        newTrade.Counterparty(counterparty)
        newTrade.Portfolio(portfolio)
        newTrade.Trader( trade.Trader() )
        
        newTrade.Price( price )
        newTrade.ReferencePrice( price )
        newTrade.Nominal(zarPnl)
        newTrade.UpdatePremium( True )
        newTrade.MirrorPortfolio(trade.Portfolio())
         
        newTrade.Status("Internal")
        newTrade.MirrorPortfolio( trade.Portfolio())
        newTrade.SuggestBaseCurrencyEquivalent()
        newTrade.YourRef(trade.YourRef())
        newTrade.Trader(trade.Trader())
        newTrade.GroupTrdnbr(trade)    
       
        newTrade.Commit()
        mirror = newTrade.MirrorTrade()
        mirror.Trader(trade.Trader() )
        mirror.Commit()
    else:
        return
        
'''================================================================================================
================================================================================================'''
def CreateZarSwapPnLTrade(trade, spot_date, fwd_date, portfolio, counterparty, spot_price, pnl): 
    if SholdCreateZarPnlTrade(trade):
        time = acm.Time.TimeNow()            
        Currency2 = trade.Currency()        
        currency_pair = ZarCurr.CurrencyPair(Currency2)        
        forward_points  = simulateFwdPoints(trade, fwd_date, spot_date)
        far_price= spot_price + forward_points         
        #--------------------------------------------------------------------
        uniquekey = str(acm.Time.TimeOnlyMs().replace(':', ''))
        
        near = acm.FTrade()
        near.RegisterInStorage() 
        near.TradeTime(spot_date)
        near.AcquireDay(spot_date)
        near.ValueDay ( near.AcquireDay() )
        near.Instrument( currency_pair.Currency1() )
        near.Currency( currency_pair.Currency2() )
        near.Acquirer( trade.Acquirer() )
        near.Counterparty( counterparty )
        near.Portfolio( portfolio )
        near.Price(spot_price)
        near.ReferencePrice(spot_price)
        near.Quantity(pnl)
        near.UpdatePremium( True )
        near.TradeProcess( TP_SWAP_NEAR_LEG )
        near.Status("Internal")  
        near.MirrorPortfolio(trade.Portfolio())
        near.GroupTrdnbr(trade) 
        near.Trader(trade.Trader())

        #--------------------------------------------------------------------\

        far = acm.FTrade()  
        far.RegisterInStorage()
        far.TradeTime(near.TradeTime())
        far.AcquireDay(fwd_date)
        far.ValueDay( far.AcquireDay()  )
        far.Instrument( near.Instrument() )
        far.Currency( near.Currency() )
        far.Acquirer( near.Acquirer() )
        far.Counterparty( near.Counterparty() )
        far.Portfolio( near.Portfolio() )   
         
        far.Price(far_price)
        far.ReferencePrice(far_price)
        far.Quantity(-1*pnl)
        far.UpdatePremium( True )
        far.TradeProcess( TP_SWAP_FAR_LEG )
        far.Status( near.Status() )
        far.MirrorPortfolio(trade.Portfolio())
        far.GroupTrdnbr(trade) 
        far.Trader(near.Trader())
        
        #--------------------------------------------------------------------
        far.ConnectedTrade( near )
        near.FxSwapFarLeg()         
        near.ConnectedTrade(far)    
        FXUtils.CommitInTransaction([near, far])
        
        # Set trader on Mirror to be the same as the main trades
        far_mirror =far.MirrorTrade()
        far_mirror.Trader(trade.Trader())
        near_mirror = near.MirrorTrade()
        near_mirror.Trader(trade.Trader())
        
        FXUtils.CommitInTransaction([far_mirror, near_mirror])
        
        print 'Done creating a near leg {0} and far leg {1}'.format(near.Oid(), far.Oid())
    else:
        return
    
'''================================================================================================
================================================================================================'''
def ael_main(config):        
    filter_trade = config['TrdFilter'][0]
    trades = acm.FTradeSelection['filter_trade']    
    fwd_portfolio = config['fwdPortfolio']
    spot_portfolio = config['spotPortfolio']
    spot_counterparty = config['spotTradeCounterparty']
    fwd_counterparty = config['fwdTradeCounterparty']
            
    for trade in filter_trade.Trades():        
        trade_date = acm.Time.DateFromTime(trade.TradeTime())
        currencyPair = ZarCurr.CurrencyPair(trade.Currency())        
        spotPnl = CalculateTradeValueDayPnL(trade)        
     
        if trade.IsFxSwap():
            fwd_date = trade.FxSwapFarLeg().ValueDay()
        else:
            fwd_date = trade.ValueDay()
            
        if trade.IsFxSwap():
            pnl = CalculateTradeValueDayPnL(trade) + CalculateTradeValueDayPnL(trade.FxSwapFarLeg())
        else:
            pnl = CalculateTradeValueDayPnL(trade)
                                
        spot_date =  currencyPair.SpotDate(trade_date)       
        spot_price = GetZARRate(trade, spot_date)     
       
        fwd_price =GetZARRate(trade, fwd_date)             
       
        if trade.IsFxSpot():
            CreateZarPnLTrade(trade, spot_date, spot_portfolio, spot_counterparty, spot_price, spotPnl)            
        else:
            if pnl != 0:                
                CreateZarPnLTrade(trade, spot_date, spot_portfolio, spot_counterparty, spot_price, pnl)                             
                CreateZarSwapPnLTrade(trade, spot_date, fwd_date, fwd_portfolio, fwd_counterparty, spot_price, pnl)
            
          
