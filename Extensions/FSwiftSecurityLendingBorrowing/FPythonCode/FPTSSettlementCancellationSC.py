"""----------------------------------------------------------------------------
MODULE:
    FPTSSettlementCancellationSC

DESCRIPTION:
    OPEN EXTENSION MODULE
    State chart creation for FX trade confirmation.
    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:
      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

FUNCTIONS:
    define_state_transition():
        Defines the state transition for state chart
    create_fx_trade_conf_sc():
        Creates the state chart

VERSION: 2.1.1-0.5.2995

RESTRICTIONS/LIMITATIONS:
    1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
    2. This module is not customizable.
    3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftReaderLogger
import FMTStateChart


notifier = FSwiftReaderLogger.FSwiftReaderLogger('SBL', 'FSwiftSecurityLendingBorrowingOutNotify_Config')


def define_state_transition():
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

    state_chart_name = 'FPTSSettlementCancellation'
    state_chart = {
                    'Ready': {'Ack':'Acknowledged'},
                    'Acknowledged': {'Cancel':'Cancelled',
                                     'Fail': 'CancelFailed'},
                }
    return state_chart_name, state_chart


def create_custom_message_sc():
    state_chart_name, state_chart_dict = define_state_transition()
    state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict, '')

    # EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
    '''co_string = 'Acknowledged, 332, 0;SwiftMsgGenerated, -220, 0;XMLGenerated, -300, 0;NetworkRulesValidated, -14, 0;SendFailed, 156, -204;GenerationFailed, -358, -203;Ready, -500, 0;Sent, 159, 0;'
    try:
        FMTStateChart.layout_state_chart(state_chart_name, co_string)
        notifier.INFO('Done with layout of state chart %s.' % state_chart_name)
    except Exception, e:
        notifier.WARN(str(e))'''

#create_custom_message_sc()
#delete_state_chart('FPTSSettlementCancellation')
