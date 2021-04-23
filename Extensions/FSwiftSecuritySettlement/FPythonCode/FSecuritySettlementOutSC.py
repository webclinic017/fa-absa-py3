"""----------------------------------------------------------------------------
MODULE:
    FSecuritySettlementOutSC

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
        Defines the state transition for state chart
    create_sec_settlement_conf_out_sc():
        Creates the state chart

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftWriterLogger
notifier = FSwiftWriterLogger.FSwiftWriterLogger('SecSetOut', 'FSecuritySettlementOutNotify_Config')
import FMTStateChart
import FOutStateChart

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

        state_chart_name = 'FSwiftSecuritySettlementOut'
        state_chart = {
                        'Ready':    {'GenerateSWIFT'                   :    'SwiftMsgGenerated',
                                                      'Fail'                            :    'GenerationFailed'},
                        'SwiftMsgGenerated':    {'Send'                            :    'Sent',
                                                      'SendFail'                        :    'SendFailed'},
                        'GenerationFailed':    {'Regenerate'                      :    'Ready'},
                        'SendFailed':    {'ReSend'                          :    'Sent',
                                                      'Regenerate'                      :    'Ready'},
                        'Sent':    {'Ack'                             :    'Acknowledged',
                                                      'Nack'                            :    'SendFailed',
                                                      'Fail'                            :    'SendFailed'},
                    }
        return state_chart_name, state_chart


def define_state_transition_trade_confirmation():
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

    state_chart_name = 'FSwiftSecurityConfirmationOut'
    state_chart = {
                    'Ready'                             : {'GenerateSWIFT' : 'SwiftMsgGenerated',
                                                           'Fail'          : 'GenerationFailed'},

                    'SwiftMsgGenerated'                 : {'Send'          : 'Sent',
                                                           'SendFail'      : 'SendFailed',
                                                           'Regenerate': 'Ready'},       # check

                    'GenerationFailed'                  : {'Regenerate'    : 'Ready'},

                    'SendFailed'                        : {'ReSend'        : 'Sent',
                                                           'Regenerate'    : 'Ready'},

                    'Sent'                              : {'Ack'           : 'Acknowledged',
                                                           'Nack'          : 'SendFailed',
                                                           'Fail'          : 'SendFailed'},

                    'Acknowledged'                      : {'Dupl'          : 'Duplicate'},

                    'Duplicate'                         : {'Ack'           : 'Acknowledged',
                                                           'Dupl'          : 'Duplicate'}

    }
    return state_chart_name, state_chart


def create_narrative_out_sc():
    """ create free format message StateChart"""
    FOutStateChart.create_out_statechart('FSwiftNarrativeOut', notifier)

def create_sec_settlement_conf_out_sc():
    try:
        state_chart_name, state_chart_dict = define_state_transition()
        state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict)
        # EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
        co_string = 'Acknowledged, 332, 0;SwiftMsgGenerated, -220, 0;XMLGenerated, -300, 0;NetworkRulesValidated, -14, 0;SendFailed, 156, -204;GenerationFailed, -358, -203;Ready, -500, 0;Sent, 159, 0;'
        FMTStateChart.layout_state_chart(state_chart_name, co_string)

        state_chart_name, state_chart_dict = define_state_transition_trade_confirmation()
        state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict)
        # EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
        co_string = 'Duplicate,333,-123;XMLGenerated,-300,0;SwiftMsgGenerated,-220,0;Acknowledged,332,0;NetworkRulesValidated,-14,0;SendFailed,156,-204;GenerationFailed,-358,-203;Sent,159,0;Ready,-500,0;'
        FMTStateChart.layout_state_chart(state_chart_name, co_string)

    except Exception as e:
        notifier.ERROR("Exception in create_cash_settlement_conf_out_sc : %s"%str(e))
        notifier.DEBUG(str(e), exc_info=1)




