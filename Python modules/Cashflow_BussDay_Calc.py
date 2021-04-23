'''
Purpose:        [This AEL regenerates individual cash flows and resets for specific trades and/or instruments to correct for non-business days.
                Where the IMM day method is used, the known Front issue (IMM does not take business days into account) is corrected.
                Only executes when all reset and cash flow calendars are ZAR]
Department:     [PCG]
Requester:      [Thalia Petousis]
Developer:      [Willie van der Bank]
CR Number:      [14/03/2012, 93192],[19/03/2012, 99666]
'''

import ael, acm
from MarkitWire_Listener import correctIMM_DateIssue

def AmendIns(ins, Date, validCal):
    invalidMessage = 'Invalid calendar on '
    change = 'False'
    cashflowText = 'Cash flow'
    resetText = 'Reset'
    
    for leg in ins.legs():
        
        if leg.pay_calnbr:
            if leg.pay_calnbr.calid not in validCal:
                return invalidMessage + 'leg.pay_calnbr'
        if leg.pay2_calnbr:
            if leg.pay2_calnbr.calid not in validCal:
                return invalidMessage + 'leg.pay2_calnbr'
        if leg.pay3_calnbr:
            if leg.pay3_calnbr.calid not in validCal:
                return invalidMessage + 'leg.pay3_calnbr'
                
        if leg.reset_calnbr:
            if leg.reset_calnbr.calid not in validCal:
                return invalidMessage + 'leg.reset_calnbr'
        if leg.reset2_calnbr:
            if leg.reset2_calnbr.calid not in validCal:
                return invalidMessage + 'leg.reset2_calnbr'
        if leg.reset3_calnbr:
            if leg.reset3_calnbr.calid not in validCal:
                return invalidMessage + 'leg.reset3_calnbr'
        if leg.reset4_calnbr:
            if leg.reset4_calnbr.calid not in validCal:
                return invalidMessage + 'leg.reset4_calnbr'
        if leg.reset5_calnbr:
            if leg.reset5_calnbr.calid not in validCal:
                return invalidMessage + 'leg.reset5_calnbr'
    
    legCal = ael.Instrument['ZAR']
    resetCal = ael.Instrument['ZAR']
    try:
        for leg in ins.legs():
            
            print leg.pay_day_method, leg.reset_day_method
            if leg.reset_day_method == 'IMM':
                resetMethod = 'Mod. Following'
            elif leg.reset_day_method != 'IMM':
                resetMethod = leg.reset_day_method

            if leg.pay_day_method == 'IMM':
                CFresetMethod = 'Mod. Following'
            elif leg.pay_day_method != 'IMM':
                CFresetMethod = leg.pay_day_method
                
            for cf in leg.cash_flows():
                if cf.end_day >= ael.date(Date):
                    for reset in leg.resets():
                        if reset.end_day >= ael.date(Date):
                            clone_Reset = reset.clone()
                            bussDay = clone_Reset.end_day.adjust_to_banking_day(resetCal, resetMethod)
                            if clone_Reset.end_day != bussDay:
                                resetText = resetText + ' end_day ' + str(clone_Reset.end_day) + ' set to ' + str(bussDay)
                                clone_Reset.end_day = bussDay
                                change = 'True'
                        
                            bussDay = clone_Reset.start_day.adjust_to_banking_day(resetCal, resetMethod)
                            if clone_Reset.start_day != bussDay:
                                resetText = resetText + ' start_day ' + str(clone_Reset.start_day) + ' set to ' + str(bussDay)
                                clone_Reset.start_day = bussDay
                                change = 'True'
                                
                            bussDay = clone_Reset.day.adjust_to_banking_day(resetCal, resetMethod)
                            if clone_Reset.day != bussDay:
                                resetText = resetText + ' day ' + str(clone_Reset.day) + ' set to ' + str(bussDay)
                                clone_Reset.day = bussDay
                                change = 'True'
                                
                        if change == 'True':
                            clone_Reset.commit()
                            print resetText + ' amended.'
                            change = 'False'
                            resetText = 'Reset'
                        
                    cfClone = cf.clone()
                    bussDay = cf.end_day.adjust_to_banking_day(legCal, CFresetMethod)
                    if  bussDay != cf.end_day:
                        cashflowText = cashflowText + ' end_day ' + str(cf.end_day) + ' set to ' + str(bussDay)
                        cfClone.end_day = bussDay
                        change = 'True'
                        
                    bussDay = cf.start_day.adjust_to_banking_day(legCal, CFresetMethod)
                    if  bussDay != cf.start_day:
                        cashflowText = cashflowText + ' start_day ' + str(cf.start_day) + ' set to ' + str(bussDay)
                        cfClone.start_day = bussDay
                        change = 'True'
                        
                    bussDay = cf.pay_day.adjust_to_banking_day(legCal, CFresetMethod)
                    if  bussDay != cf.pay_day:
                        cashflowText = cashflowText + ' pay_day ' + str(cf.pay_day) + ' set to ' + str(bussDay)
                        cfClone.pay_day = bussDay
                        change = 'True'
                        
                    if change == 'True':
                        cfClone.commit()
                        print cashflowText + ' amended.'
                        change = 'False'
                        cashflowText = 'Cash flow'
        return 'Done.'
    except:
        return 'Error on above trade!'
                        
def filters():
    filters = []
    for f in ael.TradeFilter:
        filters.append(f.fltid)
    filters.sort()
    return filters

ael_variables = [('InsID', 'Instrument', acm.FInstrument, [], '', 0, 1, 'Multiple instrument IDs can be entered, eg: "ID1,ID2,ID3".'),
                 ('Trds', 'Trades', 'string', None, None, 0, 0, 'Multiple trade numbers can be entered, eg: "123,456,789".'),
                 ('tf', 'TradeFilter', 'string', filters()),
                 ('RunDate', 'Date', 'string', '', '', 0, 0, 'Leave blank to run for todays date')]
#('valCalendars','Valid calendars',acm.FCalendar, [], '', 0, 1, 'Multiple calendars can be entered, eg: "Cal1,Cal2,Cal3".')

def ael_main(dict):
    validCal = []
    '''
    for cal in dict['valCalendars']:
        print cal.Name()
        validCal.append(cal.Name())
    '''
    validCal.append('ZAR Johannesburg')
    date = dict['RunDate']
    if dict['Trds'] != '':
        trds = dict['Trds'].split(',')
        for trd in trds:
            aeltrd = ael.Trade[int(trd)]
            ins = aeltrd.insaddr
            print 'Trade', int(trd)
            print AmendIns(ins, date, validCal)
            
    elif dict['tf'] != '':
        Processed = []
        tf = ael.TradeFilter[dict['tf']]
        for aeltrd in tf.trades():
            ins = aeltrd.insaddr
            if ins.insid not in Processed:
                print 'Trade', aeltrd.trdnbr
                print AmendIns(ins, date, validCal)
                Processed.append(ins.insid)

    elif dict['InsID'] != '':
        for acmins in dict['InsID']:
            ins = ael.Instrument[acmins.Oid()]
            print 'Instrument', ins.insid
            print AmendIns(ins, date, validCal)
