""" Compiled: 2009-10-23 13:36:45 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementUpdateEffectiveFromDate

    (c) Copyright 2006 by SunGard FRONT ARENA. All rights reserved.
    
DESCRIPTION
    For this script to work properly, you have to log on to Prime with an old
    date, preferably 1970-01-01.
    
    This script updates the effective from date in existing settle instruction
    rules. If a standard settle instruction has more than one settle
    instruction rule, only the settle instruction rule with the earliest
    effective from date will be updated.
    
    When all effective from dates have been updated, the script will clone
    and commit ALL existing trades. This will in turn update the trade 
    account links.
----------------------------------------------------------------------------"""

import ael

ael_variables = [['date', 'Effective from date (yyyy-mm-dd)', 'date', 
                  None, ael.date_today().to_string(), 1, 0]]

def ael_main(dict):
    counter = 0
    effective_from = ael.date(dict['date'])
    
    list_ssi = ael.SettleInstruction.select()
    print('Updating effective from dates. Please wait...')
    for ssi in list_ssi.members():
        query = 'settle_seqnbr = %d' % ssi.seqnbr
        list_sir = ael.SettleInstructionRule.select(query)
        earliest_date = None
        sir_entity = None
        if(len(list_sir.members()) > 0):
            for sir in list_sir.members():
                if(earliest_date == None):
                    if(sir.effective_from != None):
                        earliest_date = sir.effective_from
                        sir_entity = sir
                if(earliest_date != None and sir.effective_from < earliest_date):
                    if(sir.effective_from != None):
                        earliest_date = sir.effective_from
                        sir_entity = sir
            sir_clone = sir_entity.clone()
            sir_clone.effective_from = effective_from
            try:
                sir_clone.commit()
                counter = counter + 1
            except RuntimeError, e:
                print('A runtime error ocurred while committing settle instruction rule %d: %s' % (sir_clone.seqnbr, e))
                print('Script still running. Please wait...')
            
    ael.poll()
    print('%d effective from dates updated. Now committing trades, please wait...' % counter)
    
    list_instrument = []
    list_deposit = ael.Instrument.select('instype = "Deposit"')
    list_zero = ael.Instrument.select('instype = "Zero"')
    list_option = ael.Instrument.select('instype = "Option"')
    list_future = ael.Instrument.select('instype = "Future/Forward"')
    list_trs = ael.Instrument.select('instype = "TotalReturnSwap"')
    list_cd = ael.Instrument.select('instype = "CD"')
    list_frn = ael.Instrument.select('instype = "FRN"')
    
    for ins in list_deposit:
        list_instrument.append(ins)
    for ins in list_zero:
        list_instrument.append(ins)
    for ins in list_option:
        list_instrument.append(ins)
    for ins in list_future:
        list_instrument.append(ins)
    for ins in list_trs:
        list_instrument.append(ins)
    for ins in list_cd:
        list_instrument.append(ins)
    for ins in list_frn:
        list_instrument.append(ins)
    
    trade_counter = 0
    for instrument in list_instrument:
        if instrument.legs().members() != []:
            list_trade = instrument.trades()
            for trade in list_trade.members():
                if trade.status == 'FO Confirmed' or trade.status == 'BO Confirmed' or trade.status == 'BO-BO Confirmed':
                    trade_clone = trade.clone()
                    try:
                        trade_clone.commit()
                        trade_counter = trade_counter + 1
                    except RuntimeError, e:
                        print('A runtime error ocurred while committing trade %d: %s' % (trade_clone.trdnbr, e))
                        print('Script still running. Please wait...')
    
    #list_trade = ael.Trade.select()
    #trade_counter = 0
    #for trade in list_trade.members():
    #    trade_clone = trade.clone()
    #    try:
    #        trade_clone.commit()
    #        trade_counter = trade_counter + 1
    #    except RuntimeError, e:
    #        print 'A runtime error ocurred while committing trade %d: %s' % (trade_clone.trdnbr, e)
    #        print 'Script still running. Please wait...'
    print('%d Trades committed. Script ended.' % trade_counter)



