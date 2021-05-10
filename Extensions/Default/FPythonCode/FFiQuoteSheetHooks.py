"""
Hooks for Fixed Income Quote Sheet
"""
import FFiQuoteSheetHelpFunctions as qs
import acm

def clearQuoteLock(row, side):
    package = row.QuoteController().ProposedQuotePackage()
    level = package.MasterLevelIndex()
    if package:
        InvalidPrice = acm.GetFunction('invalidPrice', 0)
        if side == 'Bid':
            package.Level(level).BidPrice(InvalidPrice())
        if side == 'Ask':
            package.Level(level).AskPrice(InvalidPrice())
        
def preChangeSpreadTypeAsk(row, col, cellInfo, str, operation):
    """Save new spread type on ask side in instrument spread 
    curve if save spread on input toggled.
    """
    qs.pre_change_driver_type(row, str, 'Ask', operation)
    
def preChangeSpreadTypeBid(row, col, cellInfo, str, operation):
    """Save new spread type on bid side in instrument spread 
    curve if save spread on input toggled."""
    qs.pre_change_driver_type(row, str, 'Bid', operation)
            
def saveSpreadToCurve (row, col, cellInfo, value, operation):
    """Save the current spread data to instrument spread curve."""
    quoteController = row.QuoteController()
    if quoteController:
        qs.save_instrument_spread_info(quoteController)

def changeQuoteValueBid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Quote", value, operation, 'Bid')
    clearQuoteLock(row, 'Bid')

def changeISpreadValueBid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "I-Spread", value, operation, 'Bid')
    clearQuoteLock(row, 'Bid')

def changeZSpreadValueBid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Z-Spread", value, operation, 'Bid')
    clearQuoteLock(row, 'Bid')
    
def changeAswSpreadValueBid(row, col, calcval, value, operation):
    qs.change_driver_value(row, qs.get_curve_type(row), value, operation, 'Bid')
    clearQuoteLock(row, 'Bid')
    
def changePriceSpreadValueBid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Price", value, operation, 'Bid')
    clearQuoteLock(row, 'Bid')

def changeYTMSpreadValueBid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "YTM", value, operation, 'Bid')
    clearQuoteLock(row, 'Bid')

def changeYTMValueBid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "YTMValue", value, operation, 'Bid')
    clearQuoteLock(row, 'Bid')

def changeGrossBasisBid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Gross Basis", value, operation, 'Bid')
    clearQuoteLock(row, 'Bid')
    
def changeOffsetValueBid(row, col, calcval, value, operation):
    qs.change_offset(row, value, 'Proposed Quote Offset Bid', 'Bid', operation)
    clearQuoteLock(row, 'Bid')
    
def changeQuoteValueAsk(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Quote", value, operation, 'Ask')
    clearQuoteLock(row, 'Ask')

def changeISpreadValueAsk(row, col, calcval, value, operation):
    qs.change_driver_value(row, "I-Spread", value, operation, 'Ask')
    clearQuoteLock(row, 'Ask')

def changeZSpreadValueAsk(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Z-Spread", value, operation, 'Ask')
    clearQuoteLock(row, 'Ask')
    
def changeAswSpreadValueAsk(row, col, calcval, value, operation):
    qs.change_driver_value(row, qs.get_curve_type(row), value, operation, 'Ask')
    clearQuoteLock(row, 'Ask')

def changePriceSpreadValueAsk(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Price", value, operation, 'Ask')
    clearQuoteLock(row, 'Ask')

def changeYTMSpreadValueAsk(row, col, calcval, value, operation):
    qs.change_driver_value(row, "YTM", value, operation, 'Ask')
    clearQuoteLock(row, 'Ask')

def changeYTMValueAsk(row, col, calcval, value, operation):
    qs.change_driver_value(row, "YTMValue", value, operation, 'Ask')
    clearQuoteLock(row, 'Ask')

def changeGrossBasisAsk(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Gross Basis", value, operation, 'Ask')
    clearQuoteLock(row, 'Ask')

def changeBidPriceSpreadAsk(row, col, calcval, value, operation):
    qs.change_price_spread(row, value, operation)
    clearQuoteLock(row, 'Ask')

def changeBidDriverSpreadAsk(row, col, calcval, value, operation):
    qs.change_driver_spread(row, value, operation)
    clearQuoteLock(row, 'Ask')

def changeOffsetValueAsk(row, col, calcval, value, operation):
    qs.change_offset(row, value, 'Proposed Quote Offset Ask', 'Ask', operation)
    clearQuoteLock(row, 'Ask')

def changeAswSpreadValueMid(row, col, calcval, value, operation):
    qs.change_driver_value(row, qs.get_curve_type(row), value, operation, 'Mid')
    clearQuoteLock(row, 'Ask')
    clearQuoteLock(row, 'Bid')

def changeZSpreadValueMid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Z-Spread", value, operation, 'Mid')
    clearQuoteLock(row, 'Ask')
    clearQuoteLock(row, 'Bid')

def changeQuoteValueMid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Quote", value, operation, 'Mid')
    clearQuoteLock(row, 'Ask')
    clearQuoteLock(row, 'Bid')

def changeYTMSpreadValueMid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "YTM", value, operation, 'Mid')
    clearQuoteLock(row, 'Ask')
    clearQuoteLock(row, 'Bid')

def changeYTMValueMid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "YTMValue", value, operation, 'Mid')
    clearQuoteLock(row, 'Ask')
    clearQuoteLock(row, 'Bid')

def changePriceSpreadValueMid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Price", value, operation, 'Mid')
    clearQuoteLock(row, 'Ask')
    clearQuoteLock(row, 'Bid')

def changeGrossBasisMid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "Gross Basis", value, operation, 'Mid')
    clearQuoteLock(row, 'Ask')
    clearQuoteLock(row, 'Bid')

def changeISpreadValueMid(row, col, calcval, value, operation):
    qs.change_driver_value(row, "I-Spread", value, operation, 'Mid')
    clearQuoteLock(row, 'Ask')
    clearQuoteLock(row, 'Bid')
    
def changeOffsetValueMid(row, col, calcval, value, operation):
    qs.change_offset(row, value, 'Proposed Quote Offset Mid', 'Mid', operation)
    clearQuoteLock(row, 'Ask')
    clearQuoteLock(row, 'Bid')
