"""--------------------------------------------------------------------------
MODULE
   FUploaderUtils

DESCRIPTION
    This module houses the common funstionality of uploaders

HISTORY 
Date: 2019-10-10 
Jira:  FAFO-23 - Added common functionality to display trades output
   
-----------------------------------------------------------------------------"""
import acm
import FRunScriptGUI
import FUxCore


class CreateOutput(FUxCore.LayoutDialog):
    # Embedding trading manager sheets into custom dialogs

    def __init__(self, caption, trades):
        self.caption = caption
        self.trade_sheet = None
        self.trade_portfolio = None
        trade_list = trades
        
        # Add trades to the sheet
        self.add_trades(trade_list)

    def initialise_sheet(self,default_columns = None):
        if default_columns is not None:
            context = acm.GetDefaultContext()
            default_columns = acm.GetColumnCreators(default_columns, context)
            columns = self.trade_sheet.ColumnCreators()
            columns.Clear()
            
            for i in range(default_columns.Size()):
                columns.Add(default_columns.At(i))

        self.trade_sheet.InsertObject(self.trade_portfolio, 'IOAP_LAST')
        self.trade_sheet.PrivateTestSyncSheetContents()

    def add_trades(self, trade_list):
        # Insert Items and add to the sheet.
        self.trade_portfolio = acm.FASQLQueryFolder()
        self.trade_portfolio.Name(self.caption)
        query = acm.CreateFASQLQuery('FTrade', 'OR')

        for trade in trade_list:
            query.AddOpNode('OR')
            query.AddAttrNode('Oid', 'EQUAL', trade.Oid())

        self.trade_portfolio.AsqlQuery(query)

    def CreateLayout(self):
        # Create the dialog layout
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')

        b.AddSpace(5)
        b.AddSeparator()
        b.AddSpace(5)
        b.BeginVertBox()
        b.AddCustom('trade_sheet', 'sheet.FTradeSheet', 500, 250)
        b.EndBox()
        b.AddSpace(5)
        b.AddSeparator()

        b.AddSpace(10)
        b.BeginHorzBox()
        b.AddFill()
        b.AddButton('ok', 'OK')
        b.AddButton('cancel', 'Cancel')
        b.EndBox()
        b.EndBox()

        return b

    def HandleCreate(self, dialog, layout):
        self.dialog = dialog
        dialog.Caption(self.caption)

        # get a handle to the sheet
        ctrl = layout.GetControl
        self.trade_sheet = ctrl('trade_sheet').GetCustomControl()

        self.initialise_sheet()

    def HandleApply(self):
        return True
