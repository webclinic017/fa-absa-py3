
import acm
import FC_UTILS
from FC_CALCULATION_SINGLETON import FC_CALCULATION_SINGLETON
tradeNumber=23267895

#tradeNumber=3177703
#
trade = acm.FTrade[tradeNumber]
'''
#calcSingleton = FC_CALCULATION_SINGLETON()
for leg in trade.Instrument().Legs():
    print leg.Oid()
    (calcResults, calcErrors) = FC_CALCULATION_SINGLETON.Instance().calcWorksheetColumnValues('FC_TRADE_LEG',leg)
    print calcResults
    print calcErrors
'''
calcSpace = FC_CALCULATION_SINGLETON.Instance().worksheetCalcSpaces['FC_TRADE_SCALAR']
#col = FC_CALCULATION_SINGLETON.Instance().worksheetColumns['FC_TRADE_STATIC']['createDateTime']
#value = FC_CALCULATION_SINGLETON.Instance().calcColumnValue(calcSpace,trade, col)
#print value
cols = FC_CALCULATION_SINGLETON.Instance().worksheetColumns['FC_TRADE_SCALAR']
for col in cols:
   print col, FC_CALCULATION_SINGLETON.Instance().calcColumnValue(calcSpace, trade, cols[col])

#if col.Formatter().IsKindOf('FDateTimeFormatter'):
#    print FC_UTILS.formatDate(value)
