"""-----------------------------------------------------------------------------
PURPOSE         :       This module is used to pull the daily call account
                        balances for clients for a set period and write the
                        output to a csv file.
--------------------------------------------------------------------------------
HISTORY
================================================================================
Date            Change no       Developer            Description
--------------------------------------------------------------------------------
2016-08-16      CHNG0003864231  Willie vd Bank       Initial Implementation
"""

import acm, sys, datetime, ael
from acm import Time
from Call_Average_Balances_OvrPeriod import AvgBalance

cf_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def writefile(text, location):
    try:
        file = open(location, 'w')
        file.write(text)
        file.close()
    except Exception, e:
        print 'Error creating output file.', e
        
def filters():
    return sorted(tf.fltid for tf in ael.TradeFilter)

ael_variables = [('Start', 'Start Date', 'string', '', Time.DateAddDelta(Time.DateNow(), 0, 0, -365), 1),
                ('End', 'End Date', 'string', '', Time.DateNow(), 1),
                ('Filter', 'Trade Filter', 'string', filters(), 'Call_AV_Bal'),
                ('Folder', 'Folder_Path', 'string', ['F:\\'], '', 1)]

def ael_main(params):
    print 'Started...'
    tradesdict = {}
    startdate = params['Start']
    enddate = params['End']
    filter = params['Filter']
    path = params['Folder']
    
    context = acm.GetDefaultContext()
    calc_space = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
    
    trades = ael.TradeFilter[filter].trades()
    #trades = [ael.Trade[1581361], ael.Trade[2450935], ael.Trade[1902072]]
    
    for aeltrade in trades:
        tradesdict[aeltrade.trdnbr] = []
        ins = acm.FInstrument[aeltrade.insaddr.insaddr]
        #endValue = calc_space.CalculateValue(ins, 'PLPeriodEnd')
        start = startdate
        tradesdict[aeltrade.trdnbr].append(aeltrade.counterparty_ptynbr.ptyid)
        while start <= enddate:
            calc_space.SimulateValue(ins, 'PLPeriodEnd', start)
            tradesdict[aeltrade.trdnbr].append(aeltrade.quantity * calc_space.CalculateValue(ins, 'Deposit balance').Number())
            start = acm.Time().DateAddDelta(start, 0, 0, 1)
    
    output = 'Trade Number,Counterparty,'
    start = startdate
    while start <= enddate:
        output += str(start) + ','
        start = acm.Time().DateAddDelta(start, 0, 0, 1)
    
    outputfile = path + 'Loans_Call_Balance_Extract_'+ str(datetime.datetime.utcnow())[0:10] + '.csv'
    print 'Calculation done'
    print 'Creating output file', outputfile
    
    output += '\n'
    for i in sorted(tradesdict.keys()):
        output += str(i) + ','
        for val in tradesdict[i]:
            output += str(val) + ','
        output += '\n'

    writefile(output, outputfile)
    print 'Finished.'
