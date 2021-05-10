"""-----------------------------------------------------------------------
MODULE
    AnnuityPayment

DESCRIPTION

    Date                : 2011-02-08
    Purpose             : Calculates the Annuity Payment for Annuity type cashflow structures.
    Department and Desk : FO Money Market
    Requester           : Neeran Govender
    Developer           : Herman Hoon
    CR Number           : 565028
    
ENDDESCRIPTION
-----------------------------------------------------------------------"""

import acm

calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def getAnnuityPayment(trade):
    ins = trade.Instrument()
    legs = ins.Legs()
     
    if legs:
        leg = legs[0]
        if leg.AmortType() == 'Annuity':
            cashFlows = leg.CashFlows()
            if cashFlows:
                cfs = []
                legStartDate = leg.StartDate()
                for cf in cashFlows:
                    if cf.StartDate() == legStartDate:
                        cfs.append(cf)
                
                if len(cfs) == 2:
                    cf1 = cfs[0].Calculation().Projected(calcSpace, trade)
                    cf2 = cfs[1].Calculation().Projected(calcSpace, trade)
                    annuityPayment = cf1 + cf2
                    return annuityPayment.Number()
    return 0
