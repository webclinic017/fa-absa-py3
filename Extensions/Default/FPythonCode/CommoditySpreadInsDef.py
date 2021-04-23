
import acm

def InitCustomInstrument(ins):
    ins.PayType('Future')
    ins.SpotBankingDaysOffset(0)
    ins.PayOffsetMethod('Business Days')
    ins.SettlementType('Cash')
    
def StartCommoditySpread(eii):
    acm.StartApplication('Instrument Definition', acm.FSymbol("Commodity Spread"))
