'''
HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2013-06-12      CHNG0001099408  Heinrich Cronje                 Updated Numeric function. Try to get the
                                                                Number from the input value then move on
                                                                to test the string.

-------------------------------------------------------------------------------------------------------------
'''

import acm, ael

def Numeric(num):
    try:
        num = num.Number()
    except:
        num = num
        
    if str(num) in ('1.#QNAN', 'NaN', 'nan'):
        return 0
    else:
        return num


def trs_Proj_Amt_Pay(t, Date):

    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

    AmtList = []

    for l in t.Instrument().Legs():
        
        for cf in l.CashFlows():    
            cals = cf.Calculation()
            if l.PayLeg():
                if cf.PayDate()>= Date:
                    proj = Numeric(cals.Projected(cs, t))
                    AmtList.append(proj)
    sum = 0                
    for AmtVal in AmtList:
        sum += AmtVal

    return sum
    
def trs_Proj_Amt_Rec(t, Date):

    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

    AmtList = []

    for l in t.Instrument().Legs():
        
        for cf in l.CashFlows():    
            cals = cf.Calculation()
            if not l.PayLeg():
                if cf.PayDate()>= Date:
                    proj = Numeric(cals.Projected(cs, t))
                    AmtList.append(proj)
    sum = 0                
    for AmtVal in AmtList:
        
        sum += AmtVal

    return sum    

def pv_Amount_Pay(t, Date):
    
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

    AmtList = []

    for l in t.Instrument().Legs():
        
        for cf in l.CashFlows():    
            cals = cf.Calculation()
            if cf.PayDate()>= Date:
                if l.PayLeg():
                    pv = Numeric(cals.PresentValue(cs, t))
                    AmtList.append(pv)
    sum = 0                
    for AmtVal in AmtList:
        
        sum += AmtVal
     
    return sum    
  
def pv_Amount_Rec(t, Date):
    
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

    AmtList = []

    for l in t.Instrument().Legs():
        
        for cf in l.CashFlows():    
            cals = cf.Calculation()
            if cf.PayDate()>= Date:
                if not l.PayLeg():
                    pv = Numeric(cals.PresentValue(cs, t))
                    AmtList.append(pv)
    sum = 0                
    for AmtVal in AmtList:
        
        sum += AmtVal
     
    return sum      
    
#trd = acm.FTrade[19367008] 
#Date = acm.Time().AsDate(ael.date('24/02/2012'))

#trs_Proj_Amt_Rec(trd,Date)
#pv_Amount_Rec(trd,Date)
#print 'Proj Pay=', trs_Proj_Amt_Pay(trd,Date)       
#print 'Proj Rec=', trs_Proj_Amt_Rec(trd,Date) 
#print 'PV Pay=', pv_Amount_Pay(trd,Date)
#print 'PV Rec=', pv_Amount_Rec(trd,Date)
      
#print trs_Proj_Amt_Pay(trd)
#print pv_Amount_Pay(trd)
    
