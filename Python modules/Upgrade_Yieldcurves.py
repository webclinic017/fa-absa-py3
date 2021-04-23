# This python script template is provided by SunGard Front Arena in order to facilitate a scripted 
# upgrade of yield curves for PRIME 2011.2 (or later). Please refer to SPR 316459 for more 
# information on the changes in yield curve handling in PRIME 2011.2.
#
# Note that this script must be customized by each customer in order to select the correct set of
# yield curves and then perform the preferred set of actions on these yield curves.
#  
# The default layout of the script below will currently only do the following;
#
# 1. Select all yield curve objects (see "Main Script" at the end)
#
# 2. For each curve that meets the criteria in "ValidCurve" (currently the filters only removes all 
#    historical yield curves) the script will perform the following actions:
#
# * If the curve has estimation_type Boot Strap Alt and Use Benchmark Dates is selected 
#	=> Clear the Use Benchmark Dates setting
# * If the curve has benchmarks 
#	=> Delete all existing yield curve points and generate new benchmark yield curve points 
# * If the curve has yield curve points that has been updated
#	=> Calibrate the yield curve and commit new rate values to the ADM
#
# Note that it is strongly recommended to always run the script in test mode first and go through 
# the created log.
#
# Change log (any chnages made (by Front Arena staff) to the file saved as attachment in FAST 
# should be stated here):
#
# 2011-05-18: Intitial version saved in FAST (marlar01)
#

import acm

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------
# User Inputs:

# testMode is True if no changes to be committed - only set to False if CERTAIN that your changes are intended.
testMode = False

# Filtering. An empty dictionary means "everything"

# Only yield curve types that should be upgraded
# e.g. inputYieldCurveTypes = ["Benchmark", "Spread"]
filterYieldCurveTypes = []

# Only yield curves with the following bootstrap methods will be upgraded
# e.g. filterDefinedBootstrapMethods = ["Boot Strap", "Boot Strap Alt"]
filterDefinedBootstrapMethods = []

# Only yield curves with the following use benchmark settings will be upgraded
# e.g. filterUseBenchmarkDatesSettings = [True], or filterUseBenchmarkDatesSettings = [False]
#      or filterUseBenchmarkDatesSettings = [True, False] but this is just the same as filterUseBenchmarkDatesSettings = []
filterUseBenchmarkDatesSettings = []

# If you only want to upgrade curves with benchmark or without etc
# e.g. filterCurveHasBenchmarks = [True] ... etc
filterCurveHasBenchmarks = []

# True if you only want to upgrade real time updated curves, False if only non real time updated curves, otherwise empty
# e.g. filterRealTimeUpdatedCurves = [True] ... etc
filterRealTimeUpdatedCurves = []

# Only upgrade curves with the following Currencies, empty means all
# e.g. filterCurrencyNames = ["EUR", "CHF", "SEK"]
filterCurrencyNames = []

# Only upgrade following curves, empty means all
# e.g. filterCurveNames = ["EUR-SWAP"]
filterCurveNames = []

# Exclude the following curves from upgrade.
# (Has higher priority than the positive filters above.)
excludeCurveNames = ['ZAR-PRIME'] # ZAR-PRIME agreed with business not to upgrade, according to Anil.

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

# Constants and methods relating to what changes have happened to an upgraded curve -----------------------
class UpgradeChange:
    UntoggledUseBenchmarkDatesOnBootstrapAltCurve   = 1
    BenchmarkPointsGeneratedAndCalculated           = 2
    StorageCalcTypeUpdated                          = 3

reason = "Reason"
action = "Action"

def ChangeDescription( changeEnum ):
    changeDescription = {}
    changeDescription[reason] = ""
    changeDescription[action] = ""
    
    if UpgradeChange.UntoggledUseBenchmarkDatesOnBootstrapAltCurve == changeEnum:
        changeDescription[reason] = "'Use Benchmark Dates' was toggled and Solver input was set to 'Boot Strap Alt'."
        changeDescription[action] = "'Use Benchmark Dates' has been untoggled."
    elif UpgradeChange.BenchmarkPointsGeneratedAndCalculated == changeEnum:
        changeDescription[reason] = "The yield curve contains benchmarks."
        changeDescription[action] = "The yield curve points have been cleared and benchmark points have been generated."
    elif UpgradeChange.StorageCalcTypeUpdated == changeEnum:
        changeDescription[reason] = "The yield curve is of type Spread and has an incompatible pair of IpolRateType and StorageCalcType."
        changeDescription[action] = "StorageCalcType has been set to Spot Rate"
    else:
        changeDescription[reason] = "Unknown reason."
        changeDescription[action] = "Unknown action."
       
    
    return changeDescription
# ---------------------------------------------------------------------------------------------------------


# Helper functions ----------------------------------------------------------------------------------------

# This method, for the given curve, is intended to determine whether it is acceptable
# for new benchmark instrument points to be generated or not
def CurveIsBenchmarkPointCandidate( yieldCurve ):
    benchmarkSize = yieldCurve.Benchmarks().Size()
    if benchmarkSize > 0:
        return True
    return False
# ---------------------------------------------------------------------------------------------------------
    

# Changes -------------------------------------------------------------------------------------------------
# For each change that can be made, there should exist:
#    1. A Method that takes as parameters: the yield curve, a dictionary that will contain boolean values
#       indicating whether a change was made, and a dictionary containing boolean values indicating
#       whether the change was successful if it was attempted. This method should perform the change on
#       the yield curve, and it should fill the dictionaries, at a key defined in class UpdateChanges, with
#       boolean values flagging if a change was made and whether it was successful, as described above.
#    2. As implied above, there should be a unique integer member of class UpgradeChanges, that will be
#       used as a key as explained in part 1 above.
#    3. For each integer member of UpgradeChanges, the method ChangeDescription should return a dictionary
#       that, for the integer, gives a "Reason" and an "Action" 

# Change 1:
def UntoggledUseBenchmarkDatesOnBootstrapAltCurveIfNeeded( yieldCurve, changesDictionary, failuresDictionary ):
    failure = False
    changed = False
    
    if (yieldCurve.EstimationType() == "Boot Strap Alt") and (yieldCurve.UseBenchmarkDates()) :
        yieldCurve.UseBenchmarkDates( False )
        changed = True

    failuresDictionary[UpgradeChange.UntoggledUseBenchmarkDatesOnBootstrapAltCurve] = failure
    changesDictionary[UpgradeChange.UntoggledUseBenchmarkDatesOnBootstrapAltCurve] = changed
    
    
# Change 2: This method tries to generate new benchmark instrument points, then calculate the curve
def GenerateBenchmarkPointsAndCalculate( yieldCurve, changesDictionary, failuresDictionary ):
    failure = False
    changed = False
    
    if CurveIsBenchmarkPointCandidate( yieldCurve ):
        try:
            yieldCurve.GenerateAndLinkPointsFromBenchmarks()
            changed = True
        except:
            failure = True

        try:
            yieldCurve.Calculate()
            changed = True
        except:
            failure = True
            
    failuresDictionary[UpgradeChange.BenchmarkPointsGeneratedAndCalculated] = failure
    changesDictionary[UpgradeChange.BenchmarkPointsGeneratedAndCalculated] = changed


# Change 3: Prevent the "invalid properties set" dialog. (Hynek)
def UpdateStorageCalcType(yieldcurve, changesDictionary, failuresDictionary):
    failure = changed = False
    try:
        if (yieldcurve.Type() == 'Spread' and yieldcurve.StorageCalcType() == 'Par FRN Rate' and
                yieldcurve.IpolRateType() == 'Spot Rate'):
            yieldcurve.StorageCalcType('Spot Rate')
            changed = True
    except Exception:
        failure = True
    failuresDictionary[UpgradeChange.StorageCalcTypeUpdated] = failure
    changesDictionary[UpgradeChange.StorageCalcTypeUpdated] = changed

# ---------------------------------------------------------------------------------------------------------
    
    
# This method "upgrades" any curve. As a template, the suggestion is that any curve with
# estimation type "Boot Strap Alt" should have "Use Benchmark Dates" untoggled, and secondly,
# if a curve contains benchmarks, then all points should be cleared, and new points
# containing these benchmarks should be generated - this is done with the method
# GenerateBenchmarkPointsAndCalculate().
def UpgradeCurve( yieldCurve, changesDictionary, failuresDictionary ):
    # First suggested upgrade action
    UntoggledUseBenchmarkDatesOnBootstrapAltCurveIfNeeded( yieldCurve, changesDictionary, failuresDictionary )    
    
    # Second suggested upgrade action
    GenerateBenchmarkPointsAndCalculate( yieldCurve, changesDictionary, failuresDictionary )

    # Custom added upgrade action
    UpdateStorageCalcType(yieldCurve, changesDictionary, failuresDictionary)
    

# Commit the curve only if not in test mode
def CommitCurve( yieldCurve, clone ):
    if not testMode:
        try:
            yieldCurve.Apply( clone )
            yieldCurve.Commit()
        except:
            print(" "*4 + "Commit failed - please update curve '" + yieldCurve.Name() + "' manually.")


# Logging -------------------------------------------------------------------------------------------------
def LogIndividualChanges( yieldCurve, changeDictionary ):
    print("")
    print(" "*4 + "Change details for yield curve '" + yieldCurve.Name() + "':")
    i = 0
    for change in changeDictionary:
        if changeDictionary[change]:
            i = i + 1
            changeDetails = ChangeDescription(change)
            print("")
            print(" "*4 + "Change " + str(i) + ":")
            print(" "*4 + "Reason: " + changeDetails[reason])
            print(" "*4 + "Action: " + changeDetails[action])

def LogChanges( yieldCurve, changeDictionary, failureDictionary ):
    changed = False
    failed = False

    for change in changeDictionary:
        changed = (changed or changeDictionary[change])

    for failure in failureDictionary:
        failed = (failed or failureDictionary[failure])
         
    openingMessage = "Yield Curve '" + yieldCurve.Name() + "'"
    logIndividualChanges = False
    
    print("")
    print("-"*120)
    
    if failed:
        openingMessage = openingMessage + " requires upgrade but was not successful. Please open the Yield Curve Definition and upgrade manually."
    else:
        if changed:
            openingMessage = openingMessage + " met the user specified criteria for upgrade, changes were applicable and were made successfully."
            logIndividualChanges = True
        else:
            openingMessage = openingMessage + " met the user specified criteria for upgrade, but no changes were applicable."
        
    print(openingMessage)
    
    if logIndividualChanges:
        LogIndividualChanges( yieldCurve, changeDictionary )
# ---------------------------------------------------------------------------------------------------------


# Methods for filtering yield curves to those that the user wants to change -------------------------------
def ValidEntry( list, entry ):
    if 0 == len(list):
        return True
    elif entry in list:
        return True
    return False

def YieldCurveTypeValidity( yieldCurveType ):
    return ValidEntry( filterYieldCurveTypes, yieldCurveType )

def DefinedBootstrapMethodValidity( definedBootstrapMethod ):
    return ValidEntry( filterDefinedBootstrapMethods, definedBootstrapMethod )

def UseBenchmarkDatesSettingValidity( useBenchmarkDatesSetting ):
    return ValidEntry( filterUseBenchmarkDatesSettings, useBenchmarkDatesSetting )

def CurveHasBenchmarkValidity( curveHasBenchmark ):
    return ValidEntry( filterCurveHasBenchmarks, curveHasBenchmark )

def RealTimeUpdatedCurveValidity( realTimeUpdatedCurve ):
    return ValidEntry( filterRealTimeUpdatedCurves, realTimeUpdatedCurve )

def CurrencyNameValidity( currencyName ):
    return ValidEntry( filterCurrencyNames, currencyName )

def CurveNameValidity( curveName ):
    return ValidEntry( filterCurveNames, curveName ) and curveName not in excludeCurveNames


# This method determines if, given the user input criteria, whether a given yield curve
# is a candidate for upgrade
def ValidCurve( yieldCurve ):
    if yieldCurve.IsHistorical():
        return False
    if not YieldCurveTypeValidity( yieldCurve.Type() ):
        return False
    if not DefinedBootstrapMethodValidity( yieldCurve.EstimationType() ):
        return False
    if not UseBenchmarkDatesSettingValidity( yieldCurve.UseBenchmarkDates() ):
        return False
    if not CurveHasBenchmarkValidity( yieldCurve.Benchmarks().Size() > 0 ):
        return False
    if not RealTimeUpdatedCurveValidity( yieldCurve.RealTimeUpdated() ):
        return False
    if not CurrencyNameValidity( yieldCurve.Currency().Name() ):
        return False
    if not CurveNameValidity( yieldCurve.Name() ):
        return False
    return True
# ---------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------
# --------------------------------------------- Main Script -----------------------------------------------
# ---------------------------------------------------------------------------------------------------------






ael_variables = [
    ['firstRunTypes', 'Yield Curve Types for the first run', 'string', None, '', 1, 1, 'Yield Curve types to be upgraded first', None, 1],
    ['secondRunTypes', 'Yield Curve Types for the second run', 'string', None, '', 1, 1, 'Yield Curve types to be upgraded second', None, 1],
]
def ael_main(parameters):
    # Get hold of all yield curves in the database. Note that the Select statement below can be altered
    # in order to select a smaller set of yield curves, for example by using: 
    # yieldCurves = acm.FYieldCurve.Select("name like 'EUR-SWAP*'")
    
    yieldCurves = acm.FYieldCurve.Select("")

    if testMode:
        print("Running in test mode - changes will not be saved")

    print("Total Curves in selection: " + str(len(yieldCurves)))

    # Iterate through all curves and for each curve, if the curve meets the criteria specified
    # by method ValidCurve(), then upgrade the curve. Note that by "upgrade the curve" is meant
    # "perform on the curve what is specified in the method UpgradeCurve()"

    for yc_types in (parameters['firstRunTypes'], parameters['secondRunTypes']): # First benchmark curves are upgraded, then the rest.
        filterYieldCurveTypes[:] = list(yc_types) # Set the yield curve type filter.
        print(filterYieldCurveTypes)
        for yieldCurve in yieldCurves:
            if ValidCurve( yieldCurve ):
                changes = {}
                failures = {}
                clone = yieldCurve.Clone()
                UpgradeCurve( clone, changes, failures )
                CommitCurve( yieldCurve, clone )
                LogChanges( yieldCurve, changes, failures )

# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

