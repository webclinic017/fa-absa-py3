
import acm, FVaRFileParsing, FRTBIMATools

startDateEndDate = ['Start Date', 'End Date']
endDateValues = acm.FEnumeration['EnumPLEndDate'].Enumerators()

ael_variables = [
['Scenario File', 'Scenario File', 'string', None, None, 1, 0, 'The name or path to an external scenario file. If no path is given, the path fallbacks to the FCS_RISK_DIR environment variable first and then the current working directory.'],
['Scenario End Date', 'Scenario End Date', 'string', endDateValues, 'Now', 1, 0, 'The end date of the 1-day scenario.'],
['Scenario End Date Custom', 'Scenario End Date Custom', 'string', None, '', 0, 0, 'The custom end date of the 1-day scenario.'],
['Reference Date', 'Reference Date', 'string', startDateEndDate, 'End Date', 1, 0, 'The reference date used to generate the scenario.'],
['Calendar', 'Calendar', acm.FCalendar, acm.FCalendar.Select(''), '', 1, 0, 'The calendar used to calculate the scenario start and end date.'],
['Risk Factor Setup', 'Risk Factor Setup', acm.FRiskFactorSetup, acm.FRiskFactorSetup.Select(''), '', 1, 0, 'The Risk Factor Setup, repository for the Risk Factors.']
]

def startAndEndDate(scenarioEndDate, scenarioEndDateCustom, calendar):
    endDate = acm.Time.DateToday()
    if 'Yesterday' == scenarioEndDate:
        endDate = calendar.AdjustBankingDays(endDate, -1)
    elif 'Two Days Ago' == scenarioEndDate:
        endDate = calendar.AdjustBankingDays(endDate, -2)
    elif 'Custom Date' == scenarioEndDate:
        endDate = scenarioEndDateCustom
    startDate = calendar.AdjustBankingDays(endDate, -1)
    return startDate, endDate

def ael_main_ex(parameters, unused):
    fileData = FVaRFileParsing.scenario_file_data(parameters['Scenario File'])
    if not fileData:
        print ('No file found!', file)
    else:
        riskFactorSetup = parameters['Risk Factor Setup']
        riskFactorCreatorCache = acm.RiskFactor.CreatorCache()
        startDate, endDate = startAndEndDate(parameters['Scenario End Date'], parameters['Scenario End Date Custom'], parameters['Calendar'])
        scenarioIndex = fileData.Labels().IndexOfFirstEqual(acm.FSymbol(endDate)) + 1
        referenceDate = endDate if ('End Date' == parameters.get('Reference Date')) else startDate

        scenarioBuilder = acm.FScenarioBuilder()
        riskFactors = []
        for collection in riskFactorSetup.RiskFactorCollections():
            for riskFactorInstance in collection.RiskFactorInstances():
                externalId = acm.FSymbol(acm.RiskFactor.RiskFactorExternalId(riskFactorInstance))
                if fileData.HasKey(externalId):
                    riskFactors.append(acm.RiskFactor.RiskFactorFromRiskFactorInstance(riskFactorInstance, externalId, riskFactorCreatorCache, referenceDate))

        if len(riskFactors):
            scenario = scenarioBuilder.CreateScenario(riskFactors, fileData, scenarioIndex, scenarioIndex)
            print ('Created scenario with: ' +  str(len(riskFactors)) + ' risk factors.' )
        else:
            scenario = scenarioBuilder.CreateScenario()
            scenarioBuilder.CreateScenarioDimension(scenario)
            print ('Empty scenario created.' )
            
    return scenario
