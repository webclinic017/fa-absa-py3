
import acm
import SpanADS
from collections import namedtuple

class SpanParametersGenerator(object):
       
    def __init__(self, dataProvider, *args):
        self.methodTuple = namedtuple('methodTuple', 'method start end')
        self.dataProviderArgs = args
        self.spanParameters = acm.FSpanParameters()
        self.dataProvider = dataProvider
        self.methodNames = {'CombinedCommodity' : [self.methodTuple('AddCombinedCommodity', 1, 2), self.methodTuple('AddShortOptionMinimumCharge', 2, 4)], 
                            'Instrument'        : [self.methodTuple('AddInstrument', 1, 10), self.methodTuple('AddRiskArray', 11, 27)], 
                            'InterCommodity'    : [self.methodTuple('AddInterCommodityCreditsRule', 1, -1)],
                            'InterMonth'        : [self.methodTuple('AddIntraCommodityPriority', 1, -1)],
                            'SpotMonth'         : [self.methodTuple('AddSpotMonthCharge', 1, -1)],
                            'Tiers'             : [self.methodTuple('AddTier', 1, -1)]
                            }
        
       
    def getSpanParameters(self):
        for k in sorted(self.methodNames):
            self.addData(k)
        return self.spanParameters
        
            
    def checkEntities(self, inputs, dataStr):
        if dataStr == 'Instrument':
            insId = SpanADS.getAdsInstance(inputs)
            inputs[0] = insId # overwrite instrument descriptor with Oid
            return inputs
        else:
            return inputs
            
    def addData(self, dataStr):
        inputList = self.dataProvider(dataStr)[0]
        methods = self.methodNames[dataStr]
        for inputs in inputList:
            inputs = self.checkEntities(inputs, dataStr)
            if dataStr == 'Instrument' and not isinstance(inputs[0], (int, int)):
                acm.Log('No match in ADS for instrument %s, no data added.' % inputs[0])
                continue
            for methodName in methods:
                methodToCall = getattr(self.spanParameters, methodName.method)
                methodArguments = [inputs[0]] + inputs[methodName.start:methodName.end]
                if methodName.method == 'AddRiskArray':
                    methodArguments = [inputs[0]]+ [inputs[methodName.start:methodName.end]]
                methodToCall(*methodArguments)
