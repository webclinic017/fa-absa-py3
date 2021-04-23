""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FDeletePrices.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FDeletePrices.py - Delete Prices.

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import os


import acm


import FBDPGui
import importlib
importlib.reload(FBDPGui)


SCRIPT_NAME = 'Delete Prices'


DUMP_PREFIX = 'DeletePrices'
DUMP_SUFFIX = 'out'


cvDates = ['Never', 'Today', '-6m', '-1y']
dvDates = cvDates[0]


cvMtMMkt = [pt.Name() for pt in acm.FMTMMarket.Select('')]
dvMtMMkt = FBDPGui.getMtMMarket()


cvMktBkr = [pt.Name() for pt in acm.FParty.Select('') if
        pt.Type() in ('Market', 'Broker')]
dvMktBkr = ''


cvDumpPath = [FBDPGui.defaultLogDir()]
dvDumpPath = cvDumpPath[0]


def _handleDepFieldEnableAndCallBack(depFieldName, isToEnable, fieldValues):

    depField = getattr(ael_variables, depFieldName)
    depField.enable(int(isToEnable))
    if depFieldName in ('DateMtM', 'DateLast'):
        if not depField.isEnabled():
            fieldValues[depField.sequenceNumber] = ''
    if depField.hasCallback():
        fieldValues = depField.callback(fieldValues)
    return fieldValues


def _handleProtInsAndSavePricesEnable(fieldValues):

    isToDelPrcOnExpUntrdIns = bool(int(fieldValues[
            getattr(ael_variables, 'DropExpIns').sequenceNumber]))
    fieldValues = _handleDepFieldEnableAndCallBack('TradeOpenPeriod',
            isToDelPrcOnExpUntrdIns, fieldValues)
    isToDelSelPrc = bool(int(fieldValues[
            getattr(ael_variables, 'DelSelPrc').sequenceNumber]))
    isToEnableProtInsAndDumpPath = isToDelPrcOnExpUntrdIns or isToDelSelPrc
    fieldValues = _handleDepFieldEnableAndCallBack('Protected',
            isToEnableProtInsAndDumpPath, fieldValues)
    fieldValues = _handleDepFieldEnableAndCallBack('SavePrices',
            isToEnableProtInsAndDumpPath, fieldValues)
    return fieldValues


def cbDelPrcOnExpUntrdIns(index, fieldValues):

    fieldValues = _handleProtInsAndSavePricesEnable(fieldValues)
    return fieldValues


def cbDelSelPrc(index, fieldValues):

    depFieldNames = ('Instruments', 'KeepEndOfMonth', 'ClosedInstrumentsOnly')
    isToEnableDepFields = bool(int(fieldValues[index]))
    for depFieldName in depFieldNames:
        fieldValues = _handleDepFieldEnableAndCallBack(depFieldName,
                isToEnableDepFields, fieldValues)
    fieldValues = _handleProtInsAndSavePricesEnable(fieldValues)
    return fieldValues


def cbInstruments(index, fieldValues):

    depFieldNames = ('MtMMarkets', 'Markets')
    isToEnableDepFields = (bool(
            getattr(ael_variables, 'Instruments').isEnabled()) and bool(
            fieldValues[index]))
    for depFieldName in depFieldNames:
        fieldValues = _handleDepFieldEnableAndCallBack(depFieldName,
                isToEnableDepFields, fieldValues)
    return fieldValues


def cbMtMMkt(index, fieldValues):

    depFieldNames = ('DateMtM',)
    isToEnableDepFields = (bool(
            getattr(ael_variables, 'MtMMarkets').isEnabled()) and bool(
            fieldValues[index]))
    for depFieldName in depFieldNames:
        fieldValues = _handleDepFieldEnableAndCallBack(depFieldName,
                isToEnableDepFields, fieldValues)
    return fieldValues


def cbMktBkr(index, fieldValues):

    depFieldNames = ('DateLast',)
    isToEnableDepFields = (bool(
            getattr(ael_variables, 'Markets').isEnabled()) and bool(
            fieldValues[index]))
    for depFieldName in depFieldNames:
        fieldValues = _handleDepFieldEnableAndCallBack(depFieldName,
                isToEnableDepFields, fieldValues)
    return fieldValues


def cbSavePrices(index, fieldValues):

    if getattr(ael_variables, 'SavePrices').isEnabled():
        isToEnableDumpDirPathField = bool(int(fieldValues[index]))
    else:
        fieldValues[index] = 0
        isToEnableDumpDirPathField = False
    # work on dump path field
    dumpDirPathField = getattr(ael_variables, 'DumpDirPath')
    isDumpDirPathFieldEnabled = dumpDirPathField.isEnabled()
    if isDumpDirPathFieldEnabled and not isToEnableDumpDirPathField:
        # Currently enabled, and is to disable:
        # --> Disable and callback
        dumpDirPathField.enable(0)
        fieldValues = dumpDirPathField.callback(fieldValues)
    elif not isDumpDirPathFieldEnabled and isToEnableDumpDirPathField:
        # Currently disabled, and is to disable:
        # --> Enable, set field and callback
        dumpDirPathField.enable(1)
        if not fieldValues[dumpDirPathField.sequenceNumber]:
            fieldValues[dumpDirPathField.sequenceNumber] = dvDumpPath
        fieldValues = dumpDirPathField.callback(fieldValues)
    return fieldValues


def cbDumpDirPath(index, fieldValues):

    dumpDirPathField = getattr(ael_variables, 'DumpDirPath')
    if dumpDirPathField.isEnabled() and not fieldValues[index]:
        # Currently enabled, and has no value, disable SavePrice
        savePricesField = getattr(ael_variables, 'SavePrices')
        fieldValues[savePricesField.sequenceNumber] = 0
        fieldValues = savePricesField.callback(fieldValues)
    return fieldValues


## Tool Tip
ttDelPrcOnNonExistIns = ('All prices referencing removed instruments will be '
        'deleted. This will be done for latest and historical prices across '
        'all markets and currencies.')
ttDelPrcOnExpUntrdIns = ('All prices of expired untraded instruments will be '
        'deleted. Protected instruments are excluded. This will be done for '
        'latest and historical prices across all markets and currencies.')
ttDelSelPrc = ('Delete historical prices of selected instruments')
ttInstruments = ('Delete prices of the selected instruments')
ttTradeOpenPeriod = ('Only the prices of selected instruments which '
        'are untraded or with trade time < (today - Trade open period) '
        'will be deleted. Leave blank to indicate never traded')
ttMtMMkt = 'Prices on these MtM markets will be deleted'
ttDateMtM = ('MtM prices before and on this date will be deleted')
ttMktBkr = ('Prices on these markets and brokers will be deleted')
ttDateMktBkr = ('Market and broker prices before and on this date will be '
        'deleted')
ttClosedInstrumentsOnly = ('Delete historical prices of selected instruments '
        'with no open positions.')
ttKeepEndOfMonth = ('Keep prices on the last banking day for every month')
ttProtected = ('Prices of these instruments will not be deleted')
ttMaxRuntime = ('The execution will be terminated after this amount of time '
        'in seconds')
ttSavePrices = ('Save deleted prices on file. Prices of existing instruments '
        'will be saved in AMBA message format. Prices referencing removed '
        'instruments will not be saved.')
ttDumpPath = ('Path to directory where the deleted prices will be saved. The '
        'filename will be either {0}_<date>.{1} or <given prefix>_<date>.{2} '
        'if a file prefix is given.'.format(DUMP_PREFIX, DUMP_SUFFIX,
        DUMP_SUFFIX))


ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['CheckForPricesWithoutIns',
                'Delete all prices of removed instruments',
                'int', [0, 1], 0,
                0, 0, ttDelPrcOnNonExistIns, None, 1],
        ['DropExpIns',
                'Delete all prices of expired untraded instruments',
                'int', [0, 1], 0,
                0, 0, ttDelPrcOnExpUntrdIns, cbDelPrcOnExpUntrdIns, 1],
        ['DelSelPrc',
                'Delete selected historical prices',
                'int', [0, 1], 1,
                0, 0, ttDelSelPrc, cbDelSelPrc, 1],
        ['Instruments',
                'Instruments',
                'FInstrument', None, '',
                0, 1, ttInstruments, cbInstruments, 1],
        ['TradeOpenPeriod',
                'Trade open period',
                'string', None, '',
                False, False, ttTradeOpenPeriod, None, False],
        ['MtMMarkets',
                'MtM Markets',
                'string', cvMtMMkt, dvMtMMkt,
                0, 1, ttMtMMkt, cbMtMMkt, 0],
        ['DateMtM',
                'Date for MtM prices',
                'string', ['Yesterday', 'Today', '-6m', '-1y'], 'Yesterday',
                0, 0, ttDateMtM, None, 0],
        ['Markets',
                'Market places and Brokers',
                'string', cvMktBkr, '',
                0, 1, ttMktBkr, cbMktBkr, 0],
        ['DateLast',
                'Date for Market prices',
                'string', ['Yesterday', 'Today', '-6m', '-1y'], 'Yesterday',
                0, 0, ttDateMktBkr, None, 0],
        ['ClosedInstrumentsOnly',
                'Exclude instruments with open positions',
                'int', [0, 1], 0,
                0, 0, ttClosedInstrumentsOnly, None, 1],
        ['KeepEndOfMonth',
                'Keep end of month prices',
                'int', [0, 1], None,
                0, 0, ttKeepEndOfMonth, None, 1],
        ['Protected',
                'Protected instruments',
                'FInstrument', None, 'HISTORICAL_FINANCING',
                0, 1, ttProtected, None, 1],
        ['SavePrices',
                'Save Prices to file',
                'int', [0, 1], 1,
                0, 0, ttSavePrices, cbSavePrices, 1],
        ['DumpDirPath',
                'Output file path',
                'string', cvDumpPath, dvDumpPath,
                0, 0, ttDumpPath, cbDumpDirPath, 1],
        ['MaxRuntime',
                'Max runtime',
                'float', None, '3600',
                0, 0, ttMaxRuntime, None, 1])


def _appendDumpPrefixIfOnlyDirSpecified(dumpDirPath):

    dumpDirPath = dumpDirPath.strip()
    if dumpDirPath and os.path.isdir(dumpDirPath):
        dumpDirPath = os.path.normpath(os.path.join(dumpDirPath, DUMP_PREFIX))
    return dumpDirPath


def ael_main(execParam):
    """
    The entry point of FDeletePrices after the Run button of the Run
    Script window is clicked.
    """
    # Import Front modules.
    import FBDPWorld
    importlib.reload(FBDPWorld)
    import FBDPPerform
    importlib.reload(FBDPPerform)
    import FDelPricePerform
    importlib.reload(FDelPricePerform)
    import FDelPriceUtil
    importlib.reload(FDelPriceUtil)
    # Parameter
    execParam['ScriptName'] = SCRIPT_NAME
    # Compatible to previous behaviour
    if 'SavePrices' in execParam:
        execParam['SavePrices'] = bool(int(execParam['SavePrices']))
    else:
        execParam['SavePrices'] = bool(execParam['DumpDirPath'])
    # Raise use case error for save prices toggle and output path.
    if execParam['SavePrices'] and not execParam['DumpDirPath']:
        raise RuntimeError('You have chosen to save the prices to file, but '
                'output file path has not been provided.')
    # Tidy up dump path if set to save price
    if execParam['SavePrices']:
        execParam['DumpDirPath'] = _appendDumpPrefixIfOnlyDirSpecified(
                execParam['DumpDirPath'])
    execParam['DumpSuffix'] = DUMP_SUFFIX
    # Date conversion
    from FBDPCommon import toDate
    execParam['DateMtM'] = toDate(execParam['DateMtM'])
    execParam['DateLast'] = toDate(execParam['DateLast'])
    # Execute script
    FBDPPerform.execute_perform(FDelPricePerform.perform, execParam)
