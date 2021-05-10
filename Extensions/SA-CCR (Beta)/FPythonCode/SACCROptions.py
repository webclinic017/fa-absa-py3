
import acm
import SACCRParameters
import SACCRTools

#------------------------------------------------------------------------------
def SACCRIsOption( object ):
    instrument = object if object.IsKindOf( acm.FInstrument ) else object.Instrument()
    
    if instrument.IsKindOf( acm.FOption ):
        if instrument.ExerciseType() in ["European", "Bermudan", "American"]:
            if not instrument.IsQuanto():
                return True
    elif instrument.IsKindOf( acm.FCap ) or instrument.IsKindOf( acm.FFloor ):
        return True
                
    return False

#------------------------------------------------------------------------------
def SACCRIsCallOption( option ):
    isCallOption = False
    
    if option.IsKindOf( acm.FOption ):
        isCallOption = option.OptionTypeIsCall()
    elif option.IsKindOf( acm.FCashFlow ) and option.CashFlowType() == "Caplet":
        isCallOption = True

    return isCallOption

#------------------------------------------------------------------------------
def SACCRSupervisoryDeltaAdjustmentOption( option, positionQuantity, strikePrices, forwardPrices ):
    timeToLatestExercise, strikePrice, forwardPrice = GetLatestExerciseData( option, strikePrices, forwardPrices )

    sigma = GetVolatilityFactor( option )

    d = ( acm.Math.Ln( forwardPrice / strikePrice) + 0.5 * sigma * sigma * timeToLatestExercise) / ( sigma * acm.Math.Sqrt( timeToLatestExercise ) )

    if SACCRIsCallOption( option ):
        return normcdf( d ) if positionQuantity > 0 else -normcdf( d )
    else:
        return -normcdf( -d ) if positionQuantity > 0 else normcdf( -d )

#------------------------------------------------------------------------------
def GetLatestExerciseData( option, strikePrices, forwardPrices ):    
    strikePrices = strikePrices.SortByProperty( "DateTime", False )
    forwardPrices = forwardPrices.SortByProperty( "DateTime", False )
    
    price = float( forwardPrices.First() )
    strike = float( strikePrices.First() )
    
    latestExercise = option.SACCRLatestExercise()
    
    return latestExercise, strike, price

#------------------------------------------------------------------------------
def GetVolatilityFactor( option ):
    instrument = option if option.IsKindOf( acm.FInstrument ) else option.Instrument()
    assetClass = instrument.SACCRAssetClass()
    
    return SACCRParameters.GetOptionVolatility( assetClass, SACCRTools.SACCRSubclass( instrument, assetClass ) )

#------------------------------------------------------------------------------
def normcdf( x ):
    f = acm.GetFunction( 'normalPercentileForStandardDeviations', 1 )
    return f(x)
    
