""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FMarkToMarket.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FMarkToMarket - Module which executes the Mark-to-Market.

DESCRIPTION
    This is the start-script for the Mark-to-Market procedure. It mainly
    contains the parameter GUI. The script FMtMPerform then takes over the
    execution of the MtM procedure.
----------------------------------------------------------------------------"""


import acm
import FBDPCurrentContext

import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FBDPYieldCurveLib
importlib.reload(FBDPYieldCurveLib)


import FSelCurrDupletCustomDlg
importlib.reload(FSelCurrDupletCustomDlg)


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FMtMVariables')


qInstruments = FBDPGui.insertInstruments(generic=None)


qYieldCurves = FBDPGui.insertYieldCurves(includeYcTypes=(
        FBDPYieldCurveLib.CURVE_TYPES_SUPPORT_CALCULATE +
        FBDPYieldCurveLib.CURVE_TYPES_SUPPORT_CALIBRATE_SPREADS))


qVolBenchmarks = FBDPGui.insertInstruments(generic=None, showStrike=True)


def getRealtimePrices():
    try:
        return acm.UX(
        ).SessionManager().SessionPreferences().RealtimePrices()
    except:
        return 0

def setRealtimePrices(value):
    try:
        acm.UX(
        ).SessionManager().SessionPreferences().RealtimePrices(value)
    except:
        pass

def currDupletCustomDlg(shell, params):
    customDlg = FSelCurrDupletCustomDlg.SelectCurrDupletCustomDlg(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


cvInsType = sorted([s for s in
        acm.FEnumeration['enum(InsType)'].Enumerators()])
cvMtMMarket = sorted([mtmmkt.Name() for mtmmkt in acm.FMTMMarket.Select('')])
cvContext = sorted([ctx.Name() for ctx in acm.FContext.Select('')])
cvDecimals = [1, 2, 3, 4, 5, 6]
cvDate = [acm.Time.DateToday(), 'Today', 'Previous Banking Day']


def disable_variables(variables, enable=0, disabledTooltip=None):

    for i in variables:
        getattr(ael_variables, i).enable(enable, disabledTooltip)


def cbInstruments(index, fieldValues):

    disable_variables(('AddRelated',), len(fieldValues[index]) > 0,
            'Choose "Instrument(s)" to enable this field.')
    return fieldValues


def cbUseYesterday(index, fieldValues):
    disable_variables(('sourceMtmMarket',), fieldValues[index],
            'choose "useYesterday" to enable this field')
    return fieldValues


def cbCurrencies(index, fieldValues):
    disable_variables(('AllExceptCurrencies',), len(fieldValues[index]) > 0)
    return fieldValues


def cbVolBenchmarks(index, fieldValues):

    if ael_variables[index][0] == 'VolBenchmarks':
        disable_variables(('VolPrefix', 'ExcludeInsFromVS', 'VolBase',
                'VolSuffix', 'Context', 'CallPut', 'SaveVolAsPrice'),
                len(fieldValues[index]) > 0,
                ('Choose "Volatility Benchmark Instruments" to enable this '
                        'field.'))
        # Make context mandatory.
        ael_variables.Context[5] = (len(fieldValues[index]) > 0 and 1 or 0)
        if len(fieldValues[index]) == 0:
            disable_variables(('VolMarket',),
                    disabledTooltip=('Choose "Volatility Benchmark '
                            'Instruments" to enable this field.'))
        else:
            disable_variables(('VolMarket',),
                    fieldValues[ael_variables.SaveVolAsPrice.sequenceNumber],
                    ('Check "Save imp. vol. in price table" to enable this '
                            'field.'))
    return fieldValues


def cbSaveVolAsPrice(index, fieldValues):

    disable_variables(('VolMarket',), fieldValues[index],
            'Check "Save imp. vol. in price table" to enable this field.')
    # Make VolMarket mandatory.
    ael_variables.VolMarket[5] = fieldValues[index]
    return fieldValues


def cbVolSurfaces(index, fieldValues):

    disable_variables(('AllExceptVolsurf',), len(fieldValues[index]) > 0)
    return fieldValues


def cbYieldCurves(index, fieldValues):

    enableAllExceptYieldCurve = len(fieldValues[index]) > 0
    disable_variables(('AllExceptYieldcurve',), enableAllExceptYieldCurve)
    fieldValues = getattr(ael_variables, 'AllExceptYieldcurve').callback(
            fieldValues)
    return fieldValues


def cbAllExceptYieldcurve(index, fieldValues):

    if not getattr(ael_variables, 'AllExceptYieldcurve').isEnabled():
        fieldValues[getattr(ael_variables,
                'AllExceptYieldcurve').sequenceNumber] = 0
    isAllExceptYieldCurveSet = bool(int(fieldValues[getattr(
            ael_variables, 'AllExceptYieldcurve').sequenceNumber]))
    isRecalcYcInDepOrderCleared = not bool(int(fieldValues[getattr(
            ael_variables, 'RecalcYcInDepOrder').sequenceNumber]))
    enableRecalcAlsoDepYc = not (isAllExceptYieldCurveSet or
            isRecalcYcInDepOrderCleared)
    disable_variables(('RecalcAlsoDepYc',), enableRecalcAlsoDepYc)
    fieldValues = getattr(ael_variables, 'RecalcAlsoDepYc').callback(
            fieldValues)
    return fieldValues


def cbRecalcYcInDepOrder(index, fieldValues):

    isAllExceptYieldCurveSet = bool(int(fieldValues[getattr(
            ael_variables, 'AllExceptYieldcurve').sequenceNumber]))
    isRecalcYcInDepOrderCleared = not bool(int(fieldValues[getattr(
            ael_variables, 'RecalcYcInDepOrder').sequenceNumber]))
    enableRecalcAlsoDepYc = not (isAllExceptYieldCurveSet or
            isRecalcYcInDepOrderCleared)
    disable_variables(('RecalcAlsoDepYc',), enableRecalcAlsoDepYc)
    fieldValues = getattr(ael_variables, 'RecalcAlsoDepYc').callback(
            fieldValues)
    return fieldValues


def cbRecalcAlsoDepYc(index, fieldValues):

    if not getattr(ael_variables, 'RecalcAlsoDepYc').isEnabled():
        fieldValues[getattr(ael_variables,
                'RecalcAlsoDepYc').sequenceNumber] = 0
    return fieldValues


def cbPreferredMarkets(index, fieldValues):

    disable_variables(('ExcludeInstypesPM',), len(fieldValues[index]) > 0,
            'Choose "Preferred markets" to enable this field.')
    return fieldValues


def cbExportCredBalAAJ(index, fieldValues):

    isExportCredBalAAJSet = bool(int(fieldValues[getattr(ael_variables,
            'ExportCredBalAAJ').sequenceNumber]))
    disable_variables(('ExportPath',), isExportCredBalAAJSet)
    if not getattr(ael_variables, 'ExportPath').isEnabled():
        fieldValues[getattr(ael_variables, 'ExportPath').sequenceNumber] = ''
    return fieldValues

def cbBackDatedInsts(index, fieldValues):
    if int(fieldValues[index]) == 1:
        fieldValues[ael_variables.Date.sequenceNumber] = 'Previous Banking Day'
    disable_variables(('AddBenchmarks',
            'VolBenchmarks',
            'VolSurfaces',
            'YieldCurves',
            'RecalcYcInDepOrder',
            'RecalcAlsoDepYc',
            'ExportCredBalAAJ',
            'Date'
        ),
        int(fieldValues[index]) == 0,
        ''
    )

    return fieldValues

# ## Tool Tip


ttSelIns = ('Save MtM Prices for these instruments. (Currency instruments are '
        'not included here)')
ttMtMMarket = "MtM prices will be saved in this market."
ttAddRelated = ("Also save MtM Prices for related instruments (underlyings, "
       "combination members etc.)")
ttAddBenchmarks = 'Save MtM Prices for yield curve benchmark instruments'
ttPairsOfCurr = ('Save prices for these pairs of currencies.  For each pair '
        'curr1/curr2, save the price for instrument curr1 in the currency '
        'curr2')
ttExceptCurrencies = ("Prices for all currency pairs except the ones defined "
        "in the field above will be saved")
ttBidAndAsk = "Also save current bid and ask prices along with the MtM Price"
ttHighAndLow = "Also save current high and low prices"
ttLast = "Also save latest prices"
ttUseZeroIfMissingPrices = ("Use zero for prices that are missing, "
                            "or their value can not be calculated correctly")
ttSelBmIns = "Select benchmark instruments for the volatility structures"
ttVolBase = ("The generated volatility structures will be named "
        "<vol-Prefix>_<vol_base>_<vol_suffix> where volbase is either the "
        "name or external id of the underlying instrument")
ttVoPrefix = ("The generated volatility structures will be named "
        "<vol-Prefix>_<vol_base>_<vol_suffix> ")
ttVolSuffix = ("The generated volatility structures will be named "
        "<vol-Prefix>_<vol_base>_<vol_suffix> ")
ttContext = ("The volatility structures generated will be linked to the "
        "underlying instrument with a context link in the Context you define "
        "here")
ttCallPut = ("Create volatilities of type Benchmark Call/Put, instead of "
        "type Benchmark.")
ttVolStructures = ("These volatility structures will be recalculated and "
        "cleared from expired instruments.  No bench mark instruments will "
        "be added")
ttAEVolSurf = ("ALL volatility structures except the ones defined in the "
        "field above will be recalculated")
ttVolAsPrice = ("Implied volatilities will, apart from being stored in a vol. "
        "structure, also be saved in the price table")
ttVolMarket = "Market on which implied volatilities will be saved"
ttRecalcYC = "These yield curves will be recalculated and saved"
ttAllExceptYieldcurve = ('ALL yield curves except the ones defined above '
        'will be recalculated and saved')
ttRecalcYcInDepOrder = ('Recalculate selected yield curves in their '
        'dependency ordering.')
ttRecalcAlsoDepYc = ('Recalculate also curves that the selected curve(s) '
        'depend upon (even if not selected in the task). Such curves can '
        'be Base, Dependency, Member or Constituent curves in any number '
        'of hierarchy levels below the selected curves(s)')
ttExportCredBal = 'Export Credit Balance instruments\' AAJ files.'
ttExportPath = 'Export path'
ttZeroPrices = "Should a MtM price of 0.0 be saved or not?"
ttUseYesterday = ("Save yesterday's price as today's")
ttSourceMtMMarket = "MtM prices will be retrieved from this market."
ttDecimals = ("The MtM price will be rounded to this number of decimals. "
        "Empty field means no rounding.")
ttExclVolIns = ("Options with this pattern (regular expression) in the "
        "instrument id will be excluded from volatility structures maintained "
        "by the script.")
ttPrefMkt = ("List of Markets from where to fetch the MtM price as a "
        "complement to the normal Price Finding Rules. Example: {"
        "'None':['EUREX','LIFFE','XETRA'],"
        "'PriceFindRuleName':['LIFFE','XETRA']}")
ttExclInstPM = ("These instrument types will not use the Preferred Market "
        "structure to get MtM Prices")
ttSEQ = ("Enables the calculation of Structured Equity related data.  If "
         "enabled, it will run FSEQDataMaint script, which performs data "
         "maintenance for structured equities, such as updates of exotic "
         "events.")
ttOverrideP = "Whether the script should override an existing MtM price or not"
ttDate = "MtM Prices will be saved on this date"
ttBackDatedInsts = ("Only select the back dated instruments")
ttRemoveZeroVolatilities = ("If selected, volatility points will be deleted"
                        "(removed) from relevant surfaces if the calibrated "
                        "volatility result is zero for any such point.")
ttApplyFilter = ("If selected, add all new instruments selected by the "
                "volatility filter to the surface."
                "Do not remove any existing items. ")
ttRealTimePriceUpdate = ("Check this box if realtime prices should be"
                "turned off when executing your Mark To Market task")

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['Instruments',
                'Instruments',
                'FInstrument', None, qInstruments,
                None, 1, ttSelIns, cbInstruments, None],
        ['AddRelated',
                'Add related instruments',
                'int', [1, 0], 0,
                0, 0, ttAddRelated, None, None],
        ['AddBenchmarks',
                'Add benchmark instruments',
                'int', [1, 0], 0,
                0, 0, ttAddBenchmarks, None, None],
        ['BackDated',
                'Only back dated instruments',
                'int', [1, 0], 0,
                0, 0, ttBackDatedInsts, cbBackDatedInsts, None],
        ['DisableRealtimePrices',
                'Disable realtime updated prices',
                'bool', [0, 1], 0,
                1, 0, ttRealTimePriceUpdate, None, 1],
        ['MtmMarket',
                'MtM Market',
                'string', cvMtMMarket, FBDPGui.getMtMMarket(),
                2, 0, ttMtMMarket, None, None],
        ['Decimals',
                'Nbr of decimals in MtM Price',
                'string', cvDecimals, None,
                0, 0, ttDecimals, None, None],
        ['PairsOfCurr',
                'Pairs of currencies_Currencies',
                'string', [], None,
                0, 1, ttPairsOfCurr, cbCurrencies, None, currDupletCustomDlg],
        ['AllExceptCurrencies',
                'ALL EXCEPT list above_Currencies',
                'int', [1, 0], 0,
                0, 0, ttExceptCurrencies, None, None],
        ['VolBenchmarks',
                'Volatility Benchmark Instruments_Vol and yield',
                'FInstrument', None, qVolBenchmarks,
                None, 1, ttSelBmIns, cbVolBenchmarks, None],
        ['Context',
                'Link Volatility Structure in Context_Vol and yield',
                'string', cvContext, None,
                0, 0, ttContext, None, None],
        ['CallPut',
                'Benchmark Call/Put_Vol and yield',
                'int', [1, 0], 0,
                0, 0, ttCallPut, None, None],
        ['VolSurfaces',
                'Recalc also these Vol. Structures_Vol and yield',
                'FVolatilityStructure', None, FBDPGui.insertVolatilities(),
                0, 1, ttVolStructures, cbVolSurfaces, None],
        ['AllExceptVolsurf',
                'ALL EXCEPT list above_Vol and yield',
                'int', [1, 0], 0,
                0, 0, ttAEVolSurf, None, None],
        ['YieldCurves',
                'Recalc also these Yield Curves_Vol and yield',
                'FYieldCurve', None, qYieldCurves,
                0, 1, ttRecalcYC, cbYieldCurves, None],
        ['AllExceptYieldcurve',
                'ALL EXCEPT list above_Vol and yield',
                'int', [1, 0], 0,
                0, 0, ttAllExceptYieldcurve, cbAllExceptYieldcurve, None],
        ['RecalcYcInDepOrder',
                'Recalc Yield Curves in Dependency Order_Vol and yield',
                'int', [1, 0], 1,
                0, 0, ttRecalcYcInDepOrder, cbRecalcYcInDepOrder, None],
        ['RecalcAlsoDepYc',
                'Recalc Base/Dependency/Member/Constituent curves_Vol '\
                'and yield',
                'int', [1, 0], 0,
                0, 0, ttRecalcAlsoDepYc, cbRecalcAlsoDepYc, None],
        ['ZeroVolatilities',
                'Remove Zero Volatilities_Vol and yield',
                'int', [1, 0], 1,
                0, 0, ttRemoveZeroVolatilities, None, None],
        ['ApplyFilter',
                'ApplyFilter_Vol and yield',
                'int', [1, 0], 0,
                0, 0, ttApplyFilter, None, None],
        ['ExportCredBalAAJ',
                'Export Credit Balance instruments AAJ file_CVA',
                'int', [1, 0], 0,
                0, 0, ttExportCredBal, cbExportCredBalAAJ, None],
        ['ExportPath',
                'Export path_CVA',
                'string', None, None,
                0, 0, ttExportPath, None, None],
        ['Date',
                'Date_Advanced',
                'string', cvDate, None,
                1, 0, ttDate, None, None],
        ['SaveZeroPrices',
                'Save MtM-price even if zero_Advanced',
                'int', [1, 0], 0,
                0, 0, ttZeroPrices, None, None],
        ['UseYesterday',
                "Use price from yesterday_Advanced",
                'int', [1, 0], 0,
                0, 0, ttUseYesterday, cbUseYesterday, None],
        ['sourceMtmMarket',
                'Source MtM Market_Advanced',
                'string', cvMtMMarket, FBDPGui.getMtMMarket(),
                0, 0, ttSourceMtMMarket, None, None],
        ['SaveBidAndAsk',
                'Save bid and ask prices_Advanced',
                'int', [1, 0], 0,
                1, 0, ttBidAndAsk, None, None],
        ['SaveHighAndLow',
                'Save high and low prices_Advanced',
                'int', [1, 0], 0,
                1, 0, ttHighAndLow, None, None],
        ['SaveLast',
                'Save last prices_Advanced',
                'int', [1, 0], 0,
                1, 0, ttLast, None, None],
        ['UseZeroIfPricesMissing',
                'Use zero for erroneous prices_Advanced',
                'int', [1, 0], 1,
                1, 0, ttUseZeroIfMissingPrices, None, None],
        ['OverridePrice',
                'Override existing MtM-price_Advanced',
                'int', [1, 0], 0,
                0, 0, ttOverrideP, None, None],
        ['SaveSEQData',
                'Save SEQ data_Advanced',
                'int', [1, 0], 0,
                0, 0, ttSEQ, None, None],
        ['PreferredMarkets',
                'Preferred markets_Advanced',
                'string', None, None,
                0, 0, ttPrefMkt, cbPreferredMarkets, None],
        ['ExcludeInstypesPM',
                'Exclude instypes in PM_Advanced',
                'string', cvInsType, None,
                0, 0, ttExclInstPM, None, None],
        ['ExcludeInsFromVS',
                'Excl. ins. from vol. struct_Advanced',
                'string', None, None,
                0, 0, ttExclVolIns, None, None],
        ['SaveVolAsPrice',
                'Save imp. vol. in price table_Advanced',
                'int', [1, 0], 0,
                0, 0, ttVolAsPrice, cbSaveVolAsPrice, None],
        ['VolMarket',
                'Volatility market_Advanced',
                'string', cvMtMMarket, None,
                0, 0, ttVolMarket, None, 0],
        ['VolBase',
                'Vol. structure base id_Advanced',
                'string', ['Name', 'ExternalId1'], None,
                2, 0, ttVolBase, None, None],
        ['VolPrefix',
                'Vol. structure prefix_Advanced',
                'string', None, None,
                0, 0, ttVoPrefix, None, None],
        ['VolSuffix',
                'Vol. structure suffix_Advanced',
                'string', '_impvol', None,
                0, 0, ttVolSuffix, None, None]
)


def ael_main(execParam):

    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPWorld
    importlib.reload(FBDPWorld)
    import FBDPInstrument
    importlib.reload(FBDPInstrument)
    import FMtMUtil
    importlib.reload(FMtMUtil)
    import FMtMCalcVal
    importlib.reload(FMtMCalcVal)
    import FMtMSelInsCurr
    importlib.reload(FMtMSelInsCurr)
    import FMtMTask
    importlib.reload(FMtMTask)
    import FMtMPerform
    importlib.reload(FMtMPerform)

    execParam['ScriptName'] = 'Mark To Market'

    execParam['Instruments'] = FBDPCommon.convertEntityList(
            execParam['Instruments'], execParam)
    execParam['VolBenchmarks'] = FBDPCommon.convertEntityList(
            execParam['VolBenchmarks'], execParam)
    if execParam['VolBase'] == 'External ID 1':
        execParam['VolBase'] = 'ExternalId1'
    execParam['VolSurfaces'] = FBDPCommon.convertEntityList(
            execParam['VolSurfaces'], execParam)
    execParam['YieldCurves'] = FBDPCommon.convertEntityList(
            execParam['YieldCurves'], execParam)
    needRestore = False
    realTmUptP = getRealtimePrices()
    disableRealtimePrices = execParam.get('DisableRealtimePrices', 0)
    try:
        if disableRealtimePrices and realTmUptP:
            FBDPCurrentContext.Logme()(
            "Temporarily disabled realtime prices.")
            needRestore = True
            setRealtimePrices(False)
        FMtMPerform.perform_mtm(execParam)
    except Exception as e:
        FBDPCurrentContext.Logme()(
        'Exception when running FMarkToMarket: ' + str(e), 'ERROR')
    if needRestore:
        setRealtimePrices(realTmUptP)
        FBDPCurrentContext.Logme()(
            "Restored realtime prices.")
