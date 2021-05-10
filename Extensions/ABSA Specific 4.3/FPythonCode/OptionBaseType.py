
import acm
import OptionFunctions

def GetBaseType(temp, trdnbr, *rest):
    trade = acm.FTrade[trdnbr]
    ins = trade.Instrument()
    return OptionFunctions.GetExoticOptionBaseType(ins)
