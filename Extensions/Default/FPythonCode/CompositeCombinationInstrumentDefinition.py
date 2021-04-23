import acm
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageChoiceListSource, AttributeDialog, Action, Object, Bool, Str, CalcVal, ParseSuffixedFloat, UXDialogsWrapper, ContextMenu, ContextMenuCommand
from CompositeInstrumentDefinition import InstrumentDefinition
from CompositeAttributes import SelectInstrumentsDialog
from ChoicesExprInstrument import getCombCategories


class CombinationInstrumentDefinition(InstrumentDefinition):

    def OnInit(self, instrument, **kwargs):
        super(CombinationInstrumentDefinition, self).OnInit(instrument, **kwargs)

    def Attributes(self):
        
        attributes = super(CombinationInstrumentDefinition, self).Attributes()
        
        attributes['factor']                    = Object( label='Index factor',
                                                          objMapping=self._instrument+'.Factor')
                                                          
        attributes['historicalDividendSource']  = Object( label='Hist Source',
                                                          objMapping=self._instrument+'.HistoricalDividendSource',
                                                          visible='@IsShowModeInstrumentDetail')                                                                
        attributes['physicalContractSize']      = Object( label='Fut Contr Size',
                                                          objMapping=self._instrument+'.PhysicalContractSize')
    
        attributes['combinationCategoryChlIem'] = Object( label='Comb Category',
                                                          objMapping=self._instrument+'.CombinationCategoryChlIem',
                                                          choiceListSource=getCombCategories())

        attributes['underlyings']               = Object( label='Underlying Instruments',
                                                          objMapping=self._instrument+'.InstrumentMaps',
                                                          columns=self.UniqueCallback('@ListColumns'),
                                                          onSelectionChanged=self.UniqueCallback('@SetSelectedUnderlying'),
                                                          dialog=AttributeDialog( label='Edit Combination Link', 
                                                          customPanes=self.UniqueCallback('@EditDialogCustomPanes')))
                                                          #onRightClick = ContextMenu(self.UniqueCallback('@EditLinkContextMenuItem'), self.UniqueCallback('@RemoveLinkContextMenuItem')) )
     
        attributes['addInstrument']             = SelectInstrumentsDialog( label='Add...',
                                                          objMapping=self.UniqueCallback('InstrumentMapping'))
    
        attributes['removeInstrument']          = Action( label='Remove...',
                                                          action=self.UniqueCallback('@RemoveInstrument'),
                                                          enabled=self.UniqueCallback('@HasSelectedInstrument'))
                                                          
        attributes['editInstrument']            = Action( label='Edit...',
                                                          dialog=AttributeDialog( label='Edit Combination Link', 
                                                            customPanes=self.UniqueCallback('@EditDialogCustomPanes')),
                                                            enabled=self.UniqueCallback('@HasSelectedInstrument'))

        attributes['editDialogDefinition']      = Str(    defaultValue="""
                                                                       selectedCIM_Ins;
                                                                       selectedCIM_FixFxRate;
                                                                       selectedCIM_Weight;
                                                                       selectedCIM_DefaultDate;
                                                                       selectedCIM_AuctioningDate;
                                                                       selectedCIM_SettlementDate;
                                                                       selectedCIM_RecoveryRate;
                                                                       selectedCIM_RestructuringType;
                                                                       """)
                                                   
            # Attributes part of dialog, showing the Combination Instrument Map (CIM)
        attributes['selectedCIM']                   = Object( defaultValue=acm.FCombInstrMap(),
                                                          domain='FCombInstrMap')
    
        attributes['selectedCIM_Ins']               = Object( label='Instrument',
                                                          objMapping=self.UniqueCallback('SelectedCombInstrMap')+'.Instrument',
                                                          enabled=False,
                                                          choiceListSource=[])
    
        attributes['selectedCIM_FixFxRate']         = Object( label='Fix Fx Rate',
                                                          formatter='SixDecimalDetailed',
                                                          objMapping=self.UniqueCallback('SelectedCombInstrMap')+'.FixFxRate',
                                                          domain='double')
    
        attributes['selectedCIM_Weight']            = Object( label='Weight',
                                                          objMapping=self.UniqueCallback('SelectedCombInstrMap')+'.Weight',
                                                          formatter='SixDecimalDetailed',
                                                          domain='double')
                                                          
        attributes['selectedCIM_DefaultDate']       = Object( label='Default Date',
                                                          objMapping=self.UniqueCallback('SelectedCombInstrMap')+'.DefaultDate',
                                                          transform=self.UniqueCallback('@TransformPeriodToDate'),
                                                          domain='date')
                                                          
        attributes['selectedCIM_AuctioningDate']    = Object( label='Auctioning Date',
                                                          objMapping=self.UniqueCallback('SelectedCombInstrMap')+'.AuctioningDate',
                                                          transform=self.UniqueCallback('@TransformPeriodToDate'),
                                                          domain='date')
                                                          
        attributes['selectedCIM_SettlementDate']    = Object( label='Settlement Date',
                                                          objMapping=self.UniqueCallback('SelectedCombInstrMap')+'.SettlementDate',
                                                          transform=self.UniqueCallback('@TransformPeriodToDate'),
                                                          domain='date')       

        attributes['selectedCIM_RecoveryRate']      = Object( label='Recovery Rate',
                                                          objMapping=self.UniqueCallback('SelectedCombInstrMap')+'.RecoveryRate',
                                                          formatter='SixDecimalDetailed',
                                                          domain='double') 

        attributes['selectedCIM_RestructuringType'] = Object( label='Restructuring Type',
                                                          objMapping=self.UniqueCallback('SelectedCombInstrMap')+'.RestructuringType',
                                                          choiceListSource=self.UniqueCallback('@RestructuringTypeChoices'))
                                                                
        
        return attributes
 

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #
    
    def TransformExpPeriodToDate(self, attributeName, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Option().ExpiryDateFromPeriod(newDate)
        return newDate
        
    def AddInstrument(self, attrName, instruments):
        if instruments:
            for instrument in instruments:
                self.Instrument().AddInstrument(instrument, 1)  
                self.Instrument().RegisterInStorage()
    
    def RemoveInstrument(self, attrName):
        if self.HasSelectedInstrument():
            self.Instrument().Remove(self.selectedCIM_Ins)  
            self.Instrument().RegisterInStorage()
    
    def SetSelectedUnderlying(self, attrName, selectedObj):
        index = self._BasketMaps().FindString(selectedObj) if selectedObj else -1
        if index >= 0:
            self.selectedCIM = self._BasketMaps()[index]
        else:
            self.selectedCIM = acm.FCombInstrMap()
    
    def EditDialogCustomPanes(self, attrName):
        layout = self.UniqueLayout(
                 self.editDialogDefinition)
        return [{'General' : layout}]
    
    def HasSelectedInstrument(self, *args):
        return self.selectedCIM_Ins != None
        
    def ListColumns(self, *args):
        return [{'methodChain': 'Instrument.VerboseName', 'label': 'Insid'},
                {'methodChain': 'Instrument.InsType',     'label': 'Ins Type'},
                {'methodChain': 'Instrument.Currency',    'label': 'Curr'},
                {'methodChain': 'FixFxRate',              'label': 'Fix FX Rate', 'formatter': 'SixDecimalDetailed'},
                {'methodChain': 'Weight',                 'label': 'Weight', 'formatter': 'SixDecimalDetailed'},
                {'methodChain': 'DefaultDate',            'label': 'Default Date'},
                {'methodChain': 'AuctioningDate',         'label': 'Auctioning Date'},
                {'methodChain': 'SettlementDate',         'label': 'Settlement Date'},
                {'methodChain': 'RecoveryRate',           'label': 'Recovery Rate','formatter': 'SixDecimalDetailed'},
                {'methodChain': 'RestructuringType',      'label': 'Restructuring Type'}]

    def EditLinkContextMenuItem(self, attrName):
        return ContextMenuCommand(commandPath = 'Custom/Edit..', 
                                  dialog = AttributeDialog( label='Edit Combination Link', 
                                                            customPanes='@EditDialogCustomPanes'),
                                  default=True)
                                  
    def RemoveLinkContextMenuItem(self, attrName):
        return ContextMenuCommand(commandPath = 'Custom/Remove', 
                                  invoke = '@RemoveInstrument',
                                  default=False)
                                 
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
       
    def SelectedCombInstrMap(self):
        return self.selectedCIM
    
    def ShowAddInstrumentSelectDialog(self, attrName):
        return UXDialogsWrapper(acm.UX().Dialogs().SelectObjectsInsertItems, acm.FInstrument, True)
    
    def _BasketMaps(self):
        return self.Instrument().InstrumentMaps()
        
    def _GetInsFromBasketMaps(self):
        return [cim.Instrument() for cim in self._BasketMaps()]
        
    def InstrumentMapping(self, value='Reading'):
        if value == 'Reading':
            return self._GetInsFromBasketMaps()
        else:
            for ins in value:
                if ins not in self._GetInsFromBasketMaps():
                    self.AddInstrument('', [ins])
            for cim in self._BasketMaps():
                if cim.Instrument() not in value:
                    self.selectedCIM = cim
                    self.RemoveInstrument('')
    
    # Enabled callbacks
        
    # Visible callbacks
        
    # ChoiceListSource callbacks
    def RestructuringTypeChoices(self, attributeName):
        return acm.FIndexedPopulator(acm.FEnumeration['enum(RestructuringType)'].Enumerators())   
       
    # Transform callbacks
    def TransformPeriodToDate(self, name, date, *args):
        period = acm.Time().PeriodSymbolToDate(date)
        if period:
            date = period
        return date
        
    # OnChanged callbacks
        
    # Util


        
