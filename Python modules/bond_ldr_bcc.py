'''
Purpose: Created. Based on bond_ldr. Updated to except date as input.
Department: PCG
Requester: Mthetho Mhlafu
Developer: Willie van der Bank
CR Number:  C286232 (20/04/2010)
'''
#C860581,863654 Peter Kutnik - fixed calculation for inflation-linked bonds, adjusted to include only trades live as of ex-coupon date in calc

import ael, time, acm #,FCalcUtil

def next_bond_paydte(ins,DDate,*rest):
    
    #ins = ael.Instrument[ins]
    RDate = ael.date(DDate)
    paydte = []
       
    for l in ins.legs():
        for cf in l.cash_flows():
            if cf.pay_day > RDate:
                if cf.type <> 'Fixed Amount':
                    paydte.append(cf.end_day)
                else:
                    paydte.append(cf.pay_day)
    if len(paydte) == 0:
        print 'Error, no flows detected for instrument %s' % ins.insid
    else:
    
        paydte.sort()
    
        next_paydte = paydte[0]
    
        return next_paydte

def next_bond_paydte_includeToday(ins,DDate,*rest):
    
    #ins = ael.Instrument[ins]
    RDate = ael.date(DDate)
    paydte = []
       
    for l in ins.legs():
        for cf in l.cash_flows():
            if cf.pay_day >= RDate:
                if cf.type <> 'Fixed Amount':
                    paydte.append(cf.end_day)
                else:
                    paydte.append(cf.pay_day)
    if len(paydte) == 0:
        print 'Error, no flows detected for instrument %s' % ins.insid
    else:
    
        paydte.sort()
    
        next_paydte = paydte[0]
    
        return next_paydte
        
def next_bond_Flow_includeToday(ins,DDate,*rest):

    RDate = ael.date(DDate)
    flows = []
       
    for l in ins.legs():
        for cf in l.cash_flows():
            if cf.pay_day >= RDate:
                if cf.type <> 'Fixed Amount':
                    flows.append((cf.end_day, cf))
                else:
                    flows.append((cf.pay_day, cf))
    
    flows.sort()    
    next_flow = flows[0]    
    return next_flow

def next_bond_excoupdte(ins,DDate,*rest):
    nextFlowInfo = next_bond_Flow_includeToday(ins, DDate, *rest)
    nextPayDate = nextFlowInfo[0]
    nextFlow = nextFlowInfo[1]
    if ins.ex_coup_method == 'AdditionalInfo':
        #find the closest past ex coupon date:
        closestRange = 5000
        closestIndex = -1
        exCoup = {}
        for i in range(1, 5):
            if len(ins.add_info('ExCoup%d' % i)) < 10:
                continue
            exCoup[i] = ael.date_from_string(str(nextPayDate.to_ymd()[0]) + ins.add_info('ExCoup%d' % i)[4:])
            while exCoup[i].days_between(nextPayDate) < 0:
                exCoup[i] = exCoup[i].add_years(-1)
            if exCoup[i].days_between(nextPayDate) < closestRange:
                closestRange = exCoup[i].days_between(nextPayDate)
                closestIndex = i
        if closestIndex == -1:
            raise IndexError('AdditionalInfo ex-coupon method selected for %s but no ExCoup additional info found' % ins.insid)
        return exCoup[closestIndex]
    elif ins.ex_coup_method == 'Business Days':
        return nextPayDate.add_period('-%s' % ins.ex_coup_period).adjust_to_banking_day(ins.curr, 'Following')
    elif ins.ex_coup_method == 'Calendar Days':
        return nextPayDate.add_period('-%s' % ins.ex_coup_period)
    elif ins.ex_coup_method == 'Proprietary':
        raise ValueError('%s: Ex coupon method "Proprietary" currently not supported. Contact IT to add support.' % ins.insid)
        #Proprietary ex-coupon calculation requires use of FCalcUtil module.
        #However, this module is inaccessible due to policy on safe modules.
        #Since there are no instruments with proprietary ex coupon method,
        #this does not need to be handled
        #exCoupUnit = ins.ex_coup_period[-1:]
        #exCoupCount = int(ins.ex_coup_period[:-1])
        
        #d = FCalcUtil.ex_coupon_day(nextFlow, ins, nextFlow.end_day, exCoupCount, exCoupUnit, None)
        #return d
        

def bond_ldr_date(ins,dte,DDate,*rest):
    
    #ins = ael.Instrument[ins]
    RDate = ael.date(DDate)
    paydte = []
    cashflows = []
    
    if ins.maturity_date() < RDate:  
        return
    
    for l in ins.legs():
        for cf in l.cash_flows():
            if cf.pay_day >= RDate:
                paydte.append(cf.pay_day)
                cashflows.append(cf)
    
    paydte.sort()
    
    next_paydte = paydte[0]
              
    enddte = []
    
    if next_paydte == dte:
        for cf in cashflows:
            if cf.type <> 'Fixed Amount' and cf.end_day >= RDate.add_banking_day(ins.curr, -5):
                enddte.append(cf.end_day)

    else:
        enddte.append(ael.date('1970-01-01'))
    
    enddte.sort()
           
    ex_period = int(ins.ex_coup_period[:-1])
    
    exdte = enddte[0].add_days(-ex_period)
    
    ldr_date = exdte.add_banking_day(ins.curr, -1)

    return ldr_date
    
    
#bond_ldr_date(ael.Instrument['ZAR/R153'],ael.date_today())
