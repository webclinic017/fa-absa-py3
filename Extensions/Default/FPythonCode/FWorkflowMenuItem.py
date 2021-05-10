""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FWorkflowMenuItem.py"
"""--------------------------------------------------------------------------
MODULE
    FWorkflowMenuItem

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Base class for menu items supporting workflows

-----------------------------------------------------------------------------"""

import acm
import FUxCore
import FBusinessProcessUtils

class WorkflowMenuItem(FUxCore.MenuItem, object):

    def __init__(self, extObj, workflow, event):
        self._frame = extObj
        self._workflow = workflow
        self._event = event
        
    def Workflow(self):
        return self._workflow
        
    def Event(self):
        return self._event
    
    def _RequiresComment(self):
        settings = self._workflow.Settings()
        return self.Event() in settings.EventsRequiringComment()
    
    def BusinessProcess(self):
        raise NotImplementedError
        
    def _HandleEvent(self, businessProcess, parameters=None, notes=None):
        self.Workflow()(businessProcess)._HandleEvent(self.Event(), parameters=parameters, notes=notes)
        
    def _CanHandleEvent(self, businessProcess):
        if businessProcess:
            return FBusinessProcessUtils.IsValidEvent(businessProcess, self.Event())
        else:
            return False
    
    def _SatisfiesCondition(self, businessProcess, parameters):
        step = businessProcess.CurrentStep()
        message = '{0} condition not satisfied for event "{1}"'
        try:
            assert step.IsExitConditionSatisfied(self.Event(), parameters), message.format('Exit', self.Event())           
            assert step.IsEntryConditionSatisfied(self.Event(), parameters), message.format('Entry', self.Event())
        except AssertionError as e:
            acm.UX.Dialogs().MessageBoxOKCancel(self._frame.Shell(), 'Warning', str(e))
            return False
        else:
            return True
    
    def _UserComment(self):
        if self._RequiresComment():
            return acm.UX.Dialogs().GetTextInput(self._frame.Shell(), 'Enter comment', None)

    def _NotesAndParameters(self):
        comment = self._UserComment()
        notes = [comment] if comment else []
        parameters = {'UserComment':bool(comment)}
        return notes, parameters

    def Enabled(self):
        return self._CanHandleEvent(self.BusinessProcess())
    
    def Invoke(self, eii):
        notes, parameters = self._NotesAndParameters()
        if self._SatisfiesCondition(self.BusinessProcess(), parameters):
            self._HandleEvent(self.BusinessProcess(), parameters, notes)

class MultiWorkflowMenuItem(WorkflowMenuItem):
    
    def BusinessProcesses(self):
        raise NotImplementedError
        
    def Enabled(self):
        if self.BusinessProcesses():
            return all(self._CanHandleEvent(bp) for bp in self.BusinessProcesses())
        else:
            return False
        
    def Invoke(self, eii):
        notes, parameters = self._NotesAndParameters()
        for bp in self.BusinessProcesses():
            if self._SatisfiesCondition(bp, parameters):
                self._HandleEvent(bp, parameters, notes)
