
import acm
from AGGREGATION_PARAMETERS import PARAMETERS
from FBDPCurrentContext import Logme

class GENERIC_HELPERS():
    def acmOidToLinstInts(self, acmList):
        return [object.Oid() for object in acmList]

    def getMirrorTrades(self, trades):
        list = []
        for trade in trades:
            mirrorTrade = trade.TrueMirror()
            if mirrorTrade:
                list.append(mirrorTrade)
        return list

    def addToSummary(self, entity, action, number):
        try:
            keyValue = (entity, action)
            if keyValue in list(PARAMETERS.summaryDict.keys()):
                PARAMETERS.summaryDict[keyValue] = PARAMETERS.summaryDict[keyValue] + int(number)
            else:
                PARAMETERS.summaryDict[keyValue] = int(number)
        except Exception as e:
            Logme()('ERROR: Unable to action to summary: {}'.format(e), 'ERROR')

    def logSummry(self):
        Logme()('%-30s\t%-30s\t%-30s' %('Entity', 'Action', 'Number'))
        for entity, action in list(PARAMETERS.summaryDict.keys()):
            Logme()('%-30s\t%-30s\t%-30i' %(entity, action, PARAMETERS.summaryDict[(entity, action)]))

    def intToACMObjects(self, idList, acmObjectType):
        if acmObjectType == 'FInstrument':
            return [acm.FInstrument[id] for id in idList]
        if acmObjectType == 'FTrade':
            return [acm.FTrade[id] for id in idList]
