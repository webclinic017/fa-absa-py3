import acm
import FRTBIMAHierarchy, FVaRFileParsing

def RiskFactorRiskClass(riskFactorInstance):
    return riskFactorInstance.RiskFactorCollection().AdditionalInfo().FRTB_IMA_Risk_Class()

def RiskFactorLiquidityHorizon(riskFactorInstance, imaHierarchy):
    riskClass = RiskFactorRiskClass(riskFactorInstance)
    riskFactorCategory = riskFactorInstance.AdditionalInfo().FRTB_IMA_Category()
    return imaHierarchy.FRTBLiquidityHorizon(riskClass, riskFactorCategory)

def RiskFactorIsPartOfReducedSet(riskFactorInstance):
    riskFactorIsPartOfReducedSet = True
    if acm.RiskFactor.RiskFactorPropertyAdditionalInfoSpecification(riskFactorInstance, 'Include In Reduced'):
        riskFactorIsPartOfReducedSet = riskFactorInstance.AdditionalInfo().Include_In_Reduced()
    return riskFactorIsPartOfReducedSet

def RiskFactorIsModellable(riskFactorInstance):
    riskFactorIsModellable = True
    if acm.RiskFactor.RiskFactorPropertyAdditionalInfoSpecification(riskFactorInstance, 'Modellable'):
        riskFactorIsModellable = riskFactorInstance.AdditionalInfo().Modellable()
    return riskFactorIsModellable

def StressedCapitalAddOnPerRiskFactorScenario(stressedCapitalAddOnPerRiskFactorParameters):
    commonParameters = stressedCapitalAddOnPerRiskFactorParameters[0]
    
    nonModellableRiskFactorsPerId = {}
    for collection in commonParameters.Parameter('riskFactorSetup').RiskFactorCollections():
        for instance in collection.RiskFactorInstances():
            if not RiskFactorIsModellable(instance):
                nonModellableRiskFactorsPerId[acm.RiskFactor.RiskFactorExternalId(instance)] = instance

    fileData = FVaRFileParsing.scenario_file_data(commonParameters.Parameter('scenarioFile'))

    absoluteShiftsPerInstance = {}
    relativeShiftsPerInstance = {}
    riskFactorInstances = []
    for namedParameter in stressedCapitalAddOnPerRiskFactorParameters:
        key = namedParameter.Name()
        instance = nonModellableRiskFactorsPerId.get(key)
        if instance:
            absoluteShiftsPerInstance[instance] = fileData.AbsoluteShiftsRowData(key).Slice(0, 1).ColumnValues()
            relativeShiftsPerInstance[instance] = fileData.RelativeShiftsRowData(key).Slice(0, 1).ColumnValues()
            riskFactorInstances.append(instance)

    scenarioBuilder = acm.FScenarioBuilder()
    scenario = scenarioBuilder.CreateScenario()
    dimension = scenarioBuilder.CreateScenarioDimension(scenario)

    riskFactorCreatorCache = acm.RiskFactor.CreatorCache()
    dateToday = acm.Time().DateToday()
    counter = 0
    numberOfInstances = len(absoluteShiftsPerInstance)
    for instance in riskFactorInstances:
        relativeShifts = [1.0] * numberOfInstances
        relativeShifts[counter] = relativeShiftsPerInstance[instance]
        absoluteShifts = [0.0] * numberOfInstances
        absoluteShifts[counter] = absoluteShiftsPerInstance[instance]
        externalId = acm.RiskFactor.RiskFactorExternalId(instance)
        riskFactor = acm.RiskFactor.RiskFactorFromRiskFactorInstance(instance, externalId, riskFactorCreatorCache, dateToday)
        scenarioBuilder.CreateRiskFactorScenarioMember(dimension, riskFactor, relativeShifts, absoluteShifts)
        counter += 1    
    return scenario
