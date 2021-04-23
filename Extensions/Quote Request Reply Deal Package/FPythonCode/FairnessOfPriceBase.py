
import acm
import FairnessOfPriceCustomization

'''********************************************************************
* Fairness of price
********************************************************************'''  
def FairnessOfPriceString(quoteController, *args):
    def CreateStringFromDict(dict):
        dictString = ''
        if hasattr(dict, 'Keys'):
            for key in dict.Keys():
                value = dict[key]
                if hasattr(value, 'Name'):
                    value = value.Name()
                dictString += str(key) + ':' + str(value) + ', '
            return dictString[:-2]
        else:
            return 'FairnessOfPrice customization function must return an FDictionary'
       
    try:
        if hasattr(quoteController.ExtendedData(), 'FairnessOfPrice'):
            dict = FairnessOfPriceCustomization.FairnessOfPrice(quoteController)
            dictString = CreateStringFromDict(dict)
            quoteController.ExtendedData().FairnessOfPrice(dictString)
        else:
            print ("No FairnessOfPrice extended data exists.")
        return quoteController.ExtendedData()
    except Exception as e:
        print ('FairnessOfPriceString failed', e)
