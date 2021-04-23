import ael, SAGEN_TRADE_UPDATES

ael_variables = [
                 ['date', 'Effective from date (yyyy-mm-dd)', 'date', None, ael.date_today().to_string(), 1, 0],
                 ['party', 'Counterparty', 'string', SAGEN_TRADE_UPDATES.CParty(), None, 1, 0]
                ]

def ael_main(dict):
    counter = 0
    effective_from = ael.date(dict['date'])
    party = ael.Party[dict['party']]
    print dict['party']
    list_ssi = ael.SettleInstruction.select('ptynbr=%d' %party.ptynbr)
    
    for ssi in list_ssi.members():
        list_sir = ael.SettleInstructionRule.select('settle_seqnbr=%d' %ssi.seqnbr)
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
                print 'A runtime error ocurred while committing settle instruction rule %d: %s' % (sir_clone.seqnbr, e)
                print 'Script still running. Please wait...'
                
    ael.poll()
    print '%d effective from dates updated. Now committing trades, please wait...' % counter
    
    trade_counter = 0
    trades = ael.Trade.select('counterparty_ptynbr=%d' %party.ptynbr)
    valid_instypes = ['Deposit', 'Zero', 'Option', 'Future/Forward', 'TotalReturnSwap']
    for t in trades.members():
        if t.insaddr.instype in valid_instypes:
            if t.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                trade_clone = t.clone()
                try:
                    trade_clone.commit()
                    trade_counter = trade_counter + 1
                except RuntimeError, e:
                    print 'A runtime error ocurred while committing trade %d: %s' % (trade_clone.trdnbr, e)
                    print 'Script still running. Please wait...'
                    
    print '%d Trades committed. Script ended.' % trade_counter
