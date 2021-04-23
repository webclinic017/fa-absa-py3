""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FLimitUtils

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of helper classes and functions for limits management.

-------------------------------------------------------------------------------------------------------"""
import acm
import FStateChartUtils
from FLimitExceptions import EmptyCalculationError, TransformFunctionError
from FLimitTreeSpecification import LimitTreeSpecification

STATE_PRIORITY = [
    'Unknown',
    'Error',
    'Inactive',
    'Ready',
    'Active',
    'Under Investigation',
    'Warning',
    'Breached'
    ]
OPERATOR_ENUMS = {
    '>' : 'Greater',
    '<' : 'Less',
    '=' : 'Equal',
    '<>': 'Not Equal',
    '>=': 'Greater or Equal',
    '<=': 'Less or Equal'
    }
OPERATOR_SYMBOLS = dict(list(zip(OPERATOR_ENUMS.values(), OPERATOR_ENUMS.keys())))
CONSTRAINT_SEP = '/'
TARGET_SHEET_CLASSES = {
    acm.FRiskMatrixSheet: acm.FPortfolioSheet,
    acm.FVerticalPortfolioSheet: acm.FPortfolioSheet,
    }
VALID_SHEET_CLASSES = [
    acm.FPortfolioSheetBase, 
    acm.FRiskMatrixSheet,
    acm.FLimitSheet,
    acm.FSalesActivitySheet,
    acm.FSettlementSheet,
    acm.FTradeSheet,
    acm.FDealSheet
    ]
INVALID_ROW_OBJECTS = [
    acm.FDeliverableLinkAndTrades,
    acm.FCombInstrMapAndTrades,
    acm.FLegAndTrades
    ]


def AvailableValue(limit, currentValue=None):
    try:
        if currentValue is None:
            currentValue = CurrentValue(limit)
        if currentValue is not None:
            threshold = limit.Threshold()
            operator = limit.ComparisonOperator()
            if operator in ('Less', 'Less or Equal'):
                return min(threshold - currentValue, 0)
            elif operator in ('Greater', 'Greater or Equal'):
                return max(threshold - currentValue, 0)
            elif operator in ('Equal',):
                return threshold - currentValue
    except StandardError:
        pass
    return 0    
        
def BreachedAmount(limit, limitAvailability=None, currentValue=None):
    try:
        if (limitAvailability or 
            CurrentState(limit) in ('Ready', 'Error')):
            return 0
        if currentValue is None:
            currentValue = CurrentValue(limit)
        if currentValue is not None:
            return limit.Threshold() - currentValue
    except StandardError:
        pass
    return 0

def ColumnName(limit):
    return limit.LimitTarget().ColumnLabel()

def Constraints(limit):
    return limit.LimitTarget().Path()

def ConstraintsArray(limit):
    return limit.LimitTarget().PathAsArray(False)

def ConstraintsSummary(limit):
    constraints = ConstraintsArray(limit)
    if constraints:
        summary = [str(constraints[0]), ]
        if len(constraints) > 2:
            summary.append('...')
        if len(constraints) > 1:
            summary.append(str(constraints[-1]))
        return CONSTRAINT_SEP.join(summary)
    return ''

def CurrentState(limit):
    bp = limit.BusinessProcess()
    if bp:
        return bp.CurrentStep().State().Name()
    return 'Unknown'

def CurrentValue(limit):
    import FLimitMonitor
    try:
        if not limit.IsParent():
            monitoredLimit = FLimitMonitor.FMonitoredLimit(limit)
            return monitoredLimit.GetCurrentValue()
    except EmptyCalculationError:
        pass

def WarningValue(limit):
    value = limit.WarningValue()
    threshold = Threshold(limit)
    if not IsWarningEnabled(limit):
        value = threshold
    elif limit.PercentageWarning():
        operator = limit.ComparisonOperator()
        if operator in ('Greater', 'Greater or Equal'):
            value = threshold - (abs(threshold) * value / 100)
        else:
            value = threshold + (abs(threshold) * value / 100)
    return value

def WarningPercentage(limit):
    value = limit.WarningValue()
    threshold = Threshold(limit)
    if not IsWarningEnabled(limit) or not threshold:
        value = 0
    elif not limit.PercentageWarning():
        operator = limit.ComparisonOperator()
        if operator in ('Greater', 'Greater or Equal'):
            value = (threshold - value) * 100 / threshold
        else:
            value = (value - threshold) * 100 / threshold
    return abs(value)

def Threshold(limit):
    return limit.Threshold()

def ComparisonOperatorAsSymbol(enumString):
    return OPERATOR_SYMBOLS.get(enumString, '')

def ComparisonOperatorAsEnum(symbol):
    return OPERATOR_ENUMS.get(symbol, 'None')

def ComparisonOperatorSymbols():
    return OPERATOR_ENUMS.keys()

def InitialiseLimit(limit):
    bp = limit.BusinessProcess()
    if bp and bp.CurrentStep().IsInReadyState():
        try:
            bp.HandleEvent('Monitor Limit')
            bp.Commit()
        except StandardError as e:
            msg = 'Limit %d could not be initialised for monitoring: %s' % (limit.Oid(), e)
            raise ValueError(msg)

def IsActive(limit):
    # Assume active if business process doesn't exist. This can be the case if a
    # check is made while the limit is undergoing a business process event change
    return bool(CurrentState(limit) in ('Unknown', 'Active', 'Warning', 'Breached'))

def IsWarningEnabled(limit):
    return limit.ComparisonOperator() not in ('Equal', 'Not Equal')

def OriginObjectName(limit):
    try:
        return limit.LimitTarget().TreeSpecification().OriginObject().StringKey()
    except StandardError:
        return '<Deleted object>'

def TargetSheetType(cls):
    return TARGET_SHEET_CLASSES.get(cls, cls)

def CellRowObject(cell):
    try:
        return cell.CalculatedValue().Object()
    except AttributeError:
        return cell.RowObject()
        
def IsSupportedSheetClass(sheetClass):
    if isinstance(sheetClass, str):
        sheetClass = acm.FClass[sheetClass]
    return bool(sheetClass and 
           any(sheetClass.IncludesBehavior(cls) for cls in VALID_SHEET_CLASSES))

def IsSupportedCell(cell):
    calcSpec = cell.CalculationSpecification()
    treeSpec = LimitTreeSpecification(cell).TreeSpecification()
    rowObject = cell.RowObject()
    return (rowObject and
            rowObject.Class() not in INVALID_ROW_OBJECTS and
            calcSpec and calcSpec.ColumnName() and calcSpec.ContextName() and 
            treeSpec and treeSpec.OriginObject() and 
            (not treeSpec.OriginObject().Class().IncludesBehavior(acm.FASQLQueryFolder)))

def SuggestedLimitValue(value):
    try:
        if abs(value) > 100:
            # E.g. 2,983,667.1240061 -> 2,980,000.0
            numDigits = len(str(int(value))) - 3
            value = round(value, -numDigits)
    except StandardError:
        pass
    return value
    
def ActiveSheet(extObj):
    try:
        if hasattr(extObj, 'ActiveSheet'):
            return extObj.ActiveSheet()
        return ActiveSheet(extObj.CustomLayoutApplication())
    except AttributeError:
        return None

def IsMultiRow(rowObject):
    try:
        return not rowObject.IsSingleInstrument()
    except AttributeError:
        return (rowObject.IsKindOf(acm.FMultiInstrumentAndTrades) or
            rowObject.IsKindOf(acm.FTreeBuilderMultiItem) or
                rowObject.IsKindOf(acm.FLimitMultiItem) or
                rowObject.IsKindOf(acm.FStoredASQLQuery) or
                rowObject.IsKindOf(acm.FSettlementMultiItem))
        
def CreateStandardLimitStateChart(name='Limits'):
    limit = 'Single'
    layout = 'Inactive,118,6;Warning,271,-246;Ready,-67,-147;Breached,430,-153;' \
             'Under Investigation,430,7;Active,114,-149;'
    definition = {
        'Ready':                {'Monitor Limit': 'Active'},
        'Active':               {'Deactivate': 'Inactive',
                                 'Warn': 'Warning'},
        'Warning':              {'Breach': 'Breached',
                                 'Recede': 'Active'},
        'Inactive':             {'Activate': 'Active'},
        'Breached':             {'Investigate': 'Under Investigation',
                                 'Warn': 'Warning',
                                 'Recede': 'Active'},
        'Under Investigation':  {'Breach Accepted': 'Active',
                                 'Deactivate': 'Inactive'},
        }
    return FStateChartUtils.CreateStateChart( \
            name, definition, layout, limit)

def DefaultSuggestedName(limit):
    path = None
    if limit.LimitTarget():
        path = limit.LimitTarget().StringKey()
    else:
        path = '[Unknown Path]'
    return ' '.join([path, str(limit.ComparisonOperatorSymbol()), str(limit.Threshold())])

def SheetTypeDisplayName(sheetType):
    if sheetType:
        sheetDef = acm.Sheet.GetSheetDefinition(sheetType)
        return sheetDef.DisplayName() if sheetDef else ''
    else:
        return ''

def LimitTransformFunction(limit):
    ''' This function returns the acm function object used for limit value transformations.
        If no function is found, 'limitValue' is used '''
    transformFunctionCl = limit.TransformFunction()
    transformFunctionName = transformFunctionCl.Description() if transformFunctionCl else "limitValue"
    try:
        func = acm.GetFunction(transformFunctionName, 1)
    except StandardError as e:
        raise TransformFunctionError('Error when loading transform frunction "%s": %s'%(transformFunctionName,e))
    if transformFunctionName and not func:
        raise TransformFunctionError('Did not find transform function: "%s"'%transformFunctionName)
    if func and not func.Domain().IsKindOf(acm.FDoubleDomain):
        raise TransformFunctionError('Transform function "%s" does not return a double'%func)
    return func
    
def StartLimitApplication(eii):
    acm.StartApplication('Limit', None)