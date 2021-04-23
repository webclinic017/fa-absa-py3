"""-----------------------------------------------------------------------------
PURPOSE              :  Copies historical prices from one instrument to another
DEPATMENT AND DESK   :  SM PCG - Securities Lending Desk
REQUESTER            :  Marko Milutinovic
DEVELOPER            :  Francois Truter
CR NUMBER            :  526074
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer          Description
--------------------------------------------------------------------------------
2010-12-17 526074    Francois Truter    Initial Implementation
"""

import acm

def GetMarket(name):
    party = acm.FParty[name]
    if not party:
        raise Exception('Could not load market [%s].' % name)
    return party
    
def _marketArrayToStr(markets):
    marketsStr = '['
    syntax = ''
    for market in markets:
        marketsStr += syntax + market.Name()
        syntax = ', '
    marketsStr += ']'
    return marketsStr

def _getHistoricalPrices(instrument, markets):
    query = acm.CreateFASQLQuery('FPrice', 'AND')
    
    op = query.AddOpNode('AND')
    op.AddAttrNode('Day', 'LESS', acm.Time().DateNow())
    op.AddAttrNode('Instrument.Oid', 'EQUAL', instrument.Oid())
    
    if markets:
        op = query.AddOpNode('OR')
        for market in markets:
            op.AddAttrNode('Market.Oid', 'EQUAL', market.Oid())
            
    return query.Select()

def CopyHistoricalPrices(source, destination, markets, log):
    log.Information('Loading prices')
    prices = _getHistoricalPrices(source, markets)
    if not prices:
        log.Warning('%(instrument)s has no prices to copy for market(s) %(markets)s.' % 
            {'instrument': source.Name(), 'markets': _marketArrayToStr(markets)})
        return
    
    existingPrices = _getHistoricalPrices(destination, markets)
    acm.BeginTransaction()
    try:
        if existingPrices:
            log.Information('Deleting existing prices')
            for price in existingPrices:
                price.Delete()

        log.Information('Copying prices')
        counter = 0
        for price in prices:
            newPrice = price.Clone()
            newPrice.Instrument(destination)
            newPrice.Commit()
            counter += 1

        log.Information('Committing to database')
        acm.CommitTransaction()
    except Exception as ex:
        acm.AbortTransaction()
        log.Exception('An error occurred while copying prices from %(source)s to %(destination)s: %(exception)s' % 
            {'source': source.Name(), 'destination': destination.Name(),'exception': ex})
    else:
        log.Information('Copied %(counter)i price(s) from %(source)s to %(destination)s.' % 
            {'counter': counter, 'source': source.Name(), 'destination': destination.Name()})

