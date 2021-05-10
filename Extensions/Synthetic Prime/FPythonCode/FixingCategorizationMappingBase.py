
def SyntheticPrimeFixingCategorization(resetType, legCategory):
    extensionValue = "None"
    if legCategory.Name() == "Financing":
        if resetType == "Nominal Scaling":
            extensionValue = "customFinancingNominalScaling"
    if legCategory.Name() == "Performance":
        if resetType == "Return":
            extensionValue = "customPerformanceReturn"
    if legCategory.Name() == "Performance UPL":
        if resetType == "Return":
            extensionValue = "customPerformanceReturnUPL"
    if legCategory.Name() == "Performance RPL":
        if resetType == "Return":
            extensionValue = "customPerformanceReturnRPL"
    if legCategory.Name() == "Dividend":
        if resetType == "Nominal Scaling":
            extensionValue = "customDividendNominalScaling"
        if resetType == "Dividend Scaling":
            extensionValue = "customDividendScaling"
    if legCategory.Name() == "Stock Borrow":
        if resetType == "Nominal Scaling":
            extensionValue = "customStockBorrowNominalScaling"
    return extensionValue
