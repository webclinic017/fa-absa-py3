import acm



def getHedgeInstrumentForPortfolio(portfolioName, underlyingName):
    return acm.FInstrument['ZAR/ALSI']


def portfolioHedgeAlternatives(portfolioName, underlyingName, defaultInstrument):
    hedgeInstrument = getHedgeInstrumentForPortfolio(portfolioName, underlyingName)
    if hedgeInstrument:
        return hedgeInstrument
    else:
        return defaultInstrument

