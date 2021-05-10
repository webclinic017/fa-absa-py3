
"""----------------------------------------------------------------------------
MODULE
    MR_PortfolioSwapGrouper - Allows for grouping of portfolio swaps

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module allows for grouping of stock portfolios on mapped portfolio swaps
----------------------------------------------------------------------------"""

import acm

def Group_PortfolioSwapSplit(self): 
   
    pswaps = acm.FPortfolioSwap.Select('')
    
    ret=[]
    for pswap in pswaps:
        if pswap.Instrument().FundPortfolio() and self.Portfolio():
        
            if self.Portfolio().Name() == pswap.Instrument().FundPortfolio().Name():
                ret.append(pswap.Instrument().Name())
           
    
    return ret
            
