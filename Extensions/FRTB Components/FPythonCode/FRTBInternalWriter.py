import acm, FRTBTestCommon

class FRTBInternalWriter(FRTBTestCommon.FRTBTestCommonWriter):
    def addResult(self, posInfoID, columnID, calculationInfos):
        if calculationInfos:
            positionKey = self.m_positionKeyTable[posInfoID]
            columnIDInfo = columnID.split('|')
            riskClass = columnIDInfo[1]
            liquidityHorizon = int(columnIDInfo[0])
            self.m_resultDictionary.setdefault(positionKey, {})
            self.m_resultDictionary[positionKey].setdefault(riskClass, {})
            self.m_resultDictionary[positionKey][riskClass].setdefault(liquidityHorizon, {})
            for calculationInfo in calculationInfos:
                projectionCoordinates = calculationInfo.projectionCoordinates
                scenarioElement = projectionCoordinates[0]
                calculatedValue = calculationInfo.values
                self.m_resultDictionary[positionKey][riskClass][liquidityHorizon][scenarioElement] = calculatedValue
