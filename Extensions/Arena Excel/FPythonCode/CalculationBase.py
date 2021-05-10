""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/CalculationBase.py"
import acm

NoConfiguration = object()


class Calculation(object):

    def __init__(self, space, node, columnId, configuration=None, projectionParts=None):
        self._space = space
        self._node = node
        self._columnId = columnId
        self._configuration = configuration
        self._projectionParts = projectionParts
        self._calculation = None
        self._isDirty = False
        
    def Value(self):
        if self.IsInitialized():
            self._isDirty = False
            return self._GetCalculation().ValueAtAsVariant(self._projectionParts)
            
    def IsInitialized(self):
        return bool(self._GetCalculation())
        
    def IsDirty(self):
        return self._isDirty
        
    def Destroy(self):   
        self._GetCalculation().RemoveDependent(self)
        self._calculation = None
            
    def ServerUpdate(self, sender, aspect, parameter):
        self._isDirty = True
        
    
class SheetCalculation(Calculation):

    def _GetCalculation(self, configuration=NoConfiguration):
        if self._calculation is None:
            if self._node.Unwrap() is not None:
                if configuration is NoConfiguration:
                    configuration = self._configuration
                self._calculation = self._space.CreateCalculation(self._node.Unwrap(), 
                                                                  self._columnId, 
                                                                  configuration)
                self._space.Refresh()
                self._calculation.AddDependent(self)
                self._isDirty = True
        return self._calculation
        
        
class DealSheetCalculation(Calculation):

    def _GetCalculation(self):
        if self._calculation is None:
            self._calculation = self._space.CreateCalculation(self._node.Unwrap(), 
                                                              self._columnId)
            self._calculation.AddDependent(self)
        return self._calculation
        
        
class Node(object):

    PATH_SEPARATOR = ' / '
    _insertItemsCache = dict()

    def __init__(self, space, origin, grouper=None, constraint=None):
        self._space = space
        self._origin = origin
        self._grouper = grouper
        self._constraint = constraint
        self._node = None
        
    def Unwrap(self):
        if self._node is None:
            topNode = self._InsertItem()
            self._node = self._FindTargetNode(topNode)
        return self._node
        
    def _CreateItemKey(self):
        return (self._space, 
                self._ObjKey(self._origin),
                self._grouper)
        
    def _InsertItem(self):
        itemKey = self._CreateItemKey()
        if itemKey not in self._insertItemsCache:
            node = self._space.InsertItem(self._origin)
            if self._grouper:
                node.ApplyGrouper(self._grouper)
            self._insertItemsCache[itemKey] = node
        self._space.Refresh()
        return self._insertItemsCache[itemKey]
        
    def _FindTargetNode(self, node):
        nodeIter = node.Iterator()
        try:
            for constraint in self._constraint:
                if constraint:
                    nodeIter = nodeIter.Find(constraint)
                    if not nodeIter:
                        path = (node.StringKey() + 
                                self.PATH_SEPARATOR + 
                                self.PATH_SEPARATOR.join(self._constraint))
                        raise ValueError('Required path "%s" does not exist' % path)
        except ValueError:
            return None
        return nodeIter.Tree()    
        
    @classmethod
    def _ObjKey(cls, obj):
        # FASQLQuery is mutable and does not implement a reliable Hash method.
        # Use the string reprensentation of the referenced SQL query instead.
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
        
        
class PortfolioNode(Node):

    def __init__(self, space, portfolioId, grouper=None, constraint=None):
        portfolio = (acm.FPhysicalPortfolio[portfolioId] or 
                     acm.FStoredASQLQuery[portfolioId] or 
                     acm.FTradeSelection[portfolioId])
        super(PortfolioNode, self).__init__(space, portfolio, grouper, constraint)
        
        
class InstrumentNode(object):

    def __init__(self, insId):
        self._instrument = acm.FInstrument[insId]
        
    def Unwrap(self):
        return self._instrument
        
        
class TreeSpecNode(Node):

    def __init__(self, space, treeSpec):
        super(TreeSpecNode, self).__init__(space,
                                           treeSpec.OriginObject(),
                                           treeSpec.Grouper(),
                                           treeSpec)
        
    def _FindTargetNode(self, topNode):
        self._ResetOriginObject(self._constraint, topNode)
        return topNode.Iterator().Find(self._constraint).Tree()
        
    @staticmethod
    def _ResetOriginObject(treeSpec, topNode):
        # Comparing two instances of an ASQL portfolio or query folder
        # only works if the instances are the same. Since we are caching
        # these objects, it is necessary to reset the object on the treespec
        # to find it in the TreeIterator::Find method
        try:
            if treeSpec.IsKindOf(acm.FASQLPortfolio):
                treeSpec.OriginObject(topNode.Item().Portfolio())
            elif treeSpec.IsKindOf(acm.FASQLQueryFolder):
                treeSpec.OriginObject(topNode.Item())
        except AttributeError:
            pass
            
            
class Result(object):

    def __init__(self, calculation):
        self._calcValue = calculation.Value()
        
    def Value(self):
        try:
            if math.isnan(self._calcValue):
                return 'NaN'
        except: 
            pass
        return self._calcValue
