"""
Description             : Work-around tool to correctly book NDS trades in Front Arena
Department and Desk     : Risk Solutions Group
Requester               : Opy Ramaremisa
Developer               : Mighty Mkansi
Change                  : CHNG0005201499 (2017-12-06: Initial implementation)
JIRA                    : ABITFA-5132 - Action Tool For Currency Swaps - Cashflow Netting

History
=======

2018-05-08  Mighty Mkansi  ABITFA-5389 - Xccy nett settle with reset nominal booking procedure
"""


import acm

def netFinalNominal(eii):
    instrument = eii.ExtensionObject().CurrentObject().Instrument()
    instrumentStartDate =  acm.Time.DateFromTime(instrument.StartDate())
    instrumentExpiryDate = instrument.ExpiryDate()
    today = acm.Time.DateToday()
    calendar = acm.FCalendar['ZAR Johannesburg']

    cfs_dict = {}
    resets = []
    for leg in instrument.Legs():

        if leg.NominalAtEnd():
            leg.NominalAtEnd(False) 
            
        if leg.NominalAtStart():
            leg.NominalAtStart(False)

        if leg.NominalScaling():
            for cashflow in leg.CashFlows():            
                if cashflow.CashFlowType() == 'Return': 
                    cfs_dict[cashflow.StartDate()] = cashflow.Oid()
                    
        if not leg.IsLocked():
            firstNominalFixingRate = leg.NominalFactor()
            
        for cashflow in leg.CashFlows():
            if  cashflow.CashFlowType() == 'Fixed Amount':
                try:
                    cashflow.Delete()
            
                except Exception as e:
                    print 'Error on cash flow %s' %cf, e
                    
            for reset in cashflow.Resets():
                if reset.ResetType() == 'Nominal Scaling':
                    resets.append(reset.Oid())
                        
                  
    for cf in cfs_dict.keys():
        cashflowObject = acm.FCashFlow[cfs_dict[cf]]        
            
        if cf != instrumentStartDate:
            try:
                cashflowObject.Delete()
                
            except Exception as e:
                print 'Error on cash flow %s' %cf, e
        else:
            cashflowObject.PayDate(instrumentExpiryDate)
            cashflowObject.EndDate(instrumentExpiryDate)
            for reset in cashflowObject.Resets():
                if reset.Day()> instrumentStartDate:                   
                    reset.Day(calendar.AdjustBankingDays(instrumentExpiryDate, -2))
                    cashflowObject.Commit()
                    try:
                        reset.Commit()
                    except Exception as e:
                        print 'Could not apply a fixing for reset date %s', reset.Day()
                
     
    for reset in resets:
        resetObject = acm.FReset[reset]
        if resetObject is not None:
            if str(resetObject.ClassName()) == 'FReset':
                resetObject.Day(calendar.AdjustBankingDays(resetObject.StartDate(), -2))
                resetObject.FixFixingValue(float(firstNominalFixingRate))        
                resetObject.Commit()        
                print 'Done fixing reset %s with value %s'%(reset, firstNominalFixingRate)                
   
    try:
        msg = 'Created a netted nominal exchange successfully'
        func = acm.GetFunction('msgBox', 3)
        ret = func('Info', msg, 0)
    except Exception as e:
        msg = 'Could not create a netted nominal exchange' + ' ' + e
        func = acm.GetFunction('msgBox', 3)
        ret = func('Info', msg, 0)
