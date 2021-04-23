'''-----------------------------------------------------------------------
MODULE
    DCRM_FXBalances

DESCRIPTION
    This module is called by the DCRM_FXBalances ASQL to return PV balance 
    per currency per portfolio per instrument

    Department and Desk : Credit Desk
    Requester           : De Clercq Wentzel
    Developer           : Herman Hoon

    History:
    When: 	  CR Number:   Who:		What:       
    2010-05-24    203010       Herman Hoon	Created
    2010-11-03    483993       Herman Hoon      Amended to pick up FX Cash instruments.
    2010-11-08    487618       Herman Hoon      Amended to accumulate the values if there are more than one FX Cash instrument.
END DESCRIPTION
-----------------------------------------------------------------------'''

import acm, ael

def getBalance(temp,currn,pn,insn,*rest):  
    '''
Returns the PV balance per currency per portfolio per instrument 
from a virtual Trading Manager portfolio sheet
    '''
    context         = acm.GetDefaultContext()
    sheet_type      = 'FPortfolioSheet'
    column_id_1     = 'Portfolio Present Value Per Currency'
    column_id_2     = 'Portfolio Cash Vector'
    pf              = acm.FPhysicalPortfolio[pn]
    ins             = acm.FInstrument[insn]
    curr            = acm.FCurrency[currn]
    
    #create CalculationSpace (virtual Trading Manager)
    calc_space = acm.Calculations().CreateCalculationSpace(context, sheet_type)
    
    position = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    
    position.AddAttrNodeString('Instrument.Name', [insn], 'EQUAL')
    position.AddAttrNodeString('Portfolio.Name', [pn], 'EQUAL')
    
    position = position.Select()
    adhoc = acm.FAdhocPortfolio()
    for trade in position:
        adhoc.Add(trade)
    vector = acm.FArray()
    param  = acm.FNamedParameters()
    param.AddParameter('currency', curr)
    vector.Add(param)
    pv_column_config   = acm.Sheet.Column().ConfigurationFromVectorItem(vector)
    cash_column_config   = acm.Sheet.Column().ConfigurationFromVector(vector)
    
    pv = calc_space.CreateCalculation(adhoc, column_id_1, pv_column_config)
    cash = calc_space.CreateCalculation(adhoc, column_id_2, cash_column_config)
    
    try:
        pv = pv.Value()[0].Number()
        cash = cash.Value().Number()
        total = pv + cash
        #print currn, insn, pn, pv, cash, total, position.Size()
    except Exception, e:
        pv = None
        cash = None
        total = None
        print 'Error processing instrument %s: %s' %(insn, str(e))
    
    return total
