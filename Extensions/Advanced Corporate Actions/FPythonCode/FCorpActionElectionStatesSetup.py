""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionElectionStatesSetup.py"
"""----------------------------------------------------------------------------
 MODULE
     FCorpActionElectionStatesSetup - Module which define the Corporate Action Election States 

 DESCRIPTION
     This module defines the Corporate Action Election state transition
 ---------------------------------------------------------------------------"""


import acm
import FBDPCommon
import FStateChartUtils
import FBusinessProcessUtils

CA_POSITION_STATES_ORDER = ['Unknown', 'Ready', 'Deadline Received', 'Pending Lender Election',
                            'Borrower Instructed', 'Lender Election Received', 'Processed']

StateTransitions = {
    'Ready':                {
                                'Contact Borrower':           'Deadline Received',
                                'Contact Lender':  'Pending Lender Election',
                            },
    'Deadline Received':    {
                                'Instruct Borrower':          'Borrower Instructed',
                            },
    'Pending Lender Election':    {
                                'Lender Response': 'Lender Election Received',
                            },
    'Lender Election Received':    {
                                'Process':         'Processed',
                            },
    'Borrower Instructed':    {
                                'Process':         'Processed',
                            },
    'Processed':            {
                            }
}

def CreateCorporateActionElectionStateChart():
    limit = 'Single'
    if not acm.FStateChart['CorpActionElectionStateChart']:
        layout = ''
        FStateChartUtils.CreateStateChart('CorpActionElectionStateChart', StateTransitions, layout, limit)
    else:
        FBDPCommon.UpdateStateChart('CorpActionElectionStateChart', StateTransitions)

def DeleteStateChart(chartName):
    if acm.FStateChart[chartName]:
        updater = FStateChartUtils.FStateChartUpdate(chartName)
        updater.DeleteStateChart()

def GetEvent(fromState, toState):
    if fromState in StateTransitions:
        eventDict = StateTransitions[fromState]
        for event, to in eventDict.items():
            if to == toState:
                return event

    return None

def CreateBusinessProcess(name, caAcm):
    bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(caAcm,
                            name)
    bp.Commit()

def GetStatus(ca):
    bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(ca,
                                "CorpActionElectionStateChart")
    return bp.CurrentStep().StateName()

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

    return True
