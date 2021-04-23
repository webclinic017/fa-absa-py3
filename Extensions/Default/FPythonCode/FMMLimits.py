from __future__ import print_function
import acm

def getLimitName(portfolio, colId, instrument, perUnd):
        
    if not portfolio:
        return ''
    extValName = colId.replace(' ', '')
    extValName += "'" + portfolio.Name()

    if perUnd:
        underlying = instrument.UnderlyingOrSelf()
        if not underlying:
            return ''
        extValName += '/' + underlying.Name()
    else:
        extValName += '/' + instrument.Name()
    extValName += "'"
    return extValName

def isPerUndLimit(groupLabel):
    return groupLabel == 'Delta Limit' #expand with others...

def saveLimitValue(row, col, cell, valString, operation):

    if (str(operation) == 'remove') or not (row.IsKindOf(acm.FSingleInstrumentAndTrades) or row.IsKindOf(acm.FPriceLevelRow)):
        return
    
    groupLabel = col.GroupLabel().AsString()
    colId = col.ColumnId().AsString().replace('/Call', '').replace('/Put', '')  

    ctx = col.Context()
    portfolio = acm.FPhysicalPortfolio[ row.TradingInterface().GetDefaultValueEx('qPortfolio', ctx) ]
    extValName = getLimitName(portfolio, colId, row.Instrument(), isPerUndLimit(groupLabel))
    editModule = ctx.EditModule()
    if extValName:
        if editModule.IsBuiltIn():
            print ('Can not save value to built-in module '+editModule.Name()+\
            '! Please put editable extension module at the bottom of context '+ctx.Name()+'!')
        else:
            acm.SetDefaultValueFromName(ctx, 'FInstrumentAndTrades', extValName, valString)
            editModule.Commit()
    cell.Unsimulate()

def getUnderlyingGrouper():
    return acm.FUnderlyingGrouper()
