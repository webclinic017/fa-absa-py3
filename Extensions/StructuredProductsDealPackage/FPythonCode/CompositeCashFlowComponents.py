
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, CompositeAttributeDefinition, ValGroupChoices, InstrumentPart
from CompositeComponentBase import CompositeBaseComponent
from SP_DealPackageHelper import IsDateTime
from SP_DealPackageHelper import MergeDictionaries as dMerge
from functools import partial


class CashFlowComponent(CompositeBaseComponent):

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------

    def Attributes(self):

        return {
                    # Slim view
                                               
                    'startDate'     : Object ( objMapping = InstrumentPart(self._instrumentName + '.LegStartDate'),
                                               label = "Start Date",
                                               toolTip = 'Start Date',
                                               onChanged = self.UniqueCallback("@SetEndDateAfterStartDate|RegenerateCashFlows"),
                                               transform = self.UniqueCallback("@TransformPeriodToStartDate")),

                    'endDate'       : Object ( objMapping = InstrumentPart(self._instrumentName + '.LegEndDate'),
                                               label = 'End Date',
                                               toolTip = 'End Date',
                                               onChanged = self.UniqueCallback("@RegenerateCashFlows"),
                                               transform = self.UniqueCallback("@TransformPeriodToEndDate"),
                                               validate = self.UniqueCallback("@ValidateEndDate") ),
                                               
                    'contractSize'  : Object ( objMapping = InstrumentPart(self._instrumentName + '.ContractSize'),
                                               label = 'Contract Size',
                                               onChanged = self.UniqueCallback("@RegenerateCashFlows"),
                                               toolTip = 'Contract Size' ),
                                                                   
                    # Detailed view                    
                    'payCalendar'   : Object ( objMapping = InstrumentPart(self._legName + '.PayCalendar'),
                                               label = 'Calendar',
                                               toolTip = 'Calendar',
                                               onChanged = self.UniqueCallback("@RegenerateCashFlows"),
                                               visible = self.UniqueCallback("@IsShowModeDetail") ),
                    
                    'valuationGroup' : Object ( objMapping = InstrumentPart(self._instrumentName + '.ValuationGrpChlItem'),
                                                label= 'Val Group',
                                                toolTip = 'Valuation Group',
                                                visible = self.UniqueCallback("@IsShowModeDetail"),
                                                choiceListSource = ValGroupChoices() )

                }

    def OnInit(self):
        raise DealPackageError('Use instrument type specific class instead of CashFlowComponent')
    

    # -----------------------------------------------
    # ##### Attribute callbacks that carry out
    # ##### specific tasks
    # -----------------------------------------------

    def VisibleContractSize(self, attrName):
        return False

    def RegenerateCashFlows(self, *rest):
        raise DealPackageException ( 'Component %s does not implement method RegenerateCashFlows' 
                                    % (self.__class__.__name__) )

    def SetEndDateAfterStartDate(self, *rest):
        # If start date is set to a date after end date, adjust the end date
        # to the next business date.
        # Using silent mode to enure that regenerate Cash flow is not called
        # from both start date and end date
        if IsDateTime(self.startDate) and IsDateTime(self.endDate):
            if acm.Time.DateDifference(self.startDate, self.endDate) >= 0:            
                self.SetAttribute('endDate', '1d', silent=True)

    # -----------------------------------------------
    # ##### Attribute callbacks that can be intercepted
    # ##### by the deal package
    # -----------------------------------------------
    
    def TransformPeriodToStartDate(self, attrName, value):
        if acm.Time().PeriodSymbolToDate(value):
            value = self.GetMethod(self._instrumentName)().LegStartDateFromPeriod(value)
        return value

    def TransformPeriodToEndDate(self, attrName, value):
        if acm.Time().PeriodSymbolToDate(value):
            value = self.GetMethod(self._instrumentName)().LegEndDateFromPeriod(value)
        return value

    def ValidateEndDate(self, attrName, value):
        validationStartDate = self.TransformPeriodToStartDate('startDate', self.startDate)
        if acm.Time().DateDifference(validationStartDate, value) >= 0:
            raise DealPackageUserException('End date must be after start date')

class CouponComponent(CashFlowComponent):

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------
    
    def Attributes(self):

        attributes = super(CouponComponent, self).Attributes()

        attributes['coupon']    = Object ( objMapping = InstrumentPart(self._legName + '.FixedRate'),
                                           label = 'Coupon',
                                           toolTip = 'Coupon',
                                           solverParameter = self.UniqueCallback('@SolverParametersCoupon'),
                                           backgroundColor = '@SolverColor',
                                           onChanged = self.UniqueCallback("@RegenerateCashFlows"),
                                           transform = self.UniqueCallback("@TransformCoupon") )

        return attributes


    def AttributeOverrides(self, overrideAccumulator):

        overrideAccumulator(
                {'startDate' : dict(label = 'Interest Start Date')})

    # -----------------------------------------------
    # ##### On Change Callbacks                #####
    # -----------------------------------------------

    def RegenerateCashFlows(self, *rest):
        self.GetMethod(self._legName)().GenerateCashFlows(self.coupon)

    # -----------------------------------------------
    # ##### Methods intended to be called from #####
    # ##### the Deal package itself            #####
    # -----------------------------------------------
            
    def SetParRate(self):
        if IsDateTime(self.startDate) and IsDateTime(self.endDate) and acm.Time.DateDifference(self.endDate, self.startDate) > 0:
            self.GetMethod(self._legName)().GenerateCashFlows(0)
            insCalc = self.GetMethod(self._instrumentName)().Calculation()
            calcSpace = self.GetMethod('_GetStdCalcSpace')()
            parRate = insCalc.ParRate(calcSpace) * 100.0
            self.coupon = parRate

    def SolverParametersCoupon(self, attrName, *rest):
        return {'minValue':0.0, 'maxValue':100.0}

    # -----------------------------------------------
    # ##### Other callback methods             #####
    # -----------------------------------------------

    def TransformCoupon(self, attrName, value):
        return self.TransformSolver(attrName, value)


class Deposit(CouponComponent):

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------
    
    def OnInit(self, depositName, depositLegName, **kwargs):
        self._instrumentName = depositName
        self._legName = depositLegName

    def IsValid(self, exceptionAccumulator, aspect):
        insToValidate = self.GetMethod(self._instrumentName)()
        if insToValidate:

            # Check instrument type:
            if insToValidate.InsType() != 'Deposit':
                exceptionAccumulator(
                        'Instrument type for deposit component must be deposit.')


    # -----------------------------------------------
    # ##### Methods intended to be called from #####
    # ##### the Deal package itself            #####
    # -----------------------------------------------
        
    def CreateInstrument(self):
        ins = acm.DealCapturing().CreateNewInstrument('Deposit')
        ins.Quotation('Clean')
        ins.MtmFromFeed(False)
        ins.FirstFixedLeg().PayOffset('0d')
        return ins
    
class CD(CouponComponent):

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------

    def OnInit(self, cdName, cdLegName, **kwargs):
        self._instrumentName = cdName
        self._legName = cdLegName

    def IsValid(self, exceptionAccumulator, aspect):

        insToValidate = self.GetMethod(self._instrumentName)()
        if insToValidate:

        # Check instrument type:
            if insToValidate.InsType() != 'CD':
                exceptionAccumulator(
                        'Instrument type for CD component must be CD.')

    # -----------------------------------------------
    # ##### Methods intended to be called from #####
    # ##### the Deal package itself            #####
    # -----------------------------------------------

    def CreateInstrument(self):
        ins = acm.DealCapturing().CreateNewInstrument('CD')
        ins.FirstFixedLeg().RollingPeriod('0d')
        ins.MtmFromFeed(False)
        ins.FirstFixedLeg().PayOffset('0d')
        return ins


class Bond(CouponComponent):

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------

    def OnInit(self, bondName, bondLegName, **kwargs):
        self._instrumentName = bondName
        self._legName = bondLegName

    def IsValid(self, exceptionAccumulator, aspect):

        insToValidate = self.GetMethod(self._instrumentName)()
        if insToValidate:

        # Check instrument type:
            if insToValidate.InsType() != 'Bond':
                exceptionAccumulator(
                        'Instrument type for bond component must be bond.')

    # -----------------------------------------------
    # ##### Methods intended to be called from #####
    # ##### the Deal package itself            #####
    # -----------------------------------------------

    def CreateInstrument(self):
        ins = acm.DealCapturing().CreateNewInstrument('Bond')
        ins.FirstFixedLeg().RollingPeriod('0d')
        ins.Quotation('Clean')
        ins.MtmFromFeed(False)
        ins.FirstFixedLeg().PayOffset('0d')
        return ins



class ZeroBond(CashFlowComponent):

    # -----------------------------------------------
    # ##### Override of methods from Dev Kit ###### #
    # -----------------------------------------------

    def OnInit(self, zeroName, zeroLegName, **kwargs):
        self._instrumentName = zeroName
        self._legName = zeroLegName

    def IsValid(self, exceptionAccumulator, aspect):
        insToValidate = self.GetMethod(self._instrumentName)()
        if insToValidate:

            # Check instrument type:
            if insToValidate.InsType() != 'Zero':
                exceptionAccumulator(
                        'Instrument type for zero bond component must be zero bond.')

    # -----------------------------------------------
    # ##### On Change Callbacks                #####
    # -----------------------------------------------

    def RegenerateCashFlows(self, *rest):
        self.GetMethod(self._legName)().GenerateCashFlows(0)

    # -----------------------------------------------
    # ##### Methods intended to be called from #####
    # ##### the Deal package itself            #####
    # -----------------------------------------------
        
    def CreateInstrument(self):
        ins = acm.DealCapturing().CreateNewInstrument('Zero')
        ins.Quotation('Pct of Nominal')
        ins.MtmFromFeed(False)
        ins.FirstFixedLeg().PayOffset('0d')
        return ins
