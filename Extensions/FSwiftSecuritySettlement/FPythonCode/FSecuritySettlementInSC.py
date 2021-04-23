"""----------------------------------------------------------------------------
MODULE:
    FSecuritySettlementInSC

DESCRIPTION:
    OPEN EXTENSION MODULE
    State chart creation for Security settlement confirmation.
    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:
      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

FUNCTIONS:
    define_state_transition():
        Define the state transition for state chart
    create_security_settlment_conf_sc():
        Creates the state chart

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('SecSetlConf', 'FSecuritySettlementInNotify_Config')
import FMTStateChart

def define_state_transition_SecuritySettlement():
        """
        Creates a state chart with the given name, if required.
        The definition parameter must completely define the content of the business
        process state chart, including all states and transitions between them. Its
        format is a dictionary of states mapped to a dictionary of transitions as
        event->next_state items, e.g.:
          {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}
        """

        state_chart_name = 'FSwiftSecuritySettlementIn'
        old_state_chart_name = 'SecuritySettlementConfMsg'
        state_chart = {
                        'Ready':    {'Identified'                      :    'Paired',
                                                      'NotIdentified'                   :    'Unpaired',
                                                      'SecurityTransfer'                :    'TradeGenerated'},
                        'Paired':    {'PartialMatch'                    :    'PartialMatch',
                                                      'NoMatch'                         :    'Difference',
                                                      'Match'                           :    'Settled',
                                                      'AlreadyCancelled'                :    'ManuallyCancelled' },
                        'Unpaired':    {'Ignore'                          :    'Ignored',
                                                      'Identified'                      :    'Paired'},
                        'Difference':    {'ManuallyCorrect'                 :    'ManuallyCorrected',
                                                      'Unpair'                          :    'Unpaired',
                                                      'Re-Match'                        :    'Paired',
                                                      'ManuallyMatch'                   :    'Settled'},
                        'PartialMatch':    {'Identified'                      :    'Paired'},
                        'TradeGenerated':    {'Identified'                      :    'Paired'},
                        'Settled':    {'Unpair'                          :    'Unpaired'},
                    }
        co_string = 'Ready,-500,0;Paired,-300,0;PartialMatch,-300,400;Settled,400,0;Unpaired,-300,-200;Ignored,400,-200;Difference,400,250;ManuallyCorrected,400,400;TradeGenerated,-500,400;ManuallyCancelled,100,400'
        #state_charts_list.append({state_chart_name:[state_chart]+[co_string]})

        return state_chart_name, state_chart, old_state_chart_name, co_string


def define_state_transition_SettlementStatusProcessingAdvice():
    """
    Creates a state chart with the given name, if required.
    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:
      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}
    """

    state_chart_name = 'FSwiftSettStatusProcessAdviceIn'
    old_state_chart_name = ''
    state_chart = {
                    'Ready': {'Identified': 'Paired',
                              'NotIdentified': 'Unpaired'},

                    'Unpaired': {'Identified': 'Paired'},

                    'Paired': {'Acknowledge': 'Acknowledged',
                               'NoMatch': 'NotMatched',
                               'Match': 'Matched',
                               'Pending': 'PendingSettlement',
                               'Failing': 'FailingSettlement',
                               'Reject': 'Rejected',
                               'Cancel': 'Cancelled',},

                    'Acknowledged': {'NoMatch': 'NotMatched',
                                    'Match': 'Matched',
                                    'Pending': 'PendingSettlement',
                                    'Failing': 'FailingSettlement',
                                    'Cancel': 'Cancelled',
                                    'Reject': 'Rejected',
                                    'AmndCancRequest':'AmendCancelRequested',
                                    'AmndCancPending':'AmendCancelPending',
                                    'Done':'Processed'},

                    'Matched': {'Pending': 'PendingSettlement',
                                'Cancel': 'Cancelled',
                                'Reject': 'Rejected',
                                'Failing': 'FailingSettlement',
                                'AmndCancRequest':'AmendCancelRequested',
                                'AmndCancPending':'AmendCancelPending',
                                'Done':'Processed'
                                },

                    'FailingSettlement':{'AmndCancRequest':'AmendCancelRequested',
                                         'AmndCancPending':'AmendCancelPending',
                                         'Reject': 'Rejected',
                                         'Cancel': 'Cancelled',
                                         'Done':'Processed'},

                    'NotMatched': {'Match': 'Matched',
                                  'Pending': 'PendingSettlement',
                                  'Failing': 'FailingSettlement',
                                  'Cancel': 'Cancelled',
                                  'Reject': 'Rejected',
                                  'AmndCancRequest':'AmendCancelRequested',
                                  'AmndCancPending':'AmendCancelPending',
                                  'Done':'Processed'},

                    'AmendCancelRequested': {'AmndCancComplete':'AmendCancelCompleted',
                                            'Done':'Processed'},

                    'AmendCancelPending': {'AmndCancComplete':'AmendCancelCompleted',
                                            'Done':'Processed'},

                    'PendingSettlement': {'Failing': 'FailingSettlement',
                                          'Cancel': 'Cancelled',
                                          'AmndCancRequest':'AmendCancelRequested',
                                          'AmndCancPending':'AmendCancelPending',
                                          'Reject': 'Rejected',
                                          'Done':'Processed'},
                    'Cancelled' : { 'Done':'Processed'},
                    'AmendCancelCompleted' : { 'Done':'Processed'},

                    'Rejected': {'Cancel': 'Cancelled',
                                 'Done': 'Processed'}

    }

    co_string = 'Paired,73,-105;Cancelled,676,329;Not Match,696,-223;Match,1271,173;AmendCancelPending,728,189;Matched,347,-133;Unpaired,-178,-351;Acknowledge,435,-110;Reject,229,538;AmendCancelCompleted,862,90;Rejected,177,338;NotMatched,432,-283;Acknowledged,549,-429;Processed,1072,-131;Pending Settlement,1193,495;PendingSettlement,304,22;FailingSettlement,255,179;Ready,-237,-98;AmendCancelRequested,737,0;'
    #state_charts_list.append({state_chart_name: [state_chart] + [co_string]})

    return state_chart_name, state_chart, old_state_chart_name, co_string



def define_state_transition_ClientStatementOfHolding():
    """
        Creates a state chart with the given name, if required.
        The definition parameter must completely define the content of the business
        process state chart, including all states and transitions between them. Its
        format is a dictionary of states mapped to a dictionary of transitions as
        event->next_state items, e.g.:
          {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}
    """

    state_chart_name = 'FSwiftClientStmtOfHoldingIn'
    old_state_chart_name = ''
    state_chart = {
        'Ready': {'TradeCreated': 'Processed',
                  'TradeCreationFailure': 'Failed'}
    }
    co_string = 'Failed,-58,84;Processed,-55,-228;Ready,-673,-70;'
    # state_charts_list.append({state_chart_name:[state_chart]+[co_string]})

    return state_chart_name, state_chart, old_state_chart_name, co_string


def define_state_transition_SecurityConfirmation():
    """
    Creates a state chart with the given name, if required.
    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:

      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

    All defined next_states values must be unique within a state's transitions
    (i.e. multiple events cannot lead to the same next_state).
    """

    state_chart_name = 'FSwiftSecurityConfirmationIn'
    state_chart = {
        'Ready': {'Identified': 'Paired',
                  'NotIdentified': 'Unpaired'},
        'Paired': {'NoMatch': 'Difference',
                   'Match': 'Matched',
                   'Cancel': 'Cancelled'},
        'Unpaired': {'Identified': 'Paired',
                     'Cancel': 'Cancelled'},
        'Difference': {'ManuallyMatched': 'Matched',
                       'Unpair': 'Unpaired',
                       'Re-Match': 'Paired',
                       'Cancel': 'Cancelled'},
        'Matched': {'Unpair': 'Unpaired',
                    'Cancel': 'Cancelled'}
    }
    co_string = 'Ready,-603,-83;Cancelled,-30,-320;Unpaired,-380,-322;Paired,-379,-84;Difference,-22,84;Matched,271,-79;'
    return state_chart_name, state_chart, co_string


def create_state_charts(state_chart_name, state_chart, old_state_chart_name, co_string):
    state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart, old_state_chart_name)
    FMTStateChart.layout_state_chart(state_chart_name, co_string)
    notifier.INFO('Done with layout of state chart %s.' % state_chart_name)

def create_security_settlment_conf_sc():
    notifier.INFO('Create SC for Security Settlement')
    notifier.INFO('Define state transition for SecuritySettlement called')
    state_chart_name, state_chart_dict, old_state_chart_name, co_string = define_state_transition_SecuritySettlement()
    create_state_charts(state_chart_name, state_chart_dict, old_state_chart_name, co_string)
    notifier.INFO('Create SC for Security Settlement done')

    notifier.INFO('Create SC for Settlement Status Processing Advice')
    notifier.INFO('Define state transition SettlementStatusProcessingAdvice called')
    state_chart_name, state_chart_dict, old_state_chart_name, co_string = define_state_transition_SettlementStatusProcessingAdvice()
    create_state_charts(state_chart_name, state_chart_dict, old_state_chart_name, co_string)
    notifier.INFO('Create SC for Settlement Status Processing Advice done')

    notifier.INFO('Create SC for Client Statement of Holding')
    notifier.INFO('Define state transition ClientStatementOfHolding called')
    state_chart_name, state_chart_dict, old_state_chart_name, co_string = define_state_transition_ClientStatementOfHolding()
    create_state_charts(state_chart_name, state_chart_dict, old_state_chart_name, co_string)
    notifier.INFO('Create SC for Client Statement of Holding done')

    notifier.INFO('Create SC for Security Trade Confirmation')
    notifier.INFO('Define state transition SecurityTradeConf called')
    state_chart_name, state_chart_dict, co_string = define_state_transition_SecurityConfirmation()
    old_state_chart_name = ''
    create_state_charts(state_chart_name, state_chart_dict, old_state_chart_name, co_string)
    notifier.INFO('Create SC for Security Trade Confirmation done')

