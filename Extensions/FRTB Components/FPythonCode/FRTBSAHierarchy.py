
import acm

__saHierarchyObjectCache = {}

class FRTBSAHierarchy():
    def __NodeCacheKey(self, node):
        riskClass = None
        bucket = None
        subtype = None
        currencyPair = None
        while self.__saHierarchyTree.Parent(node):
            for dataValue in node.HierarchyDataValues():
                if 'Level Type' == dataValue.HierarchyColumnSpecification().Name():
                    if (not riskClass) and ('Risk Class' == dataValue.DataValue()):
                        riskClass = node.DisplayName()
                    elif (not bucket) and ('Bucket' == dataValue.DataValue()):
                        bucket = node.DisplayName()
                    elif (not subtype) and ('Subtype' == dataValue.DataValue()):
                        subtype = node.DisplayName()
                    elif (not currencyPair) and ('Currency Pair' == dataValue.DataValue()):
                        currencyPair = node.DisplayName()
                    break
            node = self.__saHierarchyTree.Parent(node)
        return riskClass, bucket, subtype, currencyPair

    def __ChildStopLevel(self, children):
        node = children[0]
        for dataValue in node.HierarchyDataValues():
            if 'Level Type' == dataValue.HierarchyColumnSpecification().Name():
                return dataValue.DataValue() in ('Correlation Bucket', 'Time Bucket')
        return False

    def __RecurseTreeAndFillNodeCache(self, node, treeNodeByKeyCache):
        children = self.__saHierarchyTree.Children(node)
        stopRecursing = (not children) or (self.__ChildStopLevel(children))
        if stopRecursing:
            treeNodeByKeyCache[self.__NodeCacheKey(node)] = node
        else:
            for child in children:
                self.__RecurseTreeAndFillNodeCache(child, treeNodeByKeyCache)

    def __init__(self, saHierarchyName):
        self.__saHierarchy = acm.FHierarchy[saHierarchyName]
        if not self.__saHierarchy:
            errorMessage = 'Hierarchy with name ' + saHierarchyName + ' not found.'
            print (errorMessage)
            raise Exception(errorMessage)

        self.__saTreeNodeByKeyCache = {}
        self.__saHierarchyTree = acm.FHierarchyTree()
        self.__saHierarchyTree.Hierarchy = self.__saHierarchy
        self.__RecurseTreeAndFillNodeCache(self.__saHierarchyTree.RootNode(), self.__saTreeNodeByKeyCache)

    def ColumnValue(self, riskClass, bucket, subtype, currencyPair, columnName):
        key = (riskClass, bucket, subtype, currencyPair)
        if key in self.__saTreeNodeByKeyCache:
            node = self.__saTreeNodeByKeyCache[key]
            while node:
                for dataValue in node.HierarchyDataValues():
                    if columnName == dataValue.HierarchyColumnSpecification().Name():
                        return dataValue.DataValueVA()
                node = self.__saHierarchyTree.Parent(node)
        return None
    
def GetSAHierarchy(saHierarchyName):
    if not saHierarchyName in __saHierarchyObjectCache:
        __saHierarchyObjectCache[saHierarchyName] = FRTBSAHierarchy(saHierarchyName)
    return __saHierarchyObjectCache[saHierarchyName]        
