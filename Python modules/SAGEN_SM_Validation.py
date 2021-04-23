import ael

def TradeUpdates(e, op):
    if e.record_type == 'Trade' and op == 'Update':
        if e.insaddr.instype == 'Deposit':
            if e.insaddr.legs()[0].cash_flows():
                for cf in e.insaddr.legs()[0].cash_flows():
                    if ael.Settlement.select('cfwnbr = %d' % cf.cfwnbr):
                        settlement = ael.Settlement.select('cfwnbr = %d' % cf.cfwnbr)
                        for s in settlement.members():
                            if s.status == 'Released':
                                print 'Can not update the trade because there is a payment being processed.'
                                raise 'Can not update the trade because there is a payment being processed.'

def InstrumentUpdates(e, op):
    if e.record_type == 'Instrument' and op == 'Update':
        if e.instype == 'Deposit':
            if e.legs()[0].cash_flows():
                for cf in e.legs()[0].cash_flows():
                    if ael.Settlement.select('cfwnbr = %d' % cf.cfwnbr):
                        settlement = ael.Settlement.select('cfwnbr = %d' % cf.cfwnbr)
                        for s in settlement.members():
                            if s.status == 'Released':
                                print 'Can not update the instrument because there is a payment being processed.'
                                raise 'Can not update the instrument because there is a payment being processed.'

def PartyUpdates(e, op):
    if e.record_type == 'Party' and op != 'Insert':
        status = ael.enum_from_string('SettlementStatus', 'Released')
        settlements = '''select
                            party.ptynbr
                        from
                            trade      ,
                            party      ,
                            settlement
                        where
                                trade.counterparty_ptynbr = party.ptynbr
                            and trade.trdnbr = settlement.trdnbr
                            and settlement.status = %d''' % (status)
        
        for settlement in ael.dbsql(settlements)[0]:
            for s in settlement:
                if e.ptynbr == s:
                    print 'Can not update the party because there is a payment being processed.'
                    raise 'Can not update the party because there is a payment being processed.'


def AcquirerUpdates(e, op):
    if e.record_type == 'Party' and op != 'Insert':
        status = ael.enum_from_string('SettlementStatus', 'Released')
        settlements = '''select
                            party.ptynbr
                        from
                            trade      ,
                            party      ,
                            settlement
                        where
                                trade.acquirer_ptynbr = party.ptynbr
                            and trade.trdnbr = settlement.trdnbr
                            and settlement.status = %d''' % (status)
        
        for settlement in ael.dbsql(settlements)[0]:
            for s in settlement:
                if e.ptynbr == s:
                    print 'Can not update the party because there is a payment being processed.'
                    raise 'Can not update the party because there is a payment being processed.'
