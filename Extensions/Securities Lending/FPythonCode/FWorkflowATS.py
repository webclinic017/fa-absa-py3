""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FWorkflowATS.py"
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
from collections import deque
import acm
import ael
import FAssetManagementUtils
from FParameterSettings import ParameterSettingsCreator
from FSecLendUtils import fn_timer
from FWorkflow import Logger
from FSecLendWorkflow import SETTINGS

logger = Logger()
settings = ParameterSettingsCreator.FromRootParameter('WorkflowATSSettings')
newBPs = deque()
workflowImplementations = dict()


def start():
    WorkflowImplementations()
    RecoverBusinessProcesses()
    logger.info('Starting Business Process subscriptions.')
    ael.BusinessProcess.subscribe(BusinessProcessCB)
    """
    for sc in workflowImplementations.keys():
        ael.BusinessProcess.subscribe(BusinessProcessCB, 'None',
                                      'state_chart_seqnbr = {}'.format(acm.FStateChart[sc].Oid()))
    """


def work():
    ProcessBusinessProcesses()


def stop():
    ael.BusinessProcess.unsubscribe(BusinessProcessCB)


def BusinessProcessCB(obj, ael_entity, arg, event):
    if event in ['insert', 'update'] and HasAELWorkflowImplementation(ael_entity):
        bp = acm.Ael.AelToFObject(ael_entity)
        if bp not in newBPs:
            newBPs.append(bp)


@fn_timer
def RecoverBusinessProcesses():
    for stateChart in list(workflowImplementations.keys()):
        dt = acm.Time.PeriodSymbolToDate(SETTINGS.RecoverFrom())
        query = acm.BusinessProcess().FindByStateChartQuery(stateChart)
        query.AddAttrNode('UpdateTime', 'GREATER_EQUAL', dt)
        for bp in query.Select():
            if bp.Subject() and \
                    HasWorkflowImplementation(bp) and \
                    HasWorkflowActions(bp):
                if bp not in newBPs:
                    newBPs.append(bp)
    logger.info('Recovering {} Business Processes. '.format(len(newBPs)))


def ProcessBusinessProcesses():
    while newBPs:
        bp = newBPs.popleft()
        if bp.Subject() and \
                HasWorkflowImplementation(bp) and \
                HasWorkflowActions(bp):
            workflowClass = WorkflowClass(bp.StateChart().Name())
            if not workflowClass.HasHandledStep(bp):
                logger.info('Processing Business Process {0}'.format(bp.Oid()))
                workflow = workflowClass(bp)
                workflow.HandleNewState()
                logger.debug('*' * 50)


def HasWorkflowImplementation(bp):
    return WorkflowClass(bp.StateChart().Name()) is not None


def HasAELWorkflowImplementation(ael_entity):
    return WorkflowClass(ael_entity.state_chart_seqnbr.name) is not None


def HasWorkflowEntryState(bp):
    workflowClass = WorkflowClass(bp.StateChart().Name())
    return workflowClass.IsEntryState(bp.CurrentStateName())


def HasWorkflowActionState(bp):
    workflowClass = WorkflowClass(bp.StateChart().Name())
    return workflowClass.IsActionState(bp.CurrentStateName())


def HasWorkflowActions(bp):
    workflowClass = WorkflowClass(bp.StateChart().Name())
    return (workflowClass.IsActionState(bp.CurrentStateName())) or \
           (workflowClass.IsEntryState(bp.CurrentStateName()))


def WorkflowClass(state_chart_name):
    return workflowImplementations.get(state_chart_name, None)


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
