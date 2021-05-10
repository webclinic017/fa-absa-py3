"""----------------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapFunctions

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Generic functions for the Portfolio Swap GUI.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 455227
    
ENDDESCRIPTION
----------------------------------------------------------------------------"""

def getPSExtExecPremRate(ins):
    port = ins.FundPortfolio()
    if port:
        return port.AdditionalInfo().PSExtExecPremRate() 
    else:
        return ''
    
def getPSClientCallAcc(ins):
    port = ins.FundPortfolio()
    if port:
        links = port.MemberLinks() 
        if links:
            owner = links[0].OwnerPortfolio()
            if owner:
                return owner.AdditionalInfo().PSClientCallAcc()
            else:
                return ''
        else:
            return ''
    else:
        return ''
    
def getPSMarginFactor(ins):
    port = ins.FundPortfolio()
    if port:
        links = port.MemberLinks() 
        if links:
            owner = links[0].OwnerPortfolio()
            if owner:
                return owner.AdditionalInfo().PSMarginFactor()
            else:
                return ''
        else:
            return ''
    else:
        return ''

def getPSONPremAsk(ins):
    index = ins.AdditionalInfo().PSONPremIndex()
    if index:
        for p in index.Prices():
            if p.Market().Name() == 'SPOT':
                return str(p.Ask())
        return ''
    else:
        return ''

def getPSONPremBid(ins):
    index = ins.AdditionalInfo().PSONPremIndex()
    if index:
        for p in index.Prices():
            if p.Market().Name() == 'SPOT':
                return str(p.Bid())
        return ''
    else:
        return ''
