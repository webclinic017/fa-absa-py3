
import acm
import ael
import Call_AdjDep_Call_Settle_Method
from ArenaFunctionBridge import cashflow_projected_cf


ael_gui_parameters = {'runButtonLabel':   '&&Update',
                      'hideExtraControls': True,
                      'windowCaption' : 'Backdate ratechanges'}
ael_variables=[
                ['rates', 'Rates', 'double', '', '', 0, 1, "Enter the new rate. If there are several changes, start with the first change and seperate each value with a comma (e.g. 7,9,8)"],
                ['dates', 'Dates', 'date', '', '', 0, 1, "Enter the date for the rate change. If there are several changes, type in the dates in the same order as the rates, seperated with a comma (e.g. 2008-01-05,2008-01-15,2008-01-25)"], 
                ['payday', 'Pay Day', 'date', '', ael.date_today().add_months(1).first_day_of_month().adjust_to_banking_day(ael.Instrument['ZAR']), 1, 0]
              ]

def backDate(object):
    acm.RunModuleWithParametersAndData('ABSABackDate', 'Standard', object ) 
    
def ael_main_ex(parameter, addData):
    #Assigning values two GUI variables
    object = addData.At('customData')    
    dates = parameter['dates']
    rates = parameter['rates']
    payday= parameter['payday']
    #Getting instruments from Trading Manager
    inslist = object.ExtensionObject().ActiveSheet().Selection().SelectedInstruments()
    #print inslist
    backDateRate(inslist, dates, rates, payday)

def backDateRate(inslist, dates, rates, payday):    
    for ins in inslist:
        #print ins
        date=dates[0]
        rate=rates[0]
        if ael.date(date)>=ael.date_today().first_day_of_month():
           changeRateCurrentPeriod(ins, dates, rates)
        else:
            leg=ins.Legs()[0]
            reset=ins.CurrentReset(ael.date(date))
            cashflows=leg.CashFlows()
        #Finding all cashflows that could be affected
            callrates=acm.FArray()
            fixedrates=acm.FArray()
            for cf in cashflows:
                if cf.CashFlowType() == "Call Fixed Rate Adjustable":
                    if ael.date(cf.EndDate())>ael.date(date):
                        callrates.Add((cf, cf.StartDate(), cashflow_projected_cf(cf.Oid())))
                        print "end", cf.EndDate(), 'date', date
                elif cf.CashFlowType() == "Fixed Rate Adjustable":
                    if ael.date(cf.EndDate())>ael.date(date):
                        fixedrates.Add((cf, cf.StartDate(), cashflow_projected_cf(cf.Oid())))
            print 'call:', callrates, 'fixed', fixedrates
            callrates.Sort()
            fixedrates.Sort()
            #Creating new cash flow
            for cf in callrates:
                cf=cf[0]
                if ael.date(cf.StartDate())<ael.date(reset.EndDate()):
                    cfnew=leg.CreateCashFlow()
                    cfnew.Apply(cf)
                    cfnew.StartDate=date
                    cfnew.EndDate=reset.EndDate()
                    cfnew.GenerateResets(0, rate)
                    if not leg.Reinvest():
                        cfnew.PayDate=payday
                    cfnew.Commit()
                    for r in cfnew.Resets():
                        if ael.date(r.EndDate())<=ael.date(reset.EndDate()):
                            orgrate=reset.FixingValue()
                            rc=r.Clone()
                            rc.FixingValue=rate-orgrate
                            #print orgrate, rate, rc.FixingValue()
                            r.Apply(rc)
                            r.Commit()
                    count = 1
                    while count<len(dates):
                        rate=rates[count]
                        date=dates[count]
                        count+=1
                        for r in cfnew.Resets():
                            if ael.date(r.StartDate())>=ael.date(date):
                                reset=ins.CurrentReset(r.StartDate())
                                orgrate=reset.FixingValue()
                                rc=r.Clone()
                                rc.FixingValue=rate-orgrate
                                r.Apply(rc)
                                r.Commit()

            func=acm.GetFunction('msgBox', 3)
            func("Success", "Backdated Rate change is successful", 0)
            Call_AdjDep_Call_Settle_Method.Call_Settle_Method(cfnew.Oid(), 'Backdated Rate Change')

            #Adjusting the Fixed Adjustable cashflows
            for cf in fixedrates:
                count = 0
                while count<len(dates):
                    date=dates[count]
                    rate=rates[count]
                    count+=1
                    for r in cf[0].Resets():
                        if ael.date(r.EndDate())<=ael.date(reset.EndDate()) and ael.date(r.StartDate())>=ael.date(date):
                            #print r.StartDate()
                            rc=r.Clone()
                            rc.FixingValue=rate
                            r.Apply(rc)
                            r.Commit()
                            #print r.FixingValue()
    
            #Adding reinvestment amount for the current month
            if leg.Reinvest():
                reinvest=leg.CreateCashFlow()
                reinvest.CashFlowType="Interest Reinvestment"
                amount=-cashflow_projected_cf(cfnew.Oid())
                reinvest.PayDate=cfnew.PayDate()
                reinvest.NominalFactor=1
                if len(fixedrates)>0:
                    if ael.date(fixedrates[0][1])<=ael.date(cfnew.EndDate()):
                        ael.poll()
                        cf=fixedrates[0][0]
                        reinvest.FixedAmount=amount+fixedrates[0][2]-cashflow_projected_cf(cf.Oid())
                else:
                    reinvest.FixedAmount=amount
                reinvest.Commit()
            #Adding reinvestment cashflows for all months after current month
            count=1
            if leg.Reinvest():
                while count<len(callrates):
                    cf=callrates[count][0]
                    if ael.date(cf.EndDate())<=ael.date_today().first_day_of_month():
                        ael.poll()
                        reinvest=leg.CreateCashFlow()
                        reinvest.CashFlowType="Interest Reinvestment"
                        reinvest.FixedAmount=callrates[count][2]-cashflow_projected_cf(cf.Oid())
                        if len(fixedrates)>=count:
                            if fixedrates[count][1]<cf.EndDate():
                                cff=fixedrates[count][0]
                                reinvest.FixedAmount=reinvest.FixedAmount()+fixedrates[count][2]-cashflow_projected_cf(cff.Oid())
                        reinvest.PayDate=cf.EndDate()
                        reinvest.NominalFactor=1
                        reinvest.Commit()
                    count+=1

def changeRateCurrentPeriod(ins, dates, rates):
    startDate=ael.date(dates[0])
    reset=ins.CurrentReset(ael.date(startDate))
    aelreset=ael.Reset[reset.Oid()]
    count = 0
    for d in dates:
        if aelreset.start_day==d:
            r_clone=aelreset.clone()
            r_clone.value=rates[count]
            r_clone.commit()
            ael.poll()
        elif aelreset.start_day<d:
            r_clone=aelreset.clone()
            r_clone.end_day=d
            r_new=aelreset.new()
            r_new.start_day=d
            r_new.day=d
            r_new.value=rates[count]
            r_new.commit()
            r_clone.commit()
            ael.poll()
        else:
            print "Date "+d+"not within this reset period, run the script again for next reset period."
            continue
        count+=1
        '''
        if reset.StartDate()==d:
            r_clone=reset.Clone()
            r_clone.FixingValue=rates[count]
            reset.Apply(r_clone)
            reset.Commit()
        elif ael.date(d)>ael.date(reset.StartDate()):
            r_clone=reset.Clone()
            r_clone.EndDate=d
            r_new=reset.new()
            r_new.Apply(reset)
            r_new.StartDate=d
            r_new.Day=d
            r_new.FixingValue=rates[0]
            r_new.Commit()
            reset.Apply(r_clone)
            reset.Commit()
        '''    
#backDate(acm.FInstrument['EUR/DEP/IR/080102-080218'],[(9.0,"2008-01-15"),(9.5,"2008-01-20"),(12,"2008-01-25")])

