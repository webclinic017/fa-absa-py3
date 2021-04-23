
import ael, acm
from FSQL_functions import FirstBusinessDay


calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')


def applyGlobalSimulation(t, date, *rest):
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)
    calcSpace.Refresh()
    return date
    
def get_Trading_Manager_Column_Value(trade, columnName, *rest):
    trade = acm.FTrade[trade.trdnbr]
    value = calcSpace.CalculateValue(trade, columnName)
    if value:
        try:
            Numbervalue = value.Number()
        except:
            Numbervalue = value
        
        return Numbervalue
    return 0.00

def PLPosEnd(temp,trd,repdate,*rest):
    applyGlobalSimulation(1, repdate)
    Value = get_Trading_Manager_Column_Value(trd, 'Portfolio Profit Loss Position End')
    return Value



def get_info(temp, i, day, flag, *rest):
    try:
        repday = ael.date_from_string(day)
    except:
        repday = day

    security = ''
    term_bucket = 0
    remaining_term = 0
    
    if i.instype in ('Repo/Reverse', 'BuySellback') and i.und_instype in ('Bond', 'IndexLinkedBond', 'FRN'):
        security = i.und_insaddr.insid
        term_bucket = 0
        remaining_term = 0
        
    else:
        if i.instype in ('Bond', 'IndexLinkedBond', 'FRN'):
            security = i.insid
            term_bucket = 0
            remaining_term = 0
        else:
            if i.instype in ('Repo/Reverse', 'BuySellback') and i.und_instype == 'Bill':
                remaining_term = repday.days_between(i.und_insaddr.exp_day, 'Act/365')
            else:
                remaining_term = repday.days_between(i.exp_day, 'Act/365')                
                
            if remaining_term < 92:
                security = 'ZAR/TB/0_91day'
                term_bucket = 91
            elif remaining_term < 183:
                security = 'ZAR/TB/92_182day'
                term_bucket = 182
            elif remaining_term < 274:
                security = 'ZAR/TB/183_273day'
                term_bucket = 273
            else:
                security = 'ZAR/TB/274_364day'
                term_bucket = 364
                
    if flag == 'security':
        return (str)(security)
    elif flag == 'term_bucket':
        return (str)(term_bucket)
    elif flag == 'remaining_term':
        return (str)(remaining_term)
    else:
        return ''
    





def get_SARB20_price(temp, i, repday, flag, *rest):
    bid = 0.0
    security = get_info(1, i, repday, 'security')
    ins_prices = ael.Instrument[security].historical_prices()
    for p in ins_prices:
        if p.ptynbr.ptyid == 'SARB20' and p.day == repday:
            bid = p.bid
            
    #if no price is found for the day, use one of the previous business days price.  
    #ie. use price of friday for sunday or saturday if it doesnt exist.
    if bid == 0.0:
        prev_day = repday.add_banking_day(ael.Instrument['ZAR'], -1)
        for p in ins_prices:
            if p.ptynbr.ptyid == 'SARB20' and p.day == prev_day:
                bid = p.bid

    return bid
      



def get_value(temp, trdnbr, day, bill_type, *rest):
    try:
        repday = ael.date_from_string(day)
    except:
        repday = day

    t = ael.Trade[trdnbr]
    i = t.insaddr
    s = get_info(1, i, repday, 'security')
    security = ael.Instrument[s]
    term_bucket = (float)(get_info(1, i, repday, 'term_bucket'))
    remaining_term = (float)(get_info(1, i, repday, 'remaining_term'))
    SARB20_price = (float)(get_SARB20_price(1, i, repday, 'SARB20'))
    position = t.position(None, None, None, repday)
    #position = PLPosEnd(1, t, repday)
    #print repday, position
    #print 'sec, t_b, r_t ', security, term_bucket, remaining_term 

    val = 0.0               
    if security.instype in ('Bond', 'IndexLinkedBond', 'BuySellback', 'Repo/Reverse', 'Future/Forward') and security.und_instype != 'Bill':
        val = position * security.dirty_from_yield(repday, None, None, SARB20_price) / 100 
    elif security.instype == 'FRN':
        val = position * round((security.present_value(repday)/10000), 5) /100
    elif security.instype in ('Repo/Reverse', 'BuySellback') and security.und_instype == 'Bill':
        val = position - (position * SARB20_price/100) * (remaining_term/365)       
    elif bill_type in ('TB', 'LBB'):
        val = position - (position * SARB20_price/100) * (remaining_term/365)
    else:
        val = position - (position * (((365/term_bucket) * ((1/(1-(SARB20_price*term_bucket/36500)))-1))*100)/100) * (remaining_term/365)                 

    return val



    


def get_MTD_value(temp, trdnbr, day, bill_type, *rest):
    try:
        repday = ael.date_from_string(day)
    except:
        repday = day

    fdom = FirstBusinessDay(1, repday)
    liq_fdom = fdom.add_banking_day(ael.Instrument['ZAR'], 14)
        
    if repday < liq_fdom:
        fdom = FirstBusinessDay(1, repday.add_months(-1))
        liq_fdom = fdom.add_banking_day(ael.Instrument['ZAR'], 14)    
        
    
    #only do banking day adjustment where security is a Bond
    adj = 0
    i = ael.Trade[trdnbr].insaddr
    if (i.instype in ('Repo/Reverse', 'BuySellback') and i.und_instype in ('Bond', 'IndexLinkedBond', 'FRN')) or (i.instype in ('Bond', 'IndexLinkedBond', 'FRN')):
        adj = 1
    
    count = 0
    MTD = 0
    liq_d = liq_fdom
    cal = ael.Calendar['ZAR Johannesburg']
    while liq_d <= repday:
        if liq_d.is_banking_day(cal) == 1:
            MTD = MTD + get_value(1, trdnbr, liq_d, bill_type)
        elif adj == 1:
            new_liq_d = liq_d.adjust_to_banking_day(cal, 'Preceding')
            MTD = MTD + get_value(1, trdnbr, new_liq_d, bill_type)
        else:
            MTD = MTD + get_value(1, trdnbr, liq_d, bill_type)
        liq_d = liq_d.add_days(1)
        count = count + 1
    
    try:
        MTD_val = MTD
        #/count
    except:
        MTD_val = 0
        
    return MTD_val
    



'''
try:
    repday = ael.date_from_string('2011-12-20')
except:
    print 'error'
day = ael.date_today().add_days(-1)
t = ael.Trade[15697353]
i = t.insaddr
applyGlobalSimulation(1, repday)
security = get_info(1, i, repday, 'security')
term_bucket = (float)(get_info(1, i, repday, 'term_bucket'))
remaining_term = (float)(get_info(1, i, repday, 'remaining_term'))
position = PLPosEnd(1, t, repday)
print 'repday', repday
print 'security', security
print 'term_bucket', term_bucket
print 'remaining_term', remaining_term
print 'position', position
    
print get_value(1, 15697353, i, repday, 'TB')
#print get_MTD_value(1, 17402451, ins, day, 'TB')
'''
