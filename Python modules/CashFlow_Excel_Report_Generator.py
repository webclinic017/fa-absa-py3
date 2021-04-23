'''
Developer   : Bhavnisha Sarawan
Module      : CashFlow_Excel_Report_Generator
Date        : 09/05/2011
Description : Generates Excel Report for trades CashFlows
CR	    : C649904
'''

import ael, acm,  time, csv

from zak_funcs               import formnum
from FBDPCommon              import acm_to_ael

def ASQL(*rest):
    acm.RunModuleWithParameters('CashFlow_Excel_Report_Generator', 'Standard' )
    return 'SUCCESS' 

ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Trade Extract'}

ael_variables = [['trdnbr', 'Trade Number:', 'string', None, '0'],
                 ['date', 'Date:', 'string', ael.date_today(), ael.date_today(), 1]]

def BuildCashFlow(temp,t,date,outfile,*rest):    
    
    Legnbr      = ''
    Type        = ''
    FixedRate   = ''
    Nominal     = ''
    StartDay    = ''
    EndDay      = ''
    Days        = ''
    PayDay      = ''
    Proj        = ''
    Premium     = ''
    ValueDay    = ''
    StartDayTrade    = ''
    EndDayTrade      = ''
    
    
    # ########################## Trade Info ################################## 
    
    Our_Ref   = t.trdnbr
    Your_Ref  = t.your_ref
    TradeDate = ael.date_from_time(t.time)
    
    Notional = round(t.nominal_amount(), 2)
    ValueDay = t.value_day
    Premium  = round(t.premium, 2)
    
    for l in t.insaddr.legs():
        FixedRate = l.fixed_rate
        StartDayTrade = l.start_day
        EndDayTrade = l.end_day
        leg = acm.FLeg[l.legnbr]
        cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
        cashFlows = cashFlowQuery.Select().SortByProperty('PayDate', True) # The last argument is "ascending"

# ########################## Trade detail ##################################

    outline = 'Notional' + '\t '+ str(formnum(Notional)) + '\t '
    outline = outline + 'Fixed Rate' + '\t '+ str(FixedRate) + '\t '
    outline = outline + 'Premium' + '\t '+ str(formnum(Premium)) + '\n'
    outline = outline + 'Our Ref' + '\t '+ str(Our_Ref) + '\t '
    outline = outline + 'Trade Start Day' + '\t '+ str(StartDayTrade) + '\t '
    outline = outline + 'Value Day' + '\t '+ str(ValueDay) + '\t '
    outline = outline + 'Trade End Day' + '\t '+ str(EndDayTrade) + '\t '
    outfile.write(outline)
    outline = ''
    
    
     
   
    # ########################## Cash Flows ##################################
 
    header = '\n \n Type \t Nominal \t Start Day \t End Day \t Days \t Pay Day \t Proj \n'
    outfile.write(header)
    
    for cfacm in cashFlows:
        cf = acm_to_ael(cfacm)
        
        Type     = cf.type
        StartDay = cf.start_day
        EndDay   = cf.end_day
        try:
            Days = int(cf.start_day.days_between(cf.end_day))
        except:
            print cf.type
        PayDay   = cf.pay_day
        Proj     = round((cf.projected_cf()*t.quantity), 2)
        Nominal  = round((cf.nominal_amount()*t.quantity), 2)        

        outline2 = str(Type) + '\t' + str(formnum(Nominal)) + '\t' + str(StartDay) + '\t' + str(EndDay) + '\t' + str(Days) + '\t' + str(PayDay) + '\t' + str(formnum(Proj)) +'\n'
        outfile.write(outline2)
        outline2 = ''


        
def ael_main(dict):
    try:
        date = ael.date(dict['date'])
    except:
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Invalid Date!", 0)
        return 'Invalid Date!'
        
    ClientName = ''
    if dict['trdnbr'] != 0:
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            t = ael.Trade[int(trd)]
            fileName = 'F:/'+ str(t.trdnbr)+  ' - '+ date.to_string('%d %b %Y') + '.tab'
            outfile = open(fileName, 'w')
            BuildCashFlow(1, t, date, outfile)
    outfile.close()
    print 'Complete'
