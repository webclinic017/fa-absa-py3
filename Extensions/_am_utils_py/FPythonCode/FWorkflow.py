""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FWorkflow.py"
"""-------------------------------------------------------------------------------------------
MODULE
    FWorkflow

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Base class used to define a workflow with State Charts by linking certain states to python methods.
    The methods are linked by naming convention and by decorating them with the ActionState decorator
    and should return the next event based on the result of the action. By accessing Business Processes
    and handling events through a Workflow class the State Chart can be used to define and customize 
    the workflow.
-------------------------------------------------------------------------------------------"""

import acm
import FBusinessProcessUtils as utils
import FStateChartUtils
from FParameterSettings import ParameterSettingsCreator
from FLogger import FLogger

def Logger():
    LEVELS = {'info': 1, 'debug': 2, 'error': 3}
    settings = ParameterSettingsCreator.FromRootParameter('WorkflowATSSettings')
    logLevel = settings.Log()
    level = logLevel.lower() if logLevel else 'info'
    LOGGER = FLogger.GetLogger(name='Workflow')
    LOGGER.Reinitialize(
        level=LEVELS.get(level),
        logToConsole=1)
    return LOGGER
LOGGER = Logger()

class ActionState(object):
    """ Decorator to mark methods as linked to an action state. Method should be named the same as the
        linked state in the State Chart. Method should return a string with the next event or a tuple 
        with the event, parameters and notes when applicable. """

    def __init__(self, func):
        self._func = func
        self._instance = None

    def __call__(self, **kwargs):
        return self._func(self._instance, **kwargs)

    def __get__(self, instance, cls):
        self._instance = instance
        return self

class Workflow(object):

    def __init__(self, businessProcess):
        self._businessProcess = businessProcess
    
    @classmethod
    def StartUp(cls):
        """ Called when Workflow ATS is started """ 
        pass
    
    @classmethod
    def StateChart(cls):
        """ Return name of state chart """
        raise NotImplementedError
    
    def SubjectName(self):
        return self.Subject().Name() if self.Subject() is not None else None
    
    @classmethod
    def Settings(cls):
        try:
            return ParameterSettingsCreator.FromRootParameter('{0}Settings'.format(cls.__name__))
        except AttributeError as e:
            LOGGER.debug('No FParameter with name {0}Settings found'.format(cls.__name__))
            return None
    
    @classmethod
    def InitializeFromSubject(cls, subject):
        cls.InitializeStateChart()
        businessProcess = utils.GetOrCreateBusinessProcess(subject, cls.StateChart())
        if businessProcess.IsInfant():
            businessProcess.Commit()
            LOGGER.info('Created business process {0}'
                ''.format(businessProcess.Oid()))
        return cls(businessProcess)

    def BusinessProcess(self):
        return self._businessProcess

    def Subject(self):
        return self.BusinessProcess().Subject()
    
    def CurrentStep(self):
        return self._businessProcess.CurrentStep()
    
    def CurrentState(self):
        return self.BusinessProcess().CurrentStep().State().Name()

    def WriteToDiary(self, step=None, notes=None, parameters=None):
        step = step or self.BusinessProcess().CurrentStep()
        entry = acm.FBusinessProcessDiaryEntry()
        entry.Notes(notes)
        entry.Parameters(parameters)
        diary = self.BusinessProcess().Diary()
        diary.PutEntry(self.BusinessProcess(), step, entry)
        diary.Commit()
        LOGGER.debug('Saving business process {0} diary'
                ''.format(self.BusinessProcess().Oid()))

    def HandleEvent(self, eventName, parameters=None, notes=None):
        self._ValidateEvent(eventName)
        self._HandleEvent(eventName, parameters, notes)
        self.HandleActionState()

    def HandleError(self, error):
        LOGGER.debug('Handle Error "{0}" for Subject {1} Business Process {2}'
                ''.format(error, self.SubjectName(), self.BusinessProcess().Oid()))
        utils.SetBusinessProcessToError(self.BusinessProcess(), str(error))

    def RevertError(self):
        try:
            self._HandleEvent('Revert')
        except RuntimeError:
            self.BusinessProcess().Undo()

    def Retry(self, **kwargs):
        # If revert puts bp back in an action state without running function
        self.HandleActionState()

    @classmethod
    def HasHandledStep(cls, step):
        return step is not step.BusinessProcess().CurrentStep()
        
    @classmethod
    def IsActionStep(cls, step):
        return cls._ActionStateMethod(step.State().Name()) is not None

    def _ValidateEvent(self, eventName):
        if not utils.IsValidEvent(self.BusinessProcess(), eventName):
            raise ValueError("{0} cannot handle event '{1}' "
                             "in current state '{2}'".format(self.__class__.__name__,
                                                           eventName,
                                                           self.CurrentState()))
        
    def _HandleEvent(self, eventName, parameters=None, notes=None):
        LOGGER.debug('Handle Event "{0}" from state "{1}" for Subject {2}, Business Process {3}'
                    ''.format(eventName, self.CurrentState(), self.SubjectName(), self.BusinessProcess().Oid()))
        self.BusinessProcess().HandleEvent(eventName, parameters, notes)
        self.BusinessProcess().Commit()

    def HandleActionState(self):
        actionFunc = self._ActionStateFunction(self.CurrentState())
        if actionFunc:
            try:
                eventResult = actionFunc()
            except StandardError as error:
                self.HandleError(error)
            else:
                self._HandleActionStepResult(eventResult)
    
    def _HandleActionStepResult(self, eventResult):
        if isinstance(eventResult, str):
            self.HandleEvent(eventResult)
        else:
            self.HandleEvent(*eventResult)

    def _ActionStateFunction(self, state):
        stateMethod = self.__class__._ActionStateMethod(state)
        if stateMethod is not None:
            stateFunc = getattr(self, stateMethod)
            if isinstance(stateFunc, ActionState):
                return stateFunc
    
    @classmethod
    def _ActionStateMethod(cls, state):
        stateMethod = cls._MethodNameFromState(state)
        if hasattr(cls, stateMethod):
            stateFunc = getattr(cls, stateMethod)
            if isinstance(stateFunc, ActionState):
                return stateMethod 

    @staticmethod
    def _MethodNameFromState(state):
        return state.replace(' ', '')

    @classmethod
    def InitializeStateChart(cls):
        FStateChartUtils.CreateStateChart(cls.StateChart(),
                                          cls.StateChartDefinition.DEFINITION,
                                          layout=cls.StateChartDefinition.LAYOUT,
                                          limit='Single')

    class StateChartDefinition(object):
        """ Used to specify the states, events and layout of the State Chart when first created.
        Should be defined as:
        DEFINITION = {'state a':  {'event to go to b': 'state b', 'event to go to c': 'state c'}}
        LAYOUT = 'state a,50,50;state b,100,100;'
        """
        DEFINITION = None
        LAYOUT = None


class AsynchronousWorkflow(Workflow):
    """ Use when when the Action State functions in the workflow are asychronous. Action State functions should
        return an object of type AsynchEventResult instead of a string. When the function is done it should call
        AsynchEventResult.Event(eventName) and the Business Process will be moved """
    
    CURRENT_HANDLED_STEPS = []
    
    def __init__(self, businessProcess):
        super(AsynchronousWorkflow, self).__init__(businessProcess)
        self._activeEventResult = None
    
    def HandleActionState(self):
        actionFunc = self._ActionStateFunction(self.CurrentState())
        if actionFunc:
            try:
                eventResult = actionFunc()
            except StandardError as error:
                self.HandleError(error)
            else:
                if eventResult.Event():
                    self._HandleActionStepResult(eventResult.Event())
                else:
                    self.CURRENT_HANDLED_STEPS.append(self.CurrentStep())
                    self._activeEventResult = eventResult
                    eventResult.AddDependent(self)
    
    @classmethod
    def HasHandledStep(cls, step):
        if not super(AsynchronousWorkflow, cls).HasHandledStep(step):
            return step in cls.CURRENT_HANDLED_STEPS
        else:
            return True
    
    def ServerUpdate(self, sender, aspect, param):
        try:
            eventResult = self.AsynchEventResult(array=sender)
            if eventResult.Event():
                self._activeEventResult = None
                eventResult.RemoveDependent(self)
                self.CURRENT_HANDLED_STEPS.remove(self.CurrentStep())
                self._HandleActionStepResult(eventResult.Event())
        except Exception as error:
            self.HandleError(error)

    class AsynchEventResult(object):

        def __init__(self, array=None, event=None):
            self._array = array or acm.FArray()
            if event:
                self.Event(event)

        def AddDependent(self, dependent):
            self._array.AddDependent(dependent)

        def RemoveDependent(self, dependent):
            self._array.RemoveDependent(dependent)

        def Event(self, event=None):
            if event is None:
                try:
                    return self._array.First()
                except RuntimeError:
                    return None
            else:
                self._array.Add(event)
