'''-----------------------------------------------------------------------------
CashEquityRicCode

Date:                   2015-11-19
Purpose:                This module returns the Ric Code that is used to uniquely identify instruments
Department and Desk:    Cash Equities
Requester:              Cameron Ashton and Siboniso Mathonsi
Developer:              Anil Parbhoo
CR Number:              CHNG0003270572 
-----------------------------------------------------------------------------'''
import acm

def getRicCode(ins):
    '''Get the RIC code of the instrument from the Price Link Definition'''
    pld = [p for p in acm.FPriceLinkDefinition.Select('instrument = %s' %ins.Name())]    
    for pl in pld:
        if pl.Market().Name()=='SPOT' and pl.PriceDistributor().Name() == 'REUTERS_FEED':
            return pl.IdpCode() 
