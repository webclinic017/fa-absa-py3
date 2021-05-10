import acm, FRTBTestCommon

class FRTBPLWriter(FRTBTestCommon.FRTBTestCommonWriter):
    def addResult(self, posInfoID, columnID, calculationInfos):
        if calculationInfos:
            for calculationInfo in calculationInfos:
                positionKey = self.m_positionKeyTable[posInfoID]
                self.m_resultDictionary.setdefault(positionKey, {})
                self.m_resultDictionary[positionKey][columnID] = calculationInfo.values
