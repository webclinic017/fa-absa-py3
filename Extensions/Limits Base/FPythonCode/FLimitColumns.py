""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitColumns.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FLimitColumns

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Functions supporting limit trading sheet columns.

-----------------------------------------------------------------------------"""
import acm
import FLimitUtils


def LimitComparisonOperator(limit):
    return (FLimitUtils.ComparisonOperatorAsSymbol(limit.ComparisonOperator()) if limit else '')

def LimitCurrentValue(limit):
    if limit:
        return FLimitUtils.CurrentValue(limit)
    return 0

def LimitAvailableValue(limit, currentValue):
    try:
        return FLimitUtils.AvailableValue(limit, currentValue)
    except (RuntimeError, AttributeError):
        return 0
        
def LimitBreachedAmount(limit, availableValue, currentValue):
    try:
        return FLimitUtils.BreachedAmount(limit, availableValue, currentValue)
    except (RuntimeError, AttributeError):
        return 0

def LimitConstraintsSummary(limit):
    return FLimitUtils.ConstraintsSummary(limit)

def LimitConstraintLevel(limit, level):
    constraints = FLimitUtils.ConstraintsArray(limit)
    try:
        return constraints[level]
    except IndexError:
        pass
    return ''
    
def LimitsInRow(rowObject, _limits):
    return acm.Limits.FindByInstrumentAndTrades(rowObject)

def LimitsPerState(limits, stateName):
    _limits = acm.FSet()    
    for limit in limits:
        if FLimitUtils.CurrentState(limit) == stateName:
            _limits.Add(limit)
    return _limits


def LimitsWithTarget(limitTarget, _limits):
    return acm.Limits.FindByTreeSpecification(limitTarget.TreeSpecification())
    
def LimitsAsSet(list_1, list_2):
    return list_1.Union(list_2)

def Limits():
    return acm.FLimit.Select('')
    
def LimitStateCount(rowObject, state):
    if rowObject and rowObject.IsKindOf(acm.FBusinessProcess):
        return len([s for s in rowObject.VisitedStates() if s.Name() == state])
    return 0
    
def LimitLastBreach(rowObject):
    if rowObject and rowObject.IsKindOf(acm.FBusinessProcess):
        step = rowObject.CurrentStep()
        while step:
            if step.State().Name() == 'Breached':
                return step
            step = step.PreviousStep()
            
def LimitsCurrentState(limits):
    if limits:
        currentState = FLimitUtils.CurrentState
        statePriority = FLimitUtils.STATE_PRIORITY
        statePriorityDict = dict(list(zip(statePriority, range(len(statePriority)))))
        return statePriority[max((set([
            statePriorityDict.setdefault(currentState(l), 0)
            for l in limits])))]
        
def LimitsLastStateChange(limits):
    if limits:
        return acm.Time.DateTimeFromTime(
            max((l.BusinessProcess().CurrentStep().CreateTime() 
            for l in limits)))
    
def LimitsLastValueChange(limits):
    if limits:
        return acm.Time.DateTimeFromTime(
            max((l.LimitValue().UpdateTime() 
            for l in limits)))
    
def LimitsLastBreachTime(limits):
    limitLastBreach = LimitLastBreach
    lastBreachTimes = []
    for l in limits:
        lastBreach = limitLastBreach(l.BusinessProcess())
        if lastBreach:
            lastBreachTimes.append(lastBreach.CreateTime())
    if lastBreachTimes:
        lastBreachTime = max(lastBreachTimes)
        return (acm.Time.DateTimeFromTime(lastBreachTime)
            if lastBreachTime else None)

def IsActivateLimitSupported(rowObject):
    if rowObject and rowObject.IsKindOf(acm.FBusinessProcess):
        bp = rowObject
        return (bp.CurrentStep().IsValidEvent(acm.FStateChartEvent('Activate')) or
                bp.CurrentStep().IsValidEvent(acm.FStateChartEvent('Deactivate')))
    return False
    
def IsActiveLimit(rowObject):
    return rowObject and rowObject.CurrentStep().IsValidEvent(acm.FStateChartEvent('Deactivate'))

def IsInvestigateLimitSupported(rowObject):
    if rowObject and rowObject.IsKindOf(acm.FBusinessProcess):
        bp = rowObject
        return bp.CurrentStep().IsValidEvent(acm.FStateChartEvent('Investigate'))
    return False

def OnActivateCheckbox(row, _col, _cell, _activate, _operation):
    try:
        limit = _GetLimitFromRowObject(row)
        if not limit or not IsActivateLimitSupported(limit.BusinessProcess()):
            return
        bp = limit.BusinessProcess()            
        event = 'Deactivate' if IsActiveLimit(bp) else 'Activate'
        bp.HandleEvent(event)
        bp.Commit()
    except StandardError as e:
        print('Error on limit activate button:', e)

def OnInvestigateButton(invokationInfo):
    try:
        button = invokationInfo.Parameter('ClickedButton')
        limit = _GetLimitFromRowObject(button.RowObject())
        if not limit or not IsInvestigateLimitSupported(limit.BusinessProcess()):
            return
        bp = limit.BusinessProcess()
        bp.HandleEvent('Investigate')
        bp.Commit()
    except StandardError as e:
        print('Error on limit investigate button:', e)

def OnCreateLimitButton(invokationInfo):
    try:
        cell = invokationInfo.Parameter('Cell')
        if cell:
            rowObject = cell.RowObject()
            return bool(_GetLimitFromRowObject(rowObject))
    except StandardError as e:
        print('Error creating limit button:', e)

def _GetLimitFromRowObject(rowObject):
    if rowObject and rowObject.IsKindOf(acm.FLimit):
        return rowObject
    elif rowObject and rowObject.IsKindOf(acm.FBusinessProcess):
        subject = rowObject.Subject()
        if subject and subject.IsKindOf(acm.FLimit):
            return subject
    return None

def SaveThreshold(limit, _col, calcval, val, operation):
    if limit and str(operation) == 'insert':
        try:
            limit.Threshold(val)
            if not FLimitUtils.IsWarningEnabled(limit) and not limit.PercentageWarning():
                limit.WarningValue(FLimitUtils.WarningValue(limit))
        except StandardError as e:
            print('Error updating limit threshold:', e)
            limit.Undo()

def SaveComparisonOperator(limit, _col, calcval, val, operation):
    if limit and str(operation) == 'insert':
        try:
            val = FLimitUtils.ComparisonOperatorAsEnum(val)
            limit.ComparisonOperator(val)
            if not FLimitUtils.IsWarningEnabled(limit):
                limit.WarningValue(FLimitUtils.WarningPercentage(limit) 
                        if limit.PercentageWarning() else FLimitUtils.WarningValue(limit))
        except StandardError as e:
            print('Error updating limit comparison operator:', e)
            limit.Undo()

def AggregatedLimitCountAggregator(subresults):
    resultSet = set()
    for s in (subresult['aggregatedLimitCount'] for subresult in subresults):
        resultSet.update(s)
    return len(resultSet)

def LimitSheetType(limit):
    return FLimitUtils.SheetTypeDisplayName(limit.LimitTarget().SheetType()) if limit else ''

def GetLimitWarningValue(limit):
    return FLimitUtils.WarningValue(limit)

def SetLimitWarningValue(limit, val):
    try:
        if FLimitUtils.IsWarningEnabled(limit):
            if limit.PercentageWarning():
                # Calculate the percentage value to store
                limit.WarningValue(val)
                limit.PercentageWarning(False)
                val = FLimitUtils.WarningPercentage(limit)
                limit.PercentageWarning(True)
            limit.WarningValue(val)
        else:
            print('ERROR: Cannot modify warning value for limits with an ' \
                'equal/not equal comparison operator')
    except StandardError as e:
        print('Error updating limit warning value:', e)
        limit.Undo()

def GetWarningPercentage(limit):
    return FLimitUtils.WarningPercentage(limit)

def SetWarningPercentage(limit, val):
    try:
        if FLimitUtils.IsWarningEnabled(limit):
            if not limit.PercentageWarning():
                # Calculate the absolute value to store
                limit.WarningValue(val)
                limit.PercentageWarning(True)
                val = FLimitUtils.WarningValue(limit)
                limit.PercentageWarning(False)
            limit.WarningValue(val)
        else:
            print('ERROR: Cannot modify warning value for limits with an ' \
                'equal/not equal comparison operator')
    except StandardError as e:
        print('Error updating limit warning percentage:', e)
        limit.Undo()