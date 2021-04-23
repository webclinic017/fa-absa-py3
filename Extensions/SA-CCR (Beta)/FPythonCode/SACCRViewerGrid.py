
from itertools import groupby

import acm
import FUxCore

#------------------------------------------------------------------------------
# GridRowDisplayer
#------------------------------------------------------------------------------
class GridRowDisplayer( object ):
    
    #------------------------------------------------------------------------------
    def Label( self, sourceData ):
        if isinstance(sourceData, str):
            return sourceData
    
        if sourceData.IsKindOf(acm.FCashFlow):
            return "Cash Flow | " + sourceData.Leg().Instrument().Name()
    
        return sourceData.StringKey()
    
    #------------------------------------------------------------------------------
    def Icon( self, sourceData, grouping=False ):
        if grouping:
            return 'Folder'
            
        if sourceData.IsKindOf(acm.FCashFlow):
            return "CashFlow"
            
        return sourceData.Icon()

#------------------------------------------------------------------------------
# Grouped Grid Data
#------------------------------------------------------------------------------
class GridTreeBuilder( object ):
 
    #------------------------------------------------------------------------------
    # Grid Node
    #------------------------------------------------------------------------------
    class GridNode( object ):

        def __init__( self, label, icon ):
            self.m_label = label
            self.m_icon = icon
            self.m_values = acm.FDictionary()
            self.m_children = dict()
 
    #------------------------------------------------------------------------------
    def __init__( self, sourceData, groupingAttributes ):
        self.m_sourceData = sourceData
        self.m_groupingAttributes = groupingAttributes
        self.m_rowDisplayer = GridRowDisplayer()
    
    #------------------------------------------------------------------------------
    def BuildTree( self ):
        tree = self.GridNode("Total", "Folder")
        tree.m_values = self.m_sourceData.GetAggregatedData([])
    
        keyTuple = lambda x : tuple(x[attr] for attr in self.m_groupingAttributes)
        sortedData = sorted(self.m_sourceData.GetSourceData(), key=keyTuple)
        
        for keys, datas in groupby(sortedData, key=keyTuple):
            keys = filter(None, keys)
        
            groupingNode = self.GetGroupingNode(tree, keys, 0)
            
            for data in datas:
                dataNode = self.GridNode(self.m_rowDisplayer.Label(data['Source']), self.m_rowDisplayer.Icon(data['Source']))
                dataNode.m_values = data
                groupingNode.m_children[data] = dataNode
                
        return tree
    
    #------------------------------------------------------------------------------
    def GetGroupingNode( self, node, levels, idx ):
        if len(levels) <= idx:
            return node
            
        key = levels[idx]
        
        children = node.m_children
        
        if key not in children:
            newGroupingNode = self.GridNode(self.m_rowDisplayer.Label(key), self.m_rowDisplayer.Icon(key, True))
            newGroupingNode.m_values = self.m_sourceData.GetAggregatedData( levels[0:idx+1] )
            
            children[key] = newGroupingNode
        
        return self.GetGroupingNode(children[key], levels, idx+1)

#------------------------------------------------------------------------------
# Grid Column
#------------------------------------------------------------------------------
class GridColumn( object ):
    def __init__( self, name, decimals=2 ):
        self.m_name = name
        self.m_decimals = decimals
    
    #------------------------------------------------------------------------------
    def SetFormattedValue( self, cell, value ):
        if value:
            cell.Alignment( 'Right' )
            roundedValue = round( float( value ), self.m_decimals )
            formattedValue = format( roundedValue, '.%df' % self.m_decimals )
            
            cell.SetData( formattedValue.replace( '.', ',' ) )

#------------------------------------------------------------------------------
# Grid Command
#------------------------------------------------------------------------------
class GridCommandItem(FUxCore.MenuItem):
    def __init__(self, subject, invokeMethod):
        self._subject = subject
        self._invokeMethod = invokeMethod
        
    @FUxCore.aux_cb
    def Invoke(self, cd):
        if self._subject:
            return self._invokeMethod(self._subject)
    
    def Applicable(self):
        return True
        
    def Enabled(self):
        return True
    
    def Checked(self):
        return False

#------------------------------------------------------------------------------
# Grid
#------------------------------------------------------------------------------
class Grid( object ):
    def __init__( self, name, gridTreeBuilder ):
        self.m_gridName = name
        self.m_gridTreeBuilder = gridTreeBuilder
        self.m_gridCtrl = None
        self.m_columns = {}
        self.m_rowColumnData = {}
    
    #------------------------------------------------------------------------------
    def HandleCreate( self, layout ):
        self.m_gridCtrl = layout.GetControl( self.m_gridName )
        self.m_gridCtrl.RowHeaderCaption( "" )
        self.m_gridCtrl.RowHeaderColumn().Width( 200 )
        self.Populate()
        
    #------------------------------------------------------------------------------
    def AddCallback(self, name, cb):
        self.m_gridCtrl.AddCallback( name, cb, self.m_gridCtrl )
        
    #------------------------------------------------------------------------------
    def AddColumn(self, column):
        self.m_gridCtrl.AddColumn( column.m_name, 100 )
        self.m_columns[column.m_name] = column

    #------------------------------------------------------------------------------
    def GetColumns(self):
        orderedColumns = []
        columnIterator = self.m_gridCtrl.GridColumnIterator()
        
        while columnIterator.Next():
            column = columnIterator.GridColumn()
            orderedColumns.append(self.m_columns[column.Label()])
            
        return orderedColumns
        
    #------------------------------------------------------------------------------
    def CreateLayout( self, builder, width, height ):
        builder.AddGrid( self.m_gridName, width, height )
    
    #------------------------------------------------------------------------------
    def Populate( self ):
        if self.m_gridTreeBuilder:
            root = self.m_gridCtrl.GetRootItem()
            self.PopulateRecursive( self.m_gridTreeBuilder.BuildTree(), root )
    
    #------------------------------------------------------------------------------
    def UpdateGrid( self, gridTreeBuilder ):
        self.m_gridTreeBuilder = gridTreeBuilder
        self.m_gridCtrl.RemoveAllItems()
        self.Populate()
    
    #------------------------------------------------------------------------------
    def InsertColumn( self, columnToInsert, position ):
        columnName = columnToInsert.m_name
    
        inserted = self.m_gridCtrl.InsertColumnAt(position, False)
        inserted.Label( columnName )
        
        self.m_columns[columnName] = columnToInsert
        self.UpdateColumns()
    
    #------------------------------------------------------------------------------
    def RemoveColumn( self, column ):
        self.m_columns.pop( column.Label() )
        self.m_gridCtrl.RemoveColumn( column )
    
    #------------------------------------------------------------------------------
    def UpdateColumns( self ):
        root = self.m_gridCtrl.GetRootItem()
        i = root.Iterator().NextUsingDepthFirst()
        
        while i:
            self.SetColumnValues( i.Tree() )
            i = i.NextUsingDepthFirst()
            
    #------------------------------------------------------------------------------
    def PopulateRecursive( self, node, treeParent ):
        newTreeItem = treeParent.AddChild()
        newTreeItem.Label( node.m_label )
        newTreeItem.Icon( node.m_icon )
        
        self.m_rowColumnData[newTreeItem] = node.m_values
        self.SetColumnValues( newTreeItem )
        
        for key, child in node.m_children.iteritems():
            self.PopulateRecursive( child, newTreeItem )
            
    #------------------------------------------------------------------------------
    def SetColumnValues( self, treeItem ):
        values = self.m_rowColumnData[treeItem]
    
        columnIterator = self.m_gridCtrl.GridColumnIterator()
        
        while columnIterator.Next():
            column = columnIterator.GridColumn()
            cell = treeItem.GetCell( column )

            self.m_columns[column.Label()].SetFormattedValue( cell, values.At( column.Label(), None ) )
