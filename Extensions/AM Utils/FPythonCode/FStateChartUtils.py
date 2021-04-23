""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FStateChartUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FStateChartUtils

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    State Chart utility functions

-------------------------------------------------------------------------------------------------------"""

import acm
import FAssetManagementUtils

BUSINESS_PROCESS_CACHE = dict()
logger = FAssetManagementUtils.GetLogger()

BASE_STATES = ('Ready', 'Error')

def GetStateNamesFromDefinition(definition):
    # Get all states, including those referenced in transitions
    state_names = definition.keys()
    for all_transitions in definition.values():
        state_names.extend([s for s in all_transitions.values() if s not in state_names])
    return state_names

def CreateStateChart(name, definition, layout=None, limit='Unlimited'):
    """Creates a state chart with the given name, if required.

    The definition parameter must completely define the content of the business
    process state chart, including all states and transitions between them. Its
    format is a dictionary of states mapped to a dictionary of transitions as
    event->next_state items, e.g.:

      {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}

    All defined next_states values must be unique within a state's transitions
    (i.e. multiple events cannot lead to the same next_state).

    """
    sc = acm.FStateChart[name]
    if sc:
        return sc

    sc = acm.FStateChart(name=name)
    sc.BusinessProcessesPerSubject(limit)

    # Create all states, including those referenced in transitions
    state_names = GetStateNamesFromDefinition(definition)
    for state_name in (s for s in state_names if s not in BASE_STATES):
        sc.CreateState(state_name)
    sc.Commit()
    states = sc.StatesByName()

    # Link states based on transitions, creating events as required
    for state_name, transitions in definition.items():
        state = states.At(state_name)
        for event_name, to_state_name in transitions.items():
            event = acm.FStateChartEvent(event_name)
            to_state = states.At(to_state_name)
            state.CreateTransition(event, to_state)
    sc.Commit()

    if layout:
        sc.Layout().Text(layout)
        sc.Commit()
        logger.info('Successfully created state chart "{0}"'.format(sc.Name()))
    return sc


class FStateChartUpdate(object):
    """A class consisting of a set of tools for modifying existing state charts:
        - Create, rename and delete state transitions
        - Create, rename and delete states
        - Update state chart to new definition
        - Delete state charts

    """
    def __init__(self, stateChartName):
        self._stateChart = acm.FStateChart[stateChartName]
        assert self._stateChart, 'StateChart %s does not exist' % stateChartName
        self._states = self._stateChart.StatesByName()
        self._layout = self._stateChart.Layout()

    def GetAllStateTransitions(self):
        transitions = []
        for state in self._states.Values():
            transitions.extend(state.Transitions())
        return transitions
        
    def GetStateTransitions(self, fromStateName, toStateName, eventName):
        transitions = []
        for trans in self._states.At(fromStateName).Transitions() if fromStateName else self.GetAllStateTransitions():
            if (not fromStateName or trans.FromState().Name() == fromStateName) and \
                (not toStateName or trans.ToState().Name() == toStateName) and \
                (not eventName or trans.EventName() == eventName):
                    transitions.append(trans)
        return transitions

    def _DeleteStateTransitions(self, fromStateName, toStateName, eventName):
        transitions = GetStateTransitions(fromStateName, toStateName, eventName)
        for trans in transitions:
            trans.Delete()
            logger.info('Deleted event %s from state %s to %s', trans.EventName(), trans.FromState().Name(), trans.ToState().Name())
        if not transitions:
            msg = 'Can not delete transitions. Transitions'
            if eventName:
                msg += ' %s' % eventName
            if fromStateName:
                msg += " from state %s " % fromStateName
            if toStateName:
                msg += " to state %s" % toStateName
            msg += "do not exist."
            logger.info(msg)
            
    def DeleteStateTransitionsBetween(self, fromStateName, toStateName):
        self._DeleteStateTransitions(fromStateName, toStateName, None)

    def DeleteStateTransition(self, fromStateName, toStateName, eventName):
        self._DeleteStateTransitions(fromStateName, toStateName, eventName)

    def DeleteAllStateTransitionsFromState(self, fromStateName):
        self._DeleteStateTransitions(fromStateName, None, None)
            
    def DeleteAllStateTransitionsToState(self, toStateName):
        self._DeleteStateTransitions(None, toStateName, None)
        
    def _CreateStateTransition(self, fromStateName, toStateName, eventName):
        event = acm.FStateChartEvent(eventName)
        states = self._stateChart.StatesByName()
        fromState = states.At(fromStateName)
        toState = states.At(toStateName)
        fromState.CreateTransition(event, toState)
        self._stateChart.Commit()
        logger.info('Created event %s from state %s to %s', eventName, fromStateName, toStateName)

    def CreateStateTransition(self, fromStateName, toStateName, eventName):
        if not self.GetStateTransitions(fromStateName, toStateName, eventName):
            self._CreateStateTransition(fromStateName, toStateName, eventName)
        else:
            logger.info('Transition %s from state %s to state %s already exists', eventName, fromStateName, toStateName)

    def CreateState(self, stateName):
        state = self._states.At(stateName)
        if not state:
            self._stateChart.CreateState(stateName)
            self._stateChart.Commit()
            logger.info('Created state %s', stateName)
            self._states = self._stateChart.StatesByName()
        else:
            logger.info('Can not create state %s. State already exists', stateName)
    
    def DeleteState(self, stateName):
        state = self._states.At(stateName)
        if state:
            state.Delete()
            logger.info('Deleted state %s', stateName)
            self._states = self._stateChart.StatesByName()
        else:
            logger.info('Can not delete state %s. State does not exists', stateName)

    def RenameEvent(self, oldEventName, newEventName):
        for transition in self.GetStateTransitions(None, None, oldEventName):
            transition.EventName(newEventName)
            transition.Commit()
            if transition.EventName() == newEventName:
                logger.info('Renamed event %s from state %s to state %s to name %s' % (oldEventName, transition.FromState().Name(),
                                                                                       transition.ToState().Name(), newEventName))

    def RenameState(self, oldStateName, newStateName, renameBusinessProcessSteps = True):
        state = self._states.At(oldStateName)
        if state:
            logger.info('State %s in state chart %s was found to be out of date. Updating...' %
                       (oldStateName, self._stateChart.Name()))
            state.Name(newStateName)
            state.Commit()
            if state.Name() == newStateName:
                if self._layout:
                    self._layout.Text = self._layout.Text().replace(oldStateName, newStateName)
                    self._stateChart.Commit()
                if renameBusinessProcessSteps:
                    bpSteps = [step for step in acm.FBusinessProcessStep.Select("stateName = '%s'" % oldStateName) if step.BusinessProcess().StateChart() == self._stateChart]
                    logger.info('%d business process steps to update' % len(bpSteps))
                    for step in bpSteps:
                        try:
                            step.StateName = newStateName
                            step.Commit()
                        except Exception as e:
                            logger.error('Failed to update business process step in bp %d [%s]' % (step.BusinessProcess().Oid(), e))
                self._states = self._stateChart.StatesByName()
                logger.info('Previous state %s in state chart %s was successfully renamed to %s.' %
                           (oldStateName, self._stateChart.Name(), state.Name()))
        else:
            logger.info('State chart %s does not have a state named %s to rename.' %
                       (self._stateChart.Name(), oldStateName))
    
    def UpdateStateChart(self, definition, layout=None, renamedStates = {}):
        currentStates = set(self._states) - set(BASE_STATES)
        newStates = set(GetStateNamesFromDefinition(definition)) - set(BASE_STATES)
        statesToRemove = currentStates - newStates
        statesToAdd = newStates - currentStates
        
        for oldStateName, newStateName in renamedStates.items():
            if oldStateName in statesToRemove and newStateName in statesToAdd:
                self.RenameState(oldStateName, newStateName)
                statesToRemove.remove(oldStateName)
                statesToAdd.remove(newStateName)
        
        for newStateName in statesToAdd:
            self.CreateState(newStateName)
        
        for oldStateName in statesToRemove:
            self.DeleteState(oldStateName)
        
        for stateName, newTransitions in definition.items():
            state = self._states.At(stateName)
            currentTransitions = dict((t.EventName(), t) for t in state.Transitions())
            transitionsToRemove = set(currentTransitions) - set(newTransitions)
            transitionsToAdd = set(newTransitions) - set(currentTransitions)
            for eventName in transitionsToRemove:
                trans = currentTransitions[eventName]
                trans.Delete()
                logger.info('Deleted event %s from state %s to %s', trans.EventName(), trans.FromState().Name(), trans.ToState().Name())
            for eventName in set(currentTransitions) & set(newTransitions):
                trans = currentTransitions[eventName]
                if not trans.ToState() or trans.ToState().Name() != newTransitions[eventName]:
                    trans.ToState = self._states.At(newTransitions[eventName])
                    trans.Commit()
                    logger.info('Changed event %s from state %s to %s', trans.EventName(), trans.FromState().Name(), trans.ToState().Name())
            for eventName in transitionsToAdd:
                self.CreateStateTransition(stateName, newTransitions[eventName], eventName)

        if layout:
            self._layout.Text = layout
            self._stateChart.Commit()
        
        self._states = self._stateChart.StatesByName()
        logger.info('Updated state chart "{0}"'.format(self._stateChart.Name()))    
            
    def _DeleteBusinessProcesses(self):
        businessProcesses = acm.BusinessProcess.FindByStateChart(self._stateChart)
        if businessProcesses:
            nr = len(businessProcesses)
            businessProcesses.Delete()
            logger.info('%i Business Processes deleted', nr)

    def _DeleteStateChart(self):
        stateChartName = self._stateChart.Name()
        self._stateChart.Delete()
        logger.info('State Chart %s deleted', stateChartName)

    def DeleteStateChart(self):
        self._DeleteBusinessProcesses()
        self._DeleteStateChart()
