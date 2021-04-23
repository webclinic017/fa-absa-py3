"""-----------------------------------------------------------------------------
PURPOSE              :  Changes underlying instrument on security loans
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

def _getSecurityLoans(underlying):
    query = acm.CreateFASQLQuery('FSecurityLoan', 'AND')
    
    op = query.AddOpNode('AND')
    op.AddAttrNode('Underlying.Oid', 'EQUAL', underlying.Oid())
    
    op = query.AddOpNode('OR')
    op.AddAttrNode('OpenEnd', 'EQUAL', acm.EnumFromString('OpenEndStatus', 'Open End'))
    op.AddAttrNode('ExpiryDate', 'GREATER_EQUAL', acm.Time().DateNow())
            
    return query.Select()

def ChangeUnderlyingInstrument(source, destination, log):
    log.Information('Loading security loans')
    securityLoans = _getSecurityLoans(source)
    
    acm.BeginTransaction()
    try:
        log.Information('Updating underlying instrument')
        for securityLoan in securityLoans:
            securityLoan.Underlying(destination)
            securityLoan.Commit()
        
        log.Information('Committing to database')
        acm.CommitTransaction()
    except Exception as ex:
        acm.AbortTransaction()
        log.Exception('An error occurred while changing the underlying from %(source)s to %(destination)s: %(exception)s' % 
            {'source': source.Name(), 'destination': destination.Name(),'exception': ex})
    else:
        log.Information('%(counter)i security loans updated from %(source)s to %(destination)s.' % 
            {'counter': len(securityLoans), 'source': source.Name(), 'destination': destination.Name()})
