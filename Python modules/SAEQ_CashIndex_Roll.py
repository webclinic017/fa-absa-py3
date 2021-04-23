"""
DESCRIPTION
    Date                : 2011-05-05
    Purpose             : Rolling of the members of the equity index 'ZAR/TRaCI' for predefined dates
    Department and Desk : Equities 
    Requester           : Shameer Sukha
    Developer           : Anil Parbhoo
    CR Number           : 643813
ENDDESCRIPTION
"""

import acm

def roll_members_of_ins_ZAR_TRaCI(eq_ins):

    runDate = acm.Time().DateToday()
        
    #runDate defined explicitly for testing only
    #runDate = acm.Time().DateFromYMD(2011,04,01)

    cal = acm.FCalendar['ZAR Johannesburg']
    
    workDay = not cal.IsNonBankingDay(cal, cal, runDate)
    
    firstOfMonth_of_runDate = acm.Time().FirstDayOfMonth(runDate)
    
    firstOfMonth_of_runDate_adj = cal.ModifyDate(cal, cal, firstOfMonth_of_runDate, 'Following')
  
    
    # define index_dict to map to the names of the corresponding instrumnets to calculate the fix rate of the members of the index 
    index_dict = {'ZAR/DEP/TRACI/1D' : 'ZAR-JIBAR-ON-DEP','ZAR/DEP/TRACI/3M' : 'ZAR-JIBAR-3M','ZAR/DEP/TRACI/6M' : 'ZAR-JIBAR-6M','ZAR/DEP/TRACI/12M': 'ZAR-JIBAR-12M'}    
    # empty rate_dict to eventually have deposit members as keys and calculate rate as the value
    rate_dict = {}



    for im in index_dict.keys():
        #print acm.FDeposit[im].Name(), acm.FRateIndex[index_dict[im]].Name()
        for p in acm.FRateIndex[index_dict[im]].Prices():
            if p.Market().Name() == 'SPOT':
                #print 'member', acm.FDeposit[im].Name(), 'index', acm.FRateIndex[index_dict[im]].Name(), p.Day(), 'rate', p.Settle() , p.Market().Name()
                rate_dict[im] = p.Settle()-0.10
                
    
    
    for im in rate_dict.keys():
        Dep = acm.FDeposit[im]
        Dep_rate = rate_dict[im]
        start = runDate
        
        #determine the end date based on the member instrument
        if im == 'ZAR/DEP/TRACI/3M':
            end = cal.ModifyDate(cal, cal, acm.Time().DateAddDelta(runDate, 0, 3, 0), 'Following')
        elif im == 'ZAR/DEP/TRACI/6M':
            end = cal.ModifyDate(cal, cal, acm.Time().DateAddDelta(runDate, 0, 6, 0), 'Following')
        elif im == 'ZAR/DEP/TRACI/12M':
            end = cal.ModifyDate(cal, cal, acm.Time().DateAddDelta(runDate, 0, 12, 0), 'Following')
        elif im == 'ZAR/DEP/TRACI/1D':
            end = cal.ModifyDate(cal, cal, acm.Time().DateAddDelta(runDate, 0, 0, 1), 'Following')
        
            
        #define l as the deposit legs to restate the start date, end date and the fix rate
        
        l = Dep.Legs().At(0)
        
        
        if im == 'ZAR/DEP/TRACI/1D':
            if workDay:
                l.StartDate(start)
                l.EndDate(end)
                l.FixedRate(Dep_rate)
                l.GenerateCashFlows(False, 0) 
                try:
                    
                    l.Commit()
                    print 'for runDate = ', runDate, ' restated the dates and the fix rate of ', Dep.Name(), 'from', start, 'to', end, 'rate', Dep_rate 

                except Exception, e:
                    print 'could not restate dates and fixed rate of', Dep.Name(), 'because', e.message
            
                
        elif im != 'ZAR/DEP/TRACI/1D': 
            
            if runDate == firstOfMonth_of_runDate_adj:
                l.StartDate(start)
                l.EndDate(end)
                l.FixedRate(Dep_rate)
                l.GenerateCashFlows(False, 0) 
                try:
                    
                    l.Commit()
                    print 'for runDate = ', runDate, ' restated the dates and the fix rate of ', Dep.Name(), 'from', start, 'to', end, 'rate', Dep_rate 

                except Exception, e:
                    print 'could not restate dates and fixed rate for', Dep.Name(), 'because', e.message
            

    
#set up run time variables



list_of_cash_indexes = ['ZAR/TRaCI']


ael_variables = [
('eq_ins', 'CashIndex',  'string', list_of_cash_indexes, 'ZAR/TRaCI', 1, 0, 'name of equity index that has deposits as members')
]


def ael_main(dict):
    myKeys = dict.keys()
    
    if dict['eq_ins'] == 'ZAR/TRaCI':
        roll_members_of_ins_ZAR_TRaCI(dict['eq_ins'])
    
    print "Completed Successfully ::"
    
