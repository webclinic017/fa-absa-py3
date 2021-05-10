""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAEquitySwapDeal.py"
import AAUtilFunctions as Util
import AAComposer
import AADealsCreator
import AAParameterDictionary
import AACfInstrumentDeal
import acm
import AAComposer

cs = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext (), 'FMoneyFlowSheet')

class TRSCashFlowListEngine(AACfInstrumentDeal.CashFlowListEngine):
    def __init__(self, static_leg_info, value_date):
        self.leg = static_leg_info.AcmLeg()
        self.leg_info = self.leg.LegInformation(value_date)
        self.static_leg_info = static_leg_info
        self.value_date = value_date
        
    def CalculateNotional(self, cashFlowListDeal, cfInformation, contractSize):
        nominalFactor = cfInformation.Nominal(self.leg_info).Number()
        if str(nominalFactor).lower() == 'nan':
            cashFlow = acm.FCashFlow[cfInformation.CashFlowNbr()]
            topnode = cs.InsertItem(cashFlow)
            calc = cs.CreateCalculation(topnode, 'Cash Analysis Nominal')
            nominalFactor = calc.Value().Number()
            
        return abs(nominalFactor * AACfInstrumentDeal.CashFlowListEngine.CalculateNotional(self, cashFlowListDeal, cfInformation, contractSize))

TOTAL_RETURN_LEG_TYPE = 'Total Return'

class AAEquitySwapDeal(object):    
    def __init__(self, trSwap, portfolioTradeQuantities, staticLegInformations, valuationDate, cfInformation):
        self.trSwap = trSwap
        self.portfolioTradeQuantities = portfolioTradeQuantities
        self.staticLegInformations = staticLegInformations
        self.valuationDate = valuationDate
        self.cfInformation = cfInformation
        
    def get(self):
        parameterDict = AAParameterDictionary.ParameterDictionary()
        deals = acm.FArray()
        staticLegInformationCashFlowEngineDict = {}
        for staticLegInformation in self.staticLegInformations:
            trsCashFlowEngine = TRSCashFlowListEngine(staticLegInformation, self.valuationDate)
            if staticLegInformation.LegType() == TOTAL_RETURN_LEG_TYPE:
                for tradeQuantity in self.portfolioTradeQuantities:
                    trsDeal = AACfInstrumentDeal.EquitySwapletListDeal(tradeQuantity, staticLegInformation, 
                        self.valuationDate, self.cfInformation, parameterDict, trsCashFlowEngine, None)
                    trsDeal.AppendToDealsArray(deals)
            else:
                staticLegInformationCashFlowEngineDict[staticLegInformation] = trsCashFlowEngine
                AADealsCreator.createLegCashFlowInstrumentDealString(deals, parameterDict, self.portfolioTradeQuantities,
                    staticLegInformation, self.valuationDate, self.cfInformation, staticLegInformationCashFlowEngineDict=staticLegInformationCashFlowEngineDict )
            
        return AAParameterDictionary.createReturnDictionary(deals, parameterDict)
