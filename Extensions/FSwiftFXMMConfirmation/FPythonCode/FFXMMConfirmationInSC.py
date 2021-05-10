"""----------------------------------------------------------------------------
MODULE:
    FFXMMConfirmationInSC

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

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""

import FSwiftReaderLogger
notifier = FSwiftReaderLogger.FSwiftReaderLogger('FXMMConfIn', 'FFXMMConfirmationInNotify_Config')
import FMTStateChart


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

        state_chart_name = 'FSwiftFXMMConfirmationIn'
        old_state_chart_name = 'FXTradeConfMsg'
        state_chart = {
                        'Ready'                 :    {'Identified'                      :    'Paired',
                                                      'NotIdentified'                   :    'Unpaired'},
                        'Paired'                :    {'NoMatch'                         :    'Difference',
                                                      'Match'                           :    'Matched',
                                                      'Cancel'                          :    'Cancelled'},
                        'Unpaired'              :    {'Identified'                      :    'Paired',
                                                      'Amend'                           :    'Amended',
                                                      'Cancel'                          :    'Cancelled'},
                        'Difference'            :    {'ManuallyMatched'                 :    'Matched',
                                                      'Unpair'                          :    'Unpaired',
                                                      'Re-Match'                        :    'Paired',
                                                      'Amend'                           :    'Amended',
                                                      'Cancel'                          :    'Cancelled'},
                        'Matched'               :    {'Unpair'                          :    'Unpaired',
                                                      'Amend'                           :    'Amended',
                                                      'Cancel'                          :    'Cancelled'}
                    }
        return state_chart_name, state_chart, old_state_chart_name




def define_state_chart_narrative_in():
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

    state_chart_name = 'FSwiftNarrativeIn'
    old_state_chart_name = 'DebitCreditConfMsg'
    state_chart = {
                        'Ready'                 :    {'Identified'                    : 'Paired',
                                                      'NotIdentified'                 : 'Unpaired',
                                                      'IdentifiedForParty'            : 'PairedWithParty'},
                        'PairedWithParty'       :    {'ManuallyPaired'                : 'Paired'         },
                        'Unpaired'              :    {'Identified'                    : 'Paired',
                                                      'Ignore'                        : 'Ignored'        },
                        'Paired'                :     {'Unpair'                       : 'Unpaired'}
    }
    return state_chart_name, state_chart, old_state_chart_name


def create_fx_trade_conf_sc():
    state_chart_name, state_chart_dict, old_state_chart_name = define_state_transition()
    state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict, old_state_chart_name)



    # EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
    co_string = 'Ready,-500,0;Paired,-300,0;Matched,400,0;Unpaired,-300,-200;Cancelled,100,-200;Difference,100,200;Amended,400,200;'
    try:
        FMTStateChart.layout_state_chart(state_chart_name, co_string)
        notifier.INFO('Done with layout of state chart %s.'%state_chart_name)
    except Exception as e:
        notifier.WARN(str(e))

    state_chart_name, state_chart_dict, old_state_chart_name = define_state_chart_narrative_in()
    state_chart = FMTStateChart.create_state_chart(state_chart_name, state_chart_dict, old_state_chart_name)

    co_string = 'Ready,-500,0;Paired,-300,0;Matched,400,0;Unpaired,-300,-200;PairedWithParty,-300,200;Ignored, 100, -200;'
    try:
        FMTStateChart.layout_state_chart(state_chart_name, co_string)
        print(('Done with layout of state chart %s.' % state_chart_name))
    except Exception as e:
        notifier.WARN(str(e))

#create_fx_trade_conf_sc()
#delete_state_chart('FSwiftFXMMConfirmationIn')

