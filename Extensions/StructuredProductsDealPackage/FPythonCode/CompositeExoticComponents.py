
import acm
import FUxCore
from CompositeComponentBase import CompositeBaseComponent
from SP_DealPackageHelper import GetFxFormatter
from DealPackageDevKit import DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DealPackageChoiceListSource, ValGroupChoices, InstrumentPart
from SP_DealPackageHelper import GetInitialFixingValue, GetInitialFixingDate, SetInitialFixingValue, SetInitialFixingDate, SetInitialFixingUnderlying, SettlementTypeChoices, BarrierTypeChoices, OptionTypeChoices, BarrierMonitoringChoices, RainbowTypeChoices, BarrierStatusChoices, AveragePriceTypeChoices, AverageStrikeTypeChoices, AverageMethodTypeChoices
from CompositeExoticEventComponents import ExoticEvent
from functools import partial




class Barrier(CompositeBaseComponent):

    def Attributes(self):
    
        return {

            'barrierLevel'       : Object ( objMapping = InstrumentPart(self._optionName + ".Barrier"),
                                            label = 'Barrier',
                                            toolTip = 'Barrier Level',
                                            solverParameter = self.UniqueCallback('@SolverParametersBarrierLevel'),
                                            backgroundColor = '@SolverColor',
                                            transform = self.UniqueCallback("@TransformBarrierLevel") ),

            'doubleBarrierLevel' : Object ( objMapping = InstrumentPart(self._optionName + ".Exotic.DoubleBarrier"),
                                            label = "2nd Barrier",
                                            toolTip = 'Second Barrier Level',
                                            solverParameter = self.UniqueCallback('@SolverParametersBarrierLevelSecond'),
                                            backgroundColor = '@SolverColor',
                                            transform = self.UniqueCallback("@TransformBarrierLevelSecond") ),
            
            'barrierType'        : Object   ( objMapping = InstrumentPart(self._optionName + ".Exotic.BarrierOptionType"),
                                            label = 'Barrier Type',
                                            toolTip = 'Barrier Type',
                                            recreateCalcSpaceOnChange=True,
                                            choiceListSource = self.UniqueCallback("@ChoicesBarrierType") ),

            'barrierMonitoring'  : Object ( objMapping = InstrumentPart(self._optionName + ".Exotic.BarrierMonitoring"),
                                            label = 'Monitoring',
                                            toolTip = 'Barrier Monitoring',
                                            recreateCalcSpaceOnChange=True,
                                            choiceListSource = self.UniqueCallback("@ChoicesBarrierMonitoring") ),
                                            
            'barrierStatus'      : Object ( objMapping = InstrumentPart(self._optionName + ".Exotic.BarrierCrossedStatus"),
                                            label = 'Crossed',
                                            toolTip = 'Barrier Status',
                                            recreateCalcSpaceOnChange=True,
                                            choiceListSource = self.UniqueCallback("@ChoicesBarrierStatus") ),
                                            
            'crossDate'          : Object ( objMapping = InstrumentPart(self._optionName + ".Exotic.BarrierCrossDate"),
                                            label = 'Cross Date',
                                            toolTip = 'Date barrier was crossed',
                                            recreateCalcSpaceOnChange=True ),
            
            'rebate'             : Object ( objMapping = InstrumentPart(self._optionName + ".Rebate"),
                                            label = 'Rebate',
                                            toolTip = 'Rebate',
                                            recreateCalcSpaceOnChange=True )
            
        }


    def GetLayout(self):
        return self.UniqueLayout( """
                                    hbox[Barrier;
                                        vbox{;
                                            barrierType;
                                            barrierMonitoring;
                                            barrierStatus;
                                            );
                                        vbox(;
                                            barrierLevel;
                                            doubleBarrierLevel;
                                            crossDate;
                                            );
                                        ];
                                  """)
                     

    def OnInit(self, optionName, **kwargs):
        self._optionName = optionName

    # -----------------------------------------------
    # ##### Attribute callbacks that carry out
    # ##### specific tasks
    # -----------------------------------------------

    def SolverParametersBarrierLevel(self, attrName, *rest):
        return [{'minValue':0.01, 'maxValue':10000}]

    def SolverParametersBarrierLevelSecond(self, attrName, *rest):
        return [{'minValue':0.01, 'maxValue':10000}]
    
    def TransformBarrierLevel(self, attrName, value):
        return self.TransformSolver(attrName, value)

    def TransformBarrierLevelSecond(self, attrName, value):
        return self.TransformSolver(attrName, value)

    def ChoicesBarrierType(self, attrName, *rest):
        return BarrierTypeChoices()

    def ChoicesBarrierMonitoring(self, attrName, *rest):
        return BarrierMonitoringChoices(self.GetMethod(self._optionName)().Exotic())

    def ChoicesBarrierStatus(self, attrName, *rest):
        return BarrierStatusChoices()

    def IsValid(self, exceptionAccumulator, aspect):
        insToValidate = self.GetMethod(self._optionName)()
        if insToValidate:
            # make sure that the instrument is still exotic type other
            if insToValidate.ExoticType() != 'Other':
                exceptionAccumulator.ValidationError('Exotic Type must be Other')
            
            # Make sure that it is a barrier option
            if not insToValidate.IsBarrier():
                exceptionAccumulator.ValidationError('Option should be a barrier option')
                        
            # make sure that only the allowed barrier type choices are used
            if(    insToValidate.Exotic() 
               and (not insToValidate.Exotic().BarrierOptionType() in self.GetAttributeMetaData('barrierType', 'choiceListSource')().GetChoiceListSource()) ):
                exceptionAccumulator.ValidationError('Barrier type "%s" not allowed on option' 
                                                      % insToValidate.Exotic().BarrierOptionType() )

            # make sure that only allowed monitrings are used
            if (    insToValidate.Exotic()
                and (not insToValidate.Exotic().BarrierMonitoring() in self.GetAttributeMetaData('barrierMonitoring', 'choiceListSource')().GetChoiceListSource()) ):
                exceptionAccumulator('Barrier Monitoring "%s" not allowed on option' % insToValidate.Exotic().BarrierMonitoring() )

class Rainbow(CompositeBaseComponent):

    def Attributes(self):
    
        return {

            'rainbowType' : Object ( objMapping = InstrumentPart(self._optionName + ".Exotic.RainbowOptionType"),
                                     label = 'Rainbow Type',
                                     toolTip = 'Rainbow Option Type',
                                     recreateCalcSpaceOnChange=True,
                                     choiceListSource = self.UniqueCallback("@ChoicesRainbowType") )
                }

    def OnInit(self, optionName, **kwargs):
        self._optionName = optionName

    def ChoicesRainbowType(self, attrName, *rest):
        return RainbowTypeChoices()

    def IsValid(self, exceptionAccumulator, aspect):
        insToValidate = self.GetMethod(self._optionName)()
        if insToValidate:
            # make sure that the instrument is still exotic type other
            if insToValidate.ExoticType() != 'Other':
                exceptionAccumulator.ValidationError('Exotic Type must be Other')
            
            # Make sure that it is a rainbow option
            if not insToValidate.IsRainbow():
                exceptionAccumulator.ValidationError('Option should be a rainbow option')
            
            # make sure that only the allowed rainbow type choices are used
            if(    insToValidate.Exotic() 
               and (not insToValidate.Exotic().RainbowOptionType() in self.ChoicesRainbowType('rainbowType')) ):
                exceptionAccumulator.ValidationError('rainbow type "%s" not allowed on option' 
                                                      % insToValidate.Exotic().RainbowOptionType() )


class Asian(CompositeBaseComponent):
    
    def Attributes(self):
    
        return {

            'averageMethodType'  : Object ( objMapping = InstrumentPart(self._optionName + ".Exotic.AverageMethodType"),
                                            label = 'Average Method',
                                            toolTip = 'Averaging method',
                                            recreateCalcSpaceOnChange=True,
                                            choiceListSource = self.UniqueCallback("@ChoicesAverageMethodType") ),
            
            'averagePriceType'   : Object ( objMapping = InstrumentPart(self._optionName + ".Exotic.AveragePriceType"),
                                            label = 'Price Type',
                                            toolTip = 'Price type of the average option',
                                            recreateCalcSpaceOnChange=True,
                                            choiceListSource = self.UniqueCallback("@ChoicesAveragePriceType") ),
            
            'averageStrikeType'  : Object ( objMapping = InstrumentPart(self._optionName + ".Exotic.AverageStrikeType"),
                                            label = 'Strike Type',
                                            toolTip = 'Strike type of the average option',
                                            recreateCalcSpaceOnChange=True,
                                            choiceListSource = self.UniqueCallback("@ChoicesAverageStrikeType") ),
            
            'averageDates'       : ExoticEvent ( optionName     = self._optionName, 
                                                 underlyingName = self._underlyingName,
                                                 displayColumns = self._eventDisplayColumns,
                                                 eventTypes     = self._eventTypes,
                                                 eventLabel     = self._eventLabel,
                                                 showAsButton   = self._showEventsAsButton,
                                                 eventUpdateAction = self._eventUpdateAction )

            }
    
    def OnInit(self, optionName, 
                    underlyingName, 
                    eventTypes = ['Average price', 'Average strike'],
                    showEventsAsButton = True,
                    eventLabel = 'Average Fixings',
                    eventDisplayColumns = None,
                    eventUpdateAction = None,
                    mustBeAsian = False,
                    **kwargs):

        self._optionName = optionName
        self._underlyingName = underlyingName
        self._eventTypes = [et for et in eventTypes if et in ['Average price', 'Average strike']]
        self._showEventsAsButton = showEventsAsButton
        self._eventLabel = eventLabel
        self._mustBeAsian = mustBeAsian
        self._eventDisplayColumns = eventDisplayColumns
        self._eventUpdateAction = eventUpdateAction

    def ChoicesAverageMethodType(self, attrName, *rest):
        return AverageMethodTypeChoices()
    
    def ChoicesAveragePriceType(self, attrName, *rest):
        return AveragePriceTypeChoices(self.averageStrikeType)
    
    def ChoicesAverageStrikeType(self, attrName, *rest):
        return AverageStrikeTypeChoices(self.averagePriceType)

    def IsValid(self, exceptionAccumulator, aspect):
        insToValidate = self.GetMethod(self._optionName)()
        if insToValidate:

            if self._mustBeAsian:

                # make sure that the instrument is still exotic type other
                if self._mustBeAsian and insToValidate.ExoticType() != 'Other':
                    exceptionAccumulator.ValidationError('Exotic Type must be Other')
            
                # Make sure that it is an asian option
                if not insToValidate.IsAsian():
                    exceptionAccumulator.ValidationError('Option should be an Asian option')
                
                # make sure that only the allowed average method type choices are used
                if(    insToValidate.Exotic() 
                   and (not insToValidate.Exotic().AverageMethodType() in self.ChoicesAverageMethodType('averageMethodType')) ):
                    # TODO: Use GetAttributeMetaData (choiceListSource) to get the allowed choices
                    exceptionAccumulator.ValidationError('Average method type "%s" not allowed on option' 
                                                          % insToValidate.Exotic().AverageMethodType() )

                # make sure that only the allowed average price type choices are used
                if(    insToValidate.Exotic() 
                   and (not insToValidate.Exotic().AveragePriceType() in self.ChoicesAveragePriceType('averagePriceType')) ):
                    # TODO: Use GetAttributeMetaData (choiceListSource) to get the allowed choices
                    exceptionAccumulator.ValidationError('Average price type "%s" not allowed on option' 
                                                          % insToValidate.Exotic().AveragePriceType() )

                # make sure that only the allowed average strike type choices are used
                if(    insToValidate.Exotic() 
                   and (not insToValidate.Exotic().AverageStrikeType() in self.ChoicesAverageStrikeType('averageStrikeType')) ):
                    # TODO: Use GetAttributeMetaData (choiceListSource) to get the allowed choices
                    exceptionAccumulator.ValidationError('Average strike type "%s" not allowed on option' 
                                                          % insToValidate.Exotic().AverageStrikeType() )
