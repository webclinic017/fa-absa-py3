import acm
import ael
import datetime
context = acm.GetDefaultContext()

column_id = 'Instrument Delta'

tag = acm.CreateEBTag() 
calc_space_tradesheet = acm.Calculations().CreateCalculationSpace( context, 'FTradeSheet' )
calc_space_orderbook  = acm.Calculations().CreateCalculationSpace( context, 'FOrderBookSheet' )    
calc_space_sheet = acm.Calculations().CreateCalculationSpace(context, 'FMoneyFlowSheet')
calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def _optionDela(ins):
   
#get raw value
    value = calc_space_orderbook.CalculateValue( ins, column_id )
    return value.Value().Number() #--> NaNSEK@"2009-04-22 22:00:00"
    
def _insValEnd(trade):
    value = calc_space_tradesheet.CalculateValue( trade, 'InsValEnd' )
    return value.Value().Number() 
    
def _estimatedValue(reset):
    value = calc_space_sheet.CalculateValue( reset, 'Cash Analysis Pay Day' )
    return value.Value().Number()
    
def _hybridNominalPosition(cashflow):     
    value = acm.GetCalculatedValueFromString(cashflow, 'Standard', 'nominalPositionNoTrade', tag)     
    try:
        value.Value().Number()
    except Exception, e:
        print 'err', e
   
    return value.Value().Number()
    
def _hybridPrice(cashflow):     
    value = acm.GetCalculatedValueFromString(cashflow, 'Standard', 'hybridPrice', tag)     
    try:
        return value.Value().Number()
    except Exception, e:
        return value.Value()

def _convertTodDays(period):
    days = 0
    if period == 'Months':
        days = 30
    if period == 'Days':
        days = 1
    if period == 'Years':
        days = 365
    
    return days
    
      
def date_from_timestamp(integer):
    ''' To the datetime is an integer value, use python to convert to string '''
    isodate = integer
    
    
    if isinstance(integer, str):
        isodate = datetime.datetime.strptime(integer, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
    
    else:
        isodate = datetime.datetime.fromtimestamp(integer).strftime('%Y%m%d')
       
    return isodate

def maturitydate_from_timestamp(integer):
    ''' To the datetime is an integer value, use python to convert to string '''
    isodate = integer
    isodate = datetime.datetime.strptime(integer, '%Y-%m-%d').strftime('%Y%m%d')
    return isodate
    
                
def get_trades_data():

    #user = 0, forces the query to pick up the shared query folder.
    
    
    queryName='EAGLE_Option'
    storedQuery = acm.FStoredASQLQuery.Select('user = 0 name="%s"' % queryName)[0]     
    all_trades1 = storedQuery.Query().Select()
    
      
    queryName = 'EAGLE_FutureForward'
    storedQuery = acm.FStoredASQLQuery.Select('user = 0 name="%s"' % queryName)[0]     
    all_trades2 = storedQuery.Query().Select()
    
    queryName='EAGLE_PriceSwap'
    storedQuery = acm.FStoredASQLQuery.Select('user = 0 name="%s"' % queryName)[0]     
    all_trades3= storedQuery.Query().Select()
    
    queryName='EAGLE_Currency'
    storedQuery = acm.FStoredASQLQuery.Select('user = 0 name="%s"' % queryName)[0]     
    all_trades4 = storedQuery.Query().Select()
    
    

    all_trades = all_trades1.AddAll(all_trades2).AddAll(all_trades3).AddAll(all_trades4)

    

    return all_trades
        
    
    
def _LegPresentValue(leg, trade):
    pv = 0
    try:
        result = leg.Calculation().PresentValue(calc_space, trade)
        pv = result.Value().Number()
    except Exception, e:
        print 'Error on trade %i : %s' %(trade.Oid(), str(e))

    return pv
    
def _TradePresentValue(trade):
    tr = int(trade.Oid())
    t  = ael.Trade[int(tr)]
    value = t.present_value()
    return value   


