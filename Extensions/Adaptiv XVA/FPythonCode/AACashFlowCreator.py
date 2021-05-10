""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACashFlowCreator.py"
import AAUtilFunctions as Util
import AAComposer

def createFixedAmountCashFlowDictionary(staticLegInformation, cashFlowInformation, tradeQuantityDV):
    cashFlowDictionary                          = AAComposer.CashFlowDataDictionary()
    cashFlowDictionary["Fixed_Amount"]          = str(cashFlowInformation.FixedAmount() * staticLegInformation.ContractSize()* tradeQuantityDV.Number() * staticLegInformation.NominalFactor())
    cashFlowDictionary["Payment_Date"]          = Util.createDateString(cashFlowInformation.PayDate())
    return cashFlowDictionary
        
def createFixedRateCashFlowDictionary(paymentDate, notional, accrualStartDate, accrualEndDate, accrualYearFraction, rate):
    cashFlowDictionary                          = AAComposer.CashFlowDataDictionary()
    cashFlowDictionary["Payment_Date"]          = Util.createDateString(paymentDate)
    cashFlowDictionary["Notional"]              = str(notional)
    cashFlowDictionary["Accrual_Start_Date"]    = Util.createDateString(accrualStartDate)
    cashFlowDictionary["Accrual_End_Date"]      = Util.createDateString(accrualEndDate)
    cashFlowDictionary["Accrual_Year_Fraction"] = str(accrualYearFraction)
    cashFlowDictionary["Rate"]                  = str(rate)
    return cashFlowDictionary

def createIndexLinkedCashFlowDictionary(notional, baseReferenceValue, finalReferenceDate, finalReferenceValue, accrualStartDate, accrualEndDate, accrualYearFraction, rate, margin, isCoupon, paymentDate):
    cashFlowDictionary                          = AAComposer.CashFlowDataDictionary()
    cashFlowDictionary["Notional"]              = str(notional)
    cashFlowDictionary["Base_Reference_Value"]   = str(baseReferenceValue)
    cashFlowDictionary["Final_Reference_Date"]  = Util.createDateString(finalReferenceDate)
    cashFlowDictionary["Final_Reference_Value"] = str(finalReferenceValue)
    if accrualStartDate:
        cashFlowDictionary["Accrual_Start_Date"]    = Util.createDateString(accrualStartDate)
    if accrualEndDate:
        cashFlowDictionary["Accrual_End_Date"]      = Util.createDateString(accrualEndDate)
    cashFlowDictionary["Accrual_Year_Fraction"] = str(accrualYearFraction)
    cashFlowDictionary["Yield"]                 = Util.createPercentageString(rate)
    cashFlowDictionary["Margin"]                = Util.createBasisPointString(margin)
    cashFlowDictionary["Rate_Multiplier"]       = "1.0"
    cashFlowDictionary["Is_Coupon"]             = "Yes" if isCoupon else "No"
    cashFlowDictionary["Payment_Date"]          = Util.createDateString(paymentDate)
    return cashFlowDictionary

def createFloatRateCashFlowDictionary(paymentDate, notional, startDate, endDate, accrualYearFraction, resetList, margin):
    cashFlowDictionary                          = AAComposer.CashFlowDataDictionary()
    cashFlowDictionary["Payment_Date"]          = Util.createDateString(paymentDate)
    cashFlowDictionary["Notional"]              = str(notional)
    cashFlowDictionary["Accrual_Start_Date"]    = Util.createDateString(startDate)
    cashFlowDictionary["Accrual_End_Date"]      = Util.createDateString(endDate)
    cashFlowDictionary["Accrual_Year_Fraction"] = str(accrualYearFraction)
    cashFlowDictionary["Resets"]                = resetList
    cashFlowDictionary["Margin"]                = Util.createBasisPointString(margin)
    return cashFlowDictionary

def createResetList(resetDate, resetStartDate, resetEndDate, rateYearFraction, rateTenor, rateDayCount, rateFrequency, rateFixing, useKnownRate, knownRate):
    singleReset = AAComposer.ResetList() # do we need to do this? it is probably enough to loop over the resets in a function outside?
    singleReset.append(AAComposer.Composable(Util.createDateString(resetDate)))
    singleReset.append(AAComposer.Composable(Util.createDateString(resetStartDate)))
    singleReset.append(AAComposer.Composable(Util.createDateString(resetEndDate)))
    singleReset.append(AAComposer.Composable(str(rateYearFraction)))
    singleReset.append(AAComposer.Composable(Util.createDatePeriodString(rateTenor)))
    singleReset.append(AAComposer.Composable(Util.createDayCountString(rateDayCount)))
    singleReset.append(AAComposer.Composable(Util.createDatePeriodString(rateFrequency)))
    singleReset.append(AAComposer.Composable(str(rateFixing)))
    singleReset.append(AAComposer.Composable(Util.createBoolString(useKnownRate)))
    singleReset.append(AAComposer.Composable(str(knownRate)+"%"))
    return singleReset.compose()
    
def createEquitySwapletCashFlowDictionary(notional, startDate, endDate, paymentDate, knownStartPrice,
 knownEndPrice):
    cashFlowDictionary                          = AAComposer.CashFlowDataDictionary()
    cashFlowDictionary["Payment_Date"]          = Util.createDateString(paymentDate)
    cashFlowDictionary["Amount"]                = notional
    cashFlowDictionary["Start_Date"]            = Util.createDateString(startDate)
    cashFlowDictionary["End_Date"]              = Util.createDateString(endDate)
    cashFlowDictionary["Start_Multiplier"]      = 1
    cashFlowDictionary["End_Multiplier"]        = 1
    cashFlowDictionary["Dividend_Multiplier"]   = 1
    cashFlowDictionary["Known_Start_Price"]     = knownStartPrice
    cashFlowDictionary["Known_End_Price"]       = knownEndPrice
    cashFlowDictionary["Known_Start_FX_Rate"]   = 1
    cashFlowDictionary["Known_End_FX_Rate"]     = 1
    cashFlowDictionary["Quanto_FX_Rate"]        = 1
    return cashFlowDictionary
