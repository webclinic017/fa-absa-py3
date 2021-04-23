
import acm

'''********************************************************************
* Template for fairness of price specification
********************************************************************''' 
def FairnessOfPriceTemplate(quoteController):
    fairnessOfPriceDict = acm.FDictionary()
    try:
        fairnessOfPriceDict.AtPut('theorPrice', quoteController.CreateDataSource('Price Theor').Get())
    except Exception as e:
        print (str(e))
    return fairnessOfPriceDict
