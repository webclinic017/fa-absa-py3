import acm
from DealPackageDevKit import DealPackageDefinition, Object, Action, Text, Settings, AttributeDialog, UXDialogsWrapper, ContextMenu, ContextMenuCommand
from inspect import cleandoc

@Settings(GraphApplicable=False, 
          SheetApplicable=True)       
class AddStocksToBasket(DealPackageDefinition):
    """
    Example showing how to work with more complex structures. 
    This example consist of:
        - A Combination with a Trade
        - An Option is put into the Combination
        - An Equity Index is put as underlying to the Option
        - The constituents of the Equity Index is added on the fly
    """
    ipName                = Object( label='Name',
                                    objMapping='InstrumentPackage.Name') 
                                
    currency              = Object( label='Currency',
                                    objMapping='Combination.Currency|Option.Currency|Option.StrikeCurrency|Basket.Currency|Trade.Currency')

    expiryDate            = Object( defaultValue='3m',
                                    label='Option Expiry',
                                    objMapping='Option.ExpiryDate',
                                    transform='@TransformExpPeriodToDate')

    underlyings           = Object( label='Underlying Basket',
                                    objMapping='Basket.InstrumentMaps',
                                    columns='@ListColumns',
                                    onSelectionChanged='@SetSelectedUnderlying',
                                    dialog=AttributeDialog( label='Edit Combination Link', 
                                                            customPanes='@EditDialogCustomPanes'),
                                    onRightClick = ContextMenu('@EditLinkContextMenuItem', '@RemoveLinkContextMenuItem') )

    addStock              = Action( label='Add...',
                                    dialog='@ShowAddStockSelectDialog',
                                    action='@AddStock')
    
    removeStock           = Action( label='Remove',
                                    action='@RemoveStock',
                                    enabled='@HasSelectedStock')
                                    
    editStock             = Action( label='Edit...',
                                    dialog=AttributeDialog( label='Edit Combination Link', 
                                                            customPanes='@EditDialogCustomPanes'),
                                    enabled='@HasSelectedStock')
                                    
    # Attributes part of dialog, showing the Combination Instrument Map (CIM)
    selectedCIM           = Object( defaultValue=acm.FCombInstrMap(),
                                    domain='FCombInstrMap')
    
    selectedCIM_Stock     = Object( label='Stock',
                                    objMapping='SelectedCombInstrMap.Instrument',
                                    enabled=False,
                                    choiceListSource=[])
    
    selectedCIM_FixFxRate = Object( label='Fix Fx Rate',
                                    objMapping='SelectedCombInstrMap.FixFxRate',
                                    domain='double')
    
    selectedCIM_Weight    = Object( label='Weight',
                                    objMapping='SelectedCombInstrMap.Weight',
                                    domain='double')

    doc                   = Text(   defaultValue=cleandoc(__doc__),
                                    editable=False,
                                    width=430,
                                    height=110)
    
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    
    def AssemblePackage(self):
        def CreateBasket():
            basket = acm.DealCapturing().CreateNewInstrument('Equity Index') 
            basketDeco = acm.FBusinessLogicDecorator.WrapObject(basket)
            basketDeco.Currency('EUR')            
            basketDeco.Name(basketDeco.SuggestName())
            return basket
            
        def CreateOption(basket):
            option = acm.DealCapturing().CreateNewInstrument('Option')
            optionDeco = acm.FBusinessLogicDecorator.WrapObject(option)
            optionDeco.Underlying(basket)
            optionDeco.Currency('EUR')
            optionDeco.Name(optionDeco.SuggestName())
            return option
            
        combTradeDeco = self.DealPackage().CreateTrade('Combination', 'comb') 
        basket = CreateBasket()
        option = CreateOption(basket)
        self.DealPackage().AddCombinationMap(option, 1, 'option', 'comb')
            
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_AddStocksToBasket_DPE')
    
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #
    
    def TransformExpPeriodToDate(self, attributeName, newDate):
        if acm.Time().PeriodSymbolToDate(newDate):
            newDate = self.Option().ExpiryDateFromPeriod(newDate)
        return newDate
        
    def AddStock(self, attrName, stocks):
        if stocks:
            for stock in stocks:
                self.Basket().AddInstrument(stock, 1)  
                self.Basket().RegisterInStorage()
    
    def RemoveStock(self, attrName):
        if self.HasSelectedStock():
            self.Basket().Remove(self.selectedCIM_Stock)  
            self.Basket().RegisterInStorage()
    
    def SetSelectedUnderlying(self, attrName, selectedObj):
        index = self._BasketMaps().FindString(selectedObj) if selectedObj else -1
        if index >= 0:
            self.selectedCIM = self._BasketMaps()[index]
        else:
            self.selectedCIM = acm.FCombInstrMap()
    
    def EditDialogCustomPanes(self, attrName):
        return [{'General' : """
                                selectedCIM_Stock;
                                selectedCIM_FixFxRate;
                                selectedCIM_Weight;
                 """}]
    
    def HasSelectedStock(self, *args):
        return self.selectedCIM_Stock != None
        
    def ListColumns(self, *args):
        return [{'methodChain': 'Instrument.VerboseName', 'label': 'InsName'},
                {'methodChain': 'Instrument.Currency',    'label': 'InsCurrency'},
                {'methodChain': 'FixFxRate',              'label': 'FXRate'},
                {'methodChain': 'Weight',                 'label': 'Weight', 'formatter': 'Imprecise'}]

    def EditLinkContextMenuItem(self, attrName):
        return ContextMenuCommand(commandPath = 'Custom/Edit..', 
                                  dialog = AttributeDialog( label='Edit Combination Link', 
                                                            customPanes='@EditDialogCustomPanes'),
                                  default=True)
                                  
    def RemoveLinkContextMenuItem(self, attrName):
        return ContextMenuCommand(commandPath = 'Custom/Remove', 
                                  invoke = '@RemoveStock',
                                  default=False)
                                 
    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def Combination(self):
        return self.InstrumentAt('comb')
    
    def Basket(self):
        return self.Option().Underlying()
        
    def Option(self):
        return self.InstrumentAt('option')
        
    def Trade(self):
        return self.TradeAt('comb')
        
    def SelectedCombInstrMap(self):
        return self.selectedCIM
    
    def ShowAddStockSelectDialog(self, attrName):
        return UXDialogsWrapper(acm.UX().Dialogs().SelectObjectsInsertItems, acm.FStock, True)
    
    def _BasketMaps(self):
        return self.Basket().InstrumentMaps()
        
