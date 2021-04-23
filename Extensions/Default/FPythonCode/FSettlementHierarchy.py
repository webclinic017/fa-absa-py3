""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementHierarchy.py"

import FSettlementStatusQueries as Queries
import FSettlementSetters as Setters
from FSettlementEnums import StatusExplanation, SettlementStatus, RelationType



class HierarchyNode:
    def __init__(self, settlement, parentNode):
        self.__nodes = list()
        self.__settlement = settlement
        self.__parentNode = parentNode

    def GetSettlement(self):
        return self.__settlement

    def GetParentNode(self):
        return self.__parentNode

    def GetNodes(self):
        return self.__nodes

    def HasNodes(self):
        hasNodes = False
        if self.GetNumberOfNodes() > 0:
            hasNodes = True
        return hasNodes

    def GetNumberOfNodes(self):
        return len(self.GetNodes())

    def __HasParent(self):
        hasParent = False
        if self.__GetParent():
            hasParent = True
        return hasParent

    def __HasSplitChildren(self):
        hasSplitChildren = False
        if len(self.__GetSplitChildren()):
            hasSplitChildren = True
        return hasSplitChildren

    def __GetSplitChildren(self):
        return self.__settlement.SplitChildren()

    def __GetChildren(self):
        return self.__settlement.Children()

    def __GetParent(self):
        return self.__settlement.Parent()

    def __HasChildren(self):
        return (len(self.__settlement.Children()) > 0)

    def __HasSplitParent(self):
        return (self.__settlement.SplitParent() != None)

    def __GetSplitParent(self):
        return self.__settlement.SplitParent()

    def AddNodes(self):
        if self.__HasParent():
            self.AddNode(self.__GetParent())
        else:
            splitChildren = self.__GetSplitChildren()
            for splitChild in splitChildren:
                self.AddNode(splitChild)

    def AddTopDownNodes(self):
        if self.__HasSplitParent():
            self.AddNode(self.__GetSplitParent())
        else:
            for child in self.__GetChildren():
                self.AddNode(child)

    def AddNode(self, settlement):
        self.__nodes.append(HierarchyNode(settlement, self))

    def PrintNodeAndParents(self):
        self.PrintNode()
        for node in self.__nodes:
            print('%d reference %d' % (self.__settlement.Oid(), node.GetSettlement().Oid()))
            node.PrintNodeAndParents()

    def PrintNode(self):
        print('Settlement Oid = %d' % self.__settlement.Oid())

    def IsRoot(self):
        ''' '''
        return self.__parentNode == None

    def SetLeafNodes(self, nodeList):
        nodes = self.GetNodes()
        if len(nodes) == 0:
            nodeList.append(self)
        else:
            for node in nodes:
                node.SetLeafNodes(nodeList)

    def GetNodePath(self):
        nodePathList = list()
        node = self
        while node.IsRoot() == False:
            nodePathList.append(node)
            node = node.GetParentNode()
        return nodePathList

    def IsClosedNode(self):
        return self.__settlement.Status() == SettlementStatus.CLOSED

    def HasClosedSettlement(self):
        if self.IsClosedNode() == True:
            return True
        for node in self.__nodes:
            if node.HasClosedSettlement() == True:
                return True
        return False

    def IsVoidNode(self):
        return self.__settlement.Status() == SettlementStatus.VOID

    def IsPrereleasedNode(self):
        query = Queries.GetPreReleasedStatusQuery()
        return query.IsSatisfiedBy(self.__settlement)

    def IsPostReleasedNode(self):
        query = Queries.GetPostReleasedStatusQuery()
        return query.IsSatisfiedBy(self.__settlement)

class HierarchyTreeTopDown:
    def __init__(self, settlement):
        self.__root = HierarchyNode(settlement, None)
        self.__root.AddTopDownNodes()
        HierarchyTreeTopDown.InitializeTree(self.__root)
        self.__bottomMostNodes = list()
        self.__SetBottomMostNodes()

    @staticmethod
    def InitializeTree(hierarchyNode):
        for node in hierarchyNode.GetNodes():
            node.AddTopDownNodes()
            HierarchyTreeTopDown.InitializeTree(node)

    def __SetBottomMostNodes(self):
        for node in self.__root.GetNodes():
            node.SetLeafNodes(self.__bottomMostNodes)

    def HasAnyLeafStatusExplanation(self, statusExplanation):
        for bottomMostNode in self.__bottomMostNodes:
            settlement = bottomMostNode.GetSettlement()
            if statusExplanation == StatusExplanation.CHANGE_TO_SOURCE_DATA:
                if settlement.IsChangeToSourceData():
                    return True
            elif statusExplanation == StatusExplanation.AMENDMENT_PROCESS:
                if settlement.IsAmendmentProcess():
                    return True
            elif statusExplanation == StatusExplanation.RECALLED_DATA:
                if settlement.IsRecalledData():
                    return True
        return False

    def PrintTree(self):
        self.__root.PrintNodeAndParents()

class HierarchyTree:
    def __init__(self, settlement, isAmendmentProcess = False):
        self.__root = HierarchyNode(settlement, None)
        self.__topmostNodes = list()
        self.__root.AddNodes()
        HierarchyTree.InitializeTree(self.__root)
        self.__SetTopmostNodes()
        self.__isAmendmentProcess = isAmendmentProcess

    @staticmethod
    def InitializeTree(hierarchyNode):
        for node in hierarchyNode.GetNodes():
            node.AddNodes()
            HierarchyTree.InitializeTree(node)

    def __SetTopmostNodes(self):
        for node in self.__root.GetNodes():
            node.SetLeafNodes(self.__topmostNodes)

    def GetRoot(self):
        return self.__root

    def GetTopmostNodes(self):
        return self.__topmostNodes

    def GetNodePaths(self):
        nodePaths = list()
        for node in self.GetTopmostNodes():
            nodePaths.append(NodePath(node, self.__isAmendmentProcess))
        return nodePaths

    def HasClosedTopmostNodeInTree(self):
        for node in self.__topmostNodes:
            if node.IsClosedNode():
                return True
        return False

    def HasClosedNodeInTree(self):
        return self.__root.HasClosedSettlement()

    def IsNetHierarchyPartOfHierarchy(self):
        isNetHierarchyPartOfHierarchy = False
        if self.__root.GetNumberOfNodes() == 1:
            node = self.__root.GetNodes()[0]
            if node.HasNodes() == True:
                query = Queries.GetNetPartQuery()
                isNetHierarchyPartOfHierarchy = query.IsSatisfiedBy(self.__root.GetSettlement())
            else:
                for child in node.GetSettlement().Children():
                    if (child.Oid() != self.__root.GetSettlement().Oid()):
                        if (child.RelationType() != RelationType.NONE and 
                            child.RelationType() != RelationType.VALUE_DAY_ADJUSTED):
                            isNetHierarchyPartOfHierarchy = True
                            break
        return isNetHierarchyPartOfHierarchy

    def PrintTree(self):
        self.__root.PrintNodeAndParents()

    def HasNodes(self):
        return self.__root.HasNodes()

class NodePath:
    def __init__(self, hierarchyNode, isAmendmentProcess):
        self.__hierarchyNode = hierarchyNode
        self.__nodePath = hierarchyNode.GetNodePath()
        self.__isAmendmentProcess = isAmendmentProcess

    def UpdateNodePath(self):
        index = 0
        nodePathLength = len(self.__nodePath)
        topNode = self.__nodePath[index]
        index = index + 1

        topSettlement = topNode.GetSettlement()
        processUpdatesSet = set()

        if topSettlement.Status() != SettlementStatus.VOID:
            hierarchyTreeTopDown = HierarchyTreeTopDown(topSettlement)
            if self.__isAmendmentProcess:
                topSettlement.IsAmendmentProcess(True)
                NodePath.ClearStatusExplanation(hierarchyTreeTopDown, topSettlement, StatusExplanation.CHANGE_TO_SOURCE_DATA)
                NodePath.ClearStatusExplanation(hierarchyTreeTopDown, topSettlement, StatusExplanation.RECALLED_DATA)
            else:
                topSettlement.IsChangeToSourceData(True)
                NodePath.ClearStatusExplanation(hierarchyTreeTopDown, topSettlement, StatusExplanation.AMENDMENT_PROCESS)
                NodePath.ClearStatusExplanation(hierarchyTreeTopDown, topSettlement, StatusExplanation.RECALLED_DATA)

        if Queries.GetPreReleasedStatusQuery().IsSatisfiedBy(topSettlement):
            topSettlement.Status(SettlementStatus.EXCEPTION)
            processUpdatesSet.add(topSettlement)
        elif Queries.GetPostReleasedStatusQuery().IsSatisfiedBy(topSettlement):
            Setters.SetPostSettleActionIfNotStatusVoid(topSettlement)

        while index < nodePathLength:
            node = self.__nodePath[index]
            index = index + 1
            settlement = node.GetSettlement()
            settlement.Status(SettlementStatus.UPDATED)
            hierarchyTreeTopDown = HierarchyTreeTopDown(settlement)
            if self.__isAmendmentProcess:
                settlement.IsAmendmentProcess(True)
                NodePath.ClearStatusExplanation(hierarchyTreeTopDown, settlement, StatusExplanation.CHANGE_TO_SOURCE_DATA)
                NodePath.ClearStatusExplanation(hierarchyTreeTopDown, settlement, StatusExplanation.RECALLED_DATA)
            else:
                settlement.IsChangeToSourceData(True)
                NodePath.ClearStatusExplanation(hierarchyTreeTopDown, settlement, StatusExplanation.AMENDMENT_PROCESS)
                NodePath.ClearStatusExplanation(hierarchyTreeTopDown, settlement, StatusExplanation.RECALLED_DATA)
            processUpdatesSet.add(settlement)

        return processUpdatesSet

    def InitialiseNodePath(self):
        self.__nodePath = self.__hierarchyNode.GetNodePath()

    def RecallNodePath(self):
        index = 0
        nodePathLength = len(self.__nodePath)
        topNode = self.__nodePath[index]
        index = index + 1

        topSettlement = topNode.GetSettlement()
        if topSettlement.Status() != SettlementStatus.VOID:
            hierarchyTreeTopDown = HierarchyTreeTopDown(topSettlement)
            topSettlement.IsRecalledData(True)
            NodePath.ClearStatusExplanation(hierarchyTreeTopDown, topSettlement, StatusExplanation.AMENDMENT_PROCESS)
            NodePath.ClearStatusExplanation(hierarchyTreeTopDown, topSettlement, StatusExplanation.CHANGE_TO_SOURCE_DATA)

        if Queries.GetPreReleasedStatusQuery().IsSatisfiedBy(topSettlement):
            topSettlement.Status(SettlementStatus.EXCEPTION)
        elif Queries.GetPostReleasedStatusQuery().IsSatisfiedBy(topSettlement):
            Setters.SetPostSettleActionIfNotStatusVoid(topSettlement)

        while index < nodePathLength:
            node = self.__nodePath[index]
            index = index + 1
            settlement = node.GetSettlement()
            settlement.Status(SettlementStatus.UPDATED)
            settlement.IsRecalledData(True)
            hierarchyTreeTopDown = HierarchyTreeTopDown(settlement)
            NodePath.ClearStatusExplanation(hierarchyTreeTopDown, topSettlement, StatusExplanation.AMENDMENT_PROCESS)
            NodePath.ClearStatusExplanation(hierarchyTreeTopDown, topSettlement, StatusExplanation.CHANGE_TO_SOURCE_DATA)

    def GetSettlements(self):
        settlementList = list()
        for node in self.__nodePath:
            settlementList.append(node.GetSettlement())
        return settlementList

    @staticmethod
    def ClearStatusExplanation(hierarchyTree, settlement, statusExplanation):
        if False == hierarchyTree.HasAnyLeafStatusExplanation(statusExplanation):
            if statusExplanation == StatusExplanation.AMENDMENT_PROCESS:
                settlement.IsAmendmentProcess(False)
            if statusExplanation == StatusExplanation.CHANGE_TO_SOURCE_DATA:
                settlement.IsChangeToSourceData(False)
            if statusExplanation == StatusExplanation.RECALLED_DATA:
                settlement.IsRecalledData(False)
