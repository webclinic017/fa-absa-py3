'''FAccounting: last updated on Thu Jan 06 11:48:13 2005. Extracted by Stowaway on 2005-02-02.'''
""" SubLedger:1.1.0 """

"""---------------------------------------------------------------------------------
 MODULE
     FAccounting - AEL functionality for Accounting.
     
     (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.
---------------------------------------------------------------------------------"""

'''
Purpose:                Added function for accrued interest on Repo/Reverse instruments. AccruedInterest_Repo_Instrument

Department and Desk:    PCG Creit DERIVATIVES
Requester:              Shanil Bisram
Developer:              Heinrich Cronje
CR Number:              636909
'''

import ael

#--------------------------------------------------------------------------------
# Class to use for passing the already calculated values between the accounting
# engine and the Accounting AEL module.
# OBS! The values can only be used for one date. When the event date changes, the
# variables must be emptied.
#--------------------------------------------------------------------------------
class accountingVariables:
    def __init__(self):
        self.ins_accrued = {}
        self.mtm = {}
        self.int_acc_pos = {}
        self.position = {}
        self.avg_price = {}
        self.mtm_fo = {}
        self.mtm_ins = {}
        self.mtm_bo = {}
        self.rpl = {}
        self.rpl_daily = {}
        self.int_acc_pos_recleg = {}
        self.int_acc_pos_payleg = {}
        self.upl_pos = {}

acc_vars=None
def init(*rest):
    globals()['acc_vars'] = accountingVariables()
    return 0
#--------------------------------------------------------------------------------
# Functions to use for calculating the the values to post. All functions that are
# called from the accounting engine must have the following parameters:
# - trade
# - the acquire day of the trade
# - date of the valuation
# - primary key of either a cash flow, payment or dividend
# - the python object holding the already calculated values
# - flag indicating whether the function is called from ASQl or python
# - *rest to make ASQL calls possible
#
# All of the functions are returning a list where the first position is the 
# calculated amount and the second is the currency that the amount is given in.
#
# The function names must be 30 characters or less
#
# The size of the module can not be larger than 32 768 bytes
#--------------------------------------------------------------------------------
######################

def test_func(t, run_day, cfwnbr, stored_values, ret, *rest):
    value = 1
    return ret_func(ret, value, t.curr.insid)


######################
def interest_accrued(t, run_day, cfwnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        value = t.interest_accrued(None, run_day, t.curr.insid)
    else:
        value = None
    return ret_func(ret, value, t.curr.insid)

def interest_accrued_payleg(t, run_day, cfwnbr, stored_values, ret, *rest):
    l = get_payleg(t, 1)
    if l and get_pos(t, run_day):
        value = abs(l.interest_accrued(None, run_day, l.curr.insid) * t.quantity)
        curr = l.curr.insid
    else:
        value = None
        curr = None
    return ret_func(ret, value, curr)
    
    
def interest_accrued_recleg(t, run_day, cfwnbr, stored_values, ret, *rest):
    l = get_payleg(t, 0)
    if l and get_pos(t, run_day):
        value = abs(l.interest_accrued(None, run_day, l.curr.insid) * t.quantity)
        curr = l.curr.insid
    else:
        value = None
        curr = None
    return ret_func(ret, value, curr)

def interest_accrued_pos(t, run_day, cfwnbr, stored_values, ret, *rest):
    pos = get_pos(t, run_day)
    i = t.insaddr
    if not pos:
        int_acc = None
    else:
        int_acc = get_stored_values(t, 'int_acc_pos')
        if not int_acc:
            key_string = t.insaddr.insid + t.prfnbr.prfid
            int_acc = i.interest_accrued(None, run_day, i.curr.insid, t.prfnbr)
            acc_vars.int_acc_pos[key_string] = int_acc
    return ret_func(ret, int_acc, i.curr.insid)

def interest_accrued_recleg_pos(t, run_day, cfwnbr, stored_values, ret, *rest):
    l = get_payleg(t, 0)
    if l and get_pos(t, run_day):
        int_acc = get_stored_values(t, 'int_acc_pos_recleg')
        if not int_acc:
            key_string = t.insaddr.insid + t.prfnbr.prfid
            int_acc = l.interest_accrued(None, run_day, l.curr.insid)
            acc_vars.int_acc_pos_recleg[key_string] = int_acc
            curr = l.curr.insid
    else:
        int_acc = None
        curr = None
    return ret_func(ret, int_acc, curr) 

def interest_accrued_payleg_pos(t, run_day, cfwnbr, stored_values, ret, *rest):
    l = get_payleg(t, 1)
    if l and get_pos(t, run_day):
        int_acc = get_stored_values(t, 'int_acc_pos_payleg')
        if not int_acc:
            key_string = t.insaddr.insid + t.prfnbr.prfid
            int_acc = l.interest_accrued(None, run_day, l.curr.insid)
            acc_vars.int_acc_pos_payleg[key_string] = int_acc
            curr = l.curr.insid
    else:
        int_acc = None
        curr = None
    return ret_func(ret, int_acc, curr)

def interest_bought(t, run_day, seqnbr, stored_values, ret, *rest):
    value = t.insaddr.interest_accrued(None, t.acquire_day, t.curr.insid) * t.quantity
    return ret_func(ret, value, t.curr.insid)

def interest_sold(t, run_day, seqnbr, stored_values, ret, *rest):
    value = abs(t.insaddr.interest_accrued(None, t.acquire_day, t.curr.insid) * t.quantity)
    return ret_func(ret, value, t.curr.insid)

def interest_settled(t, run_day, seqnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        value = abs(t.interest_settled(run_day.add_days(-1), run_day, t.curr.insid))
    else:
        value = None
    return ret_func(ret, value, t.curr.insid)

def deprec_premium(t, run_day, cfwnbr, stored_values, ret, *rest):
    return ret_func(ret, abs(t.deprec_premium(None, run_day, t.curr.insid)), t.curr.insid)

def original_premium(t, run_day, cfwnbr, stored_values, ret, *rest):
    return ret_func(ret, abs(t.original_premium(t.curr.insid)), t.curr.insid)

def premium(t, run_day, cfwnbr, stored_values, ret, *rest):
    return ret_func(ret, (t.premium), t.curr.insid)

def payment(t, run_day, seqnbr, stored_values, ret, *rest):
    payment = ael.Payment[int(seqnbr)]
    return ret_func(ret, payment.amount, payment.curr.insid)

def fee(t, run_day, seqnbr, stored_values, ret, *rest):
    return ret_func(ret, t.fee, t.curr.insid)

def nominal_amount(t, run_day, seqnbr, stored_values, ret, *rest):
    return ret_func(ret, t.nominal_amount(run_day, t.curr.insid), t.curr.insid)

def nominal_amount_td(t, run_day, seqnbr, stored_values, ret, *rest):
    td = ael.date_from_time(t.time)
    return ret_func(ret, t.nominal_amount(td, t.curr.insid), t.curr.insid)

def nominal_amount_instr(t, run_day, seqnbr, stored_values, ret, *rest):
    return ret_func(ret, t.nominal_amount(run_day, t.insaddr.curr.insid), t.insaddr.curr.insid)

def nominal_amount_instr_td(t, run_day, seqnbr, stored_values, ret, *rest):
    td = ael.date_from_time(t.time)
    return ret_func(ret, t.nominal_amount(td, t.insaddr.curr.insid), t.insaddr.curr.insid)

def nominal_amount_payleg(t, run_day, seqnbr, stored_values, ret, *rest):
    l = get_payleg(t, 1)
    if l:
        value = l.nominal_amount(run_day, l.curr.insid)
        curr = l.curr.insid
    else:
        value = None
        curr = None
    return ret_func(ret, value, curr)

def nominal_amount_recleg(t, run_day, seqnbr, stored_values, ret, *rest):
    l = get_payleg(t, 0)
    if l:
        value = l.nominal_amount(run_day, l.curr.insid)
        curr = l.curr.insid
    else:
        value = None
        curr = None
    return ret_func(ret, value, curr)

def nominal_amount_payleg_td(t, run_day, seqnbr, stored_values, ret, *rest):
    l = get_payleg(t, 1)
    td = ael.date_from_time(t.time)
    if l:
        value = l.nominal_amount(td, l.curr.insid)
        curr = l.curr.insid
    else:
        value = None
        curr = None
    return ret_func(ret, value, curr)

def nominal_amount_recleg_td(t, run_day, seqnbr, stored_values, ret, *rest):
    l = get_payleg(t, 0)
    td = ael.date_from_time(t.time)
    if l:
        value = l.nominal_amount(td, l.curr.insid)
        curr = l.curr.insid
    else:
        value = None
        curr = None
    return ret_func(ret, value, curr)

def projected_cf(t, run_day, cfwnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        cf = ael.CashFlow[int(cfwnbr)]
        value = cf.projected_cf(None, None, cf.legnbr.curr.insid) * t.quantity
    else:
        value = None
    return ret_func(ret, value, cf.legnbr.curr.insid)

def rpl(t, run_day, cfwnbr, stored_values, ret, *rest):
    return ret_func(ret, t.rpl(None, run_day, t.curr.insid, None, None, 3), t.curr.insid)

def rpl_pos(t, run_day, cfwnbr, stored_values, ret, *rest):
    rpl = get_stored_values(t, 'rpl')
    i = t.insaddr
    if not rpl:        
        key_string = t.insaddr.insid + t.prfnbr.prfid
        rpl = i.rpl(None, run_day, i.curr.insid, None, None, 3, None, t.prfnbr)
        acc_vars.rpl[key_string] = rpl
    return ret_func(ret, rpl, i.curr.insid)    

def rpl_daily(t, run_day, cfwnbr, stored_values, ret, *rest):
    return ret_func(ret, t.rpl(run_day.add_days(-1), run_day, t.curr.insid, None, None, 3), t.curr.insid)

def rpl_daily_pos(t, run_day, cfwnbr, stored_values, ret, *rest):
    rpl = get_stored_values(t, 'rpl_daily')
    i = t.insaddr
    if not rpl:        
        key_string = t.insaddr.insid + t.prfnbr.prfid
        rpl = i.rpl(run_day.add_days(-1), run_day, i.curr.insid, None, None, 3, None, t.prfnbr)
        acc_vars.rpl_daily[key_string] = rpl
    return ret_func(ret, rpl, i.curr.insid)

def upl(t, run_day, cfwnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        value = t.upl(None, run_day, t.curr.insid, None, None, None, 3)
    else:
        value = None
    return ret_func(ret, value, t.curr.insid)

def upl_pos(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    if get_pos(t, run_day):
        value = get_stored_values(t, 'upl_pos')
        if not value:
            key_string = t.insaddr.insid + t.prfnbr.prfid
            value = i.upl(None, run_day, i.curr.insid, None, None, None, 3, None, t.prfnbr)
            acc_vars.upl_pos[key_string] = value
    else:
        value = None
    return ret_func(ret, value, i.curr.insid)

def realised(t, run_day, cfwnbr, stored_values, ret, *rest):
    avg_price = get_stored_values(t, 'avg_price')
    if not avg_price:
        key_string = t.insaddr.insid + t.prfnbr.prfid
        avg_price = i.avg_price(run_day, t.curr.insid, 3, None, None, prf)
        acc_vars.avg_price[key_string] = avg_price
    real = (t.price - avg_price) * abs(t.quantity) * t.nominal_amount(None, t.curr.insid) / 100
    return ret_func(ret, real, t.curr.insid)

def net_value_buy(t, run_day, cfwnbr, stored_values, ret, *rest):
    return ret_func(ret, abs(t.original_premium(t.curr.insid)) + t.insaddr.interest_accrued(None, t.acquire_day, t.curr.insid) * t.quantity, t.curr.insid)

def net_value_sell(t, run_day, seqnbr, stored_values, ret, *rest):
    princ = abs(t.original_premium(t.curr.insid))
    int_sold = t.insaddr.interest_accrued(None, t.acquire_day, t.curr.insid) * abs(t.quantity)
    real = realised(t, run_day, seqnbr, stored_values, 0)
    nv = princ + int_sold - real
    return ret_func(ret, nv, t.curr.insid)

def end_cash_repo(t, run_day, seqnbr, stored_values, ret, *rest):
    return ret_func(ret, abs(t.interest_settled(None, run_day, t.curr.insid) - t.premium), t.curr.insid)

def mtm_value_fo(t, run_day, seqnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        value = t.mtm_value_fo(run_day, t.curr.insid, 3)
    else:
        value = None
    return ret_func(ret, value, t.curr.insid)

def mtm_value_fo_pos(t, run_day, seqnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        mtm = get_stored_values(t, 'mtm_fo')
        if not mtm:
            key_string = t.insaddr.insid + t.prfnbr.prfid
            mtm = i.mtm_value_fo(run_day, i.curr.insid, 3, None, None, prf)
            acc_vars.mtm_fo[key_string] = mtm
    else:
        mtm = None
    return ret_func(ret, mtm, i.curr.insid)

def mtm_value_bo(t, run_day, seqnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        value = t.mtm_value_bo(run_day, t.curr.insid, 3)
    else:
        value = None
    return ret_func(ret, value, t.curr.insid)

def mtm_value_bo_pos(t, run_day, seqnbr, stored_values, ret, *rest):
    i = t.insaddr
    if get_pos(t, run_day):
        mtm = get_stored_values(t, 'mtm_bo')
        if not mtm:
            key_string = t.insaddr.insid + t.prfnbr.prfid
            mtm = i.mtm_value_bo(run_day, i.curr.insid, 3, None, t.prfnbr)
            acc_vars.mtm_bo[key_string] = mtm
    else:
        mtm = None
    return ret_func(ret, mtm, i.curr.insid)

def mtm_value_ins(t, run_day, seqnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        value = t.mtm_value_ins(run_day, t.curr.insid, 3)
    else:
        value = None
    return ret_func(ret, value, t.curr.insid)

def mtm_value_ins_pos(t, run_day, seqnbr, stored_values, ret, *rest):
    i = t.insaddr
    if get_pos(t, run_day):
        mtm = get_stored_values(t, 'mtm_ins')
        if not mtm:
            key_string = t.insaddr.insid + t.prfnbr.prfid
            mtm = i.mtm_value_ins(run_day, i.curr.insid, 3, None, None, t.prfnbr)
            acc_vars.mtm_ins[key_string] = mtm
    else:
        mtm = None
    return ret_func(ret, mtm, i.curr.insid)

def projected_cf_payleg(t, run_day, seqnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        cf = ael.CashFlow[int(seqnbr)]
        if cf.legnbr.payleg == 0:
            value = None
        else:
            value = cf.projected_cf(None, None, cf.legnbr.curr.insid) * t.quantity
    else:
        value = None
    return ret_func(ret, value, cf.legnbr.curr.insid)

def projected_cf_recleg(t, run_day, seqnbr, stored_values, ret, *rest):
    if get_pos(t, run_day):
        cf = ael.CashFlow[int(seqnbr)]
        if cf.legnbr.payleg == 1:
            value = None
        else:
            value = cf.projected_cf(None, None, cf.legnbr.curr.insid) * t.quantity
    else:
        value = None
    return ret_func(ret, value, cf.legnbr.curr.insid)

def ret_func(ret, value, curr):
    if ret==1:
        if value == None:
            return None
        else:
            return [value, curr]
    else:
        if value:
            return value
        else:
            return 0.0

def get_payleg(trade, pay_flag):
    legs = trade.insaddr.legs()
    l = None
    for leg in legs:
        if leg.payleg == pay_flag:
            l = leg
            break
    return l

def get_stored_values(trade, attr):
    ret_value = None
    key_string = trade.insaddr.insid + trade.prfnbr.prfid
    attribute = getattr(acc_vars, attr) 
    if attribute.has_key(key_string):
        ret_value = attribute[key_string]
    return ret_value

def get_pos(t, run_day):
    i = t.insaddr
    pos = get_stored_values(t, 'position')
    prf = t.prfnbr
    if not pos:
        key_string = t.insaddr.insid + prf.prfid 
        pos = i.position(None, None, run_day, None, None, prf)
        acc_vars.position[key_string] = pos
    if pos == 0.0:
        return None
    else:
        return pos

'''
def CleanTrade(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value = i.clean_from_yield(t.value_day,None,None,t.price) * (t.nominal_amount(t.value_day)) / (-100)
    return value
    
def PremiumLessCleanTrade(t, run_day, cfwnbr, stored_values, ret, *rest):
    value = t.premium - CleanTrade(t, run_day, cfwnbr, stored_values, ret)
    return value
'''    
    
    
def CleanTrade(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value = i.clean_from_yield(t.value_day, None, None, t.price) * (t.nominal_amount(t.value_day)) / (-100)
    return ret_func(ret, value, t.curr.insid)    
#    return value
    
def PremiumLessCleanTrade(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value = t.premium - i.clean_from_yield(t.value_day, None, None, t.price) * (t.nominal_amount(t.value_day)) / (-100)
#    value = t.premium - CleanTrade(t, run_day, cfwnbr, stored_values, ret)    
    return ret_func(ret, value, t.curr.insid)    
#    return value    


def DAYINT(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    today = ael.date_today()
    yesterday = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)
        
    value = (((i.dirty_from_yield(today, None, None, i.mtm_price()) - i.clean_from_yield(today, None, None, i.mtm_price())) - (i.dirty_from_yield(yesterday, None, None, i.mtm_price()) - i.clean_from_yield(yesterday, None, None, i.mtm_price()))) * t.quantity * 10000)
    return ret_func(ret, value, t.curr.insid)    


def Clean_PL(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    today = ael.date_today()
 
    if t.value_day == i.exp_day:
    	value1 = t.quantity*1000000
    else:
    	vdate = ael.date_today().add_banking_day(ael.Instrument['ZAR'], 3)
    	if i.instype == 'Bond':
	    if t.value_day <= vdate:
	    	mtm = i.mtm_price(today)
	    else:
	    	mtm = i.forward_ytm(t.value_day)
	else:
	    mtm = i.mtm_price(today)
	
	value1 = i.clean_from_yield(t.value_day, None, None, mtm) * 10000 * t.quantity
	
    if t.value_day == i.exp_day:
    	value2 = t.quantity*-1000000
    else:
    	value2 = i.clean_from_yield(t.value_day, None, None, t.price) * 10000 * t.quantity * -1
	
    value = value1 + value2
    return ret_func(ret, value, t.curr.insid)    



def DepositsDueForSettlements(t, run_day, cfwnbr, stored_values, ret, *rest):
    if t.quantity < 0:
    	if ael.date_today() < t.value_day:
	    value = t.premium
	else:
	    value = 0.0
    else:
    	value = 0.0
	
    return ret_func(ret, value, t.curr.insid)    	
    
    
def LoansDueForSettlements(t, run_day, cfwnbr, stored_values, ret, *rest):
    if t.quantity >= 0:
    	if ael.date_today() < t.value_day:
	    value = t.premium
	else:
	    value = 0.0
    else:
    	value = 0.0
	
    return ret_func(ret, value, t.curr.insid)        
	

def RepoRate_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    legs = i.legs()
    value = 0
    for l in legs:
    	if l.type == 'Fixed':
	    value = l.fixed_rate
    
    return ret_func(ret, value, t.curr.insid)        



def Reval(t, run_day, cfwnbr, stored_values, ret, *rest):
    value = t.present_value()
    return ret_func(ret, value, t.curr.insid)


def NetReval_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):
    value = Reval(t, run_day, cfwnbr, stored_values, ret) + PreviousCFs_BSB(t, run_day, cfwnbr, stored_values, ret)
    return ret_func(ret, value, t.curr.insid)


def NetReval_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):
    value = Reval(t, run_day, cfwnbr, stored_values, ret) + PreviousCFs_Repos(t, run_day, cfwnbr, stored_values, ret)
    return ret_func(ret, value, t.curr.insid)
    
    
def RevalLessAccrued_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):
    value = NetReval_BSB(t, run_day, cfwnbr, stored_values, ret) - AccruedInterest_BSB(t, run_day, cfwnbr, stored_values, ret)
    return ret_func(ret, value, t.curr.insid)
 
 
def RevalLessAccrued_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):
    value = NetReval_Repo(t, run_day, cfwnbr, stored_values, ret) - AccruedInterest_Repo(t, run_day, cfwnbr, stored_values, ret)
    return ret_func(ret, value, t.curr.insid)
 

def Term(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value = t.value_day.days_between(i.exp_day, 'Act/365')
    return ret_func(ret, value, t.curr.insid)    
    
    
    
def DaysSinceStart(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    today = ael.date_today()

    if t.value_day > today:
    	value = 0
    else:
    	if t.value_day == today:
	    value = 1
	else:
	    if today < i.exp_day:
	    	value = t.value_day.days_between(today, 'Act/365') + 1
	    else:
	    	value = t.value_day.days_between(i.exp_day, 'Act/365')
	    
    return ret_func(ret, value, t.curr.insid)    
    
    


def Cash2_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value = i.ref_value * t.quantity
    return ret_func(ret, value, t.curr.insid)
    
    
    
def Cash2_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value = (t.premium * -1) + Interest_Repo(t, run_day, cfwnbr, stored_values, ret)
    return ret_func(ret, value, t.curr.insid)    



def Interest_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):
    value = t.premium + Cash2_BSB(t, run_day, cfwnbr, stored_values, ret) + Coupon(t, run_day, cfwnbr, stored_values, ret)
    return ret_func(ret, value, t.curr.insid)    
    
    

def Interest_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):
    value = t.premium * RepoRate_Repo(t, run_day, cfwnbr, stored_values, ret) * Term(t, run_day, cfwnbr, stored_values, ret)/36500 * -1
    return ret_func(ret, value, t.curr.insid)    
   
    

def Coupon(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    und = i.und_insaddr
    legs = und.legs()
    for l in legs:
    	CashFs = l.cash_flows()
        value = 0
        for cf in CashFs:
	    val = 0
	    if (cf.type != 'Fixed Amount') and (t.value_day < cf.end_day) and (cf.start_day < i.exp_day):
    	    	if IncCoupon(t, run_day, cf.cfwnbr, stored_values, ret) == 1:
		    val = cf.projected_cf() * t.quantity
		else:
		    val= 0
		    
	    value = value + val
	    
    return ret_func(ret, value, t.curr.insid)        



def IncCoupon(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    cf = ael.CashFlow[cfwnbr]
    if cf == None:
    	value = 0
    else:
    	cf_ex_date = cf.ex_coupon_date()
    	if (t.value_day < cf_ex_date) and (i.exp_day >= cf_ex_date):
    	    value = 1
    	else:
            value = 0

    return ret_func(ret, value, t.curr.insid)        
    
    
    
    
def CouponsToDate(t, run_day, cfwnbr, stored_values, ret, *rest):

#cf.pay_day == '' ? 0 : (cf.pay_day <= today ? X : 0)
#X = (t.IncCoupon = 1 ? projected_cf(cf) * t.quantity : 0)

    i = t.insaddr
    und = i.und_insaddr
    legs = und.legs()
    for l in legs:
    	CashFs = l.cash_flows()
        value = 0
        for cf in CashFs:
	    val = 0
	    if (cf.type != 'Fixed Amount') and (t.value_day < cf.end_day) and (cf.start_day < i.exp_day):
    	    	if cf.pay_day == '':
    	    	    val= 0
    	    	else:
    	    	    if cf.pay_day <= ael.date_today():
		    	if IncCoupon(t, run_day, cf.cfwnbr, stored_values, ret) == 1:
			    val = cf.projected_cf() * t.quantity
			else:
			    val= 0
		    else:
		    	val = 0
			
	    value = value + val

    return ret_func(ret, value, t.curr.insid)                



def PreviousCFs_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    today = ael.date_today()
    if t.value_day > today:
    	value = 0
    else:
    	if i.exp_day > today:
	    c2 = 0
	else:
	    c2 = Cash2_BSB(t, run_day, cfwnbr, stored_values, ret)
    	value = t.premium + CouponsToDate(t, run_day, cfwnbr, stored_values, ret) + c2
	
    return ret_func(ret, value, t.curr.insid)                



def PreviousCFs_BSB_SCash(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    if ael.date_today() >= i.exp_day:
    	value = 0
    else:
    	value = t.premium + CouponsToDate(t, run_day, cfwnbr, stored_values, ret)

    return ret_func(ret, value, t.curr.insid)
    
    
    
def PreviousCFs_Repos(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    today = ael.date_today()
    if t.value_day > today:
    	value = 0
    else:
    	if i.exp_day > today:
	    c2 = 0
	else:
	    c2 = (t.premium * -1 + (t.premium * RepoRate_Repo(t, run_day, cfwnbr, stored_values, ret) * Term(t, run_day, cfwnbr, stored_values, ret)/36500 * -1))
    	value = t.premium + c2

    return ret_func(ret, value, t.curr.insid)                



def PreviousCFs_Repos_SCash(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    if ael.date_today() >= i.exp_day:
    	value = 0
    else:
    	value = t.premium

    return ret_func(ret, value, t.curr.insid)    

    

def AccruedInterest_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):    
    value = Interest_BSB(t, run_day, cfwnbr, stored_values, ret) / Term(t, run_day, cfwnbr, stored_values, ret) * DaysSinceStart(t, run_day, cfwnbr, stored_values, ret)
    return ret_func(ret, value, t.curr.insid)
    
    
    
def AccruedInterest_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):    
    value = Interest_Repo(t, run_day, cfwnbr, stored_values, ret) / Term(t, run_day, cfwnbr, stored_values, ret) * DaysSinceStart(t, run_day, cfwnbr, stored_values, ret)
    return ret_func(ret, value, t.curr.insid)

def AccruedInterest_Repo_Instrument(t,date,*rest):
    date = ael.date(date)
    accInt = 0
    for l in t.insaddr.legs():
        for c in l.cash_flows():
            if c.type == 'Float Rate' and c.start_day <= date and c.end_day > date:
                accInt = accInt + (c.nominal_amount() * t.quantity) * c.period_rate(None, c.end_day) * (c.start_day.days_between(date, 'Act/365')+1) / 36500 * t.insaddr.curr.used_price(date, 'ZAR')
    return accInt

def AccruInt_Asset_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value1 = AccruedInterest_BSB(t, run_day, cfwnbr, stored_values, ret)
    if value1 < 0:
    	value = 0
    else:
    	if ael.date_today() >= i.exp_day:
	    value = 0
	else:
	    value = value1
    return ret_func(ret, value, t.curr.insid)
    
    

def AccruInt_Asset_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value1 = AccruedInterest_Repo(t, run_day, cfwnbr, stored_values, ret)
    if value1 < 0:
    	value = 0
    else:
    	if ael.date_today() >= i.exp_day:
	    value = 0
	else:
	    value = value1
    return ret_func(ret, value, t.curr.insid)
    
    

def AccruInt_Liab_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value1 = AccruedInterest_BSB(t, run_day, cfwnbr, stored_values, ret)
    if value1 > 0:
    	value = 0
    else:
    	if ael.date_today() >= i.exp_day:
	    value = 0
	else:
	    value = value1
    return ret_func(ret, value, t.curr.insid)
    
    
def AccruInt_Liab_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):
    i = t.insaddr
    value1 = AccruedInterest_Repo(t, run_day, cfwnbr, stored_values, ret)
    if value1 > 0:
    	value = 0
    else:
    	if ael.date_today() >= i.exp_day:
	    value = 0
	else:
	    value = value1
    return ret_func(ret, value, t.curr.insid)    
    


def TotalOpenDeposits_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):
    if t.quantity < 0:
    	value = PreviousCFs_BSB_SCash(t, run_day, cfwnbr, stored_values, ret)
    else:
    	value = 0
	
    return ret_func(ret, value, t.curr.insid)
    
    
    
def TotalOpenDeposits_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):
    if t.quantity < 0:
    	value = PreviousCFs_Repos_SCash(t, run_day, cfwnbr, stored_values, ret)
    else:
    	value = 0
	
    return ret_func(ret, value, t.curr.insid)
    
    
    
def TotalOpenLoans_BSB(t, run_day, cfwnbr, stored_values, ret, *rest):
    if t.quantity >= 0:
    	value = PreviousCFs_BSB_SCash(t, run_day, cfwnbr, stored_values, ret)
    else:
    	value = 0
	
    return ret_func(ret, value, t.curr.insid)
    
    
    
def TotalOpenLoans_Repo(t, run_day, cfwnbr, stored_values, ret, *rest):
    if t.quantity >= 0:
    	value = PreviousCFs_Repos_SCash(t, run_day, cfwnbr, stored_values, ret)
    else:
    	value = 0
	
    return ret_func(ret, value, t.curr.insid)            
   
