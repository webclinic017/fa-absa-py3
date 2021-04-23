""" Compiled: 2014-02-11 17:11:58 """

"""-------------------------------------------------------------------------------------------------------
MODULE
    FBusinessProcessUtils

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Common utility functions

-------------------------------------------------------------------------------------------------------"""
import acm
import itertools
from collections import deque, defaultdict

BUSINESS_PROCESS_CACHE = dict()

def GetBusinessProcesses(trade):
    return acm.BusinessProcess.FindBySubjectAndStateChart(trade, None)

def GetBusinessProcessWithCache(subject, stateChartName):
    try:
        key = stateChartName + str(subject.Oid())
        businessProcess = BUSINESS_PROCESS_CACHE.get(key)
        if not businessProcess or businessProcess.IsDeleted():
            businessProcess = acm.BusinessProcess.FindBySubjectAndStateChart(subject, stateChartName)
            BUSINESS_PROCESS_CACHE[key] = businessProcess[0]
            return businessProcess[0]
        return businessProcess
    except (AttributeError, IndexError):
        return None

def GetOrCreateBusinessProcess(subject, stateChartName):
    assert(subject), "You need to supply a subject when creating a FBusinessProcess"
    bp = GetBusinessProcessWithCache(subject, stateChartName)
    if not bp:
        sc = acm.FStateChart[stateChartName]
        assert(sc), "No statechart with name %s" % stateChartName
        bp = acm.BusinessProcess.InitializeProcess(subject, sc)
    return bp

def CreateBusinessProcess(subject, stateChartName):
    assert(subject), "You need to supply a subject when creating a FBusinessProcess"
    sc = acm.FStateChart[stateChartName]
    assert(sc), "No statechart with name %s" % stateChartName
    bp = acm.BusinessProcess.InitializeProcess(subject, sc)
    return bp

def IsValidEvent(businessProcess, eventId):
    assert(businessProcess), 'IsValidEvent is called without a business process'
    currentStep = businessProcess.CurrentStep()
    assert(currentStep), 'BusinessProcess must have a current step'
    stateChartEvent = acm.FStateChartEvent(eventId)
    if stateChartEvent:
        return currentStep.IsValidEvent(stateChartEvent)
    return False

def SetBusinessProcessToError(businessProcess, reason):
    assert(businessProcess)
    businessProcess.ForceToErrorState(reason)
    businessProcess.Commit()

def SetBusinessProcessesToError(businessProcesses, reason):
    for bp in businessProcesses:
        SetBusinessProcessToError(bp, reason)
        
def EventsBetween(stateChart, fromState, toState):
    """ Shortest list of event names between two states 
        using Breadth-First search. 
    """
    
    def Pairs(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)
        
    def BreadthFirstSearch(graph, start, end): 
        queue = deque([(start, [start])])
        while queue:
            state, path = queue.popleft() 
            for next in set(graph[state]).difference(path):
                if next == end:
                    yield path + [next]
                else:
                    queue.append((next, path + [next]))
                    
    def ShortestPath(graph, start, end): 
        try:
            path = next(BreadthFirstSearch(graph, start, end))
            return [graph[fromState][toState] for fromState, toState
                in Pairs(path)]
        except StopIteration:
            return None
            
    def Graph(stateChart):
        graph = defaultdict(dict)
        for s in stateChart.States():
            for t in s.Transitions():
                graph[s.Name()][t.ToState().Name()] = t.EventName()
        return graph
        
    assert(stateChart)
    return ShortestPath(Graph(stateChart), fromState, toState)
    
    
def CurrentState(subject, stateChart):
    try:
        if stateChart.BusinessProcessesPerSubject() == 'Single':
            bp = GetBusinessProcessWithCache(subject, stateChart.Name())
            return bp.CurrentStep().State()
    except AttributeError:
        return None
