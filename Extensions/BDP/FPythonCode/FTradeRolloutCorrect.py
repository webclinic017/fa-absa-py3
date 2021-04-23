""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/trade_rollout/FTradeRolloutCorrect.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FTradeRollout

DESCRIPTION

NOTE
    The modules uses the aggregation rules in...


ENDDESCRIPTION
----------------------------------------------------------------------------"""

import FBDPGui
import importlib
importlib.reload(FBDPGui)


import acm


import FAggruleSelectItem


### Load Default values from FParameters
FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FTradeRolloutCorrectVariables')


# Populate the tradeFilters for selection.
tradeFilters = []
for tf in acm.FTradeSelection.Select(''):
    # Filter out those for aggregation rules (begin with '~AggRule_')
    if not tf.Name().startswith('~AggRule_'):
        tradeFilters.append(tf.Name())


ttCorrectAll = 'Correct all trades in the database that has gone wrong'
ttUseAggRules = 'Use the Aggregation Rules when selecting trades'
ttAggRuleFilters = ('If set, only run the set of aggregation rules defined '
        'by these trade filters. If not set, all aggregation rules will be '
        'used.')
ttTradeFilters = 'Use these Trade Filters when selecting trades'
ttRolloutToAMBA = 'Export to AMBA'
ttRolloutToXML = 'Export to XML'
ttFilePath = 'This file will be created or appended'
ttUseBatching = 'Rollout trades in batches. If set, no validation is performed'
ttMaxBatchSize = 'Maximum number of trades to rollout per batch'

def disable_variables(variables, enable=0, disabledTooltip=None):
    for i in variables:
        getattr(ael_variables, i).enable(enable, disabledTooltip)


def cb(index, fieldValues):
    global ael_variables
    if ael_variables[index][0] == 'correctAll':
        disable_variables(('useAggRules', 'aggRuleFilters', 'tradeFilters'),
            fieldValues[index] == '0',
            'Uncheck "Correct all trades" to enable this field.')

    if ael_variables[index][0] == 'useAggRules':
        disable_variables(('aggRuleFilters',),
            fieldValues[index] == '1',
            'Check "Use aggregation rules" to enable this field.')
        disable_variables(('tradeFilters',),
            fieldValues[index] == '0',
            'Uncheck "Use aggregation rules" to enable this field.')

    if ael_variables[index][0] == 'rolloutToAMBA':
        disable_variables(('rolloutToXML', 'useBatching'),
            fieldValues[index] == '0',
            'Uncheck "%s" to enable this field.' % (ttRolloutToAMBA))
        for i, v in enumerate(ael_variables):
            if v[0] == 'useBatching':
                disable_variables(
                    ('maxBatchSize',),
                    fieldValues[i] == '1' and fieldValues[index] == '0'
                )
                break
    elif ael_variables[index][0] == 'rolloutToXML':
        disable_variables(('rolloutToAMBA', 'useBatching'),
            fieldValues[index] == '0',
            'Uncheck "%s" to enable this field.' % (ttRolloutToXML))
        for i, v in enumerate(ael_variables):
            if v[0] == 'useBatching':
                disable_variables(
                    ('maxBatchSize',),
                    fieldValues[i] == '1' and fieldValues[index] == '0'
                )
                break

    if ael_variables[index][0] in ['rolloutToAMBA', 'rolloutToXML']:
        disable_variables(('filePath',),
            fieldValues[index] == '1',
            'Check either "%s" or "%s" to enable this field.' % (
                ttRolloutToAMBA, ttRolloutToXML
            ))

    if ael_variables[index][0] == 'useBatching':
        disable_variables(('maxBatchSize',),
            fieldValues[index] == '1',
            'Check "%s" to enable this field.' % (ttUseBatching))

    return fieldValues


def customDialog(shell, params):
    customDlg = FAggruleSelectItem.SelectAggrulesCustomDialog(params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['useAggRules',
                'Use aggregation rules',
                'int', [1, 0], 0,
                0, 0, ttUseAggRules, cb, None],
        ['aggRuleFilters',
                'Aggregation filters',
                'int', [], '',
                0, 1, ttAggRuleFilters, None, 1, customDialog],
        ['tradeFilters',
                'Trade Filters',
                'string', tradeFilters, None,
                0, 1, ttTradeFilters, None, None],
        ['rolloutToAMBA',
                ttRolloutToAMBA,
                'int', [1, 0], 1,
                0, 0, ttRolloutToAMBA, cb, None],
        ['rolloutToXML',
                ttRolloutToXML,
                'int', [1, 0], 0,
                0, 0, ttRolloutToXML, cb, None],
        ['filePath',
                'Export file path',
                'string', None, None,
                0, 0, ttFilePath, None, None],
        ['useBatching',
                'Rollout trades in batches',
                'int', [1, 0], 0,
                0, 0, ttUseBatching, cb, None],
        ['maxBatchSize',
                'Maximum batch size',
                'int', None, 500,
                0, 0, ttMaxBatchSize, None, 0])


def ael_main(dictionary):

    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FTradeRolloutPerform
    importlib.reload(FTradeRolloutPerform)
    import FBDPCurrentContext

    FBDPCurrentContext.CreateLog('Trade Rollout Correct',
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    FBDPCommon.execute_script(FTradeRolloutPerform.perform_rollout_correct,
                              dictionary)
