""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/ASCOTOnSwap.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    ASCOT On Swap

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
class ASCOTOnSwapDefinition(ConvertiblePackageBase):
    # pylint: disable-msg=R0904

    # --------------------------------------------------------------------------
    # Traits
    # --------------------------------------------------------------------------
    def __init__(self, *args, **kwds):
        # pylint: disable-msg=E1101
        ConvertiblePackageBase.__init__(self, *args, **kwds)
        self._customPaneName = 'CustomPanes_ASCOTOnSwap' # FExtensionValue
        self.on_trait_change(self.SetAscotB2BPrice, ['price', 'b2bEnabled'])
        self.on_trait_change(self.SetStockB2BPrice, ['stockPrice', 'b2bEnabled'])
        ReinitializeLogger(3) # Debug

    # --------------------------------------------------------------------------
    # Overridden methods from DealPackageDefaultDefinition
    # --------------------------------------------------------------------------
    def LeadTrade(self):
        return self.AscotTrade()

    def LeadB2B(self):
        return self.AscotB2B()

    def SetNewInsIfNeeded(self):
        # pylint: disable-msg=E1101
        if self.insNew:
            cb = self.insNew
            self.insNew = None
            dp = self.DealPackage()
            CreateDefaultPackages.CreateDefaultASCOTOnSwapPackage(cb, dp)
            self.SetDefaultAttributes()
            self.UpdateRateIndexChoices()

    def OnSave(self, config):
        # pylint: disable-msg=E1002
        super(ASCOTOnSwapDefinition, self).OnSave(config)
        self.GenerateCashFlowsAndRelinkSwap()

    def OnSaveNew(self, config):
        # pylint: disable-msg=E1002
        super(ASCOTOnSwapDefinition, self).OnSaveNew(config)
        self.GenerateCashFlowsAndRelinkSwap()

    def AssemblePackage(self, cb = None):
        # pylint: disable-msg=E1002,W0221
        if not cb:
            cb = self.AllCBChoices().First()
        self.insNew = cb
        self.SetNewInsIfNeeded()
        super(ASCOTOnSwapDefinition, self).OnNew()

    #CB
    cb =                Object( label='Und CB',
                                objMapping='AscotTrade.Instrument.Underlying',
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
    ascotName =         Str(    label='Name',
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

    settlementType =    Object( label='Settle Type',
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
                                toolTip='Recall swap spread.')

    maturityType =      CalcVal( label='Maturity Type',
                                choiceListSource='@ValidMaturityTypes',
                                calcMapping="Ascot:FDealSheet:Maturity Type",
                                toolTip='Defaults maturity date to next CB put date or next CB maturity date',
                                )


    floatRateReference =Object( label = 'Float Ref',
                                objMapping='IRSPayLeg.FloatRateReference',
                                choiceListSource = '@RateIndexChoices',
                                toolTip = 'Recall swap float rate reference')

    #Stock
    onSwapDelta =       Float(  label='Delta',
                                objMapping='DealPackage.AdditionalInfo.OnSwapDelta',
                                toolTip='Delta for hedge. Stored in add info "OnSwapDelta"',
                                formatter='Percent')

    stockName =             Str(    label='Stock Name',
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
                                objMapping='AscotB2B.TraderAcquirer|StockB2B.TraderAcquirer',
                                choiceListSource=AcquirerChoices() )

    b2bEnabled =        Object( objMapping='AscotB2B.SalesCoverEnabled|StockB2B.SalesCoverEnabled',
                                label='B2B' )

    b2bPrf =            Object( label='B2B Portfolio',
                                objMapping='AscotB2B.TraderPortfolio|StockB2B.TraderPortfolio',
                                choiceListSource = PortfolioChoices() )
                                
    irsStartDate =      Object( label='Start Date',
                                objMapping='IRS.LegStartDate',
                                toolTip='Start date of swap cashflows',
                                transform='@TransformPeriodToDate' )

    def _tradeTime_changed(self, attribute, oldValue, newValue, *args):
        # pylint: disable-msg=E1002
        super(ASCOTOnSwapDefinition, self)._tradeTime_changed(attribute, oldValue, newValue)
        self.stockValueDay = self.StockTrade().ValueDay()

    def UpdateRateIndexChoices(self):
        self._ClearList(self.rateIndexChoices)
        constraint = 'currency="' + self.IRS().Currency().Name() + '"'
        self.rateIndexChoices.AddAll(acm.FRateIndex.Select(constraint))

    def SetDefaultAttributes(self):
        self.SetDefaultCBAttributes()
        self.SetDefaultAscotAttributes()
        self.SetDefaultOnSwapStockAttributes()
        self.SetDefaultTradeAttributes()

    def ValidateInstrument(self, traitName, value, *args):
        # pylint: disable-msg=W0613
        if not value:
            value = self.cb
        return value

    def RoundStockQuantity(self, traitName, value, *args):
        # pylint: disable-msg=W0613
        if value:
            value = round(value)
        return value


def StartASCOTOnSwapApplication(eii):
    convertibles = GetInstruments(eii)
    dp = None
    cb = None
    if hasattr(convertibles, 'First') and convertibles.First().IsKindOf(acm.FConvertible):
        cb = convertibles.First()
    dp = acm.DealPackage.New('ASCOT On Swap', cb)
    utils.StartDealPackage(dp)
