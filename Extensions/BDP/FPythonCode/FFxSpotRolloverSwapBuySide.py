""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_position_rolls/etc/BuySide/FFxSpotRolloverSwapBuySide.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
MODULE
    FFxSpotRolloverSwapFundingBuySide - GUI for FX Spot postion rollover swap
    funding at end of each trading day.

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import acm


import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FBDPCustomPairDlg
importlib.reload(FBDPCustomPairDlg)


ScriptName = "FxSpotRolloverSwapBuySide"


FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters(
        'FBDPParameters', 'FFxPositionRollover')


template = None


def brokerRatesDialog(shell, params):

    customDlg = FBDPCustomPairDlg.BrokerRatesCustomDialog(shell, params,
            template)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


def tradingDateDialog(shell, params):

    customDlg = FBDPCustomPairDlg.TradingDateCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


def defaultTemplates():

    namespace = 'FxRoll_'
    context = acm.GetDefaultContext()
    return [str(ext.Name()).split(namespace)[1] for ext in
            context.GetAllExtensions(acm.FExtensionValue) if str(
            ext.Name()).startswith(namespace)]


def defaultTemplate_cb(index, fieldValues):

    global template
    template = fieldValues[index]
    return fieldValues


qPort = FBDPGui.insertPhysicalPortfolio()
qAcq = FBDPGui.insertAcquirer()
qCtrpty = FBDPGui.insertCounterparty()


ttDefaultPortfolio = ('Select a default funding portfolio '
        '(only used if no other portfolio is assigned to a currency pair')
ttDefaultAcquirer = ('Select a default funding acquirer '
        '(only used if no other acquirer is assigned to a currency pair)')
ttDefaultCounterparty = ("Select a default counterparty for roll trades "
        "created. If rates are specified for a currency pair, 'Executing "
        "Broker' will be used as the counterparty, otherwise Default "
        "counterparty.")
ttBrokerRates = ('Define FX rates for currency pair per custodian and '
        'executing broker')
ttRollNotNeeded = 'Tick if roll should proceed only if FX rate is defined'
ttDefaultTemplate = ('Extension values used to pre-populate the FX rates. '
        'These are stored as FExtensionValues with the prefix "FxRoll_".')


ael_variables = FBDPGui.FxPositionVariablesBuySide(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['DefaultTemplate',
                'Template',
                'string', defaultTemplates(), None,
                0, 0, ttDefaultTemplate, defaultTemplate_cb],
        ['DefaultPortfolio',
                'Default funding portfolio', 'FPhysicalPortfolio', None, qPort,
                2, 1, ttDefaultPortfolio],
        ['DefaultAcquirer',
                'Default funding acquirer', 'FParty', None, qAcq,
                2, 1, ttDefaultAcquirer],
        ['Counterparty',
                'Default counterparty', 'FParty', None, qCtrpty,
                2, 1, ttDefaultCounterparty],
        ['BrokerRates',
                'Fx rates_Rates', 'string', [], None,
                0, 1, ttBrokerRates, None, 1, brokerRatesDialog],
        ['RollNotNeeded',
                'Roll only if FX rate is defined_Rates',
                'string', ['True', 'False'], 'True',
                0, 0, ttRollNotNeeded]
)


def ael_main(dictionary):

    import FBDPString
    importlib.reload(FBDPString)
    import FBDPRollback
    importlib.reload(FBDPRollback)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FFxCommonBuySide
    importlib.reload(FFxCommonBuySide)
    import FFxSpotRolloverPerformBuySide
    importlib.reload(FFxSpotRolloverPerformBuySide)

    logme = FBDPString.logme
    logme.setLogmeVar(ScriptName,
            dictionary['Logmode'],
            dictionary['LogToConsole'],
            dictionary['LogToFile'],
            dictionary['Logfile'],
            dictionary['SendReportByMail'],
            dictionary['MailList'],
            dictionary['ReportMessageType'])

    FBDPGui.setPortfolioGrouper(dictionary)
    FBDPCommon.execute_script(
            FFxSpotRolloverPerformBuySide.perform_swap_rollover, dictionary)
