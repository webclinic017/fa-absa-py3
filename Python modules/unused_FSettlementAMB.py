""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementAMB - Module that subscribes on AMB-messages.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module subscribes on AMB-messages that reflect database changes on 
    entities such as trade, cashflow, payment, account, dividend, reset, 
    party, settlement, settle instruction, instrument and netting rule. 
    Based on these database changes the Settlement table is updated.
    Netting, splitting is done as well. This module is run by ATS (single mode)    
----------------------------------------------------------------------------"""

import amb
import ael
import time
import os
import FSettlementVariables
import FSettlementGeneralRT, FSettlementGeneral, FSettlementSTP
import FSettlementParams, FSettlementGeneral2, FSettlementGeneral3

# FOLLOWING VARIABLES MUST BE CONFIGURED IN FSETTLEMENTVARIABLES

# Arena Message Broker, server:port
amb_login = FSettlementVariables.amb_login 

# Print AMBA messages or not, 1 means print
print_mode = FSettlementVariables.print_mode 

# ATS_SINGLE_PROD is receiver and therefore
# this name must be added to the system table in the AMB database
RECEIVER_MB_NAME = FSettlementVariables.RECEIVER_MB_NAME 

# Equal to the value of -sender_source configured in the amba.ini file
RECEIVER_SOURCE = FSettlementVariables.RECEIVER_SOURCE 

# Exclude settlement creation for trades with the following acquirers

global amb_mes_nbr
global version_not_ok
version_not_ok = 0
reader = None
param = None
# contains sender source entities (message subjects), see function createSenderSources
valid_entities = ['TRADE', 'INSTRUMENT', 'DIVIDEND', 'PAYMENT', 'CASHFLOW', 'LEG', 'PARTY',\
                  'ACCOUNT', 'NETTINGRULE', 'SETTLEINSTRUCTION', 'SETTLEMENT', 'RESET']

events = ['INSERT', 'UPDATE', 'DELETE']
prefixs = {'UPDATE':'!','INSERT':'+','DELETE':'-'}
prefixs_inv = {'!':'UPDATE','+':'INSERT','-':'DELETE'}
prefix_ok = FSettlementGeneral3.prefix_ok
# Following lists are used when parsing AMB-messages
accS = ['!ACCOUNT', '-ACCOUNT'] # +ACCOUNT is irrelevant
divS = ['+DIVIDEND', '!DIVIDEND', '-DIVIDEND', 'DIVIDEND']
cfS = ['+CASHFLOW', '!CASHFLOW', '-CASHFLOW', 'CASHFLOW'] #CASHFLOW needed for RESETS
nrS = ['+NETTINGRULE', '!NETTINGRULE', '-NETTINGRULE']
payS = ['+PAYMENT', '!PAYMENT', '-PAYMENT', 'PAYMENT']
partyS = ['!PARTY', '-PARTY']
resetS = ['+RESET', '!RESET', '-RESET']
setlS = ['+SETTLEMENT', '!SETTLEMENT', '-SETTLEMENT']
ssiS = ['+SETTLEINSTRUCTION', '!SETTLEINSTRUCTION', '-SETTLEINSTRUCTION']
talS = ['+TRADEACCOUNTLINK', '!TRADEACCOUNTLINK', '-TRADEACCOUNTLINK']
addS = ['+ADDITIONALINFO', '!ADDITIONALINFO', '-ADDITIONALINFO']
combS = ['+COMBINATIONLINK', '!COMBINATIONLINK', '-COMBINATIONLINK', 'COMBINATIONLINK']
corr_banks = ['CORRESPONDENT_BANK_PTYNBR', 'CORRESPONDENT_BANK2_PTYNBR',
              'CORRESPONDENT_BANK3_PTYNBR', 'CORRESPONDENT_BANK4_PTYNBR',
              'CORRESPONDENT_BANK5_PTYNBR']
accounts = ['ACCOUNT2', 'ACCOUNT3', 'ACCOUNT4', 'ACCOUNT5']

# changes in these field leed to update of all settlements connected to this trade
acc_fields      = FSettlementGeneral3.acc_fields
cf_fields       = FSettlementGeneral3.cf_fields   
div_fields      = FSettlementGeneral3.div_fields 
ins_fields      = FSettlementGeneral3.ins_fields 
leg_fields      = FSettlementGeneral3.leg_fields 
nr_fields       = FSettlementGeneral3.nr_fields 
pay_fields      = FSettlementGeneral3.pay_fields 
party_fields    = FSettlementGeneral3.party_fields 
reset_fields    = FSettlementGeneral3.reset_fields
setl_fields     = FSettlementGeneral3.setl_fields
tr_fields       = FSettlementGeneral3.tr_fields

# List with status concidered per event on entity
# better to use invertion of FSettlementGeneral.keep_status
setl_status_update = ['Exception', 'Manual Match', 'Authorised']#concider postsetlement as well

# Variables for dictionary event would be treated N=New, U=Update, E=Empty, D=Delete
EV_NUED = 1
EV_NUE  = 2
EV_NU   = 3
EV_UD  = 4

class Timer(object):
    def __init__(self, secondsUntilExpiry):
        self.__secondsUntilExpiry = secondsUntilExpiry
        self.__startTime = 0

    def __CurrentTime(self):
        return time.time()

    def Start(self):
        self.__startTime = self.__CurrentTime()

    def Stop(self):
        self.__startTime = 0

    def HasExpired(self):
        return self.GetElapsedTimeInSeconds() >= self.__secondsUntilExpiry

    def IsRunning(self):
        return self.__startTime > 0

    def GetElapsedTimeInSeconds(self):
        return self.__CurrentTime() - self.__startTime

# The pauseWorkCallback variable is used to allow the event_cb some time to wait 
# for related events after an instrument update event before work_cb kicks in.
# This was done to solve SPR 286116: Double fixed amount settlements are created on a 
# Call Deposits in some rare cases.
SECONDS_UNTIL_EXPIRY = 2.0
pauseWorkCallback = None

def get_dict_from_MBF(mbfObj, objStr, emptyMode=EV_NUE):
    '''Returns a dictionary containing AMB instrument objects (objStr). The values of the 
    dictionary keys can be +,!,- or the string empty. Unchanged object will be
    taken in to the concideration based on emptyMode flag.'''
    if emptyMode == EV_NUE: #default, recall functionality is not handled by the scripts
        e_dict = {'+':[], '!':[], 'empty':[]}
    elif emptyMode == EV_NU:
        e_dict = {'+':[], '!':[]}
    elif emptyMode == EV_UD:
        e_dict = {'!':[], '-':[]} #used for account
    elif emptyMode == EV_NUED: # probbably never needed, combinationlink?
        e_dict = {'+':[], '!':[], 'empty':[], '-':[]}

    if mbfObj:
        for prx in e_dict.keys():
            if prx == 'empty':
                mbfName = objStr #CASHFLOW
            else:
                mbfName = prx+objStr #!CASHFLOW
            obj = mbfObj.mbf_find_object(mbfName) #CASHFLOW_MBFOBJ
            while obj:
                if obj.mbf_get_name() == mbfName:
                    if obj not in e_dict[prx]:
                        e_dict[prx].append(obj)
                obj = mbfObj.mbf_next_object()
    return e_dict


def get_entity(tp_val):
    'Returns the string presentation of the entity. \
    ie TRADE from INSERT_TRADE. Empty string is returned \
    if incorrect input is deployed.'
    entity = ''
    pos = tp_val.find('_')
    if pos and pos != -1:
        entity = tp_val[pos+1:]
    return entity


def get_event(mbf_type):
    'Returns the string presentation of the event, ie INSERT'
    ev = '' #string presentation of Event
    for evt in events:
        if mbf_type.find(evt) != -1 and ev == '':
            ev = evt            
    return ev


def get_event_prefix(ev, entityStr):
    'Returns +,-,! or empty string, i.e. UPDATE,INSTRUMENT gives !INSTRUMENT'
    ret = ''
    
    if ev and ev in prefixs.keys():
        if entityStr != '' and entityStr in valid_entities:
            ret = '%s%s' % (prefixs[ev], entityStr)
        else:
            pr = 'get_event_prefix: wrong entityString %s' & (entityStr)
            log(1, pr)
    else:
        pr = 'get_event_prefix:ev not in prefixs ev: %s' % (ev)
        log(1, pr)
    return ret

           
def get_prefix(entObj):
    'Returns !, +, - or empty string, i.e. +DIVIDEND gives +'    
    prx2 = ''
    if entObj:
        prx = entObj.mbf_get_name()
    else:
        log(2, 'get_prefix: the intput is not an Object')

    if prx != '' and prx[0] in prefixs.values():
        prx2= prx[0]
    elif prx not in prefix_ok:
        #INSTRUMENT with cash flows is OK
        pr = 'get_prefix: empty string returned for %s' % (prx)
        log(1, pr)
        
    return prx2


def get_sub_entity(mes, entStr, mode):
    'A function used only for the AMB messages of the type EVENT_ENTITY.\
    Do not use this function on LEGs and simmilar entities that have \
    inner entities/object.'
    tp_val = get_type(mes)    
    if tp_val != '':
        ev = get_event(tp_val)
        entity = get_entity(tp_val)
    else:
        entity = None
        ev = ''        
        
    if entity:
        if entity == entStr:        
            if ev == 'UPDATE':
                if mode != None and mode == 1:
                    entStr = '!'+entStr            
            elif ev == 'INSERT':
                entStr = '+'+entStr
            elif ev == 'DELETE':
                entStr = '-'+entStr                        
    return mes.mbf_find_object(entStr)


def get_type(mes):
    'Returns the value of the TYPE=UPDATE_TRADE'
    tp_val = ''
    if mes:
        tp = mes.mbf_find_object('TYPE')
        if tp:
            tp_val = tp.mbf_get_value()        
    return tp_val

            
def parseEntitytoDict(mbfObj, entlist, entStr, entId):
    '''Returns a dictionary with entities that have been added or changed. Note that
    enitities such LEG will not be concidered by parseEntitytoDict, see get_dict_from_MBF!
    Note event delete is not needed any more (only for entites in delete_support).'''
    e_dict = {'+':[], '!':[]}
    delete_support = ['ADDITIONALINFO']#'COMBINATIONLINK',
    if entStr in delete_support:
        e_dict = {'+':[], '!':[], '-':[]}
        
    if mbfObj:
        for ent in entlist:            
            obj = mbfObj.mbf_find_object(ent)            
            while obj != None:
                id = None                
                pfx = get_prefix(obj)
                if e_dict.has_key(pfx) and obj.mbf_get_name() == ent:
                    if obj not in e_dict[pfx]:                    
                        e_dict[pfx].append(obj)                                
                obj = mbfObj.mbf_next_object()                                        
    return e_dict


def get_ins_from_amb(instObj):
    ''' Get ael instrument entity from amba message for Instrument'''
    instrument = None
    if instObj:
        mbf_inst = instObj.mbf_find_object('INSADDR')
        if mbf_inst:                
            instrument = ael.Instrument[int(mbf_inst.mbf_get_value())]
    return instrument
    

def set_dict_values(cf, input_dict, tr):
    '''See also FSettlementGeneralRT.createObjCf'''
    input_dict['value_day2'] = (cf.pay_day).to_string()
    input_dict['curr.insid'] = cf.legnbr.curr.insaddr
    if tr:
        input_dict['quantity'] = tr.quantity



def parseInstrEntity(instObj, ev):
    'Function that takes care of all objects in the Instrument mbfObject'
    instrument = None
    div = None
    notFound = 1
    hasTrade = 0 # nothing is done if the instrument does not have trade
    hasCoupons = 0 # need coupons of the instrument be updated?
    prohibited_events = ['-', '+'] #update or empty_string should be checked
    coupons = []
    cfs = []
    SN = 'Security Nominal'
    leg_dict = {}
    ins_c = None
    
    global version_not_ok
    if instObj:
        mbf_inst = instObj.mbf_find_object('INSADDR')
        if mbf_inst:
            notFound = 0
            if ev and ev == '-':
                return notFound
                
            instrument = ael.Instrument[int(mbf_inst.mbf_get_value())]
            version_not_ok = FSettlementGeneral3.version_not_ok(instObj, instrument, ev, 2)
            leg_dict = get_dict_from_MBF(instObj, 'LEG')
            
            ins_c = instrument
            if instrument and ev:                
                ins_c = FSettlementGeneral3.get_entity_class(instObj, ins_fields, instrument, 'Instrument')
                if FSettlementGeneral.is_valid_instrument(ins_c):                
                    trades = FSettlementGeneral2.get_trades(instrument)
                    for tr in trades:
                        if tr.insaddr.instype in FSettlementGeneral.und_ins_security:
                            # no ins_c here might be combination
                            couponList = FSettlementGeneralRT.coupons_from_tr(tr, tr.insaddr.und_insaddr) 
                        elif tr.insaddr == instrument.insaddr:
                            couponList = FSettlementGeneralRT.coupons_from_tr(tr, instrument, ins_c, leg_dict)
                        else:
                            couponList = FSettlementGeneralRT.coupons_from_tr(tr, tr.insaddr)
                        for coupon in couponList:
                            if not coupon in coupons:
                                coupons.append(coupon)
                    if len(trades):
                        hasTrade = 1
                    if len(coupons):
                        hasCoupons = 1
                else:
                    pr = '%s is not valid instrument type, no action on instrument %s' % (ins_c.instype, ins_c.insid)
                    log(1, pr)
                    return 

            #parse INSTRUMENT and see if updates are needed, use ins_c where possible
            if hasTrade or hasCoupons:                                
                sz = None
                contr_size = instObj.mbf_find_object('!CONTR_SIZE')
                iss = instObj.mbf_find_object('!ISSUER_PTYNBR')
                iss_name = instObj.mbf_find_object('!ISSUER_PTYNBR.PTYID')
                ref_value = instObj.mbf_find_object('!REF_VALUE')
                exp_value = instObj.mbf_find_object('!EXP_DAY')
                und_ins = instObj.mbf_find_object('!UND_INSADDR')
                exp_coup_period = instObj.mbf_find_object('!EX_COUP_PERIOD')
                index_factor = instObj.mbf_find_object('!INDEX_FACTOR')
                open_end = instObj.mbf_find_object('!OPEN_END')
                input_dict = {}
                if open_end and ins_c.instype == 'Deposit':
          
                    oen = instObj.mbf_find_object('OPEN_END')
                    oeo = instObj.mbf_find_object('!OPEN_END')
            
                    if oen and oeo:
                        open_end_new = oen.mbf_get_value()
                        open_end_old = oeo.mbf_get_value()
                        if open_end_old == 'Open End' and open_end_new == 'Terminated':
                            for tr in trades:
                                if not FSettlementGeneral.is_collateral_trade(tr):
                                    for cf in FSettlementGeneralRT.cfs_from_tr(tr, tr, ins_c, leg_dict):
                                        cf_ent = ael.CashFlow[cf.cfwnbr]                                        
                                        FSettlementGeneralRT.create_cf(cf_ent, tr, 'New', 0, cf, tr, cf.legnbr, ins_c)
                                   
                # Reflect here if underlying for repo trades has changed 
                if und_ins:
                    insaddr_new = int(instObj.mbf_find_object('UND_INSADDR').mbf_get_value())
                    undins_new = ael.Instrument[insaddr_new]
                    if undins_new:
                        input_dict['sec_insaddr'] = undins_new.insaddr
                        input_dict['quantity'] = 1 #?
                        input_dict['org_sec_nom'] = 1
                    
                if contr_size:
                    #RuntimeError: selection from temporary entity
                    cznew = instObj.mbf_find_object('CONTR_SIZE').mbf_get_value()
                    czold = contr_size.mbf_get_value()
                    pr = 'Instrument %s, contract size %s --> %s' % (ins_c.insid, czold, cznew)
                    log(1, pr)
                    input_dict['contr_size'] = 'sz' #?

                if iss:
                    new_iss = ''
                    if instObj.mbf_find_object('ISSUER_PTYNBR'):
                        new_iss = instObj.mbf_find_object('ISSUER_PTYNBR').mbf_get_value()
                    old_iss = iss.mbf_get_value()
                    pr = 'Instrument %s, issuer_ptynbr %s --> %s' % (ins_c.insid, old_iss, new_iss)
                    log(1, pr)
                    input_dict['issuer_ptynbr'] = new_iss

                if iss_name:
                    new_iss = ''
                    if instObj.mbf_find_object('ISSUER_PTYNBR.PTYID'):
                        new_iss = instObj.mbf_find_object('ISSUER_PTYNBR.PTYID').mbf_get_value()
                    old_iss = iss_name.mbf_get_value()
                    pr = 'Instrument %s, issuer name %s --> %s' % (ins_c.insid, old_iss, new_iss)
                    log(1, pr)
                    input_dict['issuer_ptynbr.ptyid'] = new_iss

                if ref_value:
                    new_ref = ''
                    if instObj.mbf_find_object('REF_VALUE'):
                        new_ref = instObj.mbf_find_object('REF_VALUE').mbf_get_value()
                    old_ref = ref_value.mbf_get_value()
                    pr = 'Instrument %s, ref value %s --> %s' % \
                         (ins_c.insid, old_ref, new_ref)
                    log(1, pr)
                    input_dict['org_sec_nom'] = new_ref

                if exp_value:                    
                    input_dict['exp_day'] = \
                                str(instObj.mbf_find_object('EXP_DAY').mbf_get_value())                

                if exp_coup_period:
                    input_dict['exp_coup_period'] = 'exp_coup_period'

                if index_factor:
                    input_dict['index_factor'] = 'index_factor'

                if contr_size or iss or iss_name or ref_value or exp_value or exp_coup_period or index_factor:
                    if hasTrade:
                        for tr in trades:
                            FSettlementGeneralRT.update_premium(tr, input_dict, 'Premium')
                            if tr.fee:
                                FSettlementGeneralRT.update_premium(tr, input_dict, 'Fee')
                            FSettlementGeneral2.validate(tr, 'UPDATE', tr, ins_c)
                            
                            for cf in FSettlementGeneralRT.cfs_from_tr(tr, tr, ins_c, leg_dict):
                                set_dict_values(cf, input_dict, tr)#akta
                                cfs.append(cf.cfwnbr)
                                cf_ent = ael.CashFlow[cf.cfwnbr]                                
                                FSettlementGeneralRT.update_cf(cf_ent, input_dict, tr, None, tr, ins_c, None, cf)
                    if hasCoupons:
                        for c in coupons:
                            set_dict_values(c, input_dict, None)#akta
                            cfs.append(c.cfwnbr)                     
                            cf_ent = ael.CashFlow[c.cfwnbr]                                
                            FSettlementGeneralRT.update_cf(cf_ent, input_dict, None, instrument, None, ins_c, None, c)

                if und_ins or contr_size:
                    create_end_sec = ins_c.und_insaddr in FSettlementGeneral.und_ins_security or \
                    ins_c.instype in FSettlementGeneral.und_ins_security
                    for tr in trades:
                        FSettlementGeneralRT.update_premium(tr, input_dict, SN, None, tr, ins_c)
                        if create_end_sec:                                                      
                            FSettlementGeneralRT.update_premium(tr, input_dict, 'End Security', None, tr, ins_c)
                            
                if instObj.mbf_find_object('!CURR'):
                    input_dict['curr'] = instObj.mbf_find_object('!CURR').mbf_get_value()
                    currency = int(instObj.mbf_find_object('CURR').mbf_get_value())
                    if currency:                        
                        FSettlementGeneralRT.update_secnom_from_instr(instrument, None, currency, ins_c)
                        
                if instrument.instype in FSettlementGeneral.ins_combination:
                    #comb_dict = parseEntitytoDict(instObj, combS, 'COMBINATIONLINK', 'SEQNBR')
                    comb_dict = get_dict_from_MBF(instObj, 'COMBINATIONLINK', EV_NUED)
                    print_e_dict(comb_dict, 'COMBINATIONLINK', print_mode)
                    FSettlementGeneral2.sub_combinationlink(comb_dict, instrument, trades, input_dict, ins_c)
                # combination member, find sec_insaddr security nominal settlements for combinationtrade??

                if param.valid_instrument_types_accrued_interest:
                    for tr in trades:
                        FSettlementGeneral2.update_accrued_interest(tr, input_dict, ins_c, tr)
                    
                if (input_dict.has_key('curr') or input_dict.has_key('exp_day'))\
                    and instrument.instype in FSettlementGeneral.und_ins_security:
                    for tr in trades:
                        FSettlementGeneralRT.update_premium(tr, input_dict, 'End Security')

    #DIVIDEND
    if instrument and hasTrade and instrument.instype in ['Stock', 'EquitySwap']:                
        div_dict = parseEntitytoDict(instObj, divS, 'DIVIDEND', 'SEQNBR')
        print_e_dict(div_dict, 'DIVIDEND', print_mode)
        
        if div_dict:
            sub_div(div_dict, instrument)
        else:
            log(1, 'No instrument or div_dict --> sub_dividend will not run')
        
        df = instObj.mbf_find_object('!DIVIDEND_FACTOR')
        iss = instObj.mbf_find_object('!ISSUER_PTYNBR')
        div_factor = None
        iss_ptynbr = None
        div_diff_dict = {}
        if df:
            div_factor = float(instObj.mbf_find_object\
                               ('DIVIDEND_FACTOR').mbf_get_value())
            div_diff_dict['div_factor'] = div_factor # just a trigger
        if iss:
            iss_ptynbr = int(instObj.mbf_find_object\
                             ('ISSUER_PTYNBR').mbf_get_value())
            div_diff_dict['issuer_ptynbr'] = iss_ptynbr

        # update dividend SR if stock.dividend_factor or issuer has changed
        if div_factor or iss:
            eqs_mode = FSettlementGeneral3.is_equity_swap(instrument)
            if FSettlementGeneral3.div_dict_has_values(div_dict):
                divs = FSettlementGeneralRT.divs_from_instrument(instrument, div_dict)
            else:
                divs = FSettlementGeneralRT.divs_from_instrument(instrument)
            
            for d in divs:
                pr = 'update_div: instrument %s has changed (div_factor or iss_ptynbr) Error?' \
                 % (instrument.insid)
                log(1, pr)    
                FSettlementGeneralRT.update_div(d, div_diff_dict, ins_c, None, eqs_mode)
                
    if instrument and hasTrade and instrument.instype == 'Combination':
        div_factor = 1
        iss_ptynbr = 0
        df = instObj.mbf_find_object('!DIVIDEND_FACTOR')
        iss = instObj.mbf_find_object('!ISSUER_PTYNBR')
        div_diff_dict = {}
        if df:
            div_factor = float(instObj.mbf_find_object\
                               ('DIVIDEND_FACTOR').mbf_get_value())
            div_diff_dict['div_factor'] = div_factor
        if iss:
            iss_ptynbr = int(instObj.mbf_find_object\
                             ('ISSUER_PTYNBR').mbf_get_value())
            div_diff_dict['issuer_ptynbr'] = iss_ptynbr
        if div_factor or iss:
            for tr in trades:
                FSettlementGeneralRT.update_combination_eq_swap_dividends(tr, div_diff_dict)

    if (hasTrade or hasCoupons) and (get_prefix(instObj) not in prohibited_events):        
        #comb, changes bellow should be reflected in amb_get_cf_from_leg
        for prefix in leg_dict.keys():
            prfx_list = leg_dict[prefix] # list with the legs
            for legObj in prfx_list: 
                cf_dict = get_dict_from_MBF(legObj, 'CASHFLOW')
                leg = legObj.mbf_find_object('LEGNBR')
                leg_c = None
                if leg:
                    legnbr = int(leg.mbf_get_value())
                    if legnbr:
                        leg_ent = ael.Leg[legnbr]
                        leg_c = FSettlementGeneral3.get_entity_class(legObj, leg_fields, leg_ent, 'Leg')
                        print_e_dict(cf_dict, 'CASHFLOW', print_mode)
                        sub_cf(cf_dict, instrument, legObj, cfs, ins_c, leg_c)
                #RESET                
                for pfx in cf_dict.keys():
                    for cfObj in cf_dict[pfx]:
                        cf_ent = None
                        cf = cfObj.mbf_find_object('CFWNBR')
                        if cf:
                            cfwnbr = int(cf.mbf_get_value())
                            if cfwnbr:
                                cf_ent = ael.CashFlow[cfwnbr]                        
                        cf_c = FSettlementGeneral3.get_entity_class(cfObj, cf_fields.keys(), cf_ent, 'CashFlow')
                        res_dict = get_dict_from_MBF(cfObj, 'RESET', EV_NU)
                        for prefix in res_dict.keys():
                            prfx_list = res_dict[prefix]
                            for resObj in prfx_list:
                                cfs = sub_reset(resObj, prefix, cfs, trades, leg_dict, ins_c, leg_c, cf_c)
        
    return notFound

def get_all_combination_trades_for_ins(eq_swap_ins):
    query_list = None
    ret_list = []
    
    query = """SELECT t.trdnbr
               FROM Trade t,
                    Instrument i,
                    CombinationLink c
               WHERE t.insaddr = i.insaddr AND
                     i.insaddr = c.owner_insaddr AND
                     c.member_insaddr = """ + str(eq_swap_ins.insaddr)
    try:
        query_list = ael.asql(query, 1)[1][0]
    except Exception, e:
        ael.log('Exception in get_all_combination_trades_for_ins ! Cause: %s' % e)
    if query_list:
        for (trade,) in query_list:
            ret_list.append(trade)
    return ret_list
    

def parsePartyEntity(ptyObj, ev):
    '''Important function that takes care of the Party and Account mbfObjects'''
    global version_not_ok
    pr = ''
    notFound = 1
    party = None
    intermediary = None
    if ptyObj:
        ptynbrObj = ptyObj.mbf_find_object('PTYNBR')        
        if ptynbrObj:
            notFound = 0            
            if ev and ev == '-':
                return notFound

            ptynbr = ptynbrObj.mbf_get_value()
            if ptynbr:
                party = ael.Party[int(ptynbr)]
            version_not_ok = FSettlementGeneral3.version_not_ok(ptyObj, party, ev, 3)
            if party and ev == 'UPDATE':                            
                ptyid = ptyObj.mbf_find_object('PTYID')         
                if ptyid:                    
                    ptyid = ptyObj.mbf_find_object('PTYID').mbf_get_value()
                elif version_not_ok == 3:
                    ptyid = party.ptyid
                else:
                    pr = 'parsePartyEntity: ptyid changed but version_ok=0 no update will be done (Error)'
                    log(1, pr)
                    return notFound
                                                
                oldPtyid = ptyObj.mbf_find_object('!PTYID')         
                if oldPtyid:                    
                    oldPtyid = ptyObj.mbf_find_object('!PTYID').mbf_get_value()
                    update_partyid(party, oldPtyid, ptyid) 

                #create dictionary ACCOUNT, only !,-
                acc_dict = get_dict_from_MBF(ptyObj, 'ACCOUNT', EV_UD)
                print_e_dict(acc_dict, 'ACCOUNT', print_mode)
                sub_acc(acc_dict, party)
            elif not party:
                pr = 'parsePartyEntity: party could not be found'
                log(1, pr)      
    else:
        pr = 'parsePartyEntity: No party obj, wrong input'
        log(1, pr)
    return notFound


def parseTrEntity(trObj, ev):
    'Important function that takes care of the Trade mbfObjects.\
    AMB messages for TRADE do not have information about\
    cashflows and dividends (only payments) so this information is fetched\
    via AEL.'
    
    global param
    global version_not_ok
    SN = 'Security Nominal'
    notFound = 1
    
    
    if trObj:                        
        trdnbrObj = trObj.mbf_find_object('TRDNBR')
        if trdnbrObj:
            notFound = 0
            if ev and ev == 'DELETE':
                return notFound
                
            trdnbr = int(trdnbrObj.mbf_get_value())
            pr = 'Trade %d Event %s' % (trdnbr, ev)
            log(1, pr)
            
            tr = ael.Trade[trdnbr]                
            version_not_ok = FSettlementGeneral3.version_not_ok(trObj, tr, ev, 1)
            tr_c = FSettlementGeneral3.get_entity_class(trObj, tr_fields, tr, 'Trade')
            if FSettlementGeneralRT.is_trade(tr_c):
                if FSettlementGeneral.is_valid_instrument(tr_c.insaddr):
                    correction = FSettlementGeneral2.is_correction_trade(tr_c) 
                    pay_dict = get_dict_from_MBF(trObj, 'PAYMENT', EV_NUE)
                    if ev == 'INSERT':
                        if FSettlementGeneral.is_excluded_acq_trade(tr_c) or \
                         FSettlementGeneral.is_excluded_portfolio_trade(tr_c) or \
                         FSettlementGeneral.is_prevent_settlement_processing_for_trade(tr_c):
                            return notFound
                        #insert trade takes care of premium, cfs, divs and payments
                        FSettlementGeneralRT.insert_trade(tr_c, tr_c, pay_dict)
                    elif ev == 'UPDATE':
                        diffs = 0 # amount of differences between new and old ent
                        concider_others = 1 # if status to void then special event treatment
                        newEnt = tr                            
                        diff_dict = {} #contains changed atributes and it's stringvalues
                        for atr in tr_fields:
                            oldField = trObj.mbf_find_object('!'+atr)
                            if oldField:
                                diffs = diffs + 1
                                newField = None
                                newField = trObj.mbf_find_object(atr)
                                if newField:
                                    diff_dict[atr.lower()] = newField.mbf_get_value()                                    

                        touch_closed_trade = 0
                        status = None # actual status
                        fromStatus = None # previous status
                        generate_from_new_trade_status = 0
                        term_fee = 0
                        combination_mode = 0
                        combination_trade = 0
                        if tr_c.insaddr.instype in FSettlementGeneral.ins_combination:
                            combination_trade = 1
                            if len(diff_dict):
                                combination_mode = 1
                                
                        if trObj.mbf_find_object('!STATUS'):
                            fromStatus = trObj.mbf_find_object('!STATUS').mbf_get_value()
                            if trObj.mbf_find_object('STATUS'):
                                status = trObj.mbf_find_object('STATUS').mbf_get_value()

                        if status and fromStatus:
                            pr = 'Trade %d, status change: %s to %s' % \
                            (tr.trdnbr, fromStatus, status)
                            log(1, pr)
                            if FSettlementGeneral2.is_status_to_be_voided(fromStatus) and \
                               status in FSettlementGeneral.new_status_to_void:
                                # trade status from fo conf to void (just example)
                                FSettlementGeneral.void_trade_recall_setls(tr_c, fromStatus, None)                                
                                diffs = 0 
                                concider_others = 0                                
                                term_fee = (status == 'Terminated') # add termination fee if needed
                            elif is_unqualified_trade_status(fromStatus) and status in param.status:
                                # take care of simulated trades being confirmed (just example)
                                generate_from_new_trade_status = 1
                                diffs = diffs + 1
                                touch_closed_trade = 1
                                if combination_trade:                                    
                                    combination_mode = 1
                        elif status:
                            if status in FSettlementGeneral.new_status_to_void:
                                diffs = 0 
                                concider_others = 0                                
                                term_fee = (status == 'Terminated')# Termination fee might be added, sub_pay to take care
                                pr = 'Update of Trade %d not relevant for settlements (status %s)' % (tr.trdnbr, status)
                                log(1, pr)

                        #If any TAL has been updated, all settlements of this
                        #trade have to be updated
                        tal_dict = parseEntitytoDict(trObj, talS, 'TRADEACCOUNTLINK', 'SEQNBR')
                        if tal_dict:
                            for a in tal_dict.keys():
                                if len(tal_dict[a]):
                                    diffs = diffs + 1
                                    diff_dict['trade_account_link'] = 'trade_account_link'
                                    break
                        primary_issuance_changed = 0                                    
                        add_dict = parseEntitytoDict(trObj, addS, 'ADDITIONALINFO', 'RECADDR')
                        if add_dict:
                            for a in add_dict.keys():
                                for obj in add_dict[a]:
                                    newField = obj.mbf_find_object(\
                                        'ADDINF_SPECNBR.FIELD_NAME')
                                    if newField:
                                        if newField.mbf_get_value() == \
                                               'Primary Issuance':
                                            diffs += 1
                                            valueField = obj.mbf_find_object('VALUE')
                                            if valueField:                                                
                                                primary_issuance_changed = (a == "!")
                                                diff_dict['primary_issuance'] = valueField.mbf_get_value()
                                                if diff_dict['primary_issuance']:
                                                    tr_c['primary_issuance'] = get_primary_issuance_or_ipa(diff_dict, 'primary_issuance')
                                            else:
                                                diff_dict['primary_issuance'] = None
                                                
                                        elif newField.mbf_get_value() == \
                                                 'IPA':
                                            diffs += 1
                                            if a == '-':
                                                diff_dict['ipa_removed'] = \
                                                  'ipa_removed'
                                            else:
                                                valueField = \
                                               obj.mbf_find_object('VALUE')
                                                if valueField:
                                                    diff_dict['ipa'] = \
                                                 valueField.mbf_get_value()
                                                    if diff_dict['ipa']:
                                                        tr_c['ipa'] = get_primary_issuance_or_ipa(diff_dict, 'ipa')                                                                                                           
                                                else:
                                                    diff_dict['ipa'] = None
                                        elif newField.mbf_get_value() == 'No Settlement Trade':
                                            diffs += 1
                                            valueField = obj.mbf_find_object('VALUE')
                                            if valueField:
                                                diff_dict['No Settlement Trade'] = valueField.mbf_get_value()

                        if correction and not tr_c.status in FSettlementGeneral.new_status_to_void:
                            diffs = diffs + 1                                
                            diff_dict['correction'] = 'trade_correction'
                        if FSettlementGeneral2.is_closing(tr) and touch_closed_trade:
                            FSettlementGeneral2.touch_closed_trade(tr) # only if net_based_on_close_trade!
                        if diffs:
                            # the trade has changed, do the update
                            if (diff_dict.has_key('acquirer_ptynbr.ptyid') or \
                               diff_dict.has_key('counterparty_ptynbr.ptyid') or \
                               diff_dict.has_key('No Settlement Trade')) and \
                               (FSettlementGeneral.is_excluded_acq_trade(tr_c) or \
                               FSettlementGeneral.is_prevent_settlement_processing_for_trade(tr_c)):
                                recall_excluded_settles(tr_c)
                                return notFound
                                
                            if diff_dict.has_key('prfnbr') and FSettlementGeneral.is_excluded_portfolio_trade(tr_c):
                                recall_excluded_settles(tr_c)
                                return notFound
                                
                            if (not generate_from_new_trade_status) and is_prevent_update(diff_dict, tr_c):
                                return notFound
                            FSettlementGeneralRT.update_premium(newEnt, diff_dict, 'Premium', None, tr_c)
                            if newEnt.insaddr.instype in FSettlementGeneral.und_ins_security \
                               or FSettlementGeneral.is_collateral_trade(tr_c):
                                FSettlementGeneralRT.update_premium(newEnt, diff_dict, 'End Security', None, tr_c)
                                FSettlementGeneral2.validate(newEnt, 'UPDATE', tr_c)

                            fee = trObj.mbf_find_object('!FEE')
                            if not fee and (status and fromStatus):
                                # trade status has changed, AMBA migth lost info about fee update
                                fee = trObj.mbf_find_object('FEE')
                                if fee:
                                    diff_dict['fee'] = fee.mbf_get_value()
                            if fee or \
                               len(FSettlementGeneral.get_setl_rows(tr.trdnbr, 'Fee', '')):### IV
                                #setl row of type fee can still exist and needs update
                                FSettlementGeneralRT.update_premium(newEnt, diff_dict, 'Fee', None, tr_c)

                            FSettlementGeneral2.update_accrued_interest(tr, diff_dict, tr.insaddr, tr_c)

                        do_update = (concider_others and diffs) # trigger updates only if trade changed

                        if do_update:
                            cfs = []
                            if primary_issuance_changed and diff_dict['primary_issuance'] == 'No':
                                cfs = FSettlementGeneralRT.cfs_from_tr(tr, tr_c, coupon_check = 0)
                            else:                                                        
                                cfs = FSettlementGeneralRT.cfs_from_tr(tr, tr_c)                            

                            for cf in cfs:           
                                FSettlementGeneralRT.update_cf(cf, diff_dict, tr, None, tr_c, None, None)
                                    
                            coupons = list()
                            if FSettlementGeneral.has_coupon_generating_underlying_instrument(tr):
                                coupons = FSettlementGeneralRT.coupons_from_tr(tr, None, None, None, tr.insaddr.und_insaddr)
                            else:
                                coupons = FSettlementGeneralRT.coupons_from_tr(tr, None)
                            if len(coupons) and not FSettlementGeneral3.has_closed_security_nominal(tr):
                                del coupons[:]
                            for c in coupons:
                                FSettlementGeneralRT.update_cf(c, diff_dict, None, tr_c.insaddr, None, tr_c.insaddr, None, c, None, tr)

                            eqs_mode = FSettlementGeneral3.is_equity_swap(tr_c.insaddr)
                            divs = FSettlementGeneralRT.divs_from_instrument(tr_c.insaddr, None, 1)
                            for d in divs:
                                if not eqs_mode:
                                    FSettlementGeneralRT.update_div(d, diff_dict, tr_c.insaddr, tr_c, eqs_mode)
                                else:                                    
                                    FSettlementGeneralRT.update_div(d, diff_dict, tr_c.insaddr, tr_c, eqs_mode, 1)
                                    
                            FSettlementGeneralRT.update_combination_eq_swap_dividends(tr_c, diff_dict, 1)

                        if concider_others or term_fee: #do not use do_update since it can stop add payments
                            if pay_dict:
                                sub_pay(pay_dict, tr_c, term_fee)

                        if do_update and combination_mode:
                            diff_dict['combination_quantity'] = tr_c.quantity
                            FSettlementGeneral2.update_combination_trade(newEnt, diff_dict, 0, tr_c)

                elif tr.insaddr:
                    pr = '%s is not valid instrument type, no action on trade %d (File)' % (tr.insaddr.instype, tr.trdnbr)
                    log(1, pr)
            else:
                pr = 'parseTrEntity: input not a trade or already aggregated!'
                log(1, pr)
        else:
            log(1, 'Trade and/or Event is/are missing')
    return notFound


def print_e_dict(e_dict, entStr, mode):
    '''This function prints the dictionary.'''
    if e_dict:
        for ev in e_dict.keys():            
            le = len(e_dict[ev])            
            if mode:
                if mode == 1:
                    pr = '%s %d %s(S)' % (ev, le, entStr)
                    log(1, pr)
                elif le:
                    pr = '%s %d %s(S)' % (ev, le, entStr)
                    log(1, pr)
    return

def sameUser(setlObj, attrib):
    return FSettlementGeneral3.sameUser(setlObj, attrib)
    
def set_attr_for_entity(oldEnt, attrib, oldField):
    'Sets an attribute of the entity. Takes care of the type of the attribute.'
    if oldField:
        # what if ACCOUNT.curr.insid or pay2_accnbr.ptynbr.ptyid???
        position = attrib.find('.')
        ent = None
        org = attrib
        l = long(1)
        pr = ''
        if position > -1:            
            attrib = attrib[:position] #pay2_accnbr

        old = oldField.mbf_get_value()        
        t = type(getattr(oldEnt, attrib))
        
        objName = oldField.mbf_get_name()

        if t == type(str('1')):
            setattr(oldEnt, attrib, str(old))
        elif t == type(1.1):
            setattr(oldEnt, attrib, float(old))
        elif t == type(l):
            setattr(oldEnt, attrib, long(old))            
        elif t == type(1):
            setattr(oldEnt, attrib, int(old))
        elif t == ael.ael_date:            
            if old != '0000-01-01':
                setattr(oldEnt, attrib, ael.date(old))
        elif t == ael.ael_entity: 
            pr = 'The attribute is %s (File)' % (org)
            log(1, pr)
        else:
            pr = '%s attrib not set due wrong type! (File)' % (attrib)        
            log(1, pr)
    return


def sub_acc(e_dict, party):
    '''Acts on all account update or delete events'''
    acc = None
    intermediary_update = False
    if e_dict and party:
        diff_dict = {}
        #INSERT, do not bother does not effect Settlements
        #UPDATE            
        if len(e_dict['!']):
            for accObj in e_dict['!']:
                mbf_acc = accObj.mbf_find_object('ACCNBR')
                if mbf_acc:
                    diffs = 0 # amount of differences between new and old ent
                    acc_ent = ael.Account[int(mbf_acc.mbf_get_value())]
                    acc_c = FSettlementGeneral3.get_entity_class(accObj, acc_fields.keys(), acc_ent, 'Account')
                    acc_c_old = FSettlementGeneral3.get_entity_class(accObj, acc_fields.keys(), acc_ent, 'Account')
                    
                    for atr in acc_fields.keys():
                        oldField = accObj.mbf_find_object('!'+atr)
                        if oldField:
                            diffs = 1                            
                            if atr == 'NAME':
                                acc_c_old.name = oldField.mbf_get_value()
                                diff_dict['NAME'] = acc_c.name
                            elif atr == 'ACCOUNT':
                                acc_c_old.account = oldField.mbf_get_value()
                                diff_dict['ACCOUNT'] = acc_c.account
                            elif atr == 'NETWORK_ALIAS_TYPE':
                                if param.network_update:
                                    acc_c_old.network_alias_type = ael.InstrAliasType[int(oldField.mbf_get_value())]
                                    diff_dict['NETWORK_ALIAS_TYPE'] = int(oldField.mbf_get_value())
                                else:
                                    pass
                    
                    for field in corr_banks:
                        mbf_corr_old = accObj.mbf_find_object('!' + field)
                        if mbf_corr_old:
                            diffs = 1
                            intermediary_update = True
                                   
                    for field in accounts:
                        mbf_account_old = accObj.mbf_find_object('!' + field)
                        if mbf_account_old:
                            diffs = 1
                            intermediary_update = True        
                            
                    pu = FSettlementGeneral3.PartyUpdate(intermediary_update)
                    if diffs and acc_c and acc_c_old:
                        FSettlementGeneralRT.update_accounts(acc_c, acc_c_old, diff_dict, pu)
                    elif diffs:
                        log(1, 'sub_acc: There are diffs but no Account uppdate due to empty entity classes (Error)')
                        
        #DELETE, if the account is deleted somehow
        if len(e_dict['-']):
            for accObj in e_dict['-']:
                accnbr = '0'
                ptyid = '' # fallback value
                AD = 'Account deleted'
                acc_c = FSettlementGeneral3.Account(**{})
                acc_c_old = FSettlementGeneral3.Account(**{})
                mbf_accname = accObj.mbf_find_object('NAME')
                mbf_account = accObj.mbf_find_object('ACCOUNT')
                mbf_accnbr = accObj.mbf_find_object('ACCNBR')
                mbf_ptynbr = accObj.mbf_find_object('PTYNBR')                
                ok = 0
                
                if mbf_accnbr:
                    accnbr = mbf_accnbr.mbf_get_value()
                    acc_c.accnbr = int(accnbr)
                    acc_c_old.accnbr = int(accnbr)                   
                    
                if mbf_account:
                    acc_account = mbf_account.mbf_get_value()
                    acc_c.account = AD
                    acc_c_old.account = acc_account
                    diff_dict['!ACCOUNT'] = acc_account
                    diff_dict['ACCOUNT'] = AD
                    ok = ok + 1                    
                if mbf_accname:
                    acc_c_old.name = mbf_accname.mbf_get_value()
                    acc_c.name = AD
                    diff_dict['!NAME'] = mbf_accname.mbf_get_value()
                    diff_dict['NAME'] = AD
                    ok = ok + 1 
                if mbf_ptynbr:
                    ptynbr = mbf_ptynbr.mbf_get_value()
                    pty = ael.Party[int(ptynbr)]
                    if pty:
                        acc_c.ptynbr = pty
                        acc_c_old.ptynbr = pty
                    elif accObj.mbf_find_object('PTYNBR.PTYID'):                        
                        ptyid = accObj.mbf_find_object('PTYNBR.PTYID').mbf_get_value()

                if ok == 2:
                    pr = 'Account %s is deleted, remove account info from corresponding settlements' % accnbr
                    log(1, pr)
                    FSettlementGeneralRT.update_accounts(acc_c, acc_c_old, diff_dict, None, ptyid)
    return

    
def sub_cf(cf_dict, inst, leg, cf_list, ins_c=None, leg_c=None):
    '''Acts on all cf events that are stored in the cf dictionary.
    leg is amb object not an entity. '''
    ok = 0
    newEnt = None
    if leg:
        legnbr = leg.mbf_find_object('LEGNBR')
        leg2 = ael.Leg[int(legnbr.mbf_get_value())]                    
        leg_c = set_c(leg_c, leg2, 'Leg')
        
    for prfx in cf_dict.keys():
        if prfx == '!':
            #UPDATE
            event_list = cf_dict[prfx] #list with mbf_cf_object
            for mbfCF in event_list:
                cf = mbfCF.mbf_find_object('CFWNBR')                
                if cf:                    
                    cfwnbr = int(cf.mbf_get_value())
                    if cfwnbr:
                        if cfwnbr in cf_list: #Already updated cf!
                            return
                        else:
                            newEnt = ael.CashFlow[cfwnbr]
                cf_c = FSettlementGeneral3.get_entity_class(mbfCF, cf_fields.keys(), newEnt, 'CashFlow')
                diff_o = 0
                diff_dict = {}
                
                for atr in cf_fields.keys():
                    oldField = mbfCF.mbf_find_object('!'+atr)
                    if oldField:                
                        diff_o = 1                                                
                        newField = mbfCF.mbf_find_object(atr)
                        if newField:                                
                            diff_dict[atr.lower()] = newField.mbf_get_value()

                if leg:
                    curr = leg.mbf_find_object('!CURR.INSID')
                    if curr:
                        insid = leg.mbf_find_object('CURR.INSID').mbf_get_value()
                        diff_dict['curr.insid'] = insid
                        diff_o = 1
                    red_curr = leg.mbf_find_object('!REDEMPTION_CURR.INSID')
                    if cf_c:
                        if red_curr and cf_c.type=='Fixed Amount' and \
                           leg_c.insaddr.instype == 'DualCurrBond':
                            diff_dict['curr.insid'] = red_curr
                            diff_o = 1
                if diff_o and newEnt:                                        
                    list = FSettlementGeneral2.find_coupons(newEnt, 'Coupon')
                    list += FSettlementGeneral2.find_coupons(newEnt, 'Coupon transfer')
                    if len(list):
                        FSettlementGeneralRT.update_cf(newEnt, diff_dict, None, inst, None, ins_c, leg_c, cf_c)
                    else:
                        #no ins just newEnt as cf
                        FSettlementGeneralRT.update_cf(newEnt, diff_dict, None, None, None, None, None, newEnt)
                elif diff_o:
                    log(1, 'sub_cf: cash_flow entity could not be found inspite diffs, no update (File)')
                    
        elif prfx == '+':
            #INSERT                          
            event_list = cf_dict[prfx] #list with mbf_cf_object
            for mbfCF in event_list:
                cfwnbr = mbfCF.mbf_find_object('CFWNBR')
                if cfwnbr:                                                
                    newEnt = ael.CashFlow[int(cfwnbr.mbf_get_value())]                    
                    cf_c = FSettlementGeneral3.get_entity_class(mbfCF, cf_fields.keys(), newEnt, 'CashFlow')
                    create = FSettlementGeneral3.get_create(newEnt, inst, leg_c)
                    #create_cf should check the existens of the trade                        
                    FSettlementGeneralRT.create_cf(newEnt, None, None, create, cf_c, None, leg_c)#ins_c
                    #SPR 21079: to be remodelled when amba sends in accurate cf-amb_message
                    #as it is now following block will be executed for every cf (unnecessery)
                    #new solution must include create_cf remodelling
                    if FSettlementGeneral3.create_call_fixed_float(inst, leg_c):
                        FSettlementGeneral3.create_or_update_call_fixed(inst, cf_c, create, newEnt)
                    #collateral check here and in EOD?

                    if not newEnt:
                        pr = 'create_cf: cash_flow entity for %s could not be found (File)' % (cfwnbr.mbf_get_value())
                        log(1, pr)
        elif leg:
            event_list = cf_dict[prfx] 
            for mbfCF in event_list:
                newEnt = None
                cf = mbfCF.mbf_find_object('CFWNBR')
                if cf:
                    cfwnbr = int(cf.mbf_get_value()) 
                    if cfwnbr:
                        newEnt = ael.CashFlow[cfwnbr]
                if newEnt:
                    cf_c = FSettlementGeneral3.get_entity_class(mbfCF, cf_fields.keys(), newEnt, 'CashFlow')
                    diff_dict = {}
                    curr = leg.mbf_find_object('!CURR.INSID')
                    if curr:
                        insid = leg.mbf_find_object('CURR.INSID').mbf_get_value()
                        diff_dict['curr.insid'] = insid
                    red_curr = leg.mbf_find_object('!REDEMPTION_CURR.INSID')
                    if newEnt:
                        if red_curr and cf_c.type=='Fixed Amount' and \
                           cf_c.legnbr.insaddr.instype == 'DualCurrBond':
                            diff_dict['curr.insid'] = red_curr

                    if diff_dict.has_key('curr.insid'):
                        if FSettlementGeneral2.find_coupons(newEnt, 'Coupon'):
                            FSettlementGeneralRT.update_cf(newEnt, diff_dict, None, inst, None, ins_c, leg_c, cf_c)
                        else:
                            FSettlementGeneralRT.update_cf(newEnt, diff_dict, None, None, None, None, leg_c, cf_c)#
    return

        
def sub_div(div_dict, inst):
    '''Acts on all dividends in the dictionary.
    inst can be ins_c'''
    if inst == None:
        log(1, 'sub_div: instrument is none, no dividends will be found')

    for prfx in div_dict.keys():                            
        newEnt = None        
        if prfx == '!':
            #UPDATE
            for mbfDiv in div_dict[prfx]:
                
                seqnbr = None
                mbfSeqnbr = mbfDiv.mbf_find_object('SEQNBR')
                if mbfSeqnbr:
                    seqnbr = int(mbfSeqnbr.mbf_get_value())
                if seqnbr != None:
                    if seqnbr:
                        #add valid dividends (concider historical dividends)
                        newEnt = ael.Dividend[seqnbr]
                div_c = FSettlementGeneral3.get_entity_class(mbfDiv, div_fields.keys(), newEnt, 'Dividend')
                diff_dict = {}
                diff_o = 0
                
                for atr in div_fields.keys():
                    oldField = mbfDiv.mbf_find_object('!'+atr)
                    if oldField:
                        diff_o = 1                                
                        newField = mbfDiv.mbf_find_object(atr)
                        if newField:
                            diff_dict[atr.lower()] = newField.mbf_get_value()                         
                
                if diff_o and newEnt:
                    if not FSettlementGeneral3.is_equity_swap(inst):
                        FSettlementGeneralRT.update_div(div_c, diff_dict, inst, None, 0)
                    else:
                        log(1, 'EquitySwap dividend changed, no actions will be taken! \
                        (New settlement will be created and the old removed later)')
                        
                elif diff_o:
                    log(1, 'Diff exists but newEnt is None\
                    No update_div will be done! (File)')                    
        elif prfx == '+':
            #INSERT
            divs = []
            for mbfDiv in div_dict[prfx]:                                                            
                seqnbr = None
                mbfSeqnbr = mbfDiv.mbf_find_object('SEQNBR')
                if mbfSeqnbr:
                    seqnbr = int(mbfSeqnbr.mbf_get_value())
                if seqnbr != None:
                    if seqnbr:
                        newEnt = ael.Dividend[seqnbr] #div_c
                    div_c = FSettlementGeneral3.get_entity_class(mbfDiv, div_fields.keys(), newEnt, 'Dividend')                        
                    #add valid dividends (concider historical dividends)
                    if div_c:
                        FSettlementGeneralRT.create_div(div_c, None, 'New', inst)
                        divs.append(div_c)
                    else:
                        log(1, 'No create_div will done, \
                        newEnt is none. (File)')
            if inst.instype == 'EquitySwap':
                tr_list = get_all_combination_trades_for_ins(inst)
                for tr in tr_list:
                    FSettlementGeneralRT.create_eq_swap_dividend(tr, divs)
                    
        #elif prfx == '-': The core system is taking care of this!
    return


def sub_pay(pay_dict, tr_c=None, term_fee=0):
    '''Acts on all Payments in the dictionary.
    If term_fee flag is deployed it means that settlements are about 
    to be recalled only termination fee should be left out or added.'''
    print_e_dict(pay_dict, 'PAYMENT', print_mode)
    
    for prfx in pay_dict.keys():
        if prfx in ['!', 'empty']:
            #UPDATE
            for mbfPay in pay_dict[prfx]: #list with mbf_pay_object
                newEnt = None

                paynbr = mbfPay.mbf_find_object('PAYNBR')
                if paynbr:
                    newEnt = ael.Payment[int(paynbr.mbf_get_value())]
                    pay_c = FSettlementGeneral3.get_entity_class(mbfPay, pay_fields.keys(), newEnt, 'Payment')
                diff_o = 0
                diff_dict = {}    
                if prfx == '!':
                    for atr in pay_fields.keys():
                        oldField = mbfPay.mbf_find_object('!'+atr)
                        if oldField:
                            diff_o = 1
                            newField = mbfPay.mbf_find_object(atr)
                            if newField:                                
                                diff_dict[atr.lower()] = newField.mbf_get_value()                
                elif prfx == 'empty' and (not term_fee or tr_c.status in param.status): #tr_c.status != 'Void' see SPR 275098                                
                    diff_o = 1
                    diff_dict = {'amount':pay_c.amount}#just a trigger for FSettlementGeneralRT.createObjPay
                    diff_dict['empty'] = 'empty'
                if diff_o and newEnt:                        
                    FSettlementGeneralRT.update_payment(newEnt, diff_dict, pay_c, tr_c)
                elif diff_o:
                    log(1, 'update_payment will not be done, newEnt is None! (File)')                                        
        elif prfx == '+':            
            for mbfPay in pay_dict[prfx]:
                paynbrStr = mbfPay.mbf_find_object('PAYNBR')
                if paynbrStr:
                    paynbr = int(paynbrStr.mbf_get_value())
                    if paynbr:
                        newEnt = ael.Payment[paynbr]                        
                        pay_c = FSettlementGeneral3.get_entity_class(mbfPay, pay_fields.keys(), newEnt, 'Payment')
                        pr = 'FSettlementGeneralRT.create_payment(%d,None)' % (paynbr)
                        log(2, pr)                                                    
                            
                        if newEnt:
                            #termination fee shell go through even if terminated trade!!!
                            FSettlementGeneralRT.create_payment(newEnt, 'New', pay_c, tr_c)
                        else:
                            log(1, 'No create_payment will be done, \
                            newEnt is none! (File)')
    return

def sub_reset(resObj, prefix, cf_list, trades, leg_dict, ins_c=None, leg_c=None, cf_c=None):
    '''This function is needed due to fact that AMBA does not\
    recognize Reset changes on nor Cash Flow, nor Leg nor Instrument level.'''  
    if resObj:
        newEnt = None
        oldEnt = None
        nbr = resObj.mbf_find_object('RESNBR')
        legnbr = resObj.mbf_find_object('LEGNBR')        
        cfwnbr = resObj.mbf_find_object('CFWNBR')
        resnbr = 0
        
        if cfwnbr and cfwnbr in cf_list: #update to this cf already done!
            return
        if nbr:
            resnbr = int(nbr.mbf_get_value())
            if resnbr:
                newEnt = ael.Reset[resnbr]
            
            if cfwnbr and legnbr:
                pr = 'sub_reset: Leg %d CF %d Reset %s' % (int(legnbr.mbf_get_value()), int(cfwnbr.mbf_get_value()), nbr.mbf_get_value())
                log(1, pr)            

            if (newEnt == None and resnbr) and prefix and prefix != '-':
                pr = 'Reset %d can not be found (File)!' % (resnbr)
                log(1, pr)                            

        res_c = FSettlementGeneral3.get_entity_class(resObj, reset_fields.keys(), newEnt, 'Reset')
        if newEnt:                
            if prefix and prefix == '+':            
                FSettlementGeneralRT.create_reset(newEnt, res_c, newEnt.cfwnbr, ins_c, leg_c, cf_c)
            elif prefix and prefix == '!':
                #this must be done since AMBA does not show changes on CF
                diffs = 0
                diff_dict = {}                
                for atr in reset_fields.keys():
                    oldField = resObj.mbf_find_object('!'+atr)
                    if oldField:
                        diffs = 1
                        newField = resObj.mbf_find_object(atr)
                        if newField:                                
                            diff_dict[atr.lower()] = newField.mbf_get_value()  

                if diffs:
                    # update reset/cf for all trades                    
                    FSettlementGeneralRT.update_reset(newEnt, diff_dict, newEnt.cfwnbr, ins_c, leg_c, cf_c, res_c)
                    # As of SPR 270633 When making Close trade on a swap, the Close 
                    # Amount for the accrued interest does not consider if the legs are unfixed.
                    cf_list.append(newEnt.cfwnbr)
                    for t in trades:
                        diff_dict['quantity'] = t.quantity
                        FSettlementGeneral2.update_accrued_interest(t, diff_dict, ins_c, t)                                
                    
            elif prefix and prefix == '-':
                pr = 'Reset %d has been deleted, adapt Settlements (File)' % resnbr
                log(1, pr)

    return cf_list

def sub_setl(setlObj):
    global version_not_ok
    SN = 'Security Nominal'
    notFound = 1    
    pr = ''
    run_stp = 0
    status = ''
    newEnt = None
    oldField = None
    diffs = 0
    
    if setlObj:        
        notFound = 0        
        ev = get_prefix(setlObj)
        if ev and ev == '-':
            return notFound

        seqnbrStr = setlObj.mbf_find_object('SEQNBR')
        if seqnbrStr:
            seqnbr = int(seqnbrStr.mbf_get_value())
            if seqnbr:
                newEnt = ael.Settlement[seqnbr]
                version_not_ok = FSettlementGeneral3.version_not_ok(setlObj, newEnt, ev, 4)
                stt_c  = FSettlementGeneral3.get_entity_class(setlObj, setl_fields.keys(), newEnt, 'Settlement', version_not_ok)                                                
                status = stt_c.status
                
                if ev and ev != '' and status in FSettlementGeneral.stp_status:         
                    if ev == '!':                                                
                        if not sameUser(setlObj, 'UPDAT_USRNBR.USERID'):
                            # ATS login user may not be the same as Prime loginname
                            run_stp = 1
                        elif newEnt:                                
                            for atr in setl_fields.keys():
                                oldField = None
                                oldField = setlObj.mbf_find_object('!'+atr)
                                if oldField:
                                    diffs = diffs + 1

                            if diffs:
                                run_stp = 1
                        else:
                            pr = 'Settlement %d could not be find, no STP will be done (version_not_ok=%d)' % (seqnbr, version_not_ok)
                            log(4, pr)                            
                            run_stp = 0
                    elif ev == '+':                    
                        run_stp=1

                    if run_stp == 1:                        
                        reftype = stt_c.ref_type
                        if reftype != 'Split' and reftype != 'Net Part':
                            #These are ugly checks to keep exception
                            #and authorised status for specific status
                            #explanations!
                            if stt_c.status == 'Exception':
                                if FSettlementGeneral.check_status_exp(stt_c.status_explanation):
                                    pr = 'Settl %d in status Exception to be appended to STP queue' % (seqnbr)
                                    log(4, pr)
                                    FSettlementGeneral.append_settle(stt_c)
                            elif stt_c.status == 'Authorised':
                                if stt_c.status_explanation == 64 and param.authorise_historic_value_day:
                                    pr = 'Authorised setl with status_explanation 64 allowed, no action'
                                    log(4, pr)
                                elif FSettlementGeneral.check_manually_authorised(\
                                    stt_c.status_explanation):
                                    pr = 'Settlement %d, to be appended to STP queue' % (seqnbr)
                                    log(4, pr)
                                    FSettlementGeneral.append_settle(stt_c)
                            else:
                                FSettlementGeneral.append_settle(stt_c)
                elif ev and ev == '!' and status == 'Closed':
                    if stt_c.type == SN:
                        FSettlementGeneral2.update_position_cover(stt_c, None, None, None)
                                        
    return notFound            


def createSenderSources(senderSource, valid_entities):
    'Help function for dynamic generation of Sender sources. \
    For more see sender_source in amba.ini'
    
    ret = []
    pr = ''
    if senderSource != None:
        if len(senderSource)>1:
            if len(valid_entities):
                for s in valid_entities:
                    ret.append(senderSource+'/'+s)
            else:
                pr = 'Edit array \"valid_entities\" in FSettlementAMB module!!!'
        else:
            pr = 'RECEIVER_SOURCE variable in FSettlementAMB is empty string!!!'
    else:
        pr = 'RECEIVER_SOURCE variable in FSettlementAMB is not configured!!!'

    log(0, pr)    
    return ret

def update_partyid(party, oldPtyid, ptyid):
    '''Some party may change name then corresponding non closed\
    settlements need to be updated'''

    diff_dict = {}
    if ptyid:
        diff_dict['PTYID'] = ptyid
        pr = 'Party id changed from %s to %s' % (oldPtyid, ptyid)
        log(1, pr)
        
    query = """SELECT s.seqnbr
                FROM Settlement s
                WHERE (s.party_ptyid = \'%s\' OR s.acquirer_ptyid = \'%s\') AND s.status NOT IN (\'Closed\')""" % (oldPtyid, oldPtyid)
           
    query_list = ael.asql(query, 1)[1][0]
    
    acq_setls = [] #acquirer may change acquirer_ptyid 
    cp_setls = [] #counterparty may change name party_ptyid
    acq_updated = [] # Have to update these separately, otherwise old updates will be overwritten
    cp_updated = []
        
    for (setl,) in query_list:
        if setl.status != 'Closed' and FSettlementGeneral.source_data(setl) \
           and not FSettlementGeneral.check_already_updated(setl.seqnbr, 1) \
           and FSettlementGeneral3.is_updatable(setl):
            if setl.party_ptyid == oldPtyid:
                cp_setls.append(setl)
            #might be internal settlement no else if here
            if setl.acquirer_ptyid == oldPtyid:
                acq_setls.append(setl)  
        elif setl.ref_seqnbr and setl.ref_type=='None':
            if setl.party_ptyid == oldPtyid:
                cp_updated.append(setl)
            if setl.acquirer_ptyid == oldPtyid:
                acq_updated.append(setl)

    if len(acq_setls) or len(cp_setls):
        pr = 'Corresponding settlements will be updated with new party id'
        log(1, pr)
        pr = '%d settlements have matching party_ptyid' % (len(cp_setls))
        log(1, pr)
        pr = '%d settlements have matching acquirer_ptyid' % (len(acq_setls))
        log(1, pr)
    else:
        pr = 'No settlements with matching party_ptyid or acquirer_ptyid'
        log(1, pr)
        
    for sr in cp_setls:        
        if not diff_dict or not diff_dict.has_key('PTYID'):
            continue
        setlObjList = FSettlementGeneral.create_from_settle([sr])
        if len(setlObjList):
            setlObj = setlObjList[0]
            if setlObj:
                newP = setlObj
                newP.party_ptyid = diff_dict['PTYID']
                pu = FSettlementGeneral3.PartyUpdate(False)
                FSettlementGeneralRT.update_setl_row(setlObj, newP, 'Updated', pu)  

    for setl in acq_setls:
        if not diff_dict or not diff_dict.has_key('PTYID'):
            continue
        setlObjList = FSettlementGeneral.create_from_settle([setl])
        if len(setlObjList)>0:
            setlObj = setlObjList[0]
            if diff_dict and setlObj:
                newP = setlObj
                newP.acquirer_ptyid = diff_dict['PTYID']
                pu = FSettlementGeneral3.PartyUpdate(False)
                FSettlementGeneralRT.update_setl_row(setlObj, newP, 'Updated', pu)  
    for setl in acq_updated:
        clone = setl.clone()
        clone.acquirer_ptyid = diff_dict['PTYID']
        FSettlementGeneral.append_transaction(clone)
    for setl in cp_updated:
        clone = FSettlementGeneral.get_mod_trans(setl.seqnbr)
        if not clone:
            clone = setl.clone()
        clone.party_ptyid = diff_dict['PTYID']
        FSettlementGeneral.append_transaction(clone)
    return

def set_c(ent_c, ent, entity_type):
    global version_not_ok
    return FSettlementGeneral3.set_c2(ent_c, ent, entity_type, version_not_ok)

     
####### EVENT_CB ######
def event_cb(channel, event, arg):
  global amb_mes_nbr
  global reader
  global version_not_ok
  ev = None
  entObj = None # entity Object
  entity = None # could be TRADE, INSTRUMENT
  entObjPfxN = None # ie !TRADE
  prfx = None
  pr = ''  
  version_not_ok = 0
  if event.event_type == 0:
    log(1, pr)
    amb_mes_nbr = amb_mes_nbr + 1
    buf = amb.mbf_create_buffer_from_data(event.message.data_p)
    mes = buf.mbf_read()
    if print_mode == 1:
        log(1, 'FSettlementAMB has caught the following message:')
        mes2 = mes.mbf_object_to_string()
        pr = "%d>\n %s" % (amb_mes_nbr, mes2)
        if (not mes2) or (mes2 and len(mes2) == 4):
            pr = "%d>\n Error, AMBA-message too big or just None!!!\n%s" % (amb_mes_nbr, mes2)
        
        log(1, pr)
   
    # get entity and event via TYPE=EVENT_ENTITY, ie TYPE=DELETE_TRADE
    tp_val = get_type(mes)
    if tp_val != '':        
        ev = get_event(tp_val)
        entity = get_entity(tp_val)    

    if ev and entity:                
        # TRADE
        notFound = 1
        if notFound:
            for i in range(0, 2):        
                trObj = get_sub_entity(mes, 'TRADE', i)
                if trObj and notFound:
                    notFound = parseTrEntity(trObj, ev)
        # INSTRUMENT        
        if notFound:
            for i in range(0, 2):
                instObj = get_sub_entity(mes, 'INSTRUMENT', i)
                if instObj and notFound:                
                    notFound = parseInstrEntity(instObj, ev)  # for divs, leg, cfs, resets 
                    if ev == 'UPDATE' and notFound == False and pauseWorkCallback and \
                    FSettlementGeneral.is_valid_instrument(get_ins_from_amb(instObj)):
                        log(1, 'Waiting for events that may be related to the updated instrument. Work callback disabled.')
                        pauseWorkCallback.Start()

        # PARTY
        if notFound:
            for i in range(0, 2):            
                partyObj = get_sub_entity(mes, 'PARTY', i)
                if partyObj and notFound:
                    notFound = parsePartyEntity(partyObj, ev)
        # SETTLEMENT
        if notFound:
            for i in range(0, 2):
                setlObj = get_sub_entity(mes, 'SETTLEMENT', i)
                if setlObj and notFound:
                    notFound = sub_setl(setlObj)        
    else:
        pr =  'Problems with AMBA message: empty ev and entity (%s,%s)' % (ev, entity)
        log(1, pr)
        
    amb.mb_queue_accept(reader, event.message, str(amb_mes_nbr))
      
  else:
      if event.event_type == 1:      
          amb_mes_nbr = 0
 
 
def work_cb(arg):
    if pauseWorkCallback:
        if pauseWorkCallback.IsRunning() and pauseWorkCallback.HasExpired():
            log(1, 'Waiting for events has expired after %f seconds. Work callback enabled.' % (pauseWorkCallback.GetElapsedTimeInSeconds()))
            pauseWorkCallback.Stop()
    
    if not pauseWorkCallback or (pauseWorkCallback and not pauseWorkCallback.IsRunning()):
        while FSettlementGeneral.stp_to_run():
            FSettlementGeneral.commit_settlements()
        while FSettlementGeneral.work_to_do():
            FSettlementGeneral.commit_transaction()
        
# the START of the FSettlmentAMB
def start():
    global reader
    global param
    global pauseWorkCallback
    try:    
        pr = "=== %s ===" % (time.ctime())
        log(1, pr)
        log(1, 'AMB subscription, starting setup...')
        amb.mb_init(amb_login)
        
        param = FSettlementParams.get_default_params()
        SECONDS_UNTIL_EXPIRY = param.CALL_BACK_SLEEP
        if SECONDS_UNTIL_EXPIRY > 0:
            pauseWorkCallback = Timer(SECONDS_UNTIL_EXPIRY)
        reader = amb.mb_queue_init_reader(RECEIVER_MB_NAME, event_cb, None)
        BO_ENTS = createSenderSources(RECEIVER_SOURCE, valid_entities)

        for ents in BO_ENTS:
            amb.mb_queue_enable(reader, ents)            

        ZoneInfoImported = param.ZoneInfoImported
        if ZoneInfoImported == 0:
            log(0, FSettlementGeneral2.noZoneinfoMsg())
        
        log(1, 'Setup completed, waiting for events ...')
        amb.mb_poll()
        ael.main_loop(work_cb, None)
        #amb.mb_main_loop() #calls event_cb when an event occurs

    except RuntimeError, extraInfo:
        pr = "init failed (%s)" % extraInfo
        log(1, pr)

def stop():
    return

def status():
    global param
    pr = '\nFSettlementAMB is running with parameters\n%s' % (param)    
    return pr

def log(level, s):
    return FSettlementGeneral.log(level, s)
    
def is_unqualified_trade_status(from_status):
    return FSettlementGeneral3.is_unqualified_trade_status(from_status)

def get_primary_issuance_or_ipa(diff_dict, key):
    '''Returns 1 for Yes, 0 for No and 0 for None. Function is used to set 
    primary issuance and ipa for the trade entity class'''
    
    ret = 0
    if key and key in ['primary_issuance', 'ipa'] and diff_dict.has_key(key):
        str = diff_dict[key]
        if str == 'Yes':
            ret = 1
    return ret

def recall_excluded_settles(tr_c):
    try:
        s_list = ael.Settlement.select('trdnbr = %d' % tr_c.trdnbr)
        for s in s_list:
            FSettlementGeneralRT.update_setl_row(s, ael.Settlement.new(), 'Recalled')
    except Exception, e:
        log(2, 'Settlements not found for trade %d. Cause: %s' % (tr_c.trdnbr, e))


    
def is_only_trade_status_update(diff_dict):
    """
    This function returns True if the only update was 
    update trade status.
    """
    key_list = diff_dict.keys()
    if len(key_list) == 1:
        if key_list[0] == 'status':
            return True
    return False

def is_prevent_update(diff_dict, tr_c):

    """
    If the only trade update was trade status update and
    settlements are already created for this trade,
    do not update existing settlements.
    """

    if is_only_trade_status_update(diff_dict):   
        try:
            settlements = ael.Settlement.select('trdnbr = %d' % tr_c.trdnbr)
            if len(settlements):
                for settlement in settlements:
                    FSettlementGeneral.append_settle(settlement)
                return True
        except Exception, e:
            log(2, 'Settlements not found for trade %d. Cause: %s' % (tr_c.trdnbr, e))
            return False

    return False




