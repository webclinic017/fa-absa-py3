
import acm   
    
def GetGenericSwapChoices(instrument):
    genericSwaps = acm.FInstrument.Select("insType='Swap' and generic=True")
    result = acm.FArray()
    for swap in genericSwaps:
        if swap.SwapType() == "Fixed/Float":
            result.Add(swap)

    result = result.SortByProperty("Name")
    return result
    
def GetSwaptionUnderlying(option):
    return option.Underlying()
    
def SetSwaptionUnderlying(option, swap):
    return option.Underlying(swap)
    
def UpdateDefaultInstrument(ins):
    underlying = ins.Underlying()
    
    if underlying and underlying.InsType() != "Swap":
        # No swaption default instrument created yet. Set underlying to first generic swap in the option currency.
        query = "insType='Swap' and generic=True and currency='" + ins.Currency().Name() + "'"
        swaps = acm.FInstrument.Select(query)
        ins.Underlying = swaps.First()
        ins.Quotation = "Pct of Nominal"
