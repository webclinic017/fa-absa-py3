""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/CBOriginalOption.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    CBOriginalOption

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import ConvertiblePackageUtils as utils
from ConvertiblePackageBase import ConvertiblePackageBase, Date, Str, Object, Float, AcquirerChoices, PortfolioChoices, Settings
from FAssetManagementUtils import ReinitializeLogger, GetInstruments
import CreateDefaultPackages

@Settings(MultiTradingEnabled=True)
class CBOriginalOptionDefinition(ConvertiblePackageBase):

    # --------------------------------------------------------------------------
    # Traits
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        ConvertiblePackageBase.__init__(self, *args, **kwds)
        self._customPaneName = 'CustomPanes_CBOriginalOption' # FExtensionValue
        self.on_trait_change(self.SetCBB2BPrice, ['price', 'b2bEnabled'])
        self.on_trait_change(self.SetNonLeadAscotB2BPrice, ['ascotPrice', 'b2bEnabled'])
        ReinitializeLogger(3) # Debug = 2

    # --------------------------------------------------------------------------
    # Overridden methods from DealPackageDefaultDefinition
    # --------------------------------------------------------------------------
    def LeadTrade(self):
        return self.CBTrade()

    def LeadB2B(self):
        return self.CBB2B()

    def SetNewInsIfNeeded(self):
        if self.insNew:
            ins = self.insNew
            self.insNew = None
            dp = self.DealPackage()
            CreateDefaultPackages.CreateDefaultCBOriginalOptionPackage(ins, dp)
            self.SetDefaultAttributes()

    def AssemblePackage(self, ascot = None):
        # pylint: disable-msg=W0221
        if not ascot:
            ascot = self.AllAscotChoices().First()
        self.insNew = ascot
        self.SetNewInsIfNeeded()
        super(CBOriginalOptionDefinition, self).OnNew()

    #CB
    cb =                Str( label='Und CB',
                                objMapping='CB.Name',
                                toolTip='Underlying convertible bond',
                                enabled=False)

    isin =              Object( label='Und ISIN',
                                objMapping='CB.Isin',
                                toolTip='Convertible bond ISIN',
                                enabled=False)

    payCalendar =       Object( label='Calendar 1',
                                toolTip='Coupons are adjusted with banking days from this calendar',
                                objMapping='CBLeg.PayCalendar',
                                enabled=False)

    pay2Calendar =      Object(    label='Calendar 2',
                                toolTip='Coupons are adjusted with banking days from this calendar',
                                objMapping='CBLeg.Pay2Calendar',
                                enabled=False)

    #ASCOT
    ascot     =         Object( label='Name',
                                objMapping='AscotTrade.Instrument',
                                toolTip='ASCOT',
                                choiceListSource='@AllAscotChoices',
                                transform='@ValidateInstrument')

    ascotValueDay =     Date(  label='Value Day ',
                                objMapping='AscotTrade.ValueDay',
                                transform='@TransformPeriodToDate' )

    ascotPrice =        Float(  label='Price ',
                                objMapping='AscotTrade.Price',
                                formatter='InstrumentDefinitionStrikePrice' )

    b2bAcq =            Object( label='B2B Acquirer',
                                objMapping='CBB2B.TraderAcquirer|AscotB2B.TraderAcquirer',
                                choiceListSource = AcquirerChoices() )

    b2bEnabled =        Object( objMapping='CBB2B.SalesCoverEnabled|AscotB2B.SalesCoverEnabled',
                                label='B2B' )

    b2bPrf =            Object( label='B2B Portfolio',
                                objMapping='CBB2B.TraderPortfolio|AscotB2B.TraderPortfolio',
                                choiceListSource = PortfolioChoices() )


    def _tradeTime_changed(self, attribute, oldValue, newValue, *args):
        super(CBOriginalOptionDefinition, self)._tradeTime_changed(attribute, oldValue, newValue)
        self.ascotValueDay = self.AscotTrade().ValueDay()

    def _nominal_changed(self, attribute, oldValue, newValue, *args):
        self.AscotTrade().Nominal(-self.CBTrade().Nominal())
        self.SetPremium()

    def _cb_changed(self, attr, oldInsString, newInsString, *args):
        self.Refresh()

    def SetDefaultAttributes(self):
        self.SetDefaultCBAttributes()
        self.SetDefaultTradeAttributes()

    def ValidateInstrument(self, traitName, value, *args):
        if not value:
            value = self.ascot
        return value

def StartCBOriginalOptionApplication(eii):
    instruments=GetInstruments(eii)
    ascot = None
    insPackage = None
    name = 'CBOriginalOption'
    if hasattr(instruments, 'First') and instruments.First().IsKindOf(acm.FOption) and instruments.First().Underlying().IsKindOf(acm.FConvertible):
        ascot=instruments.First()
        insPackage=utils.InstrumentPackageIfUnique(ascot, name) 
    if insPackage is None:
        dp = acm.DealPackage.New(name, ascot)
    else:
        dp = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(insPackage)
    utils.StartDealPackage(dp)