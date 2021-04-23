"""
Purpose: Script restated for Front Arena version 4.3 and to route output file to C:\ drive
         as the results from the backend are not correct - SPR 207236 raised by Sungard
Department : Trading
Desk : Fixed Income
Requester :  Jansen Van Rensburg, Hendrik
Developer : Anil Parbhoo
CR Number : 393881
Book of Work / Jira Reference Number : ABITFA-142
Previous CR Numbers relating to this deployment : 18780

=============================================================================
Date       Change no Developer              Description
-----------------------------------------------------------------------------

2010-05-06 648543    Rohan vd Walt          Instrument curves used in delta calculations instead of manually specifying.
                                            Added SWAPSWIRE_ID and SW_SINGLESIDED columns
2012-02-09 889883    Anil Parbhoo           Applied the rules of SWAPSWIRE_ID and SW_SINGLESIDED columns to fra's as well                                            
                                            
2012-02-10 890917    Anil Parbhoo           Corrected the calculation of the swap spread and set the spread of a fra to zero

2012-02-16 892004    Anil Parbhoo           Corrected next fixing date 

2012-08-03 358067    Anil Parbhoo           add a column with heading 'CSA_TYPE' and incorporate  a date in the output file
                                             
-----------------------------------------------------------------------------
"""


import acm, ael, SAGEN_str_functions, RollingPeriod, SAGEN_Cashflows


def NextCashFlow(temp, lnbr, ddate, flag, *rest):
    l = ael.Leg[lnbr]
    cashf = l.cash_flows()
    list = []
    for c in cashf:
    	tup = (c.pay_day, c.cfwnbr, c.fixed_amount, c.start_day)
#	print tup
	list.append(tup)
    	
    list.sort()

    count = 0
    value = ''
    sdate = ael.date_from_string(ddate)
    if l.start_day>=sdate:
        return l.start_day
    else:
        while count < len(list):
            pay_day = list[count][0]
            if pay_day > sdate:
    #	    print 'Next cashflow pay_day', pay_day
                if flag == 0:
                    value = (str)(list[count][2])
                    return value
                elif flag == 1:
                    value = (str)(list[count][0])
                    return value		    
                elif flag == 2:
                    if value == '':
                        value = (str)(list[count][0])
                    else:
                        if value.find((str)(list[count][0])) == -1:
                            value = value + ',' + (str)(list[count][0])
                        else: value = value
                    #return value
                elif flag == 3:
                    if pay_day==l.end_day:
                        value = (str)(list[count][3])
                    else:
                        value = (str)(list[count][0])
                    return value
                else:
                    return value
            count = count + 1
            
        return value
   

calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection() 

def deltaDates(dates, index):
    d1 = 0
    if index > 0:
       d1 = dates[index-1]
    d2 = dates[index]
    return d1, d2  

def getDelta(t, d1, d2):
    curr = t.Instrument().Currency().Name() 
    bmd = t.Calculation().InterestRateBenchmarkDelta(calcSpace, curr, None, d1, d2).Number()
    return bmd
          
def getTotalDelta(t):
    
    ins = t.Instrument()
    curr = ins.Currency().Name() 
    total_bmd = t.Calculation().InterestRateBenchmarkDelta(calcSpace, curr, None, ael.date_today(), ael.BIG_DATE).Number()
    return total_bmd

def getPV(t):

    #set context, sheet type, column id, and portfolio
    context = acm.GetDefaultContext()
    sheet_type = 'FPortfolioSheet'
    column_id = 'Portfolio Present Value'

    #create CalculationSpace (virtual Trading Manager)

    calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type )

    #get number of the raw value
    value = calc_space.CalculateValue( t, column_id )
    PV = value.Number()
    
    return PV 

# set up canidate values for ael_variables to be used for ael_main

TFs = []

for tf in ael.TradeFilter.select():
    TFs.append(tf.fltid)
TFs.sort()

sdt = str(ael.date_today())
dirdt = sdt[6:10] + sdt[3:5] + sdt[0:2]

ael_variables = [('selectedTf', 'TradeFilter_Trade Filter', 'string', TFs, 'IRD_TRIOPTIMA_2011', 1, 0),
('selectedFile', 'Outfile_Admin', 'string', [], 'C:\\temp\ABSA_Triopt_' + dirdt + '.csv', 1)
]

def ael_main(dict):

    #tf = ael.TradeFilter['IRD_TRIOPTIMA_2010']
    tf = ael.TradeFilter[dict["selectedTf"]]
    outfile = dict["selectedFile"]
    
    trades = tf.trades()
    c = []
    gl=[]
    period_dates = []
    today = ael.date_today() 
    periods = ['1d', '1w', '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '10m', '11m', '1y', '13m', '14m', '15m', '16m', '17m', '18m', '19m', '20m', '21m', '22m', '23m', '2y', '3y', '4y', '5y', '6y', '7y', '8y', '9y', '10y', '11y', '12y', '13y', '14y', '15y', '20y', '25y', '30y']

    for p in periods:
        d = ((today.add_period(p)).adjust_to_banking_day(ael.Calendar['ZAR Johannesburg'], 'Following'))
        #print d
        period_dates.append(d) 
    period_dates.sort()
    #print period_dates
            
    for trd in trades:
            
        t = acm. FTrade[trd.trdnbr]
        ins = trd.insaddr

        if ins.instype in ['Swap']:
            c = []
                
            legs = ins.legs()
            if legs[0].type == 'Fixed':
                leg0 = legs[0]
                leg1 = legs[1]
            else:
                leg0 = legs[1]
                leg1 = legs[0]
                
            c.append(trd.trdnbr)                        #TRADE_ID
            c.append(trd.counterparty_ptynbr.ptyid)     #CP_ID
            c.append(trd.counterparty_ptynbr.add_info('CSA Collateral Curr')) #CSA_TYPE
            c.append(trd.your_ref)                      #CP_REF
            c.append(trd.prfnbr.prfid)                  #TRADE_UNIT_ID
            c.append(trd.your_ref)                      #CP_TRADE_ID
            c.append(ins.instype)                       #INS_TYPE
            c.append(ins.insid)                         #INS_ID
            c.append(abs(trd.nominal_amount()))         #NOMINAL
            c.append(ins.curr.insid)                    #CURR
            if leg0.projected_cf() * trd.quantity < 0:
                c.append('Payer')                       #PAY_REC
            else:
                c.append('Receiver')                    #PAY_REC
            c.append(leg0.fixed_rate)                   #COUPON_RATE
            c.append(RollingPeriod.RP(1, leg0))          #COUPON_PER
            c.append(leg0.daycount_method)              #DAYCOUNT
            c.append(SAGEN_str_functions.split_string(1, leg1.float_rate.insid, '-', 1)) #FLOAT_RATE_INDEX
            
            if (SAGEN_str_functions.split_string(1, leg1.float_rate.insid, '-', 3)) == 'Index out of range' :
                c.append(SAGEN_str_functions.split_string(1, leg1.float_rate.insid, '-', 2))     #FLOAT_RATE_INDEX_PER
            else:
                c.append(SAGEN_str_functions.split_string(1, leg1.float_rate.insid, '-', 3))     #FLOAT_RATE_INDEX_PER

            c.append(RollingPeriod.RP(1, leg1)) #FLOAT_RATE_PAY_PER
            c.append(RollingPeriod.RP(1, leg1)) #FLOAT_RATE_FIXING_PER
            for l in ins.legs():
                if l.type == 'Float':
                    sp = (l.spread)#will reflect in percentage format rather than decimal format
                
            c.append(sp) #FLOAT_SPREAD
            
            
            if SAGEN_Cashflows.CurrentCF(1, leg1.legnbr, today, 5) == '0001-01-01':
                c.append(0.0)                                                           #FLOAT_RATE
            else:
                c.append(SAGEN_Cashflows.CurrentCF(1, leg1.legnbr, ael.date_today(), 5)) #FLOAT_RATE
                
            c.append(ael.date_from_time(trd.time))              #TRADE_DATE
            c.append(leg0.start_day)                            #START_DATE
            c.append(ins.exp_day)                               #END_DATE
            c.append(leg0.rolling_base_day)                     #ROLL_DATE
            c.append(NextCashFlow(1, leg1.legnbr, today, 3))     #NEXT_FIXING_DATE 
            c.append(SAGEN_Cashflows.NextCF(1, leg1.legnbr, today, 1))     #NEXT_FLOAT_PAY_DATE
            c.append(SAGEN_Cashflows.NextCF(1, leg0.legnbr, today, 1))     #NEXT_FIX_PAY_DATE
            
            swapswireID = trd.optional_key if trd.optional_key[0:2] == 'MW' else ''
            c.append(swapswireID)                          #SWAPSWIRE_ID
            c.append('' if swapswireID == '' else 'No')  #SW_SINGLESIDED
                                                                
            c.append(today)                                     #MTM_DATE
            c.append(getPV(t))                                  #MTM_VALUE
            c.append(ins.curr.insid)                            #MTM_CURR
            
            c.append(getTotalDelta(t))                   #DELTA_TOTAL
            
            for index in range(len(period_dates)):
                d1, d2 = deltaDates(period_dates, index)        #DELTA_1D - DELTA_99Y
                c.append(getDelta(t, d1, d2))
            
            c.append(ins.curr.insid)                            #DELTA_CURR
            gl.append(c)    
                
        else:   #FRA's Section
            c = []
                
            legs = ins.legs()
            leg0 = legs[0]
       
            c.append(trd.trdnbr)                                #TRADE_ID
            c.append(trd.counterparty_ptynbr.ptyid)             #CP_ID
            c.append(trd.counterparty_ptynbr.add_info('CSA Collateral Curr')) #CSA_TYPE
            c.append(trd.your_ref)                              #CP_REF
            c.append(trd.prfnbr.prfid)                          #TRADE_UNIT_ID
            c.append(trd.your_ref)                              #CP_TRADE_ID
            c.append(ins.instype)                               #INS_TYPE
            c.append(ins.insid)                                 #INS_ID
            c.append(abs(trd.nominal_amount()))                 #NOMINAL
            c.append(ins.curr.insid)                            #CURR
            if trd.quantity > 0:
                c.append('Payer')                               #PAY_REC
            else:
                c.append('Receiver')                            #PAY_REC
            c.append(leg0.fixed_rate)                           #COUPON_RATE
            c.append(RollingPeriod.RP(1, leg0))                  #COUPON_PER
            c.append(leg0.daycount_method)                      #DAYCOUNT
            c.append(SAGEN_str_functions.split_string(1, leg0.float_rate.insid, '-', 1)) #FLOAT_RATE_INDEX
            
            if (SAGEN_str_functions.split_string(1, leg0.float_rate.insid, '-', 3)) == 'Index out of range' :
                c.append(SAGEN_str_functions.split_string(1, leg0.float_rate.insid, '-', 2))     #FLOAT_RATE_INDEX_PER
            else:
                c.append(SAGEN_str_functions.split_string(1, leg0.float_rate.insid, '-', 3))     #FLOAT_RATE_INDEX_PER
            
            c.append(RollingPeriod.RP(1, leg0))                  #FLOAT_RATE_PAY_PER
            c.append(RollingPeriod.RP(1, leg0))                  #FLOAT_RATE_FIXING_PER
            c.append(0.0)                               #FLOAT_SPREAD
            if SAGEN_Cashflows.CurrentCF(1, leg0.legnbr, today, 5) == '0001-01-01':
                c.append(0.0)                                                           #FLOAT_RATE
            else:
                c.append(SAGEN_Cashflows.CurrentCF(1, leg0.legnbr, ael.date_today(), 5)) #FLOAT_RATE
                
            c.append(ael.date_from_time(trd.time))                      #TRADE_DATE
            c.append(leg0.start_day)                                    #START_DATE
            c.append(ins.exp_day)                                       #END_DATE
            c.append(leg0.rolling_base_day)                             #ROLL_DATE
            c.append(SAGEN_Cashflows.NextCF(1, leg0.legnbr, today, 1))     #NEXT_FIXING_DATE
            c.append(SAGEN_Cashflows.NextCF(1, leg0.legnbr, today, 1))     #NEXT_FLOAT_PAY_DATE
            c.append(SAGEN_Cashflows.NextCF(1, leg0.legnbr, today, 1))     #NEXT_FIX_PAY_DATE
            
            swapswireID = trd.optional_key if trd.optional_key[0:2] == 'MW' else ''
            c.append(swapswireID)                          #SWAPSWIRE_ID
            c.append('' if swapswireID == '' else 'No')  #SW_SINGLESIDED
            
            
            
            
            
            c.append(today)                                             #MTM_DATE
            c.append(getPV(t))                                          #MTM_VALUE
            c.append(ins.curr.insid)                                    #MTM_CURR
            
            c.append(getTotalDelta(t))                           #DELTA_TOTAL
            for index in range(len(period_dates)):
                d1, d2 = deltaDates(period_dates, index)                #DELTA_1D - DELTA_99Y
                c.append(getDelta(t, d1, d2))
            c.append(ins.curr.insid)                                    #DELTA_CURR
            gl.append(c)    
                    
    try:
        Headers = ['TRADE_ID', 'CP_ID', 'CSA_TYPE', 'CP_REF', 'TRADE_UNIT_ID', 'CP_TRADE_ID', 'INS_TYPE', 'INS_ID', 'NOMINAL', 'CURR', 'PAY_REC', 'COUPON_RATE', 'COUPON_PER', 'DAYCOUNT', 'FLOAT_RATE_INDEX', 'FLOAT_RATE_INDEX_PER', 'FLOAT_RATE_PAY_PER', 'FLOAT_RATE_FIXING_PER', 'FLOAT_SPREAD', 'FLOAT_RATE', 'TRADE_DATE', 'START_DATE', 'END_DATE', 'ROLL_DATE', 'NEXT_FIXING_DATE', 'NEXT_FLOAT_PAY_DATE', 'NEXT_FIX_PAY_DATE', 'SWAPSWIRE_ID', 'SW_SINGLESIDED', 'MTM_DATE', 'MTM_VALUE', 'MTM_CURR', '_DELTA_TOTAL', 'DELTA_1D', 'DELTA_1W', 'DELTA_1M', 'DELTA_2M', 'DELTA_3M', 'DELTA_4M', 'DELTA_5M', 'DELTA_6M', 'DELTA_7M', 'DELTA_8M', 'DELTA_9M', 'DELTA_10M', 'DELTA_11M', 'DELTA_12M', 'DELTA_13M', 'DELTA_14M', 'DELTA_15M', 'DELTA_16M', 'DELTA_17M', 'DELTA_18M', 'DELTA_19M', 'DELTA_20M', 'DELTA_21M', 'DELTA_22M', 'DELTA_23M', 'DELTA_2Y', 'DELTA_3Y', 'DELTA_4Y', 'DELTA_5Y', 'DELTA_6Y', 'DELTA_7Y', 'DELTA_8Y', 'DELTA_9Y', 'DELTA_10Y', 'DELTA_11Y', 'DELTA_12Y', 'DELTA_13Y', 'DELTA_14Y', 'DELTA_15Y', 'DELTA_20Y', 'DELTA_25Y', 'DELTA_99Y', 'DELTA_CURR']

        #newdate = ael.date_today().to_string('%Y-%m-%d')
        #outfile ='//services/frontnt/BackOffice/Atlas-End-Of-Day/' + newdate + '/SAIRD_TRIOPTIMA.csv'
                    
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
        ael.log('File printed to C:\temp\ABSA_Triopt_'+ dirdt + '.csv')
    except:
        ael.log("File not printed")

    return
