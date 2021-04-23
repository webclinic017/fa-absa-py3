""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_odf_drawdown/etc/FODFExpiryDrawdown.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FODFExpiryDrawdown - Script for ODF Expiry at EOD.
                         Process Drawdown of remaining amount.

DESCRIPTION

    This module will process ODF Drawdown of remaining
    amount by generating an FX trade.

ENDDESCRIPTION
----------------------------------------------------------------------------"""

#Import Front modules
import acm
import ael
import FBDPGui
import importlib
importlib.reload(FBDPGui)


def insertTradesODF(expiryEnd=None, expiryStart=None):
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')  # empty query
    # enum
    op = query.AddOpNode('OR')
    op.AddAttrNode('Instrument.InsType', 'EQUAL', ael.enum_from_string(
            'InsType', 'FXOptionDatedFwd'))

    # Text
    op = query.AddOpNode('OR')
    op.AddAttrNode('Portfolio.Name', 'EQUAL', None)

    # Text
    op = query.AddOpNode('OR')
    op.AddAttrNode('Acquirer.Name', 'EQUAL', None)

    # Text
    op = query.AddOpNode('OR')
    op.AddAttrNode('Trader.Name', 'EQUAL', None)
    return query


def currpairQuery():
    query = acm.CreateFASQLQuery(acm.FCurrencyPair, 'AND')
    op = query.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)
    return query

ael_variables_ref = [['dummyx'], ['dummyx']]  # forward ref, hook ael_vars.


def ddn_lastdate_hook(index, fieldValues):
    ldenum = 3
    xpld = 4
    if len(ael_variables_ref) > 5:
        if index == ldenum:
            if fieldValues[ldenum] != 'Explicit last date':
                fieldValues[xpld] = 'None'
        if index == xpld:
            if fieldValues[xpld] != 'None':
                fieldValues[ldenum] = 'Explicit last date'
    return fieldValues

tttrades = "Selected positions to be processed, or ?Queryname."
ttCurrencyPair = "Currency pair(s) filter on positions or blank."
ttlastperiodenumdays = ("Expiry days on expiring positions based on ODF "
        "currency pair.")
ttLastDate = ("Enter explicit last date to use as Expiry date. Overrides "
        "last period enum.")
ttDrawdownstatus = "Set Drawdown status for closing drawdown trade."

# Fill in smart default values for trades selection dialog
q = insertTradesODF(expiryEnd='0d', expiryStart='1900-01-01')
default_today_date = ael.date_today().to_string()

cvODFLastPeriod = ['Today', 'Tomorrow', 'Spot', 'Spot next',
        'Explicit last date']
cvODFDrawDownStatus = ['FOConfirmed', 'Simulated']

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['trades',
                'Positions or Queryname',
                'FTrade', None, q,
                2, 1, tttrades],
        ['ODFcurrpair',
                'Currency pair(s)',
                'FCurrencyPair', None, currpairQuery(),
                0, 1, ttCurrencyPair],
        ['ODFlastperiodenum',
                'Last period',
                'string', cvODFLastPeriod, 'Spot',
                1, 0, ttlastperiodenumdays, ddn_lastdate_hook],
        ['ODFlastdate',
                'or Last date',
                'string', ['None'], 'None',
                0, 0, ttLastDate, ddn_lastdate_hook],
        ['ODFDrawdownstatus',
                'Status (for drawdown)',
                'string', cvODFDrawDownStatus, 'FOConfirmed',
                1, 0, ttDrawdownstatus, None, 1])


ael_variables_ref = ael_variables


def ael_main(dictionary):

    import FBDPCommon
    importlib.reload(FBDPCommon)
    ScriptName = "ODF Expiry Drawdown"
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    import FODFExpiryDrawdown_Perform
    importlib.reload(FODFExpiryDrawdown_Perform)
    FBDPCommon.execute_script(
            FODFExpiryDrawdown_Perform.perform_expiry_drawdown, dictionary)
    return
