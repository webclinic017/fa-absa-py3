""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pl_processing/etc/FPLSweep.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPLSweep - Performs PL Sweep at end of each trading day or at end of month.

    Requirements:

    1. 'CC1/CC2 Trading' portfolio must be defined for each currency pair.
       The owner should be something like 'Forex Desk'.

    2. 'PL Sweep' portfolio must be defined for booking PL.
       It probably should be something like 'Forex PL Book'.

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module calls the FPLSweep_Perform procedure based on the
    parameters setup here.

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import acm


import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FBDPCustomPairDlg


ScriptName = 'FPLSweep'


PL_TYPE_POINTS = 'Portfolio Points Profit And Loss'
PL_TYPE_THEORETICAL_TPL = 'Portfolio Theoretical Total Profit and Loss'
PL_TYPE_SPOT_FX_TPL = 'Portfolio Spot FX Total Profit and Loss'


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FPLSweepParameters')


def AccountingCurrency():

    return acm.ObjectServer().UsedValuationParameters().AccountingCurrency()


#==================================================================
# GLOBALS
#==================================================================


class FxPositionVariables_2(FBDPGui.LogVariables):

    def __init__(self, *aelvariables):

        onlyOne = 'Use only one of these objects to select your positions.'
        ttStoredFolder = 'Select positions using stored queries. {0}'.format(
                onlyOne)
        ttTradeFilter = 'Select positions using trade filters. {0}'.format(
                onlyOne)
        ttPortfolio = 'Select positions using portfolios. {0}'.format(
                onlyOne)
        ttGrouper = ('Specify a grouper template. If no grouper is selected, '
                'a default grouping of per portfolio will be used. The '
                'instrument type grouper will enable the PL instrument '
                'mapping field.')
        ttCalculation = ('Use mark-to-market rates and historical yield '
                'curves for the calculation of the PL.')
        ttConversion = ('Use mark-to-market rates for the conversion of the '
                'PL to the risk free currency.')
        ttMtM = 'Rates will be retrieved from the selected MtM market.'
        self.createVariable(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['TradeQuery',
                        'Stored Folder_Positions',
                        'FStoredASQLQuery', None, FBDPGui.insertStoredFolder(),
                        0, 1, ttStoredFolder, self.object_cb])
        self.createVariable(
                ['TradeFilter',
                        'Trade Filter_Positions',
                        'FTradeSelection', None, None,
                        0, 1, ttTradeFilter, self.object_cb])
        self.createVariable(
                ['TradingPortfolios',
                        'Portfolio_Positions',
                        'FPhysicalPortfolio', None, None,
                        0, 1, ttPortfolio, self.object_cb])
        self.createVariable(
                ['PortfolioGrouper',
                        'Portfolio Grouper_Positions',
                        'FStoredPortfolioGrouper', None, None,
                        0, 1, ttGrouper, self.grouper_cb])
        self.createVariable(
                ['UseMtMforCalc',
                        'Use MtM valuation_Rates',
                        'int', ['0', '1'], None,
                        0, 0, ttCalculation, None])
        self.createVariable(
                ['UseMtMforConv',
                        'Use MtM conversion_Rates',
                        'int', ['0', '1'], None,
                        0, 0, ttConversion, self.enableMtM])
        self.createVariable(
                ['MtMMarket',
                        'MtM Market_Rates',
                        'FMTMMarket', None, None,
                        0, 1, ttMtM])
        FBDPGui.LogVariables.__init__(self, *aelvariables)

    def enableMtM(self, index, fieldValues):

        self.MtMMarket.enable(fieldValues[index], 'MtM Market will be '
                'enabled only if "Use MtM Rates" is selected.')
        return fieldValues

    def object_cb(self, index, fieldValues):

        tt = 'You can only select one type of object.'
        for field in [self.TradeQuery,
                self.TradeFilter,
                self.TradingPortfolios]:
            if self[index] != field:
                field.enable(not fieldValues[index], tt)
        return fieldValues

    def grouper_cb(self, index, fieldValues):

        return fieldValues


class FPLSweepVariables(FxPositionVariables_2):

    def grouper_cb(self, index, fieldValues):

        pg = acm.FStoredPortfolioGrouper.Select(
                'name={0}'.format(fieldValues[index]))
        if pg:
            underlyingInGroupers = False
            insTypeInGroupers = False

            pg = pg[0].PortfolioGrouper()
            if pg.IsKindOf(acm.FChainedGrouper):
                for g in pg.Groupers():
                    if (g.IsKindOf(acm.FAttributeGrouper) and
                            str(g.Method()) == 'Instrument.InsType'):
                        insTypeInGroupers = True
                    elif (g.IsKindOf(acm.FUnderlyingGrouper) and
                            str(g.Label()) == 'Underlying'):
                        underlyingInGroupers = True

            if not underlyingInGroupers and insTypeInGroupers:
                self.MappedInstrument.enable(1, ttInstrumentMap)
                return fieldValues
        self.MappedInstrument.enable(0, ttInstrumentMap)
        return fieldValues


def customPortDialog(shell, params):

    customDlg = FBDPCustomPairDlg.SelectCurrpairPortCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


def customAcqDialog(shell, params):

    customDlg = FBDPCustomPairDlg.SelectCurrpairAcqCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


def customInstrumentDialog(shell, params):
    customDlg = (FBDPCustomPairDlg.
            SelectMMInstrumentTypeAndCurrencyToInstrumentCustomDialog(shell,
            params))
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


def customSwapInstrumentDialog(shell, params):
    customDlg = FBDPCustomPairDlg.SelectCurrpairInstCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def customPortCurrPairDialog(shell, params):
    customDlg = \
        FBDPCustomPairDlg.SelectPortfolioCurrpairCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

ttTradingCalendar = ('Trading location calendar. Default is calendar '
        'of accounting currency.')
ttNextTradingDate = ('Spot next will sweep each day until tomorrow\'s '
        'spot date. Tom next will sweep each day until today\'s spot '
        'date. Choose Tom next if PL value is to be zero today or '
        'Spot next if it must be zero tomorrow.')
ttSweepPLToday = ('Sweep PL Today')

ttPLPortfolio = ('The PL portfolio that receives the PL from the trading '
        'portfolio.')
ttPLAcquirer = 'The acquirer that receives the PL from the trading portfolio.'
ttPLCurrency = ('The currency of the PL after the sweep. The risk free '
        'currency.')
ttPortfolioMap = ('Map a conversion portfolio to a currency pair, allowing a '
        'different conversion portfolio per currency pair, when using a '
        'currency pair grouper.')
ttAcquirerMap = ('Map a conversion acquirer to a currency pair, allowing a '
        'different conversion acquirer per currency pair, when using a '
        'currency pair grouper.')
ttInstrumentMap = ('Map a PL instrument to each combination of instrument '
        'type and currency. This field is only enabled with an instrument '
        'type grouper.')
ttDefaultPortfolio = ('The default conversion portfolio to use if a mapped '
        'conversion portfolio is not specified.')
ttDefaultAcquirer = ('The default conversion acquirer to use if a mapped '
        'acquirer is not specified.')
ttSpotForwardPLValue = ('The PL to be swept on and after the spot date. '
        'Before the spot date the ProjPL is swept.')
ttSweepPLCurrencyIfInPair = ('Use the PL currency as the sweep currency if '
        'the PL currency is one of the currencies in currency pair.')
ttSweepAccountingCurrencyIfInPair = ('Use the accounting currency as the '
         'sweep currency if the accounting currency is one of the currencies '
         'in currency pair.')
ttSweepFxBaseCurrencyIfInPair = ('Use the Fx base currency as the '
         'sweep currency if the Fx base currency is one of the currencies '
         'in currency pair.')
ttRetainPL = 'Remove FX risk but retain the PL in the trading portfolio.'
ttUsePayments = ('Use payments instead of premium or quantity '
                'to sweep PL')
ttRollbackID = ('Choose a rollback identifier. If nothing is specified, '
        '\'PLSweep\' will be used.')
ttConversion = ('Convert PL in trading portfolio. ')
ttFundingMap = ('Select specific funding instruments for currency pairs '
        '(select \'CurrencyPair:Instrument\' pairs from list).')
ttPositionPairPortfolioMap = ('Select position pair for conversion '
        'portfolios. '
        'The position pair should be the same as the currency pair in '
        'the portfolio if there is any.'
        '(select \'CurrencyPair:Portfolio\' pairs from list).')

cvSpotForwardPLValue = [PL_TYPE_POINTS, PL_TYPE_THEORETICAL_TPL,
        PL_TYPE_SPOT_FX_TPL]


def cbNextTradingDate(index, fieldValues):
    for field in (ael_variables.NextTradingDate,
                ael_variables.SweepPLToday):
        if field.sequenceNumber != index:
            field.enable(not fieldValues[index] or
                fieldValues[index] == '0', '')

    if (ael_variables.SweepPLToday.isEnabled() and
        fieldValues[ael_variables.SweepPLToday.sequenceNumber] == '1'):
        fieldValues[ael_variables.RetainPL.sequenceNumber] = '1'

    return fieldValues

ael_variables = FPLSweepVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['TradingCalendar',
                'Trading location calendar',
                'FCalendar', None, None,
                0, 1, ttTradingCalendar],
        ['NextTradingDate',
                'Next trading date',
                'string',
                ['Spot next', 'Tom next'],
                None,
                0, 0, ttNextTradingDate, cbNextTradingDate],
        ['SweepPLToday',
                'Sweep PL today',
                'int', ['0', '1'], None,
                0, 0, ttSweepPLToday, cbNextTradingDate],
        ['PLPortfolio',
                'PL portfolio',
                'FPhysicalPortfolio', None, FBDPGui.insertPhysicalPortfolio(),
                1, 1, ttPLPortfolio],
        ['PLAcquirer',
                'PL acquirer',
                'FParty', None, FBDPGui.insertAcquirer(),
                0, 1, ttPLAcquirer],
        ['PLCurrency',
                'PL currency',
                'FCurrency', None, AccountingCurrency(),
                1, 0, ttPLCurrency],
        ['MappedPortfolios',
                'Conversion portfolios for currency pairs',
                'string', [], None,
                0, 1, ttPortfolioMap, None, 1, customPortDialog],
        ['MappedPositionPairs',
                'Position pairs in conversion portfolios',
                'string', [], None,
                0, 1, ttPositionPairPortfolioMap, None, 1,
                customPortCurrPairDialog],
        ['MappedAcquirers',
                'Conversion acquirers for currency pairs',
                'string', [], None,
                0, 1, ttAcquirerMap, None, 1, customAcqDialog],
        ['MappedInstrument',
                'PL instrument mapping_Positions',
                'string', [], None,
                0, 1, ttInstrumentMap, None, 0, customInstrumentDialog],
        ['MappedFundingInstruments',
                'Funding instruments for currency pairs_Rates',
                'string', [], None,
                0, 1, ttFundingMap, None, 1, customSwapInstrumentDialog],
        ['DefaultPortfolio',
                'Default conversion portfolio',
                'FPhysicalPortfolio', None, FBDPGui.insertPhysicalPortfolio(),
                2, 1, ttDefaultPortfolio],
        ['DefaultAcquirer',
                'Default conversion acquirer',
                'FParty', None, FBDPGui.insertAcquirer(),
                0, 1, ttDefaultAcquirer],
        ['SpotForwardPLValue',
                'PL value',
                'string', cvSpotForwardPLValue, PL_TYPE_THEORETICAL_TPL,
                1, 0, ttSpotForwardPLValue],
        ['SweepPLCurrencyIfInPair',
                'Sweep PL currency if in pair',
                'int', [1, 0], 1,
                0, 0, ttSweepPLCurrencyIfInPair, None, None],
        ['AccountingCurrencyIfInPair',
                'Sweep accounting currency if in pair',
                'int', [1, 0], 1,
                0, 0, ttSweepAccountingCurrencyIfInPair, None, None],
        ['SweepFXBaseCurrencyIfInPair',
                'Sweep FX Base Currency if in pair',
                'int', [1, 0], 1,
                0, 0, ttSweepFxBaseCurrencyIfInPair, None, None],
        ['RetainPL',
                'Retain PL in trading portfolio',
                'int', [1, 0], 0,
                0, 0, ttRetainPL],
        ['UsePayments',
                'Use payments to sweep PL',
                'int', [1, 0], 1,
                0, 0, ttUsePayments],
        ['ConvertInTradingPortfolio',
                'Convert in trading portfolio',
                'int', ['0', '1'], None,
                0, 0, ttConversion],
        ['RollbackID',
                'Rollback identifier',
                'string', None, None,
                0, 0, ttRollbackID])


def ael_main(execParam):

    import FBDPString
    importlib.reload(FBDPString)
    import FBDPRollback
    importlib.reload(FBDPRollback)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FFxCommon
    importlib.reload(FFxCommon)
    import FPLSweep_Perform
    importlib.reload(FPLSweep_Perform)
    import FBDPCurrentContext  # DO NOT reload FBDPCurrentContext

    FBDPCurrentContext.CreateLog(ScriptName,
            execParam['Logmode'],
            execParam['LogToConsole'],
            execParam['LogToFile'],
            execParam['Logfile'],
            execParam['SendReportByMail'],
            execParam['MailList'],
            execParam['ReportMessageType'])

    for mappingType in ('MappedPortfolios', 'MappedAcquirers',
            'MappedInstrument', 'MappedFundingInstruments'):
        execParam[mappingType] = FBDPCustomPairDlg.GetDictFromList(
                execParam[mappingType])
    d = {}
    for p in execParam['MappedPositionPairs']:
        par = p.partition(':')
        key = par[0].strip() if par[0] else None
        val = par[2].strip() if par[2] else None
        if key and val:
            if key in d:
                d[key].append(val)
            else:
                d[key] = [val]
    execParam['MappedPositionPairs'] = d
    FBDPGui.setPortfolioGrouper(execParam)
    FBDPCommon.execute_script(FPLSweep_Perform.perform_sweep, execParam)
