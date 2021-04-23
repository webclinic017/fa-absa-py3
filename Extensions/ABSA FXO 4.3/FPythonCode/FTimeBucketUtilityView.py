import acm
timeBucketViewName = 'TimeBucketPortfolioViewer'
volatilityColumns = ['Portfolio Vega', 'Portfolio Vega Beta', 'Portfolio Vega Weighted', 'Portfolio Vega Weighted Root T', 'Portfolio Vanna', 'Portfolio Vanna Cash', 'Portfolio Vanna Cash FXO', 'Portfolio Volga']

def CollectInfo( manager ):
    sheet = manager.ActiveSheet()
    selection = None
    selectedCell = None
    calculatedValue = None
    if sheet:
        selection = sheet.Selection()
        if selection:
            selectedCell = selection.SelectedCell()
            if selectedCell:
                calculatedValue = selectedCell.CalculatedValue()
    return sheet, selection, selectedCell, calculatedValue

def UpdatePortfolioViewer(manager, utilityView):
    sheet, selection, selectedCell, calculatedValue = CollectInfo(manager)

    if calculatedValue:
        rowObject = selectedCell.RowObject()
        if ('FTimeBucketAndObject' != str(rowObject.ClassName())):
            acm.Log('This command only works for Projected Risk Time Bucket rows.')
            return
            
        if not utilityView:
            utilityView = manager.GetUtilityView(timeBucketViewName)
        if not utilityView:
            utilityView = manager.CreateUtilityView(acm.FPortfolioSheet, timeBucketViewName, 'Portfolio Viewer', None, 'Right', 250)

        columnCreators = utilityView.ColumnCreators()
        utilityView.ColumnCreators().Clear()
        column = selectedCell.Column()
        targetColumnCreator = column.Creator()
        #columnCreators.Add(targetColumnCreator)

        scenario = acm.FExplicitScenario()
        shiftVector = acm.CreateReplaceShiftVector('time distribution', None)
        shiftVector.AddReplaceShiftItem([rowObject.TimeBucket()])
        scenario.AddShiftVector(shiftVector)

        if str(column.ColumnId()) in volatilityColumns:
            shiftVector = acm.CreateReplaceShiftVector('time distribution is expiry', None)
            shiftVector.AddReplaceShiftItem([True])
            scenario.AddShiftVector(shiftVector)
                
        columnCreators.Add(targetColumnCreator.ApplyScenario(scenario))
        
        utilityView.RemoveAllRows()
        instrumentAndTrades = rowObject.Object()
        #instrumentAndTrades.Builder().IncludeSingleInstruments(True)
        utilityView.InsertObject(instrumentAndTrades, 'IOAP_LAST' )
        iterator = utilityView.GridBuilder().RowTreeIterator().FirstChild()
        if iterator:
            iterator.Tree().Expand(True)
        columnIterator = utilityView.GridBuilder().GridColumnIterator().First()
        utilityView.SortColumn(columnIterator, False)

def HandleSelectionChanged(invokationInfo, sheetClass, viewId, method):
    manager = invokationInfo.ExtensionObject()
    sheet = manager.ActiveSheet()
    if sheet and (sheet.SheetClass() == sheetClass):
        utilityView = manager.GetUtilityView(viewId)
        if utilityView:
            method(manager, utilityView)

def TimeBucketPortfolioViewer_SelChanged(invokationInfo, viewChanged):
    HandleSelectionChanged( invokationInfo, acm.FPortfolioSheet, timeBucketViewName, UpdatePortfolioViewer)

def TimeBucketSelectionInPortfolioView(invokationInfo):
    manager = invokationInfo.ExtensionObject()
    UpdatePortfolioViewer(manager, None)
