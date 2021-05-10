import acm

errorFunction = acm.GetFunction('throwError', 1)

def ProfitAndLossExplainPositionKey(instrumentAndTrades):
    portfolio = instrumentAndTrades.Portfolio()
    instrument = instrumentAndTrades.SingleInstrumentOrSingleTrade()
    positionKey = str(portfolio.ClassName()) + '|' + portfolio.Name()
    if instrument:
        positionKey += '|' + instrument.Name()
    return positionKey
    
def ParseDenominatedValue(dvString):
    dvDomain = acm.GetDomain('denominatedvalue')
    return dvDomain.ParseValue(dvString)

def ProfitAndLossExplainGreekRepositoryValue(greekRepository, positionKey, riskFactorKey, greek):
    if greekRepository.HasKey(positionKey):
        positionRepository = greekRepository[positionKey]
        if positionRepository.HasKey(riskFactorKey):
            greeks = positionRepository[riskFactorKey]
            if greeks.HasKey(greek):
                return greeks[greek]
            else:
                errorFunction('Greek ' + greek + ' not found for ' + positionKey + ' in ' + riskFactorKey)
        else:
            return None
    return errorFunction('Position ' + positionKey + ' not found')
    
def ProfitAndLossExplainGreekRepository(date):
    filePath = acm.GetDefaultValueFromName(acm.GetDefaultContext(), 'FObject', 'profitAndLossExplainStoredGreekFilePath')
    filePath = filePath.replace('\n', '')
    fileName = 'ProfitAndLossExplainStoredGreeks' + '_' + date + '.dat'
    file = open(filePath + fileName, 'r')
    lines = file.readlines()
    greekRepository = acm.FDictionary()
    for line in lines:
        line = line[:-1]
        components = line.split(';')
        if len(components) > 2:
            positionKey = components[0]
            if not greekRepository.HasKey(positionKey):
                greekRepository[positionKey] = acm.FDictionary()
            riskFactorKey = components[1]
            greeks = acm.FDictionary()
            greeks['Delta'] = ParseDenominatedValue(components[2])
            if 4 == len(components):
                greeks['Gamma'] = ParseDenominatedValue(components[3])
            greekRepository[positionKey][riskFactorKey] = greeks
    file.close()
    return greekRepository
