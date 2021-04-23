import ael, acm, FInstrumentCACashflow, CallFuturePayments
'''-----------------------------------------------------------------------------------------------------------------------------------------------------------
def accruedInterest(tag,diff,trdrow,*rest):
    accruedInt = acm.GetCalculatedValueFromString(trdrow, 'Standard','object:*"accrued"[endDate = date_add_delta(todayPL, %d, , , , ), showCurr = "ZAR"]' %diff,tag) 
    if accruedInt.PropertiesText('Value') == ' ':
        accruedInt = 0    
    else:
        accruedInt = accruedInt.Value()
    return accruedInt
def nominalChange(tag,diff,trdrow,*rest):
    nominalChange = acm.GetCalculatedValueFromString(trdrow, 'Standard','object:*"nominalChange"[endDate = date_add_delta(todayPL, %d, , , , ), showCurr = "ZAR"]' %diff,tag) 
    if nominalChange.PropertiesText('Value') == ' ':
        nominalChange = 0    
    else:
        nominalChange = nominalChange.Value()
    return nominalChange
def callAccrued(tag,diff,trdrow,*rest):
    callAccrued = acm.GetCalculatedValueFromString(trdrow, 'Standard','object:*"callAccrued"[endDate = date_add_delta(todayPL, %d, , , , ), showCurr = "ZAR"]' %diff,tag) 
    if callAccrued.PropertiesText('Value') == ' ':
        callAccrued = 0    
    else:
        callAccrued = callAccrued.Value()
    return callAccrued
-----------------------------------------------------------------------------------------------------------------------------------------------------------'''
class SheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FTradeSheet' )
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
'''---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------'''
def accruedInterest(obj,*rest):
    accruedInt      = 0
    column          = 'Portfolio Accrued Interest'
    calc            = SheetCalcSpace.get_column_calc(obj, column)
    accruedInt      = calc.Value().Number()
    return accruedInt
'''---------------------------------------------------------------------------------------------------
This nominal change column is not working correctly
---------------------------------------------------------------------------------------------------'''
def nominalChange(obj,StartDate,*rest):
    
    nominalChange   = 0
    column          = 'ABSA Nominal Change'
    calc            = SheetCalcSpace.get_column_calc(obj, column)

    nominalChange   = calc.Value().Number()
    return nominalChange

'''---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------'''
def callAccrued(obj,*rest):
    callAccrued     = 0
    column          = 'Portfolio Accrued Call Interest'  
    calc            = SheetCalcSpace.get_column_calc(obj, column)
    callAccrued     = calc.Value().Number()
    return callAccrued
'''---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------'''
def TimeSeries(partyList,startDate,endDate,fileName,*rest):

    instypeList = []
    outputList  = []
    
    inception = '1970-01-01'
    SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
    SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', inception)
    
    for party in partyList:

        tradeList       = ael.Trade.select('counterparty_ptynbr = %i' %ael.Party[party].ptynbr)
        date            = startDate

        while date <= endDate:

            SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
            SheetCalcSpace.CALC_SPACE.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', date)

            dict        = {}
            entryList   = []

            for t in tradeList:
                if t.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                    if t.acquirer_ptynbr:

                        if t.acquirer_ptynbr.ptynbr in (2246, 2247):     #Money Market Desk, Funding Desk
                            if t.insaddr:
                                if t.insaddr.exp_day:

                                    if t.insaddr.exp_day > date:

                                        instype         = t.insaddr.instype
                                        callAccountFlag = 0

                                        if instype == 'Deposit' and t.insaddr.legs().members() != [] and t.insaddr.legs()[0].type == 'Call Fixed Adjustable':
                                            callAccountFlag     = 1
                                            instype             = 'Call'

                                        key = t.acquirer_ptynbr.ptyid + '-' + instype

                                        if not instypeList.__contains__(key):
                                            instypeList.append(key)
                                            
                                        trd     = acm.FTrade[t.trdnbr]
                                        diff    =  ael.date_today().days_between(date)

                                        if dict.has_key(key):
                                            if callAccountFlag:
                                                callAcc = callAccrued(trd)
                                                callBal = callBalance(t, date)
                                                dict[key] = dict[key] + callAcc + callBal
                                            else:
                                                accruedInt = accruedInterest(trd)
                                                nomChange = nominalChange(trd, date)
                                                dict[key] = dict[key] + accruedInt + nomChange
                                        else:
                                            if callAccountFlag:
                                                callAcc = callAccrued(trd)
                                                callBal = callBalance(t, date)
                                                dict[key] = callAcc + callBal
                                            else:
                                                accruedInt = accruedInterest(trd)
                                                nomChange = nominalChange(trd, date)
                                                dict[key] = accruedInt + nomChange

            entryList.append(party)
            entryList.append(date)
            entryList.append(dict)
            outputList.append(entryList)
            date = date.add_days(1)


    #M.KLIMKE remove simulation for the end date
    SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    SheetCalcSpace.CALC_SPACE.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    
    try:
        fileName = fileName + 'SAGEN_Money_Market_History ' + startDate.to_string('%Y-%m-%d') + ' - ' + endDate.to_string('%Y-%m-%d') + ' on ' + ael.date_today().to_string('%Y-%m-%d') + '.txt'
        file = open(fileName, 'w')
    except:
        return 'Can not create the output file.'
    
    header = 'Counterparty,Date'
    for i in instypeList:
        header = header + ',' + i
    file.write(header + '\n')
        
    for entry in outputList:
        out = entry[0] + ',' + str(entry[1])
        for ins in instypeList:
            if not entry[2].has_key(ins):
                out = out + ',0'
            else:
                out = out + ',' + str(entry[2][ins])
        file.write(out + '\n')
    
    try:
        file.close()
        return 'Output file saved successfuly: ' + fileName
    except:
        return 'Could not save the output file.'
'''---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------'''
def callBalance(trd,date,*rest):
    t = acm.FTrade[trd.trdnbr]
    i = t.Instrument()
    redAmnt = -1*FInstrumentCACashflow.caRedemption(i)
    futCash = CallFuturePayments.futPayment(None, i.Oid(), str(date))
    callBalance = -1*(redAmnt - futCash)
    return callBalance
'''---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------'''
def getParty():
    partyList = []
    party = ael.Party.select()
    for p in party:
        partyList.append(p.ptyid)
    return partyList
'''---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------'''
ael_variables = [('partyList', 'Counterparty', 'string', getParty(), None, 1, 1),
                ('startDate', 'Start Date (YYYY-MM-DD)', 'date', None, ael.date_today().add_years(-1), 1),
                ('endDate', 'End Date (YYYY-MM-DD)', 'date', None, ael.date_today(), 1),
                ('fileName', 'File Path (including last "\\")', 'string', None, None, 1)
                ]
def ael_main(dict):
    print TimeSeries(dict['partyList'], dict['startDate'], dict['endDate'], dict['fileName'])
