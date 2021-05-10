import acm
import FUxUtils, FVaRFileParsing, FRTBIMATools

ael_variables = [
['filename', 'Scenario File', 'FFileSelection', None, acm.FFileSelection(), 1, 1, '', None, 1],
['rfsetup', 'Risk Factor Setup', 'string', acm.FRiskFactorSetup.Select(''), None, 1, 0,]
]

def ael_main_ex(parameters, unused):
    scenarioFile = str( parameters['filename'].SelectedFile() )
    riskFactorSetup = acm.FRiskFactorSetup[ parameters['rfsetup'] ]

    nonModellableRiskFactorsIds = []
    for collection in riskFactorSetup.RiskFactorCollections():
        for instance in collection.RiskFactorInstances():
            if not FRTBIMATools.RiskFactorIsModellable(instance):
                nonModellableRiskFactorsIds.append(acm.RiskFactor.RiskFactorExternalId(instance))

    riskFactorIds = []
    for key in FVaRFileParsing.scenario_file_data(scenarioFile).Keys():
        if str(key) in nonModellableRiskFactorsIds:
            riskFactorIds.append(str(key))
    riskFactorIds.sort()

    resultVector = acm.FNamedParametersArray()
    for idx, riskFactorId in enumerate(riskFactorIds):
        params = acm.FNamedParameters()
        params.Name(riskFactorId)
        params.UniqueTag(riskFactorId)
        if 0 == idx:
            params.AddParameter('scenarioFile', scenarioFile)
            params.AddParameter('riskFactorSetup', riskFactorSetup)
        
        resultVector.Add(params)
    return resultVector

