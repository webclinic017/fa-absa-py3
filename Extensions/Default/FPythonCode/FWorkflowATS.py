""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FWorkflowATS.py"
"""--------------------------------------------------------------------------
MODULE
    FWorkflowATS

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    ATS for creating Business Processes, exeuting Action States and moving the Business Process for
    Workflow implementations. The ATS will handle Action States for all State Charts with a workflow 
    implementation that is included in the FParameter WorkflowATSSettings.Implementations. The parameter
    should be defined as a list of <moduleName>.<className> where the workflow is implemented.
-----------------------------------------------------------------------------"""

import acm
import ael
import FAssetManagementUtils
from FParameterSettings import ParameterSettingsCreator
from FWorkflow import Logger

logger = Logger()

newSteps = set()
workflowImplementations = dict()

def start():
    logger.info('Starting Business Process subscriptions.')
    WorkflowImplementations()        
    InitializeBusinessProcesses()
    ael.BusinessProcess.subscribe(BusinessProcessCB)

def work():
    ProcessBusinessProcesses()

def stop():
    ael.BusinessProcess.unsubscribe(BusinessProcessCB)

def BusinessProcessCB(obj, ael_entity, arg, event):
    if event in ['insert', 'update']:
        bp = acm.Ael.AelToFObject(ael_entity)
        if HasWorkflowImplementation(bp):
            newSteps.add(bp.CurrentStep())

def InitializeBusinessProcesses():
    for stateChart in list(workflowImplementations.keys()):
        for bp in acm.BusinessProcess.FindByStateChart(stateChart):
            if bp.Subject() and HasWorkflowImplementation(bp):
                newSteps.add(bp.CurrentStep())

def ProcessBusinessProcesses():
    while newSteps:
        step = newSteps.pop()
        businessProcess = step.BusinessProcess()
        workflowClass = WorkflowClass(businessProcess)
        if workflowClass.IsActionStep(step) and not workflowClass.HasHandledStep(step):
            logger.info('Processing Business Process {0}'.format(businessProcess.Oid()))
            workflow = workflowClass(businessProcess)
            workflow.HandleActionState()

def HasWorkflowImplementation(bp):
    return WorkflowClass(bp) is not None

def WorkflowClass(bp):
    return workflowImplementations.get(bp.StateChart().Name(), None)
    
def WorkflowImplementations():
    settings = ParameterSettingsCreator.FromRootParameter('WorkflowATSSettings')
    for classPath in settings.Implementations():
        cls = FAssetManagementUtils.GetFunction(classPath)
        cls.InitializeStateChart()
        workflowImplementations[cls.StateChart()] = cls
    
    for implementation in workflowImplementations:
        workflow = workflowImplementations.get(implementation, None)
        if workflow:
            workflow.StartUp()