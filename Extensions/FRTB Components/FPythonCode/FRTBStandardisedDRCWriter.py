
import acm, FRTBTestCommon

simpleColumnIds = ['FRTB DRC Remaining Maturity', 'FRTB DRC JTD Scaling', 'FRTB DRC Is Long Exposure']

class FRTBStandardisedDRCWriter(FRTBTestCommon.FRTBTestCommonWriter):
    def __init__(self):
        super(FRTBStandardisedDRCWriter, self).__init__()
        
    def addColumn(self, info, ID):
        pass

    def addResult(self, posInfoID, columnID, calculationInfos):
        if calculationInfos:
            positionKey = self.m_positionKeyTable[posInfoID]

            self.m_resultDictionary.setdefault(positionKey, {})
            if columnID in simpleColumnIds:
                self.m_resultDictionary[positionKey][columnID] = calculationInfos[0].values
            else:
                self.m_resultDictionary[positionKey].setdefault(columnID, {})
                self.m_resultDictionary[positionKey][columnID] = {}

                for calculationInfo in calculationInfos:
                    projectionCoordinates = calculationInfo.projectionCoordinates
                    assert(len(projectionCoordinates) == 4)
                    seniority = projectionCoordinates[0]
                    issuerName = projectionCoordinates[1]
                    issuerType = projectionCoordinates[2]
                    issuerCreditQuality = projectionCoordinates[3]
                    calculatedValue = calculationInfo.values

                    self.m_resultDictionary[positionKey][columnID].setdefault(seniority, {})
                    self.m_resultDictionary[positionKey][columnID][seniority].setdefault(issuerName, {})
                    self.m_resultDictionary[positionKey][columnID][seniority][issuerName].setdefault(issuerType, {})
                    self.m_resultDictionary[positionKey][columnID][seniority][issuerName][issuerType].setdefault(issuerCreditQuality, {})
                    self.m_resultDictionary[positionKey][columnID][seniority][issuerName][issuerType][issuerCreditQuality] = calculatedValue
