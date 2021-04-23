import acm
from at_logging import getLogger

LOGGER = getLogger(__name__)

def getPortfolios():
    return acm.FPhysicalPortfolio.Select('')

ael_variables = [['portfolios', 'Portfolios', 'FPhysicalPortfolio', getPortfolios, None, 1, 1]]

def ael_main(ael_dict):
    collection = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection() 
    portfolios = ael_dict["portfolios"]
    for portfolio in portfolios:
        try:
            tpl = portfolio.Calculation().TotalProfitLoss(collection, acm.Time().SmallDate(), acm.Time().DateNow(), 'ZAR').Number()
            portfolio.AdditionalInfo().YesterdayEODTPL(tpl)
            portfolio.AdditionalInfo().YesterdayEODTPLDate(acm.Time().DateNow())
            portfolio.Commit()
            LOGGER.info('Portfolio %s YesterdayEODTPL add info updated to %d' %(portfolio.Name(), tpl))
            LOGGER.info('Portfolio %s YesterdayEODTPLDate add info updated to %s' %(portfolio.Name(), str(acm.Time().DateNow())))
        except Exception as e:
            LOGGER.error('Error while calculating and/or saving TPL for portfolio %s. Erros log: %s' %(portfolio.Name(), e))
