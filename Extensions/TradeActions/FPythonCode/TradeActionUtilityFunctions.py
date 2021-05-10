import acm

def DrawDown( trade ):  
    drawDownOffsetMask = 1 << 28
    drawDownChildMask = 1 << 29
    if( trade.TradeProcess() & drawDownOffsetMask ) or ( trade.TradeProcess() & drawDownChildMask ):
        return True
    return False

def ExcludeDrawDownTrades( trades ):
    tradeList = list( trades )
    tradeList[:] = [ trade for trade in tradeList if not DrawDown( trade ) ]
    return tradeList

def GetPosition( rowObject ):
    space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    return space.CalculateValue(rowObject, 'Portfolio Position')

def GetSelectedRows( eii ):
    return eii.ExtensionObject().ActiveSheet().Selection().SelectedRowObjects()
    
def GetSelectedTrades( eii ):
    # TODO: check for FSingleInstrumentAndTrades when iterating
    trades = set()
    selectedCells = eii.ExtensionObject().ActiveSheet().Selection().SelectedCells() # Dependent on number of columns
    for cell in selectedCells:
        tradeCollection = cell.RowObject().Trades().AsIndexedCollection()
        for trade in tradeCollection:
            if trade.Oid() > 0:
                trades.add( trade )

    tradeList = ExcludeDrawDownTrades( trades )
    return tradeList
            
def GetOriginalTrade( row ):
    trades = row.Trades().AsArray()
    originalTrade = None
    for trade in trades:
        if (not originalTrade) or trade.StorageId() < originalTrade.StorageId() :
            originalTrade = trade
    return originalTrade

def ShowError( shell, message ):
    acm.UX().Dialogs().MessageBoxInformation(shell, message);

def ValidateNotDistributedRow( rows ):
    for row in rows:
        if row.IsKindOf('FDistributedRow'):
            return False
    return True

def ValidateIsPosition( rows ):
    for row in rows:
        if not row.IsKindOf('FSingleInstrumentAndTrades'):
            return False
    return rows.Size() > 0
