
import acm

#----------------------------------------------------------------------------   
def GetClientSpreadInstrumentFromPrfSwap(prfSwap):
    clientSpread = None
    if prfSwap.InsType() == "Portfolio Swap":
        dpLinks = prfSwap.DealPackageInstrumentLinks()
        if dpLinks and dpLinks.Size() == 1:
            insPackage = dpLinks.At(0).InstrumentPackage()
            clientSpread = insPackage.InstrumentAt("clientSpreadIndex")
        if not clientSpread:
            raise Exception("No Portfolio Swap Deal Package")
    return clientSpread
#----------------------------------------------------------------------------    
