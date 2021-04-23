from __future__ import print_function
import acm
import FQuoteDataSource

          
def openSpreadTable(invokationInfo):
    onMenuOpenSpreadTable(invokationInfo, 'Spread Upper Limit Spread Table')

def openMinSpreadTable(invokationInfo):
    onMenuOpenSpreadTable(invokationInfo, 'Spread Lower Limit Min Spread Table')
 
def onMenuOpenSpreadTable(invokationInfo, columnId):
    tm = invokationInfo.ExtensionObject()
    sheet = tm.ActiveSheet()
    selection = sheet.Selection()
    cell = selection.SelectedCell()
    
    if cell:
        row = cell.RowObject()
        try:
            qc = row.QuoteController()
            if qc:
                openTable(qc, columnId, invokationInfo)
        except:
            pass

def showTable(table):
    acm.FTmServer().StartApplication('Spread Table Definition', table)
    
def showError(invokationInfo, message):
    shell = invokationInfo.Parameter('shell')
    if shell:
        acm.UX().Dialogs().MessageBoxInformation(shell, message)
    else:
        print (message)
        
def openTable(quoteController, columnId, invokationInfo):
    if quoteController.IsPrepared():
        source = quoteController.CreateDataSource(columnId)
        if source:
            FQuoteDataSource.ValueInvoker(source, showTable)
        else:
            showError(invokationInfo, 'Spread table data source not found: ' + columnId)
    else:
        showError(invokationInfo, 'Quoting must be prepared to show spread tables')

def onOpenSpreadTable(invokationInfo):
    button = invokationInfo.Parameter("ClickedButton")
    if button:
        row = button.RowObject()
        quoteController = row.QuoteController()
        openTable(quoteController, 'Spread Upper Limit Spread Table', invokationInfo)
    
def onOpenMinSpreadTable(invokationInfo):
    button = invokationInfo.Parameter("ClickedButton")
    if button:
        row = button.RowObject()
        quoteController = row.QuoteController()
        openTable(quoteController, 'Spread Lower Limit Min Spread Table', invokationInfo)
