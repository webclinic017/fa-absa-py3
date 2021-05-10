
def calculateVegaStrikeBucketsForRow(volatilityInformations, vegaStrikeBucketInfo):
    if (0 == len(volatilityInformations)):
        return False

    for volatilityInformation in volatilityInformations:
        if ('Absolute' != volatilityInformation.StrikeType()):
            return False

    if (vegaStrikeBucketInfo.Parameter("groupingSensitive")) and ('Absolute' != vegaStrikeBucketInfo.Parameter("strikeType")):
        volatilityStructure = volatilityInformations[0].VolatilityStructure()
        return (1 == len(volatilityInformations)) and (None != volatilityStructure) and (None != volatilityStructure.ReferenceInstrument())

    return True
