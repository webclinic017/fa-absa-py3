""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_position_rolls/etc/FFxSpotRolloverSwapFunding.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FFxSpotRolloverSwapFunding- GUI for FX Spot postion rollover swap funding
                                at end of each trading day.

DESCRIPTION

ENDDESCRIPTION
"""


import acm


import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FBDPCustomPairDlg
import FBDPCurrentContext


ScriptName = 'FxSpotRolloverSwapFunding'


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FFxPositionRollover')


def customPortDialog(shell, params):
    customDlg = FBDPCustomPairDlg.SelectCurrpairPortCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def customPortCurrPairDialog(shell, params):
    customDlg = \
        FBDPCustomPairDlg.SelectPortfolioCurrpairCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def customAcqDialog(shell, params):
    customDlg = FBDPCustomPairDlg.SelectCurrpairAcqCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


def customInstDialog(shell, params):
    customDlg = FBDPCustomPairDlg.SelectCurrpairInstCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


ttPortfolioMap = ('Select specific funding portfolios for currency pairs '
        '(select \'CurrencyPair:Portfolio\' pairs from list).')
ttPositionPairPortfolioMap = ('Select position pair for funding portfolios. '
        'The position pair should be the same as the currency pair in '
        'the portfolio if there is any.'
        '(select \'CurrencyPair:Portfolio\' pairs from list).')
ttAcquirerMap = ('Select specific funding acquirers for currency pairs '
        '(select \'CurrencyPair:Acquirer\' pairs from list)')
ttFundingMap = ('Select specific funding instruments for currency pairs '
        '(select \'CurrencyPair:Instrument\' pairs from list).  '
        'Default instrument is HISTORICAL_FINANCING.')
ttFundingIns = ('Specify FX swap instruments holding swap points for '
        'overnight, tom next and spot next positions.')
ttDefaultPortfolio = ('Select a default funding portfolio '
        '(only used if no other portfolio is assigned to a currency pair')
ttDefaultAcquirer = ('Select a default funding acquirer '
        '(only used if no other acquirer is assigned to a currency pair)')


ael_variables = FBDPGui.FxVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['MappedPortfolios',
                'Funding portfolios for currency pairs',
                'string', [], None,
                0, 1, ttPortfolioMap, None, 1, customPortDialog],
        ['MappedPositionPairs',
                'Position pairs in funding portfolios',
                'string', [], None,
                0, 1, ttPositionPairPortfolioMap, None, 1,
customPortCurrPairDialog],
        ['MappedAcquirers',
                'Funding acquirers for currency pairs',
                'string', [], None,
                0, 1, ttAcquirerMap, None, 1, customAcqDialog],
        ['MappedFundingInstruments',
                'Funding instruments for currency pairs_Rates',
                'string', [], None,
                0, 1, ttFundingMap, None, 1, customInstDialog],
        ['FundingInstruments',
                'Funding instruments_Rates',
                'FFxSwap', [], None,
                0, 1, ttFundingIns, None, 1, None],
        ['DefaultPortfolio',
                'Default funding portfolio',
                'FPhysicalPortfolio', None, FBDPGui.insertPhysicalPortfolio(),
                2, 1, ttDefaultPortfolio],
        ['DefaultAcquirer',
                'Default funding acquirer',
                'FParty', None, FBDPGui.insertAcquirer(),
                2, 1, ttDefaultAcquirer])


def ael_main(dictionary):
    #Import Front modules
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPRollback
    importlib.reload(FBDPRollback)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FFxCommon
    importlib.reload(FFxCommon)
    import FFxSpotRolloverPerform
    importlib.reload(FFxSpotRolloverPerform)

    FBDPCurrentContext.CreateLog(ScriptName,
            dictionary['Logmode'],
            dictionary['LogToConsole'],
            dictionary['LogToFile'],
            dictionary['Logfile'],
            dictionary['SendReportByMail'],
            dictionary['MailList'],
            dictionary['ReportMessageType'])

    for mappingType in ['MappedPortfolios', 'MappedAcquirers',
            'MappedFundingInstruments']:
        dictionary[mappingType] = FBDPCustomPairDlg.GetDictFromList(
                dictionary[mappingType])
    d = {}
    for p in dictionary['MappedPositionPairs']:
        par = p.partition(':')
        key = par[0].strip() if par[0] else None
        val = par[2].strip() if par[2] else None
        if key and val:
            if key in d:
                d[key].append(val)
            else:
                d[key] = [val]
    dictionary['MappedPositionPairs'] = d
    FBDPGui.setPortfolioGrouper(dictionary)
    FBDPCommon.execute_script(FFxSpotRolloverPerform.perform_swap_rollover,
            dictionary)
