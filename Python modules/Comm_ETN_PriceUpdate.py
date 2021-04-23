'''
date                          :  
Purpose                       :  Change the stock names to have a suffix '_OLD' as the original stock names will be used to set up the ETF                              :  
Department and Desk           :  PCG SM Commodities
Requester                     :  Khunal Ramesar
Developer                     :  Anil Parbhoo
CR Number                     :  427282
FO Jira / BOW reference       :  Jira ABITFA-157 
Previous cr numbers           :  333681, 284698, 228268, 424645, 427282

'''


import ael, math, acm
import ABSA_Rate


def update_stock_price_from_ins(eq, stk, start, df):
    end =ael.date_today()
    eq_curr = ael.Instrument[stk].curr.insid
    
    eqPrice = float(ael.Instrument[eq].spot_price(eq_curr))
    factor = float(1)/(1 - df)
    period = float(start.days_between(end))
    power = float(period)/365
    
    '''
    currpair = ael.Instrument[eq_curr].currency_pair("USD")
    currpair_spot_date = currpair.spot_date(end)
    days_to_spot = acm.Time.DateDifference(currpair_spot_date, end)
    t2 = end.add_days(days_to_spot)
    '''
    t2 = end.add_banking_day(ael.Instrument[stk].curr, 2)
    
     
    
    
    
    
    
    #calculation of discount rate and growth 
    ins_spot = end.add_banking_day(ael.Instrument[stk].curr, ael.Instrument[stk].spot_banking_days_offset)  
        
        
        
    if stk == 'BWP/GLD_OLD':
        yc = ael.YieldCurve['BWP-USD/FX']

        discount_for_2_days = ABSA_Rate.ABSA_yc_rate(0, 'BWP-USD/FX', end, t2, 'Discount', 'ACT/365', 'Discount', 'BWP')
        rate = ABSA_Rate.ABSA_yc_rate(0, 'BWP-USD/FX', end, ins_spot, 'Simple', 'Act/365', 'Spot Rate', 'BWP')
        growth = (1+(rate*(end.days_between(ins_spot, 'Act/365'))/365))*discount_for_2_days 
            
    else:       
        yc = ael.Instrument['ZAR'].used_yield_curve()
            
        discount_for_2_days = yc.yc_rate(end, t2, 'Discount', 'Act/365', 'Discount') 
        rate = yc.yc_rate(end, ins_spot, 'Simple', 'Act/365', 'Spot Rate') 
        growth = (1+(rate*(end.days_between(ins_spot, 'Act/365'))/365))*discount_for_2_days
        

    


 
    #calculation of constants for XPT ans XAG
    if stk == 'ZAR/PLATNOTEFWD_OLD':
        for r in ael.Instrument['ZAR/PLATNOTEDEPO_OLD'].prices():
            if r.ptynbr.ptyid == 'SPOT' and r.day == end:
                constant = r.settle
                    
    elif stk == 'ZAR/SILVERNOTEFWD_OLD':
        for p in ael.Instrument['ZAR/SILVERNOTEDEPO_OLD'].prices():
            if p.ptynbr.ptyid == 'SPOT' and p.day == end:
                constant = p.settle
    else:
        constant = 0
            
    
    
    
    
    # calculate spot price based on spot price of eq, growth, and subtraction of constant
    SpotPrice = round(float(eqPrice * growth * math.pow(factor, -power))-constant, 2) 
    #print stk, SpotPrice

    stkIns = ael.Instrument[stk]
    
    for p in stkIns.prices():
       if p.ptynbr.ptyid == 'SPOT' and p.day == end:
            p_clone = p.clone()
            break
    else:
        p_clone = ael.Price.new()

    
    try:
        p_clone.insaddr = stkIns.insaddr
        p_clone.ptynbr = ael.Party['SPOT'].ptynbr
        p_clone.day = end
        p_clone.bid = SpotPrice
        p_clone.ask = SpotPrice
        p_clone.last = SpotPrice
        p_clone.settle = SpotPrice
        p_clone.curr = stkIns.curr
        p_clone.commit()
    except:
        ael.log("Price did not commit for "+ stk)
     

update_stock_price_from_ins('XAU', 'ZAR/GLD_OLD', ael.date('2004-11-01'), 0.004)

update_stock_price_from_ins('XPT', 'ZAR/PLATNOTE_OLD', ael.date('2010-04-01'), 0.005)
update_stock_price_from_ins('XAG', 'ZAR/SILVERNOTE_OLD', ael.date('2010-04-01'), 0.005)

update_stock_price_from_ins('XPT', 'ZAR/PLATNOTEFWD_OLD', ael.date('2010-04-01'), 0.005)
update_stock_price_from_ins('XAG', 'ZAR/SILVERNOTEFWD_OLD', ael.date('2010-04-01'), 0.005)

update_stock_price_from_ins('XAU', 'BWP/GLD_OLD', ael.date('2004-11-01'), 0.004)

