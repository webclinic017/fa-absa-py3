
import acm
import math

def PriceRiskFactorComparatorCore(left, right, methods):

    for method in methods:
        lvalue = left.PerformWith( method, [] )
        rvalue = right.PerformWith( method, [] )
        if lvalue < rvalue:
            return -1
        if lvalue > rvalue:
            return 1
    return 0
    
def PriceRiskFactorComparator(left, right):
    return PriceRiskFactorComparatorCore(left, right, ["Name"])

def CommodityPriceRiskFactorComparator(left, right):
    return PriceRiskFactorComparatorCore(left, right, ["ExpiryDate"])

def AbsoluteShiftSizeCore( instrument ):
    shiftSize = instrument.AdditionalInfo().AbsoluteShiftSize()
    if shiftSize:
        shiftSize *= instrument.Quotation().MetricSpaceFactor()
        shiftSize *= instrument.Quotation().QuotationFactor()
    else:
        shiftSize = float('nan')
    return shiftSize
    
def AbsoluteShiftSize(instrument):
    shiftSize = float('nan')
    if hasattr( instrument.AdditionalInfo(), "AbsoluteShiftSize" ):
        return AbsoluteShiftSizeCore( instrument )
    return shiftSize


def TimeBucketsFromInstruments(instruments):
    if not instruments:
        return None
    bucketsDefinition =[]
    for instrument in instruments[:-1]:
        bucketDefinition = acm.FFixedDateTimeBucketDefinition()
        bucketDefinition.FixedDate( instrument.DeliveryDate( instrument.ExpiryDate() ) )
        bucketsDefinition.append(bucketDefinition)
    bucketsDefinition.append(acm.FRestTimeBucketDefinition())
    definition = acm.TimeBuckets().CreateTimeBucketsDefinition(0, bucketsDefinition, False, False, False, False, False)
    definitionAndConfiguration = acm.TimeBuckets().CreateTimeBucketsDefinitionAndConfiguration(definition)
    return acm.TimeBuckets().CreateTimeBuckets(definitionAndConfiguration)   
