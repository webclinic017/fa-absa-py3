import acm, FRTBTestCommon

isOptionColumnID = 'FRTB Is Option'

class FRTBStandardisedWriter(FRTBTestCommon.FRTBTestCommonWriter):
    def __init__(self):
        super(FRTBStandardisedWriter, self).__init__()
        self.m_resultIsOptionPerPosition = {}
        
    def addColumn(self, info, ID):
        pass

    def addResult(self, posInfoID, columnID, calculationInfos):
        if calculationInfos:
            positionKey = self.m_positionKeyTable[posInfoID]

            self.m_resultDictionary.setdefault(positionKey, {})
            if isOptionColumnID == columnID:
                self.m_resultDictionary[positionKey][columnID] = calculationInfos[0].values
            else:
                self.m_resultDictionary[positionKey].setdefault(columnID, {})
                self.m_resultDictionary[positionKey][columnID] = {}
                    
                for calculationInfo in calculationInfos:
                    projectionCoordinates = calculationInfo.projectionCoordinates
                    if len(projectionCoordinates) > 0:
                        riskFactorName = projectionCoordinates[0]

                        calculatedValue = calculationInfo.values

                        if len(projectionCoordinates) > 1: # multi-dimensional result
                            self.m_resultDictionary[positionKey][columnID].setdefault(riskFactorName, {})
                            self.m_resultDictionary[positionKey][columnID][riskFactorName][projectionCoordinates[1:]] = calculatedValue
                        else:
                            self.m_resultDictionary[positionKey][columnID][riskFactorName] = calculatedValue
