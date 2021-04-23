"""----------------------------------------------------------------------------
MODULE:
    FXTradeConf_DataPrep

DESCRIPTION:
    Data preparation script for FXTradeConf
        Scripts performs following tasks:
        A. creates FX trade confirmation state chart
        B. Unidentified business process query
        C. Additional infos
     Note:
        Make sure that FSwiftReader and FXTradeConf extension modules are present
        in extension manager.

(c) Copyright 2016 FIS FRONT ARENA. All rights reserved.
----------------------------------------------------------------------------"""
import acm
import FTRADSUtils


def define_state_transition():
    '''
    Creates a state chart with the given name, if required.
    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:

      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

    All defined next_states values must be unique within a state's transitions
    (i.e. multiple events cannot lead to the same next_state).
    '''

    state_chart_name = get_trads_state_chart_name()
    state_chart = {
        'Ready': {'sendOur': 'SentOur',
                    'fail' : 'Failed'},
        
        'SentOur' :{'sendTheir' : 'SentTheir',
                    'cancel' : 'SentOurCancel',
                    'ack' : 'OneAck',
                    'nack' : 'Failed'},

        'SentOurCancel' :{'sendTheirCancel' : 'SentTheirCancel',
                    'ack' : 'OneAckCancel',
                    'nack' : 'CancelFailed'},
        
        'SentTheir' :{'cancel' : 'SentOurCancel',
                      'ack' : 'OneAck',
                      'nack' : 'Failed'},
                      
        'SentTheirCancel' :{'ack' : 'OneAckCancel',
                      'nack' : 'CancelFailed'},
                      
        'Cancelled' : { 'amend' : 'SentOur' },
        
        'OneAck' : { 'sentTheir' : 'OneAck',
                    'ack' : 'Reported',
                    'nack' : 'Failed',
                    'cancel' : 'SentOurCancel',
                    'amend' : 'SentOur'},

        'OneAckCancel' : { 'SentTheirCancel' : 'OneAckCancel',
                    'ack' : 'Cancelled',
                    'nack' : 'CancelFailed',
                    'amend' : 'SentOur'},
                    
        'Reported' : {'amend' : 'SentOur',
                      'cancel' : 'SentOurCancel'},
                      
        'Failed' : { 'report' : 'SentOur',
                     'nack' : 'Failed'},
                     
        'CancelFailed' : { 'cancel' : 'SentOurCancel',
                           'nack' : 'CancelFailed',
                           'amend' : 'SentOur'}
    }
    return state_chart_name, state_chart

def get_trads_state_chart_name():
    return FTRADSUtils.get_trads_state_chart_name()
    #return 'FAPAStateChart_20'

def get_states(definition):
    '''Get state names from transition dictionary.'''
    state_names = set(definition.keys()) # Get from_state
    for all_transitions in list(definition.values()): # Get to_state for each from_state
        to_states = set(all_transitions.values())
        state_names = state_names | to_states # Add to_state to from_state
    return state_names

def create_states(sc, state_names):
    '''Create states for given state chart'''
    existing_states = sc.StatesByName()
    for state_name in state_names:
        if state_name not in existing_states:
            sc.CreateState(state_name)
    sc.Commit()

def create_transitions(sc, definition):
    '''Create events for given state chart from transition dictionary.'''
    states = sc.StatesByName()
    for state_name, transitions in list(definition.items()):
        state = states.At(state_name)
        for event_name, to_state_name in list(transitions.items()):
            event = acm.FStateChartEvent(event_name)
            if not state.TransitionForEvent(event):
                to_state = states.At(to_state_name)
                state.CreateTransition(event, to_state)
    sc.Commit()

def layout_state_chart(state_chart_name, co_string):
    ''' Layout state chart with the given name from given coordinate string. '''
    state_chart = acm.FStateChart[state_chart_name]
    if not state_chart:
        notifier.ERROR('The state chart %s is not present in ADS.' % state_chart_name)
    else:
        state_chart.Layout().Text(co_string)
        state_chart.Layout().Commit()

def create_state_chart(state_chart_name, definition):
    '''Creates a state chart with the given name, if required.

    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:

      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

    All defined next_states values must be unique within a state's transitions
    (i.e. multiple events cannot lead to the same next_state).

    '''
    sc = acm.FStateChart[state_chart_name]
    if not sc:
        sc = acm.FStateChart(name=state_chart_name)
    state_names = get_states(definition)
    create_states(sc, state_names)
    create_transitions(sc, definition)
    return sc

def get_operation_component_type():
    """ Get Operation component type"""
    componentTypes = acm.FEnumeration['enum(ComponentType)']
    return componentTypes.Enumeration('Operation')

def get_operation_component(operation):
    """ Returns true if given operation exists else False"""
    is_operation_exist = True
    compType = 'Operation'
    queryString = 'name=\'%s\' and type=\'%s\'' % (operation, compType)
    op_comp = acm.FComponent.Select01(queryString, '')
    return op_comp

def add_operation(operationName):
    """ Add component of type operation"""
    op_comp = get_operation_component(operationName)
    if not op_comp:
        operation = get_operation_component_type()
        op_comp = acm.FComponent()
        op_comp.Name(operationName)
        op_comp.Type(operation)
        op_comp.Commit()
    return op_comp

def create_trads_sc():
    state_chart_name, state_chart_dict = define_state_transition()
    state_chart = create_state_chart(state_chart_name, state_chart_dict)

    # EDIT 'coordinate string' ONLY IF STATE CHART MENTIONED ABOVE IS CHANGED.
    co_string = 'SentOur,-177,-54;Sent,-135,52;Reported,292,127;Cancelled,296,-285;Failed,-263,155;CancelSent,0,-140;Amended,304,109;SentTheir,116,-54;SentTheirCancel,155,-274;SentOurCancel,-148,-279;OneAck,-62,168;CancelFailed,-284,-436;OneAckCancel,65,-454;Ready,-336,-57;'

    layout_state_chart(state_chart_name, co_string)

def create_and_get_trads_user_profile():
    if not acm.FUserProfile['TRADS']:
        user_prof = acm.FUserProfile()
        user_prof.Name('TRADS')
        user_prof.Commit()
    return acm.FUserProfile['TRADS']

def link_component_to_user_profile(user_prof, comp_id):
    try:
        query = 'userProfile=%d and component=%d' % (user_prof.Oid(), comp_id)
        if not acm.FProfileComponent.Select01(query, ''):
            pc = acm.FProfileComponent()
            pc.UserProfile(user_prof)
            pc.Component(comp_id)
            pc.Commit()
    except Exception as e:
        print('Failed to link operation %d to user profile %s' % (comp_id, user_prof.Name()))
        print(e)

def create_operations_for_trads_sc_and_link_them_to_trads(user_prof):
    state_chart_name, state_chart_dict = define_state_transition()
    operation_name_preamble = 'BPR_' + state_chart_name + '_'
    for each_state, transitions in state_chart_dict.items():
        for each_transition in transitions:
            operation_name = operation_name_preamble + each_transition
            op_comp = add_operation(operation_name)
            link_component_to_user_profile(user_prof, op_comp.Oid())

create_trads_sc()
user_prof = create_and_get_trads_user_profile()
create_operations_for_trads_sc_and_link_them_to_trads(user_prof)
