import acm
from FairnessOfPriceTemplate import FairnessOfPriceTemplate
        
'''********************************************************************
* Return a dictionary with relevant fairness of price information. 
In order for this to work, the FExtensionAttribute
FQuoteController:qExtendedData = py("FairnessOfPriceBase", context).FairnessOfPriceString(object, object.QuoteRequestReply())
must be defined in the context
********************************************************************'''            
def FairnessOfPrice(quoteController):
    return FairnessOfPriceTemplate(quoteController)
