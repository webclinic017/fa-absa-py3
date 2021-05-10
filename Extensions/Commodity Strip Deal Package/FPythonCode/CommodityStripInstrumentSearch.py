
import acm
from CommodityStripSearchHook import CustomFindInstrument
import re

class StripInstrumentSearch:

    def __init__(self, tempDeal):
        self._tempDeal = tempDeal
    
        # Set the base query attributes we always want to set
        # underlying, currency etc
        self._noneNodes = []
        
        self._tempInstrument = self._tempDeal.Instruments().First()
        if hasattr(self._tempInstrument, 'DecoratedObject'):
            self._tempInstrument = self._tempInstrument.DecoratedObject()
        
        self._query = acm.CreateFASQLQuery(self._tempInstrument.Class(), 'AND')
        self._node = self._query.AddOpNode('AND')
        self._instruments = acm.FArray()

    def BuildQuery(self):

        for attribute in self._tempDeal.GetAttributes():
            queryMapping = self._tempDeal.GetAttributeMetaData(attribute, '_queryMapping')()
            if queryMapping:
                valueToMatch = self._tempDeal.GetAttribute(attribute)
                if valueToMatch is None:
                    self._noneNodes.append(queryMapping)
                else:
                    dbReference = queryMapping[0]
                    operator = queryMapping[1]
                    #Are we looking for the Name attribute...
                    if dbReference.split('.')[-1] == 'Name':
                        valueToMatch = valueToMatch.Name()
                        if operator == 'RE_LIKE_NOCASE':
                            valueToMatch = re.escape(valueToMatch)
                    elif self._tempDeal.GetAttributeMetaData(attribute, 'domain')().IsKindOf('FDateTimeDomain'):
                        valueToMatch = acm.Time.AsDate(valueToMatch)
                    
                    self._node.AddAttrNode(dbReference, operator, valueToMatch)

    def MatchesNone(self, ins, node):
        matchEntity = ins
        operator = node[1]
        for attribute in node[0].split('.'):
            matchEntity = getattr(matchEntity, attribute)()
            if hasattr(matchEntity, 'IsKindOf') and matchEntity.IsKindOf(acm.FCollection):
                matchEntity = None if matchEntity.IsEmpty() else matchEntity.First()
            if matchEntity is None:
                return True if operator in ('EQUAL', 'RE_LIKE_NOCASE') else False
        return False if operator in ('EQUAL', 'RE_LIKE_NOCASE') else True

    def Execute(self):
        allInstruments = self._query.Select()
        for ins in allInstruments:
            if ins != self._tempInstrument:
                noneMatch = True
                for noneNode in self._noneNodes:
                    if not self.MatchesNone(ins, noneNode):
                        noneMatch = False
                        break
                if noneMatch is True:
                    self._instruments.Add(ins)

    def Instruments(self):
        return self._instruments

def FindExistingInstrument(tempDeal):
    returnObj = CustomFindInstrument(tempDeal)
    if returnObj is None:
        #No custom instrument find hook, use default
        query = StripInstrumentSearch(tempDeal)
        query.BuildQuery()
        query.Execute()
        if query.Instruments().Size() > 0:
            returnObj = query.Instruments().First()
    else:
        if returnObj == tempDeal.TradeAt('Trade').Instrument():
            returnObj = None
            
    if returnObj:
        if not returnObj.IsInfant():
            returnObj = returnObj.StorageImage()
        if not returnObj.IsKindOf(acm.FBusinessLogicDecorator):
            returnObj = acm.FBusinessLogicDecorator.WrapObject(returnObj)
        return returnObj

    
