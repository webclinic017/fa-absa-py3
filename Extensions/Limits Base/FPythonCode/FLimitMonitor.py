""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitMonitor.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitMonitor

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Provides functionality for monitoring limit calculations.

-----------------------------------------------------------------------------"""
from contextlib import contextmanager
from collections import deque
import math
import numbers
import operator

import acm
import FAssetManagementUtils
import FLimitSettings
import FLimitUtils

from FLimitExceptions import (
        CreateCalculationError, 
        EmptyCalculationError, 
        CalculatedValueTypeError, 
        TransformFunctionError
        )
        
NoCalculationConfig = object()
logger = FAssetManagementUtils.GetLogger()


class ILimitListener(object):
    """Interface for listening on limit events."""

    def OnLimitValueChecked(self, checkResult):
        """Callback for when a limit's monitored current value is checked. This
        is triggered prior to any related state change callbacks."""
        pass

    def OnLimitWarningEvent(self, checkResult):
        """Callback for when a limit enters a warning state."""
        pass

    def OnLimitBreachedEvent(self, checkResult):
        """Callback for when a limit breaches the threshold value."""
        pass

    def OnLimitActiveEvent(self, checkResult):
        """Callback for when monitored item returns within acceptable limits."""
        pass

    def OnLimitReadyEvent(self, checkResult):
        """Callback for when monitored item returns EmptyCalculationError."""
        pass

    def OnLimitErrorEvent(self, checkResult):
        """Callback for when monitored item returns error."""
        pass

    def OnLimitUnmonitoredChildren(self, checkResult):
        """Callback for when a monitored parent limit encounters child target(s)
        without a limit monitoring them."""
        pass


class LimitCheckResult(object):
    """Stores the results of a single check of a monitored limit."""
    # pylint: disable-msg=R0903

    def __init__(self):
        self.Limit = None               # The FLimit object checked
        self.StateBefore = ''           # The limit state prior to checking
        self.StateAfter = ''            # The limit state post checking
        self.CheckedValue = None        # The value of the checked calculation transformed to double
        self.RawValue = None            # The checked value of the calculation
        self.ErrorMsg = ''              # LimitCheckResults for new (uncommitted)
        self.Children = []              # child limits resulting from this check
        self.TimeStamp = None           # Timestamp of check
    
    @property
    def StateChanged(self):
        return self.StateBefore != self.StateAfter

#class EmptyCalculationError(Exception):
#    """Raised when the limit does not have a resulting valid calculation."""
#    pass


class FMonitoredLimit(object):
    """Represents a monitored limit."""

    OPERATOR_FUNCS = {
        'Equal': operator.eq, 'Not Equal': operator.ne,
        'Less': operator.lt, 'Less or Equal': operator.le,
        'Greater': operator.gt, 'Greater or Equal': operator.ge,
        }

    def __init__(self, limit, listener=None):
        self._limit = limit
        self._isParent = limit.IsParent()
        self._listeners = set()
        self._ValidateLimit()
        self._calculation = None
        if listener:
            self.AddListener(listener)

    def Limit(self):
        """Returns the limit being monitored."""
        return self._limit

    def AddListener(self, listener):
        """Listen and receive updates on the limit being monitored."""
        self._listeners.add(listener)

    def RemoveListener(self, listener):
        """Stop listening to the limit being monitored."""
        self._listeners.discard(listener)

    def CheckLimit(self, trades=None):
        """Perform a check on a monitored limit.

        Updated values/states will trigger callbacks to all registered listeners.
        The result of checks on calculated cells will be returned in a
        LimitCheckResult object.

        Optionally include a list of non-committed trades to include them in the
        checked calculation (non-distributed mode only).

        """
        checkResult = None
        if not self.Limit().IsDeleted():
            with self._IncludeTrades(trades):
                checkResult = self._GetLimitCheckResult()
            if checkResult and self._listeners:
                self._UpdateListeners(checkResult)
        return checkResult

    def CalculationSpace(self):
        """Return the calculation space used for the limit calculation."""
        return self._Calculation().CalculationSpace()

    def GetCurrentValue(self):
        """Return the transformed current value of the limited cell."""
        rawValue = self.GetRawValue()
        return self.TransformLimitValue(rawValue)
        
    def GetRawValue(self):
        if not self.Limit().IsParent():
            return self._Calculation().CurrentValue()

    def TransformLimitValue(self, value):
        TransformFunction = FLimitUtils.LimitTransformFunction(self.Limit())
        if TransformFunction:
            rawValue = value
            try:
                value = TransformFunction(value)
                logger.debug('Column value %s was transformed to double %s'%(str(rawValue), str(value)))
            except Exception as e:
                raise TransformFunctionError('Error when calling transform function "%s": %s'%(TransformFunction, e))
        else:
            logger.warn('No transform function specified, using raw value')
        return value
        
    def GetDependencies(self):
        """Returns all items related to this limit that may affect its current
        value calculation."""
        items = []
        if not self._isParent:
            items.append(self._limit)
        try:
            if self._Calculation().CalculatedValue():
                items.append(self._Calculation().LimitNode() \
                    if self._isParent else self._Calculation().CalculatedValue())
        except Exception as err:
            logger.debug(err)
        return [i for i in items if i]

    def IsActive(self):
        """Returns True if the passed FLimit is a candidate for checking."""
        return FLimitUtils.IsActive(self.Limit())

    def _Calculation(self):
        if self._calculation is None:
            self._calculation = LimitCalculation(self.Limit())
        return self._calculation

    def _ValidateLimit(self):
        limitTarget = self.Limit().LimitTarget()
        if not limitTarget:
            raise ValueError('Limit does not have a limit target set')
        if not limitTarget.SheetType():
            raise ValueError('Limit target does not specify a sheet type')
        if not limitTarget.CalculationSpecification():
            raise ValueError('Limit target does not have a calculation specification')
        if not limitTarget.TreeSpecification():
            raise ValueError('Limit target does not have a tree specification')
        if self.Limit().ComparisonOperator() not in self.OPERATOR_FUNCS:
            raise ValueError('Limit comparison operator "%s" is invalid' % \
                    self.Limit().ComparisonOperator())
        if not self.Limit().BusinessProcess():
            logger.debug('Limit %d has no business process', self.Limit().Oid())

    def _NewChildren(self):
        cells = self._Calculation().TargetCells(True)
        targets = (self._GetLimitTargetForCell(c) for c in cells)
        newTargets = (t for t in targets if not self.Limit().Child(t))
        newChildren = [self.Limit().CreateChildLimit(t.Clone()) for t in newTargets]
        if newChildren:
            logger.info('Limit %i has %d unmonitored child limit(s).',
                    self.Limit().Oid(), len(newChildren))
        return newChildren

    def _CreateLimitCheckResult(self):
        result = LimitCheckResult()
        result.Limit = self.Limit()
        result.StateBefore = FLimitUtils.CurrentState(result.Limit)
        result.StateAfter = result.StateBefore
        return result

    def _GetLimitTargetForCell(self, cell):
        target = self.Limit().LimitTarget().Clone()
        target.SubLevel(0)
        target.TreeSpecification(self.CalculationSpace(), cell)
        return target

    def _GetLimitCheckResult(self):
        checkResult = self._CreateLimitCheckResult()

        try:
            if self.Limit().IsParent() is False:
                self._SetCheckedLimitValue(checkResult, self.GetRawValue())
                self._SetCheckedLimitState(checkResult)
            else:
                for child in self._NewChildren():
                    childResult = self.__class__(child)._GetLimitCheckResult()
                    checkResult.Children.append(childResult)
                checkResult.StateAfter = 'Active'
        except EmptyCalculationError as e:
            msg = 'Limit %d has no valid calculation: %s' % (checkResult.Limit.Oid(), e)
            checkResult.StateAfter = 'Ready'
            checkResult.ErrorMsg = msg
        except Exception as e:
            msg = 'Unable to monitor limit %d: %s' % (checkResult.Limit.Oid(), e)
            checkResult.StateAfter = 'Error'
            checkResult.ErrorMsg = msg

        logger.info('Limit %i has state %s for current value %s.',
                     checkResult.Limit.Oid(),
                     checkResult.StateAfter,
                     checkResult.CheckedValue)
        return checkResult

    def _SetCheckedLimitValue(self, checkResult, currentValue):
        checkResult.TimeStamp = acm.Time.TimeNow()
        checkResult.RawValue = currentValue
        transformedValue = self.TransformLimitValue(currentValue)
        if transformedValue is not None and not math.isnan(transformedValue):
            if not isinstance(transformedValue, numbers.Number):
                raise CalculatedValueTypeError('Calculated value of type {0} is not supported'.format(type(transformedValue)))
            checkResult.CheckedValue = transformedValue
            
    @classmethod
    def _SetCheckedLimitState(cls, checkResult):
        checkResult.StateAfter = checkResult.StateBefore
        if (checkResult.CheckedValue is not None and
            not math.isnan(checkResult.CheckedValue)):
            limit = checkResult.Limit
            thresholdValue = FLimitUtils.Threshold(limit)
            warningValue = FLimitUtils.WarningValue(limit)
            compareFunc = cls.OPERATOR_FUNCS[limit.ComparisonOperator()]
            if compareFunc(checkResult.CheckedValue, thresholdValue):
                checkResult.StateAfter = 'Breached'
            elif compareFunc(checkResult.CheckedValue, warningValue):
                checkResult.StateAfter = 'Warning'
            else:
                checkResult.StateAfter = 'Active'
        if (checkResult.CheckedValue is None or
            math.isnan(checkResult.CheckedValue)):
            checkResult.StateAfter = 'Ready'

    @contextmanager
    def _IncludeTrades(self, trades):
        if trades:
            try:
                self._Calculation().AddTrades(trades)
                yield
            finally:
                self._Calculation().RemoveTrades(trades)
        else:
            yield

    def _UpdateListeners(self, checkResult):
        if not self._isParent:
            self._CallListenersCallback('OnLimitValueChecked', checkResult)
        if checkResult.StateBefore != checkResult.StateAfter:
            callbackName = 'OnLimit' + checkResult.StateAfter + 'Event'
            self._CallListenersCallback(callbackName, checkResult)
        if checkResult.Children:
            self._CallListenersCallback('OnLimitUnmonitoredChildren', checkResult)

    def _CallListenersCallback(self, callbackName, parameter):
        for listener in self._listeners:
            try:
                callback = getattr(listener, callbackName)
                if callable(callback):
                    callback(parameter)
            except AttributeError as e:
                logger.warn('Failed to update listener: %s', e)
            except RuntimeError as e:
                logger.error('Listener failed in callback (%s): %s', callbackName, e)


class LimitCalculation(object):
    """Calculation for a limit value."""
    # pylint: disable-msg=R0902

    _spaceCollections = dict()
    _insertItemsCache = dict()

    def __init__(self, limit):
        self._limit = limit
        self._limitTarget = limit.LimitTarget()
        self._calculationEnvironment = self.LimitTarget().CalculationEnvironment()
        self._projectionParts = self.LimitTarget().ProjectionParts()
        self._calcSpace = None
        self._calculation = None
        self._baseCalculation = None
        self._limitNode = None
        self._isDistributed = bool(FLimitSettings.UseDistributedCalculations()
                and not limit.IsParent())
        self._targetCellItems = set()
        self._replacedTrades = set()

    def SpaceCollection(self):
        calcEnv = self.CalculationEnvironment()
        if calcEnv not in self._spaceCollections:
            spaceCollection = acm.Calculations().CreateCalculationSpaceCollection(calcEnv)
            self._spaceCollections[calcEnv] = spaceCollection
        return self._spaceCollections[calcEnv]

    def CalculationEnvironment(self):
        if self._calculationEnvironment is None:
            self._calculationEnvironment = FLimitSettings.CalculationEnvironment()
        return self._calculationEnvironment
        
    def BaseValue(self):
        if self._baseCalculation is None:
            calculationSpec = self.LimitTarget().CalculationSpecification()
            baseConfig = acm.Sheet.Column().ConfigurationWithoutScenario(calculationSpec.Configuration())
            self._baseCalculation = self._CreateCalculation(baseConfig)
        return self._baseCalculation.Value()

    def CalculatedValue(self):
        if self._calculation is None:
            self._calculation = self._CreateCalculation()
        return self._calculation

    def CurrentValue(self):
        calculation = self.CalculatedValue()
        return self._GetCalculatedValue(calculation)

    def CalculationSpace(self):
        if self._calcSpace is None:
            self._calcSpace = self.SpaceCollection().GetSpace(
                    self.LimitTarget().SheetType(),
                    self.LimitTarget().CalculationSpecification().ContextName(),
                    None, self.IsDistributed())
        return self._calcSpace

    def Limit(self):
        return self._limit

    def LimitTarget(self):
        return self._limitTarget

    def LimitNode(self):
        if self._limitNode is None:
            treeSpec = self.LimitTarget().TreeSpecification()
            topNode = self._InsertTreeSpec(treeSpec)

            if self.LimitTarget().IsTemplate():
                treeSpec = self._ResetTreeSpec(topNode)

            try:
                self._limitNode = topNode.Iterator().Find(treeSpec).Tree()
            except AttributeError:
                raise EmptyCalculationError('Failed to find target node in origin tree')
        return self._limitNode

    def IsDistributed(self):
        return self._isDistributed

    def TargetCells(self, newCellsOnly=False):
        targetCells = []
        subLevel = self.LimitTarget().SubLevel()
        if subLevel == 0:
            targetCells.append(self.LimitNode())
        else:
            parentDepth = self.LimitNode().Depth()
            compoundPortfolioDepths = deque([parentDepth, ])
            iterator = self.LimitNode().Iterator().FirstChild()
            while iterator and iterator.Tree().Depth() != 1:
                depth = iterator.Tree().Depth()
                rowTreeItem = iterator.Tree().Item()
                if (rowTreeItem.IsKindOf(acm.FPortfolioInstrumentAndTrades) and
                    rowTreeItem.Portfolio().IsKindOf(acm.FCompoundPortfolio)):
                    compoundPortfolioDepths.append(parentDepth)
                    parentDepth = depth
                elif depth <= parentDepth and compoundPortfolioDepths:
                    parentDepth = compoundPortfolioDepths.pop()

                targetDepth = parentDepth + subLevel
                if depth > targetDepth:
                    iterator = self._ParentNextSibling(iterator)
                elif depth == targetDepth:
                    targetCells.append(iterator.Tree())
                    iterator = iterator.NextSibling() or self._ParentNextSibling(iterator)
                else:
                    iterator = iterator.FirstChild() or iterator.NextSibling() \
                            or self._ParentNextSibling(iterator)
        if newCellsOnly:
            newTargets = [c for c in targetCells if c.Item() not in self._targetCellItems]
            self._targetCellItems = set([c.Item() for c in targetCells])
            targetCells = newTargets
        return targetCells

    def AddTrades(self, trades):
        assert not self.IsDistributed(), 'Cannot add trades in distributed mode'
        for trade in trades:
            assert trade.IsModified() or trade.IsInfant(), \
                    'Added trades must be new or in a modified state'
            if self._IncludesTrade(trade):
                original = trade.Originator()
                tradesInPosition = self._TradesInPosition()
                if original and original in tradesInPosition:
                    tradesInPosition.Remove(original)
                    tradesInPosition.Add(trade)
                    self._replacedTrades.add(original)
                else:
                    tradesInPortfolio = self.LimitTarget().TreeSpecification().OriginObject().Trades()
                    tradesInPortfolio.Add(trade)
        self.CalculationSpace().Refresh()

    def RemoveTrades(self, trades):
        for trade in trades:
            if self._IncludesTrade(trade):
                original = trade.Originator()
                if original and original in self._replacedTrades:
                    tradesInPosition = self._TradesInPosition()
                    tradesInPosition.Remove(trade)
                    tradesInPosition.Add(original)
                    self._replacedTrades.remove(original)
                else:
                    tradesInPortfolio = self.LimitTarget().TreeSpecification().OriginObject().Trades()
                    tradesInPortfolio.Remove(trade)
        self.CalculationSpace().Refresh()

    def _TradesInPosition(self):
        try:
            return self.LimitNode().Item().Trades()
        except EmptyCalculationError as e:
            logger.debug(e)
            return acm.FArray()

    def _IncludesTrade(self, trade):
        return acm.Limits.FindByTrade(trade, [self.Limit(), ]).Includes(self.Limit())

    def _FindPath(self, node):
        nodeIter = node.Iterator()
        path = self.LimitTarget().TemplatePath()
        for constraint in path.split(','):
            nodeIter = nodeIter.Find(constraint)
            if not nodeIter:
                raise EmptyCalculationError('Required path "%s" does not exist' % path)
        return nodeIter.Tree()

    def _ResetTarget(self, node):
        subLevel = self.LimitTarget().SubLevel()
        self.LimitTarget().TreeSpecification(self.CalculationSpace(), node)
        self.LimitTarget().SubLevel(subLevel)
        self.Limit().Commit()

    def _ResetTreeSpec(self, node):
        node = self._FindPath(node)
        self._ResetTarget(node)
        return self.LimitTarget().TreeSpecification()

    @staticmethod
    def _ResetOriginObject(treeSpec, node):
        # Comparing two instances of an ASQL portfolio or query folder
        # only works if the instances are the same. Since we are caching
        # these objects, it is necessary to reset the object on the treespec
        # to find it in the TreeIterator::Find method
        try:
            if treeSpec.OriginObject().IsKindOf(acm.FASQLPortfolio):
                treeSpec.OriginObject(node.Item().Portfolio())
            elif treeSpec.OriginObject().IsKindOf(acm.FASQLQueryFolder):
                treeSpec.OriginObject(node.Item())
        except AttributeError:
            pass

    def _InsertTreeSpec(self, treeSpec):
        try:
            itemKey = self._CreateItemKey(treeSpec)
            node = self._insertItemsCache.get(itemKey)
            if not node:
                node = self.CalculationSpace().InsertItem(
                    treeSpec.OriginObject())
                if treeSpec.Grouper():
                    node.ApplyGrouper(treeSpec.Grouper())
                self._insertItemsCache[itemKey] = node
                logger.debug('Inserting root object for limit %d in cache', self.Limit().Oid())
            else:
                self._ResetOriginObject(treeSpec, node)
                logger.debug('Found root object for limit %d in cache', self.Limit().Oid())
            self.CalculationSpace().Refresh()
            return node
        except RuntimeError as e:
            raise EmptyCalculationError('No calculation for limit target: %s', str(e))

    def _CreateCalculation(self, calculationConfig=NoCalculationConfig):
        try:
            calculationSpec = self.LimitTarget().CalculationSpecification()
            if calculationConfig is NoCalculationConfig:
                calculationConfig = calculationSpec.Configuration()
            calculation = self.CalculationSpace().CreateCalculation(
                self.LimitNode(),
                calculationSpec.ColumnName(),
                calculationConfig)
            self.CalculationSpace().Refresh()
            return calculation
        except RuntimeError as e:
            raise CreateCalculationError('Failed to create calculation: ' + str(e))
            
    def _GetCalculatedValue(self, calculation):
        value = calculation.ValueAtAsVariant(self._projectionParts)
        displayType = self.LimitTarget().ScenarioDisplayType()
        if displayType == 'Relative':
            value = self._Differential(value, self.BaseValue())
        elif displayType == 'Relative Percent':
            value = 100 * self._Differential(value, self.BaseValue(), isRelative=True)
        return value
        
    def _ParentNextSibling(self, nodeIter):
        parent = nodeIter.Parent()
        if parent and parent.Tree() != self.LimitNode():
            return parent.NextSibling() or self._ParentNextSibling(parent)
        return None

    def _CreateItemKey(self, treeSpec):
        return (self.CalculationSpace(), 
                self._OriginObjKey(treeSpec.OriginObject()),
                treeSpec.Grouper())

    @classmethod
    def _OriginObjKey(cls, obj):
        # FASQLQuery is mutable and does not implement a reliable Hash method.
        # That makes it not a valid candidate to be part of insertItemsCache key.
        # Use the string repr of the referenced SQL query instead.
        try:
            if obj.Class() is acm.FASQLPortfolio:
                return cls._SQL(obj.QueryCopy())
            elif obj.Class() is acm.FASQLQueryFolder:
                return cls._SQL(obj.Query())
            return obj
        except AttributeError:
            pass

    @staticmethod
    def _SQL(query):
        queryResult = query.Select_Triggered()
        return ''.join(str(s.SQL()) for s in queryResult.SubResults())

    @staticmethod
    def _Number(value):
        try:
            return value.Number()
        except AttributeError:
            return value

    @staticmethod
    def _Differential(x, y, isRelative=False):
        differential = acm.GetFunction('differential', 3)
        try:
            if isRelative:
                return differential(x, y, y)
            return differential(x, y)
        except TypeError:
            return float('nan')
        except RuntimeError:
            return float('nan')