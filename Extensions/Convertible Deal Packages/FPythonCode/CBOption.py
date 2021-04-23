""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/CBOption.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    CB Option

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import ConvertiblePackageUtils as utils
from DealPackageDevKit import CalcVal
from ConvertiblePackageBase import ConvertiblePackageBase, Date, Str, Object, Float, AcquirerChoices, PortfolioChoices, Settings
from FAssetManagementUtils import ReinitializeLogger, GetInstruments
import CreateDefaultPackages

@Settings(MultiTradingEnabled=False)
class CBOptionDefinition(ConvertiblePackageBase):

    # --------------------------------------------------------------------------
    # Traits
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        ConvertiblePackageBase.__init__(self, *args, **kwds)
        self._customPaneName = 'CustomPanes_CBOption' # FExtensionValue
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
            cb = self.insNew
            self.insNew = None
            dp = self.DealPackage()
            CreateDefaultPackages.CreateDefaultCBOptionPackage(cb, dp)
            self.SetDefaultAttributes()
            self.UpdateRateIndexChoices()

    def OnSave(self, config):
        super(CBOptionDefinition, self).OnSave(config)
        self.GenerateCashFlowsAndRelinkSwap()

    def OnSaveNew(self, config):
        super(CBOptionDefinition, self).OnSaveNew(config)
        self.GenerateCashFlowsAndRelinkSwap()

    def AssemblePackage(self, cb = None):
        # pylint: disable-msg=W0221
        if not cb:
            cb = self.AllCBChoices().First()
        self.insNew = cb
        self.SetNewInsIfNeeded()

        super(CBOptionDefinition, self).OnNew()

    #CB
    cb =                Object( label='Und CB',
                                objMapping='CBTrade.Instrument',
                                toolTip='Underlying convertible bond',
                                choiceListSource='@AllCBChoices',
                                transform='@ValidateInstrument')

    isin =              Object( label='Und ISIN',
                                objMapping='CB.Isin',
                                toolTip='Convertible bond ISIN',
                                enabled=False)

    payCalendar =       Object( label='Calendar 1',
                                toolTip='Coupons are adjusted with banking days from this calendar',
                                objMapping='CBLeg.PayCalendar',
                                enabled=False )

    pay2Calendar =      Object( label='Calendar 2',
                                toolTip='Coupons are adjusted with banking days from this calendar',
                                objMapping='CBLeg.Pay2Calendar',
                                enabled=False )

    #ASCOT
    ascotName =         Str(    label='Name  ',
                                objMapping='Ascot.Name',
                                toolTip='ASCOT name')

    ascotContractSize = Float(  label='Contr Size',
                                objMapping='Ascot.ContractSize',
                                toolTip='Contract size for ASCOT',
                                formatter='InstrumentDefinitionNominal')

    payDayOffset =      Object( label='Settle Days',
                                objMapping= 'Ascot.PayDayOffset',
                                toolTip='Settle days for ascot and spot days for recall swap')

    exerciseType =      Object( label='Exercise',
                                objMapping='Ascot.ExerciseType')

    maturityDateTime =    Object( label='Maturity',
                                objMapping='IRS.LegEndDate',
                                toolTip='Maturity of ASCOT and end date of IRS',
                                transform='@TransformPeriodToDate')

    firstExerciseDate = Object( label='First Exercise',
                                onChanged = '@SetIRSStartDate',
                                objMapping = 'FirstExerciseDate',
                                domain = "date",
                                toolTip='First exercise date of ascot',
                                transform='@TransformPeriodToDate' )

    lastExerciseDate =  Object( label='Last Exercise',
                                objMapping = 'Ascot.ExpiryDate',
                                toolTip='Last exercise date of ASCOT',
                                transform='@TransformPeriodToDate' )

    settlementType=     Object( label='Settle Type',
                                objMapping='Ascot.SettlementType',
                                toolTip='Describes how the ASCOT settles')

    couponFrequency =   Object( label='Rolling Period',
                                objMapping='IRSPayLeg.RollingPeriod',
                                toolTip='Float rate cash flow rolling frequency of IRS')

    dayCountMethod =    Object(   label='Day Count',
                               objMapping='IRSPayLeg.DayCountMethod',
                                toolTip='Asset swap other side day count convention. ',
                                choiceListSource='@ValidDayCountMethods')

    floatSpread  =      Float(  label='Spread (bps)',
                                objMapping='IRSPayLeg.Spread',
                                formatter='Percent',
                                toolTip='Recal swap spread.')

    maturityType =      CalcVal( label='Maturity Type',
                                choiceListSource='@ValidMaturityTypes',
                                calcMapping="Ascot:FDealSheet:Maturity Type",
                                toolTip='Defaults maturity date to next CB put date or next CB maturity date',
                                )

    floatRateReference =Object( label = 'Float Ref',
                                objMapping='IRSPayLeg.FloatRateReference',
                                choiceListSource = '@RateIndexChoices',
                                toolTip = 'Recall swap float rate reference')

    ascotValueDay =     Date(   label='Value Day ',
                                objMapping='AscotTrade.ValueDay',
                                transform='@TransformPeriodToDate' )

    ascotPrice =        Float(  label='ASCOT Price ',
                                objMapping='AscotTrade.Price',
                                formatter='InstrumentDefinitionStrikePrice' )

    b2bAcq =            Object( label='B2B Acquirer',
                                objMapping='CBB2B.TraderAcquirer|AscotB2B.TraderAcquirer',
                                choiceListSource=AcquirerChoices() )

    b2bEnabled =        Object( objMapping='CBB2B.SalesCoverEnabled|AscotB2B.SalesCoverEnabled',
                                label='B2B' )

    b2bPrf =            Object( label='B2B Portfolio',
                                objMapping='CBB2B.TraderPortfolio|AscotB2B.TraderPortfolio',
                                choiceListSource=PortfolioChoices() )
                                
    irsStartDate =      Object( label='Start Date',
                                objMapping='IRS.LegStartDate',
                                toolTip='Start date of swap cashflows',
                                transform='@TransformPeriodToDate' )

    def _tradeTime_changed(self, attribute, oldValue, newValue, *args):
        super(CBOptionDefinition, self)._tradeTime_changed(attribute, oldValue, newValue)
        self.ascotValueDay = self.AscotTrade().ValueDay()

    def _nominal_changed(self, attribute, oldValue, newValue, *args):
        self.AscotTrade().Nominal(-self.CBTrade().Nominal())
        self.GenerateCashFlowsAndRelinkSwap()
        self.SetPremium()

    def UpdateRateIndexChoices(self):
        self._ClearList(self.rateIndexChoices)
        constraint = 'currency="' + self.IRS().Currency().Name() + '"'
        self.rateIndexChoices.AddAll(acm.FRateIndex.Select(constraint))

    def SetDefaultAttributes(self):
        self.SetDefaultCBAttributes()
        self.SetDefaultAscotAttributes()
        self.SetDefaultTradeAttributes()

    def ValidateInstrument(self, traitName, value, *args):
        if not value:
            value = self.cb
        return value

def StartCBOptionApplication(eii):
    convertibles=GetInstruments(eii)
    cb = None
    name = 'CBOption'
    if hasattr(convertibles, 'First') and convertibles.First().IsKindOf(acm.FConvertible):
        cb=convertibles.First()
    dp = acm.DealPackage.New(name, cb)
    utils.StartDealPackage(dp)
