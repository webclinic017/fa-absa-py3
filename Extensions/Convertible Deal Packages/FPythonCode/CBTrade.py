""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/CBTrade.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    CBTrade

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import ConvertiblePackageUtils as utils
from ConvertiblePackageBase import ConvertiblePackageBase, Object, Settings, AcquirerChoices, PortfolioChoices
from FAssetManagementUtils import ReinitializeLogger, GetInstruments
import CreateDefaultPackages

@Settings(MultiTradingEnabled=True)
class CBTradeDefinition(ConvertiblePackageBase):

    # --------------------------------------------------------------------------
    # Traits
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        ConvertiblePackageBase.__init__(self, *args, **kwds)
        self._customPaneName = 'CustomPanes_CBTrade' # FExtensionValue
        self.on_trait_change(self.SetCBB2BPrice, ['price', 'b2bEnabled'])

        ReinitializeLogger(3) # Debug

    # --------------------------------------------------------------------------
    # Overridden methods from DealPackageDefaultDefinition
    # --------------------------------------------------------------------------
    def LeadTrade(self):
        return self.CBTrade()

    def LeadB2B(self):
        return self.CBB2B()

    def SetNewInsIfNeeded(self):
        if self.insNew:
            cb = self.insNew
            self.insNew = None
            dp = self.DealPackage()
            CreateDefaultPackages.CreateDefaultCBTradePackage(cb, dp)
            self.SetDefaultAttributes()

    def AssemblePackage(self, cb = None):
        # pylint: disable-msg=W0221
        if not cb:
            cb = self.AllCBChoices().First()
        self.insNew = cb
        self.SetNewInsIfNeeded()
        super(CBTradeDefinition, self).OnNew()

   #CB
    cb =               Object(  label='Name',
                                objMapping='CBTrade.Instrument',
                                toolTip='Convertible bond',
                                choiceListSource='@AllCBChoices',
                                transform='@ValidateInstrument')

    isin =              Object( label='ISIN',
                                objMapping='CBTrade.Instrument.Isin',
                                toolTip='Convertible bond ISIN',
                                enabled=False )

    payCalendar =       Object( label='Calendar 1',
                                objMapping='CBLeg.PayCalendar',
                                toolTip='Coupons are adjusted with banking days from this calendar',
                                enabled=False )

    pay2Calendar =      Object( label='Calendar 2',
                                objMapping='CBLeg.Pay2Calendar',
                                toolTip='Coupons are adjusted with banking days from this calendar',
                                enabled=False )

    b2bAcq =            Object( label='B2B Acquirer',
                                objMapping='CBB2B.TraderAcquirer',
                                choiceListSource = AcquirerChoices() )

    b2bEnabled =        Object( objMapping='CBB2B.SalesCoverEnabled',
                                label='B2B' )

    b2bPrf =            Object( label='B2B Portfolio',
                                objMapping='CBB2B.TraderPortfolio',
                                choiceListSource = PortfolioChoices() )

    def SetDefaultAttributes(self):
        self.SetDefaultCBAttributes()
        self.SetDefaultTradeAttributes()

    def ValidateInstrument(self, traitName, value, *args):
        if not value:
            value = self.cb
        return value

def StartCBTradeApplication(eii):
    convertibles=GetInstruments(eii)
    insPackage = None
    cb = None
    name = 'CBTrade'
    if hasattr(convertibles, 'First') and convertibles.First().IsKindOf(acm.FConvertible):
        cb=convertibles.First()
        insPackage=utils.InstrumentPackageIfUnique(cb, name) 
    if insPackage is None:
        dp = acm.DealPackage.New(name, cb)
    else:
        dp = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(insPackage)
    utils.StartDealPackage(dp)