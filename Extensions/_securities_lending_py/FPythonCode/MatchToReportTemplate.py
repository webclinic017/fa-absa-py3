""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/MatchToReportTemplate.py"
"""------------------------------------------------------------------------------------------------
MODULE
    MatchToReportTemplate

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Match To Report Template

------------------------------------------------------------------------------------------------"""

import acm
import OrderMappingHierarchyDefinitions
    
class HierarchyInfo(object):
    Name = OrderMappingHierarchyDefinitions.Names.HierarchyInstance
    FileDestination = 'Destination'
    Counterparty = 'Counterparty'
    OutputTemplate = 'Output Template'
    TradeSheetTemplate = 'Trade Sheet Template'
    OutputPath = 'Output Path'
    FileType = 'File Type'
    ReportName = 'Report Name'
    
class MatchToReportTemplateHelper(object):
    def FindHierarchy(self):
        return acm.FHierarchy[HierarchyInfo.Name]

    def FindMatchingNode(self, tree, children, counterparty, fileDestination):       
        for child in children:
            if self.MatchCounterparty(child, counterparty):
                for leafNode in tree.Children(child) or []:
                    if self.MatchFileDestination(leafNode, fileDestination):
                        return leafNode
                if self.IsValidTargetNode(child):
                    return child
        return None
                
    def Match(self, fileDestination, counterparty):
        if not fileDestination:
            raise Exception('File Export cannot match without Destination')
        hierarchy = self.FindHierarchy()
        tree = acm.FHierarchyTree()
        tree.Hierarchy(hierarchy)
        root = tree.RootNode()
        children = tree.Children(root)
        node = self.FindMatchingNode(tree, children, counterparty, fileDestination)
        if not node:
            node = self.FindMatchingNode(tree, children, None, fileDestination)
        if not node:
            raise Exception('File Export not setup for Counterparty %s and destination %s.' % (counterparty and counterparty.Name(), fileDestination))
        return node
            
    def MatchFileDestination(self, child, fileDestination):
        return self.GetNodeValue(child, HierarchyInfo.FileDestination) == fileDestination
        
    def MatchCounterparty(self, leafNode, counterparty):
        return self.GetNodeValue(leafNode, HierarchyInfo.Counterparty) == (counterparty and counterparty.Name())
        
    def IsValidTargetNode(self, node):
        return self.GetNodeValue(node, HierarchyInfo.OutputTemplate) and self.GetNodeValue(node, HierarchyInfo.TradeSheetTemplate)
                                    
    def GetNodeValue(self, node, valueIdentifier):
        if node:
            values = node.HierarchyDataValues()
            for value in values:
                if value.HierarchyColumnSpecification().Name() == valueIdentifier:
                    return value.DataValue()
        return None

    def MatchToReportCreateInfo(self, fileDestination, counterparty):
        leafNode = self.Match(fileDestination, counterparty)
        outputTemplate = self.GetNodeValue(leafNode, HierarchyInfo.OutputTemplate)
        tradeSheetTemplate = self.GetNodeValue(leafNode, HierarchyInfo.TradeSheetTemplate)
        if not (outputTemplate and tradeSheetTemplate):
            raise Exception('File Export not setup correctly for counterparty %s and destination %s' % 
                            (self.GetNodeValue(leafNode, HierarchyInfo.Counterparty), fileDestination))
        outputPath = self.GetNodeValue(leafNode, HierarchyInfo.OutputPath)
        fileType = self.GetNodeValue(leafNode, HierarchyInfo.FileType)
        reportName = self.GetNodeValue(leafNode, HierarchyInfo.ReportName)
        return outputPath, fileType, tradeSheetTemplate, outputTemplate, reportName
