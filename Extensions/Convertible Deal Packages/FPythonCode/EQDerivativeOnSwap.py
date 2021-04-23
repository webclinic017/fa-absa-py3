""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/EQDerivativeOnSwap.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    Equity Derivative On Swap

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import ConvertiblePackageUtils as utils
from ConvertiblePackageBase import ConvertiblePackageBase, Date, Str, Object, Float, AcquirerChoices, PortfolioChoices, Settings
from FAssetManagementUtils import ReinitializeLogger, GetInstruments
import CreateDefaultPackages

@Settings(MultiTradingEnabled=True)
class EquityDerivativeOnSwapDefinition(ConvertiblePackageBase):

    # --------------------------------------------------------------------------
    # Traits
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        ConvertiblePackageBase.__init__(self, *args, **kwds)
        self._customPaneName = 'CustomPanes_EQDerivativeOnSwap' # FExtensionValue
        self.on_trait_change(self.SetOptionB2BPrice, ['price', 'b2bEnabled'])
        ReinitializeLogger(3) # Debug = 2

    # --------------------------------------------------------------------------
    # Overridden methods from DealPackageDefaultDefinition
    # --------------------------------------------------------------------------

    def LeadTrade(self):
        return self.OptionTrade()

    def LeadB2B(self):
        return self.OptionB2B()

    def SetNewInsIfNeeded(self):
        if self.insNew:
            stock = self.insNew
            self.insNew = None
            dp = self.DealPackage()
            CreateDefaultPackages.CreateDefaultEquityDerivativeOnSwapPackage(stock, dp)
            self.SetDefaultAttributes()

    def AssemblePackage(self, stock = None):
        # pylint: disable-msg=W0221    
        if not stock:
            stock = self.AllStockChoices().First()
        self.insNew = stock
        self.SetNewInsIfNeeded()
        super(EquityDerivativeOnSwapDefinition, self).OnNew()

    #Option
    optionName =         Str(  label='Name ',
                                objMapping='Option.Name',
                                toolTip='Option name')

    payDayOffset =      Object( label='Settle Days',
                                objMapping='Option.PayDayOffset',
                                toolTip='Pay day offset')

    strikePrice =      Float( label='Strike Price',
                                objMapping='Option.StrikePrice',
                                toolTip='Strike price')

    optionType =      Object( label='Type',
                                objMapping='Option.OptionType',
                                toolTip='Indicates if the instrument is a call or a put option ',
                                choiceListSource='@ValidOptionTypes')

    exerciseType =      Object( label='Exercise',
                                objMapping='Option.ExerciseType')

    maturityDateTime =    Object(   label='Maturity',
                                objMapping='Option.ExpiryDate',
                                toolTip='Maturity of option',
                                transform='@TransformPeriodToDate')

    settlementType=      Object( label='Settle Type',
                                objMapping='Option.SettlementType',
                                toolTip='Describes how the option settles')

    #Stock
    stock =             Object( label='Name',
                                objMapping='StockTrade.Instrument',
                                toolTip='Stock',
                                choiceListSource='@AllStockChoices',
                                transform='@ValidateInstrument')

    stockValueDay =     Date(  label='Value Day ',
                                objMapping='StockTrade.ValueDay',
                                transform='@TransformPeriodToDate' )

    b2bAcq =            Object( label='B2B Acquirer',
                                objMapping='OptionB2B.TraderAcquirer|StockB2B.TraderAcquirer',
                                choiceListSource=AcquirerChoices() )

    b2bEnabled =        Object( objMapping='OptionB2B.SalesCoverEnabled|StockB2B.SalesCoverEnabled',
                                label='B2B' )

    b2bPrf =            Object( label='B2B Portfolio',
                                objMapping='OptionB2B.TraderPortfolio|StockB2B.TraderPortfolio',
                                choiceListSource=PortfolioChoices() )
                                
    def _payDayOffset_changed(self, attribute, oldValue, newValue, *args):
        """ Override: Necessary to inactivate default-behaviour in parent class """
        pass
    
    def _tradeTime_changed(self, attribute, oldValue, newValue, *args):
        super(EquityDerivativeOnSwapDefinition, self)._tradeTime_changed(attribute, oldValue, newValue)
        self.stockValueDay = self.StockTrade().ValueDay()

    def _nominal_changed(self, attribute, oldValue, newValue, *args):
        option = self.Option()
        stockTrade = self.StockTrade()
        isCall = 1
        if not option.IsCallOption():
            isCall = -1
        nominal = -isCall * self.LeadTrade().Nominal()
        stockTrade.Nominal(nominal)
        self.SetPremium()

    def SetDefaultAttributes(self):
        self.SetDefaultOptionAttributes()
        self.SetDefaultTradeAttributes()

    def ValidateInstrument(self, traitName, value, *args):
        if not value:
            value = self.stock
        return value

def StartEquityDerivativeOnSwapApplication(eii):
    instruments=GetInstruments(eii)
    insPackage = None
    stock = None
    name = 'EquityDerivativeOnSwap'
    if hasattr(instruments, 'First') and instruments.First().IsKindOf(acm.FConvertible):
        stock = instruments.First().Underlying()
        insPackage=utils.InstrumentPackageIfUnique(stock, name) 
    elif hasattr(instruments, 'First') and instruments.First().IsKindOf(acm.FStock):
        stock = instruments.First()
        insPackage=utils.InstrumentPackageIfUnique(stock, name) 
    if insPackage is None:
        dp = acm.DealPackage.New(name, stock)
    else:
        dp = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(insPackage)
    utils.StartDealPackage(dp)