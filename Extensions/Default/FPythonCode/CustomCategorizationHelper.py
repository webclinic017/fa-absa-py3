
import acm
USER_MODULE_EXISTS = False
try:
    import FixingCategorizationMapping
    USER_MODULE_EXISTS = True
except:
    pass

def FixingCategorization(resetType, legCategory):
    if USER_MODULE_EXISTS and hasattr(FixingCategorizationMapping, "FixingCategorization"):
        return FixingCategorizationMapping.FixingCategorization(resetType, legCategory)
    else:
        return None

def CreateFixingReferenceInstrumentAndTradesObject(leg, resetType):
    insPortfolioReference = leg.Instrument().FundPortfolio()
    legCategory = leg.CategoryChlItem().Name()
    fixingReference = None
    
    if resetType == "Nominal Scaling":
        fixingReference = leg.IndexRef()
    if resetType == "Return":
        fixingReference = leg.FloatRateReference()
    if resetType == "Dividend Scaling":
        fixingReference = leg.FloatRateReference()
    if resetType == "Spread":
        fixingReference = leg.IndexRef()
            
    if fixingReference:
        builder = acm.Risk.CreateSingleInstrumentAndTradesBuilder(insPortfolioReference, fixingReference)
        return builder.GetTargetInstrumentAndTrades()
    else:
        return acm.Risk.CreatePortfolioInstrumentAndTrades(insPortfolioReference)
    
