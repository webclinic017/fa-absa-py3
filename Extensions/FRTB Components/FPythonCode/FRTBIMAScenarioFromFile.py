
import acm, FVaRFileParsing, FRTBIMAHierarchy, FRTBIMATools

falseTrue = ['False', 'True']

riskClassNames = FRTBIMAHierarchy.RiskClassNames()

ael_variables = [
['file', 'Scenario File', 'string', None, None, 1, 0, 'The name or path to an external scenario file. If no path is given, the path fallbacks to the FCS_RISK_DIR environment variable first and then the current working directory.'],
['startIndex', 'Column Start', 'int', None, None, 1, 0, 'The starting column used in the external scenario file.'],
['endIndex', 'Column End', 'int', None, None, 1, 0, 'The ending column used in the external scenario file.'],
['riskClass', 'Risk Class', 'string', riskClassNames, '', 1, 0, 'Only Risk Factors of this Risk Class will be shifted.'],
['riskFactorSetup', 'Risk Factor Setup', acm.FRiskFactorSetup, acm.FRiskFactorSetup.Select(''), '', 1, 0, 'The Risk Factor Setup, repository for the Risk Factors.'],
['hierarchy', 'Hierarchy', 'string', acm.FHierarchy.Select(''), '', 1, 0, 'The hierarchy containing liquidity horizon data.'],
['liquidityHorizon', 'Liquidity Horizon', 'int', [10, 20, 40, 60, 120], '', 1, 0, 'The liquidity horizon.'],
['reducedFactorSet', 'Reduced Factor Set', 'string', falseTrue, 'False', 1, 0, 'Work with the reduced factor set? If not checked, the full factor set will be used.']
]

def ael_main_ex(parameters, unused):
    fileData = FVaRFileParsing.scenario_file_data(parameters['file'])
    dateToday = acm.Time().DateNow()
    if not fileData:
        print ('No file found! ', file)
    else:
        riskFactorCreatorCache = acm.RiskFactor.CreatorCache()
        startIndex = parameters['startIndex']
        endIndex = parameters['endIndex']
        riskClass = parameters['riskClass']
        riskFactorSetup = parameters['riskFactorSetup']
        liquidityHorizon = parameters['liquidityHorizon']
        reducedFactorSet = falseTrue.index(parameters['reducedFactorSet'])
        if not startIndex or startIndex < 0:
            startIndex = 0
        if not endIndex or endIndex < 0:
            endIndex = 0
        
        if endIndex < startIndex:
            raise Exception('Column End < Column Start')

        imaHierarchy = FRTBIMAHierarchy.FRTBIMAHierarchy(parameters['hierarchy'], riskFactorSetup.Name())

        scenarioBuilder = acm.FScenarioBuilder()
        riskFactors = []
        for collection in riskFactorSetup.RiskFactorCollections():
            for riskFactorInstance in collection.RiskFactorInstances():
                externalId = acm.FSymbol(acm.RiskFactor.RiskFactorExternalId(riskFactorInstance))
                if fileData.HasKey(externalId):
                    riskFactorSpecificationClass = FRTBIMATools.RiskFactorRiskClass(riskFactorInstance)
                    if riskFactorSpecificationClass and (('Unconstrained' == riskClass) or (riskFactorSpecificationClass == riskClass)):
                        if FRTBIMATools.RiskFactorLiquidityHorizon(riskFactorInstance, imaHierarchy) >= liquidityHorizon:
                            if (not reducedFactorSet) or FRTBIMATools.RiskFactorIsPartOfReducedSet(riskFactorInstance):
                                if FRTBIMATools.RiskFactorIsModellable(riskFactorInstance):
                                    riskFactors.append(acm.RiskFactor.RiskFactorFromRiskFactorInstance(riskFactorInstance, externalId, riskFactorCreatorCache, dateToday))

        if len(riskFactors):
            scenario = scenarioBuilder.CreateScenario(riskFactors, fileData, startIndex, endIndex)
            print ('Created scenario for Risk Class: ' + riskClass + ', Liquidity Horizon: ' + str(liquidityHorizon) + ', resulting in ' +  str(len(riskFactors)) + ' risk factors.' )
        else:
            scenario = scenarioBuilder.CreateScenario()
            scenarioBuilder.CreateScenarioDimension(scenario)
            print ('Empty scenario created for Risk Class: ' + riskClass + ', Liquidity Horizon: ' + str(liquidityHorizon) + ', no risk factors.' )
            
    return scenario
