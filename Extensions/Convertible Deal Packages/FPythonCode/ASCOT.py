""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/ASCOT.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    ASCOT

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm
from ConvertiblePackageBase import ConvertiblePackageBase, Str, Object, Float, AcquirerChoices, PortfolioChoices, Settings
from DealPackageDevKit import CalcVal, DatePeriod
from DealPackageUtil import SetNew
import ConvertiblePackageUtils as utils
from FAssetManagementUtils import ReinitializeLogger, GetInstruments
import CreateDefaultPackages
from FAscotValuationFunctions import GetRecallSwap

@Settings(MultiTradingEnabled=False)
class ASCOTDefinition(ConvertiblePackageBase):

    def __init__(self, *args, **kwds):
        ConvertiblePackageBase.__init__(self, *args, **kwds)
        self._customPaneName = 'CustomPanes_ASCOT' # FExtensionValue
        self.on_trait_change(self.SetAscotB2BPrice, ['price', 'b2bEnabled'])
        ReinitializeLogger(3) # Release = 3

    def LeadTrade(self):
        return self.AscotTrade()

    def LeadB2B(self):
        return self.AscotB2B()

    def SetNewInsIfNeeded(self):
        if self.insNew:
            cb = self.insNew
            self.insNew = None
            dp = self.DealPackage()
            CreateDefaultPackages.CreateDefaultASCOTPackage(cb, dp)
            self.SetDefaultAttributes()
            self.UpdateRateIndexChoices()
            
    def OnOpen(self):
        recallSwap = GetRecallSwap(self.Ascot().DecoratedObject().Originator())
        self.SetAttribute('ascotPricingType', 'Swap' if recallSwap else 'Yield', silent = True)
        super(ASCOTDefinition, self).OnOpen()
    
    def OnSave(self, config):
        saveNewIns = []
        ascotPricingType = self.AscotPricingType()
        if config.InstrumentPackage() == 'Save':
            if self.InstrumentPackageIsEditable():
                if ascotPricingType == 'Swap':
                    saveNewIns = self.Instruments()
                elif ascotPricingType == 'Yield':
                    saveNewIns = self.Instruments().Filter(OnSaveInsFilter)
        elif config.InstrumentPackage() == 'SaveNew':
            if ascotPricingType == 'Swap':
                saveNewIns = self.Instruments()
            elif ascotPricingType == 'Yield':
                saveNewIns = self.Instruments().Filter(OnSaveInsFilter)
        SetNew(saveNewIns)
        super(ASCOTDefinition, self).OnSave(config)
        
        if ascotPricingType == 'Swap':
            self.GenerateCashFlowsAndRelinkSwap()

    def AssemblePackage(self, cb = None):
        # pylint: disable-msg=W0221
        if not cb:
            cb = self.AllCBChoices().First()
        self.insNew = cb
        self.SetNewInsIfNeeded()
        super(ASCOTDefinition, self).OnNew()

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
    ascotName =         Str(    label='Name ',
                                objMapping='Ascot.Name',
                                toolTip='Unique name of ascot')
                                
    ascotPricingType =  Object(    label = 'Pricing Type',
                                   defaultValue = 'Swap',
                                   onChanged = '@UpdateFixedYield',
                                   choiceListSource = ['Swap', 'Yield',],
                                   enabled = '@InstrumentPackageIsEditable',
                                   toolTip = 'Ascot pricing type. For pricing type Swap, a recall swap is created and linked to the ascot; ' \
                                             'for pricing type Yield, no swap is created and the fixed yield is stored in the rebate field of the ascot.',
                            )
                                 
    recallSwapFixedYield = Float(  label = 'Yield (%)',
                                   defaultValue = 0.0,
                                   objMapping = 'Ascot.Rebate',
                                   toolTip = 'Fixed yield of recall swap',
                                   visible = '@IsYieldValued',)

    ascotContractSize = Float(  label='Contr Size',
                                objMapping='Ascot.ContractSize',
                                toolTip='Ascot contract size',
                                formatter='InstrumentDefinitionNominal')

    payDayOffset =      Object( label='Settle Days',
                                objMapping= 'Ascot.PayDayOffset',
                                toolTip='Settle days for ascot and spot days for recall swap')

    exerciseType =      Object( label='Exercise',
                                objMapping='Ascot.ExerciseType')


    firstExerciseDate = Object( label='First Exercise',
                                onChanged = '@SetIRSStartDate',
                                objMapping = 'FirstExerciseDate',
                                domain = "date",
                                toolTip='First exercise date of ascot',
                                transform='@TransformPeriodToDate' )

    lastExerciseDate =  Object( label='Last Exercise',
                                objMapping = 'Ascot.ExpiryDate',
                                toolTip='Last exercise date of ascot',
                                transform='@TransformPeriodToDate' )

    settlementType =    Object( label='Settle Type',
                                objMapping='Ascot.SettlementType',
                                toolTip='Ascot settlement style')
                                    
    maturityDateTime =    Object( label='Maturity',
                                  objMapping='IRS.LegEndDate',
                                  toolTip='Maturity of ascot and end date of IRS',
                                  visible = '@IsSwapValued',
                                  transform='@TransformPeriodToDate')  

    maturityType =      CalcVal( label='Maturity Type',
                                choiceListSource='@ValidMaturityTypes',
                                calcMapping="Ascot:FDealSheet:Maturity Type",
                                toolTip='Defaults maturity date to next CB put date or next CB maturity date',
                                visible = '@IsSwapValued',
                                )         

    couponFrequency =   DatePeriod( label='Rolling Period',
                                    objMapping='IRSPayLeg.RollingPeriod',
                                    visible = '@IsSwapValued',                                    
                                    toolTip='Float rate cash flow rolling frequency of IRS')                                

    dayCountMethod =    Object(  label='Day Count',
                                 objMapping='IRSPayLeg.DayCountMethod',
                                 toolTip='Other side day count convention. ',
                                 visible = '@IsSwapValued',                                
                                 choiceListSource='@ValidDayCountMethods')

    floatSpread  =      Float(  label='Spread (bps)',
                                objMapping='IRSPayLeg.Spread',
                                formatter='Percent',
                                visible = '@IsSwapValued',                                
                                toolTip='Recall swap spread.')

    floatRateReference =Object( label = 'Float Ref',
                                objMapping='IRSPayLeg.FloatRateReference',
                                choiceListSource = '@RateIndexChoices',
                                visible = '@IsSwapValued',                                
                                toolTip = 'Recall swap float rate reference')

    b2bAcq =            Object( label='B2B Acquirer',
                                objMapping='AscotB2B.TraderAcquirer',
                                choiceListSource=AcquirerChoices())

    b2bEnabled =        Object( objMapping='AscotB2B.SalesCoverEnabled',
                                label='B2B' )

    b2bPrf =            Object( label='B2B Portfolio',
                                objMapping='AscotB2B.TraderPortfolio',
                                choiceListSource=PortfolioChoices() )
                                
    irsStartDate =      Object( label='Start Date',
                                objMapping='IRS.LegStartDate',
                                visible = '@IsSwapValued',
                                toolTip='Start date of swap cashflows',
                                transform='@TransformPeriodToDate' )

    def SetDefaultAttributes(self):
        self.SetDefaultCBAttributes()
        self.SetDefaultAscotAttributes()
        self.SetDefaultTradeAttributes()

    def UpdateRateIndexChoices(self):
        self._ClearList(self.rateIndexChoices)
        constraint = 'currency="' + self.IRS().Currency().Name() + '"'
        self.rateIndexChoices.AddAll(acm.FRateIndex.Select(constraint))

    def ValidateInstrument(self, traitName, value, *args):
        if not value:
            value = self.cb
        return value
        
    def UpdateFixedYield(self, attrName, oldValue, newValue, *args):
        if newValue == 'Swap':
            self.SetAttribute('recallSwapFixedYield', 0.0, silent = True)
        
    def AscotPricingType(self):
        return self.ascotPricingType

    def InstrumentPackageIsEditable(self, *args):
        return self.DealPackage().Originator().InstrumentPackage().Originator().IsInfant()
        
    def IsSwapValued(self, attrName, *args):
        return self.AscotPricingType() == "Swap"
        
    def IsYieldValued(self, attrName, *args):
        return self.AscotPricingType() == "Yield"

def OnSaveInsFilter(ins):
    return ins.InsType() == 'Option'

def StartASCOTApplication(eii):
    convertibles = GetInstruments(eii)
    cb = None
    if hasattr(convertibles, 'First') and hasattr(convertibles.First(), 'IsKindOf') and convertibles.First().IsKindOf(acm.FConvertible):
        cb = convertibles.First()
    dp = acm.DealPackage.New('ASCOT', cb)
    utils.StartDealPackage(dp)
