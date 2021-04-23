""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FUpdateTradeAccountLinks

    (c) Copyright 2006 by SunGard FRONT ARENA. All rights reserved.
    
DESCRIPTION
    This script updates the Trade account links of existing trades when 
    a new SSI (Standard Settlement Instruction) or SIR
    (Settle Instruction Rule) has been inserted.
----------------------------------------------------------------------------"""

import ael, time

ptyDict = {}

#This method returns a list containing all counterparties
def parties(sort=1):
    partyTypes = ['Counterparty', 'Intern Dept', 'Issuer', \
                  'Broker', 'Client']
    for p in partyTypes:
        pList = ael.Party.select('type = ' + '"' + p + '"')
        for pty in pList:
            ptyDict[pty.ptyid] = p
    if sort:
        tuplesList = [(x.upper(), x) for x in ptyDict.keys()]
        tuplesList.sort()
        return [x[1] for x in tuplesList]
    else:
        return ptyDict.keys()

cpList = parties(1) #List with all parties
    
#This method returns a list containing all instrument types, except None type   
def getAllInstTypes():
    i = 0
    str = ael.enum_to_string("InsType", i)
    pn = []
    while str != '?':
        if str != 'None' and str != 'UnKnown':
            pn.append(str)
        i = i +1
        str = ael.enum_to_string("InsType", i)
    return pn

instList = getAllInstTypes() #List with all instrument types
instList.sort()

ael_variables = [['parties', 'Party', 'string', cpList, None,\
    1, 1, 'Select Party'], ['instTypes', 'Instrument type', 'string',\
    instList, None, 1, 1, 'Select instrument type']]

def ael_main(dict):
    updated_trades = []
    for pty in dict["parties"]: 
            for i in dict["instTypes"]:
                for j in ael.Instrument.select("instype = " + i):
                    for t in j.trades():
                        update_TAL(t, pty, i, updated_trades)
    if len(updated_trades) == 1:
        print('One trade was commited.\n')
        print('Trade #' + updated_trades[0][0] + '   Instrument type: ' +\
                  updated_trades[0][1] + '   Party: ' + updated_trades[0][2])
    elif len(updated_trades) > 1:
        n = len(updated_trades)
        print(str(n) + ' trades were commited.\n')
        k = 0
        for tr in updated_trades:
            print('Trade #' + updated_trades[k][0] + '   Instrument type: ' +\
                  updated_trades[k][1] + '   Party: ' + updated_trades[k][2])
            k = k + 1

    else:
        print('No trades were commited.')

def TAL_is_valid(tal):
    ret = False
    if tal.accnbr != None or tal.sec_accnbr != None:
        if tal.accnbr == None: #tal.sec_nbr is not None
            if tal.sec_accnbr.name != None and\
            tal.settle_seqnbr != None and \
            tal.settle_seqnbr.seqnbr != None:
                ret = True
        else:
            if tal.accnbr.name != None and\
            tal.settle_seqnbr != None and \
            tal.settle_seqnbr.seqnbr != None:
                ret = True
    return ret

def get_ssi_type(tal):
    ret = ''
    if tal.accnbr != None and tal.sec_accnbr != None:
        ret = 'dvp'
    elif tal.accnbr != None:
        ret = 'cash'
    else:
        ret = 'sec'
    return ret

def set_unique_TALs(tal_list, dict):
    for tal in tal_list:
        if not dict.has_key(tal.seqnbr):
            dict[tal.seqnbr] = tal
            
def get_unique_valid_TALs(y_dict, t_dict):
    ret_dict = {}
    for k in y_dict.keys():
        if TAL_is_valid(y_dict[k]):
            ret_dict[k] = y_dict[k]
        elif TAL_is_valid(t_dict[k]):
            ret_dict[k] = t_dict[k]
    return ret_dict
    
def get_the_TALs(t):
    y_dict = {}
    t_dict = {}
    set_unique_TALs(t.used_accounts(0, ael.date_today().add_days(-1)), y_dict)
    set_unique_TALs(t.used_accounts(0, ael.date_today()), t_dict)
    return get_unique_valid_TALs(y_dict, t_dict)
    
def commit_trade_clone(trade_clone, seqnbr):
    for l in trade_clone.trade_account_links():
        if l.system_generated and l.seqnbr == seqnbr:
            l.updat_time = int(time.time())

def set_update_time(TAL_dict, tal, trade_clone, t):
    for j in TAL_dict.keys():
        if get_ssi_type(TAL_dict[j]) == 'cash':
            if TAL_dict[j].settle_seqnbr.seqnbr == tal.settle_seqnbr.seqnbr and \
            TAL_dict[j].accnbr.name != tal.accnbr.name:
                commit_trade_clone(trade_clone, j)
        elif get_ssi_type(TAL_dict[j]) == 'sec':
            if TAL_dict[j].settle_seqnbr.seqnbr == tal.settle_seqnbr.seqnbr and \
            TAL_dict[j].sec_accnbr.name != tal.sec_accnbr.name:
                commit_trade_clone(trade_clone, j)
        elif get_ssi_type(TAL_dict[j]) == 'dvp':
            if TAL_dict[j].settle_seqnbr.seqnbr == tal.settle_seqnbr.seqnbr and \
            (TAL_dict[j].sec_accnbr.name != tal.sec_accnbr.name or \
            TAL_dict[j].accnbr.name != tal.accnbr.name):
                commit_trade_clone(trade_clone, j)

def update_TAL(t, pty, instr, updated_trades):
    commited = False
    date_dict = {}
    earliest = ael.date('2500-01-01')
    if isValid(t, pty) and t.value_day != None:
        today = ael.date_today()
        valueDay = t.value_day
        ssil = ael.Settlement.select('trdnbr = ' + '"' + str(t.trdnbr) + '"')
        for s in ssil:
            if s.value_day >= ael.date_today():
                date_dict[s.value_day.to_string()] = True
                if s.value_day < earliest:
                    earliest = s.value_day
        if len(date_dict) > 0:
            trade_clone = t.clone()
            try:
                TAL_dict = {}
                for k in date_dict.keys():
                    for l in t.used_accounts(0, ael.date(k)):
                        if TAL_is_valid(l):
                            TAL_dict[l.seqnbr] = l
                    valid_dict = get_the_TALs(t)
                    for seqnbr in valid_dict.keys():
                        set_update_time(TAL_dict, valid_dict[seqnbr],\
                        trade_clone, t)
                    TAL_dict.clear()                
                trade_clone.commit()
                updated_trades.append([str(t.trdnbr), instr, pty])
            except RuntimeError:
                print("Due to a RuntimeError trade #" + \
                      str(t.trdnbr) + " was not commited.")


def isValid(trade, pty):
    ret = False
    if trade.counterparty_ptynbr != None and \
    trade.counterparty_ptynbr.ptyid != None and \
    trade.counterparty_ptynbr.ptyid == pty:
        ret = True
               
    elif trade.acquirer_ptynbr != None and \
    trade.acquirer_ptynbr.ptyid != None and \
    trade.acquirer_ptynbr.ptyid == pty:
        ret = True
               
    elif trade.broker_ptynbr != None and \
    trade.broker_ptynbr.ptyid != None and \
    trade.broker_ptynbr.ptyid == pty:
        ret = True
    return ret

    


