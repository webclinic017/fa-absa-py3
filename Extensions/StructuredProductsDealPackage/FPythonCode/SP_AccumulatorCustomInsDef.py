import acm


def SetUp(definitionSetUp):
    import SP_AccumulatorSetup
    SP_AccumulatorSetup.Setup(definitionSetUp)

def SetUserBlockedDefaultValues(accumulator):
    # Set default values that the user should not be allowed to change
    # These fields are hidden or disbled from the Custom Instrument UI.
    accumulator.Quotation('Per Contract')
    accumulator.PayType('Spot')
    accumulator.ExerciseType('Bermudan')
    accumulator.Digital(False)
    accumulator.StrikeQuotation(None)
    accumulator.Generic(True)
    accumulator.StrikeType('Absolute')

def SetUserBlockedExoticValues(accumulator):
    # Default values on the exotic record.
    barrierType = 'Up & Out' if accumulator.OptionTypeIsCall() else 'Down & Out'
    accumulator.Exotic().BarrierOptionType(barrierType)

def SetStrikeEqualUnderlying(accumulator):
    if accumulator.Underlying():
        calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        price = accumulator.Underlying().Calculation().MarketPrice(calcSpace).Value()
        if (price and price.Number() > 0.0):
            accumulator.StrikePrice(price.Number())

def SetDefaultIfMissing(accumulator):
    if accumulator.StartDate()is None or accumulator.StartDate() == '':
        accumulator.StartDate(acm.Time().DateToday())
    
    monitoring = accumulator.Exotic().BarrierMonitoring()
    if monitoring is None or monitoring not in ('Continuous', 'Discrete'):
        accumulator.Exotic().BarrierMonitoring('Continuous')
    
    if accumulator.Barrier() is None or accumulator.Barrier() == 0.0:
        accumulator.Barrier(accumulator.StrikePrice())

def SetAdditionalInfoFromDefaultValue(accumulator):
    default = acm.FAdditionalInfoSpec['AccumulatorLeverage'].DefaultValue()
    # Set leverage to 2 if no default value or if defuatl value is 0
    accumulator.AdditionalInfo().AccumulatorLeverage(default if default else 2.0)

def AccumulatorInstrumentDefaultHook(accumulator):
    # Set the filter criteria
    accumulator.AdditionalInfo().StructureType('Accumulator')

    SetAdditionalInfoFromDefaultValue(accumulator)

    SetUserBlockedDefaultValues(accumulator)

    # Make sure that the instrument is created with 
    # an exotic record
    accumulator.CreateExotic()
 
    SetUserBlockedExoticValues(accumulator)
    
    # Set Strike price equal to underlying price
    SetStrikeEqualUnderlying(accumulator)

    SetDefaultIfMissing(accumulator)

def SetUserBlockedFxDefaultValues(accumulator):

    # Make sure that the instrument is created with 
    # an exotic record
    accumulator.CreateExotic()

    # Set default values that the user should not be allowed to change
    # These fields are hidden or disbled from the Custom Instrument UI.
    storeAwayMonitoring = accumulator.Exotic().BarrierMonitoring()
    accumulator.Exotic().BaseType('Barrier')
    accumulator.Exotic().BarrierMonitoring(storeAwayMonitoring)

    if accumulator.OptionTypeIsCall():
        accumulator.Exotic().BarrierOptionType('Up & Out')
    else:
        accumulator.Exotic().BarrierOptionType('Down & Out')
    accumulator.ExerciseType('Bermudan')
    accumulator.Quotation('Per Contract')
    accumulator.PayType('Spot')
    accumulator.Generic(True)
    accumulator.Exotic().FxoRebate(0.0)

def SetFxStrikeEqualUnderlying(accumulator):
    if accumulator.Underlying():
        calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        if accumulator.ForeignCurrency() and accumulator.DomesticCurrency():
            price = accumulator.ForeignCurrency().Calculation().FXRate(calcSpace, accumulator.DomesticCurrency()).Value()
            if (price and price.Number() > 0.0):
                accumulator.StrikeDomesticPerForeign(price.Number())

def SetFxDefaultIfMissing(accumulator):
    if accumulator.StartDate()is None or accumulator.StartDate() == '':
        accumulator.StartDate(acm.Time().DateToday())
    
    monitoring = accumulator.Exotic().BarrierMonitoring()
    if monitoring is None or monitoring not in ('Continuous', 'Discrete'):
        accumulator.Exotic().BarrierMonitoring('Continuous')
    
    if accumulator.Barrier() is None or accumulator.Barrier() == 0.0:
        accumulator.Exotic().BarrierDomesticPerForeign(accumulator.StrikeDomesticPerForeign())

def FxAccumulatorInstrumentDefaultHook(accumulator):
    AccDecorator = acm.FBusinessLogicDecorator.WrapObject(accumulator)

    # Set the filter criteria
    AccDecorator.AdditionalInfo().StructureType('Accumulator')

    SetUserBlockedFxDefaultValues(AccDecorator)

    SetAdditionalInfoFromDefaultValue(AccDecorator)
    
    # Add strike and missing default values
    SetFxStrikeEqualUnderlying(AccDecorator)

    SetFxDefaultIfMissing(AccDecorator)

def DataMaint(instrument, dateToday, updateHistorical, updateResult):
    return ['Price Fixing']

