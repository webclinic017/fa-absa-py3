
import acm
import FFiQuoteSheetHelpFunctions as qs


def isRemove(operation):
    return str(operation) == 'remove'
    
##############################################################################
# Quantity
##############################################################################
def GetBidQuantity(self, level):
    propLevel = self.Level(level)
    if propLevel:
        return propLevel.BidQuantity()
    return 0.0
        
def GetAskQuantity(self, level):
    propLevel = self.Level(level)
    if propLevel:
        return propLevel.AskQuantity()
    return 0.0
    
def GetBidQuantity0(self):
    return GetBidQuantity(self, 0)
    
def GetBidQuantity1(self):
    return GetBidQuantity(self, 1)

def GetBidQuantity2(self):
    return GetBidQuantity(self, 2)

def GetBidQuantity3(self):
    return GetBidQuantity(self, 3)

def GetBidQuantity4(self):
    return GetBidQuantity(self, 4)

def GetAskQuantity0(self):
    return GetAskQuantity(self, 0)

def GetAskQuantity1(self):
    return GetAskQuantity(self, 1)

def GetAskQuantity2(self):
    return GetAskQuantity(self, 2)

def GetAskQuantity3(self):
    return GetAskQuantity(self, 3)

def GetAskQuantity4(self):
    return GetAskQuantity(self, 4)
    
def SetBidQuantity(self, level, qty):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.BidQuantity(qty)

def ClearBidQuantity(self, level):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.ClearBidQuantity()
        
def SetAskQuantity(self, level, qty):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.AskQuantity(qty)

def ClearAskQuantity(self, level):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.ClearAskQuantity()

def SetBidQuantity0(self, quantity):
    SetBidQuantity(self, 0, quantity)
    
def SetBidQuantity1(self, quantity):
    SetBidQuantity(self, 1, quantity)

def SetBidQuantity2(self, quantity):
    SetBidQuantity(self, 2, quantity)

def SetBidQuantity3(self, quantity):
    SetBidQuantity(self, 3, quantity)

def SetBidQuantity4(self, quantity):
    SetBidQuantity(self, 4, quantity)

def SetAskQuantity0(self, quantity):
    SetAskQuantity(self, 0, quantity)
    
def SetAskQuantity1(self, quantity):
    SetAskQuantity(self, 1, quantity)

def SetAskQuantity2(self, quantity):
    SetAskQuantity(self, 2, quantity)

def SetAskQuantity3(self, quantity):
    SetAskQuantity(self, 3, quantity)

def SetAskQuantity4(self, quantity):
    SetAskQuantity(self, 4, quantity)




def postBidQuantityLevel1(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidQuantity(row.QuoteController().ProposedQuotePackage(), 0)

def postBidQuantityLevel2(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidQuantity(row.QuoteController().ProposedQuotePackage(), 1)

def postBidQuantityLevel3(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidQuantity(row.QuoteController().ProposedQuotePackage(), 2)

def postBidQuantityLevel4(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidQuantity(row.QuoteController().ProposedQuotePackage(), 3)

def postBidQuantityLevel5(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidQuantity(row.QuoteController().ProposedQuotePackage(), 4)

def postAskQuantityLevel1(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskQuantity(row.QuoteController().ProposedQuotePackage(), 0)

def postAskQuantityLevel2(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskQuantity(row.QuoteController().ProposedQuotePackage(), 1)

def postAskQuantityLevel3(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskQuantity(row.QuoteController().ProposedQuotePackage(), 2)

def postAskQuantityLevel4(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskQuantity(row.QuoteController().ProposedQuotePackage(), 3)

def postAskQuantityLevel5(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskQuantity(row.QuoteController().ProposedQuotePackage(), 4)

##############################################################################
# Fixed Income
##############################################################################

def postProposedPriceAsk(row, col, cell, val, operation):
    postProposedPrice(row, val, operation, "Ask")

def postProposedPriceBid(row, col, cell, val, operation):
    postProposedPrice(row, val, operation, "Bid")

def postProposedPrice(row, val, operation, side):
    if UseFIQuoting(row):
        specifier = PriceSpecifier(row)
        if specifier == "Price":
            qs.change_driver_value(row, "Quote", val, operation, side)
        elif specifier == "Yield":
            qs.change_driver_value(row, "YTMValue", val/100, operation, side)
        elif specifier == "Spread":
            qs.change_driver_value(row, "YTM", val/10000, operation, side)
        else:
            qs.change_driver_value(row, "Quote", val, operation, side)    

def UseFIQuoting(row):
    data_source = row.QuoteController().CreateDataSource('Use Fixed Income Quoting')
    if data_source:
        return data_source.Get()
    return None

def PriceSpecifier(row):
    data_source = row.QuoteController().CreateDataSource('Proposed Quote Price Specifier')
    if data_source:
        return data_source.Get()
    return None

##############################################################################
# Tick offsets
##############################################################################
def GetBidTickOffsetForLevel(self, level):
    propLevel = self.Level(level)
    if propLevel:
        return propLevel.BidTickOffset()
    return 0

def GetAskTickOffsetForLevel(self, level):
    propLevel = self.Level(level)
    if propLevel:
        return propLevel.AskTickOffset()
    return 0
    
def SetBidTickOffsetForLevel(self, level, tickOffset):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.BidTickOffset(tickOffset)
        
def SetAskTickOffsetForLevel(self, level, tickOffset):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.AskTickOffset(tickOffset)

def ClearBidTickOffsetForLevel(self, level):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.ClearBidTickOffset()

def ClearAskTickOffsetForLevel(self, level):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.ClearAskTickOffset()
        
# Level 1
def GetAskTickOffsetLevel1(self):
    return GetAskTickOffsetForLevel(self, 0)

def GetBidTickOffsetLevel1(self):
    return GetBidTickOffsetForLevel(self, 0)  
    
def SetAskTickOffsetLevel1(self, tickOffset):
    SetAskTickOffsetForLevel(self, 0, tickOffset)
    
def SetBidTickOffsetLevel1(self, tickOffset):
    SetBidTickOffsetForLevel(self, 0, tickOffset)

def postAskTickOffsetLevel1(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 0)

def postBidTickOffsetLevel1(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 0)

# Level 2
def GetAskTickOffsetLevel2(self):
    return GetAskTickOffsetForLevel(self, 1)

def GetBidTickOffsetLevel2(self):
    return GetBidTickOffsetForLevel(self, 1)  
    
def SetAskTickOffsetLevel2(self, tickOffset):
    SetAskTickOffsetForLevel(self, 1, tickOffset)
    
def SetBidTickOffsetLevel2(self, tickOffset):
    SetBidTickOffsetForLevel(self, 1, tickOffset)

def postAskTickOffsetLevel2(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 1)

def postBidTickOffsetLevel2(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 1)

# Level 3
def GetAskTickOffsetLevel3(self):
    return GetAskTickOffsetForLevel(self, 2)

def GetBidTickOffsetLevel3(self):
    return GetBidTickOffsetForLevel(self, 2)  
    
def SetAskTickOffsetLevel3(self, tickOffset):
    SetAskTickOffsetForLevel(self, 2, tickOffset)
    
def SetBidTickOffsetLevel3(self, tickOffset):
    SetBidTickOffsetForLevel(self, 2, tickOffset)
   
def postAskTickOffsetLevel3(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 2)

def postBidTickOffsetLevel3(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 2)
 
 # Level 4
def GetAskTickOffsetLevel4(self):
    return GetAskTickOffsetForLevel(self, 3)

def GetBidTickOffsetLevel4(self):
    return GetBidTickOffsetForLevel(self, 3)  
    
def SetAskTickOffsetLevel4(self, tickOffset):
    SetAskTickOffsetForLevel(self, 3, tickOffset)
    
def SetBidTickOffsetLevel4(self, tickOffset):
    SetBidTickOffsetForLevel(self, 3, tickOffset)
  
def postAskTickOffsetLevel4(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 3)

def postBidTickOffsetLevel4(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 3)
  
 # Level 5
def GetAskTickOffsetLevel5(self):
    return GetAskTickOffsetForLevel(self, 4)

def GetBidTickOffsetLevel5(self):
    return GetBidTickOffsetForLevel(self, 4)  
    
def SetAskTickOffsetLevel5(self, tickOffset):
    SetAskTickOffsetForLevel(self, 4, tickOffset)
    
def SetBidTickOffsetLevel5(self, tickOffset):
    SetBidTickOffsetForLevel(self, 4, tickOffset)

def postAskTickOffsetLevel5(row, col, cell, val, operation):
    if isRemove(operation):
        ClearAskTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 4)

def postBidTickOffsetLevel5(row, col, cell, val, operation):
    if isRemove(operation):
        ClearBidTickOffsetForLevel(row.QuoteController().ProposedQuotePackage(), 4)

##############################################################################
# Price Slacks
##############################################################################
def GetPriceSlackForLevel(self, level):
    propLevel = self.Level(level)
    if propLevel:
        return propLevel.Slack()
    return 0

def GetPriceSlackTypeForLevel(self, level):
    propLevel = self.Level(level)
    if propLevel:
        return propLevel.SlackType()
    return 0

def SetPriceSlackForLevel(self, level, priceSlack):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.Slack(priceSlack)

def SetPriceSlackTypeForLevel(self, level, priceSlackType):
    propLevel = self.Level(level)
    if propLevel:
        propLevel.SlackType(priceSlackType)

# Level 1
def GetPriceSlackLevel1(self):
    return GetPriceSlackForLevel(self, 0)

def GetPriceSlackTypeLevel1(self):
    return GetPriceSlackTypeForLevel(self, 0)

def SetPriceSlackLevel1(self, priceSlack):
    SetPriceSlackForLevel(self, 0, priceSlack)

def SetPriceSlackTypeLevel1(self, priceSlackType):
    SetPriceSlackTypeForLevel(self, 0, priceSlackType)

# Level 2
def GetPriceSlackLevel2(self):
    return GetPriceSlackForLevel(self, 1)

def GetPriceSlackTypeLevel2(self):
    return GetPriceSlackTypeForLevel(self, 1)

def SetPriceSlackLevel2(self, priceSlack):
    SetPriceSlackForLevel(self, 1, priceSlack)

def SetPriceSlackTypeLevel2(self, priceSlackType):
    SetPriceSlackTypeForLevel(self, 1, priceSlackType)

# Level 3
def GetPriceSlackLevel3(self):
    return GetPriceSlackForLevel(self, 2)

def GetPriceSlackTypeLevel3(self):
    return GetPriceSlackTypeForLevel(self, 2)

def SetPriceSlackLevel3(self, priceSlack):
    SetPriceSlackForLevel(self, 2, priceSlack)

def SetPriceSlackTypeLevel3(self, priceSlackType):
    SetPriceSlackTypeForLevel(self, 2, priceSlackType)

# Level 4
def GetPriceSlackLevel4(self):
    return GetPriceSlackForLevel(self, 3)

def GetPriceSlackTypeLevel4(self):
    return GetPriceSlackTypeForLevel(self, 3)

def SetPriceSlackLevel4(self, priceSlack):
    SetPriceSlackForLevel(self, 3, priceSlack)

def SetPriceSlackTypeLevel4(self, priceSlackType):
    SetPriceSlackTypeForLevel(self, 3, priceSlackType)

# Level 5
def GetPriceSlackLevel5(self):
    return GetPriceSlackForLevel(self, 4)

def GetPriceSlackTypeLevel5(self):
    return GetPriceSlackTypeForLevel(self, 4)

def SetPriceSlackLevel5(self, priceSlack):
    SetPriceSlackForLevel(self, 4, priceSlack)

def SetPriceSlackTypeLevel5(self, priceSlackType):
    SetPriceSlackTypeForLevel(self, 4, priceSlackType)
