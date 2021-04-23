from __future__ import print_function
import acm, time

__riskFactorCollections = {
    'Commodity':['Commodity', {'ValueUnit':'Unit'}, [['Commodity', 'Commodity', 'AdditionalInfo.Commodity'], ['Commodity', 'Grade', 'AdditionalInfo.Grade'], ['Commodity', 'Location', 'AdditionalInfo.Location'], ['Time', 'Time', None]]],
    'Commodity Volatility':['Volatility', {'ValueUnit':'Percent'}, [['Volatility Surface', 'Volatility', None], ['Time', 'Time', None]]],
    'Cross Currency Basis':['Zero Coupon', {'ZeroCouponRateType':'Yield','ValueUnit':'Percent','TotalOrTopSpread':'Total'}, [['Yield Curve', 'Yield Curve', None]]],
    'Cross Currency Basis Benchmark Price':['Benchmark Price', {'ValueUnit':'Percent'}, [['Benchmark Curve', 'Yield Curve', None]]],
    'CSR (NS)':['Par CDS Rate', {'DaycountMethod':'Act/360','CalcType':'Par CDS Rate','ValueUnit':'Percent','RateType':'Quarterly'}, [['Issuer', 'Issuer', None], ['Time', 'Time', None]]],
    'CSR (NS) (IS)':['Stored Instrument Spread', {'ValueUnit':'Percent'}, [['Instrument', 'Issuer', 'Issuer'], ['Time', 'Time', None]]],
    'CSR (NS) (ZCS)':['Zero Coupon', {'ZeroCouponRateType':'Yield','ValueUnit':'Percent','TotalOrTopSpread':'Top Spread'}, [['Yield Curve', 'Issuer', 'AdditionalInfo.Issuer'], ['Time', 'Time', None]]],
    'Equity':['Equity', {'ValueUnit':'Unit'}, [['Equity', 'Equity', None]]],
    'Equity Repo':['Equity Repo Rate', {'ZeroCouponRateType':'Yield','ValueUnit':'Percent','TotalOrTopSpread':'Total'}, [['Equity', 'Equity', None]]],
    'Equity Volatility':['Volatility', {'ValueUnit':'Percent'}, [['Volatility Surface', 'Volatility', None], ['Time', 'Time', None]]],
    'FX':['FX', {'ValueUnit':'Unit'}, [['BaseCurrency', 'Currency', None], ['TermCurrency', 'Term Currency', None]]],
    'FX Volatility':['Volatility', {'ValueUnit':'Percent'}, [['Volatility Surface', 'Volatility', None], ['Time', 'Time', None]]],
    'Interest Rate':['Zero Coupon', {'ZeroCouponRateType':'Yield','ValueUnit':'Percent','TotalOrTopSpread':'Total'}, [['Yield Curve', 'Yield Curve', None], ['Time', 'Time', None]]],
    'Interest Rate Benchmark Price':['Benchmark Price', {'ValueUnit':'Percent'}, [['Benchmark Curve', 'Yield Curve', None], ['Time', 'Time', None]]],
    'Interest Rate Volatility':['Volatility', {'ValueUnit':'Percent'}, [['Volatility Surface', 'Volatility', None], ['Time', 'Time', None], ['UnderlyingMaturity', 'Underlying Maturity', None]]],
    'Inflation Benchmark Price':['Inflation Benchmark Price', {'ValueUnit':'Percent'}, [['Inflation Curve', 'Yield Curve', None]]],
    'Inflation Rate':['Inflation Rate', {'ValueUnit':'Percent'}, [['Inflation Curve', 'Yield Curve', None]]]
}

def __TimeStamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def AddInfoSpecFromName(name, admClassName):
    addInfoSpec = acm.FAdditionalInfoSpec.Select01('name="' + name + '" recType="' + admClassName + '"', '')
    if not addInfoSpec:
        addInfoSpec = acm.FAdditionalInfoSpec()
        addInfoSpec.RecType = admClassName
        addInfoSpec.Name = name
        addInfoSpec.DataTypeGroup = 'RecordRef'
        addInfoSpec.DataTypeType = 32
        addInfoSpec.Description = name
        addInfoSpec.Commit()
    return addInfoSpec

def TimeBucketsFromName(datePeriods, name):
    storedTimeBuckets = acm.FStoredTimeBuckets.Select01('name="' + name + '"', '')
    if not storedTimeBuckets:
        print (__TimeStamp() + ' Creating time buckets "' + name + '"')
        buckets = []
        for datePeriod in datePeriods:
            bucket = acm.FDatePeriodTimeBucketDefinition()
            bucket.DatePeriod = datePeriod
            bucket.Name = datePeriod
            bucket.Adjust = True
            bucket.RelativeSpot = True
            buckets.append(bucket)
        config = acm.TimeBuckets.CreateTimeBucketsConfiguration(None, 0, 0)
        definition = acm.TimeBuckets.CreateTimeBucketsDefinition(0, buckets, False, False, False, False, False)
        defAndConfig = acm.TimeBuckets.CreateTimeBucketsDefinitionAndConfiguration(definition, config)
        timeBuckets = acm.TimeBuckets.CreateTimeBuckets(defAndConfig)
        storedTimeBuckets = acm.FStoredTimeBuckets()
        storedTimeBuckets.TimeBuckets = timeBuckets
        storedTimeBuckets.Name = name
        storedTimeBuckets.AutoUser = False
        storedTimeBuckets.User = None
        storedTimeBuckets.Commit()
    return storedTimeBuckets

def CreateRiskFactorSetup(riskFactorSetupName, addInfoSpecDictionary, timeBucketsDictionary, addInfoSpecValueDictionary):
    if acm.FRiskFactorSetup[riskFactorSetupName]:
        errorMessage = 'Risk Factor Setup ' + riskFactorSetupName + ' already exists'
        print (errorMessage)
        raise Exception(errorMessage)

    rfs = acm.FRiskFactorSetup()
    rfs.Name = riskFactorSetupName
    rfs.Commit()

    print (__TimeStamp())

    for addInfoSpecName in addInfoSpecDictionary:
        print (__TimeStamp() + ' Creating attribute "' + addInfoSpecName + '"')
        ps = acm.FRiskFactorPropertySpecification()
        ps.AdditionalInfoSpec = addInfoSpecDictionary[addInfoSpecName]
        ps.RiskFactorSetup = rfs
        ps.Commit()

    for collectionName in __riskFactorCollections:
        print (__TimeStamp())
        print (__TimeStamp() + ' Creating collection "' + collectionName + '"')

        collection = acm.FRiskFactorCollection()
        collection.RiskFactorSetup = rfs
        collection.DisplayName = collectionName

        collectionData = __riskFactorCollections[collectionName]
        collection.RiskFactorType = collectionData[0]
        collection.Commit()

        addInfoValueDictionary = addInfoSpecValueDictionary[collection.DisplayName()]
        for addInfoSpecName in addInfoValueDictionary:
            addInfoSpec = addInfoSpecDictionary[addInfoSpecName]
            addInfo = acm.FAdditionalInfo()
            addInfo.AddInf(addInfoSpec)
            addInfo.Parent(collection)
            addInfo.FieldValue(addInfoValueDictionary[addInfoSpecName])
            addInfo.Commit()

        for valueParameterKey in collectionData[1]:
            valueParameter = acm.FRiskFactorValueParameter()
            valueParameter.ParameterKey = valueParameterKey
            valueParameter.ParameterValue = collectionData[1][valueParameterKey]
            valueParameter.RiskFactorCollection = collection
            valueParameter.Commit()
            print (__TimeStamp() + '   Value parameter "' + valueParameter.ParameterKey() + '" -> "' + valueParameter.ParameterValue() + '"')

        for dimensionData in collectionData[2]:
            dimension = acm.FRiskFactorDimension()
            dimension.DimensionId = dimensionData[0]
            dimension.DisplayName = dimensionData[1]
            dimension.MethodChain = dimensionData[2]
            dimension.RiskFactorCollection = collection
            timeBucketsKey = (collection.DisplayName(), dimension.DisplayName())
            if timeBucketsKey in timeBucketsDictionary:
                dimension.CoordinatesSource(timeBucketsDictionary[timeBucketsKey])
            dimension.Commit()
            print (__TimeStamp() + '   Dimension "' + dimension.DisplayName() + '"')

    print (__TimeStamp())
