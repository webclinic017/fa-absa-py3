""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/AMUtils/./etc/FCalculationSpaceUtils.py"
"""--------------------------------------------------------------------------
MODULE
    FCalculationSpaceUtils

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Provides functionality for reusing calculation spaces.

-----------------------------------------------------------------------------"""
import acm
from FEventUtils import Observable
from FAssetManagementUtils import logger
from collections import defaultdict

differential = acm.GetFunction('differential', 3)


class CalculationError(RuntimeError):
    
    @classmethod
    def Create(cls, error):
        if str(error).startswith('Invalid Column'):
            return MissingColumnError(error)
        return MissingNodeError(error)
        
        
class MissingNodeError(CalculationError): 
    pass
    
class MissingColumnError(CalculationError): 
    pass
    

class SpaceParams(object):

    def __init__(self, params=None):
        self._params = params

    def SheetClass(self):
        try:
            return self._params.SheetClass()
        except AttributeError:
            return 'FPortfolioSheet'

    def Context(self):
        try:
            return self._params.Context()
        except AttributeError:
            return acm.GetDefaultContext()   

    def CalculationEnvironment(self):
        #TODO: Add CalculationEnvironment to rule definition info
        try:
            return self._params.CalculationEnvironment()
        except AttributeError:
            return None    

    def GridConfiguration(self):
        try:
            return self._params.GridConfiguration()
        except AttributeError:
            return None               

    def IsDistributed(self):
        #TODO: Add UseDistributedCalculations to rule defintion info
        try:
            return self._params.IsDistributed()
        except AttributeError:
            return False
            
            
class GridColumnParams(SpaceParams):

    def ColumnId(self):
        return self._params.ColumnId()
        
    def CalculationConfiguration(self):
        try:
            return self._params.CalculationConfiguration()
        except AttributeError:
            return None
        
    def Projection(self):
        try:
            return self._params.Projection()
        except AttributeError:
            return []
            
            
class GridRowColumnParams(GridColumnParams):

    def Entity(self):
        return self._params.Entity()
        
    def Grouper(self):
        try:
            return self._params.Grouper()
        except AttributeError:
            return None
            
            
class Node(object):

    def __init__(self, node):
        self._node = node
        
    def SubNodes(self):
        nodeIter = self._node.Iterator()
        while nodeIter.NextUsingDepthFirst():
            subNode = nodeIter.Tree()
            if self._IsSibling(subNode):
                break
            yield subNode
    
    def _IsSibling(self, node):
        return self._node.Parent() == node.Parent()
        

class ItemCache(object):

    def __init__(self):
        self._dict = defaultdict(dict)

    def __getitem__(self, key):
        try:
            try:
                space, obj, grouper = key
            except (TypeError, ValueError):
                raise KeyError
            else:
                return self._dict[space][(obj, grouper)]
        except KeyError:
            raise KeyError('[{0}]'.format(key))
        
    def __setitem__(self, key, value):
        space, obj, grouper = key
        self._dict[space][(obj, grouper)] = value
        
    def get(self, key, value=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return value
            
    def clear(self):
        self._dict.clear()
        
    def remove(self, space):
        if self._dict.get(space):
            del self._dict[space]
            
    def __repr__(self):
        return str(self._dict)
        
        
class SpaceCollection(object):

    _spaceCollections = dict()
    _spaces = set()
    
    @classmethod
    def GetSpace(cls, spaceParams=None):
        params = SpaceParams(spaceParams)
        environment = params.CalculationEnvironment()
        space = cls._GetCollection(environment).GetSpace(params.SheetClass(),
                                                         params.Context(),
                                                         params.GridConfiguration(),
                                                         params.IsDistributed())
        cls._spaces.add(space)
        return Space(space)

    @classmethod
    def Refresh(cls):
        for space in cls._spaces:
            try:
                space.Refresh()        
            except RuntimeError as err:
                logger.debug(err)
                
    @classmethod
    def Clear(cls):
        for collection in cls._spaceCollections:
            collection.Clear()
        cls._spaces.clear()
        
    @classmethod
    def _GetCollection(cls, environment):
        if environment not in cls._spaceCollections:
            spaceCollection = acm.Calculations().CreateCalculationSpaceCollection(environment)
            cls._spaceCollections[environment] = spaceCollection
        return cls._spaceCollections[environment]        


class Space(object):

    _itemCache = ItemCache()

    def __init__(self, space):
        self._space = space

    def InsertItem(self, obj, grouper=None):
        itemKey = self._CreateItemKey(obj, grouper)
        node = self._itemCache.get(itemKey)
        if not node:
            node = self._space.InsertItem(obj)
            if grouper:
                node.ApplyGrouper(grouper)
            self._space.Refresh()
            self._itemCache[itemKey] = node
            logger.debug('Inserting {0} in cache'.format(node))
        else:
            logger.debug('Node {0} found in cache'.format(node))
        return node

    def CreateCalculation(self, node, columnId, config=None):
        return self._space.CreateCalculation(node, columnId, config)
        
    def Clear(self):
        self._space.Clear()
        self._itemCache.remove(self._space)
        
    def Refresh(self):
        try:
            self._space.Refresh()
        except RuntimeError as err:
            logger.debug(err)
    
    def SubNodes(self, node):
        self.Refresh()
        return Node(node).SubNodes()
            
    def __getattr__(self, attr):
        if '_space' not in self.__dict__:
            raise AttributeError('{0} object has no attribute {1}'.format(self.__class__.__name__, '_space'))    
        return getattr(self._space, attr)
        
    def _CreateItemKey(self, obj, grouper):
        return (self._space,
                self._ObjKey(obj),
                grouper)

    @classmethod
    def _ObjKey(cls, obj):
        # FASQLQuery does not have a reliable hash.
        # Use the SQL query hash instead.
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
        

class Calculation(Observable):

    def __init__(self, space, node, columnId, config=None):
        super(Calculation, self).__init__()
        self._space = space
        self._node = node
        self._columnId = columnId
        self._config = config
        self._calculation = None
        self._baseCalculation = None
        
    def Value(self):
        return self._Calculation().ValueAtAsVariant()    

    def ValueAtAsVariant(self, projection=[]):
        if self._Calculation().IsCollection():
            return [c.ValueAtAsVariant(projection) for c in self._Calculation()]
        return self._Calculation().ValueAtAsVariant(projection)
        
    def BaseValue(self):
        return self._BaseCalculation().Value()

    def RelativeValue(self, projection):
        value = self._Calculation().ValueAtAsVariant(projection)
        return self.Differential(value, self.BaseValue())
        
    def RelativePercentValue(self, projection):
        value = self._Calculation().ValueAtAsVariant(projection)
        return 100 * self.Differential(value, self.BaseValue(), isRelative=True)
        
    def ServerUpdate(self, sender, aspect, param):
        self.NotifyObservers(aspect, sender)

    def OnObservableStart(self):
        if self not in self._Calculation().Dependents():
            self._Calculation().AddDependent(self)

    def OnObservableEnd(self):
        if self in self._Calculation().Dependents():
            self._Calculation().RemoveDependent(self)
            
    @staticmethod
    def Differential(x, y, isRelative=False):
        try:
            if isRelative:
                return differential(x, y, y)
            return differential(x, y)
        except TypeError:
            return float('nan')
        except RuntimeError:
            return float('nan')
            
    def _Calculation(self):
        if self._calculation is None:
            self._calculation = self._space.CreateCalculation(self._node, 
                                                              self._columnId, 
                                                              self._config)
        return self._calculation
        
    def _BaseCalculation(self):
        if self._baseCalculation is None:
            baseconfig = acmcm.Sheet.Column().ConfigurationWithoutScenario(self._config)            
            self._baseCalculation = self._space.CreateCalculation(self._node, 
                                                                  self._columnId, 
                                                                  baseconfig)
        return self._baseCalculation
    


class CalculationGrid(Observable):

    def __init__(self, spaceParams=None):
        super(CalculationGrid, self).__init__()
        self._space = SpaceCollection.GetSpace(spaceParams)
        self._calculations = defaultdict(dict)
        self._observedNodes = set()

    def GetValue(self, node, columnId, config=None, projection=[]):
        try:
            return self._GetCalculation(node, columnId, config).ValueAtAsVariant(projection)
        except RuntimeError as err:
            self._StopObserving(node)
            self._RemoveNode(node)
            raise CalculationError.Create(err)
            
    def OnObservableStart(self):
        for node in self._calculations:
            self._StartObserving(node)
            
    def OnObservableEnd(self):
        for node in self._calculations:
            self._StopObserving(node)
            
    def ServerUpdate(self, sender, aspect, param):
        try:
            if str(aspect) == 'Remove' and param:
                self._StopObserving(param)
                self._RemoveNode(param)
            self.NotifyObservers(aspect, param)
        except Exception as err:
            logger.error(err)
            
    def __getattr__(self, attr):
        if '_space' not in self.__dict__:
            raise AttributeError('{0} object has no attribute {1}'.format(self.__class__.__name__, '_space'))
        return getattr(self._space, attr)            

    def _Calculations(self):
        for node in self._calculations:
            for calc in self._calculations[node].itervalues():
                yield calc       

    def _GetCalculation(self, node, columnId, config):
        if node.IsKindOf(acm.FCalculation):
            return node          
        if node not in self._calculations:
            logger.debug('Adding node {0} to calculation cache'.format(node.StringKey()))
            calculation = Calculation(self._space, node, columnId, config)
            self._calculations[node][(columnId, config)] = calculation
            if self.IsObserved():
                self._StartObserving(node)        
        elif (columnId, config) not in self._calculations[node]:
            logger.debug('Adding columnId {0} and config {1} to node {2} in calculation '
                         'cache'.format(columnId, config, node.StringKey()))
            calculation = Calculation(self._space, node, columnId, config)
            self._calculations[node][(columnId, config)] = calculation
            if self.IsObserved():
                calculation.AddObserver(self)
        return self._calculations[node][(columnId, config)]

    def _StartObserving(self, node):
        parent = node.Parent()    
        if parent and parent not in self._observedNodes:
            logger.debug('Start observing node {0}'.format(node.StringKey()))
            parent.AddDependent(self)
            self._observedNodes.add(parent)
        for calc in self._Calculations():
            calc.AddObserver(self)

    def _StopObserving(self, node):
        if node in self._observedNodes:
            logger.debug('Stop observing node {0}'.format(node.StringKey()))
            node.RemoveDependent(self)
        for calc in self._Calculations():
            calc.RemoveObserver(self)

    def _RemoveNode(self, node):
        if node in self._calculations:
            logger.debug('Removing node {0} from calculation cache'.format(node.StringKey()))
            del self._calculations[node]
            
            
class CalculationGridColumn(CalculationGrid):

    def __init__(self, gridColumnParams):
        params = GridColumnParams(gridColumnParams)
        super(CalculationGridColumn, self).__init__(params)
        self._columnId = params.ColumnId()
        self._config = params.CalculationConfiguration()
        self._projection = params.Projection()
        
    def GetValue(self, node):
        return super(CalculationGridColumn, self).GetValue(node, 
                                                           self._columnId, 
                                                           self._config, 
                                                           self._projection)
                                                           
                                                           
class CalculationGridRowColumn(CalculationGridColumn):

    def __init__(self, gridRowColumnParams):
        params = GridRowColumnParams(gridRowColumnParams)
        super(CalculationGridRowColumn, self).__init__(params)
        self._entity = params.Entity()
        self._grouper = params.Grouper()
        self._entityNode = None
        
    def EntityNode(self):
        if self._entityNode is None:
            self._entityNode = self.InsertItem(self._entity, 
                                               self._grouper)
        return self._entityNode
        
    def EntitySubNodes(self):
        return self.SubNodes(self.EntityNode())


class CalculationService(object):

    _onIdleFrequency = .5
    _onIdleCallback = None    

    def __init__(self, space):
        self._space = space

    def Start(self):
        self._InitOnIdleCallback()

    def Stop(self):
        self._RemoveOnIdleCallback()

    def __getattr__(self, attr):
        return getattr(self._space, attr) 

    def _InitOnIdleCallback(self):
        if self._onIdleCallback is None:
            self.__class__._onIdleCallback = acm.Time.Timer().CreatePeriodicTimerEvent(
                self._onIdleFrequency, self._OnHandleOnIdle, None)

    def _RemoveOnIdleCallback(self):
        acm.Time.Timer().RemoveTimerEvent(self._onIdleCallback)
        self.__class__._onIdleCallback = None

    def _OnHandleOnIdle(self, *args):
        self._space.Refresh()