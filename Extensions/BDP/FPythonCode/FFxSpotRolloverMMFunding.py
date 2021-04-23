""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_position_rolls/etc/FFxSpotRolloverMMFunding.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FFxSpotRolloverMMFunding - GUI for FX spot rollover MM Funding
                               at end of each trading day.

    Requirements:

DESCRIPTION
----------------------------------------------------------------------------"""

import acm

import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FBDPCustomPairDlg
import FBDPCurrentContext

ScriptName = 'FxSpotRolloverMMFunding'

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FFxPositionRollover')

def customPortDialog(shell, params):
    customDlg = FBDPCustomPairDlg.SelectCurrPortCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def customAcqDialog(shell, params):
    customDlg = FBDPCustomPairDlg.SelectCurrAcqCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

ttPortfolioMap = ('Identify physical funding portfolio to be used for each '
        'currency (select \'CCY:Portfolio\' pairs from list)')
ttAcquirerMap = ('Identify funding acquirer to be used for each currency '
        '(select \'CCY:Acquirer\' pairs from list)')
ttDefaultPortfolio = ('Select default physical funding portfolio to be used '
        'by this script (only used if no other portfolio is assigned to a '
        'currency)')
ttFundingIns = ('Specify Deposit instruments holding rates for '
        'overnight, tom next and spot next positions')
ttDefaultAcquirer = ('Select default funding acquirer to be used by this '
        'script (only used if no other acquirer is assigned to a currency)')
ttUseFXSwapTrades = ('Use FX Swaps to roll positions when grouping '
        'by currency pair')

ael_variables = [
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['MappedPortfolios',
                'Funding portfolios for currencies',
                'string', [], None,
                0, 1, ttPortfolioMap, None, 1, customPortDialog],
        ['MappedAcquirers',
                'Funding acquirers for currencies',
                'string', [], None,
                0, 1, ttAcquirerMap, None, 1, customAcqDialog],
        ['FundingInstruments',
                'Funding instruments for currencies_Rates',
                'FDeposit', [], None,
                0, 1, ttFundingIns, None, 1, None],
        ['DefaultPortfolio',
                'Default funding portfolio',
                'FPhysicalPortfolio', None, FBDPGui.insertPhysicalPortfolio(),
                2, 1, ttDefaultPortfolio],
        ['DefaultAcquirer',
                'Default funding acquirer',
                'FParty', None, FBDPGui.insertAcquirer(),
                2, 1, ttDefaultAcquirer],
        ['UseFXSwapTrades',
                'Use FX Swaps to roll',
                'int', [1, 0], 0,
                0, 0, ttUseFXSwapTrades, None, None]
]
additional_kwargs = {'additional_trading_dates': ['Tom']}
ael_variables = FBDPGui.FxVariables(*ael_variables, **additional_kwargs)

def ael_main(execParam):
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
            execParam['Logmode'],
            execParam['LogToConsole'],
            execParam['LogToFile'],
            execParam['Logfile'],
            execParam['SendReportByMail'],
            execParam['MailList'],
            execParam['ReportMessageType'])

    for mappingType in ['MappedPortfolios', 'MappedAcquirers']:
        execParam[mappingType] = FBDPCustomPairDlg.GetDictFromList(
                execParam[mappingType])

    FBDPGui.setPortfolioGrouper(execParam)

    FBDPCommon.execute_script(FFxSpotRolloverPerform.perform_mm_rollover,
                              execParam)
