""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/business_data_upload/../AM_common/FBusinessDataStateChartUpgrader.py"
"""--------------------------------------------------------------------------
MODULE
    BusinessDataStateChartUpgrader

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

    Used to update an existing state chart according to class specific
    specifications, defined as class variables. Used in the business data upload/
    reconciliation frameworks.

-----------------------------------------------------------------------------"""

import acm
import itertools
import operator
from FStateChartUtils import FStateChartUpdate
from FAssetManagementUtils import logger

# pylint: disable-msg=W0110
class BusinessDataStateChartUpgrader(object):
    ''' Generic state chart upgrade handler. Contains base functionality
        for upgrading business data state charts.

        The following dictionaries have to be set up in a certain way - 
        see the concrete child classes for examples of how to construct them.
    '''
    
    # {oldStateName : newStateName, ...}
    STATE_CHART_STATE_RENAME_DICT        =  {}  # (For renaming state chart states)
    
    # oldEventName : newEventName
    STATE_CHART_EVENT_RENAME_DICT        =  {}  # (For renaming events between states) 
    
    # {fromState : {eventName : toState}, ...}    
    STATE_CHART_TRANSITION_CREATE_DICT   =  {}  # (For adding state chart transitions)
    
    # {fromState : {eventName : toState}, ...}    
    STATE_CHART_TRANSITION_DELETE_DICT   =  {}  # (For deleting state chart transitions)
    
    ''' 
        ... 
        [ Define any other state chart specific structures
          to update 
        ]
        ...
    '''

    def __init__(self, stateChartName):
        self.stateChart = acm.FStateChart[stateChartName]
        assert self.stateChart != None, 'No state chart named %s exists' % stateChartName
        self.stateChartUpgrader = FStateChartUpdate(stateChartName)

    def StateChart(self):
        return self.stateChart
        
    def StateChartUpgrader(self):
        return self.stateChartUpgrader
        
    def HasDeprecatedStateNames(self):
        boolHasDeprStateNames = bool(len(filter(lambda s: s.Name() in 
                                                self.STATE_CHART_STATE_RENAME_DICT.keys(), 
                                                self.StateChart().States())))
        return boolHasDeprStateNames
        
    def HasDeprecatedEventNames(self):
        boolHasDeprEventNames = bool(len(filter(lambda t: t.EventName() in 
                                                self.STATE_CHART_EVENT_RENAME_DICT.keys(), 
                                                
                                                itertools.chain(t for t in itertools.chain(*[s.Transitions() for 
                                                                s in self.StateChart().States()])))))   
        return boolHasDeprEventNames
    
    def _CompareStateTransitionsWithDict(self, stateChartTransitionDict, compOperator):
        targetEvents = list()
        targetStateNames = stateChartTransitionDict.keys()
        for targetState in targetStateNames:
            targetEvents.extend([targetEventName for targetEventName in 
                                 stateChartTransitionDict.get(targetState).keys()])
                          
        filteredStates = filter(lambda s: s.Name() in stateChartTransitionDict.keys(), 
                                self.StateChart().States())
                         
        filteredEvents = list()
        eventNames = list(itertools.chain(t.EventName() for 
                          t in itertools.chain(*[s.Transitions() for 
                          s in filteredStates])))
        for eventName in eventNames:
            if eventName in targetEvents:
                filteredEvents.append(eventName)
                
        return compOperator(len(targetEvents), len(filteredEvents))
        
    def LacksRequiredEventTransitions(self):
        stateChartTransitionUpgrDict = self.STATE_CHART_TRANSITION_CREATE_DICT
        return self._CompareStateTransitionsWithDict(stateChartTransitionUpgrDict, operator.ne)
        
    def HasRedundantStateTransitions(self):
        stateChartTransitionDeleteDict = self.STATE_CHART_TRANSITION_DELETE_DICT
        return self._CompareStateTransitionsWithDict(stateChartTransitionDeleteDict, operator.eq)        
        
    def StateChartIsNotUpToDate(self):
        return (self.HasDeprecatedStateNames() or 
               self.LacksRequiredEventTransitions() or
               self.HasRedundantStateTransitions() or
               self.HasDeprecatedEventNames())
        
    def StateChartIsUpToDate(self):
        return not self.StateChartIsNotUpToDate()

    def EnsureUpgradedStateChart(self):
        ''' Add any logic here that effects whether the state chart
            needs to be upgraded. Only perform update operations if 
            the state chart is found to be out of date.
        '''
        if self.StateChartIsNotUpToDate():
            logger.info('State chart %s is not up to date. Initiating upgrade routines to ensure compatibility...' % self.StateChart().Name())        
            self._UpgradeStateChart()
            if self.StateChartIsUpToDate():
                logger.info('Successfully upgraded state chart %s' % self.StateChart().Name())   
            else:
                raise Exception('Could not upgrade state chart %s to concurrent status' % self.StateChart().Name())
            
    def _UpdateStateNames(self):
        statesToRenameDict = self.STATE_CHART_STATE_RENAME_DICT
        if statesToRenameDict:
            for fromStateName, toStateName in statesToRenameDict.items():
                self.StateChartUpgrader().RenameState(fromStateName, toStateName)  

    def _UpdateEventNames(self):
        eventsToRenameDict = self.STATE_CHART_EVENT_RENAME_DICT
        if eventsToRenameDict:
            for oldEventName, newEventName in eventsToRenameDict.items():
                self.StateChartUpgrader().RenameEvent(oldEventName, newEventName)

    def _CreateNewStateTransitions(self):
        stateTransitionsToCreateDict = self.STATE_CHART_TRANSITION_CREATE_DICT  
        if stateTransitionsToCreateDict:
            for fromState, transitionDict in stateTransitionsToCreateDict.items():
                if transitionDict:
                    for eventName, toState in transitionDict.items():
                        self.StateChartUpgrader().CreateStateTransition(fromState, toState, eventName)
                        
    def _DeleteStateTransitions(self):
        stateTransitionsToDeleteDict = self.STATE_CHART_TRANSITION_DELETE_DICT  
        if stateTransitionsToDeleteDict:
            for fromState, transitionDict in stateTransitionsToDeleteDict.items():
                if transitionDict:
                    for eventName, toState in transitionDict.items():
                        self.StateChartUpgrader().DeleteStateTransition(fromState, toState, eventName) 
                       
    def _UpgradeStateChart(self):
        self._UpdateStateNames()
        self._UpdateEventNames()
        self._DeleteStateTransitions()        
        self._CreateNewStateTransitions()
    
                                      
class BusinessDataUploadStateChartUpgrader(BusinessDataStateChartUpgrader):
    ''' Define state chart specific structures for upgrade
        in the business data upload solution
    '''
    
    STATE_CHART_EVENT_RENAME_DICT        = {'Re-run triggered' : 'Redo'}    
    
    STATE_CHART_TRANSITION_CREATE_DICT  = {'Discrepancy'      : {'Redo' :  'Ready'}, 
                                           'Invalid data'     : {'Redo' :  'Ready'}}
                                           
    STATE_CHART_TRANSITION_DELETE_DICT   = {'Discrepancy'      :  {'Corrected' : 'Ready',
                                                                   'Re-run triggered' : 'Ready'},
                                            'Invalid data'     :  {'Corrected' : 'Ready',
                                                                   'Re-run triggered' : 'Ready'}}
                                           
                                                             
    def __init__(self, stateChartName):
        super(BusinessDataUploadStateChartUpgrader, self).__init__(stateChartName)                                                             


class BusinessDataReconciliationStateChartUpgrader(BusinessDataStateChartUpgrader):
    ''' Define state chart specific structures for upgrade
        in the business data reconciliation solution
    '''
    
    STATE_CHART_STATE_RENAME_DICT       = {'Not in document'  : 'Missing in document'}
    
    STATE_CHART_EVENT_RENAME_DICT       = {'Re-run triggered' : 'Redo'}
    
    STATE_CHART_TRANSITION_CREATE_DICT =  {'Discrepancy'      :   {'Redo' :  'Ready'}, 
                                           'Unidentified'     :   {'Redo' :  'Ready'}}
                                           
    STATE_CHART_TRANSITION_DELETE_DICT  = {'Discrepancy'      :   {'Corrected' : 'Comparison',
                                                                   'Re-run triggered' : 'Ready'},     
                                           'Unidentified'     :   {'Re-run triggered' :  'Ready'}}
    
                                        
    def __init__(self, stateChartName):
        super(BusinessDataReconciliationStateChartUpgrader, self).__init__(stateChartName)