from __future__ import print_function
import acm, FRTBCreateRiskFactorSetupCommon
import importlib
importlib.reload(FRTBCreateRiskFactorSetupCommon)

ael_variables = [['Risk Factor Setup Name', 'Risk Factor Setup Name', 'string', None, None, 1, 0, 'The desired name of the Risk Factor Setup.']]

__saRiskClassName = 'FRTB SA Risk Class'
__saSubtypeName = 'FRTB SA Subtype'
__saBucketName = 'FRTB SA Bucket'

def ael_main(parameters):
    riskFactorSetupName = parameters['Risk Factor Setup Name']
    
    print ('---------------- Setup of FRTB SA Risk Factors "' + riskFactorSetupName + '" ----------------')

    riskClassChoiceList = acm.FChoiceList.Select01('name="' + __saRiskClassName + '" list="MASTER"', '')
    subtypeChoiceList = acm.FChoiceList.Select01('name="' + __saSubtypeName + '" list="MASTER"', '')
    bucketChoiceList = acm.FChoiceList.Select01('name="' + __saBucketName + '" list="MASTER"', '')

    if (not subtypeChoiceList) or (not riskClassChoiceList) or (not bucketChoiceList):
        errorMessage = 'Choice lists not found, run script "FRTBCreateSAHierarchyChoiceLists".'
        print (errorMessage)
        raise Exception(errorMessage)

    addInfoSpecDictionary = {}
    addInfoSpecDictionary[__saRiskClassName] = FRTBCreateRiskFactorSetupCommon.AddInfoSpecFromName(__saRiskClassName, 'RiskFactorCollection')
    addInfoSpecDictionary[__saSubtypeName] = FRTBCreateRiskFactorSetupCommon.AddInfoSpecFromName(__saSubtypeName, 'RiskFactorCollection')
    addInfoSpecDictionary[__saBucketName] = FRTBCreateRiskFactorSetupCommon.AddInfoSpecFromName(__saBucketName, 'RiskFactorInstance')

    addInfoSpecValueDictionary = {}
    addInfoSpecValueDictionary['Commodity'] = {__saRiskClassName:'Commodity'}
    addInfoSpecValueDictionary['Commodity Volatility'] = {__saRiskClassName:'Commodity'}
    addInfoSpecValueDictionary['Cross Currency Basis'] = {__saRiskClassName:'GIRR', __saSubtypeName:'Cross Currency Basis'}
    addInfoSpecValueDictionary['Cross Currency Basis Benchmark Price'] = {__saRiskClassName:'GIRR', __saSubtypeName:'Cross Currency Basis'}
    addInfoSpecValueDictionary['CSR (NS)'] = {__saRiskClassName:'CSR (NS)', __saSubtypeName:'CDS'}
    addInfoSpecValueDictionary['CSR (NS) (IS)'] = {__saRiskClassName:'CSR (NS)', __saSubtypeName:'Bond'}
    addInfoSpecValueDictionary['CSR (NS) (ZCS)'] = {__saRiskClassName:'CSR (NS)', __saSubtypeName:'Bond'}
    addInfoSpecValueDictionary['Equity'] = {__saRiskClassName:'Equity', __saSubtypeName:'Spot Price'}
    addInfoSpecValueDictionary['Equity Repo'] = {__saRiskClassName:'Equity', __saSubtypeName:'Repo Rate'}
    addInfoSpecValueDictionary['Equity Volatility'] = {__saRiskClassName:'Equity', __saSubtypeName:'Spot Price'}
    addInfoSpecValueDictionary['FX'] = {__saRiskClassName:'FX'}
    addInfoSpecValueDictionary['FX Volatility'] = {__saRiskClassName:'FX'}
    addInfoSpecValueDictionary['Interest Rate'] = {__saRiskClassName:'GIRR', __saSubtypeName:'Interest Rate'}
    addInfoSpecValueDictionary['Interest Rate Benchmark Price'] = {__saRiskClassName:'GIRR', __saSubtypeName:'Interest Rate'}
    addInfoSpecValueDictionary['Interest Rate Volatility'] = {__saRiskClassName:'GIRR', __saSubtypeName:'Interest Rate'}
    addInfoSpecValueDictionary['Inflation Benchmark Price'] = {__saRiskClassName:'GIRR', __saSubtypeName:'Inflation'}
    addInfoSpecValueDictionary['Inflation Rate'] = {__saRiskClassName:'GIRR', __saSubtypeName:'Inflation'}

    timeBucketsDictionary = {}
    timeBucketsDictionary[('Commodity', 'Time')] = FRTBCreateRiskFactorSetupCommon.TimeBucketsFromName(['0D', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '10Y', '15Y', '20Y', '30Y'], 'FRTB SA Commodity')

    timeBucketsDictionary[('Commodity Volatility', 'Time')] = FRTBCreateRiskFactorSetupCommon.TimeBucketsFromName(['6M', '1Y', '3Y', '5Y', '10Y'], 'FRTB SA Commodity Volatility')

    creditBuckets = FRTBCreateRiskFactorSetupCommon.TimeBucketsFromName(['6M', '1Y', '3Y', '5Y', '10Y'], 'FRTB SA CSR')
    timeBucketsDictionary[('CSR (NS)', 'Time')] = creditBuckets
    timeBucketsDictionary[('CSR (NS) (IS)', 'Time')] = creditBuckets
    timeBucketsDictionary[('CSR (NS) (ZCS)', 'Time')] = creditBuckets

    timeBucketsDictionary[('Equity Volatility', 'Time')] = FRTBCreateRiskFactorSetupCommon.TimeBucketsFromName(['6M', '1Y', '3Y', '5Y', '10Y'], 'FRTB SA Equity Volatility')

    timeBucketsDictionary[('FX Volatility', 'Time')] = FRTBCreateRiskFactorSetupCommon.TimeBucketsFromName(['6M', '1Y', '3Y', '5Y', '10Y'], 'FRTB SA FX Volatility')

    girrTimeBuckets = FRTBCreateRiskFactorSetupCommon.TimeBucketsFromName(['3M', '6M', '1Y', '2Y', '3Y', '5Y', '10Y', '15Y', '20Y', '30Y'], 'FRTB SA GIRR')

    timeBucketsDictionary[('Interest Rate', 'Time')] = girrTimeBuckets
    timeBucketsDictionary[('Interest Rate Benchmark Price', 'Time')] = girrTimeBuckets

    girrVolBuckets = FRTBCreateRiskFactorSetupCommon.TimeBucketsFromName(['6M', '1Y', '3Y', '5Y', '10Y'], 'FRTB SA GIRR Volatility')
    timeBucketsDictionary[('Interest Rate Volatility', 'Time')] = girrVolBuckets
    timeBucketsDictionary[('Interest Rate Volatility', 'Underlying Maturity')] = girrVolBuckets

    FRTBCreateRiskFactorSetupCommon.CreateRiskFactorSetup(riskFactorSetupName, addInfoSpecDictionary, timeBucketsDictionary, addInfoSpecValueDictionary)

    print ('---------------- Setup of FRTB SA Risk Factors "' + riskFactorSetupName + '" finished ----------------')
