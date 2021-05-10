
import acm

def FindValidationLevelPortfolios(prf):
    res = []
    if prf != None:
        if prf.AdditionalInfo().IsValidationLevel():
            res.append( prf )
        for links in prf.MemberLinks():
            res += FindValidationLevelPortfolios( links.OwnerPortfolio() )
    return res

def FindShortSellLimitCheckPortfolios(prf):
    res = []
    if prf != None:
        if prf.AdditionalInfo().ShortSellOffset():
            res.append( prf )
        for links in prf.MemberLinks():
            res += FindShortSellLimitCheckPortfolios( links.OwnerPortfolio() )
    return res

def FindShortSellOffsetPortfolios(prf):
    res = []
    if prf != None:
        if prf.AdditionalInfo().ShortSellOffset():
            res.append( prf.AdditionalInfo().ShortSellOffset() )
        if hasattr( prf, 'OwnerLinks' ):
            for links in prf.OwnerLinks():
                res += FindShortSellOffsetPortfolios( links.MemberPortfolio() )
    return res

def GetValidationLevelPortfolio(prf):
    return ( FindValidationLevelPortfolios( prf ) + [ prf ] ) [ 0 ] # If no match is found use input portfolio

def GetShortSellLimitCheckPortfolio(prf):
    return ( FindShortSellLimitCheckPortfolios( prf ) + [ None ] ) [ 0 ] # Make sure there is at least None to return

def GetShortSellOffsetPortfolio(prf):
    return ( FindShortSellOffsetPortfolios( prf ) + [ None ] ) [ 0 ] # Make sure there is at least None to return
    
