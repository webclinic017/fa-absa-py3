import csv

import ael, acm 
import at

#       Zaakirah Kajee
#       All my Shizz

def currsym(currency):
    """Return currency symbol for given currency."""
    acmcurr = at.to_acm(currency, acm.FCurrency)
    if not acmcurr: 
        return None
    
    # If symbol is not specified return currency name
    currsym = at.addInfo.get_value(acmcurr, at.addInfoSpecEnum.CURRENCY_SYMBOL)
    return currsym or acmcurr.Name()
    

def formcurr(value, symbol = None, currency = 'ZAR'):
    """Return value formatted as currency."""
    # locale module displays negative values as 'R222,221.00-'
    if not symbol:
        symbol = currsym(currency)

    return symbol + " " + formnum(value)

def formnum(x):
    """Return number rounded to two decimal places with thousands separators."""
    y = '%.2f' %x
    sp = y.split('.')
    check = 0
    if sp[0][0] == '-':
        check = 1
        conv = sp[0][1:]
    else:
        conv =sp[0]
    l = len(conv)
    ns = ''
    x = (l%3)
    
    if l > 3:
        ind = l -3
        ns = conv[ind:l]
        while ind >= 0:
           
            if x ==0 and ind == 0:
                ns = ns + '.' + sp[1]
            else:
                ns =  conv[ind-3:ind] + ',' + ns
            
            ind -=3
        
        if x != 0:
            
            ns = conv[0:x] + ns + '.' + sp[1]
            
        if check ==1:
            ns = '-' + ns
    else:
        ns = y
    
    return ns
    
#Updates or adds (value) an additional info (field) to any type of entity    
def update_addinfo(entity, field, value):
    flag = 0
    
    for x in entity.additional_infos():
        if x.addinf_specnbr.field_name == field:
            flag = x
            break
    
    if flag == 0:
        
        e_clone = entity.clone()
        add = ael.AdditionalInfo.new(e_clone)
        spec = ael.AdditionalInfoSpec[field].specnbr
        add.addinf_specnbr = spec
        add.value = value
        try:
            add.commit()
            e_clone.commit()
            s = field + ' was updated'
            print s
        except:
            print (field + ' was not created')
    else:
        a_clone = x.clone()
        a_clone.value = value
        try:
            a_clone.commit()
            s = field + ' was updated '  
            print s
        except:
            print 'not commited'    
'''----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------'''
class OrderBookSheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FOrderBookSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = OrderBookSheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        print calc.Value()
        return calc
        
class TradeSheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FTradeSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = TradeSheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
'''----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------'''
def Redemption(i,*rest):
    
    ins = acm.FInstrument[i.insid]
    t = ins.Trades().At(0)
    calc = TradeSheetCalcSpace.get_column_calc( t, 'Redemption Amt' )
    return max(calc.Value().Number(), 0)
    
    
# Added for commitment fee replacing the redemption amount.    
def Balance(trade,date=None,*rest):
    context = acm.GetDefaultContext()
  
    calc_space = acm.Calculations().CreateCalculationSpace( context,
    'FPortfolioSheet' )
      
    if date:
        acmDate = acm.Ael.AelToFObject(date)
        calc_space.SimulateGlobalValue( 'Portfolio Profit Loss End Date', 'Custom Date' )
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', acmDate.Value())
    
    
    acmTrade = acm.Ael.AelToFObject(trade)
    value = calc_space.CalculateValue(acmTrade, 'Deposit balance' )
    
    return abs(value.Value().Number())
        
 

#print Redemption(ael.Instrument['362123-ZAR-2203-01'])
'''----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------'''
def Interest(ins, *rest):
    cfs = ins.legs()[0].cash_flows()
    interest  = 0
    today = ael.date_today()
    for cf in cfs:
        if cf.type in ("Call Fixed Rate Adjustable", "Fixed Rate Adjustable" ) and cf.pay_day <= today:
            interest += cf.projected_cf()
    return interest
'''----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------'''
def get_undspot(ins, *rest):
    i       = acm.FInstrument[ins.insid]
    calc    = OrderBookSheetCalcSpace.get_column_calc(i, 'Portfolio Underlying Price')
    print calc.Value()
    return  calc.Value().Number()
'''----------------------------------------------------------------------------------------------------------------------------------------------
We can just use used_vold here?
----------------------------------------------------------------------------------------------------------------------------------------------'''
def get_vol(ins, *rest):
    return ins.used_vol()
    #i       = acm.FInstrument[ins.insid]
    #calc    = OrderBookSheetCalcSpace.get_column_calc(i,'Portfolio Volatility')
    #return  calc.FormattedValue()
    
'''----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------'''
def get_vega(ins,p, *rest):            
    try:
        #i       = acm.FInstrument[ins.insid]            
        port    = acm.FPhysicalPortfolio[p]            
        calc    = OrderBookSheetCalcSpace.get_column_calc(port, 'Vega')
        return calc.Value()
    except:
        return -1    
'''----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------'''
def write_file(name, data):
    f = file(name, 'wb')
    c = csv.writer(f, dialect = 'excel')
    c.writerows(data)
    f.close()
'''----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------'''
def get_vol_surface(ins,*rest):
    return ins.used_volatility().vol_name
