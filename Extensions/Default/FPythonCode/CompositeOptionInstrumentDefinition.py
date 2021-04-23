import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool, CalcVal, ParseSuffixedFloat, Settings
from ChoicesExprInstrument import getExerciseTypeChoices
from CompositeDerivativeInstrumentDefinition import DerivativeInstrumentDefinition

@Settings(LogMode='Verbose')
class OptionInstrumentDefinition(DerivativeInstrumentDefinition):

    def OnInit(self, instrument, trade, **kwargs):
        super(OptionInstrumentDefinition, self).OnInit(instrument, **kwargs)
        self._trade = trade
        self._exerciseTypeChoices = DealPackageChoiceListSource()

    def Attributes(self):
        
        attributes = super(OptionInstrumentDefinition, self).Attributes()
        
        attributes['barrier']                 = Object( label='Barrier',
                                                        objMapping=self._instrument+'.Barrier',
                                                        visible=False,
                                                        solverParameter={'minValue':0.0001, 'maxValue':10000.0},
                                                        transform=self.UniqueCallback('@TransformStrike'),
                                                        backgroundColor='@SolverColor')
        attributes['exerciseType']            = Object( label='Exercise',
                                                        objMapping=self._instrument+'.ExerciseType',
                                                        choiceListSource=self.UniqueCallback('@ExerciseTypeChoices'),
                                                        width=13)
        attributes['rebate']                 = Object( label='Rebate',
                                                        objMapping=self._instrument+'.Rebate',
                                                        visible=False)
        attributes['strikePrice']             = Object( label='Strike Price',
                                                        objMapping=self._instrument+'.StrikePrice',
                                                        solverParameter={'minValue':0.0001, 'maxValue':10000.0},
                                                        transform=self.UniqueCallback('@TransformStrike'),
                                                        backgroundColor='@SolverColor',
                                                        width=13)
        attributes['strikeQuotation']         = Object( label='StrikeQuot',
                                                        objMapping=self._instrument+'.StrikeQuotation',  
                                                        visible=self.UniqueCallback('@StrikeQuotationVisible'))
        attributes['strikeType']              = Object( label='',
                                                        objMapping=self._instrument+'.StrikeType')                                                        
        
        attributes['tradePv']                 = CalcVal(label='PV',
                                                        calcMapping = self._trade + ':FTradeSheet:Portfolio Present Value',
                                                        solverTopValue = True)
        
        attributes['theorPrice']              = CalcVal(label='Theor Price',
                                                        calcMapping = self._trade + ':FTradeSheet:Price Theor',
                                                        solverTopValue = True)
                                                        
        attributes['undPrice']                = CalcVal( label='Und Price',
                                                         calcMapping=self._instrument + ':FDealSheet:Portfolio Underlying Price')

        attributes['undFwdPrice']             = CalcVal( label= 'Und Fwd Price',
                                                         calcMapping=self._instrument + ':FDealSheet:Portfolio Underlying Forward Price')
        
        return attributes
     
    # Enabled callbacks
    def ExpiryDateTimeEnabled(self, attributeName):
            return (self.Instrument().ExerciseType() != 'Bermudan' and not self.Instrument().Generic())

    # Visible callbacks
    def DigitalVisible(self, attributeName):
        if self.ExoticNeverShow(self.underlyingType):
            return False
        elif self.underlyingType in ['Average Future/Forward', 'Bill', 'Bond', 'CFD', 'CLN', 'Commodity Index', 'CreditDefaultSwap', 'CurrSwap', 'Deposit', 'FreeDefCF', 'FRA', 'FRN', 'IndexLinkedSwap', 'PromisLoan', 'RateIndex', 'Swap', 'TotalReturnSwap', 'VarianceSwap', 'Zero']:
            return (self.IsShowModeDetail() or self.Instrument().Digital())
        else:
            return True
    
    def StrikeQuotationVisible(self, attributeName):
        return self.IsShowModeDetail() or self.Instrument().StrikeQuotation()
        
    # ChoiceListSource callbacks             
    def ExerciseTypeChoices(self, attributeName):
        if self._exerciseTypeChoices.IsEmpty():
            self.UpdateExerciseTypeChoices()
        return self._exerciseTypeChoices
       
    # Transform callbacks
    def TransformStrike(self, attrName, value):
        if value in ['atm', 'atms', 's', 'spot']:
            return self.undPrice.Value().Number()
        elif value in ['atmf', 'fwd', 'f', 'forward']:
            return self.undFwdPrice.Value().Number()
        else:
            return self.TransformSolver(attrName, value)
    
    def TransformSolver(self, attrName, value):
        def Parse(topValueAttribute, value, suffix):
            f = self.GetAttributeMetaData(topValueAttribute, 'formatter')()
            topValue = None
            goalValue = ParseSuffixedFloat(value, suffix, f, True)
            if goalValue != None:
                topValue = self.PrefixedName(topValueAttribute)
            return goalValue, topValue
            
        # Parse pv
        goalValue, topValue = Parse('tradePv', value, ['pv'])
        
        # Parse theor
        if topValue == None:
            goalValue, topValue = Parse('theorPrice', value, ['theor', 'th', 't', 'pr', 'price'])
        
        if goalValue != None and topValue != None:
            return self.GetMethod("Solve")(topValue, attrName, goalValue)
        else:
            return value
        
        
    # OnChanged callbacks        
    def UpdateExerciseTypeChoices(self, *args):
        for exerciseType in getExerciseTypeChoices(self.underlyingType):
            if exerciseType != 'Bermudan':
                self._exerciseTypeChoices.Add(exerciseType)
        
    # Util


        
