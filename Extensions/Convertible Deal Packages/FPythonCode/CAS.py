""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/CAS.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    CAS

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
import ConvertiblePackageUtils as utils
from DealPackageDevKit import CalcVal, Bool
from ConvertiblePackageBase import ConvertiblePackageBase, Date, Str, Object, Float, AcquirerChoices, PortfolioChoices, Settings
from FAssetManagementUtils import ReinitializeLogger, GetInstruments
import CreateDefaultPackages

@Settings(MultiTradingEnabled=False)
class CASDefinition(ConvertiblePackageBase):
    # --------------------------------------------------------------------------
    # Traits
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        ConvertiblePackageBase.__init__(self, *args, **kwds)
        self._customPaneName = 'CustomPanes_CAS' # FExtensionValue
        self.on_trait_change(self.SetCBB2BPrice, ['price', 'b2bEnabled'])
        ReinitializeLogger(3)

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
            CreateDefaultPackages.CreateDefaultCASPackage(cb, dp)
            self.SetDefaultAttributes()
            self.UpdateRateIndexChoices()

    def OnSave(self, config):
        super(CASDefinition, self).OnSave(config)
        self.GenerateCashFlowsAndRelinkSwap()

    def OnSaveNew(self, config):
        super(CASDefinition, self).OnSaveNew(config)
        self.GenerateCashFlowsAndRelinkSwap()

    def AssemblePackage(self, cb = None):
        # pylint: disable-msg=W0221    
        if not cb:
            cb = self.AllCBChoices().First()
        self.insNew = cb
        self.SetNewInsIfNeeded()
        super(CASDefinition, self).OnNew()

    def IsValid(self, errorAccumulator, aspect):
        super(CASDefinition, self).IsValid(errorAccumulator, aspect)
        if self.IRSPayLeg().LegType() == 'Float' and self.IRSPayLeg().FloatRateReference() == None:
            errorAccumulator.ValidationError('Float rate reference missing for IRS')

    #CB
    cb =                Object( label='Name',
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

    settlementType =	Object( label='Settle Type',
                                objMapping='Ascot.SettlementType',
                                toolTip='Describes how the ASCOT settles')

    couponFrequency =   Object( label='Rolling Period',
                                objMapping='IRSPayLeg.RollingPeriod',
                                toolTip='Float rate cash flow rolling frequency of IRS')

    maturityType =      CalcVal( label='Maturity Type',
                                choiceListSource='@ValidMaturityTypes',
                                calcMapping="Ascot:FDealSheet:Maturity Type",
                                toolTip='Defaults maturity date to next CB put date or next CB maturity date',
                                )

    # IRS
    irsName =           Str(    label='Name ',
                                objMapping='IRS.Name',
                                toolTip='Name of IRS in CAS')

    irsStartDate =      Object( label='Start Date',
                                objMapping='IRS.LegStartDate',
                                toolTip='Start date of IRS in CAS',
                                transform='@TransformPeriodToDate' )

    irsEndDate =        Object( label='End Date',
                                objMapping='IRS.LegEndDate',
                                toolTip='End date of IRS in CAS',
                                transform='@TransformPeriodToDate' )

    dayCountMethod =    Object(    label='Day Count',
                                objMapping='IRSPayLeg.DayCountMethod',
                                toolTip='Asset swap other side day-basis in Monis ASCOT',
                                choiceListSource='@ValidDayCountMethods')

    fixedRate =         Float(  label='Fixed Rate (%)',
                                objMapping='IRSPayLeg.FixedRate',
                                toolTip='Recall swap fixed rate')

    floatSpread =       Float(  label='Spread (bps)',
                                objMapping='IRSPayLeg.Spread',
                                formatter='Percent',
                                toolTip='Recall swap spread')

    floatRateReference =   Object( label='Float Ref',
                                objMapping='IRSPayLeg.FloatRateReference',
                                choiceListSource='@RateIndexChoices')

    irsPayCalendar =       Object( label='Calendar 1 ',
                                objMapping='IRSPayLeg.PayCalendar',
                                toolTip='Coupons are adjusted with banking days from this calendar')

    irsPay2Calendar =      Object( label='Calendar 2 ',
                                objMapping='IRSPayLeg.Pay2Calendar',
                                toolTip='Coupons are adjusted with banking days from this calendar')

    irsPay3Calendar =      Object( label='Calendar 3 ',
                                objMapping='IRSPayLeg.Pay3Calendar',
                                toolTip='Coupons are adjusted with banking days from this calendar')

    irsPay4Calendar =      Object( label='Calendar 4 ',
                                objMapping='IRSPayLeg.Pay4Calendar',
                                toolTip='Coupons are adjusted with banking days from this calendar')

    payDayMethod =      Object( label='Day Conv',
                                objMapping='IRSPayLeg.PayDayMethod',
                                toolTip='Determines method to adjust cash flow pay dates if a date is not a valid banking day')

    longStub =          Bool(   label='Long Stub',
                                objMapping='IRSPayLeg.LongStub',
                                toolTip='Determines if there is a long or short first coupon period.')

    fixedCoupon =       Bool(   label='Fix Period',
                                objMapping='IRSPayLeg.FixedCoupon',
                                toolTip='If selected cash flow start and end days will not be business day adjusted. Cash flow pay days will not be affected by this setting')

    legType =           Object( label='Payment Type',
                                objMapping='IRSPayLeg.LegType',
                                choiceListSource='@ValidLegTypes',
                                toolTip='Payment type')

    b2bAcq =            Object( label='B2B Acquirer',
                                objMapping='CBB2B.TraderAcquirer|AscotB2B.TraderAcquirer|IRSB2B.TraderAcquirer',
                                choiceListSource = AcquirerChoices() )

    b2bEnabled =        Object( objMapping='CBB2B.SalesCoverEnabled|AscotB2B.SalesCoverEnabled|IRSB2B.SalesCoverEnabled',
                                label='B2B' )

    b2bPrf =            Object( label='B2B Portfolio',
                                objMapping='CBB2B.TraderPortfolio|AscotB2B.TraderPortfolio|IRSB2B.TraderPortfolio',
                                choiceListSource = PortfolioChoices() )
    #Trade
    irsStatus =          Object( label='IRS Status',
                                objMapping='IRSTrade.Status',
                                enabled=False )

    ascotStatus =        Object( label='ASCOT Status',
                                objMapping='AscotTrade.Status',
                                enabled=False)

    irsValueDay =       Date(  label='Value Day  ',
                                objMapping='IRSTrade.ValueDay',
                                transform='@TransformPeriodToDate' )

    ascotValueDay =     Date(  label='Value Day ',
                                objMapping='AscotTrade.ValueDay',
                                transform='@TransformPeriodToDate' )

    def _tradeTime_changed(self, attribute, oldValue, newValue, *args):
        super(CASDefinition, self)._tradeTime_changed(attribute, oldValue, newValue)
        self.irsValueDay = self.IRSTrade().ValueDay()
        self.ascotValueDay = self.AscotTrade().ValueDay()

    def _nominal_changed(self, attribute, oldValue, newValue, *args):
        self.IRSTrade().Nominal(-self.CBTrade().Nominal())
        self.AscotTrade().Nominal(-self.CBTrade().Nominal())
        self.GenerateCashFlowsAndRelinkSwap()
        self.SetPremium()

    def _ascotContractSize_changed(self, attribute, oldValue, newValue, *args):
        self.AscotTrade().Nominal(-self.CBTrade().Nominal())
        self.GenerateCashFlowsAndRelinkSwap()

    def SetTradeStatusOnNonLeadTrades(self):
        self.irsStatus = self.status
        self.ascotStatus = self.status

    def UpdateRateIndexChoices(self):
        self._ClearList(self.rateIndexChoices)
        constraint = 'currency="' + self.IRS().Currency().Name() + '"'
        self.rateIndexChoices.AddAll(acm.FRateIndex.Select(constraint))

    def ValidMaturityTypes(self, *args):
        types = [utils.CB_MAT_2BD, utils.CB_PUT_2BD]
        return types

    def SetDefaultAttributes(self):
        self.SetDefaultCBAttributes()
        self.SetDefaultAscotAttributes()
        self.SetDefaultIRSAttributes()
        self.SetDefaultTradeAttributes()

    def ValidateInstrument(self, traitName, value, *args):
        if not value:
            value = self.cb
        return value

def StartCASApplication(eii):
    convertibles=GetInstruments(eii)
    cb = None
    name = 'CAS'
    if hasattr(convertibles, 'First') and convertibles.First().IsKindOf(acm.FConvertible):
        cb=convertibles.First()
    dp = acm.DealPackage.New(name, cb)
    utils.StartDealPackage(dp)
