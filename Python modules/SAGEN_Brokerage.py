#----------------------------------------------------------------------------------------------
#  Name      : SAGEN_Brokerage
#  Purpose   : Calculate and insert broker fees for FRAs, Swaps and CurrSwaps for IRD
#
#  Changes
#
#  Developer : Jaysen Naicker
#  Purpose   : Add in calculation for CurrSwaps
#  Date      : 04-03-2010
#  Department and Desk : MO
#  Requester           : Lauren de Jager
#  CR Number           : 243501
#-----------------------------------------------------------------------------------------------

import ael
import acm
import time
calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection() 

curr = acm.FCurrency['ZAR']


def instrumentGetDates(curve_name):
    dates = []
    
    curve = acm.FYieldCurve[curve_name]
    
    if curve.UnderlyingCurve():
        curve = acm.FYieldCurve[curve_name].UnderlyingCurve()
    
    instruments =  curve.BenchmarkInstruments()

    for instrument in instruments:
        dates.append(instrument.LastIRSensDay())
        
    dates.sort()
    return dates
    
def deltaDates(dates, index):
    d1 = 0
    if index > 0:
       d1 = dates[index-1]
    d2 = dates[index]
    return d1, d2  
    

class CalcSpace(object):

    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()


def get_spread_delta(trd, curve_name, *rest ):

    yc=acm.FYieldCurve[curve_name]
    
    pv01 = 0.00
    
    for attribute in yc.Attributes():
        trd_calc = trd.Calculation()
        pv0 = trd_calc.PresentValue(CalcSpace.calcSpace).Number()
            
        for spread in attribute.Spreads():
            spreadClone = spread.Clone()
            spreadClone.Spread = spreadClone.Spread()+ 0.0001 
            spread.Apply(spreadClone)
            pv1 = trd_calc.PresentValue(CalcSpace.calcSpace).Number()
            pv01 = pv01 + pv1 - pv0
            spread.Undo()
            
    yc.Undo()

    return pv01

def get_bmdelta(trade, curve_name):
    bmd = 0.0
    curve = acm.FYieldCurve[curve_name]
    dates = instrumentGetDates(curve_name)
    
    for index in range(len(dates)):
        d1, d2 = deltaDates(dates, index)

        bmd += trade.Calculation().InterestRateBenchmarkDelta(calcSpace, curr, None, d1, d2, None, curve).Number()
    return bmd

def CalcBrokerage(temp,*rest):
    stf = 'Portfolios_Brokerage'
    tf = ael.TradeFilter[stf]
    gl=[]
    
    bmdelta = 0
    factor = 0
    today = ael.date_today()
    
    for trd in tf.trades():
  
        if trd.insaddr.instype == 'CurrSwap':
            curve = 'ZAR-BASIS'
            curr = []
            for l in trd.insaddr.legs():
                curr.append(l.curr.insid)
            if 'ZAR' in curr and 'USD' in curr:
                has_currencies = True
            else:
                has_currencies = False
        else:
            has_currencies = True            
            curve = 'ZAR-SWAP'
     
        if trd.broker_ptynbr and ael.date_from_time(trd.time) == today:
            if (trd.status not in ('Simulated', 'Void', 'Terminated')) and (trd.insaddr.instype in ('Swap', 'FRA', 'CurrSwap')) and has_currencies:
                bf = ael.BrokerFeeRate.select("ptynbr =" +  str(trd.broker_ptynbr.ptynbr))
                if bf:
                    for x in bf:
                        if x.instype == trd.insaddr.instype:
                            factor =  x.broker_fee_rate
                            break
                    w =[]
                    w.append(trd.trdnbr)
                    w.append(trd.broker_ptynbr.ptyid)
                    w.append(factor)
                    stat = 0
                    yc = ael.YieldCurve[curve]
                    trade = acm.FTrade[trd.trdnbr]
                    if trd.insaddr.instype == 'CurrSwap':
                        bmdelta = get_spread_delta(trade, curve)
                    else:
                        bmdelta = get_bmdelta(trade, curve)
                        
                    if (trd.insaddr.instype == 'Swap')  and (trd.insaddr.legs()[0].start_day == today):
                        val = -abs(bmdelta)*factor - 24*abs(trd.quantity)*factor
                    else:
                        val = -abs(bmdelta)*factor
                    w.append(bmdelta)
                    w.append(val)
                    if abs(bmdelta) > 0.01:
                        d1 = ael.date_today().add_months(1).to_ymd()
                        if len(str(d1[1])) == 1: 
                            d2 =ael.date(str(d1[0]) +'-0'+ str(d1[1]) + '-' + str(10)).adjust_to_banking_day(ael.Instrument['ZAR']) 
                        else:
                            d2 = ael.date(str(d1[0]) +'-'+ str(d1[1]) + '-' + str(10)).adjust_to_banking_day(ael.Instrument['ZAR']) 
                        trd_c = trd.clone()
                        paym = ael.Payment.new(trd_c)
                        paym.type = 'Broker Fee'
                        paym.amount = val
                        paym.ptynbr = trd.broker_ptynbr
                        paym.payday = d2
                        paym.valid_from = today
                        try:
                            paym.commit()
                            print 'success', trd.trdnbr
                        except:
                            print 'Unable to commit payment for trade', trd.trdnbr
                    #print w
                    gl.append(w)
    
    
    Headers = ['Trade Number', 'Broker', 'Factor', 'Benchmark Delta', 'Brokerage Fee']
    newdate = ael.date_today().to_string('%Y-%m-%d')
    #outfile ='//services/frontnt/BackOffice/Atlas-End-Of-Day/' + newdate + '/SAGEN_Brokerage.csv'     
    outfile ='//apps/frontnt/REPORTS/BackOffice/Atlas-End-Of-Day/' + newdate + '/SAGEN_Brokerage.csv'     
    report = open(outfile, 'w')
    
        
    for i in Headers:
            report.write((str)(i))
            report.write(',')
    report.write('\n')
            
        
    for lsts in gl:
            
            for ls in lsts:
                
                report.write((str)(ls))
                report.write(',')
            report.write('\n')
            
    report.close()
    
    return 'Success'
    

#CalcBrokerage(1)






 
