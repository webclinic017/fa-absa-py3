
import acm

def _getSwiftAlias(party):
    
    swiftAlias = acm.FPartyAlias.Select01("party = %i and type = 'SWIFT'" % party.Oid(), 'More than one SWIFT alias for party: %i, %s' % (party.Oid(), party.Name()))
    if swiftAlias:
        return swiftAlias.Alias()
    else:
        return None

def _getSwiftCustodyAccount(party):
    custodyAccount = party.AdditionalInfo().CustodyAccount()
    if not custodyAccount:
        raise Exception("Party Additional Info 'CustodyAccount' is required for SWIFT MT535 and MT515 messages, it is not set for '%s'." % party.Name())
    else:
        return custodyAccount

def _getTradeCounterparty(instrument):
    trades = instrument.Trades()
    if len(trades) != 1:
        raise Exception("Could not get property 'TradeCounterparty' for instrument '%s'. Expected 1 trade, got %i." % (instrument.Name(), len(trades)))
    
    trade = trades[0]
    return trade.Counterparty()
    
def _getCustomOtcOrIsin(instrument, isCFd):
    if instrument.Otc() or isCFd:
        ISIN_LEN = 12
        PREFIX = 'ASA'
        return PREFIX + str(instrument.Oid()).rjust(ISIN_LEN - len(PREFIX), '0')
    elif instrument.InsType() in ('Future/Forward', 'Option', 'Repo', 'BuySellback') and not instrument.Otc():
        temp  = str(instrument.StorageId()).rjust(10, '0') 
        return 'AB' + temp 
    else:
        return instrument.Isin()
