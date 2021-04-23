""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/HierarchySearch.py"

"""-------------------------------------------------------------------------------------------
MODULE
    HierarchySearch

    (c) Copyright 2017 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Implements a custom search algorithm for a given tree, input criteria in -> result column out
-------------------------------------------------------------------------------------------"""

import acm
from collections import OrderedDict

class HierarchyResults:
    def __init__(self, tree, criteria, results, nodes):
        self._tree = tree
        self._criteria = criteria
        self._results = results # { string -> FHierarchyDataValue }, consuming code should use FHierarchyDataValue.DataValueVA() to get actual value
        self._values = OrderedDict.fromkeys( [ value for value in results.values() if value ] ) # OrderedDict.fromkeys( FHierarchyDataValue )
        self._nodes = OrderedDict.fromkeys( [ node for group in nodes.values() for node in group ] ) # OrderedDict.fromkeys( FHierarchyNode ) - nodes are { string -> ( FHierarchyNode ), string -> ( FHierarchyNode ) ... }
        self._stringResults = dict( [ [ key, value.DataValue() if value else None ] for key, value in results.iteritems() ] ) # string representation of values, nice for testing/viewing
        self._values = self._values.keys()
        self._nodes = self._nodes.keys()

    def Result(self):
        return self._results


class HierarchyTree:
    def __init__(self, name, criteriaColumns, resultColumns = None, resultFunction = None):
        self._nodes = {}
        self._name = name
        self._hierarchy = acm.FHierarchy[ name ]
        columnNames = { spec.Name() for spec in self._hierarchy.HierarchyType().HierarchyColumnSpecifications() }
        self._criteriaColumns = OrderedDict.fromkeys( criteriaColumns ) if criteriaColumns is not None else OrderedDict.fromkeys( columnNames.difference( resultColumns ) )
        self._resultColumns = OrderedDict.fromkeys( resultColumns ) if resultColumns is not None else OrderedDict.fromkeys( columnNames.difference( criteriaColumns ) )
        self._resultFunction = resultFunction or self.DefaultFunction   # If a resultFunction is provided it can be used to perform actions based upon the results before returning a value
        self._criteriaColumns = self._criteriaColumns.keys()
        self._resultColumns = self._resultColumns.keys()

        self.Initialize()

    def Initialize(self):
        self._tree = acm.FHierarchyTree()                       # Create empty tree
        self._tree.Hierarchy( self._hierarchy )                 # Load hierarchy into tree
        self._root = self.FindNode( self._tree.RootNode() )
        self._root.AddChildren()

    def FindNode(self, node, *args):
        return self._nodes.get( node, None ) or self._nodes.setdefault( node, self.NodeFactory( node, *args ) )

    def NodeFactory(self, node, *args):
        return HierarchyNode( self, node, *args )

    def Search(self, **criteria):
        result, nodes = self._root.Search( criteria = criteria, result = self.DefaultResults(), nodes = {} )
        return self._resultFunction( HierarchyResults( self, criteria, result, nodes ) )

    def DefaultFunction(self, result):
        return result          # Default behaviour is to simply return the result dictionary

    def DefaultResults(self):
        return dict.fromkeys( self._resultColumns )     # Default behaviour is to create entries for all resultColumn names with a None value

    def ContinueSearch(self, node, matched):
        return matched     # Default is to stop search in current branch if current level failed to match - override in derived class to implement other smartness here


class SubscribedHierarchyTree( HierarchyTree ):
    def Initialize(self):
        self._hierarchy.HierarchyNodes().AddDependent( self )   # Subscribe to changes
        self._update = True
        self._wa = acm.FArray()
        self._wa.Add( 0 )

    def NodeFactory(self, node, *args):
        return SubscribedHierarchyNode( self, node, *args )

    def Notify(self):
        self._wa.Add( self._wa.At( 0 ) + 1 )
        self._wa.RemoveAt( 0 )

    def ServerUpdate(self, sender, aspect, param):
        if aspect.AsString() in ['insert', 'remove'] : # When a node is inserted/removed, the tree is re-evaluated
            self.Update()
        self._update = True
        self.Notify()

    def Update(self):
        if self._update:
            HierarchyTree.Initialize(self)
        self._update = False

    def Search(self, **criteria):
        self.Update()
        return HierarchyTree.Search(self, **criteria)


def YieldKeysAndValues(values, columnFilter):
    for value in values:
        name = value.HierarchyColumnSpecification().Name()
        if name in columnFilter:
            yield name, value

class HierarchyNode:
    ai = acm.EnumFromString( 'B92RecordType', 'AdditionalInfo' )
    def __init__(self, tree, node, *nodes):
        self._tree = tree
        self._node = node
        self._nodes = nodes
        self.Initialize()

    def GetCompareMethod(self, value):
        if value.HierarchyColumnSpecification().DataTypeGroup() == 'RecordRef':
            return value.DataValue
        else:
            return value.DataValueVA

    def Initialize(self):
        criteriaColumns = self._tree._criteriaColumns
        resultColumns = self._tree._resultColumns
        values = self._node.HierarchyDataValues()
        self._criteria = dict( [ [ key, self.GetCompareMethod( value ) ] for key, value in YieldKeysAndValues( values, criteriaColumns ) ] )    # Only non-None values
        self._result   = dict( [ [ key,  value ] for key, value in YieldKeysAndValues( values, resultColumns   ) ] )                            # Only non-None values
        self._parents  = dict( [ [ key, self._nodes ] for key in self._result.keys() ] )                                                        # To keep track of what nodes should be expanded to get to a matched result

    def AddChildren(self):
        self._children = [ self._tree.FindNode( child, self._node, *self._nodes ) for child in self._tree._tree.Children( self._node ) or [] ]
        for child in self._children:
            child.AddChildren()

    def CompareValues(self, findValue, compareMethod, name):
        # If column names are Valid To/From, check a range (supported for date columns)
        if name == 'Valid To':
            return findValue <= compareMethod()
        elif name == 'Valid From':
            return findValue >= compareMethod()

        return findValue == compareMethod()

    def Match(self, criteria, result, nodes):
        StringKeyValue = lambda v: v.StringKey() if hasattr(v, 'StringKey') else v
        for key, compareMethod in self._criteria.iteritems():
            if not self.CompareValues( StringKeyValue( criteria.get( key, None ) ), compareMethod, key):
                return False
        # Update result set - only if all criteria specified matched
        result.update( self._result )
        nodes.update( self._parents )
        return True

    def Search(self, criteria, result, nodes):
        matched = self.Match( criteria, result, nodes )
        if self._tree.ContinueSearch( self, matched ):
            for child in self._children:
                child.Search( criteria, result, nodes )
        return result, nodes


class SubscribedHierarchyNode( HierarchyNode ):
    def Initialize(self):
        self._update = True
        self._node.HierarchyDataValues().AddDependent( self )

    def ServerUpdate(self, sender, aspect, param):
        if aspect.AsString() == 'update':
            if param.HierarchyColumnSpecification().Name() in self._tree._resultColumns:
                return
        self._update = True
        self._tree.Notify()

    def Update(self):
        if self._update:
            HierarchyNode.Initialize( self )
        self._update = False

    def Search(self, criteria, result, nodes):
        self.Update()
        return HierarchyNode.Search( self, criteria, result, nodes )

