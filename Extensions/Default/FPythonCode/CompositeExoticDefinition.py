import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, ReturnDomainDecorator, CalcVal, ParseSuffixedFloat
from CompositeExoticEventDefinition import ExoticEvent  
from CompositeAttributes import SelectInstrumentField 
from ChoicesExprExotic import getBarrierOptionTypeChoices, getBarrierMonitoringChoices, getVariationSwapCorridorTypeChoices, getVariationSwapTypeChoices

class ExoticDefinition(CompositeAttributeDefinition):

    def OnInit(self, instrument, trade):
        self._instrument = instrument
        self._trade = trade
        
    def Attributes(self):
        return {
                
                'varianceSwapCap'              : Object( label='Cap Strike',
                                                         objMapping=self._instrument + '.Exotic.VarianceSwapCap',
                                                         visible=self.UniqueCallback('@VarianceSwapCapVisible')),
                'varianceSwapFloor'            : Object( label='Floor Strike',
                                                         objMapping=self._instrument + '.Exotic.VarianceSwapFloor',
                                                         visible=self.UniqueCallback('@VarianceSwapFloorVisible')),
                'varianceSwapType'             : Object( label='Type',
                                                         choiceListSource=getVariationSwapTypeChoices,
                                                         objMapping=self._instrument + '.Exotic.VarianceSwapType'),
                'variationSwapUpperCorridor'   : Object( label='Upper Corridor',
                                                         objMapping=self._instrument + '.Exotic.VariationSwapUpperCorridor',
                                                         visible=self.UniqueCallback('@VariationSwapUpperCorridorVisible')),
                'variationSwapLowerCorridor'   : Object( label='Lower Corridor',
                                                         objMapping=self._instrument + '.Exotic.VariationSwapLowerCorridor',
                                                         visible=self.UniqueCallback('@VariationSwapLowerCorridorVisible')),
                'variationSwapCorridorType'    : Object( label='Corridor Type',
                                                         choiceListSource=getVariationSwapCorridorTypeChoices,
                                                         objMapping=self._instrument + '.Exotic.VariationSwapCorridorType'),
                'baseType'                     : Object( label='Base Type',
                                                         objMapping=self.UniqueCallback('BaseType'),
                                                         choiceListSource=['Vanilla', 'Barrier']),
                'barrierOptionType'            : Object( label='Barrier Type',
                                                         objMapping=self._instrument + '.Exotic.BarrierOptionType',
                                                         visible=self.UniqueCallback('@IsBarrierOption'),
                                                         choiceListSource=getBarrierOptionTypeChoices,
                                                         onChanged=self.UniqueCallback('@BarrierOptionTypeChanged')),
                'digitalBarrierType'           : Object( label='Digital Type',
                                                         objMapping=self._instrument + '.Exotic.DigitalBarrierType',
                                                         visible=self.UniqueCallback('@IsBarrierOption')),
                'doubleBarrier'                : Object( label='2nd Barrier',
                                                         objMapping=self._instrument + '.Exotic.DoubleBarrier',
                                                         visible=self.UniqueCallback('@IsBarrierOption'),
                                                         enabled=self.UniqueCallback('@IsDoubleBarrier'),
                                                         solverParameter={'minValue':0.0001, 'maxValue':10000.0},
                                                         transform=self.UniqueCallback('@TransformBarrier'),
                                                         backgroundColor='@SolverColor'),
                'barrierRebateOnExpiry'        : Object( label='Pay At Expiry',
                                                         objMapping=self._instrument + '.Exotic.BarrierRebateOnExpiry',
                                                         visible=self.UniqueCallback('@IsBarrierOption')),
                'barrierRiskManagement'        : Object( label='Risk Mgmt',
                                                         objMapping=self._instrument + '.Exotic.BarrierRiskManagement',
                                                         visible=self.UniqueCallback('@IsBarrierOption')),
                'secondBarrierRiskMgmt'        : Object( label='2nd Risk Mgmt',
                                                         objMapping=self._instrument + '.Exotic.SecondBarrierRiskMgmt',
                                                         visible=self.UniqueCallback('@IsBarrierOption'),
                                                         enabled=self.UniqueCallback('@IsDoubleBarrier')),
                'outsideBarrierInstrument'     : SelectInstrumentField( label='Instrument',
                                                         objMapping=self._instrument + '.Exotic.OutsideBarrierInstrument',
                                                         visible=self.UniqueCallback('@IsBarrierOption')),
                'barrierCrossedStatus'         : Object( label='Crossed',
                                                         objMapping=self._instrument + '.Exotic.BarrierCrossedStatus',
                                                         visible=self.UniqueCallback('@IsBarrierOption')),
                'barrierCrossDate'             : Object( label='Cross Date',
                                                         objMapping=self._instrument + '.Exotic.BarrierCrossDate',
                                                         visible=self.UniqueCallback('@IsBarrierOption'),
                                                         enabled=self.UniqueCallback('@IsBarrierCrossed'),
                                                         transform=self.UniqueCallback('@TransformPeriodToDate')),
                'barrierMonitoring'            : Object( label='Monitoring',
                                                         objMapping=self._instrument + '.Exotic.BarrierMonitoring',
                                                         visible=self.UniqueCallback('@IsBarrierOption'),
                                                         choiceListSource=['None', 'Continuous']),#self.UniqueCallback('@MonitoringChoices')),
                                                         
                'barrierDates'                 : ExoticEvent( optionName        = 'Instrument', 
                                                              underlyingName    = 'Underlying',
                                                              eventTypes        = ['Barrier date'],
                                                              eventLabel        = 'Dates...',
                                                              showAsButton      = True),                                                              
                'tradePv'                      : CalcVal(label='PV',
                                                        calcMapping = self._trade + ':FTradeSheet:Portfolio Present Value',
                                                        solverTopValue = True),        
                'theorPrice'                   : CalcVal(label='Theor Price',
                                                        calcMapping = self._trade + ':FTradeSheet:Price Theor',
                                                        solverTopValue = True),
                'undPrice'                     : CalcVal( label='Und Price',
                                                         calcMapping=self._instrument + ':FDealSheet:Portfolio Underlying Price'),
                'undFwdPrice'                  : CalcVal( label= 'Und Fwd Price',
                                                         calcMapping=self._instrument + ':FDealSheet:Portfolio Underlying Forward Price')
                                                         
                                                         
        }
    
    def GetLayout(self):
        return self.UniqueLayout("""
                                    hbox(;
                                    );
                                """)

    def Instrument(self):
        return self.GetMethod(self._instrument)()
        
    def Exotic(self):
        return self.Instrument().Exotic()
    
    def IsValid(self, exceptionAccumulator, aspect):
        if aspect == 'DealPackage':
            pass
    
    # Visible callbacks
    def VarianceSwapCapVisible(self, *args):
        show = False
        if self.varianceSwapType not in ['Floor', 'None']:
            show = True
        return show
    
    def VarianceSwapFloorVisible(self, *args):
        show = False
        if self.varianceSwapType not in ['Cap', 'None']:
            show = True
        return show
        
    def VariationSwapLowerCorridorVisible(self, *args):
        show = False
        if self.variationSwapCorridorType not in ['Downside Corridor', 'None']:
            show = True
        return show
    
    def VariationSwapUpperCorridorVisible(self, *args):
        show = False
        if self.variationSwapCorridorType not in ['Upside Corridor', 'None']:
            show = True
        return show
    
    def IsBarrierOption(self, *args):
        return self.baseType == 'Barrier'
        
    # Enabled callbacks
    def IsDiscreteMonitor(self, *args):
        return self.barrierMonitoring in ['Discrete', 'Window']
        
    def IsDoubleBarrier(self, *args):
        return self.barrierOptionType in ['Double In', 'Double Out', 'Custom']
        
    def IsBarrierCrossed(self, *args):
        return self.barrierCrossedStatus != 'None'
        
    # OnChanged callbacks
    def BarrierOptionTypeChanged(self, *args):
        if self.barrierOptionType == 'None':
            self.Instrument().ExoticType('None')
        
    # ChoiceListSource callbacks      
    def MonitoringChoices(self, attributeName):
        return getBarrierMonitoringChoices(self.Exotic())
        
    #Transform Callbacks
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
    
    def TransformBarrier(self, attrName, value):
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
               
    # Util
    @ReturnDomainDecorator('string')
    def BaseType(self, value = '*Reading*'):
        if value == '*Reading*':
            if self.barrierOptionType != 'None':
                return 'Barrier'
            else:
                return 'Vanilla'
        else:
            if value=='Barrier':
                if self.barrierOptionType == 'None':
                    self.barrierOptionType='Down & Out'
                    self.Instrument().ExoticType('Other')
            elif value=='Vanilla':
                self.barrierOptionType='None'
                self.Instrument().ExoticType('None')
            '''
            contractTrade = acm.FTrade[value] if value else None
            if not contractTrade and value:
                raise DealPackageException('No Trade')
            self.Trade().ContractTrdnbr(value)
            '''
