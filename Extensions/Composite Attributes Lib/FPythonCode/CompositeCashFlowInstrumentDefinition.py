import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool, List
from DealPackageUtil import UnDecorate
from ChoicesExprInstrument import getCategories
from CompositeInstrumentDefinition import InstrumentDefinition

class CashFlowInstrumentDefinition(InstrumentDefinition):

    def OnInit(self, instrument, **kwargs):
        super(CashFlowInstrumentDefinition, self).OnInit(instrument, **kwargs)
        
        
    def Attributes(self):
        
        attributes = super(CashFlowInstrumentDefinition, self).Attributes()
        
        attributes['cashFlowGeneration']      = Action( label='CF Gen...',
                                                        dialog=AttributeDialog( label='Cash Flow Generation', 
                                                        customPanes=self.UniqueCallback('@CashFlowGenerationPanes')),
                                                        visible=self.UniqueCallback('@CashFlowGenerationVisible'))
        attributes['cfgRegenerate']           = Bool(   label='Regenerate                 ')
        attributes['cfgRegenerateAll']        = Bool(   label='All',
                                                        enabled=self.UniqueCallback('@CfgRegenerateAllEnabled'),
                                                        onChanged=self.UniqueCallback('@OnCfgRegenerateAllChanged'))
        attributes['cfgRegenerateFuture']     = Bool(   label='Future',
                                                        enabled=self.UniqueCallback('@CfgRegenerateFutureEnabled'),
                                                        onChanged=self.UniqueCallback('@OnCfgRegenerateFutureChanged'))
        attributes['cfgSetFixedRate']         = Bool(   label='Set Fixed Rate',
                                                        enabled=self.UniqueCallback('@CfgSetFixedRateEnabled'),
                                                        visible=self.UniqueCallback('@CfgSetFixedRateVisible'),
                                                        recreateCalcSpaceOnChange=True)
        attributes['cfgSetSpread']            = Bool(   label='Set Spread',
                                                        enabled=self.UniqueCallback('@CfgSetSpreadEnabled'),
                                                        visible=self.UniqueCallback('@CfgSetSpreadVisible'),
                                                        recreateCalcSpaceOnChange=True)
        attributes['endDate']                 = Object( label='End',
                                                        objMapping=self._instrument+'.LegEndDate',
                                                        transform=self.UniqueCallback('@EndDateTransform'),
                                                        enabled=self.UniqueCallback('@EndDateEnabled'),
                                                        formatter='EndDateField',
                                                        width=11)
        attributes['endPeriod']               = Object( label='',
                                                        objMapping=self._instrument+'.LegEndPeriod',
                                                        enabled=self.UniqueCallback('@EndPeriodEnabled'),
                                                        width=11)
        attributes['fixNominalLeg']           = Object( label='Lock',
                                                        objMapping=self._instrument+'.FixNominalLeg',
                                                        choiceListSource = ["Pay Leg", "Receive Leg", "None"]) 
        attributes['legsFxRate']              = Object( label=self.UniqueCallback('@CurrPairLabel'),
                                                        objMapping=self._instrument+'.LegsFxRate',
                                                        formatter='InstrumentDefintionLegsFxRate',
                                                        editable=self.UniqueCallback('@FxRateEditable'))
        attributes['legsFxRateInv']           = Object( label='',
                                                        objMapping=self._instrument+'.LegsFxRateInv',
                                                        formatter='InstrumentDefintionLegsFxRate',
                                                        editable=self.UniqueCallback('@FxRateEditable'))
        attributes['nonDeliverable']          = Object( label='NDS',
                                                        objMapping=self._instrument+'.NonDeliverable',
                                                        visible=self.UniqueCallback('@NonDeliverableVisible'))                                                       
        attributes['noticePeriod']            = Object( label='',
                                                        objMapping=self._instrument+'.NoticePeriod',
                                                        enabled=self.UniqueCallback('@NoticePeriodEnabled'),
                                                        width=11)
        attributes['rateType']                = Object( label='Rate Type',
                                                        objMapping=self._instrument+'.RateType',
                                                        visible='@IsShowModeInstrumentDetail')                                                      
        attributes['resetNominal']            = Object( label='Reset Nom.',
                                                        objMapping=self._instrument+'.ResetNominal',
                                                        enabled=self.UniqueCallback('@ResetNominalEnabled'))
        attributes['startDate']               = Object( label='Start',
                                                        objMapping=self._instrument+'.LegStartDate',
                                                        transform=self.UniqueCallback('@StartDateTransform'),
                                                        enabled=self.UniqueCallback('@StartDateEnabled'),
                                                        formatter='StartDateField',
                                                        width=11)
        attributes['startPeriod']             = Object( label='',
                                                        objMapping=self._instrument+'.LegStartPeriod',
                                                        enabled=self.UniqueCallback('@StartPeriodEnabled'),
                                                        width=11)
        attributes['triggerCashFlowUpdate']   = Action( action=self.UniqueCallback('@TriggerCashFlowUpdate'),
                                                        noDealPackageRefreshOnChange=True)
        attributes['askBeforeSave']           = Action( action=self.UniqueCallback('@AskBeforeSave'))
        attributes['cfGenerationBeforeSave']  = Action( action=self.UniqueCallback('@ContinueSave'),
                                                        dialog=AttributeDialog( label='Cash Flow Generation', 
                                                        customPanes=self.UniqueCallback('@CashFlowGenerationPanes'),
                                                        btnLabel='Continue'))
        attributes['calledDialogs']           = List()

        self.Owner().RegisterCallbackOnAttributeChanged(self.AttributeChanged, last=True)
        
        return attributes
        
    # Interface overrides
    def OnNew(self):
        self.RegenerateCashFlowsIfNeeded()
 
    # ChoiceListSource callbacks      
       
    # Label Callbacks
    def CurrPairLabel(self, attributeName):
        try:
            if self.nonDeliverable:
                return self.Instrument().FirstPayLeg().NonDeliverableCurrency().Name() + '/' + self.Instrument().FirstReceiveLeg().NonDeliverableCurrency().Name()
            else:
                return self.Instrument().FirstPayLeg().Currency().Name() + '/' + self.Instrument().FirstReceiveLeg().Currency().Name()
        except:
            return ''
        
    # Enabled callbacks
    def CfgRegenerateAllEnabled(self, attributeName):
        return self.cfgRegenerate
        
    def CfgRegenerateFutureEnabled(self, attributeName):
        return self.cfgRegenerate
        
    def CfgSetFixedRateEnabled(self, attributeName):
        return not self.cfgRegenerate
        
    def CfgSetSpreadEnabled(self, attributeName):
        return not self.cfgRegenerate
        
    def EndDateEnabled(self, attributeName):
        if self.Instrument().IsOpenEnd():
            return False
        elif self.Instrument().FixedEndDay():
            return True
        else:
            return not self.Instrument().Generic()
    
    def EndPeriodEnabled(self, attributeName):
        if self.Instrument().IsOpenEnd():
            return False
        elif self.Instrument().FixedEndDay():
            return False
        else:
            return self.Instrument().Generic()
        
    def NoticePeriodEnabled(self, attributeName):
        return self.Instrument().IsOpenEnd()
        
    def ResetNominalEnabled(self, attributeName):
        return self.fixNominalLeg != 'None'
    
    def StartDateEnabled(self, attributeName):
        return not self.Instrument().Generic()
    
    def StartPeriodEnabled(self, attributeName):
        return self.Instrument().Generic()
        
    # Editable callbacks
    def FxRateEditable(self, attributeName):
        return self.Instrument().IsEnabled('LegsFxRate')
        
    # Visible callbacks
    def CashFlowGenerationVisible(self, attributeName):
        return self.Instrument().IsCashFlowInstrument() and self.Instrument().Originator().Oid() > 0
        
    def CfgSetFixedRateVisible(self, attributeName):
        return True
        
    def CfgSetSpreadVisible(self, attributeName):
        return True
        
    def NonDeliverableVisible(self, attributeName):
        return self.Instrument().NonDeliverable() or self.IsShowModeDetail()
        
    # Transform callbacks
    def EndDateTransform(self, attributeName, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Instrument().LegEndDateFromPeriod(newDate)
        return newDate
        
    def StartDateTransform(self, attributeName, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Instrument().LegStartDateFromPeriod(newDate)
        return newDate
        
    # OnChanged callbacks
    def OnCfgRegenerateAllChanged(self, *args):
        self.cfgRegenerateFuture = not self.cfgRegenerateAll
        
    def OnCfgRegenerateFutureChanged(self, *args):
        self.cfgRegenerateAll = not self.cfgRegenerateFuture
        
    # Action
    def TriggerCashFlowUpdate(self, attributeName):
        pass # Just needed to trigger refresh of attributes
    def GetCashFlowsAndResets(self, ins):
        cashFlowsAndResets = acm.FArray()
        for leg in ins.Legs():
            cashFlowsAndResets.AddAll(leg.CashFlows())
            cashFlowsAndResets.AddAll(leg.Resets())
        return cashFlowsAndResets

    def CashFlowsDiffer(self, ins1, ins2):
        cashFlowsAndResets1 = self.GetCashFlowsAndResets(UnDecorate(ins1))
        cashFlowsAndResets2 = self.GetCashFlowsAndResets(UnDecorate(ins2))
        return len(cashFlowsAndResets1.Difference(cashFlowsAndResets2, True))
        
    def AskBeforeSave(self, attributeName, saveConfig):
        ins = UnDecorate(self.Instrument())
        if not self.cfgRegenerate and ins.IsStorageImage():
            copy = acm.FBusinessLogicDecorator.WrapObject(ins.StorageImage())
            self.RegenerateCashFlows(copy, True)
            if self.CashFlowsDiffer(copy, ins) and attributeName not in self.calledDialogs:
                self.calledDialogs.Add(attributeName)
                result = self.Owner().DealPackage().CallUserAction(self.PrefixedName('cfGenerationBeforeSave'))
                return result
    
    def ContinueSave(self, attributeName, *args):
        try:
            return self.Owner().DealPackage().Save()
        except:
            self.calledDialogs.Clear()
            raise

    # Util   
    def AttributeChanged(self, attributeName, oldValue, newValue, userInputAttributeName):
        if -1 != attributeName.find('_') and -1 == attributeName.find('triggerCashFlowUpdate') and not userInputAttributeName:
            self.RegenerateCashFlowsIfNeeded()
    
    def RegenerateCashFlows(self, ins, regenerateAll=False):
        ins.RegenerateCashFlowsIfNeeded(
                                regenerateAll or (self.cfgRegenerate and (self.cfgRegenerateAll or self.cfgRegenerateFuture)),
                                self.cfgRegenerateFuture and not regenerateAll,
                                self.cfgSetFixedRate,
                                False, #strike
                                False, #strike2
                                self.cfgSetSpread,
                                False, #spread2
                                False, #stepUpValue
                                False, #dividendCashFlowsAreRegenerated
                                None,  #initialFixing1
                                None   #initialFixing2
                                )

    def RegenerateCashFlowsIfNeeded(self):
        if self.Instrument().Originator().StorageId() < 0 or self.cfgRegenerate or self.cfgSetFixedRate or self.cfgSetSpread:
            copy = self.Instrument().Clone()
            self.RegenerateCashFlows(self.Instrument())
            if self.CashFlowsDiffer(self.Instrument(), copy):
                self.Instrument().Changed()
                try:
                    self.triggerCashFlowUpdate()
                except:
                    pass

    def CashFlowGenerationPanes(self, attrName):
        layout = self.UniqueLayout(
                    """
                    cfgRegenerate;
                    vbox[;
                        cfgRegenerateAll;
                        cfgRegenerateFuture;
                    );
                    cfgSetFixedRate;
                    cfgSetSpread;
                    """
                )
        return [{'Settings' : layout}]
