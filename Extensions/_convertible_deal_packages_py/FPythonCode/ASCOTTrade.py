""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/ASCOTTrade.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    ASCOTTrade

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
from ConvertiblePackageBase import ConvertiblePackageBase, Object, AcquirerChoices, PortfolioChoices, Settings
import ConvertiblePackageUtils as utils
from FAssetManagementUtils import ReinitializeLogger, GetInstruments
import CreateDefaultPackages

@Settings(MultiTradingEnabled=True)
class ASCOTTradeDefinition(ConvertiblePackageBase):

    # --------------------------------------------------------------------------
    # Traits
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        ConvertiblePackageBase.__init__(self, *args, **kwds)
        self._customPaneName = 'CustomPanes_ASCOTTrade' # FExtensionValue
        self.on_trait_change(self.SetAscotB2BPrice, ['price', 'b2bEnabled'])

        ReinitializeLogger(3) # Release = 3

    # --------------------------------------------------------------------------
    # Overridden methods from DealPackageDefaultDefinition
    # --------------------------------------------------------------------------

    def LeadTrade(self):
        return self.AscotTrade()

    def LeadB2B(self):
        return self.AscotB2B()

    def SetNewInsIfNeeded(self):
        if self.insNew:
            ascot = self.insNew
            self.insNew = None
            dp = self.DealPackage()
            CreateDefaultPackages.CreateDefaultASCOTTradePackage(ascot, dp)
            self.SetDefaultAttributes()
            
    def AssemblePackage(self, ascot = None):
        # pylint: disable-msg=W0221    
        if not ascot:
            ascot = self.AllAscotChoices().First()
        self.insNew = ascot
        self.SetNewInsIfNeeded()
        super(ASCOTTradeDefinition, self).OnNew()

    #ASCOT
    ascot =             Object( label='Name',
                                objMapping='AscotTrade.Instrument',
                                toolTip='ASCOT',
                                choiceListSource='@AllAscotChoices',
                                transform='@ValidateInstrument')

    b2bAcq =            Object( label='B2B Acquirer',
                                objMapping='AscotB2B.TraderAcquirer',
                                choiceListSource= AcquirerChoices() )

    b2bEnabled =        Object( objMapping='AscotB2B.SalesCoverEnabled',
                                label='B2B' )

    b2bPrf =            Object( label='B2B Portfolio',
                                objMapping='AscotB2B.TraderPortfolio',
                                choiceListSource= PortfolioChoices() )

    def SetDefaultAttributes(self):
        self.SetDefaultTradeAttributes()

    def ValidateInstrument(self, traitName, value, *args):
        if not value:
            value = self.ascot
        return value


def StartASCOTTradeApplication(eii):
    instruments=GetInstruments(eii)
    ascot = None
    insPackage = None
    name = 'ASCOTTrade'
    if hasattr(instruments, 'First') and instruments.First().IsKindOf(acm.FOption) and instruments.First().Underlying().IsKindOf(acm.FConvertible):
        ascot=instruments.First()
        insPackage=utils.InstrumentPackageIfUnique(ascot, name)
    if insPackage is None:
        dp = acm.DealPackage.New(name, ascot)
    else:
        dp = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(insPackage)
    utils.StartDealPackage(dp)
