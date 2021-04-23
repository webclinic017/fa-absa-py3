"""----------------------------------------------------------------------------
MODULE:
    FCashOutSC

DESCRIPTION:
    OPEN EXTENSION MODULE
    State chart creation for cash settlement confirmation.
    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:
      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

FUNCTIONS:
    define_state_transition():
        Defines the state transition for state chart
    create_cash_settlement_conf_out_sc():
        Creates the state chart

VERSION: 3.0.0-0.5.3383

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import FSwiftWriterLogger
notifier = FSwiftWriterLogger.FSwiftWriterLogger('CashSetlemnt', 'FCashOutNotify_Config')
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

        state_chart_name = 'FSwiftCashOut'
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


def define_state_transition_MT304():
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

    state_chart_name = 'FSwiftCashOutMT304'
    state_chart = {
                    'Ready'                             : {'GenerateSWIFT' : 'SwiftMsgGenerated',
                                                           'Fail'          : 'GenerationFailed'},
                    'SwiftMsgGenerated'                 : {'Send'          : 'Sent',
                                                           'SendFail'      : 'SendFailed'},
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

def define_state_transition_4msgparent():
    """
    Create a state chart for 4 msg parent.
    """
    state_chart_name = 'FSwift4msgParent'
    state_chart = {
                'Ready':    {'RcvdAck'                         :    'OneSent',
                                                  'Fail'                            :    'OneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneSent':    {'RcvdAck'                         :    'TwoSent',
                                                  'Fail'                            :    'OneSentOneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'TwoSent':    {'RcvdAck'                         :    'ThreeSent',
                                                  'Fail'                            :    'TwoSentOneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'ThreeSent':    {'RcvdAck'                         :    'Acknowledged',
                                                  'Fail'                            :    'ThreeSentOneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneFailed':    {'RcvdAck'                         :    'OneSentOneFailed',
                                                  'Fail'                            :    'TwoFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneSentOneFailed':   {'RcvdAck'                          :    'TwoSentOneFailed',
                                                  'Fail'                            :    'OneSentTwoFailed',
                                                  'Resend'                          :    'OneSent',
                                                  'Cancel'                          :    'Cancelled'},
                'TwoSentOneFailed':   {'RcvdAck'                          :    'ThreeSentOneFailed',
                                                  'Fail'                            :    'TwoSentTwoFailed',
                                                  'Resend'                          :    'TwoSent',
                                                  'Cancel'                          :    'Cancelled'},
                'ThreeSentOneFailed':   {'Resend'                           :    'ThreeSent',
                                                  'Cancel'                          :    'Cancelled'},
                'TwoFailed':    {'RcvdAck'                         :    'OneSentTwoFailed',
                                                  'Fail'                            :    'ThreeFailed',
                                                  'Resend'                          :    'OneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneSentTwoFailed':   {'RcvdAck'                          :    'TwoSentTwoFailed',
                                                  'Fail'                            :    'OneSentThreeFailed',
                                                  'Resend'                          :    'OneSentOneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'TwoSentTwoFailed':   {'Resend'                           :    'TwoSentOneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'ThreeFailed':    {'RcvdAck'                         :    'OneSentThreeFailed',
                                                  'Fail'                            :    'FourFailed',
                                                  'Resend'                          :    'TwoFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneSentThreeFailed':   {'Resend'                           :    'OneSentTwoFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'FourFailed':   {'Resend'                           :    'ThreeFailed',
                                                  'Cancel'                          :    'Cancelled'},

}

    return state_chart_name, state_chart


def define_state_transition_3msgparent():
    """
    Create a state chart for 3 msg parent.
    """
    state_chart_name = 'FSwift3msgParent'
    state_chart = {
                'Ready':    {'RcvdAck'                         :    'OneSent',
                                                  'Fail'                            :    'OneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneSent':    {'RcvdAck'                         :    'TwoSent',
                                                  'Fail'                            :    'OneSentOneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'TwoSent':    {'RcvdAck'                         :    'Acknowledged',
                                                  'Fail'                            :    'TwoSentOneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneFailed':    {'RcvdAck'                         :    'OneSentOneFailed',
                                                  'Fail'                            :    'TwoFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneSentOneFailed':    {'RcvdAck'                         :    'TwoSentOneFailed',
                                                  'Fail'                            :    'OneSentTwoFailed',
                                                  'Resend'                          :    'OneSent',
                                                  'Cancel'                          :    'Cancelled'},
                'TwoSentOneFailed':    {'Resend'                          :    'TwoSent',
                                                  'Cancel'                          :    'Cancelled'},
                'TwoFailed':    {'RcvdAck'                         :    'OneSentTwoFailed',
                                                  'Fail'                            :    'ThreeFailed',
                                                  'Resend'                          :    'OneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneSentTwoFailed':    {'Resend'                          :    'OneSentOneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'ThreeFailed':    {'Resend'                          :    'TwoFailed',
                                                  'Cancel'                          :    'Cancelled'},

}


    return state_chart_name, state_chart


def define_state_transition_2msgparent():
    """
    Create a state chart for 2 msg parent.
    """
    state_chart_name = 'FSwift2msgParent'
    state_chart = {
                'Ready':    {'RcvdAck'                         :    'OneSent',
                                                  'Fail'                            :    'OneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneSent':    {'RcvdAck'                         :    'Acknowledged',
                                                  'Fail'                            :    'OneSentOneFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneFailed':    {'RcvdAck'                         :    'OneSentOneFailed',
                                                  'Fail'                            :    'TwoFailed',
                                                  'Cancel'                          :    'Cancelled'},
                'OneSentOneFailed':    {'Resend'                          :    'OneSent',
                                                  'Cancel'                          :    'Cancelled'},
                'TwoFailed':    {'Resend'                          :    'OneFailed',
                                                  'Cancel'                          :    'Cancelled'},

}


    return state_chart_name, state_chart


def define_state_transition_narrative():
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

        state_chart_name = 'FSwiftNarrativeOut'
        state_chart = {
            'Ready': {'GenerateSWIFT': 'SwiftMsgGenerated',
                      'Fail': 'GenerationFailed'},
            'SwiftMsgGenerated': {'Send': 'Sent',
                                  'SendFail': 'SendFailed',
                                  'Regenerate': 'Ready'},
            'GenerationFailed': {'Regenerate': 'Ready'},
            'SendFailed': {'ReSend': 'Sent',
                           'Regenerate': 'Ready'},
            'Sent': {'Ack': 'Acknowledged',
                     'Nack': 'SendFailed',
                     'Fail': 'SendFailed'},
        }
        return state_chart_name, state_chart


def create_cash_settlement_conf_out_sc():
    try:
        state_chart_name, state_chart_dict = define_state_transition()
        state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict)
        # EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
        co_string = 'Acknowledged, 332, 0;SwiftMsgGenerated, -220, 0;XMLGenerated, -300, 0;NetworkRulesValidated, -14, 0;SendFailed, 156, -204;GenerationFailed, -358, -203;Ready, -500, 0;Sent, 159, 0;'
        FMTStateChart.layout_state_chart(state_chart_name, co_string)

        state_chart_name, state_chart_dict = define_state_transition_MT304()
        state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict)
        # EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
        co_string = 'Duplicate,333,-123;XMLGenerated,-300,0;SwiftMsgGenerated,-220,0;Acknowledged,332,0;NetworkRulesValidated,-14,0;SendFailed,156,-204;GenerationFailed,-358,-203;Sent,159,0;Ready,-500,0;'
        FMTStateChart.layout_state_chart(state_chart_name, co_string)

        state_chart_name, state_chart_dict = define_state_transition_4msgparent()
        state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict)
        co_string = 'OneSentOneFailed,535,-227;Cancelled,1107,169;OneSentThreeFailed,537,92;FourFailed,217,277;ThreeFailed,218,87;OneSentTwoFailed,536,-68;ThreeSentOneFailed,1108,-218;ThreeSent,982,-407;OneFailed,222,-239;TwoSent,657,-402;OneSent,370,-402;TwoSentOneFailed,826,-228;Acknowledged,1278,-404;TwoSentTwoFailed,827,-60;TwoFailed,221,-71;Ready,71,-404;'
        FMTStateChart.layout_state_chart(state_chart_name, co_string)

        state_chart_name, state_chart_dict = define_state_transition_3msgparent()
        state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict)
        co_string = 'OneFailed,-54,-352;Cancelled,714,-9;ThreeFailed,-56,75;Acknowledged,899,-512;TwoFailed,-53,-151;Ready,-234,-519;OneSentOneFailed,326,-347;OneSent,167,-514;TwoSentOneFailed,715,-337;OneSentTwoFailed,325,-145;TwoSent,535,-515;'
        FMTStateChart.layout_state_chart(state_chart_name, co_string)

        state_chart_name, state_chart_dict = define_state_transition_2msgparent()
        state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict)
        co_string = 'TwoFailed,63,188;Acknowledged,542,-226;OneFailed,62,-44;Cancelled,464,189;Ready,-78,-225;OneSent,242,-229;OneSentOneFailed,396,-44;'
        FMTStateChart.layout_state_chart(state_chart_name, co_string)

        state_chart_name, state_chart_dict = define_state_transition_narrative()
        state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict)

        # EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
        co_string = 'Acknowledged, 332, 0;SwiftMsgGenerated, -220, 0;XMLGenerated, -300, 0;NetworkRulesValidated, -14, 0;SendFailed, 156, -204;GenerationFailed, -358, -203;Ready, -500, 0;Sent, 159, 0;'
        FMTStateChart.layout_state_chart(state_chart_name, co_string)

    except Exception as e:
        notifier.ERROR("Exception in create_cash_settlement_conf_out_sc : %s"%str(e))
        notifier.DEBUG(str(e), exc_info=1)

