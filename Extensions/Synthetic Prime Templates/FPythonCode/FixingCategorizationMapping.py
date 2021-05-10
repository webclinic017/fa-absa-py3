
import FixingCategorizationMappingBase

def FixingCategorization(resetType, legCategory):
    extensionValue = "None"
    if legCategory.Name() == "Financing":
        if resetType == "Spread":
            extensionValue = "customFinancingSpreadHook"
    if legCategory.Name() == "Stock Borrow":
        if resetType == "Spread":
            extensionValue = "customStockBorrowSpreadHook"
            
    if extensionValue == "None":
        extensionValue = FixingCategorizationMappingBase.SyntheticPrimeFixingCategorization(resetType, legCategory)
    return extensionValue
