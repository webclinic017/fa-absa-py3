import acm

arrayFunc = acm.GetFunction('array', 1)
class ProfitAndLossExplainGreekWriter(object):
    def __init__(self, validRiskFactorColumnIDs, validTimeColumnID):
        self.output = []
        self.columnIDTable = {}
        self.positionKeyTable = {}
        self.positionInfoTable = {}
        self.validRiskFactorColumnIDs = validRiskFactorColumnIDs
        self.validTimeColumnID = validTimeColumnID

    def addColumn(self, info, ID):
        self.columnIDTable[ID] = info.columnID

    def addRootPosition(self, info, ID):
        pass

    def positionKey(self, info):
        if info.parentInfoID:
            positionKey = self.positionKey(self.positionInfoTable[info.parentInfoID]) + '|' + info.name
        else:
            positionKey = info.acmDomainName + '|' + info.name
        return positionKey

    def addPosition(self, info, ID):
        self.positionInfoTable[ID] = info
        self.positionKeyTable[ID] = self.positionKey(info)

    def addResult(self, posInfoID, storedSpecName, calculationInfos):
        if calculationInfos:
            columnID = self.columnIDTable[storedSpecName]
            keyString = self.positionKeyTable[posInfoID] + ';'
            
            if (columnID in self.validRiskFactorColumnIDs):
                for calculationInfo in calculationInfos:
                    key = calculationInfo.projectionCoordinates
                    greeks = calculationInfo.values
                    self.output.append(keyString + str(key))
                    for greek in arrayFunc(greeks):
                            self.output.append(';' + str(greek))
                    self.output.append('\n')
            elif self.validTimeColumnID == columnID:
                self.output.append(keyString + 'Time;' + str(arrayFunc(calculationInfos[0].values)[0]) + '\n')
