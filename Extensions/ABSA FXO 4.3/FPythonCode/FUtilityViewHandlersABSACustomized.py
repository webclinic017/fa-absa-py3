"""
FUtilityViewHandlersABSACustomized

Functionality where a Utility View is controlled
from the main window selection customized for ABSA.
"""
import acm
from FUtilityViewHandlers import CollectInfo

def UpdateTradeViewer( manager, utilityView ):
    sheet, selection, selectedCell, calculatedValue = CollectInfo( manager )
    
    if not utilityView:
        utilityView = manager.CreateUtilityView( acm.FTradeSheet, 'TradeViewer', 'TradeViewer', None, 'Right', 350 )
        rowObject = selectedCell.RowObject()
        gridBuilder = utilityView.GridBuilder()
        columnCreators = utilityView.ColumnCreators()
        removeCreators = []
        
        for columnIndex in range( columnCreators.Size() ):
            column = columnCreators.At( columnIndex )
            removeCreators.append( column )
        
        for creator in removeCreators:
            columnCreators.Remove( creator )
        
        selectedCells = selection.SelectedCells()
        for cell in selectedCells:
            columnCreators.Add( cell.Column().Creator() ) 
        
        rowObjects = acm.FSet()
        for cell in selectedCells:
            calculatedValue = cell.CalculatedValue()
            
            if calculatedValue:
                businessObject = calculatedValue.Object()
                rowObjects.Add( businessObject )
            
            for object in rowObjects.AsArray():
                utilityView.InsertObject( object, 'IOAP_LAST' )

def PortfolioSheetSelectionInTradeSheet( invokationInfo ):
    manager = invokationInfo.ExtensionObject()
    UpdateTradeViewer( manager, None )
