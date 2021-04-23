import acm
    
def CreateBuckets(validSpreadCurve):
    buckets = acm.FArray()
    for point in validSpreadCurve.Points():
        bucketDef = acm.FFixedDateTimeBucketDefinition()
        date = point.ActualDate()
        bucketDef.FixedDate( date )
        bucketDef.DiscardIfExpired( True )
        if(point.Instrument()):
            bucketDef.Name(point.Name())
        elif(not point.Date()):
            period = point.DatePeriod()
            bucketDef.Name(acm.Time().DatePeriodToString(period))
        buckets.Add(bucketDef)
    if buckets.Size():
        return buckets;
    else:
        return None


yieldCurveTypeEnum = acm.GetDomain('enum(IrType)')
q = acm.CreateFASQLQuery(acm.FYieldCurve, 'AND')
yieldCurveType = q.AddOpNode('OR')
yieldCurveType.AddAttrNode('Type', 'EQUAL', yieldCurveTypeEnum.Enumeration('Spread'))
yieldCurveType.AddAttrNode('Type', 'EQUAL', yieldCurveTypeEnum.Enumeration('Attribute Spread'))
validSpreadCurves = q.Select()
ael_variables = [
    ['Base Value', 'Base Value', 'string', acm.GetDomain('EnumRiskBaseCalculation').Enumerators(), None, 1, 0, 'Determines if Theoretical TPL or Theoretical Value (default) is used as the base for curve shifts. Different results can be arrived at if the ThTPL column includes Cash values sensitive to curves (for example via Exact FX conversions).', None, 1],
    ['Yield Curve', 'Yield Curve', 'FYieldCurve', validSpreadCurves, None, 1, 0, 'The attribute spread curve that will be shifted in buckets.', None, 1]
    ]
    
def ael_custom_label( parameters, dictExtra ):
    label = parameters.At('Yield Curve').Name()
    if parameters.At('Base Value'):
        label += ", Including Cash"
    return label

def ael_main_ex(parameters, dictExtra):
    validSpreadCurve = parameters['Yield Curve']
    baseValue = parameters['Base Value']
    
    buckets = CreateBuckets(validSpreadCurve)
    if not buckets:
        return 0

    resultVector = []
    
    timeBuckets = acm.Time.CreateTimeBucketsFromDefinitions(0, buckets, None, 0, True, False, False, False, False)
    for idx, bucket in enumerate(timeBuckets):
        params = acm.FNamedParameters()
        if idx == 0:
            params.AddParameter('baseValueChoice', baseValue)
            params.AddParameter('buckets', timeBuckets)
            params.AddParameter('yieldCurve', validSpreadCurve)
        params.Name(bucket.Name())
        params.UniqueTag(bucket.Spec())
        resultVector.append(params)
    return resultVector

    

