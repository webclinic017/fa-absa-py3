"""
Purpose: File 2 required for trioptima
Department : Trading
Desk : Fixed Income
Requester :  Jansen Van Rensburg, Hendrik
Developer : Anil Parbhoo
CR Number : 883172
Book of Work / Jira Reference Number : ABITFA-1178
Previous CR Numbers relating to this deployment : 18780


=============================================================================
Date       Change no Developer              Description
-----------------------------------------------------------------------------

2012-08-03 358067    Anil Parbhoo           incorporate  a date in the output file

2015-04-08 FAU-663  Paseka Motsoeneng       Use time buckets instead of dates to calculate discount deltas.

"""

import acm, ael

calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection() 

def deltaDates(dates, index):
    d1 = 0
    if index > 0:
       d1 = dates[index-1]
    d2 = dates[index]
    return d1, d2  

def getDelta(t, d1, d2):
    curr = t.Instrument().Currency().Name() 
    dd = t.Calculation().InterestRateDiscountDeltaDates(calcSpace, curr, curr, d1, None, d2).Number()
    
    return dd

def getTimeBucketsDelta(trade, timeBucket):
    curr = trade.Instrument().Currency().Name() 
    delta = trade.Calculation().InterestRateDiscountDeltaBuckets(calcSpace, curr, curr, timeBucket)
    return delta          

# set up canidate values for ael_variables to be used for ael_main

TFs = []

for tf in ael.TradeFilter.select():
    TFs.append(tf.fltid)
TFs.sort()

sdt = str(ael.date_today())
dirdt = sdt[6:10] + sdt[3:5] + sdt[0:2]

ael_variables = [('selectedTf', 'TradeFilter_Trade Filter', 'string', TFs, 'IRD_TRIOPTIMA_2011', 1, 0),
('selectedFile', 'Outfile_Admin', 'string', [], 'C:\\temp\ABSA_Triopt_discount_deltas_'+ dirdt + '.csv', 1)
]

def ael_main(dict):

    #tf = ael.TradeFilter['IRD_TRIOPTIMA_2010']
    tf = ael.TradeFilter[dict["selectedTf"]]
    outfile = dict["selectedFile"]
    
    time_buckets = []
    trades = tf.trades()
    c = []
    gl=[]
    period_dates = []
    today = ael.date_today()
    bucket_list = []
    periods = ['1d', '1w', '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '10m', '11m', '1y', '13m', '14m', '15m', '16m', '17m', '18m', '19m', '20m', '21m', '22m', '23m', '2y', '3y', '4y', '5y', '6y', '7y', '8y', '9y', '10y', '11y', '12y', '13y', '14y', '15y', '20y', '25y', '30y']
    
    for p in periods:
        d = ((today.add_period(p)).adjust_to_banking_day(ael.Calendar['ZAR Johannesburg'], 'Following'))
        period_dates.append(d) 
        bd = acm.FFixedDateTimeBucketDefinition()
        bd.FixedDate(d)
        bd.DiscardIfExpired(True)
        bd.UninterruptedSequence(True)
        bucket_list.append(bd)
    
    time_bucket_definition = acm.TimeBuckets().CreateTimeBucketsDefinition(
        acm.Time().DateToday(), 
        bucket_list, 
        False, 
        False, 
        False, 
        False, 
        False
    )
    
    def_conf = acm.TimeBuckets().CreateTimeBucketsDefinitionAndConfiguration(time_bucket_definition)
    time_buckets = acm.TimeBuckets().CreateTimeBuckets(def_conf)
    
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
            c.append('DISCOUNT')                        #Delta Type

            for delta in getTimeBucketsDelta(t, time_buckets):
                c.append(delta.Number())

            gl.append(c)    
                
        else:   #FRA's Section
            c = []
                
            legs = ins.legs()
            leg0 = legs[0]
       
            c.append(trd.trdnbr)                                #TRADE_ID
            c.append('DISCOUNT')                                #Delta Type

            for delta in getTimeBucketsDelta(t, time_buckets):
                c.append(delta.Number())
            
            gl.append(c)    
                    
    try:
        Headers = ['TRADE_ID', 'DELTA_TYPE', 'DELTA_1D', 'DELTA_1W', 'DELTA_1M', 'DELTA_2M', 'DELTA_3M', 'DELTA_4M', 'DELTA_5M', 'DELTA_6M', 'DELTA_7M', 'DELTA_8M', 'DELTA_9M', 'DELTA_10M', 'DELTA_11M', 'DELTA_12M', 'DELTA_13M', 'DELTA_14M', 'DELTA_15M', 'DELTA_16M', 'DELTA_17M', 'DELTA_18M', 'DELTA_19M', 'DELTA_20M', 'DELTA_21M', 'DELTA_22M', 'DELTA_23M', 'DELTA_2Y', 'DELTA_3Y', 'DELTA_4Y', 'DELTA_5Y', 'DELTA_6Y', 'DELTA_7Y', 'DELTA_8Y', 'DELTA_9Y', 'DELTA_10Y', 'DELTA_11Y', 'DELTA_12Y', 'DELTA_13Y', 'DELTA_14Y', 'DELTA_15Y', 'DELTA_20Y', 'DELTA_25Y', 'DELTA_99Y']

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
        ael.log('File printed to C:\temp\ABSA_Triopt_discount_deltas_'+ dirdt + '.csv')
    except:
        ael.log("File not printed")

    return
