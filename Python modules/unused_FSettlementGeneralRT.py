""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementGeneralRT - Module including all functions common to the 
                         Settlement population and update process.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module stores those functions which are common to the Settlement
    population and update process.
    
DIARY    

----------------------------------------------------------------------------"""

import ael, time, FSettlementGeneral, FSettlementParams, FSettlementAMB
import FSettlementGeneral2, FSettlementGeneral3


param = FSettlementParams.get_default_params()

verbosity = param.verbosity

UPDATED = ael.enum_from_string('SettlementStatus', 'Updated')
RECALLED = ael.enum_from_string('SettlementStatus', 'Recalled')

# Valid trade statuses
tr_status = param.status

#
days_curr = param.days_curr.values()

# End_day, offently used for dividends
end_day = ael.date_today().add_banking_day(\
                ael.Instrument[param.acc_curr], max(days_curr))

# no update of Settlement is done in this statuses
noupdate_stl_status = ['Closed']

def cfs_from_tr(tr, tr_c=None, ins_c=None, leg_dict=None, comb_member = None, coupon_check = 1):
    '''Returns a list with cash flows for a certain trade.
    Coupon candidates for primary_issuance trade are not included if 
    coupon_check flag is on. Note when using leg_dict all cfs will be returned.'''

    cf_list = []
    use_amb = 0
    tr_c = set_c(tr_c, tr, 'Trade')
    if is_trade(tr_c) and not FSettlementGeneral.is_collateral_trade(tr_c):
        instr = tr_c.insaddr #caution, combination trade instr and ins_c member
        if ins_c:
            if ins_c.insaddr == instr.insaddr:
                instr = ins_c
                use_amb = 1
            elif instr.instype != "Combination":
                pr = "wrong ins_c %s (!= %s) input in cfs_from_tr (Error)" % (ins_c.insid, instr.insid)
                log(2, pr)
                
        if instr:            
            if instr.instype == 'Combination':
                if param.handle_combination_cash_flows:
                    if comb_member:
                        instr = comb_member
                    for cf in instr.cash_flows():
                        cf_list.append(cf)
            elif instr.instype != 'Combination' and use_amb:
                cf_list = FSettlementGeneral3.amb_get_cf_from_leg(leg_dict, tr, 0)
            else:
                for leg in instr.legs(): #todo 95
                    for cf in leg.cash_flows(): #todo 96                        
                        if coupon_check:
                            if not FSettlementGeneral.is_coupon(tr, cf, tr_c, cf, leg):
                                cf_list.append(cf)
                        else:
                            if FSettlementGeneral.paydayOK(cf.pay_day, cf, 1, cf.type): #Filter out irrelevant cash flows.
                                cf_list.append(cf)
    else:
        log(1, 'cfs_from_trade: the input trade is None or \
                                this is a collateral trade')                                      
    return cf_list

def check_coupon(ins, cf):
    ''' NOT USED! Adapt to ent_c when used.'''
    if ins.instype in FSettlementGeneral.coupon_types and \
        (cf.type == 'Fixed Rate' or FSettlementGeneral2.is_float_coupon(cf)):
        return 1
    else:
        return 0

def coupons_from_tr(tr, instr, ins_c=None, leg_dict=None, underlying_instrument = None):
    '''Returns coupons from the trade instrument or instr. Refer also to cfs_from_tr.
    Note instr must not be ins_c! Careful with underlying instruments!
    '''
    cf_list = []
    if not instr:
        ins_c = None
        leg_dict = None
        if not tr:
            log(2, 'coupons_from_tr: no trade deployed')
        else:
            instr = tr.insaddr #todo??
    elif instr and ins_c:
        if instr.insaddr != ins_c.insaddr:
            pr = "wrong ins_c %s (!= %s) input in coupons_from_tr (Error)" % (ins_c.insid, instr.insid)
            log(2, pr)
            ins_c = None
            leg_dict = None
            
    if instr:
        if leg_dict and instr.instype != 'Combination':
            cf_list = FSettlementGeneral3.amb_get_cf_from_leg(leg_dict, tr, 1)
        elif instr.instype == 'Combination' and \
           param.handle_combination_cash_flows == 1:
            for cf in instr.cash_flows():
                if FSettlementGeneral.is_coupon(tr, cf, tr, cf): # no leg here!
                    cf_list.append(cf)
        else:
            for leg in instr.legs():#todo 95
                for cf in leg.cash_flows(): #todo 96
                    if FSettlementGeneral.is_coupon(tr, cf, tr, cf, leg, underlying_instrument):
                        cf_list.append(cf)
            if underlying_instrument:
                for leg in underlying_instrument.legs():
                    for cf in leg.cash_flows():
                        if FSettlementGeneral.is_coupon(tr, cf, tr, cf, leg, underlying_instrument):
                            cf_list.append(cf)
                
    return cf_list

    
# CREATE FUNCTIONS     
# paydayOK uses flag = 1 meaning that +/- banking days are used
# this can leed to that a closed and archived settlement 
# that is x days old can theoreticaly be added because of
# the fact that someone does some amendemends
# create function need to check if the entity is already stored in
# in the settlement table

def create_cf(cf, tr, inStatus, create = 0, cf_c=None, tr_c=None, leg_c=None, ins_c = None, append_trans = 1):
    '''Creates a settlement row record for a CashFlow. If a tr is stated only a \
    Settlement row for that cf/trade will be created.
    leg_c, res_c seem not to be needed.'''
    ret = None
    trades = []
    single_trade = 0 #if the trade is input
    log(2, 'FSettlementGeneralRT.create_cf:')
    cf_c = set_c(cf_c, cf, 'CashFlow')
    tr_c = set_c(tr_c, tr, 'Trade')
    leg = cf.legnbr
    if leg_c:
        leg = leg_c
    instrument = leg.insaddr
    if ins_c:
        instrument = ins_c
    if is_trade(tr_c):
        # trade deployed since it was missing in settlement table
        # or when creating a new trade
        if not FSettlementGeneral.enter_cashflow(tr_c, cf, cf_c):
            return
        single_trade = 1
        pr = 'Trade %d: Create settlement for CF' % (tr.trdnbr)
        log(2, pr)
    else:
        tr = None

    if is_cf(cf_c):
        if single_trade:
            if FSettlementGeneral.is_coupon(tr, cf, tr_c, cf_c, leg) and not\
               FSettlementGeneral2.enter_coupon(cf, tr_c, cf_c):
                return
        else:
            if FSettlementGeneral.is_coupon(tr, cf, tr_c, cf_c, leg) and not\
               FSettlementGeneral2.enter_coupon(cf, None, cf_c):
                return
    else:
        log(0, 'create cf: input Not CF')

    corrected_setl = 0
    correct_trade = FSettlementGeneral2.is_correction_trade(tr_c)
    if correct_trade:
        corrected_setl = FSettlementGeneral2.get_corrected_setl(cf, tr, None)

    if is_cf(cf_c):
        # paydayOK with flag 1 = intervall between -days back and bankingday
        if cf_c.pay_day and FSettlementGeneral.paydayOK(cf_c.pay_day, cf, 1, ''):
            if cf.projected_cf() != 0:
                # ael dependency
                # how is Cash Flow table application taking care of spot days?
                if single_trade:
                    # Batch job calls this code
                    trades.append(tr)
                else:
                    # AMB module calls this code
                    trades = FSettlementGeneral.get_tradelist_cf(cf.cfwnbr)
            else:
                pr = 'CF %d not added due to zero amount' % (cf.cfwnbr)
                log(2, pr)            

    for tr in trades: #no tr_c from here!
        if FSettlementGeneral3.is_deposit_and_openEnded(tr, cf_c, create):
            continue
        if tr.status in tr_status:
            if FSettlementGeneral.is_coupon(tr, cf, tr, cf_c, leg):
                sec = FSettlementGeneral2.get_sec_trade(tr.trdnbr, instrument)
                if sec and FSettlementGeneral2.enter_coupon(cf, tr, cf_c):
                    FSettlementGeneral2.update_position_cover(sec, tr, leg, cf_c)
            else:
                ok = FSettlementGeneral.create_selection(cf.cfwnbr,\
                                    'CashFlow', tr.trdnbr, None, None, append_trans)
                if ok:
                    if FSettlementGeneral.enter_cashflow(tr, cf, cf_c) and \
                       FSettlementGeneral.is_prevent_cash_flow(cf) == False:
                        status = 'New'
                        if inStatus and inStatus != status:
                            status = inStatus
                        setl = ael.Settlement.new()
                        ret = FSettlementGeneral.cf_creation(setl, cf, status, 0, tr, 1, 0, 0, corrected_setl, leg, cf_c, tr, append_trans)
                else:
                    pr='CashFlow %d has already been added' % cf.cfwnbr
                    log(2, pr)
        else:
            pr = 'Trade %d has invalid status (%s), no cf creation' % (tr.trdnbr, tr.status)
            log(2, pr)
    return ret


def create_reset(res, res_c, cf, ins_c=None, leg_c=None, cf_c=None):
    ''' '''
    if cf:
        log(1, 'create_reset:')
        update_reset(res, {'update': 'reset'}, cf, ins_c, leg_c, cf_c, res_c)
    return


def create_divs(insaddr):
    '''Returns a list with dividens for an instrument.
    Seems NOT to be used in 3_2_fix branch!!! 
    div_list = []
    if insaddr:
        inst =  ael.Instrument[insaddr]
        if inst:
            divs = inst.historical_dividends()            
            for div in divs:
                div_list.append(div)
    else:
        log(0, 'create_divs: input (insaddr) is none')
    return div_list
    '''
            
def create_div(div, tr, inStatus, ins_c=None):
    '''Creates a settlement row record for a Dividend. Dividends payday must be\
    in intervall +/- banking days. 
    tr can be tr_c
    div can be div_c'''

    setl = None
    trades = []
    status = 'New'
    ins_c = set_c(ins_c, div.insaddr, 'Instrument')
    if is_div(div):
        if FSettlementGeneral.paydayOK(div.pay_day, div, 1, ''):
            if div.dividend != 0:                
                if is_trade(tr):
                    # the trade is deployed via insert trade
                    trades.append(tr)
                else:
                    trades = FSettlementGeneral.get_tradelist_div(div.seqnbr)
            else:
                pr = 'Dividend %d not added due to zero amount' % (div.seqnbr)
                log(1, pr)                
    else:
        log(1, 'create_div: Input not a dividend entity')

    for tr in trades:
        if tr.status in tr_status:
            if is_div_related(tr) and FSettlementGeneral.enter_dividend(tr, div):
                if (FSettlementGeneral3.is_equity_swap(tr.insaddr) or \
                is_combination_with_eq_swap(tr.insaddr, div)) and not \
                trade_has_dividend_settlement_record(tr, div):
                    create_eq_swap_dividend(tr, [div])
                else:
                    sec = FSettlementGeneral2.get_sec_trade(tr.trdnbr, ins_c)
                    if sec and FSettlementGeneral2.check_security([sec]):
                        FSettlementGeneral2.update_position_cover(sec, tr, None, None)
        else:
            pr='No dividend of trade %d will be added due to the trade status'\
                 % (tr.trdnbr)
            log(1, pr)
    return 

def is_combination_with_eq_swap(comb_ins, div):
    ret = False
    if comb_ins.instype == 'Combination':
        links = comb_ins.combination_links()
        for link in links:
            ins = FSettlementGeneral.get_combination_member(link)
            if ins and ins.instype == 'EquitySwap' and div.insaddr and \
               ins.insaddr == div.insaddr.insaddr:
                ret = True
                break
    return ret


def create_payment(pay, inStatus, pay_c=None, tr_c=None, append_trans = 1):
    'Creates a settlement for a Additional Payment. APs payday must be\
    in intervall +/- banking days' 

    setl = None
    exist = 0
    ok = 0 # proceede with creation    
    pay_c = set_c(pay_c, pay, 'Payment')
    tr_c = set_c(tr_c, pay_c.trdnbr, 'Trade')
    ret = None
    
    if inStatus == None:
        if inStatus == '':
            inStatus = 'New'
    
    if is_pay(pay_c):
        tr = pay_c.trdnbr
        if tr_c.status in tr_status or \
            (tr_c.status == 'Terminated' and pay_c.type == 'Termination Fee'):
            ok = 1        
        else:                
            pr = 'Payment %d not added! Trade status %s' % (pay.paynbr, tr_c.status)
            log(1, pr)

        corrected_setl = 0
        input_str = ''
        correct_trade = FSettlementGeneral2.is_correction_trade(tr_c)
        if correct_trade:
            input_str = FSettlementGeneral3.get_input_string(pay, tr)#todo tr_c, all pay_c
            corrected_setl = FSettlementGeneral2.get_corrected_setl(pay, tr, None)
        if ok and pay_c.type not in FSettlementGeneral.invalid_payment_types:
            if pay_c.payday and FSettlementGeneral.\
               paydayOK(pay_c.payday, pay, 1, ''):
                if pay_c.amount != 0:
                    ok = FSettlementGeneral.create_selection(\
                        pay_c.paynbr, 'Payment', tr.trdnbr, None, None, append_trans)
                    if ok:
                        setl = ael.Settlement.new()
                        ret = FSettlementGeneral.payment_creation(setl, pay_c, 'New', 0,
                                                            tr_c, 1, corrected_setl, input_str, append_trans)
                    else:
                        pr='Payment %d has already been added' % (pay.paynbr)
                        log(1, pr)
                else:
                    pr = 'create_payment: zero payments are not added!'
                    log(1, pr)                                      
        elif pay_c.type in FSettlementGeneral.invalid_payment_types:
            pr = 'Payment %d not added, invalid type (%s)' % (pay.paynbr, pay.type)
            log(1, pr)
    else:
        pr = 'create_payemnt: Payment not added, input is not Payment entity'
        log(1, pr)
                
    return ret

    
def get_settlements(tr, combination_member=None, typ='', include=1, comb_link_removed = False):    
    return FSettlementGeneral2.get_settlements2(tr, combination_member, typ, include, comb_link_removed)    
    
    
def create_premium_t(tr, typ, inStatus, defProcedure=0, comblink=None, tr_c=None, ins_c=None, append_trans = 1, create_premium_2 = 1):
    '''Creates a settlement row record of type premium, fee or security nominal.
    Input parameter defProcedure restricts generation of the sec nom.
    If defProcedure is 1 the sec nom will not be generated at the same
    time as the premium.'''  
    ret = None
    tr_c = set_c(tr_c, tr, 'Trade')
    ins_c = set_c(ins_c, tr.insaddr, 'Instrument')
    if FSettlementGeneral.is_collateral_trade(tr_c) and not typ=='End Security':
        typ = 'Security Nominal'
    
    types = ['Premium', 'Fee', 'Security Nominal', 'End Security']
    type_ok = 0
    combination_member = FSettlementGeneral.get_combination_member(comblink)
    
    if combination_member and not param.handle_combination_cash_flows and typ != 'Premium':
        return ret
    
    if typ and (typ in types or \
        (combination_member and combination_member.instype == 'Curr' and typ=='Premium 2')):
        type_ok = 1
    else:
        log(1, 'create_premium_t: Wrong type of the trade deployed')

    if inStatus == None:
        if inStatus == '':
            inStatus = 'New'
            
    if is_trade(tr_c) and type_ok:
        corrected_setl = 0
        correct_trade = FSettlementGeneral2.is_correction_trade(tr_c)
        if correct_trade:
            corrected_setl = FSettlementGeneral2.get_corrected_setl(None, tr, typ)  
        if tr_c.status in tr_status:
            try:
                sel = get_settlements(tr.trdnbr, combination_member, typ, 1) ### IV or VI
            except:
                sel = []

            SN = 'Security Nominal'
            ok1 = FSettlementGeneral.create_selection(tr.trdnbr, typ, tr.trdnbr, sel, combination_member, append_trans)
            if (typ != 'Fee'):
                sel2 = get_settlements(tr.trdnbr, combination_member, SN, 1) ### IV or VI
                ok2 = FSettlementGeneral.create_selection(tr.trdnbr, SN, tr.trdnbr, sel2, combination_member)
            if ok1:
                amount = 0
                day = tr_c.value_day
                if typ == 'Fee':
                    amount = FSettlementGeneral2.get_fee(tr_c, corrected_setl)
                elif typ == 'Premium':
                    amount = FSettlementGeneral2.get_premium(tr_c, corrected_setl)
                elif typ == 'Security Nominal':
                    day = tr_c.acquire_day
                    amount = FSettlementGeneral.calc_security_nominal(tr_c, comblink, corrected_setl, 0, ins_c)
                elif typ == 'End Security':
                    amount = FSettlementGeneral.calc_end_security(tr_c, comblink, corrected_setl, ins_c)
                    day = end_security_value_day(tr_c, combination_member, ins_c)
                elif typ == 'Premium 2':
                    amount = FSettlementGeneral2.get_premium2(tr_c, corrected_setl, comblink)
                    
                if FSettlementGeneral.paydayOK(day, tr, 1, typ):
                    corrected_sn = FSettlementGeneral2.get_corrected_setl(None, tr_c, SN)
                    if typ=='Premium' and ok2 and defProcedure==0 and \
                       FSettlementGeneral.has_security_nominal(tr):
                        # Add premium if non zero
                        if amount != 0:
                            setl = ael.Settlement.new()
                            ret = FSettlementGeneral.premium_creation(\
                                  setl, 0, inStatus, 0, tr, 1, typ, comblink, corrected_setl, tr_c, ins_c, append_trans)
                        else:
                            pr = 'Zero premium for trade %d not added!' % (tr.trdnbr)
                            log(1, pr)
                        if is_correction_trade_handling(tr_c, ins_c, corrected_sn):
                            setl2 = ael.Settlement.new()
                            ret = FSettlementGeneral.premium_creation(\
                            setl2, 0, inStatus, 0, tr, 1, SN, comblink, corrected_sn, tr_c, ins_c, append_trans)
                        # Add Security Nominal if non zero
                        elif FSettlementGeneral.calc_security_nominal(tr_c, None, corrected_sn, 0, ins_c) != 0:
                            # no sec nom correct
                            setl2 = ael.Settlement.new()
                            ret = FSettlementGeneral.premium_creation(\
                                  setl2, 0, inStatus, 0, tr, 1, SN, comblink, corrected_sn, tr_c, ins_c, append_trans)
                        else:
                            pr = 'Zero security nominal for trade %d not added!' % (tr.trdnbr)
                            log(1, pr)
                    elif amount != 0 or (is_correction_trade_handling(tr_c, ins_c, corrected_sn) and typ == 'Security Nominal'):
                        setl = ael.Settlement.new()
                        ret = FSettlementGeneral.premium_creation(\
                              setl, 0, inStatus, 0, tr, 1, typ, comblink, corrected_setl, tr_c, ins_c, append_trans)
                        if tr.insaddr:
                            if tr.insaddr.instype=='Curr':
                                corrected_premium2 = 0
                                if correct_trade:
                                    corrected_premium2 = FSettlementGeneral2.get_corrected_setl(None, tr, typ)#typ
                                setl = ael.Settlement.new()
                                if create_premium_2:
                                    ret = FSettlementGeneral.premium_creation(setl, 0, inStatus, 0, tr, 1,\
                                    'Premium 2', comblink, corrected_premium2, tr_c, tr.insaddr, append_trans) #ins_c ok?
                    else:
                        pr = 'Zero %s for trade %d not added!' % (typ, tr.trdnbr)  
                        log(1, pr)                        
            else:
                log_str= 'Trade %d (%s) already in Settlement table' % (tr.trdnbr, typ)
                log(2, log_str)    
        else:
            log_str = '%s not added, wrong trade status' % (typ)
            log(2, log_str)    
    return ret

def is_div(div):
    'Checks if the input has record_type CashFlow'
    ok = 0
    
    if div and div.record_type == 'Dividend':
        ok = 1  
    return ok
    
    
def is_div_related(tr):
    'Checks if the instrument of the trade is Stock.'

    ok = 0
    if is_trade(tr):
        inst = tr.insaddr
        if inst and (inst.instype == 'Stock' or FSettlementGeneral3.is_equity_swap(inst) or \
        FSettlementGeneral3.is_combination_with_dividend(inst)):
            ok = 1
    log(5, "is_div_related: %d" % (ok))
    return ok


def is_cf(cf):
    'Checks if the input has record_type CashFlow'
    ok = 0
    
    if cf and cf.record_type == 'CashFlow':
        ok = 1  
    return ok
    
    
def is_pay(pay):
    'Checks if the input has record_type Payment'
    ok = 0
    
    if pay and pay.record_type == 'Payment':
        ok = 1  
    return ok


def is_trade(tr):
    'Checks if the input has record_type Trade'
    ok = 0
    
    if tr and tr.record_type == 'Trade' and not tr.aggregate:
        ok = 1
    return ok

def print_diff(list):
    'Prints differences deployed in a list'
    
    pr = ''
    if list and len(list):
        for a in list:
            pr = '%s differ' % (a)
            log(1, pr)
    return

# UPDATE FUNCTIONS
# All update function need to concider pre, postsetlement statuses!!!

def update_accounts(account, account_old, diff_dict, party_update = None, ptyid = ''):
    '''Updates settlement rows containing the account-info either \
    in party or acquirer fields. Input accounts are entity classes.'''

    pr = "update_accounts:"
    if account:    
        pr = "update_accounts(%s): update connected settlements" % (account.account)
    else:
        pr = 'update_accounts: Input not account'
        
    log(1, pr)
    acc = 0
    name = ''
    nameo= ''
    setls = []
    setl_acq = [] # list with settlements connected to the account
    setl_pty = [] # list with settlements connected to the account
    intermediary_update = False
    if party_update:
        intermediary_update = party_update.intermediary_update

    if not diff_dict and not intermediary_update:
        log(2, 'Irrelevant account change, no setl update. (File)')
        return
    
    if account and account_old:
        acc     = account.account       
        name    = account.name
        
        if ptyid != '':
            pass # already provided
        elif type(account.ptynbr) == ael.ael_entity:
            ptyid = account.ptynbr.ptyid # partyid does not change
        
        acco    = account_old.account   
        nameo   = account_old.name
       
        query = """SELECT s.seqnbr
                        FROM Settlement s
                        WHERE (s.party_ptyid = \'%s\' OR s.acquirer_ptyid = \'%s\') AND s.status NOT IN (\'Closed\')""" % (ptyid, ptyid)
                   
        query_list = ael.asql(query, 1)[1][0]
        
        for (setl,) in query_list:
            if setl.status != 'Closed' and FSettlementGeneral.source_data(setl):   
                child_settlement = child(setl)
                if is_acquirer_change(setl, nameo, acco, ptyid, child_settlement):
                    setl_acq.append(setl)
                if is_counterparty_change(setl, nameo, acco, ptyid, child_settlement):
                    setl_pty.append(setl)

    update_acc(account, setl_acq, diff_dict, 0, party_update)
    update_acc(account, setl_pty, diff_dict, 1, party_update)
    return    

def child(settlement):
    returned_settlement = None
    ch_list = ael.Settlement.select('ref_seqnbr = %d' % settlement.seqnbr)
    if len(ch_list):
        if ch_list[0].ref_type == 'None':
            returned_settlement = ch_list[0]
    return returned_settlement
    
def is_counterparty_change(settlement, name_old, account_old, ptyid, child = None):
    change = False
    s = settlement
    if child:
        s = child
    if s.party_accname == name_old and \
    s.party_account == account_old and \
    s.party_ptyid == ptyid:
        change = True
    
    return change
    
def is_acquirer_change(settlement, name_old, account_old, ptyid, child = None):
    change = False
    s = settlement
    if child:
        s = child
    if s.acquirer_accname == name_old and \
    s.acquirer_account == account_old and \
    s.acquirer_ptyid == ptyid:
        change = True
    return change


def update_cf(cf, diff_dict, trade, instr, tr_c=None, ins_c=None, leg_c=None, cf_c=None, res_c=None, tr_for_sec_nom = None):
    '''Updates settlement containing the CashFlow. This update is done
    seperaterly for general cash flows and coupons.
    Note:
    Both trade and instr (incl amb_msg) should not be deployed!
    When instrument is deployed then coupons are handled.
    '''
    
    cfs = []    
    pays = [] #list with Settlement objects
    setls = [] #list with rows from settlement table
    trades = []
    payday = ''
    typ = ''
    isCoupon = 0
    
    tr_c = set_c(tr_c, trade, 'Trade')
    if not trade:
        tr_c = None # see note above

    cf_c = set_c(cf_c, cf, 'CashFlow')
    leg_c = set_c(leg_c, cf.legnbr, 'Leg')
    ins_c = set_c(ins_c, instr, 'Instrument')
    if not instr:
        ins_c = None
                    
    if is_cf(cf_c):
        if is_trade(tr_c):     
            trades.append(tr_c)
        else:
            if instr:
                isCoupon = 1
            elif FSettlementGeneral3.is_valid_cf_type(cf_c):
                trades = FSettlementGeneral.get_tradelist_cf(cf.cfwnbr)
    else:
        log(1, 'update_cf: CF not deployed. (File)')

    for tr in trades:        
        # do not use tr_c bellow in this loop
        if tr.status in tr_status:
            setls = get_setl_rows_ref(cf, tr, None) #via reference in
            if len(setls) == 0:
                if is_trade(tr):
                    # what if archived
                    pr = 'update_cf: Not found, Create CF %d for Trade %d' \
                         % (cf.cfwnbr, tr.trdnbr)
                    log(2, pr)
                    create_cf(cf, tr, 'New', 0, cf_c, tr, leg_c) #collateral
               
            else:
                # Settlement entities in a list
                setlObjList = FSettlementGeneral.create_from_settle(setls)

                # Settlement object of the new CF
                if len(setlObjList)>0 and diff_dict:
                    for setlObj in setlObjList:
                        if setlObj.status not in noupdate_stl_status and FSettlementGeneral3.is_updatable(setlObj):
                            cf_n = create_setlObj(setlObj, diff_dict, tr, cf, None, None, None, None, None, tr, leg_c, cf_c, res_c, None, None)
                            
                            # Update should be done only if something is changed!
                            if cf_n != None:
                                prim = 1
                                if FSettlementGeneral2.coupon_ok(tr.insaddr):                                                                
                                    prim = FSettlementGeneral3.check_primary_issuance(tr, diff_dict)
                                                                    
                                log(3, 'update_cf: treat CF based on enter_cashflow (File)')
                                if FSettlementGeneral.enter_cashflow(tr, cf, cf_c) and prim and \
                                FSettlementGeneral.paydayOK(cf_c.pay_day, cf, 1, setlObj.type) and \
                                FSettlementGeneral.is_prevent_cash_flow(cf) == False:
                                    update_setl_row(setlObj, cf_n, 'Updated')
                                else:
                                    update_setl_row(setlObj, cf_n, 'Recalled')
                        else:
                            pr = 'setlObj.status %s is not subject to updates' % (setlObj.status)
                            log(1, pr)
                elif diff_dict == None:
                    log(2, 'Irrelevant cf change, no setl update. (File)')
        else:
            pr = 'No update of CF: %d, Invalid trade status: %s, Tr:%d' \
                 % (cf.cfwnbr, tr.status, tr.trdnbr)
            log(1, pr)              
            
    if isCoupon:
        settles = ael.Settlement.select('cfwnbr=%d' % cf_c.cfwnbr) #do not use create_selection here
        if settles:
            list = settles.members()
            settleList = FSettlementGeneral.create_from_settle(list)
            for settle in settleList:
                couponOK = 0
                if not settle.trdnbr:
                    couponOK = 1
                elif settle.type == 'Coupon transfer':
                    coupon_mode_update(settle.trdnbr, ins_c, leg_c, cf_c)
                    return
                if couponOK and settle.status not in noupdate_stl_status and FSettlementGeneral3.is_updatable(settle):
                    pr = 'update_cf: isCoupon Mode, CF %d' % (cf_c.cfwnbr)
                    log(3, pr)
                    cf_n = create_setlObj(settle, diff_dict, None, cf, None, None, None, ins_c, None, None, leg_c, cf_c, res_c, None, tr_for_sec_nom)
                    if cf_n != None:
                        enterOK = FSettlementGeneral2.enter_coupon(cf, None, cf_c)
                        if enterOK and cf_n.amount != 0:
                            log(4, 'update_cf: enter_coupon 1 and non zero amount')
                            update_setl_row(settle, cf_n, 'Updated')
                        else:
                            # Remove coupons which after update have amount 0
                            # either because of value day or position
                            if not enterOK:
                                log(2, 'update_cf: enter_coupon 0 (File)')
                            else:
                                log(2, 'update_cf: recall zero amount cf (File)')
                            update_setl_row(settle, cf_n, 'Recalled')
        else:
            log(4, 'update_cf: isCoupon Mode -- trades = instr.trades()')
            trades = instr.trades()
            for trade in trades:
                coupon_mode_update(trade.trdnbr, ins_c, leg_c, cf_c)
    return

def coupon_mode_update(trdnbr, ins_c, leg_c, cf_c):
    sec = FSettlementGeneral2.get_sec_trade(trdnbr, ins_c)
    if sec and FSettlementGeneral2.check_security([sec]):
        FSettlementGeneral2.update_position_cover(sec, None, leg_c, cf_c)

def update_dividend_settlement(s_list, d, div, i, tr_c, trade_update = False, comb_info = None):
    # s_list is a list containing dividend settlement records. d is the diff_dict dictionary.
    # i is an instrument. If trade_update is true we have an update trade event
    # for an equity swap trade.
    
    settleList = FSettlementGeneral.create_from_settle(s_list)
    for settle in settleList:
        if settle.status not in noupdate_stl_status and FSettlementGeneral3.is_updatable(settle):
            tr_c = set_c(tr_c, FSettlementGeneral3.get_trade_entity(settle.trdnbr), 'Trade')
            
            div_n = create_setlObj(settle, d, None, None, div, None, None, i, None, tr_c, None, None, None,\
                                   trade_update, None, comb_info)
            if not div_n:
                log(1, 'create_setlObj returned None. update_dividend_settlement will be aborted!')
                return
            if div_n.amount != 0 and FSettlementGeneral.enter_dividend(tr_c, div):
                update_setl_row(settle, div_n, 'Updated')
            else:
                update_setl_row(settle, div_n, 'Recalled')
        else:
            pr = 'update of settlement %d will not be done due to settlement status %s' % (settle.seqnbr, settle.status)
            log(1, pr)

def update_div(div, diff_dict, ins_c=None, tr_c=None, eqsw_mode=0, trade_update = False, comb_info = None):
    '''Updates settlement containing the Dividend.
    When eqsw_mode no update should be done since the dividend settlement
    is about to be deleted sooner or later by FSEQEquitySwap script (also
    no creation will be done if not found?!).
    
    div can be div_c.'''
   
    settles = []
    if is_div(div):
        instr = div.insaddr
        if ins_c:
            instr = ins_c

        settles2 = ael.Settlement.select('dividend_seqnbr=%d' % div.seqnbr).members()
        if tr_c and tr_c.trdnbr:
            for s in settles2:
                if s.trdnbr and s.trdnbr.trdnbr == tr_c.trdnbr:
                    settles.append(s)
        else:
            settles = settles2
        if len(settles) > 0 and not eqsw_mode:
            update_dividend_settlement(settles, diff_dict, div, instr, tr_c, trade_update, comb_info)
        elif trade_update: #amb-message was !TRADE and instr is EQ swap.
            setls = get_setl_rows_ref(div, tr_c.get_ael_entity(), None)
            if len(setls) == 0:
                create_div(div, tr_c, 'New', instr)
            else:
                update_dividend_settlement(setls, diff_dict, div, instr, tr_c, trade_update, comb_info)
        elif not eqsw_mode:
            create_div(div, tr_c, 'New', instr)
        elif eqsw_mode:
            pr = "No update of Equity swap dividend %d. FSEQEquitySwap task must act." % (div.seqnbr)
            log(1, pr)
    return


def update_payment(pay, diff_dict, pay_c=None, tr_c=None):
    '''Updates settlement containing the payment'''

    setls = []
    pay_c = set_c(pay_c, pay, 'Payment')
    tr_c = set_c(tr_c, pay_c.trdnbr, 'Trade')    
    if is_pay(pay_c): 
        if pay_c.type not in FSettlementGeneral.invalid_payment_types:
            # get settlements that reference the payment
            setl_rows = get_setl_rows_ref(pay, pay.trdnbr, None)

            if len(setl_rows) == 0:
                create_payment(pay, 'New', pay_c, tr_c)
            else:               
                # make Settlement objects in a list
                setlObjList = FSettlementGeneral.create_from_settle(setl_rows)
                if len(setlObjList):
                    setlObj = setlObjList[0]
                 
                # Settlement objects based on Payment
                if setlObj and diff_dict and do_payment_update(diff_dict, setlObj):
                    if setlObj.status not in noupdate_stl_status and FSettlementGeneral3.is_updatable(setlObj):
                        pay_n = create_setlObj(setlObj, diff_dict,\
                                tr_c, None, None, pay_c, None, None, None, tr_c)
                        # Update
                        if pay_n:
                            s = ael.Settlement[pay_n.seqnbr]
                            if pay_n.amount != 0 or FSettlementGeneral3.has_the_keyword(s):
                                update_setl_row(setlObj, pay_n, 'Updated')
                            else:
                                update_setl_row(setlObj, pay_n, 'Recalled')
                    else:
                        pr = 'update of settlement %d will not be done due to settlement status %s' % (setlObj.seqnbr, setlObj.status)
                        log(1, pr)
                elif diff_dict == None:
                    log(2, 'Irrelevant pay change, no setl update. (File)')
    return

def do_payment_update(diff_dict, settlement):
    return (not diff_dict.has_key('empty') or settlement.status in \
    FSettlementGeneral.stp_status) #SPR 275516, 282365
    
def check_update(party_accname, acquirer_accname, setl2):
    update = 1
    if party_accname==setl2.party_accname and \
       acquirer_accname==setl2.acquirer_accname:
        update = 0
    return update

def update_from_ssi(ssi_seqnbr):
    'Updates of settlements dependent on SSI update'
    if not ssi_seqnbr:
        return
    list = []
    trade_list = []
    settle_list = []
    tals = ael.TradeAccountLink.select('settle_seqnbr=%d' % ssi_seqnbr)
    for t in tals:
        if t.trdnbr:
            if t.trdnbr.trdnbr not in trade_list:
                trade_list.append(t.trdnbr.trdnbr)
    for trdnbr in trade_list:
        setls = ael.Settlement.select('trdnbr=%d' % trdnbr)
        for s in setls:
            settle_list.append(s)
    for setl in settle_list:
        if not setl.type=='Coupon' and not setl.type=='Coupon transfer':
            if FSettlementGeneral.source_data(setl):
                list.append(setl)
    setlObjList = FSettlementGeneral.create_from_settle(list)
    for settle in setlObjList:
        if settle.status not in noupdate_stl_status and settle.trdnbr and FSettlementGeneral3.is_updatable(settle):
            p_accname = settle.party_accname
            a_accname = settle.acquirer_accname
            new = settle
            trade = ael.Trade[settle.trdnbr]
            FSettlementGeneral.account_info(trade, new, 1)
            if check_update(p_accname, a_accname, new):
                update_setl_row(settle, new, 'Updated')
        else:
            str = 'Settlement %d can not be updated, either it is closed/void \
                   or has no trade' % settle.seqnbr
            log(3, str)
                        
def update_premium(tr, diff_dict, st, comblink=None, tr_c=None, ins_c=None, comb_link_removed = False):
    '''Updates settlements with the premium of the trade'''
    tr_c = set_c(tr_c, tr, 'Trade')
    ins_c = set_c(ins_c, tr.insaddr, 'Instrument')
    setls = [] 
    typ = 'Premium'
    SN = 'Security Nominal'
    securNom = 0 # security nominal mode candidate
    curr = 0
    endSec = 0
    combination_member = FSettlementGeneral.get_combination_member(comblink)
    
    if is_trade(tr_c):
        if FSettlementGeneral.has_security_nominal(tr_c) or combination_member:
            securNom = 1
            if FSettlementGeneral.has_end_security(None, combination_member):
                endSec = 1
                securNom = 0
        elif ins_c.instype=='Curr' or \
            (combination_member and combination_member.instype=='Curr'):
            curr = 1
            if st == 'Premium' and (combination_member and combination_member.instype=='Curr'):
                curr = 0 # Premium 2 is handled via update_combination_member
        elif FSettlementGeneral.has_end_security(tr):
            endSec = 1
    else:
        return

    if st and st in ['Security Nominal', 'Premium 2', 'End Security', 'Fee']:
        typ = st
        securNom = 0
        endSec = 0
        curr = 0
    st = "update_premium: %s Mode" % (typ)
    if combination_member:
        st = "update_premium: %s Mode (combination member:%s)" % (typ, combination_member.insid)
    log(1, st)
    
    setls = []
    input_list = []
    setl = None
    if combination_member and not param.handle_combination_cash_flows:
        setls  = get_premium_settlement_record(tr)
        typ = 'Premium'
    else:
        setls = FSettlementGeneral.get_setl_rows(tr.trdnbr, typ, '', combination_member, 1, comb_link_removed)### IV or VI
    
    if len(setls) == 0:
        if typ == 'Premium':
            create_premium_t(tr, typ, 'New', 1, None, tr_c, ins_c) #create only premium
        elif combination_member:
            create_premium_t(tr, typ, 'New', 1, comblink, tr_c, ins_c)#create only SN/EndSec/Prem2 for comb
        else:
            create_premium_t(tr, typ, 'New', 0, None, tr_c, ins_c) #default procedure
    else:
        if len(setls) > 1:
            pr = 'update_premium: more than one setl of (type:%s)! (Error)' % (typ)
            if combination_member:
                pr = 'update_premium: more than one combination setl (type:%s)! (Error)' % (typ)
            log(1, pr)
        else:
            #there should be only one premium/secnom/fee
            setl = setls[0]
            input_list.append(setl)

        # setl to setlObj
        setlObjList = FSettlementGeneral.create_from_settle(input_list)
        setlObj = None
        if len(setlObjList):
            setlObj = setlObjList[0]
                
        if setlObj:
            if setlObj.status not in noupdate_stl_status and FSettlementGeneral3.is_updatable(setlObj):
                if diff_dict:
                    newP = create_setlObj(setlObj, diff_dict, tr, None, None, None, typ, None, comblink, tr_c)
                    if setl and newP != None:
                        #setl deployed, not setlObj
                        
                        day = tr_c.value_day
                        typ = setl.type
                        
                        if typ == 'Security Nominal':
                            day = tr_c.acquire_day
                        elif typ == 'End Security':
                            day = end_security_value_day(tr_c, combination_member, ins_c)
                            
                        if newP.amount != 0 and FSettlementGeneral.paydayOK(day, tr, 1, typ) or \
                        (is_correction_sec_nom_update(tr, newP) and FSettlementGeneral.paydayOK(day, tr, 1, typ)):
                            update_setl_row(setl, newP, 'Updated')
                        else:
                            update_setl_row(setl, newP, 'Recalled')
                            
                    elif not setl:
                        pr = 'update_premium: Empty settlement (File)'
                        log(1, pr)
                else:
                    pr = 'Irrelevant trade change, no setl update. (File)'
                    log(2, pr)
            else:
                pr = 'update of %s will not be done due to settl status %s' % (typ, setlObj.status)
                log(1, pr)
        else:
            log(1, 'Could not find settlement row to update')

    if typ == 'Premium' and (curr or endSec or securNom):
        if curr:
            st = 'Premium 2'
        elif endSec:
            st = 'End Security'
        else:
            st = 'Security Nominal'
        update_premium(tr, diff_dict, st, None, tr_c) #comb is handled specifically
    return

def update_row(created, new, party_update = None):
    'Already created settlement row is replaced with the new one.'
    if created: 
        seqnbr = int(created.seqnbr)
        pr = "Settlement %d about to be updated..." % (seqnbr)
        log(1, pr)                        
    else:
        seqnbr = None   
    
    if new and seqnbr:
        FSettlementGeneral2.handle_changed_source_data(seqnbr, new, new.status, party_update)
    else:
        log(1, 'update_row: input(s) are None')
    return


def update_values(settle_clone, new):
    'This function takes one already existing and one old settlements.\
    Values of the new settlement will override the old ones.'
    ref_s = ael.Settlement[new.seqnbr]
    new_new = None
    new_status_explanation = new.status_explanation
    new_text = ''
    if settle_clone.seqnbr < 0:
        new_text = new.text
    else:
        new_text = settle_clone.text
        
    if ref_s and FSettlementGeneral3.is_in_update_status(ref_s) or (settle_clone.seqnbr == new.seqnbr):
        if settle_clone.type == 'Premium':
            new_new = create_premium_t(settle_clone.trdnbr, 'Premium', 'New', 1, None, None, settle_clone.trdnbr.insaddr, 0, 0)
        elif settle_clone.type == 'Premium 2':
            new_new = create_premium_t(settle_clone.trdnbr, 'Premium', 'New', 1, None, None, settle_clone.trdnbr.insaddr, 0) #Second parameter is correct! Will create Premium 2.
        elif settle_clone.type == 'Fee':
            new_new = create_premium_t(settle_clone.trdnbr, 'Fee', 'New', 1, None, None, settle_clone.trdnbr.insaddr, 0)
        elif settle_clone.type == 'Security Nominal':
            new_new = create_premium_t(settle_clone.trdnbr, 'Security Nominal', 'New', 1, None, None, settle_clone.trdnbr.insaddr, 0)
        elif settle_clone.type == 'End Security':
            new_new = create_premium_t(settle_clone.trdnbr, 'End Security', 'New', 1, None, None, settle_clone.trdnbr.insaddr, 0)
        elif settle_clone.cfwnbr and settle_clone.type not in ['Coupon', 'Redemption', 'Coupon transfer']:
            new_new = create_cf(settle_clone.cfwnbr, settle_clone.trdnbr, 'New', 0, None, None, None, None, 0)
        elif settle_clone.paynbr:
            new_new = create_payment(settle_clone.paynbr, 'New', settle_clone.paynbr, settle_clone.paynbr.trdnbr, 0)
            corrected_setl = FSettlementGeneral2.get_corrected_setl(settle_clone.paynbr, settle_clone.trdnbr, None, settle_clone)
            amount = FSettlementGeneral2.get_payment(settle_clone.trdnbr, settle_clone.paynbr, corrected_setl)    
            if new_new:
                new_new.amount = amount
        elif settle_clone.type == 'Fixed Rate':
            new_new = FSettlementGeneral3.create_accrued_interest(settle_clone.trdnbr, None, None, 0)
        elif settle_clone.dividend_seqnbr:
            if settle_clone.sec_insaddr:
                i = settle_clone.sec_insaddr
                if i and i.instype == 'Stock':
                    prfnbr = None
                    if settle_clone.to_prfnbr:
                        prfnbr = settle_clone.to_prfnbr.prfnbr
                    sec_nom = FSettlementGeneral2.get_security(None, settle_clone.dividend_seqnbr, prfnbr)
                    if sec_nom:
                        pos = FSettlementGeneral2.get_position(sec_nom, settle_clone.dividend_seqnbr.pay_day)
                        new_new = FSettlementGeneral2.create_dividend(sec_nom, settle_clone.dividend_seqnbr, pos, i, 0)
                        
        if new_new:
            new = new_new
            
    settle_clone.text = new_text
    settle_clone.amount = new.amount
    settle_clone.curr = new.curr
    settle_clone.value_day = new.value_day
    settle_clone.acquirer_accname = new.acquirer_accname
    settle_clone.acquirer_account = new.acquirer_account
    settle_clone.party_accname = new.party_accname
    settle_clone.party_account = new.party_account
    settle_clone.acquirer_ptyid = new.acquirer_ptyid
    settle_clone.party_ptyid = new.party_ptyid
    settle_clone.to_prfnbr = new.to_prfnbr
    settle_clone.from_prfnbr = new.from_prfnbr    
    cats = ['Adjusted', 'Compensation Claim', 'Compensation Payment',\
            'Fair Value', 'Funds Transfer', 'Good Value']
    if type(settle_clone.settle_category) != type(new.settle_category):
        pr = 'category types: %s %s' % (type(settle_clone.settle_category), type(new.settle_category))
        log(1, pr)
    if str(settle_clone.settle_category) != str(new.settle_category):
        pr = 'categories: %s %s' % (str(settle_clone.settle_category), str(new.settle_category))
        log(1, pr)
    #'Delivery versus Payment','Delivery Free of Payment'
    if new.settle_category in cats:
        settle_clone.settle_category = new.settle_category
    else:
        settle_clone.settle_category = 'None'        
    settle_clone.trdnbr = new.trdnbr
    settle_clone.cfwnbr = new.cfwnbr
    settle_clone.dividend_seqnbr = new.dividend_seqnbr
    settle_clone.paynbr = new.paynbr
    settle_clone.settleinstruction_seqnbr = new.settleinstruction_seqnbr
    settle_clone.status = new.status
    settle_clone.type = new.type
    settle_clone.delivery_type = new.delivery_type
    settle_clone.status_explanation = new_status_explanation
    settle_clone.netting_rule_seqnbr = new.netting_rule_seqnbr
    settle_clone.manual_match = new.manual_match
    settle_clone.post_settle_action = new.post_settle_action
    settle_clone.sec_insaddr = new.sec_insaddr
    settle_clone.org_sec_nom = new.org_sec_nom
    settle_clone.protection= new.protection
    settle_clone.owner_usrnbr = new.owner_usrnbr
    settle_clone.primary_issuance = new.primary_issuance
    if param.network_update:
        settle_clone.party_account_network_name = new.party_account_network_name
        settle_clone.acquirer_account_network_name = new.acquirer_account_network_name
    
    if settle_clone.type != new.type:
        pr = "update_values: Types differ, %s != %s (File)" % \
        (settle_clone.type, new.type)
        log(1, pr)
        settle_clone.type = new.type
    return


def update_secnom_from_instr(instr, size, currInst, ins_c=None):
    return FSettlementGeneral3.update_secnom_from_instr(instr, size, currInst, ins_c)

def update_setl_row(setl, candidate, inStatus, party_update = None):
    'Updates settlement row if status allows that'

    ok = 1            
    if setl == None or candidate == None:
        ok = 0          
    elif inStatus and inStatus != '':
        ##if type(setl) == ael.ael_entity:
        candidate.status = inStatus
        pr = "update_setl_row: %s to be %s (File)" % (str(setl.seqnbr), inStatus)
        log(3, pr)
        
    if ok:
        update_row(setl, candidate, party_update)    
    else:
        log(0, 'update_setl_row: invalid input parameters!')
    return

def update_reset(reset, diff_dict, cf, ins_c=None, leg_c=None, cf_c=None, res_c=None):
    ''' amb!'''
    
    cf_setl_rows = []
    trades = []
    if cf and reset:
        pr = 'Leg: %d CF: %d Reset %d:' % (cf.legnbr.legnbr, cf.cfwnbr, reset.resnbr)
        log(2, pr)  
    
    if cf_c:        
        if FSettlementGeneral3.is_valid_cf_type(cf_c):
            trades = FSettlementGeneral.get_tradelist_cf(cf_c.cfwnbr)
    
    for tr in trades:
        if tr.status in tr_status:                 
            setls = get_setl_rows_ref(cf, tr, None)# no need for stt_c bellow
            if len(setls):
                for setl in setls:                      
                    setlObjList = FSettlementGeneral.create_from_settle([setl])                
                    if len(setlObjList):
                        setlObj = setlObjList[0]
                    else:
                        log(1, 'create_from_settle([setl]) returned empty list')
                    
                    if setlObj and diff_dict:
                        if setlObj.status not in noupdate_stl_status and FSettlementGeneral3.is_updatable(setlObj):                        
                            cf_n = create_setlObj(setlObj, diff_dict, tr, cf, None, None, None, None, None, tr, leg_c, cf_c, res_c)               
                            if cf_n != None:                                
                                # note that this code is pretty similar to update_cf
                                trade = ael.Trade[cf_n.trdnbr]
                                cf = ael.CashFlow[cf_n.cfwnbr]
                                if FSettlementGeneral.is_coupon(trade, cf, trade, cf_c, leg_c):
                                    if not FSettlementGeneral.enter_cashflow(trade, cf, cf_c):
                                        update_setl_row(setlObj, cf_n, 'Recalled')
                                    else:
                                        update_setl_row(setlObj, cf_n, 'Updated')
                                else:
                                    update_setl_row(setlObj, cf_n, 'Updated')                                
                            else:
                                log(1, 'create_setlObj could not create cf_n')
                    elif diff_dict == None:
                        pr = 'Irrelevant reset change, no setl update. (File)'
                        log(1, pr)                        
            else:    
                if is_trade(tr):                    
                    # what if archived                    
                    create_cf(cf, tr, 'New', 0, cf_c, tr, leg_c) #collateral
    return
        
              
# HELP FUNCTIONS
               
def get_setl_rows_ref(ent, trd, paydayFlag):
    'Returns a list of Settlements that refer to a certain entity.\
    The entity can be cashflow, dividend or payment. Only those \
    settlements that are source data and valid day not earlier than today\
    are returned. PaydayFlag turned on means that paydayOK check is done.'

    ok = 1
    slist = []
    setls = []
    valid_entities = ['CashFlow', 'Dividend', 'Payment']  
    if ent:
        if ent.record_type in valid_entities:
            setls = FSettlementGeneral3.get_settlements_from_entity(ent)
            for setl in setls:
                if setl.record_type=='Settlement' and not \
                   setl.type=='Coupon' and not setl.type=='Coupon transfer':                    
                    # handling selling of stocks/cf_insts!!!???
                    if trd and setl.trdnbr:
                        if trd.trdnbr == setl.trdnbr.trdnbr:
                            if FSettlementGeneral.source_data(setl):
                                if paydayFlag != None:
                                    # update functions should not use this
                                    if type(paydayFlag) == int(1) and paydayFlag < 3:
                                        if FSettlementGeneral.paydayOK(\
                                            setl.value_day, setl, paydayFlag, ''):                                
                                            slist.append(setl)
                                else:
                                    slist.append(setl)
                            else:
                                pr = 'Setl %d is not source data' % (setl.seqnbr)
                                log(1, pr)
        else:
            pr = 'get_setl_rows_ref: Entity %s not supported! (File)' % (ent.record_type)
            log(1, pr)
    
    return slist


def create_eq_swap_dividend(tr_c, divs=None):
    '''get_setl_rows_ref should be done if this function is called as a part of update procedure.'''
    eq_swap_list = []
    if tr_c.insaddr and tr_c.insaddr.instype == 'Combination':
        set_equity_swaps_in_list(eq_swap_list, tr_c.insaddr)
        for (eq_swap, link) in eq_swap_list:
            comb_info = CombInfo(tr_c.insaddr, link)
            eq_swap_dividend_creation(tr_c, eq_swap, divs, comb_info)
    else:
        eq_swap_dividend_creation(tr_c, tr_c.insaddr, divs)


class CombInfo(object):

    def __init__(self, comb_ins, comb_link):
        self. comb_ins = comb_ins
        self.comb_link = comb_link


def eq_swap_dividend_creation(tr_c, instrument, divs = None, comb_info = None):
    if tr_c.status in tr_status and (FSettlementGeneral3.is_equity_swap(instrument) or \
       FSettlementGeneral3.is_combination_with_dividend(instrument)):
        if not divs:
            divs = divs_from_instrument(instrument, None, 1)
        for div in divs:
            n = ael.Settlement.new()                                                
            trade = ael.Trade[tr_c.trdnbr]                                    
            if FSettlementGeneral.enter_dividend(trade, div) and \
            FSettlementGeneral.paydayOK(div.pay_day, div, 1, '') and \
            not trade_has_dividend_settlement_record(tr_c, div):
                FSettlementGeneral.dividend_creation(n, div, 'New', 0, trade, 1, 0, tr_c, div.insaddr, 1, comb_info)
                
def set_equity_swaps_in_list(eq_swap_list, inst):
    links = inst.combination_links()
    for link in links:
        ins = FSettlementGeneral.get_combination_member(link)
        if ins and ins.instype == 'EquitySwap':
            eq_swap_list.append((ins, link))

def insert_trade(tr, tr_c=None, pay_dict=None):
    'This function is used when AMBA has sent the event that\
    a new trade has been inserted.'
    
    tr_c = set_c(tr_c, tr, 'Trade')
    if is_trade(tr_c):
        if tr_c.status in tr_status:
            if not FSettlementGeneral3.check_otc_handling(tr_c):
                return
            create_premium_t(tr_c, 'Premium', 'New', 0, None, tr_c, tr_c.insaddr) # takes care of secnome as well
            is_collateral = FSettlementGeneral.is_collateral_trade(tr_c)
            if tr_c.insaddr.instype in FSettlementGeneral.und_ins_security or is_collateral:
                FSettlementGeneral2.validate(tr_c, 'INSERT', tr_c)
            if tr_c.fee > 0 or tr_c.fee < 0:
                create_premium_t(tr_c, 'Fee', 'New', 0, None, tr_c, tr_c.insaddr)
            
            if tr_c.insaddr.instype in FSettlementGeneral.ins_combination:
                for comblink in tr_c.insaddr.combination_links():
                    FSettlementGeneral2.create_combination_member(tr_c, comblink, tr_c, tr_c.insaddr)
                FSettlementGeneral2.create_combination_securities(tr_c, None, tr_c.insaddr)
                
            # Create CFS for this trade
            if not is_collateral:
                for cf in cfs_from_tr(tr_c, tr_c):                 
                    create_cf(cf, tr_c, 'New', 0, cf, tr_c, None)

            create_eq_swap_dividend(tr_c)
                       
            # PAYMENTS
            FSettlementAMB.sub_pay(pay_dict, tr_c)
                
            # Settlement for the accrued interest     
            FSettlementGeneral2.create_accrued_interest(tr_c, tr_c)
                
            FSettlementGeneral2.touch_closed_trade(tr_c)
        else:
            pr = 'Trade status %s is not supported for settlement creation!' % (tr_c.status)
            log(0, pr)
    else:
        log(1, 'insert_trade: trade not deployed as input or aggregate.')


def update_acc(account, setl_list, diff_dict, mode=0, party_update = None):
    '''Takes a list as an input with settlements connected to the account.\
    Mode zero is default and it means that changes will be done on \
    acquirer part of the settlement while Mode one is on counterparty.
    account can be acc_c.'''
    intermediary_update = False
    if party_update:
        intermediary_update = party_update.intermediary_update
    for sr in setl_list:
        if sr.status not in noupdate_stl_status and FSettlementGeneral3.is_updatable(sr):            
            setlObjList = FSettlementGeneral.create_from_settle([sr])
            if len(setlObjList):
                setlObj = setlObjList[0]
                if (diff_dict or intermediary_update) and setlObj:
                    newP = setlObj
                    r = 0 # flag to apply changes encountered
                    if mode == 0:
                        if diff_dict.has_key('NAME'):
                            newP.acquirer_accname = account.name
                            r = 1
                        if diff_dict.has_key('ACCOUNT'):
                            newP.acquirer_account = account.account
                            r = 1
                        if param.network_update:
                            if diff_dict.has_key('NETWORK_ALIAS_TYPE'):
                                if account.network_alias_type:
                                    newP.acquirer_account_network_name = account.network_alias_type.alias_type_name
                                else:
                                    newP.acquirer_account_network_name = ''
                                r = 1
                    elif mode == 1:                        
                        if diff_dict.has_key('NAME'):
                            newP.party_accname = account.name
                            r = 1
                        if diff_dict.has_key('ACCOUNT'):
                            newP.party_account = account.account
                            r = 1
                        if param.network_update:
                            if diff_dict.has_key('NETWORK_ALIAS_TYPE'):
                                if account.network_alias_type:
                                    newP.party_account_network_name = account.network_alias_type.alias_type_name
                                else:
                                    newP.party_account_network_name = ''
                                r = 1
                    if intermediary_update:
                        r = 1
                    
                    if r:
                        pu = None
                        if party_update:
                            pu = FSettlementGeneral3.PartyUpdate(intermediary_update)

                        update_setl_row(setlObj, newP, 'Updated', pu)
    return

def createObjTrade(typ, diff_dict, setl, tr, comblink=None, tr_c=None, ins_c=None):
    tr_c = set_c(tr_c, tr, 'Trade')
    curr = None
    curr = set_curr(diff_dict, curr)
    combination_member = FSettlementGeneral.get_combination_member(comblink)
    corrected_setl = 0
    correction = diff_dict.has_key('correction')
    if correction:
        corrected_setl = FSettlementGeneral2.get_corrected_setl(None, tr, typ)    
    
    if curr:
        setl['curr'] = curr.insaddr            
    if typ =='Premium':
        if diff_dict.has_key('premium'):
            setl['amount'] = FSettlementGeneral2.get_premium(tr_c, corrected_setl)
            setl['curr'] = tr_c.curr.insaddr
    elif typ=='Fee':
        if diff_dict.has_key('fee'):
            setl['amount'] = FSettlementGeneral2.get_fee(tr_c, corrected_setl)
            setl['curr'] = tr_c.curr.insaddr
    elif typ in FSettlementGeneral.sec_types: 
        if diff_dict.has_key('premium') or diff_dict.has_key('quantity') or\
           diff_dict.has_key('sec_insaddr') or diff_dict.has_key('org_sec_nom') \
           or diff_dict.has_key('acquire_day') or diff_dict.has_key('combinationlink')\
           or diff_dict.has_key('combination_quantity') or diff_dict.has_key('index_factor') \
           or diff_dict.has_key('primary_issuance') or diff_dict.has_key('exp_day'):
            # see also FSettlementGeneral.premium_creation           
            if typ=='Security Nominal':
                amount = FSettlementGeneral.calc_security_nominal(tr_c, comblink, corrected_setl, 0, ins_c)
                setl['primary_issuance'] = FSettlementGeneral.check_primary_issuance(tr, diff_dict)                    
            else:
                amount = FSettlementGeneral.calc_end_security(tr_c, comblink, corrected_setl, ins_c)
                                    
            setl['amount'] = amount
            setl['curr'] = tr_c.curr.insaddr
            instr = tr_c.insaddr
            if instr and instr.instype in FSettlementGeneral.und_ins_security:
                if instr.und_insaddr:
                    setl['sec_insaddr'] = instr.und_insaddr.insaddr
                if instr.instype=='Repo/Reverse' or \
                   instr.instype=='SecurityLoan':
                    setl['org_sec_nom'] = instr.ref_value
                else:
                    setl['org_sec_nom'] = instr.nominal_amount()
        if diff_dict.has_key('acquire_day') and typ=='Security Nominal':    
            setl['value_day'] = tr_c.acquire_day
        elif typ=='End Security':            
            setl['value_day'] = end_security_value_day(tr_c, combination_member, ins_c)
        if curr or diff_dict.has_key('curr.insid'):                    
            #sec nom takes currency from instrument
            if tr_c.insaddr:
                if tr_c.insaddr.curr:
                    setl['curr'] = tr_c.insaddr.curr.insaddr
                if tr_c.insaddr.instype in FSettlementGeneral.und_ins_security:
                    if tr_c.insaddr.und_insaddr:
                        setl['sec_insaddr']=tr_c.insaddr.und_insaddr.insaddr
                        if tr_c.insaddr.und_insaddr.curr:
                            setl['curr'] = tr_c.insaddr.und_insaddr.curr.insaddr
        if combination_member:
            setl['curr']        = combination_member.curr.insaddr
            setl['sec_insaddr'] = combination_member.insaddr
            setl['org_sec_nom'] = combination_member.nominal_amount()     
    elif typ=='Premium 2':
        if curr or diff_dict.has_key('curr.insid'):                    
            setl['curr'] = FSettlementGeneral2.get_curr_premium2(tr_c, combination_member)
        if diff_dict.has_key('quantity') or diff_dict.has_key('contr_size') or \
        diff_dict.has_key('combinationlink') or diff_dict.has_key('index_factor'):
            if tr_c.insaddr.contr_size and tr_c.quantity:
                setl['amount'] = FSettlementGeneral2.get_premium2(tr_c, corrected_setl, comblink)
                setl['curr'] = FSettlementGeneral2.get_curr_premium2(tr_c, combination_member)
            else:
                pr = 'Amount of setlement %d for Premium 2 not updated! (File)' % (setl.seqnbr)
                log(1, pr)
    elif FSettlementGeneral2.accrued_interest_setl_needed(tr_c):
        if diff_dict.has_key('quantity') or diff_dict.has_key('acquire_day') \
        or diff_dict.has_key('value_day') or diff_dict.has_key('curr.insid'):
            setl['amount']    = FSettlementGeneral2.get_interest_accrued(tr_c, ins_c)
            setl['curr']      = tr_c.insaddr.curr.insaddr
            setl['value_day'] = tr_c.value_day
        
    FSettlementGeneral.account_info(tr, setl, 1)


def createObjCf(diff_dict, setl, cf, tr, instr, tr_c=None, leg_c = None, cf_c=None, res_c=None, tr_for_sec_nom = None):
    '''instr can be ins_c, cf must not be cf_c.
    Check res_c if None'''
    # Note that Reset updates come here as well!
    instype = None    
    correction_amount = 0    
    #remove bellow ael calls
    cf_c = set_c(cf_c, cf, 'CashFlow')
    tr_c = set_c(tr_c, tr, 'Trade')
    correction = diff_dict.has_key('correction')    
    if tr and tr.insaddr:
        instrument = tr.insaddr
        instype = tr.insaddr.instype        
    if instr:
        instrument = instr
        instype = instr.instype
    leg = cf.legnbr
    if leg_c:
        leg = leg_c 
    if diff_dict.has_key('curr.insid'):
        if cf.legnbr.insaddr.instype == 'DualCurrBond' and \
           cf.type=='Fixed Amount':
            setl['curr'] = leg.redemption_curr.insaddr
        else:
            setl['curr'] = leg.curr.insaddr
    if diff_dict.has_key('type'):                
        if FSettlementGeneral3.is_valid_cf_type(cf_c):
            setl['type'] = FSettlementGeneral3.get_cf_type(cf_c)
        elif cf:
            pr = "CashFlow %d has changed type, type will not be changed for settlement %d" % (cf.cfwnbr, setl.seqnbr)
            log(1, pr)        
            
    if (cf_c.pay_day != setl.value_day) or \
        diff_dict.has_key('pay_day') or diff_dict.has_key('day') or \
        diff_dict.has_key('rolling_base_day') or diff_dict.has_key('value') or \
        diff_dict.has_key('read_time') or diff_dict.has_key('value_day') or \
        diff_dict.has_key('exp_day') or diff_dict.has_key('value_day2'):
        pr = "CashFlow %d has new pay_day! Changing settlement value_day from %s to %s." % \
        (cf.cfwnbr, setl.value_day, cf_c.pay_day)
        log(5, pr)                    
        setl['value_day'] = cf_c.pay_day

    if instype in FSettlementGeneral.issuer_list and not \
       setl.type=='Coupon transfer':
        if FSettlementGeneral.check_primary_issuance(tr, diff_dict):
            if tr_c.counterparty_ptynbr:
                setl['party_ptyid'] = tr_c.counterparty_ptynbr.ptyid
        else:
            if diff_dict.has_key('issuer_ptynbr') or \
                   diff_dict.has_key('primary_issuance'):
                if diff_dict.has_key('issuer_ptynbr'):
                    issuer = ael.Party[int(diff_dict['issuer_ptynbr'])]
                    if issuer:
                        setl['party_ptyid'] = issuer.ptyid
                elif tr_c and tr_c.insaddr.issuer_ptynbr:
                    setl['party_ptyid'] = tr_c.insaddr.issuer_ptynbr.ptyid
                elif instrument.issuer_ptynbr:
                    setl['party_ptyid'] = instrument.issuer_ptynbr.ptyid
                else:
                    setl['party_ptyid'] = ''
            elif diff_dict.has_key('issuer_ptynbr.ptyid'):
                setl['party_ptyid'] = diff_dict['issuer_ptynbr.ptyid']
            elif instrument.issuer_ptynbr:
                setl['party_ptyid'] = instrument.issuer_ptynbr.ptyid
            else:
                setl['party_ptyid'] = ''
    elif tr_c and tr_c.counterparty_ptynbr:                
        if diff_dict.has_key('counterparty_ptynbr.ptyid'):
            setl['party_ptyid'] = diff_dict['counterparty_ptynbr.ptyid']
        elif diff_dict.has_key('ipa'):
            setl['party_ptyid'] = diff_dict['ipa']
        elif diff_dict.has_key('ipa_removed'):
            setl['party_ptyid'] = tr_c.counterparty_ptynbr.ptyid
    if not tr and not instr and diff_dict.has_key('quantity'):
        # akta FSettlementAMB.set_dict_values
        if setl:
            pr = 'Alert! Amount of setlement %d might not be updated! (File)' % (setl.seqnbr)
            log(1, pr)
    elif tr and not instr:
        if correction:
            correction_amount = FSettlementGeneral2.get_corrected_setl(cf, tr, None)
        setl['amount'] = FSettlementGeneral2.get_cashflow(tr, cf, correction_amount)
        setl['curr'] = leg.curr.insaddr
    elif instr:
        if setl.type=='Coupon' or setl.type=='Redemption':
            settle = FSettlementGeneral2.get_security(cf, None, setl.to_prfnbr, None, tr_for_sec_nom)
            if settle:
                pos = FSettlementGeneral2.get_position(settle, cf_c.pay_day)
                setl['amount'] = pos * cf.projected_cf()
                coupon_already_exists, new_amount = FSettlementGeneral3.intact_coupon_amount(setl)
                if coupon_already_exists and round(new_amount, 6) != 0:
                    setl['amount'] = new_amount
                
                setl['curr'] = leg.curr.insaddr
                tr = settle.trdnbr
        elif setl.type=='Coupon transfer':
            tr = ael.Trade[setl.trdnbr]
            setl['amount'] = FSettlementGeneral2.coupon_transfer_amount(tr, cf, cf_c)
            setl['curr'] = leg.curr.insaddr
                
    FSettlementGeneral.account_info(tr, setl, 1)

def createObjDiv(diff_dict, setl, div, ins_c=None, tr_c=None, comb_info = None):
    '''div can be div_c '''
    if not div or not setl:
        pr = 'createObjDiv: div or setl is not, None will be returned'
        log(1, pr)
        return
    pr = ''
    ins_c = set_c(ins_c, div.insaddr, 'Instrument')
    if diff_dict.has_key('curr.insid'):
        setl['curr'] = div.curr.insaddr

    settle = FSettlementGeneral2.get_security(None, div, setl.to_prfnbr)
    if settle:
        tr_c = settle.trdnbr
        pos = FSettlementGeneral2.get_position(settle, div.pay_day)
        setl['amount'] = FSettlementGeneral2.get_dividend(div, tr_c, ins_c, pos)
        setl['curr'] = div.curr.insaddr
        
    if ins_c.instype == "EquitySwap":
        setl['amount'] = FSettlementGeneral2.get_dividend(div, tr_c, ins_c, 0, comb_info)
        setl['curr'] = div.curr.insaddr
        
    if diff_dict.has_key('pay_day') or diff_dict.has_key('value_day') or diff_dict.has_key('day'):
        setl['value_day'] = div.pay_day

    if diff_dict.has_key('issuer_ptynbr.ptyid') or diff_dict.has_key('issuer_ptynbr'):
        setl['party_ptyid'] = FSettlementGeneral.get_counterparty(tr_c, ins_c, 1, 1) 
    tr = None
    if tr_c:        
        tr = ael.Trade[tr_c.trdnbr]        
    FSettlementGeneral.account_info(tr, setl, 1, tr_c)   #trade was none before   

def createObjPay(diff_dict, setl, pay, tr):
    '''pay can be pay_c '''
    correction_amount = 0
    correction = diff_dict.has_key('correction') or FSettlementGeneral2.is_correction_trade(tr)
    
    if diff_dict.has_key('amount') or correction:
        if correction:
            correction_amount = FSettlementGeneral2.get_corrected_setl(pay, tr, None, setl)
        setl['amount'] = FSettlementGeneral2.get_payment(tr, pay, correction_amount)
        if pay.curr:
            setl['curr'] = pay.curr.insaddr
    if diff_dict.has_key('payday'):            
        setl['value_day'] = pay.payday
    if diff_dict.has_key('type'):
        if diff_dict['type'] not in FSettlementGeneral.invalid_payment_types and pay:
            setl['type'] = FSettlementGeneral3.get_pay_type(pay)
        elif pay:
            pr = "Payment %d has changed type, type will not be changed for settlement %d" % (pay.paynbr, setl.seqnbr)
            log(1, pr)
                
    if diff_dict.has_key('curr.insid'):
        curr = ael.Instrument[diff_dict['curr.insid']]
        if curr:
            setl['curr'] = curr.insaddr
        else:
            setl['curr'] = pay.curr
    if diff_dict.has_key('our_accnbr'):
        our_accnbr = int(diff_dict['our_accnbr'])
        setl['acquirer_accname'] = FSettlementGeneral.account_name(our_accnbr)
        setl['acquirer_account'] = FSettlementGeneral.account_account(our_accnbr)
        if our_accnbr:
            acc = ael.Account[our_accnbr]
            if acc:    
                acq = acc.ptynbr
                if acq:            
                    setl['acquirer_ptyid']= acq.ptyid

    if diff_dict.has_key('our_accnbr.ptyid'):
        setl['acquirer_ptyid'] = diff_dict['our_accnbr.ptyid']
    elif diff_dict.has_key('our_accnbr.ptynbr'):
        party = ael.Party[int(diff_dict['our_accnbr.ptynbr'])]
        if party:
            setl['acquirer_ptyid']= party.ptyid
    if diff_dict.has_key('accnbr'):
        accnbr = int(diff_dict['accnbr'])
        setl['party_accname'] = FSettlementGeneral.account_name(accnbr)
        setl['party_account'] = FSettlementGeneral.account_account(accnbr)
    if diff_dict.has_key('accnbr.ptyid'):
        setl['party_ptyid'] = diff_dict['accnbr.ptyid']
    elif diff_dict.has_key('accnbr.ptynbr'):
        party = ael.Party[int(diff_dict['accnbr.ptynbr'])]
        if party:
            setl['party_ptyid']= party.ptyid
    elif pay.ptynbr and diff_dict.has_key('ptynbr.ptyid'):
        if pay.accnbr == None:
            setl['party_ptyid'] = pay.ptynbr.ptyid
    
def create_setlObj(oldSetl, diff_dict, tr, cf, div, pay, typ, instr, comblink=None, tr_c=None, leg_c = None, cf_c=None, res_c=None, \
                   trade_update = False, tr_for_sec_nom = None, comb_info = None):
    '''Takes an existing setlement object as a input. Changes some attributes 
    according to diff_dict that contains attribute names and its values. 
    Different entities are deployed and if only trade is deployed then 
    the type can be premium, sec nominal or fee.
    tr_c is trade entity class parsed via the incomming amb message, 
    tr_c MUST BE DEPLOYED if tr is used/deployed! instr and div can be ent_c.'''
   
    amount = None
    curr = None 
    fee = None
    insid = None
    setl = None    # old setl to be renewed
    dictOK = 0
    trOK = 0
    instrOK = 0
    entityMode = 0 # cf, div or payment is deployed
    trade_types = ['Premium', 'Fee', 'Security Nominal']    
    oldSetlOK = 1 # input not ael_entity, settlement object expected   
    instype = None
    corrected_setl = 0    
    tr_c = set_c(tr_c, tr, 'Trade')
    cf_c = set_c(cf_c, cf, 'CashFlow')    
    
    if diff_dict:
        k = len(diff_dict.keys())
        if k:
            dictOK = 1
        else:
            log(0, 'empty diff_dict')
    else:
        log(0, 'createSetlObj: no diff_dict (File)')
    
    if is_trade(tr_c):
        trOK = 1
        trade_update = True
        if tr_c.insaddr:
            instype = tr_c.insaddr.instype
    elif instr:
        instrOK = 1
        instype = instr.instype
    else:
        log(1, 'create_setlObj: trade/instr not deployed')

    if div or cf or pay:
        entityMode = 1 #otherwise mode with trade and its type

    if oldSetl:
        if type(oldSetl) == ael.ael_entity:
            oldSetlOK = 0
            log(1, 'create_setlObj: input oldSet is entity not instance!!! File')
    if oldSetlOK and (trOK or instrOK) and dictOK:
        setl = oldSetl        
        if diff_dict.has_key('trdnbr'):
            oldtr = int(setl['trdnbr'])
            newtr = int(diff_dict['trdnbr'])
            setl['trdnbr'] = newtr
            pr = 'create_setlObj: Settlement %d trdnbr %d --> %d'\
                 % (setl['seqnbr'], oldtr, newtr)
            log(0, pr)

        if diff_dict.has_key('protection') and tr_c:
            setl['protection'] = tr_c.protection
            
        elif diff_dict.has_key('protection'):
            setl['protection'] = diff_dict['protection']
            
        if diff_dict.has_key('owner_usrnbr') and tr_c:
            setl['owner_usrnbr'] = tr_c.owner_usrnbr.usrnbr
        elif diff_dict.has_key('owner_usrnbr'):
            setl['owner_usrnbr'] = int(diff_dict['owner_usrnbr'])

        # sec nom uses tr.acquire_day, handled later...
        if diff_dict.has_key('value_day'):
            if not entityMode and typ not in FSettlementGeneral.sec_types:            
                setl['value_day'] = ael.date(diff_dict['value_day']) 

        # ENTITIES HAVE BEEN HANDLED NOW, set account information
        # set acquirer_accname and acquirer_account ##
        account_acq = 0
        account_pty = 0

        # acquirer_ptyid for trade, cf and div (not payment) ###
        if diff_dict.has_key('acquirer_ptynbr.ptyid'):
            setl['acquirer_ptyid'] = diff_dict['acquirer_ptynbr.ptyid']
            
        # party_ info ###
        # should always correspond FSettlementGeneral.*_creation functions
        if not entityMode:
            if typ != 'Fee':
                if diff_dict.has_key('counterparty_ptynbr.ptyid'):
                    setl['party_ptyid']=diff_dict['counterparty_ptynbr.ptyid']
                elif diff_dict.has_key('ipa'):
                    setl['party_ptyid'] = diff_dict['ipa']
                elif diff_dict.has_key('ipa_removed'):
                    setl['party_ptyid'] = tr_c.counterparty_ptynbr.ptyid
            elif typ == 'Fee':                
                if diff_dict.has_key('broker_ptynbr.ptyid'):
                    setl['party_ptyid'] = diff_dict['broker_ptynbr.ptyid']
                    # setl['party_accname'] and setl['party_account'] remain
                elif diff_dict.has_key('broker_ptynbr'):                    
                    p = ael.Party[int(diff_dict['broker_ptynbr'])]
                    if p:
                        setl['party_ptyid'] = p.ptyid

        if diff_dict.has_key('prfnbr'):
            if amount:
                if amount > 0:
                    setl['to_prfnbr'] = int(diff_dict['prfnbr'])
                else:
                    setl['from_prfnbr'] = int(diff_dict['prfnbr'])
            elif trOK and tr_c.prfnbr:
                # amount has not changed above so retrieve portfolio via trade
                if setl['amount'] > 0:
                    setl['to_prfnbr'] = tr_c.prfnbr.prfnbr
                else:
                    setl['from_prfnbr'] = tr_c.prfnbr.prfnbr
        
        if div and instrOK:
            createObjDiv(diff_dict, setl, div, instr, tr_c)
        elif div and trade_update:
            createObjDiv(diff_dict, setl, div, instr, tr_c, comb_info)
        elif cf and trOK:
            createObjCf(diff_dict, setl, cf, tr, None, tr_c)
        elif cf and instrOK:        
            createObjCf(diff_dict, setl, cf, None, instr, None, leg_c, cf_c, res_c, tr_for_sec_nom)
        elif pay and trOK:
            createObjPay(diff_dict, setl, pay, tr)
        elif not entityMode and trOK:
            createObjTrade(typ, diff_dict, setl, tr, comblink, tr_c, instr)

    else:
        log(1, 'create_setlObj: empty setl returned')
    return setl

def set_curr(diff_dict, curr):
    return FSettlementGeneral3.set_curr(diff_dict, curr)
    
def divs_from_instrument(instr, div_dict=None, from_trade = 0):
    return FSettlementGeneral3.divs_from_instrument(instr, div_dict, from_trade)
    
def get_bank_day_per_curr(inst):
    return FSettlementGeneral3.get_bank_day_per_curr(inst)

def end_security_value_day(tr, combination_member, ins_c=None):
    return FSettlementGeneral3.end_security_value_day(tr, combination_member, ins_c)
    
def log(level, s):
    return FSettlementGeneral.log(level, s)

def set_c(ent_c, ent, entity_type):
    '''AMB is called due to global variable version_not_ok'''
    return FSettlementAMB.set_c(ent_c, ent, entity_type)

def get_premium_settlement_record(trade):
    return_list = []
    settlements = ael.Settlement.select('trdnbr=%d' % trade.trdnbr)
    for settlement in settlements:
        if settlement.type == 'Premium':
            return_list.append(settlement)
            break
    return return_list
    
def get_closed_security_nominals_for_corrected_trades(trade):
    sec_nom_list = []
    corrected_trades = get_all_corrected_trades(trade)
    if len(corrected_trades):
        for corrected_trade in corrected_trades:
            settlements = ael.Settlement.select('trdnbr=%d' % corrected_trade.trdnbr)
            for settlement in settlements:
                if settlement.type == 'Security Nominal' and \
                settlement.status == 'Closed':
                    sec_nom_list.append(settlement)
    return sec_nom_list
    
def get_all_corrected_trades(trade):
    corrected_trade = trade.correction_trdnbr
    if corrected_trade and corrected_trade.trdnbr != trade.trdnbr:
        return [corrected_trade] + get_all_corrected_trades(corrected_trade)
    else:
        return []
        
def trade_has_security_nominal(trade):
    answer = False
    settlements = ael.Settlement.select('trdnbr=%d' % trade.trdnbr)
    for settlement in settlements:
        if settlement.type == 'Security Nominal':
            answer = True
            break
    return answer
    
def is_correction_sec_nom_update(trade, settlement):
    if trade.insaddr:
        ins_ref = trade.insaddr
        if trade.insaddr.instype in FSettlementGeneral.und_ins_security:
            ins_ref = trade.insaddr.und_insaddr
        return (ins_ref.instype in ['Bond', 'Stock'] and\
                settlement.type == 'Security Nominal' and \
                FSettlementGeneral3.is_correction_trade(trade) and\
                len(get_closed_security_nominals_for_corrected_trades(trade)))
    return False
    
def is_correction_trade_handling(tr, ins, corrected_sn):
    ins_ref = ins
    if ins.instype in FSettlementGeneral.und_ins_security:
        ins_ref = ins.und_insaddr
    return (ins_ref.instype in ['Bond', 'Stock'] and \
            FSettlementGeneral2.is_correction_trade(tr) and \
            not FSettlementGeneral.calc_security_nominal(tr, None, corrected_sn, 0, ins)\
            and not trade_has_security_nominal(tr) and \
            len(get_closed_security_nominals_for_corrected_trades(tr)))
            
def trade_has_dividend_settlement_record(trade, dividend):
    result_set = ael.Settlement.select('trdnbr = %d' % trade.trdnbr)
    exists = False
    for settlement in result_set:
        if settlement.dividend_seqnbr and \
           settlement.dividend_seqnbr.seqnbr == dividend.seqnbr:
           exists = True
           log(1, 'Settlment already exist for trade %d dividend %d' % (trade.trdnbr, dividend.seqnbr))
           break
    return exists
    
def update_combination_eq_swap_dividends(tr_c, diff_dict, trade_update = 0):
    eq_swap_list = []
    if tr_c.insaddr and tr_c.insaddr.instype == 'Combination':
        set_equity_swaps_in_list(eq_swap_list, tr_c.insaddr)
        for (eq_swap, comb_link) in eq_swap_list:
            divs = divs_from_instrument(eq_swap, None, 1)
            comb_info = CombInfo(tr_c.insaddr, comb_link)
            for d in divs:
                if trade_update:
                    update_div(d, diff_dict, eq_swap, tr_c, 1, trade_update, comb_info)
                else:
                    update_div(d, diff_dict, eq_swap, tr_c, 0, trade_update, comb_info)

