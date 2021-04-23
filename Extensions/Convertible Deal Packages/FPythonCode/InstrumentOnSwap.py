""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/InstrumentOnSwap.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    Instrument On Swap

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
from ConvertiblePackageBase import ConvertiblePackageBase, Date, Str, Object, Float, AcquirerChoices, PortfolioChoices, Settings
import ConvertiblePackageUtils as utils
from FAssetManagementUtils import ReinitializeLogger, GetInstruments
import CreateDefaultPackages

@Settings(MultiTradingEnabled=True)
class InstrumentOnSwapDefinition(ConvertiblePackageBase):

    # --------------------------------------------------------------------------
    # Traits
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        ConvertiblePackageBase.__init__(self, *args, **kwds)
        self._customPaneName = 'CustomPanes_InstrumentOnSwap' # FExtensionValue
        self.on_trait_change(self.SetInsB2BPrice, ['price', 'b2bEnabled'])
        self.on_trait_change(self.SetStockB2BPrice, ['stockPrice', 'b2bEnabled'])
        ReinitializeLogger(3)

    # --------------------------------------------------------------------------
    # Overridden methods from DealPackageDefaultDefinition
    # --------------------------------------------------------------------------
    def CB(self):
        cb = None
        ins = self.Instrument()
        if ins.InsType() == 'Option':
            cb = ins.Underlying()
        else:
            cb = ins
        return cb

    def LeadTrade(self):
        return self.InsTrade()

    def LeadB2B(self):
        return self.InsB2B()

    def SetNewInsIfNeeded(self):
        if self.insNew:
            ins = self.insNew
            self.insNew = None
            dp = self.DealPackage()
            CreateDefaultPackages.CreateDefaultInstrumentOnSwapPackage(ins, dp)
            self.SetDefaultAttributes()

    def AssemblePackage(self, ins = None):
        # pylint: disable-msg=W0221    
        if not ins:
            ins = self.AllCBChoices().First()
        self.insNew = ins
        self.SetNewInsIfNeeded()
        super(InstrumentOnSwapDefinition, self).OnNew()

    #Instrument

    insType =           Str(    label='Ins Type',
                                toolTip='Type of derivative',
                                choiceListSource='@ValidInstrumentTypes')

    ins  =              Object( label='Ins Name',
                                objMapping='InsTrade.Instrument',
                                toolTip='Instrument',
                                choiceListSource ='@InstrumentList',
                                transform='@ValidateInstrument')

    onSwapDelta =       Float(  label='Delta',
                                objMapping='DealPackage.AdditionalInfo.OnSwapDelta',
                                toolTip='Delta for hedge. Stored in add info "OnSwapDelta"',
                                formatter='PercentShowZero')

    #Stock
    stockName =         Str(    label='Name',
                                objMapping='Stock.Name',
                                toolTip='Stock name',
                                enabled=False)

    stockQuantity =     Float(  label='Quantity',
                                objMapping='StockTrade.Quantity',
                                toolTip='Quantity of stock hedge',
                                formatter='InstrumentDefinitionNominal',
                                validate='@RoundStockQuantity',
                                backgroundColor='@StockQuantityBackGroundColor')

    stockPrice =        Float(  label='Price ',
                                objMapping='StockTrade.Price',
                                formatter='InstrumentDefinitionStrikePrice' )

    stockValueDay =     Date(  label='Value Day ',
                                objMapping='StockTrade.ValueDay',
                                transform='@TransformPeriodToDate' )

    b2bAcq =            Object( label='B2B Acquirer',
                                objMapping='InsB2B.TraderAcquirer|StockB2B.TraderAcquirer',
                                choiceListSource=AcquirerChoices() )

    b2bEnabled =        Object( objMapping='InsB2B.SalesCoverEnabled|StockB2B.SalesCoverEnabled',
                                label='B2B' )

    b2bPrf =            Object( label='B2B Portfolio',
                                objMapping='InsB2B.TraderPortfolio|StockB2B.TraderPortfolio',
                                choiceListSource=PortfolioChoices() )

    def _tradeTime_changed(self, attribute, oldValue, newValue, *args):
        super(InstrumentOnSwapDefinition, self)._tradeTime_changed(attribute, oldValue, newValue)
        self.stockValueDay = self.StockTrade().ValueDay()

    def SetDefaultAttributes(self):
        self.SetDefaultOnSwapStockAttributes()
        self.SetDefaultTradeAttributes()

    def ValidateInstrument(self, traitName, value, *args):
        if not value:
            value = self.ins
        return value

    def RoundStockQuantity(self, traitName, value, *args):
        if value:
            value = round(value)
        return value

def StartInstrumentOnSwapApplication(eii):
    instruments=GetInstruments(eii)
    name = 'Instrument On Swap'
    insPackage = None
    inst = None
    if isAscotOrConvertible(instruments):
        inst=instruments.First()
        insPackage = utils.InstrumentPackageIfUnique(inst, name)
    if insPackage is None:
        dp = acm.DealPackage.New(name, inst)
    else:
        dp = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(insPackage)
    utils.StartDealPackage(dp)

def isAscotOrConvertible(instruments):
    alt1 = hasattr(instruments, 'First') and instruments.First().IsKindOf(acm.FConvertible)
    alt2 = hasattr(instruments, 'First') and instruments.First().IsKindOf(acm.FOption) and instruments.First().Underlying().IsKindOf(acm.FConvertible)
    return alt1 or alt2