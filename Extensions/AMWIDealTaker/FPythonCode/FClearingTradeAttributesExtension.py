"""------------------------------------------------------------------------
MODULE
    FClearingTradeAttributesExtension -
DESCRIPTION:
    Any overrides that users needs to achieve as per the business requirement can be achieved here. Kindly refer to documentation for further details   
VERSION: 1.0.30 
--------------------------------------------------------------------------"""
import ael
import acm
def updateTradeAttributes(aelTrd):
    """update the trade attributes as required"""
    #please note that the code provided below is a sample code
    '''
    aelTrd.fee = 50000
    aelTrd.quantity = 450000
    portfolio = ael.Portfolio['Backspread']
    if portfolio:
        aelTrd.prfnbr = portfolio
    '''    
    return aelTrd
    
    
def updateTradeOnCptyChange(acmTrade):
    #please note that the code provided below is a sample code
    '''
    portfolio = acm.FPhysicalPortfolio['Backspread']
    acmTrade.Portfolio(portfolio)
    '''
    return acmTrade
