""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/HierarchyHelpers.py"
"""-------------------------------------------------------------------------------------------
MODULE
    HierarchyHelpers

    (c) Copyright 2017 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Helpers for getting an extended FHierarchy with search functionality and a result from input data
-------------------------------------------------------------------------------------------"""

import acm
from HierarchySearch import SubscribedHierarchyTree, HierarchyResults

def GetTree(name, inputColumnNames):
    return SubscribedHierarchyTree(name, inputColumnNames)

def GetTreeResult(tree, inputValueColumns):
    mappedColumns = dict(list(zip(tree._criteriaColumns, inputValueColumns))) 
    return tree.Search( **mappedColumns ) #Returns a result value from the "missing" result column

def OpenHierarchy(eii):
    def RecurseGraph(evaluator, depth = 3, level = 0):
        try:
            if evaluator.IsEvaluator():         # throws if not an FObject
                cv = evaluator.CachedValue()
                if isinstance( cv, HierarchyResults ):
                    return cv
                if level <= depth:
                    for input in evaluator.Inputs():
                        results = RecurseGraph( input, depth, level + 1 )
                        if results is not None:
                            return results
        except:
            pass
                
    results = RecurseGraph( eii.ExtensionObject().ActiveSheet().Selection().SelectedCell().Evaluator() )
    
    if isinstance( results, HierarchyResults ):
        frame = acm.UX().SessionManager().StartApplication( 'Hierarchy Editor', None )
        frame.CustomLayoutApplication().HighlighSearchResults( results )
