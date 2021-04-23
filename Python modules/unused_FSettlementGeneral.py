""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementGeneral - Module including all functions common to the 
                         Settlement population and update process.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module contains those functions which are common to the Settlement
    population and update process.

----------------------------------------------------------------------------"""
import ael, FSettlementParams, FSettlementGeneralRT, FSettlementGeneral2
import FSettlementSTP, FSettlementGeneral3, FSettlementNetting

param = FSettlementParams.get_default_params()
verbosity = param.verbosity # see log(level, s)
acc_curr = param.acc_curr
trans_size = param.trans_size

#pre-settlement status
delete_status = ['New', 'Recalled', 'Updated', 'Exception', 'Manual Match',\
                 'Hold', 'Void', 'Authorised', 'Not Acknowledged']

unexpected_credit_status = ['Unexpected Credit']

#post-settlement status: keep_status deleted via SPR 275715

fictitious_types = ['Credit Default', 'Total Return']

reset_types = ['Call Float Rate', 'Float Rate', 'Caplet', 'Digital Caplet',
               'Digital Floorlet', 'Floorlet', 'Redemption Amount', 'Return']

# Both Reset and CF types are:
# Call Float Rate, Float Rate, Caplet, Digital Caplet, Digital Floorlet,
# Floorlet, Redemption Amount, Return
cf_types = ['Fixed Amount', 'Fixed Rate', 'Float Rate', 'Caplet', 'Floorlet',
            'Digital Caplet', 'Digital Floorlet', 'Total Return', 
            'Credit Default', 'Call Fixed Rate', 'Call Float Rate', 
            'Redemption Amount', 'Zero Coupon Fixed', 'Return', 'Dividend',
            'Interest Reinvestment', 'Call Fixed Rate Adjustable',
            'Fixed Rate Adjustable']

# PaymentTypes that should not result in a settlement record
# empty string is used for backcompability purposes
invalid_payment_types = ['Aggregated Settled', 'Aggregated Accrued',
                         'Aggregated Funding', 'Aggregated Dividends',
                         'Aggregated Fees', 'Aggregated Depreciation',
                         'Aggregated Future Settle',
                         'Aggregated Forward Funding PL',
                         '']

premium_types = ['Premium', 'Broker Fee', 'Security Nominal',
                 'Premium 2', 'End Security']

#settlement status that are not to be voided
not_to_void = ['Released', 'Acknowledged', 'Pending Closure']

# from_status_to_void and new_status_to_void are used
# in the trade update process in the FSettlementAMB

# trades that get any of these statuses should be "recalled" in Settlement table
if param.recall_if_trade_status_is_void:
    new_status_to_void = ['Void', 'Confirmed Void', 'Terminated', 'Simulated']
else:
    new_status_to_void = ['Confirmed Void', 'Terminated', 'Simulated']

# trades that have had following status will be recalled if the
# new status is represented in new_status_to_void
if param.recall_if_trade_status_is_void:
    from_status_to_void = ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed',
                           'Legally Confirmed', 'Internal', 'Exchange', 'Terminated']
else:
    from_status_to_void = ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed',
                           'Legally Confirmed', 'Internal', 'Exchange', 'Terminated', 'Void']


# if the settlement is in any of these statuses then STP-rules will be applied
stp_status = ['New', 'Exception', 'Manual Match', 'Authorised']

# Security types
sec_types = ['End Security', 'Security Nominal']    

# Instrument types to generate Security Nominals for
ins_security = ['Bill', 'Zero', 'Bond', 'Convertible', 'FRN', 'IndexLinkedBond',
                'PromisLoan', 'Stock', 'DualCurrBond', 'CLN', 'MBS/ABS',
                'FreeDefCF']
                
und_ins_security = ['SecurityLoan', 'Repo/Reverse', 'BuySellback']

ins_combination = ['EquityIndex', 'CreditIndex', 'Combination']    

# Instrument types that coupons should be created for, based on instrument
# position. See also function coupon_ok!
coupon_types = ['Bond', 'DualCurrBond', 'IndexLinkedBond', 'PromisLoan', 'FRN',
                'Zero']

# Instrument types in addition to coupon_types for which fixed amount should be
# generated on position level
fixed_amount_pos = ['Bill']

# fields of the Settlement object used for comparation
cf_fields   = ['trdnbr', 'type', 'curr', 'value_day', 'amount']
div_fields  = ['trdnbr', 'type', 'curr']
secnom_fields = ['trdnbr', 'type']
tr_fields   = ['trdnbr', 'type']
pay_fields  = ['trdnbr', 'type', 'curr', 'party_ptyid', 'value_day',\
'party_accname', 'amount']
all_fields  = ['seqnbr', 'trdnbr', 'cfwnbr', 'dividend_seqnbr', 'paynbr', 'amount',\
 'curr', 'value_day', 'settle_seqnbr', 'ref_seqnbr', 'to_prfnbr', 'from_prfnbr', \
 'settleinstruction_seqnbr', 'status', 'type', 'settle_category', \
 'ref_type', 'delivery_type', 'acquirer_ptyid', 'acquirer_account', \
 'acquirer_accname', 'party_ptyid', 'party_account', 'party_accname', \
 'text', 'status_explanation', 'netting_rule_seqnbr', \
 'manual_match', 'post_settle_action']

stp_fields = ['trdnbr', 'type', 'curr', 'value_day', 'amount', 'to_prfnbr',\
              'from_prfnbr', 'acquirer_ptyid', 'acquirer_account',\
              'acquirer_accname', 'party_ptyid', 'party_account', 'party_accname',
              'settle_seqnbr', 'settle_category']

# Default Instrument types that are supported are 
# now stated in the FSettlementParams
# Note that FSettlementVariable.valid_instrument_types contains
# customer specific list that might exclude some instrument types
#valid_instr = []

cf_diff_acc = ['Curr', 'FxSwap', 'CurrSwap']

issuer_list = ['Bill', 'Bond', 'CD', 'DualCurrBond', 'FRN', 'IndexLinkedBond',
               'MBS/ABS', 'PromisLoan', 'Zero']

# Dictionary with entities to commit generated out of one AMBA message
trans_dict = {}

# Dictionary with settlements, uses special key
double_dict = {}

# Dictionary with settlement entity classes to do STP on
settle_dict = {}

# Dictionary with settlements to net
net_dict = {}

# List with deleted settlements
delete_list = []

# See get_version_entity()
versions = ['entity', 'Trade', 'Instrument', 'Party', 'Settlement']

def remove_net():
    pr = 'remove_net'
    log(3, pr)

    net_list = []
    status = ael.enum_from_string('SettlementStatus', 'Released')
    sel = ael.Settlement.select()
    for s in sel:
        if s.netting_rule_seqnbr and s.ref_type=='Net':
            net_list.append(s)
    for net in net_list:
        sel = ael.Settlement.select('ref_seqnbr=%d' % net.seqnbr).members()
        if len(sel) == 0:
            n_status=ael.enum_from_string('SettlementStatus', net.status)
            if n_status < status:
                pr = 'Net Settlement %d will be deleted' % (net.seqnbr)
                log(3, pr)
                log(4, net.pp())
                net.delete()
            
def append_settle(stt_c):
    ''' '''
    global settle_dict
    if stt_c:
        if get_mod_settle(stt_c.seqnbr):
            pr = 'append_settle: %d already there (File)' % (stt_c.seqnbr)
            log(2, pr)        
            settle_dict[stt_c.seqnbr].compare(stt_c)
        settle_dict[stt_c.seqnbr] = stt_c

def append_net(settle):
    '''settle should not be stt_c!'''
    global net_dict    
    if settle:
        if get_net(settle) != None:
            pr = 'append_net: %d already there (File)' % (settle.seqnbr)
            log(2, pr)        
            setl_diff(net_dict[settle.seqnbr], settle)
        net_dict[settle.seqnbr]=settle

def get_net(net):
    if not net.seqnbr:
        return None
    global net_dict
    if net_dict.has_key(net.seqnbr):
        return net_dict[net.seqnbr]
    else:
        return None

def append_transaction(settle, combination_member=None):
    ''' stt_c is not needed'''
    global trans_dict
    global double_dict
    if settle:
        if settle.seqnbr < 0:
            trdnbr='0'
            cfwnbr='0'
            paynbr='0'
            dividend_seqnbr='0'
            
            if settle.trdnbr:
                trdnbr = '%s' % settle.trdnbr.trdnbr
                if combination_member:
                    pr = "append_transaction for combmember %s" % (combination_member.insid)
                    log(5, pr)
                    trdnbr = '%s%s' % (trdnbr, combination_member.insid)                
            
            if settle.cfwnbr:
                cfwnbr = '%s' % settle.cfwnbr.cfwnbr
            elif settle.paynbr:
                paynbr = '%s' % settle.paynbr.paynbr
            elif settle.dividend_seqnbr:
                dividend_seqnbr = '%s' % settle.dividend_seqnbr.seqnbr
            
            str2 = trdnbr + cfwnbr + paynbr + dividend_seqnbr
            if settle.type in premium_types or FSettlementGeneral2.is_interest_accrued(settle) or \
               settle.type == 'Coupon transfer':
                str2 = str2 + settle.type
            added = 0
            for k, v in double_dict.items():
                if k == str2:
                    if trans_dict.has_key(v):#
                        pr = "%s in trans_dict will be replaced!" % (k)
                        log(5, pr)
                        setl_diff(trans_dict[v], settle)
                        del trans_dict[v]
                    double_dict[k] = settle.seqnbr
                    added = 1
                    break
            if not added:
                double_dict[str2] = settle.seqnbr
        # positive seqnbr setls are added to trans_dict
        trans_dict[settle.seqnbr] = settle
        

def commit_transaction(alt_trans_size=0):

    global trans_dict
    count = 0
    to_delete=[]
    ts = trans_size # see FSettlementVariable
    if alt_trans_size != 0:
        ts = alt_trans_size #use deployed trans size

    try:
        ael.begin_transaction()
        for k, v in trans_dict.items():
            commit_ok = 1
            #equity swap dividens might already be deleted by the FSEQEquitySwap script 
            if v.type == "Dividend" and not v.dividend_seqnbr and v.trdnbr:                
                if v.trdnbr.insaddr.instype == "EquitySwap":
                    commit_ok = 0
                    
            if v.trdnbr and is_excluded_acq_trade(v.trdnbr):
                commit_ok = 0
            
            if v.trdnbr and is_prevent_settlement_processing_for_trade(v.trdnbr):
                commit_ok = 0
    
            if v.trdnbr and is_excluded_portfolio_trade(v.trdnbr):
                commit_ok = 0

            if v.trdnbr and not FSettlementGeneral3.check_otc_handling(v.trdnbr):
                commit_ok = 0
                
            if commit_ok:
                v.commit()
            to_delete.append(k)
            count+=1
            if count >= ts:
                break
        ael.commit_transaction()
        pr = 'Transaction commited, trans_dict (File)'
        log(4, pr)

        if len(to_delete) == len(trans_dict.keys()):
            trans_dict = {}
            pr = 'Transaction list emptied (File)'
            log(4, pr)
        else:
            for k in to_delete:
                remove_trans(k)
            pr = 'Transaction list emptied, %d settlements left (File)' % (len(trans_dict.keys()))
            log(4, pr)        
                
    except Exception, e:
        print_trans(trans_dict, "trans_dict")
        ael.abort_transaction()
        pr = '%d settlements in the transaction (File)' % (len(trans_dict.keys()))
        log(0, pr)            
        pr = 'ERROR: %s. Unable to commit transaction (File)' % (str(e))
        log(0, pr)

        if 'SQL query too large' in str(e):
            ts = ts/2
            pr = 'Trying insted with transaction size %d (File)' % (ts)
            log(0, pr)
        else:
            pr = 'This transaction will be dropped. (File)'
            log(0, pr)
            trans_dict = {}

    if len(trans_dict.keys()):
        commit_transaction(ts)


def commit_settlements():
    global settle_dict
    global net_dict
    global double_dict
    global delete_list
    
    for k, stt_c in settle_dict.items():
        if settle_dict.has_key(k): # DO NOT REMOVE
            FSettlementSTP.STP(stt_c, param)
    
    commit_net()
    remove_net()
    
    settle_dict = {}
    net_dict = {}
    double_dict = {}
    delete_list = []


def commit_net(alt_trans_size=0):
    'Called from commit_settlements in order to commit netted settlements'
    
    global net_dict
    
    count = 0    
    to_delete=[]
    ts = trans_size
    if alt_trans_size != 0:
        ts = alt_trans_size
    cont = 0
    
    if param.round_net_amount:
        parent_list = FSettlementNetting.get_net_parents(net_dict)
        for parent in parent_list:
            net_list = FSettlementNetting.get_net_children(net_dict, parent)
            rounded_amount = FSettlementNetting.round_net_amount(net_list, None, 0)
            parent.amount = rounded_amount
        
    try:
        ael.begin_transaction()
        for n, m in net_dict.items():
            m.commit()
            to_delete.append(n)
            count+=1
            if count >= ts:                
                break
        ael.commit_transaction()
        pr = 'Transaction commited, net_dict (File)'
        log(4, pr)
        
        if len(to_delete) != len(net_dict.keys()):
            for n in to_delete:
                remove_net_dict(n)
            pr = 'Transaction list (net_dict) emptied, %d settlements left (File)' % (len(net_dict.keys()))
            log(4, pr)
            cont = 1
                
    except Exception, e:
        print_trans(net_dict, "net_dict")
        ael.abort_transaction()
        pr = 'net_dict includes %d settlements (File)' % (len(net_dict.keys()))
        log(0, pr)
        pr = 'ERROR: %s. Unable to commit transaction (File)' % (str(e))
        log(0, pr)

        if 'SQL query too large' in str(e):
            ts = ts/2
            pr = 'Trying to net instead with transaction size %d (File)' % (ts)
            log(0, pr)
        else:
            pr = 'This netting transaction will be dropped. (File)'
            log(0, pr)
            net_dict = {}
    
    if len(net_dict.keys()) and cont:
        commit_net(ts)


def get_mod_trans(seqnbr):
    global trans_dict
    
    if trans_dict.has_key(seqnbr):
        return trans_dict[seqnbr]
    else:
        return None

def get_mod_settle(seqnbr):
    '''Returns stt_c or None '''
    global settle_dict
    if settle_dict.has_key(seqnbr):
        return settle_dict[seqnbr]
    else:
        return None
    
def work_to_do():
    global trans_dict
    
    if len(trans_dict.keys()):
        return 1
    else:
        return 0

def stp_to_run():
    global settle_dict

    if len(settle_dict.keys()):
        return 1
    else:
        return 0
    
def remove_trans(seqnbr):
    global trans_dict
    if trans_dict.has_key(seqnbr):
        del trans_dict[seqnbr]

def remove_settle(seqnbr):
    global settle_dict
    if settle_dict.has_key(seqnbr):
        del settle_dict[seqnbr]

def remove_net_dict(seqnbr):
    global net_dict
    if net_dict.has_key(seqnbr):
        del net_dict[seqnbr]


def append_delete(seqnbr):
    global delete_list
    if seqnbr:
        delete_list.append(seqnbr)
    return

def is_deleted(seqnbr):
    global delete_list
    deleted = 0
    if seqnbr:
        if seqnbr in delete_list:
            deleted = 1
    return deleted

def check_status_exp(explanation):
    ok =1
    cu = ael.enum_from_string('StatusExplanation', 'Change to source data')
    cc = ael.enum_from_string('StatusExplanation', 'Recalled data')
    if (explanation & pow(2, cu)):
        ok = 0
    if (explanation & pow(2, cc)):
        ok = 0
    return ok        

def check_manually_authorised(explanation):
    ok = 1
    ma = ael.enum_from_string('StatusExplanation',\
                              'Late payment -manually authorised')
    if (explanation & pow(2, ma)):
        ok = 0
    return ok

def print_commit(setl):
    'Default print when commiting to Settlement table'
    
    if setl:
        if setl.trdnbr:
            str = "%s, Trade %s, Settlnbr %d" % (setl.type, setl.trdnbr.trdnbr, setl.seqnbr)
            log(1, str)
    return

#class Settlement: see FSettlementGeneral3!

class DeliveryType:
    acq_type = 'None'
    counter_type = 'None'
            
def check_references(seqnbr):
    referenced = 0
    settle = ael.Settlement[seqnbr]
    if settle:
        if settle.ref_type=='Split':
            referenced = 1
            pr = "check_references: Settlement %d referenced (Split)" % (seqnbr)
            log(5, pr)
        elif settle.ref_seqnbr and settle.ref_type=='Net Part':
            referenced = 1
            pr = "check_references: Settlement %d referenced (Net Part)" % (seqnbr)
            log(5, pr)

    return referenced

def check_already_updated(seqnbr, check_status):
    referenced_to = 0
    sel = ael.Settlement.select('ref_seqnbr=%d' % seqnbr)
    if sel:
        for s in sel:
            if s.ref_type=='None' and not check_status:
                referenced_to = 1
                break
            elif s.ref_type=='None' and check_status:
                if s.status=='Closed':
                    referenced_to = 1
                    break
    if referenced_to:
        pr = "check_already_updated: Settlement %d already updated" % (seqnbr)
        log(5, pr)
                    
    return referenced_to

def check_referenced_to(seqnbr, check_status):
    referenced_to = 0
    if seqnbr:
        try:
            sel = ael.Settlement.select('settle_seqnbr=%d' % seqnbr)
            if sel:
                referenced_to = 1
                if check_status:
                    pr = "check_referenced_to: Settlement %d referenced but status must be checked" % (seqnbr)
                    log(5, pr)
                    referenced_to = 0
                    for s in sel:
                        if s.status=='Closed':
                            referenced_to = 1
                            break
            if not referenced_to:
                referenced_to = check_already_updated(seqnbr, check_status)
            else:
                pr = "check_referenced_to: Settlement %d referenced" % (seqnbr)
                log(5, pr)
        except:
            sel = []

    return referenced_to
    
def get_setl_rows(trdnbr, setl_type, pay_day, combination_member=None, include=1, comb_link_removed = False):
    'Returns a list of Settlements with certain \
    type and trdnbr for a certain day. If premium, security nominal\
    or fee is requested pay_day is not mandatory.'

    ok = 1
    slist = []
    setls = []
    
    if trdnbr == None:
        log(0, 'get_setl_rows: trdnbr input is None! (File)')
        ok = 0
        
    if setl_type:
        if setl_type == '':
            ok = 0
            log(0, 'get_setl_rows: setl_type is empty! (File)')
    else:
        ok = 0
        log(0, 'get_setl_rows: setl_type input is None! (File)')
        
    if pay_day == None:
        ok = 0
        log(0, 'get_setl_rows: pay_day input is None! (File)')
        pay_day = ''

    if ok:
        try:
            setls = FSettlementGeneralRT.get_settlements(trdnbr, combination_member, setl_type, include, comb_link_removed)### IV or VI
        except:
            setls = []

        for setl in setls:
            if setl.type and setl.type == setl_type:
                # do we need create_selection(trdnbr, type):
                if pay_day != '':
                    if setl.value_day.to_string() == pay_day:
                        if source_data(setl):
                            #only source data setl row will be included
                            slist.append(setl)
                        else:
                            pr = 'Setl %d not source data (%s %s)' % \
                            (setl.seqnbr, pay_day, setl.type)
                            log(1, pr)
    
                    elif type(setl.value_day.to_string()) != type(pay_day):             
                        log(0, 'get_setl_rows: input pay_day must be a String') 
                else:
                    # pay_day is not mandatory for premium, 
                    # security nominal or fee 
                    if setl.type in ['Premium', 'Fee', 'Security Nominal',\
                                     'Premium 2', 'End Security']:
                        if source_data(setl):
                            slist.append(setl)
                            break
        l = 0
        if slist:
            l = len(slist)
            pr = "%d Settlements found for payday %s" % (l, pay_day)
            log(3, pr)   
    
    return slist

def get_tradelist_cf(cfwnbr):
    'Returns a list with trades connected to a Cash Flow'

    list = []

    if cfwnbr == None:    
        log(1, 'get_tradelist_cf: input cfwnbr is None. (File)')
        cf = None
    else:
        cf = ael.CashFlow[cfwnbr]
        
    if cf:
        leg = cf.legnbr
        if leg:            
            list = FSettlementGeneral3.get_trades(leg.insaddr)
    return list
    
def get_tradelist_div(divnbr):
    'Returns a list with trades in certain instrument (via dividend)'    
    
    list = []

    if divnbr == None:    
        log(0, 'get_tradelist_div: input divnbr is None.  (File)')
        div = None
    else:    
        div = ael.Dividend[divnbr]
    
    if div:
        list = FSettlementGeneral3.get_trades(div.insaddr)
    return list

def get_last_cashflow(leg):
    last_cfw = None
    for cfw in leg.cash_flows():
        if (cfw.type in ['Call Fixed Rate', 'Call Fixed Rate Adjustable', 'Call Float Rate']):
            if not last_cfw:
                last_cfw = cfw
            elif cfw.end_day > last_cfw.end_day:
                last_cfw = cfw
    return last_cfw
        
def is_last_cashflow(cashflow):
    last_cfw = get_last_cashflow(cashflow.legnbr)
    if (last_cfw and cashflow and cashflow.cfwnbr == last_cfw.cfwnbr):
        return True
    else:
        return False      

def check_payday_for_call_accounts(cashflow):
    ok = 1
    # This applies only for interests in open ended deposits with rolling period
    if ((cashflow.record_type == 'CashFlow') and 
        (cashflow.legnbr.insaddr.instype == 'Deposit') and
        (cashflow.type in ['Call Fixed Rate', 'Call Fixed Rate Adjustable', 'Call Float Rate']) and
        (cashflow.legnbr.insaddr.open_end != 'Terminated') and
        (cashflow.legnbr.rolling_period != '0d')):
        # Adjust the end_day according to the setting in the variables.
        period_end = None
        end_date = \
            ael.date(cashflow.end_day).add_banking_day(cashflow.legnbr.curr, \
                param.days_forward_for_call_account)
        if is_last_cashflow(cashflow):
            # If the variable 'days_forward_for_call_account' is set to something negative then
            # use the old behaviour and do not call ael function since it requires ATS of
            # version 3.2.2.hotfix33 or later.
            if (param.days_forward_for_call_account >= 0):
                # Get the end date of the rolling period from the leg
                period_end = cashflow.legnbr.find_last_rolling_date()
            if (period_end and end_date < period_end):
                ok = 0
    return ok

def paydayOK(paydate, object, flag, s_type):
    ok = 0
    if paydate:
        if type(paydate) == ael.ael_date:
            end_day = ''
            curr = ''
            if object:
                obj_type = object.record_type
                if (obj_type=='Trade'):
                    if s_type in sec_types:
                        if object.insaddr:
                            if object.insaddr.curr:
                                curr = object.insaddr.curr.insid
                    elif s_type=='Premium' or s_type=='Broker Fee' or \
                         s_type=='End Cash':
                        if object.curr:
                            curr = object.curr.insid
                    curr = object.curr.insid
                elif (obj_type=='CashFlow'):
                    if object.legnbr:
                        if object.legnbr.curr:
                            curr = object.legnbr.curr.insid
                        else:
                            curr = ael.used_acc_curr()
                elif obj_type in ['Dividend', 'Payment', 'Settlement']:
                    if object.curr:
                        curr = object.curr.insid
                    else:
                        curr = param.acc_curr
                else:
                    curr = param.acc_curr

                if (curr!=''):
                    # end_day is a bankingday based on the instrument currency
                    days_curr = FSettlementGeneralRT.get_bank_day_per_curr(curr)
                    
                    if ael.Instrument[curr]:
                        end_day = ael.date_today().add_banking_day(ael.Instrument[curr], days_curr)
                    else:
                        end_day = ael.date_today().add_banking_day(ael.Instrument[ael.used_acc_curr()], days_curr)

                    if flag == 0:
                        # intervall between today and end_day
                        if (ael.date_today() <= paydate <= end_day):
                            ok = 1
                    elif flag==1:
                        start_day = ael.date_today().add_banking_day(ael.\
                        Instrument[curr], (0-param.days_back))
                        # intervall between -days back and bankingday
                        if (start_day <= paydate <= end_day):
                            ok = 1                          
                    elif flag==2:
                        # intervall past untill bankingday
                        # this flag should be concidered as default!
                        if (paydate <= end_day):
                            ok = 1
                    else:
                        pr = 'paydayOK: invalid input flag %d' % flag
                        log(0, pr)
                        
                ok = (ok and check_payday_for_call_accounts(object))                        

                pr = 'paydayOK: %d (type: %s)' % (ok, obj_type)
                log(2, pr)
    else:
        log(0, 'paydayOK: The input to the paydayOK is null')

    return ok

def premium_creation(setl, pre, status, seqnbr, trade, flag, typ, comblink=None, corrected_setl=0, tr_c=None, ins_c=None,\
append_trans = 1):
    ''' Changes in this function need to be replicated to FSettlementGeneralRT.createObjTrade'''
    tr_c = FSettlementGeneralRT.set_c(tr_c, trade, 'Trade')
    ins_c = FSettlementGeneralRT.set_c(ins_c, tr_c.insaddr, 'Instrument')
    setl.type             = typ
    setl.status           = status
    FSettlementGeneral2.copy_protection_from_trade(setl, tr_c)
    combination_member = get_combination_member(comblink)
    if flag:
        setl.value_day        = tr_c.value_day
        setl.settle_category  = 'None'
        setl.curr             = tr_c.curr.insaddr
        if (typ == 'Premium'):
            setl.amount       = FSettlementGeneral2.get_premium(tr_c, corrected_setl)
        elif (typ == 'Fee'):
            setl.amount       = FSettlementGeneral2.get_fee(tr_c, corrected_setl)
        elif typ in sec_types:
            if typ=='Security Nominal':
                setl.amount       = calc_security_nominal(tr_c, comblink, corrected_setl, 0, ins_c)
                setl.value_day    = tr_c.acquire_day
            else:
                setl.amount       = calc_end_security(tr_c, comblink, corrected_setl, ins_c)
                setl.value_day    = FSettlementGeneralRT.end_security_value_day(tr_c, combination_member, ins_c)
            if tr_c.insaddr:
                instr = tr_c.insaddr
                if tr_c.insaddr.insaddr == ins_c.insaddr:
                    instr = ins_c # use instr bellow!
                else:
                    pr = "premium_creation: tr instrument %s differs from ins_c %s (Error)" % (tr_c.insaddr.insid, instr.insid)
                    log(1, pr)
                if instr.curr:
                    setl.curr         = instr.curr.insaddr
                if instr.instype in ins_security:
                    setl.sec_insaddr = instr.insaddr
                    setl.org_sec_nom = tr_c.insaddr.nominal_amount() # no ins_c here
                    if check_primary_issuance(trade):
                        setl.primary_issuance = 1
                elif instr.instype in und_ins_security:
                    if instr.und_insaddr:
                        setl.sec_insaddr=instr.und_insaddr.insaddr
                        if instr.und_insaddr.curr:
                            setl.curr = instr.und_insaddr.curr
                    if instr.instype in ['Repo/Reverse', 'SecurityLoan']:
                        setl.org_sec_nom = instr.ref_value
                    else:
                        setl.org_sec_nom = tr_c.insaddr.nominal_amount()
            if combination_member:                
                setl.curr         = combination_member.curr.insaddr
                setl.sec_insaddr  = combination_member.insaddr
                setl.org_sec_nom  = combination_member.nominal_amount()
                        
        elif typ == 'Premium 2':
            setl.curr         = FSettlementGeneral2.get_curr_premium2(tr_c, combination_member)
            setl.amount       = FSettlementGeneral2.get_premium2(tr_c, corrected_setl, comblink)
            setl.sec_insaddr  = tr_c.insaddr.curr.insaddr 
            if combination_member:                        
                setl.sec_insaddr  = combination_member.curr.insaddr                
    else:       
        setl.text       = pre.text              
        setl.amount     = pre.amount
        setl.curr       = pre.curr
        setl.value_day  = pre.value_day       
        setl.ref_seqnbr = pre.ref_seqnbr
        setl.ref_type   = pre.ref_type
        setl.settleinstruction_seqnbr = pre.settleinstruction_seqnbr
        setl.netting_rule_seqnbr = pre.netting_rule_seqnbr
        setl.manual_match = pre.manual_match
        setl.post_settle_action = pre.post_settle_action
        setl.settle_category = pre.settle_category
       
    setl.settle_seqnbr = seqnbr
    setl.trdnbr        = trade.trdnbr
    if tr_c.prfnbr:
        if setl.amount > 0:
            setl.to_prfnbr = tr_c.prfnbr.prfnbr
        else:
            setl.from_prfnbr = tr_c.prfnbr.prfnbr
   
    setl.acquirer_ptyid = get_acquirer(tr_c)
        
    if typ != 'Fee':
        ipa = issuing_paying_agent(trade)
        cp = tr_c.counterparty_ptynbr
        if ipa:
            setl.party_ptyid = ipa
        elif cp:        
            setl.party_ptyid = cp.ptyid
    elif typ == 'Fee':
        br = tr_c.broker_ptynbr
        if br:
            setl.party_ptyid = br.ptyid
        else:
            pr = 'No broker ptynbr for trade %d' % (trade.trdnbr)
            log(1, pr)
            
    account_info(trade, setl, 0)
    ret = None
    if append_trans:
        append_transaction(setl, combination_member)
        print_commit(setl)
    else:
        ret = setl
    return ret     

def create_from_settle(sel):
    
    l = []
    ok = 0
    if sel and type(l) == type(sel):
        ok = 1

    if ok:    
        for i in sel:
            values = {}
            values['seqnbr'] = i.seqnbr
            values['protection'] = i.protection
            owner = i.owner_usrnbr
            if owner:
                values['owner_usrnbr'] = owner.usrnbr
            else:
                values['owner_usrnbr'] = 0
            values['type'] = i.type
            values['status'] = i.status            
            values['text'] = i.text
            if i.trdnbr:
                if i.trdnbr.trdnbr:
                    values['trdnbr'] = i.trdnbr.trdnbr
                else:
                    values['trdnbr'] = i.trdnbr
            elif i.type == 'Stand Alone Payment':
                values['trdnbr'] = 0
                pr = 'Settlement %d is Stand Alone Payment (no trdnbr)' % (i.seqnbr) #todo
                log(2, pr)
            values['amount'] = i.amount
            if i.to_prfnbr:
                values['to_prfnbr'] = i.to_prfnbr.prfnbr
            if i.from_prfnbr:
                values['from_prfnbr'] = i.from_prfnbr.prfnbr
            values['curr'] = i.curr.insaddr
            values['value_day'] = i.value_day
            values['settle_category'] = i.settle_category
            values['acquirer_accname'] = i.acquirer_accname
            values['acquirer_account'] = i.acquirer_account
            values['party_accname'] = i.party_accname
            values['party_account'] = i.party_account
            values['acquirer_ptyid'] = i.acquirer_ptyid
            values['party_ptyid'] = i.party_ptyid
            values['settle_seqnbr'] = i.settle_seqnbr
            values['ref_seqnbr']   = i.ref_seqnbr
            values['ref_type'] = i.ref_type
            values['settleinstruction_seqnbr'] = i.settleinstruction_seqnbr
            values['netting_rule_seqnbr'] = i.netting_rule_seqnbr
            values['manual_match'] = i.manual_match
            values['post_settle_action'] = i.post_settle_action
            if i.cfwnbr:
                if i.cfwnbr.cfwnbr:
                    values['cfwnbr']          = i.cfwnbr.cfwnbr
            if i.dividend_seqnbr:
                if i.dividend_seqnbr.seqnbr:
                    values['dividend_seqnbr'] = i.dividend_seqnbr.seqnbr
            if i.paynbr:
                if i.paynbr.paynbr:
                    values['paynbr']          = i.paynbr.paynbr
            if i.sec_insaddr:
                if i.sec_insaddr.insaddr:
                    values['sec_insaddr']     = i.sec_insaddr
            values['status_explanation'] = i.status_explanation
            values['delivery_type']   = i.delivery_type
            values['org_sec_nom']   = i.org_sec_nom
            if param.network_update:
                values['party_account_network_name'] = i.party_account_network_name
                values['acquirer_account_network_name'] = i.acquirer_account_network_name
            pay = FSettlementGeneral3.Settlement(**values)
            if pay:
                l.append(pay)
    elif sel:
        pr = 'create_from_settle: input is not a list but %s' % (type(sel))
        log(2, pr)
    else:        
        log(2, 'create_from_settle: input is empty')        
    return l

# This function creates Settlement from Payment
# The last parameter says if the Settlement is created
# from a Payment from the database (1) or from a Payment object (0)

def payment_creation(setl, pay, status, seqnbr, trade, flag, correction_amount, input_str, append_trans = 1):
    
    if trade == None:
        if pay:
            if pay.trdnbr:
                trade = pay.trdnbr

    type = get_pay_type(pay)
    if type not in invalid_payment_types:
        setl.type         = type
        setl.status       = status              
        setl.trdnbr       = trade.trdnbr
        setl.paynbr       = pay.paynbr
        setl.settle_seqnbr = seqnbr #?
        FSettlementGeneral2.copy_protection_from_trade(setl, trade)
        if flag:
            setl.value_day    = pay.payday
            setl.curr         = pay.curr.insaddr
            if input_str == '':
                setl.amount       = FSettlementGeneral2.get_payment(trade, pay,\
                                                            correction_amount)
            else:
                setl.amount = 0.0
                index = input_str.find("=")+1
                input_str = input_str + ' This payment references a closed payment with paynbr ' + input_str[index:]
                setl.add_diary_note(input_str)
        else:
            setl.amount           = pay.amount
            setl.value_day        = pay.value_day
            setl.curr             = pay.curr
            setl.settle_category  = pay.settle_category
            setl.settle_seqnbr    = pay.settle_seqnbr
            setl.ref_seqnbr       = pay.ref_seqnbr
            setl.ref_type         = pay.ref_type
            setl.settleinstruction_seqnbr = pay.settleinstruction_seqnbr
            setl.netting_rule_seqnbr = pay.netting_rule_seqnbr
            setl.manual_match     = pay.manual_match
            setl.post_settle_action = pay.post_settle_action
                    
        if trade.prfnbr and setl.amount:
            if setl.amount > 0:
                setl.to_prfnbr = trade.prfnbr.prfnbr
            else:
                setl.from_prfnbr = trade.prfnbr.prfnbr

        # changes here must be refleted to FSettlementGeneralRT.create_setlObj
        if pay.accnbr:
            #party information is fetched from the payment entity
            setl.party_accname   = account_name(pay.accnbr.accnbr)
            setl.party_account   = account_account(pay.accnbr.accnbr)        
            setl.party_ptyid     = pay.accnbr.ptynbr.ptyid
        elif pay.ptynbr:
            # no account stated, party id is fetched via party nbr
            setl.party_ptyid     = pay.ptynbr.ptyid
            
        if pay.our_accnbr:
            #acquirer information is fetched from the payment entity
            setl.acquirer_accname = account_name(pay.our_accnbr.accnbr)
            setl.acquirer_account = account_account(pay.our_accnbr.accnbr)
            setl.acquirer_ptyid   = pay.our_accnbr.ptynbr.ptyid
        elif trade.acquirer_ptynbr:
            # no account stated, party id is fetched via trade
            setl.acquirer_ptyid   = trade.acquirer_ptynbr.ptyid
        
        ret = None
        if append_trans:
            append_transaction(setl)
            print_commit(setl)
        else:
            ret = setl
        return ret

def check_primary_issuance(trade, diff_dict = None):
    return FSettlementGeneral3.check_primary_issuance(trade, diff_dict)
    
def check_issuer_accounts(party):
    return FSettlementGeneral3.check_issuer_accounts(party)
    
def issuing_paying_agent(trade):
    return FSettlementGeneral3.issuing_paying_agent(trade)
    
def issuing_paying_agent_position(trade):
    return FSettlementGeneral3.issuing_paying_agent_position(trade)    

def get_cf_curr(cf, leg_c=None):
    return FSettlementGeneral3.get_cf_curr(cf, leg_c)
    
def has_coupon_generating_underlying_instrument(trade):
    return_value = False
    if trade.insaddr and trade.insaddr.instype in und_ins_security:
        underlying_instrument = trade.insaddr.und_insaddr
        if underlying_instrument:
            return_value = FSettlementGeneral2.coupon_ok(underlying_instrument)
    return return_value

def cf_creation(setl, cf, status, seqnbr, trade, flag, amount, insaddr, correction_amount=0, leg_c=None, cf_c=None, tr_c=None,\
append_trans = 1):
    '''tr_c may be ent_c but mostly trade'''
    setl.status = status
    cf2 = cf
    if not flag:
        cf2 = cf.cfwnbr # settlement actually
    cf_c = FSettlementGeneralRT.set_c(cf_c, cf2, 'CashFlow')
    tr_c = FSettlementGeneralRT.set_c(tr_c, trade, 'Trade')
    #When creating coupons type is already set, otherwise use cf type
    if setl.type=='None':
        if not FSettlementGeneral3.is_valid_cf_type(cf):    
            return
        setl.type = FSettlementGeneral3.get_cf_type(cf)    
    #If amount is set, this is a coupon and no trade should be set
    setl.trdnbr = trade.trdnbr
    
    if has_coupon_generating_underlying_instrument(trade):
        if is_coupon(trade, cf, trade, cf_c, None, trade.insaddr.und_insaddr) and \
           (setl.type == 'Coupon' or setl.type == 'Redemption'):
            setl.trdnbr = 0      
    else:
        if is_coupon(trade, cf, trade, cf_c, leg_c):
            setl.trdnbr = 0
    setl.settle_seqnbr = seqnbr #?
    setl.cfwnbr = cf.cfwnbr
    leg = cf.legnbr
    if leg_c:
        if leg_c.insaddr.insaddr == insaddr:
            leg = leg_c
        elif insaddr:
            pr = "cf_creation: Different instruments via leg:%d ins:%d (Error)" % (leg_c.insaddr.insaddr, insaddr)
            log(0, pr)
            leg_c = leg       
        
    FSettlementGeneral2.copy_protection_from_trade(setl, trade)
    if flag:
        if amount != 0:
            setl.amount = amount
            setl.sec_insaddr = insaddr 
        else:
            setl.amount = FSettlementGeneral2.get_cashflow(trade, cf,\
                                                            correction_amount)    
        setl.curr = get_cf_curr(cf, leg)
        setl.value_day = cf_c.pay_day
    else:
        setl.amount = cf.amount
        setl.curr = cf.curr
        setl.value_day = cf.value_day
        setl.settle_category = cf.settle_category
        setl.settle_seqnbr        = cf.settle_seqnbr
        setl.ref_seqnbr           = cf.ref_seqnbr
        setl.ref_type             = cf.ref_type
        setl.settleinstruction_seqnbr = cf.settleinstruction_seqnbr
        setl.netting_rule_seqnbr = cf.netting_rule_seqnbr
        setl.manual_match         = cf.manual_match
        setl.post_settle_action = cf.post_settle_action
        
    if trade.prfnbr:
        if setl.amount > 0:
            setl.to_prfnbr = trade.prfnbr.prfnbr
        else:
            setl.from_prfnbr = trade.prfnbr.prfnbr    

    setl.acquirer_ptyid = get_acquirer(trade)
    setl.party_ptyid = get_counterparty(tr_c, tr_c.insaddr, 1, 1)
    # following should be reflected to interest_accrued_creation
    ipa = issuing_paying_agent(tr_c)
    if ipa:
        setl.party_ptyid = ipa
    elif setl.type == 'Coupon' or setl.type == 'Redemption':
        ipa = issuing_paying_agent_position(tr_c)
        if ipa:
            setl.party_ptyid = ipa
            
    if not ipa:
        if insaddr:
            instr = ael.Instrument[insaddr]
            if instr and instr.issuer_ptynbr:
                # If the trade is a bond issuance, counterparty of coupon
                # settlements should be trade counterparty
                setl.party_ptyid = instr.issuer_ptynbr.ptyid
            elif instr and not instr.issuer_ptynbr and tr_c.counterparty_ptynbr:
                setl.party_ptyid = tr_c.counterparty_ptynbr.ptyid
        elif trade and (check_primary_issuance(tr_c) or \
                        setl.type == 'Coupon transfer'):
            if tr_c.counterparty_ptynbr:
                setl.party_ptyid = tr_c.counterparty_ptynbr.ptyid

    account_info(trade, setl, 0)
    ret = None
    if append_trans:
        append_transaction(setl)
        print_commit(setl)
    else:
        ret = setl
    return ret
    
    
def dividend_creation(setl, div, status, seqnbr, trade, flag, pos, tr_c=None, ins_c=None, append_trans = 1, comb_info = None):
    '''Changes here must be reflected in createObjDiv '''
    tr_c = FSettlementGeneralRT.set_c(tr_c, trade, 'Trade')
    setl.type         = 'Dividend'
    setl.status       = status
    setl.settle_seqnbr= seqnbr
    #contr_size = 1
    FSettlementGeneral2.copy_protection_from_trade(setl, tr_c)
    if flag:
        instr                = tr_c.insaddr
        if ins_c:
            instr = ins_c
        if instr:
            #contr_size = instr.contr_size            
            if instr.instype == 'EquitySwap':
                setl.trdnbr = tr_c.trdnbr
                setl.amount = FSettlementGeneral2.get_dividend(div, tr_c, instr, 0, comb_info)
            else:
                setl.sec_insaddr = instr.insaddr
                setl.amount = FSettlementGeneral2.get_dividend(div, tr_c, instr, pos)
                setl.trdnbr = 0 # common dividend via security instrument position
        setl.curr            = div.curr.insaddr
        setl.value_day       = div.pay_day
        setl.dividend_seqnbr = div.seqnbr
    else:
        setl.text            = div.text
        setl.amount          = div.amount
        setl.curr            = div.curr
        setl.value_day       = div.value_day
        setl.settle_category = div.settle_category
        setl.settle_seqnbr   = div.settle_seqnbr
        setl.ref_seqnbr      = div.ref_seqnbr
        setl.ref_type        = div.ref_type
        setl.settleinstruction_seqnbr = div.settleinstruction_seqnbr
        setl.netting_rule_seqnbr = div.netting_rule_seqnbr
        setl.manual_match    = div.manual_match
        setl.post_settle_action = div.post_settle_action
        setl.dividend_seqnbr = div.dividend_seqnbr
    
    if tr_c.prfnbr:
        if setl.amount > 0:
            setl.to_prfnbr = tr_c.prfnbr.prfnbr
        else:
            setl.from_prfnbr = tr_c.prfnbr.prfnbr 
    
    setl.acquirer_ptyid = get_acquirer(trade)
    setl.party_ptyid = get_counterparty(tr_c, instr, 1, 1)
    account_info(trade, setl, 0, tr_c)
    ret = None
    if append_trans:
        append_transaction(setl)
        print_commit(setl)
    else:
        ret = setl
    return setl

  
def void_trade_recall_setls(tr, oldTrStatus, combination_member=None):
    '''Function moved. Passing also forward param.'''
    FSettlementGeneral2.void_trade_recall_setls2(tr, oldTrStatus, combination_member)

def account_name(accnbr):   
    account_name=''
    if accnbr:
        acc = ael.Account[accnbr]
        if acc:
            account_name=acc.name
    return account_name
    
def account_account(accnbr):
    account_account=''
    if accnbr:
        acc = ael.Account[accnbr]
        if acc:
            account_account=acc.account
    return account_account
    
def get_pay_type(pay):
    return FSettlementGeneral3.get_pay_type(pay)
    
def calc_security_nominal(trade, comblink=None, corrected_setl=0, end_sec=0, ins_c=None):
    '''corrected_setl (already closed and payed out) affects the amount'''
    amount = 0

    if trade:
        combination_member = get_combination_member(comblink)
        ins = trade.insaddr
        if not ins_c:
            ins_c = ins
        instype = ''
        if not ins:
            return
        else:
            instype = ins.instype
        q = trade.quantity
        day = trade.acquire_day
        if end_sec:
            day = ins_c.exp_day
        if instype in ins_security:
            amount = ins.nominal_amount(day) * q

        elif instype in und_ins_security:
            if instype in ['Repo/Reverse', 'SecurityLoan']:
                amount = ins_c.ref_value * q
            else:
                amount = ins.nominal_amount(day) * q
        
        if combination_member and ins_has_security_nominal(combination_member):
            ins2 = trade.insaddr
            if ins_c and ins_c.insaddr == ins2:
                ins2 = ins_c
            weight = FSettlementGeneral2.get_instrument_combination_weight(combination_member, trade)
            amount = combination_member.nominal_amount(day) * weight * q
            if combination_member.instype in ['Repo/Reverse', 'SecurityLoan']:
                amount = (combination_member.ref_value) * weight * q

        if corrected_setl:
            amount = amount - corrected_setl
            
    return amount

def calc_end_security(trade, comblink=None, corrected_setl=0, ins_c=None):

    amount = calc_security_nominal(trade, comblink, corrected_setl, 1, ins_c)
    amount = 0 - amount
    return amount
    
def source_data(setl):
    'Source data is a settlement row created upon event in the database. The row\
    is later processed through the STP etc.'
    
    source_data=1

    if setl:    
        if (setl.ref_seqnbr and setl.ref_type=='Split Part'):
            source_data=0
        elif (setl.settle_category=='Adjusted' or \
              setl.settle_seqnbr or setl.netting_rule_seqnbr or \
              setl.ref_type=='Ad_hoc Net'):
            source_data=0
        #Added this since update rows has to reference a trade
        # but should not be treated as source data
        elif (setl.ref_seqnbr and setl.ref_type=='None'):
            source_data=0
    return source_data     

    
def log(level, s):
    '''Logs to the output. Log level is based on \
    FSettlementVariables.verbosity'''   
    if verbosity >= level: ael.log(s)


def check_adjusted_closed(settle):
    'Is the adjusted settlement closed? If yes, 0 is returned.'
    ok = 1
    try:
        sel = ael.Settlement.select('settle_seqnbr=%d' % settle.seqnbr)
    except:
        sel = []
    
    #there should be only one adjusted setlement
    for s in sel:
        if (s.status=='Closed'):
            ok = 0
            break # or use if (ok and s.status == 'Closed'):
    return ok
            
def check_status_closed(settle):

    closed = 0
    if settle.status == 'Closed':
        closed = 1
    elif check_adjusted_closed(settle) == 0:
        closed = 1
    elif settle.ref_seqnbr != 0 and settle.ref_type == 'Net Part':
        s = ael.Settlement[settle.ref_seqnbr.seqnbr]
        if s and s.status == 'Closed':
            closed = 1
        elif check_adjusted_closed(s) == 0:
            closed = 1
    elif settle.ref_type == 'Split':
        try:
            selection = ael.Settlement.select('ref_seqnbr =%d' % settle.seqnbr)
        except:
            selection = []
    
        for s in selection:
            if s.status == 'Closed':
                closed = 1
            elif check_adjusted_closed(s) == 0:
                closed = 1
    return closed            

def update_settle_and_references_cover(settle, enum_status):
    #This function is called from ael_update_settlement_reference
    #and before a list was returned from the ael function. Therefore
    #it is kept this way. FUNCTION_CALLED_FROM_PRIME do not touch!
    status=ael.enum_to_string('SettlementStatus', enum_status)
    s = None
    if settle:
        seqnbr=settle.seqnbr
        log(2, 'update_settle_and_references_cover (File)')
        s = FSettlementGeneral2.handle_recalled(seqnbr, 1)
    return [0, s]

def ins_has_security_nominal(ins):
    if (ins.instype in ins_security and ins.instype != 'FreeDefCF') or \
           ins.instype in und_ins_security:
        return 1
    else:
        return 0

def has_security_nominal(trade):
    return FSettlementGeneral3.has_security_nominal(trade)

def has_end_security(trade=None, instr=None):
    return FSettlementGeneral3.has_end_security(trade, instr)
    
def get_acquirer(trade):
    ptyid = ''
    if trade:
        if trade.acquirer_ptynbr:
            ptyid = trade.acquirer_ptynbr.ptyid
    else:
        log(1, 'get_acquirer: trade not deployed (File)')
    return ptyid

def get_counterparty(trade, ins_c=None, cp_mode=1, ipa_mode=0):
    return FSettlementGeneral3.get_counterparty(trade, ins_c, cp_mode, ipa_mode)
    
def enter_dividend(trade, div):
    ''' '''
    ok = 0
    if not trade:
        return 1
    if FSettlementGeneralRT.is_div(div):
        if trade.quantity != 0:
            if FSettlementGeneral2.is_eligible_for_dividend_creation(trade, div):
                ok = 1
            else:
                pr = "Trade %d is not eligible for dividend creation!" % trade.trdnbr
                log(3, pr)

    log(5, 'enter_dividend: %d' % (ok))
    return ok

def cf_from_und_insaddr(cf, instr):
    '''cf_c and ins_c ok '''
    if not instr.und_insaddr:
        return 0
    if cf.legnbr and cf.legnbr.insaddr:
        cf_insaddr=cf.legnbr.insaddr.insaddr
        if cf_insaddr==instr.und_insaddr.insaddr:
            return 1
    return 0

def enter_cashflow(trade, cf, cf_c=None, ins_c=None, leg_c=None):
    ''' This function requires both trade and cash flow as input. 
    Input trade and cf can be ent_c'''
    if not trade:
        log(1, 'enter_cashflow: 0, no Trade deployed as input (File)')
        return 0
    if not cf:
        log(1, 'enter_cashflow: 0, no CF deployed as input (File)')
        return 0
    if FSettlementGeneral2.cf_not_comb_member(trade, cf):
        return 0
    ok = 1
    cf_c = FSettlementGeneralRT.set_c(cf_c, cf, 'CashFlow')
    quantity = trade.quantity
    instr = trade.insaddr
    if ins_c:
        if instr.insaddr != ins_c.insaddr:
            log(0, "enter_cashflow: instruments differ via tr:%s ins_c:%s (Error)" % (instr.insid, ins_c.insid))
        instr = ins_c    
        
    leg = cf_c.legnbr
    if leg_c:
        leg = leg_c
    if trade.category == 'Collateral' and trade.connected_trdnbr:
        instr = trade.connected_trdnbr.insaddr
        if instr.exp_day <= cf.ex_coupon_date():
            return 0
    if instr and instr.instype in und_ins_security and \
       cf_from_und_insaddr(cf, instr):# instr may not be same as ins_c
        if instr.exp_day <= cf.ex_coupon_date():
            ok = 0
            pr = "Instrument exp_day before CF ex_coupon_date (%s <= %s)" % (str(instr.exp_day), str(cf.ex_coupon_date()))
            log(3, pr)
            log(3, 'enter_cashflow: 0')
            return ok
    if quantity != 0:
        pr3 = ""
        if not cf:
            return
        if cf.ex_coupon_date() <= trade.acquire_day:
            ok = 0
            pr3 = "CF ex_coupon_date before Trade acquire_day (%s <= %s)" % (str(cf.ex_coupon_date()), str(trade.acquire_day))            
        if not ok and cf_c.type=='Fixed Amount' and \
           leg.start_day == trade.acquire_day:
            ok = 1
        elif not ok:
            log(3, pr3)
            log(3, 'enter_cashflow: 0')
    if ok:
        ok = FSettlementGeneral3.create_cf_for_call_dep(cf_c, trade)
    return ok

def create_selection(unique_no, sel_type, trdnbr, sel, combination_member=None, append_trans = 1):
    '''Returns 0 if there is a settlement row in the settlement table that
    has got the same type (trade number for CashFlows and Dividends).
    Netting and splitting is not taken into concideration, all settlement 
    rows are treated equally. sel is a list with selected setttlements.
    See also FSettlementGeneral.get_setl_rows_ref'''
    
    does_not_exist = 1
    # Fixed Rate bellow used for interest accrued
    types = ['Security Nominal', 'Premium', 'Fee', 'End Security', 'Fixed Rate', 'Premium2']
      
    if sel_type=='CashFlow':
        if sel == None:
            try:
                sel = ael.Settlement.select('cfwnbr=%d' % unique_no)
            except:
                sel = []
                
        for s in sel:            
            if trdnbr and s.trdnbr and s.trdnbr.trdnbr == trdnbr:                
                does_not_exist = 0
                break            
    elif sel_type=='Payment':
        if sel == None:
            try:
                sel = ael.Settlement.select('paynbr=%d' % unique_no)
            except:
                sel = []
                
        if len(sel):
            does_not_exist = 0
    elif sel_type=='Dividend':
        if sel == None:
            try:
                sel = ael.Settlement.select('dividend_seqnbr=%d' % unique_no)
            except:
                sel = []

    elif sel_type in types:
        if sel == None:
            try:
                sel = ael.Settlement.select('trdnbr=%d' % unique_no)
            except:
                sel = []
                
        for r in sel: #combination kan have more then one
            if r.type == sel_type:
                does_not_exist = 0
                if combination_member and r.sec_insaddr != combination_member:
                    does_not_exist = 1
                if does_not_exist == 0:                    
                    break                
    else:
        pr = 'invalid input to create_selection, sel_type=%s  (File)' % (sel_type)
        log(1, pr)
    if not append_trans:
        does_not_exist = 1
    return does_not_exist

def find_account(links, curr, setl, obj_flag, delivery_obj, acquirer):
    ''' 
    links    -- trade_account_links for acquirer or counterparty/broker
    curr     -- currency of the settlement
    setl     -- settlement entity
    obj_flag -- not used
    delivery_obj -- delivery type
    acquirer -- type of the party, used for delivery type
    '''
    tal = None # matching trade_account_link
    accnbr = 0 # account number to be returned
    link_type = 'None' # tal/ssi type must match settlement type
    del_type = 'None' # delivery type
    DVS = 'Delivery versus Payment'
    who = '' # log message bellow

    for l in links:
        link_type = 'None'
        if setl.type in sec_types:
            if l.sec_settle_cf_type != 'None': 
                link_type = l.sec_settle_cf_type
            elif l.settle_seqnbr:
                if (l.settle_seqnbr.account_type in \
                    ['Security', 'Cash and Security']) or \
                    (l.settle_seqnbr.account_type=='None' and \
                     l.settle_seqnbr.settle_delivery_type==DVS):
                    link_type = l.settle_seqnbr.sec_settle_cf_type
        
        else:
            if l.settle_cf_type != 'None':            
                link_type = l.settle_cf_type     
            elif l.settle_seqnbr:
                if (l.settle_seqnbr.account_type in \
                    ['Cash', 'Cash and Security']) or \
                    (l.settle_seqnbr.account_type=='None' and \
                     l.settle_seqnbr.settle_delivery_type==DVS):
                    link_type = l.settle_seqnbr.settle_cf_type

        if setl.type == link_type and (l.curr == None or l.curr == curr):
            tal = l                   
            break # bingo! TAL found

    if acquirer:
        who = 'acquirer'
    else:
        who = 'counterparty'

            
    if tal == None:    
        pr = "find_account: %s %s TALs but no match for %s setl:%d (File)" % (len(links), who, setl.type, setl.seqnbr)
        log(1, pr)            
    else:
        if tal.settle_delivery_type not in ['None', '', ' ']:
            del_type = tal.settle_delivery_type
            if tal.settle_seqnbr:
                candidate = tal.settle_seqnbr.settle_delivery_type
                if candidate != del_type:
                    if candidate not in ['None', '', ' ']:
                        pr = "find_account: delivery types differ! TAL=%s vs %s=SSI (File)" % (del_type, candidate)
                        log(1, pr)
                        del_type = candidate
                        pr = "delivery type from SSI %s will be used for settlement %d (File)" % (candidate, setl.seqnbr)
                        log(1, pr)
        elif tal.settle_seqnbr:            
            if tal.settle_seqnbr.settle_delivery_type not in ['None', '', ' ']:
                del_type = tal.settle_seqnbr.settle_delivery_type
              
        if acquirer:
            delivery_obj.acq_type = del_type
        else:
            delivery_obj.counter_type = del_type
            
        if tal.settle_seqnbr:
            value_day = setl.value_day 
            if setl.type in sec_types:
                a = tal.settle_seqnbr.get_account(value_day, 0)
                if a:
                    accnbr = a.accnbr
            else:
                a = tal.settle_seqnbr.get_account(value_day, 1)
                if a:
                    accnbr = a.accnbr
        elif tal.accnbr: 
            accnbr = tal.accnbr.accnbr
        elif tal.sec_accnbr:
            accnbr = tal.sec_accnbr.accnbr
        else:
            pr = "find_account: %s TALs but no %s account found for %s setlement %d (File)" % (len(links), who, setl.type, setl.seqnbr)
            log(1, pr)            
    
    return accnbr
    
def get_ptyid_from_account(accnbr):
    
    returned_ptyid = ''
    account = ael.Account[accnbr]
    if account:
        returned_ptyid = account.ptynbr.ptyid
    return returned_ptyid

def get_network_for_account(account):
    returned_name = ''
    nat = account.network_alias_type
    if nat:
        returned_name = nat.alias_type_name
    return returned_name
    
def set_account(setl, links, acquirer, obj_flag, delivery_obj):
    noa = "no account will be set"
    if not setl.curr:
        pr = "set_account: settlement %d does not have currency, %s (File)" % (setl.seqnbr, noa)
        log(1, pr)            
        return
    if not setl.type:    
        pr = "set_account: settlement %d does not have type, %s (File)" % (setl.seqnbr, noa)
        log(1, pr)            
        return
        
    if obj_flag and ael.Instrument[setl.curr]:
        curr = ael.Instrument[setl.curr]
    else:
        curr = setl.curr


    accnbr = find_account(links, curr, setl, obj_flag, delivery_obj, acquirer)

    if acquirer:
        if accnbr:
            setl.acquirer_account = account_account(accnbr)
            setl.acquirer_accname = account_name(accnbr)
            setl.acquirer_ptyid = get_ptyid_from_account(accnbr)
            account = ael.Account[accnbr]
            if param.network_update:
                if account:
                    setl.acquirer_account_network_name = get_network_for_account(account)
                else:
                    setl.acquirer_account_network_name = ''
        else:
            setl.acquirer_account = ''
            setl.acquirer_accname = ''
            if param.network_update:
                setl.acquirer_account_network_name = ''
    else:
        if accnbr:
            setl.party_account=account_account(accnbr)
            setl.party_accname=account_name(accnbr)
            setl.party_ptyid = get_ptyid_from_account(accnbr)
            account = ael.Account[accnbr]
            if param.network_update:
                if account:
                    setl.party_account_network_name = get_network_for_account(account)
                else:
                    setl.party_account_network_name = ''
        else:
            setl.party_account = ''
            setl.party_accname = ''
            if param.network_update:
                setl.party_account_network_name = ''

def account_info(trade, setl, obj_flag, tr_c=None):
    ''' 
    Sets settlement account info for acquirer and counterparty.
    Set also delivery type of the settlement. 
    When used obj_flag means that settlement class is used.
    See also set_account and find_account.
    adapt to trade to ent_c!!!
    '''

    if not trade or not setl:
        return

    instr = None
    instype = None
    if setl.trdnbr:
        if obj_flag:
            trade = ael.Trade[setl.trdnbr]
            instr = trade.insaddr
        else:
            instr = setl.trdnbr.insaddr
    elif setl.sec_insaddr:
        instr = setl.sec_insaddr
    if instr:
        instype=instr.instype
    
    issuer = None
    if instr and instr.issuer_ptynbr:
        issuer = instr.issuer_ptynbr
    # uggly    
    if setl.type=='Fee':
        cp_type = 'Broker'
    elif issuing_paying_agent(trade):
        cp_type = 'Counterparty'
    elif setl.type == 'Coupon' or setl.type == 'Redemption':
        if issuing_paying_agent_position(trade):
            cp_type = 'Counterparty'
        else:
            cp_type = 'Issuer'
    elif instype == 'FRN' and setl.type == 'Float Rate' and \
         not check_primary_issuance(trade) and check_issuer_accounts(issuer):
        cp_type = 'Issuer'
    else:
        cp_type = 'Counterparty'

    acq_links = []
    party_links = []
    links = get_tals(setl, trade)    
    for l in links:
        if l.party_type == 'Intern Dept':
            acq_links.append(l)
        elif l.party_type == cp_type:
            # cp of type counterparty, broker and issuer
            party_links.append(l)
    
    del_obj = DeliveryType()
    # Set acquirer account for all type of settlements
    set_account(setl, acq_links, 1, obj_flag, del_obj)

    # Set party accounts, for settlements where party is
    # issuer, no account information should be set
    if instype in issuer_list:
        if not setl.cfwnbr or setl.type=='Coupon transfer' \
               or cp_type == 'Issuer' or check_primary_issuance(trade) \
               or issuing_paying_agent_position(trade):
            set_account(setl, party_links, 0, obj_flag, del_obj)
    elif instype=='Stock':
        if not setl.dividend_seqnbr:
            set_account(setl, party_links, 0, obj_flag, del_obj)
    else:        
        set_account(setl, party_links, 0, obj_flag, del_obj)

    del_type = 'None'
    if del_obj.acq_type==del_obj.counter_type:
        del_type = del_obj.acq_type
    else:
        del_type = 'Delivery Free of Payment'
        
    if obj_flag:
        setl['delivery_type'] = del_type
    else:
        setl.delivery_type = del_type
    
    
def is_valid_instrument(instrument):
    return FSettlementGeneral3.is_valid_instrument(instrument)

def is_coupon(trade, cf, tr_c=None, cf_c=None, leg_c=None, underlying_instrument = None):
    return FSettlementGeneral3.is_coupon(trade, cf, tr_c, cf_c, leg_c, underlying_instrument)
                        
def clear_status_explanation(settle):
    FSettlementGeneral3.clear_status_explanation(settle)
    
def is_collateral_trade(trade):
    collateral = 0
    if not trade:
        return collateral
    if trade.category=='Collateral':
        collateral = 1
    return collateral

def get_tals(setl,trade=None):
    return FSettlementGeneral3.get_tals(setl, trade)
    
def get_all_comb_instruments(comb_link, comb_link_dictionary):
    """
    Finds all combinations that comb_link.member_insaddr is part of or combinations with combinations
    that comb_link.member_insaddr is part of. No restrictions on combination depth.
    Sets comb_link_dictionary with all the combination links part of the 'combination trees' 
    """
    if not comb_link_dictionary.has_key(comb_link.seqnbr):
            comb_link_dictionary[comb_link.seqnbr] = comb_link
            
    comb_links = ael.CombinationLink.select('member_insaddr=%d' % comb_link.owner_insaddr.insaddr)
    for cbl in comb_links:
        get_all_comb_instruments(cbl, comb_link_dictionary)
    
    
def get_comb_instruments(instr):
    ''''Returns list with combination links where the instrument is a member.    
    instr can be ins_c'''
    if not instr:
        return None
    #no comb_synch needed bellow
    sel = ael.CombinationLink.select('member_insaddr=%d' % instr.insaddr)
    
    comb_link_dictionary = {}    
    for comb_link in sel:
        get_all_comb_instruments(comb_link, comb_link_dictionary)
    
    return comb_link_dictionary.values()

def get_combination_member(comblink):
    '''Returns member instrument from the combinationlink.'''
    if comblink and comblink.member_insaddr:
        return comblink.member_insaddr
    else:
        return None

def get_coupons(instrument):    
    return FSettlementGeneral3.get_coupons(instrument)

def setl_diff(setl1, setl2, result_dict={}, exclude_cols=[]):
    return FSettlementGeneral3.setl_diff(setl1, setl2, result_dict, exclude_cols)

def print_trans(d, d_name):
    log(0, "%s includes:" % (d_name))
    for k, v in d.items():
        print v.pp()
        
def get_version_entity(mode=0):
    '''Get the name of the entity expiriencing version diff.'''
    ret = ''
    if mode in range(0, len(versions)):
        ret =  versions[mode]
    return ret

def print_set_c(entity_type, record_type):
    '''Returns 1 if it is rellevant to print set_c version diff.'''
    ret = 0
    if entity_type == 'Trade' and record_type in ['Trade', 'Payment']:
        ret = 1
    elif entity_type == 'Instrument' and record_type in ['Instrument', 'CashFlow', 'CombinationLink', 'Dividend', 'Leg', 'Reset']:
        ret = 1
    elif entity_type == 'Party' and record_type in ['Account', 'Party']:
        ret = 1
    elif entity_type == 'Settlement' and record_type in ['Settlement']:
        ret = 1
    return ret
    
def get_previous_function_from_stack():
    import inspect
    stack = inspect.stack()
    frame = stack[2]
    log(1, 'function %s' % frame[3])
    args = inspect.getargvalues(frame[0])[3]
    log(1, 'Input parameters:')
    for (arg, value) in args.items():
        print arg, '=', value
        
def get_all_function_calls():
    import inspect
    stack = inspect.stack()
    for frame in stack:
        log(1, 'FUNCTION: %s LINE: %d' % (frame[3], frame[2]))

def settle_exists(trade):
    ret = None
    try:
        payouts = []
        selection = ael.Settlement.select('trdnbr = %d' % trade.trdnbr)
        if len(selection):
            for s in selection:
                if s.type == 'Payout':
                    payouts.append(s)
            if len(payouts):
                if len(payouts) > 1:
                    for s in payouts:
                        if s.ref_seqnbr:
                            ret = s
                            break
                else:
                    ret =  payouts[0]
    except RuntimeError, e:
        log(1, 'Error in settle_exists! Cause: %s' % e)
    return ret
    
def is_prevent_settlement_processing_for_trade(trade):
    prevent = False
    party = trade.counterparty_ptynbr
    prevent = is_prevent_settlement_processing_for_party(party)
    if not prevent:
        party = trade.acquirer_ptynbr
        prevent = is_prevent_settlement_processing_for_party(party)
    if not prevent:
        prevent = is_no_settlement_trade(trade)
    return prevent

def is_prevent_settlement_processing_for_party(party):
    prevent = False
    if party:
        for info in party.additional_infos():
            spec = info.addinf_specnbr
            name = spec.field_name
            if name == 'No Settlements' and info.value == 'Yes':
                prevent = True            
    if prevent:
        log(1, 'Settlement processing for party %s is prevented' % party.ptyid)
        log(1, 'Check additional info No Settlements for party %s' % party.ptyid)
    return prevent
    
def is_no_settlement_trade(trade):
    prevent = False
    if trade:
        for info in trade.additional_infos():
            spec = info.addinf_specnbr
            name = spec.field_name
            if name == 'No Settlement Trade' and info.value == 'Yes':
                prevent = True            
    if prevent:
        log(1, 'Settlement processing for trade %d is prevented' % trade.trdnbr)
        log(1, 'Check additional info No Settlement Trade for trade %d' % trade.trdnbr)
    return prevent

def is_prevent_cash_flow(ael_cash_flow):
    global param
    prevent = False
    for (field_name, field_value) in param.cash_flow_additional_infos:
        if is_additional_info_set(ael_cash_flow, field_name, field_value) == True:
            prevent = True
            log(5, 'Preventing settlement processing for cash flow %d' % ael_cash_flow.cfwnbr) 
            break
    return prevent
        
def is_additional_info_set(ael_record, field_name, field_value):
    info_is_set = False
    for info in ael_record.additional_infos():
        if type(info.value) == str:
            spec = info.addinf_specnbr
            spec_field_name = spec.field_name
            if spec_field_name == field_name and info.value == field_value:
                info_is_set = True
                break
    return info_is_set


def is_excluded_acq_trade(tr_c):
    global param
    trd_acq = None
    ret = False
    log_str = 'Acquirer %s is excluded from settlement creation! \n'\
            'See FSettlementVariables.exclude_acq and \nFSettlementVariables.invert_exclude_acq.\n'\
            'Settlement records for trade %d will not be created.'
    try:
        trd_acq = tr_c.acquirer_ptynbr.ptyid
    except Exception, e:
        log(3, 'Acquirer not found for trade %d. Cause: %s' % (tr_c.trdnbr, e))
    if not param.invert_exclude_acq:
        if trd_acq and trd_acq in param.exclude_acq:
            log(1, log_str % (trd_acq, tr_c.trdnbr))
            ret = True
    else:
        if trd_acq and trd_acq not in param.exclude_acq:
            log(1, log_str % (trd_acq, tr_c.trdnbr))
            ret = True
    return ret
    
def is_excluded_portfolio_trade(tr_c):
    global param
    prfid = None
    ret = False
    log_str = 'Portfolio %s is excluded from settlement creation! \n'\
            'See FSettlementVariables.exclude_portfolio and \nFSettlementVariables.invert_exclude_portfolio.\n'\
            'Settlement records for trade %d will not be created.\n'
    try:
        prfid = tr_c.prfnbr.prfid
    except Exception, e:
        log(3, 'Portfolio not found for trade %d. Cause: %s' % (tr_c.trdnbr, e))
    if not param.invert_exclude_portfolio:
        if prfid and prfid in param.exclude_portfolio:
            log(1, log_str % (prfid, tr_c.trdnbr))
            ret = True
    else:
        if prfid and prfid not in param.exclude_portfolio:
            log(1, log_str % (prfid, tr_c.trdnbr))
            ret = True
    return ret


def get_net_children_wrapper(parent):
    global net_dict
    return FSettlementNetting.get_net_children(net_dict, parent)

