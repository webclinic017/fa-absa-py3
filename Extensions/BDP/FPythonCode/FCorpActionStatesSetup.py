""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FCorpActionStatesSetup.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
 MODULE
     FCorpActionStatesSetup - Module which define the Corporate Action States 

 DESCRIPTION
     This module defines the Corporate Action state transition
 ---------------------------------------------------------------------------"""


import acm
import FBDPCommon
import FStateChartUtils
import FBusinessProcessUtils

StateTransitions = {
    'Ready':                  {
                                'Activate':           'Active',
                                'De-Activate':        'Inactive'
                            },

    'Active':               {
                                'Process':          'Processed',
                                'De-Activate':      'Inactive',
                                'Preview':          'Pending'
                            },
    'Pending':              {
                                'Approve':          'Processed',
                                'Rollback':         'Active',
                            },

    'Inactive':             {
                                'Activate':         'Active'
                            },

    'Processed':            {
                                'Rollback':         'Active',
                                'Remove':           'Removed'
                            },
    'Removed':              {
                            }
}

def CreateCorporateActionStateChart():
    limit = 'Single'
    if not acm.FStateChart['CorporateActionStateChart']:
        layout = 'Inactive,280,-76;Active,469,133;Processed,91,133;Pending,466,-70;Removed,280,76;Ready,91,76'
        FStateChartUtils.CreateStateChart('CorporateActionStateChart', StateTransitions, layout, limit)

def DeleteStateChart(chartName):
    if acm.FStateChart[chartName]:
        updater = FStateChartUtils.FStateChartUpdate(chartName)
        updater.DeleteStateChart()

def GetEvent(fromState, toState):
    if fromState in StateTransitions:
        eventDict = StateTransitions[fromState]
        for event, to in eventDict.iteritems():
            if to == toState:
                return event
    else:
        return None

    return 'Set to ' + toState

def CreateBusinessProcess(name, caAcm):
    if not CorporateActionUsingBusinessProcess():
        return
    bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(caAcm,
                            name)
    bp.Commit()

def UpdateBusinessProcess(name, caAcm, fromState, toState, param):
    if not CorporateActionUsingBusinessProcess():
        return
    if fromState == toState:
        return
    else:
        event = GetEvent(fromState, toState)
        print(fromState, '--', toState, '--', event)
        bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(caAcm,
                                name)
        bp.HandleEvent(event, param)
        bp.Commit()

def GetStatus(ca):
    bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(ca,
                                "CorporateActionStateChart")
    return bp.CurrentStep().StateName()

def ConvertStatus(status):
    retState = status
    if status == 'None':
        retState = 'Ready'
    return retState

def CovertBSStatusToCAStatus(status):
    retState = status
    if status == 'Ready':
        retState = 'None'
    return retState

def CorporateActionUsingBusinessProcess():
    params = acm.GetDefaultContext().GetExtension('FParameters',
                    'FObject', 'FCAVariables')
    if not params:
        return False
    paramsKeysAndValues = params.Value()
    key = acm.FSymbol('UseBusinessProcess')
    if key not in paramsKeysAndValues.Keys() \
                or paramsKeysAndValues[key] == acm.FSymbol('0'):
        return False
    #Checks if the state chart exists and creates it if not
    CreateCorporateActionStateChart()
    return True

