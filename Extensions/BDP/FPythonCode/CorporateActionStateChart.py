""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/CorporateActionStateChart.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
 MODULE
     CorporateActionStateChart - Module which define the callback functions for 
     Corporate Action States

 DESCRIPTION
     This module defines the Corporate Action transition callback functions
 ---------------------------------------------------------------------------"""

import acm
import FCorpActionStatesSetup
import FStartRollback
from collections import namedtuple

CATaskFieldValues = namedtuple('CATaskFieldValues', ['default', 'ca_method'])
Default_CA_Task_Parameter_Dict = {
    'ExercisePct': CATaskFieldValues('', 'ExercisePct'),
    'ProtectedComb': CATaskFieldValues('', None),
    'WhatToDoWithNewInstrument': CATaskFieldValues('Distribute it', None),
    'NewShortCode': CATaskFieldValues('', None),
    'Testmode': CATaskFieldValues(0, None),
    'OldShortCode': CATaskFieldValues('', None),
    'CloseAll': CATaskFieldValues(0, 'CloseAll'),
    'SpinoffCostFraction': CATaskFieldValues('', 'SpinoffCostFraction'),
    'ChangeWeightsWithStrikeDiff': CATaskFieldValues(0, None),
    'Settledate': CATaskFieldValues('', 'Settledate'),
    'ChangeWeightsWithRfactor': CATaskFieldValues(0, None),
    'Logfile': CATaskFieldValues('BDP_CorporateAction.log', None),
    'SettleMarket': CATaskFieldValues('', 'SettleMarket'),
    'ReportMessageType': CATaskFieldValues('Full Log', None),
    'SendReportByMail': CATaskFieldValues(0, None),
    'Template': CATaskFieldValues('', 'Template'),
    'ChangeHistoricalPrices': CATaskFieldValues(0, 'AdjustHistoricalPrices'),
    'DividendDecimals': CATaskFieldValues(-1, 'DividendDecimals'),
    'DerivativeTypes': CATaskFieldValues('', None),
    'LogToFile': CATaskFieldValues(0, None),
    'RoundingType': CATaskFieldValues('', 'RoundingType'),
    'NewOptions': CATaskFieldValues('', None),
    'CashCurrency': CATaskFieldValues('', 'CashCurrency'),
    'ClosingPrice': CATaskFieldValues('Average', None),
    'OldContractSizeFormula': CATaskFieldValues(0, None),
    'Portfolio': CATaskFieldValues('', 'Portfolio'),
    'TradeFilter': CATaskFieldValues('', 'TradeFilter'),
    'ChangeDividends': CATaskFieldValues(1, 'AdjustDividends'),
    'CopyIsin': CATaskFieldValues(0, None),
    'ChangeStrike': CATaskFieldValues(0, 'AdjustStrike'),
    'DoAbandon': CATaskFieldValues(0, 'DoAbandon'),
    'SavePriceChanges': CATaskFieldValues(0, None),
    'OldQuantity': CATaskFieldValues('', 'OldQuantity'),
    #'InstrumentType' : CATaskFieldValues('Stock', 'InstrumentType'),
    'InstrumentType': CATaskFieldValues('Stock', None),
    'LogToConsole': CATaskFieldValues(1, None),
    'AdjustOTC': CATaskFieldValues('', 'AdjustOtc'),
    'ChangeWeights': CATaskFieldValues(0, None),
    'NewInstrument': CATaskFieldValues('', 'NewInstrument'),
    'NewPrice': CATaskFieldValues('Zero', None),
    'ChangeTradePrice': CATaskFieldValues(1, 'AdjustTradePrice'),
    'WeightDecimals': CATaskFieldValues(-1, None),
    'MailList': CATaskFieldValues('', None),
    'Grouper': CATaskFieldValues('', 'Grouper'),
    'StartDate': CATaskFieldValues('', None),
    'NewContractSizeFormula': CATaskFieldValues(0, None),
    'CashAmount': CATaskFieldValues(0.0, 'CashAmount'),
    'AddModifier': CATaskFieldValues(0, None),
    'DoExerciseAssign': CATaskFieldValues(0, 'DoExerciseAssign'),
    'ProtectedMarkets': CATaskFieldValues('', None),
    'ChangeContractSize': CATaskFieldValues(0, 'AdjustContractSize'),
    'Instrument': CATaskFieldValues('', 'Instrument'),
    'Preview': CATaskFieldValues(0, None),
    'Derivatives': CATaskFieldValues('', None),
    'TradePriceDecimals': CATaskFieldValues(-1, 'TradePriceDecimals'),
    'IssuePerShare': CATaskFieldValues('', 'IssuePerShare'),
    'HistoricalPriceDecimals': CATaskFieldValues(-1, 'HistoricalPriceDecimals'),
    'NewQuantity': CATaskFieldValues(0, 'NewQuantity'),
    'ChangeName': CATaskFieldValues(0, None),
    'RoundingCompensationCash': CATaskFieldValues(0, None),
    'QuantityDecimals': CATaskFieldValues(0, 'QuantityDecimals'),
    'StrikePrice': CATaskFieldValues(None, 'StrikePrice'),
    #'Method' : CATaskFieldValues('CloseAndOpen', Method),
    'Method': CATaskFieldValues('CloseAndOpen', None),
    'InstrumentNameDecimals': CATaskFieldValues('', 'InstrumentNameDecimals'),
    'ShortCodeFieldName': CATaskFieldValues('', None),
    'SettlePrice': CATaskFieldValues('', 'SettlePrice'),
    'ContractSizeDecimals': CATaskFieldValues(-1, 'ContractSizeDecimals'),
    'Corpact': CATaskFieldValues('', None),
    'AliasType': CATaskFieldValues('', None),
    'ChangeRebate': CATaskFieldValues(0, None),
    'ChangeQuantity': CATaskFieldValues(1, 'AdjustQuantity'),
    'Logmode': CATaskFieldValues(1, None),
    'StrikeDecimals': CATaskFieldValues(1, 'StrikeDecimals'),
    'ChangeBarriers': CATaskFieldValues(0, None),
    'Date': CATaskFieldValues('', None),
    'ExerciseMode': CATaskFieldValues('', 'ExerciseMode'),
    'Exdate': CATaskFieldValues('', 'Exdate'),
    }

Default_RB_Task_Parameter_Dict =\
{
   'instruments': [],
   'Logfile': 'BDP.log',
   'Logmode': 1,
   'LogToConsole': 1,
   'LogToFile': 0,
   'MailList': [],
   'ReportMessageType': ('Full Log',),
   'rollbackSpec': [],
   'SendReportByMail': 0,
   'void': 'Delete',
}
def updateCorpAction(context):
    params = context.Parameters()
    subject = context.Subject()
    TargetState = context.TargetState()
    state = FCorpActionStatesSetup.CovertBSStatusToCAStatus(TargetState.Name())
    subject.Status(state)
    subject.Commit()

def updateCAUpdateSource(context, value):
    pass

def buildCAParameterText(subject, params):
    paramText = ''
    for key, value in Default_CA_Task_Parameter_Dict.iteritems():
        setting = ''
        if not value.ca_method:
            setting = str(value.default)
            if key == 'Corpact':
                setting = '<' + subject.Name() + '>'
        else:
            try:
                method = acm.FCorporateAction.GetMethod(value.ca_method, 0)
                valueFromCA = method.Call([subject])
                if valueFromCA is not None:
                    if isinstance(valueFromCA, float):
                        setting = valueFromCA
                    elif isinstance(valueFromCA, int):
                        setting = int(valueFromCA)
                    elif isinstance(valueFromCA, basestring):
                        if 'none' not in valueFromCA.lower():
                            if key == 'Template':
                                setting = '<' + valueFromCA + '>'
                            else:
                                setting = valueFromCA
                    else:
                        setting = valueFromCA.Name()
            except Exception as e:
                print('Exception:', key, e)
        paramText +=('{0}={1};'.format(key, setting))
    return paramText

def createDefaultCorpActionTask(context):
    print('Creating task ')
    subject = context.Subject()
    params = context.Parameters()
    text = buildCAParameterText(subject, params)
    aelTask = acm.FAelTask()
    aelTask.ModuleName('FCorporateAction')
    taskName = 'BP' + subject.Name()
    if acm.FAelTask[taskName]:
        acm.FAelTask[taskName].Delete()
    aelTask.Name(taskName)
    aelTask.ParametersText(text)
    return aelTask

def processCorpAction(context):
    print('processCorpAction ')
    params = context.Parameters()
    task = None
    if 'task' in params:
        task = acm.FAelTask[params['task']]
    else:
        task = createDefaultCorpActionTask(context)
        task.Commit()
    if task:
        print('executing Task')
        ret = task.Execute()
        print('task returned', ret)
        return 1
    else:
        print('no task found')
        return 0

def on_entry_state_ready(context):
    print('on_entry_state_ready ')
    event = context.Event()
    if event.Name() == 'Initialize':
        return
    updateCAUpdateSource(context, 1)
    updateCorpAction(context)
    updateCAUpdateSource(context, 0)

def on_entry_state_active(context):
    print('on_entry_state_active ')
    updateCAUpdateSource(context, 1)
    if context.Event().Name() != 'Rollback':        
        updateCorpAction(context)
    updateCAUpdateSource(context, 0)

def on_entry_state_inactive(context):
    print('on_entry_state_inactive ')
    updateCAUpdateSource(context, 1)
    updateCorpAction(context)
    updateCAUpdateSource(context, 0)

def on_entry_state_processed(context):
    print('on_entry_state_processed')
    params = context.Parameters()
    updateCAUpdateSource(context, 1)
    processCorpAction(context)

def on_exit_state_processed(context):
    print('on_exit_state_processed ')
    if (context.Event().Name() != 'Rollback'):
        return
    
    #ca is the clone of original action - done in C++
    ca = context.Subject()
    if (ca.IsClone()):
        ca = ca.Original()

    corpActionId = str(ca.Oid())
    query = "name like '{0}%'".format('corporate_action_oid = ' + corpActionId)
    rows = acm.FPersistentText.SqlSelect('oid', query)
    ids = [row.ColumnValues()[0] for row in rows]
    ids.sort()
    if len(ids) == 0:
        return

    # This will be changed when instand of class "FPersistentText"
    # link between "FRollbackSpec" and "FCorporateAction" will used.
    forDeletion = acm.FPersistentText[ids[-1]]
    rollbackSpecNameStr = forDeletion.Text()
    forDeletion.Delete()

    rollbackSpec = acm.FRollbackSpec[rollbackSpecNameStr]
    
    if (rollbackSpec != None):
        Default_RB_Task_Parameter_Dict['rollbackSpec']=[rollbackSpec]
        FStartRollback.ael_main(Default_RB_Task_Parameter_Dict)

def condition_entry_state_active(context):
    print('condition_entry_state_active ')
    return True

def condition_exit_state_active(context):
    print('condition_exit_state_active ')
    return True

def condition_entry_state_ready(context):
    print('condition_entry_state_ready ')    
    return True

def condition_exit_state_ready(context):
    print('condition_exit_state_ready ')
    return True