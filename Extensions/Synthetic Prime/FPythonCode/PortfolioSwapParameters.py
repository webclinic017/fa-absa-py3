
"""----------------------------------------------------------------------------
MODULE
    
    PortfolioSwapParameters

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

----------------------------------------------------------------------------"""
import acm
import PortfolioSwapMetaLegs
class DealPackageParameters:

    dealpackage = None
    
    def __init__(self, dealpackage):
        self.dealpackage = dealpackage
    
    def DealPackage(self):
        return self.dealpackage
        
    def PortfolioSwap(self):
        return self.DealPackage().InstrumentAt('PrfSwap').Instrument()
        
    def FundPortfolio(self):
        return self.PortfolioSwap().FundPortfolio()
    
    def FilteredPortfolio(self):
        return self.DealPackage().GetAttribute('filteredPortfolio')
        
    def AccountingParameters(self):
        return self.FundPortfolio().MappedAccountingParametersLink().Link()

    def PortfolioSwapTrade(self):
        return self.DealPackage().TradeAt('PrfSwap').Trade()
        
    def PayCalendar(self):
        return self.DealPackage().GetAttribute('payCalendar')

#----- Meta Legs -----------------------------------------------------------------------          
    def FinancingMetaLeg(self, *args):
        return self.DealPackage().GetAttribute('financingMetaLeg')()
    
    def PerformanceMetaLeg(self, *args):
        return self.DealPackage().GetAttribute('performanceMetaLeg')()
    
    def PerformanceRPLMetaLeg(self, *args):
        return self.DealPackage().GetAttribute('rplPerformanceMetaLeg')()
    
    def PerformanceUPLMetaLeg(self, *args):
        return self.DealPackage().GetAttribute('uplPerformanceMetaLeg')()
    
    def StockBorrowMetaLeg(self, *args):
        return self.DealPackage().GetAttribute('stockBorrowMetaLeg')()
    
    def SyntheticCashMetaLeg(self, *args):
        return self.DealPackage().GetAttribute('syntheticCashMetaLeg')()
        
    def FeeMetaLeg(self, *args):
        return self.DealPackage().GetAttribute('feeMetaLeg')()
    
    def NoPerformanceSplitEnabled(self):
        return self.DealPackage().GetAttribute('enableNoPerformanceSplit')
        
#----- Utility Functions ---------------------------------------------------------------        
    def GetClientSpreadInstrument(self):
        return self.DealPackage().GetAttribute("clientSpreadInstr")()
        
    def GetFeeLeg(self, security):
        if isinstance(security, type(str())):
            security = acm.FInstrument[security]
        return self.DealPackage().GetAttribute('legPerSecAndType')(security, self.FeeMetaLeg().CategoryChlItem())
    
    def GetDividendLeg(self, security):
        if isinstance(security, type(str())):
            security = acm.FInstrument[security]
        return self.DealPackage().GetAttribute('legPerSecAndType')(security, PortfolioSwapMetaLegs.LEG_CATEGORY_DIVIDEND)
        
    def GetSyntheticCashLeg(self):
        return self.DealPackage().GetAttribute('legPerSecAndType')(None, self.SyntheticCashMetaLeg().CategoryChlItem())
        
    def GetSingleFinancingLeg(self):
        return self.DealPackage().GetAttribute('legPerSecAndType')(None, self.FinancingMetaLeg().CategoryChlItem())

    def GetLegPerSecurity(self, security, categoryChlItem):
        if isinstance(security, type(str())):
            security = acm.FInstrument[security]
        return self.DealPackage().GetAttribute('legPerSecAndType')(security, categoryChlItem)

    def GetPerformanceRPLLeg(self, security):
        return self.GetLegPerSecurity(security, self.PerformanceRPLMetaLeg().CategoryChlItem())

    def GetPerformanceUPLLeg(self, security):
        return self.GetLegPerSecurity(security, self.PerformanceUPLMetaLeg().CategoryChlItem())
    
    def GetPerformanceLeg(self, security):
        return self.GetLegPerSecurity(security, self.PerformanceMetaLeg().CategoryChlItem())
        
    def GetFinancingLeg(self, security):
        return self.GetLegPerSecurity(security, self.FinancingMetaLeg().CategoryChlItem())
        
    def GetStockBorrowLeg(self, security):
        return self.GetLegPerSecurity(security, self.StockBorrowMetaLeg().CategoryChlItem())
        
    def StockBorrowEnabled(self):
        return self.DealPackage().GetAttribute('stockBorrowEnabled')
        
    def CashEnabled(self):
        return self.DealPackage().GetAttribute('cashEnabled')
    
