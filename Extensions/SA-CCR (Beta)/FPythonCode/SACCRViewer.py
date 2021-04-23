

from collections import OrderedDict

import acm
import FUxCore

from SACCRViewerGrid import Grid, GridTreeBuilder, GridColumn, GridCommandItem
from SACCRViewerSourceData import SourceData, GetValuesForColumns

#------------------------------------------------------------------------------
# Dock Keys
#------------------------------------------------------------------------------
class DockKeys :
    SACCRViewerCreate = 'SACCRViewerCreateDockWindow'
    SACCRViewer       = 'SACCRViewerDockWindow'
    SACCRCaption      = 'SA-CCR Viewer'

#------------------------------------------------------------------------------
# Default Settings
#------------------------------------------------------------------------------
DEFAULT_DECIMALS = 2
DEFAULT_DECIMALS_CURRENCY = 0

DEFAULT_COLUMNS = OrderedDict([('Add-On', DEFAULT_DECIMALS_CURRENCY),
                               ('Effective Notional',  DEFAULT_DECIMALS_CURRENCY),
                               ('Delta', DEFAULT_DECIMALS),
                               ('Maturity Factor', DEFAULT_DECIMALS),
                               ('Adjusted Notional', DEFAULT_DECIMALS_CURRENCY),
                               ('Duration', DEFAULT_DECIMALS),
                               ('Notional', DEFAULT_DECIMALS_CURRENCY),
                               ('Latest Exercise', DEFAULT_DECIMALS),
                               ('End', DEFAULT_DECIMALS),
                               ('Start', DEFAULT_DECIMALS),
                               ('Maturity', DEFAULT_DECIMALS)])

#------------------------------------------------------------------------------
# Callbacks
#------------------------------------------------------------------------------
def OnRefreshClicked( self, cd ):
    self.RefreshViewer()

#------------------------------------------------------------------------------
# Grid commands
#------------------------------------------------------------------------------
class OnInsertColumnGridCommandItem( GridCommandItem ):
    def __init__( self, subject, invokeMethod, enabled=True ):
        self.m_enabled = enabled
        GridCommandItem.__init__( self, subject, invokeMethod )
        
    def Enabled( self ):
        return self.m_enabled

#------------------------------------------------------------------------------
# SA-CCR Viewer
#------------------------------------------------------------------------------
class SACCRViewer( FUxCore.LayoutPanel ):

    #------------------------------------------------------------------------------
    def __init__( self, parent, ):
        self.m_parent = parent
        self.m_creditBalance = self.GetSelectedCreditBalance()
    
    #------------------------------------------------------------------------------
    def CreateGrid(self):
        self.m_addOnGrid = Grid( 'addOnGrid', self.CreateGridTreeBuilder() )
    
    #------------------------------------------------------------------------------
    def CreateGridTreeBuilder( self ):
        if self.m_creditBalance:
            portfolio = self.m_creditBalance.BalancePortfolio()
            sourceData = SourceData(portfolio)
    
            return GridTreeBuilder( sourceData, ['Asset Class', 'Hedging Set', 'Hedging Subset'] )
        
        return None
    
    #------------------------------------------------------------------------------
    def AddColumns( self ):
        savedColumns = self.InitialContents()
        
        if savedColumns:
            for column in savedColumns:
                self.m_addOnGrid.AddColumn( GridColumn( column['colName'], column['decimals'] ) )
        else:
            for col, decimals in DEFAULT_COLUMNS.iteritems():
                self.m_addOnGrid.AddColumn( GridColumn( col, decimals ) )
    
    #------------------------------------------------------------------------------
    def GetContents( self ):
        """ Called by UX framework when saving a workspace to obtain the LayoutPanels contents.
        """
        columnsToSave = acm.FArray()
        
        for col in self.m_addOnGrid.GetColumns():
            column = acm.FDictionary()
            column["colName"] = col.m_name
            column["decimals"] = col.m_decimals
            columnsToSave.Add(column)
        
        return columnsToSave

    #------------------------------------------------------------------------------
    def GetSelectedSheetCell( self ):
        sheet = self.m_parent.ActiveSheet()
        if sheet:
            selection = sheet.Selection()
            if selection:
                return selection.SelectedCell()
    
    #------------------------------------------------------------------------------
    def GetRowObject( self ):
        row = None 
        cell = self.GetSelectedSheetCell()
        if cell:
            row = cell.RowObject()
        return row       
    
    #------------------------------------------------------------------------------
    def GetSelectedCreditBalance( self ):
        rowObject = self.GetRowObject()
        if rowObject:
            instrument = rowObject.Instrument()
            return instrument if instrument.Class() == acm.FCreditBalance else None
        else:
            return None
    
    #------------------------------------------------------------------------------
    def SetCreditBalance( self ):
        self.m_creditBalance = self.GetSelectedCreditBalance()
        self.RefreshViewer()
    
    #------------------------------------------------------------------------------
    def RefreshViewer( self ):
        if self.m_creditBalance:
            self.SetValues()
            self.m_creditBalanceName.SetData( self.m_creditBalance.Name() )
            self.m_addOnGrid.UpdateGrid( self.CreateGridTreeBuilder() )
    
    #------------------------------------------------------------------------------
    def HandleCreate( self ):
        self.CreateGrid()
        
        layout = self.SetLayout( self.CreateLayout() )
        
        self.m_refreshBtn = layout.GetControl( "refreshButton" )
        self.m_refreshBtn.AddCallback( "Activate", OnRefreshClicked, self )
        self.m_refreshBtn.ToolTip( "The Refresh command initiates an update of all calculated values in the viewer" )
        
        self.m_creditBalanceName = layout.GetControl( "creditBalanceName" )
        self.m_mtm = layout.GetControl( "markToMarket" )
        self.m_collmtm = layout.GetControl( "collMarkToMarket" )
        self.m_replacementCost = layout.GetControl( "replacementCost" )
        self.m_addOn = layout.GetControl( "addOn" )
        self.m_addOnMultiplier = layout.GetControl( "addOnMultiplier" )
        self.m_pfe = layout.GetControl( "potentialFutureExposure" )
        self.m_ead = layout.GetControl( "exposureAtDefault" )
        
        self.m_mtm.Editable( False )
        self.m_collmtm.Editable( False )
        self.m_replacementCost.Editable( False )
        self.m_addOn.Editable( False )
        self.m_addOnMultiplier.Editable( False )
        self.m_pfe.Editable( False )
        self.m_ead.Editable( False )
        self.m_creditBalanceName.Editable( False )
        
        if self.m_creditBalance:
            self.SetValues()
        
        self.m_addOnGrid.HandleCreate( layout )
        self.AddColumns()
        self.m_addOnGrid.AddCallback( 'ContextMenu', self.OnContextMenu )
    
    #------------------------------------------------------------------------------
    def SetValues( self ):
        columns = ["SA-CCR Mark To Market", "SA-CCR Collateral Mark To Market", "SA-CCR Replacement Cost", "SACCR Add-On", \
                   "SACCR Add-On Multiplier", "SACCR Potential Future Exposure", "SACCR Exposure At Default"]
        
        values = GetValuesForColumns( self.m_creditBalance, columns )
        
        self.SetValue( self.m_mtm, values["SA-CCR Mark To Market"], DEFAULT_DECIMALS_CURRENCY )
        self.SetValue( self.m_collmtm, values["SA-CCR Collateral Mark To Market"], DEFAULT_DECIMALS_CURRENCY )
        self.SetValue( self.m_replacementCost, values["SA-CCR Replacement Cost"], DEFAULT_DECIMALS_CURRENCY )
        self.SetValue( self.m_addOn, values["SACCR Add-On"], DEFAULT_DECIMALS_CURRENCY )
        self.SetValue( self.m_addOnMultiplier, values["SACCR Add-On Multiplier"], DEFAULT_DECIMALS )
        self.SetValue( self.m_pfe, values["SACCR Potential Future Exposure"], DEFAULT_DECIMALS_CURRENCY )
        self.SetValue( self.m_ead, values["SACCR Exposure At Default"], DEFAULT_DECIMALS_CURRENCY )
        
        self.m_creditBalanceName.SetData( self.m_creditBalance.Name() )
    
    #------------------------------------------------------------------------------
    def SetValue( self, column, value, decimals ):
        roundedValue = round( float( value ), decimals )
        formattedValue = format( roundedValue, '.%df' % decimals )
        column.SetData( formattedValue.replace( '.', ',' ) )
    
    #------------------------------------------------------------------------------
    def CreateLayout( self ):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginHorzBox( 'Invisible', '', 'backgroundBox' )
        b.    AddInput( 'creditBalanceName', 'Credit Balance', 30, 45, 25 )
        b.    AddFill()
        b.  EndBox()
        b.BeginHorzBox( 'Invisible', '', 'backgroundBox' )
        b.  BeginVertBox( 'EtchedIn', 'Exposure at Default' )
        b.    AddInput( 'exposureAtDefault', 'Exposure at Default' )
        b.  EndBox()
        b.  BeginVertBox( 'EtchedIn', 'Replacement Cost' )
        b.    AddInput( 'replacementCost', 'Replacement Cost' )
        b.    AddInput( 'markToMarket', 'Mark-to-Market' )
        b.    AddInput( 'collMarkToMarket', 'Collateral Mark-to-Market' )
        b.  EndBox()
        b.  BeginVertBox( 'EtchedIn', 'Potential Future Exposure' )
        b.    AddInput( 'potentialFutureExposure', 'Potential Future Exposure' )
        b.    AddInput( 'addOnMultiplier', 'Add-On Multiplier' )
        b.    AddInput( 'addOn', 'Add-On' )
        b.  EndBox()
        b.EndBox()
        b.  BeginVertBox( 'Invisible', '', 'backgroundBox' )
        b.    BeginHorzBox( 'EtchedIn', 'Add-On' )
        self.m_addOnGrid.CreateLayout( b, 350, 100 )
        b.    EndBox()
        b.    AddButton( 'refreshButton', 'Refresh' )
        b.  EndBox()
        b.EndBox()
        return b

    #-------------------------------------------------------------------------
    def OnInsertColumn( self, args ):
        control, columnToInsert = args

        columns = control.GetSelectedColumns()
        position = None
        if columns.Size():
            position = columns.At( 0 )
        
        self.m_addOnGrid.InsertColumn( GridColumn( columnToInsert, DEFAULT_COLUMNS[columnToInsert] ), position )
    
    #-------------------------------------------------------------------------
    def OnRemoveColumn( self, column ):
        self.m_addOnGrid.RemoveColumn( column )
    
    #-------------------------------------------------------------------------
    def OnDecimals( self, args ):
        column, decimals = args
        
        self.m_addOnGrid.m_columns[column.Label()].m_decimals = decimals
        self.m_addOnGrid.UpdateColumns()
    
    #-------------------------------------------------------------------------
    def OnExpandCollapseRow( self, row ):
        if row.IsExpanded():
            row.Expand(False)
        else:
            row.Expand(True)
            
    #-------------------------------------------------------------------------
    def OnContextMenu( self, control, cd ):
        menuBuilder = cd.At( 'menuBuilder' )
        selectedCell = control.GetSelectedCell()
        selectedRows = control.GetSelectedItems()
        selectedRow = control.GetSelectedItem()
        selectedColumn = control.GetSelectedColumn()
        
        commands = []
        if selectedCell:
            if 'RowHeader' == str( selectedCell.HeaderType() ):
                self.BuildExpandCollapseCommand( selectedRow, commands )
            if 'ColumnHeader' == str( selectedCell.HeaderType() ):
                self.BuildInsertCommands( control, commands )
                
                if selectedColumn != control.RowHeaderColumn():
                    self.BuildDecimalCommands( selectedColumn, commands )
                    commands.append( ['remove', '', 'Remove column', '', '', '', lambda : GridCommandItem(selectedColumn, self.OnRemoveColumn), False ] )
                
        if commands:
            menuBuilder.RegisterCommands( FUxCore.ConvertCommands(commands) )
    
    #-------------------------------------------------------------------------
    def BuildDecimalCommands( self, selectedColumn, commands ):
        commands.append( ['decimals', '', 'Decimals/' + '<Default>', '', '', '', lambda : GridCommandItem([selectedColumn, DEFAULT_COLUMNS[selectedColumn.Label()]], self.OnDecimals), False ] )
        for i in range(0, 7):
            commands.append( ['decimals', '', 'Decimals/' + str(i), '', '', '', lambda decimals = i : GridCommandItem([selectedColumn, decimals], self.OnDecimals), False ] )
    
    #-------------------------------------------------------------------------
    def BuildExpandCollapseCommand( self, selectedRow, commands ):
        if selectedRow.NumberOfChildren():
            commandLabel = "Collapse Row" if selectedRow.IsExpanded() else "Expand Row"
            commands.append( ['expandCollapseRow', '', commandLabel, '', '', '', lambda: GridCommandItem(selectedRow, self.OnExpandCollapseRow), False ] )
    
    #-------------------------------------------------------------------------
    def BuildInsertCommands( self, control, commands ):
        defaultColumns = set( DEFAULT_COLUMNS.keys() )
        currentColumns = self.m_addOnGrid.m_columns.keys()
        
        columnsToInsert = defaultColumns.difference( currentColumns )
        
        if not columnsToInsert:
            commands.append( ['insert', '', 'Insert column', '', '', '', lambda : OnInsertColumnGridCommandItem(control, self.OnInsertColumn, False), False ] )
        else:
            for col in columnsToInsert:
                commands.append( ['insert', '', 'Insert column/' + col, '', '', '', lambda x = col : OnInsertColumnGridCommandItem([control, x], self.OnInsertColumn), False ] )
    
#-------------------------------------------------------------------------
class SACCRCalculatorMenuItem( FUxCore.MenuItem ):
    def __init__( self, extObj ):
        self.m_extObj = extObj
    
    #------------------------------------------------------------------------------
    def IsMenuEnabled( self, extObj ):
        applicable = False
        
        try:
            instrument = extObj.ActiveSheet().Selection().SelectedCell().RowObject().Instrument()
            
            if instrument and (instrument.Class() == acm.FCreditBalance):
                applicable = True
        except:
            pass
            
        return applicable
    
    #------------------------------------------------------------------------------
    def Invoke( self, eii ):
        basicApp = eii.ExtensionObject()
        if self.IsMenuEnabled( basicApp ):
            try :
                basicApp.ShowDockWindow( DockKeys.SACCRViewer, True )
            except Exception as e:
                basicApp.CreateRegisteredDockWindow( DockKeys.SACCRViewerCreate, DockKeys.SACCRViewer, DockKeys.SACCRCaption, 'Bottom', True, True, False, True )
                
            customDockWindow = basicApp.GetCustomDockWindow( DockKeys.SACCRViewer )
            customDockWindow.CustomLayoutPanel().SetCreditBalance()
            

    #------------------------------------------------------------------------------
    def Applicable( self ):
        return True
        
    #------------------------------------------------------------------------------
    def Enabled( self ):
        return self.IsMenuEnabled( self.m_extObj )

#------------------------------------------------------------------------------
def CreateSACCRViewer( eii ) :
    basicApp = eii.ExtensionObject()
    myPanel = SACCRViewer( basicApp )
    return myPanel

#-------------------------------------------------------------------------
def CreateSACCRCalculatorMenuItem( extObj ):
    return SACCRCalculatorMenuItem( extObj )

#------------------------------------------------------------------------------    
def Create( eii ) :
    basicApp = eii.ExtensionObject()
    dockWindow = basicApp.GetCustomDockWindow( DockKeys.SACCRViewer )
    
    try:
        if dockWindow :
            basicApp.DestroyDockWindow( DockKeys.SACCRViewer )
        else:
            basicApp.CreateRegisteredDockWindow( DockKeys.SACCRViewerCreate, DockKeys.SACCRViewer, DockKeys.SACCRCaption, 'Bottom' )
    except Exception as e:
        print (str( e ))

#------------------------------------------------------------------------------    
def OnCreate( eii ):
    basicApp = eii.ExtensionObject()
    basicApp.RegisterDockWindowType( DockKeys.SACCRViewerCreate, 'SACCRViewer.CreateSACCRViewer' )
