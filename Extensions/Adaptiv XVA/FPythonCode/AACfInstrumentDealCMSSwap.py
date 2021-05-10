""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AACfInstrumentDealCMSSwap.py"
import AAUtilFunctions as Util
import AAComposer
import AADealsCreator
import AAParameterDictionary
import AACfInstrumentDeal
import AACfInstrumentDealCapFloor
import acm


class AACMSSwapDeal(object):
    def __init__(self, cmsSwap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
        self.cmsSwap = cmsSwap
        self.portfolioTradeQuantities = portfolioTradeQuantities
        self.staticLegInformations = staticLegInformations
        self.valuationDate = valuationDate
        self.cfInformation = cfInformation

    def createCMSLegDealString(self, deals, parameterDict, staticLegInformation):
        cashFlowEngine = AACfInstrumentDeal.CashFlowListEngine()
        capfloorCflEngine = AACfInstrumentDealCapFloor.CashFlowListEngineCapFloor()
        contract_size = None
        for tradeQuantity in self.portfolioTradeQuantities:
            if staticLegInformation.LegType() == "Float":
                floatDeal = AACfInstrumentDeal.CMSFloatInterestDeal(tradeQuantity, staticLegInformation, 
                    self.valuationDate, self.cfInformation, parameterDict, cashFlowEngine, contract_size)
                floatDeal.AppendToDealsArray(deals)
            elif staticLegInformation.LegType() == "Capped Float":
                capDeal = AACfInstrumentDeal.CMSCapInterestDeal(tradeQuantity, staticLegInformation, self.valuationDate, 
                             self.cfInformation, parameterDict, capfloorCflEngine, contract_size)
                capDeal.AppendToDealsArray(deals)
                
                floatDeal = AACfInstrumentDeal.CMSFloatInterestDeal(tradeQuantity, staticLegInformation, 
                    self.valuationDate, self.cfInformation, parameterDict, cashFlowEngine, contract_size)
                floatDeal.AppendToDealsArray(deals)
                
            elif staticLegInformation.LegType() == "Floored Float":
                floorDeal = AACfInstrumentDeal.CMSFloorInterestDeal(tradeQuantity, staticLegInformation, self.valuationDate,
                               self.cfInformation, parameterDict, capfloorCflEngine, contract_size)
                floorDeal.AppendToDealsArray(deals)
                floatDeal = AACfInstrumentDeal.CMSFloatInterestDeal(tradeQuantity, staticLegInformation, 
                    self.valuationDate, self.cfInformation, parameterDict, cashFlowEngine, contract_size)
                floatDeal.AppendToDealsArray(deals)
                
            elif staticLegInformation.LegType() == "Collared Float":
                capDeal = AACfInstrumentDeal.CMSCapInterestDeal(tradeQuantity, staticLegInformation, self.valuationDate, 
                             self.cfInformation, parameterDict, capfloorCflEngine, contract_size)
                capDeal.AppendToDealsArray(deals)
                
                floorDeal = AACfInstrumentDeal.CMSFloorInterestDeal(tradeQuantity, staticLegInformation, self.valuationDate,
                               self.cfInformation, parameterDict, capfloorCflEngine, contract_size)
                floorDeal.AppendToDealsArray(deals)
                
                floatDeal = AACfInstrumentDeal.CMSFloatInterestDeal(tradeQuantity, staticLegInformation, 
                    self.valuationDate, self.cfInformation, parameterDict, cashFlowEngine, contract_size)
                floatDeal.AppendToDealsArray(deals)
            
        return
        
    def get(self):
        deals = acm.FArray()
        parameterDict = AAParameterDictionary.ParameterDictionary()
        for staticLegInformation in self.staticLegInformations:
            leg = staticLegInformation.AcmLeg()
            if leg.FloatRateReference() and leg.FloatRateReference().IsKindOf("FSwap"):
                self.createCMSLegDealString(deals, parameterDict, staticLegInformation)
            else:
                AADealsCreator.createLegCashFlowInstrumentDealString(deals, parameterDict, self.portfolioTradeQuantities,
                    staticLegInformation, self.valuationDate, self.cfInformation)
            
        returnDictionary = AAParameterDictionary.createReturnDictionary(deals, parameterDict)
        return AAParameterDictionary.createReturnDictionary(deals, parameterDict)
