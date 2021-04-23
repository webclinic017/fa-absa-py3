""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/HierarchyOverrides.py"
"""-------------------------------------------------------------------------------------------
MODULE
    HierarchyOverrides

    (c) Copyright 2017 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Override standard app in some aspects
-------------------------------------------------------------------------------------------"""

import acm
from HierarchySearch import SubscribedHierarchyTree, HierarchyResults
 
def GetRGB(r, g, b):
    return r + (g*256) + (b*256*256)

LIGHT_GREEN = GetRGB( 183, 255, 183 )

import HierarchyEditorApp

def CreateApplicationInstance():
    return HierarchyEditorApplicationWithHighlighting()


class HierarchyEditorApplicationWithHighlighting(HierarchyEditorApp.HierarchyEditorApplication):
    def __init__(self):
        HierarchyEditorApp.HierarchyEditorApplication.__init__(self)
        # Additions below
        self.m_highlightValues = set()  # ( FDataValue ) - the FDataValues containing the matched value for the specific column
        self.m_highlightNodes = set()   # ( node ids )   - the parent nodes "leading" to a the nodes in the m_highlightValues (to indicate which nodes should be expanded to see the highlighted cells)
        
    def Clear(self):
        HierarchyEditorApp.HierarchyEditorApplication.Clear(self)
        # Additions below
        self.m_highlightValues = {}      
        self.m_highlightNodes = set()   
    
    def UpdateItemFromNode(self, hierarchyNode, treeNode):
        HierarchyEditorApp.HierarchyEditorApplication.UpdateItemFromNode(self, hierarchyNode, treeNode)
        # Additions below - part of the code can be added to an existing iteration over hierarchyNode.HierarchyDataValues()
        def Highlight(treeNode, index, color = LIGHT_GREEN):
            treeNode.Style(index, False, None, color)
        
        for dataValue in hierarchyNode.HierarchyDataValues():
            if dataValue.Original() in self.m_highlightValues:
                index = self.m_columnIndexByColumnDef[dataValue.HierarchyColumnSpecification()]
                Highlight(treeNode, index)
                
        if hierarchyNode.Original() in self.m_highlightNodes:
            Highlight(treeNode, 0)
        
    # Additions below - but there probably is a standard way to pass parameters for initialization?
    def HighlighSearchResults(self, results):
        if isinstance( results, HierarchyResults ):
            self.m_highlighResults = results            # Hold on to result to handle refresh (then tree and criteria are used)
            self.m_highlightValues = results._values
            self.m_highlightNodes = results._nodes
            self.PopulateObject( acm.FHierarchy[ results._tree._name ] )
            
    def CreateHierarchyRefreshCB(self):
        return HierarchyEditorApp.HierarchyNodeCommand(self, self.OnRefreshCB, self.OnAddNodeEnabledCB)

    def Commands(self):
        commands = HierarchyEditorApp.HierarchyEditorApplication.Commands(self)
        return commands + [ ['refreshHL', 'View',  'Refresh', 'Refresh Highlight', 'F5', 'h', self.CreateHierarchyRefreshCB, False ] ]
        
    def OnRefreshCB(self):
        hlr = self.m_highlighResults
        results = hlr._tree.Search( ** hlr._criteria )
        self.HighlighSearchResults( results )
        
