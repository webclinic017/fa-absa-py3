""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACfInstrumentDealCCSwap.py"
import AAUtilFunctions as Util
import AAComposer
import AADealsCreator
import AAParameterDictionary
import AACfInstrumentDeal
import AAParamsAndSettingsHelper
import acm
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

class CashFlowListEngineCurrencySwapFxScalingLeg(AACfInstrumentDeal.CashFlowListEngine):
    def AddCashFlowIfValid(self, cashFlowListDeal, cfInformation):
        if cfInformation.Type() == cashFlowListDeal.interestCashFlowType:
            if acm.AAIntegration.IsValidFutureCashFlow(cfInformation, cashFlowListDeal.valuationDate, cashFlowListDeal.tradeQuantityDV.DateTime()):
                cashFlowListDeal.AddInterestCashFlow(cfInformation)
        elif cfInformation.Type() == "Fixed Amount":
            # Fixed amounts are created implicitly by the Principal_Exchange flag on the MtM swap (i.e. instrument level). 
            pass
    
    def CalculateNotional(self, cashFlowListDeal, cfInformation, contractSize):
        return contractSize* cashFlowListDeal.tradeQuantityDV.Number()
    
    def AppendInterestCashFlow(self, interestCashFlowList, cashFlowDictionary, cfInformation, valuationDate):
        cashFlowDictionary['FX_Reset_Date'] = Util.createDateString(cfInformation.NominalScalingStartDays()[0])
        if cfInformation.NominalScalingsAreFixed(valuationDate):
            cashFlowDictionary['Known_FX_Rate'] = str(cfInformation.NominalScalingValues()[0])
        else:
            cashFlowDictionary['Known_FX_Rate'] = 0
        interestCashFlowList.append(cashFlowDictionary)

class CashFlowListEngineCurrencySwapLockedLeg(AACfInstrumentDeal.CashFlowListEngine):
    def AddCashFlowIfValid(self, cashFlowListDeal, cfInformation):
        if cfInformation.Type() == cashFlowListDeal.interestCashFlowType:
            if acm.AAIntegration.IsValidFutureCashFlow(cfInformation, cashFlowListDeal.valuationDate, cashFlowListDeal.tradeQuantityDV.DateTime()):
                cashFlowListDeal.AddInterestCashFlow(cfInformation)
        elif cfInformation.Type() == "Fixed Amount":
            # Fixed amounts are created implicitly by the Principal_Exchange flag on the MtM swap (i.e. instrument level). 
            pass

class AAMtMCrossCurrencySwapDeal(object):
    def __init__(self, currencySwap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
        self.currencySwap = currencySwap
        self.portfolioTradeQuantities = portfolioTradeQuantities
        self.staticLegInformations = staticLegInformations
        self.valuationDate = valuationDate
        self.cfInformation = cfInformation

    def getAAMtMCrossCurrencySwapDealString(self, parameterDict):
        deal = AAComposer.PairList()
        deal["Object"] = "MtMCrossCurrencySwapDeal"
        deal["Reference"] = Util.createAALabel(self.currencySwap.Name())
        deal["Effective_Date"] = Util.createDateString(self.currencySwap.StartDate())
        deal["Maturity_Date"] = Util.createDateString(self.currencySwap.EndDate())
        payLeg = self.currencySwap.PayLeg()
        recLeg = self.currencySwap.RecLeg()
        
        currencySymbol = payLeg.Currency().AsSymbol()
        deal["Pay_Currency"] = currencySymbol
        deal["Pay_Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(payLeg.MappedDiscountLink())
        if payLeg.IsFloatLeg():
            deal["Pay_Interest_Rate"] = parameterDict.AddForwardCurveAndGetName(payLeg.MappedForwardLink())
        
        currencySymbol = recLeg.Currency().AsSymbol()
        deal["Receive_Currency"] = currencySymbol
        deal["Receive_Discount_Rate"] = parameterDict.AddDiscountCurveAndGetName(recLeg.MappedDiscountLink())
        if recLeg.IsFloatLeg():
            deal["Receive_Interest_Rate"] = parameterDict.AddForwardCurveAndGetName(recLeg.MappedForwardLink())
        
        # We assume here that payLeg.NominalAtStart() != recLeg.NominalAtStart() and payLeg.NominalAtEnd() != recLeg.NominalAtEnd() are not possible
        deal["Principal_Exchange"] = Util.getPrincipalExchangeStr(payLeg)
        
        deal["Pay_Rate_Type"] = Util.getLegType(payLeg.LegType())
        deal["Receive_Rate_Type"] = Util.getLegType(recLeg.LegType())
        
        if payLeg.NominalScaling() == "FX":
            deal["MtM_Side"] = "Pay"
        elif recLeg.NominalScaling() == "FX":
            deal["MtM_Side"] = "Receive"
        else:
            logger.LOG("Unknown nominal scaling type")
        return deal.compose()
      
    def get(self):
        if AAMtMCrossCurrencySwapDeal.hasFXNominalScaling(self.currencySwap):
            staticLegInformationCashFlowEngineDict = {}
            for staticLegInformation in self.staticLegInformations:
                if staticLegInformation.NominalScaleType() == "FX":
                    staticLegInformationCashFlowEngineDict[staticLegInformation] = CashFlowListEngineCurrencySwapFxScalingLeg()
                else:
                    staticLegInformationCashFlowEngineDict[staticLegInformation] = CashFlowListEngineCurrencySwapLockedLeg()
            (deals, parameterDict) = AADealsCreator.createAnyCashFlowInstrumentDealString(self.portfolioTradeQuantities, self.staticLegInformations, self.valuationDate, self.cfInformation, staticLegInformationCashFlowEngineDict = staticLegInformationCashFlowEngineDict) 
            dealsXML = ''
            for deal in deals:
                dealsXML += '<Deal>' + deal + '</Deal>'
            wholeDealString = "<Properties>" + self.getAAMtMCrossCurrencySwapDealString(parameterDict) + "</Properties><Deals>" + dealsXML + "</Deals>"
            returnDictionary = AAParameterDictionary.createReturnDictionary([wholeDealString], parameterDict)
            return returnDictionary
        else:
            (deals, parameterDict) = AADealsCreator.createAnyCashFlowInstrumentDealString(self.portfolioTradeQuantities, self.staticLegInformations, self.valuationDate, self.cfInformation)
            return AAParameterDictionary.createReturnDictionary(deals, parameterDict)

    @staticmethod
    def hasFXNominalScaling(currencySwap):
        payLeg = currencySwap.PayLeg()
        recLeg = currencySwap.RecLeg()
        return (payLeg.NominalScaling() == "FX" or recLeg.NominalScaling() == "FX")
