
import acm
import FUxCore
from DealPackageDevKit import DealPackageDefinition, DealPackageException, DealPackageUserException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, Text, DatePeriod, DealPackageChoiceListSource, CompositeAttributeDefinition, ValGroupChoices, InstrumentPart, AttributeDialog, UXDialogsWrapper, ContextMenu, ContextMenuCommand
from SP_DealPackageHelper import GetFxFormatter

from CompositeComponentBase import CompositeBaseComponent
from functools import partial

# ###############################################################
# Columns displayed per comb link configurable when creating object
# Edit dialog fields decided dynamically based on comb link columns
# Edit button only visible if at least one editable column (i.e. field directly on combination link record)
# ###############################################################

class Basket(CompositeBaseComponent):

    # ############################################
    # Dev kit methods
    # ############################################

    def Attributes(self):
        attributes =  { 

            'instruments'            : Object( objMapping = InstrumentPart(self._instrumentName + '.InstrumentMaps'),
                                               label = self.UniqueCallback("@LabelInstruments"),
                                               toolTip = self.UniqueCallback("@ToolTipInstruments"),
                                               columns=self.UniqueCallback('@DisplayColumns'),
                                               onSelectionChanged=self.UniqueCallback('@SetSelectedUnderlying'),
                                               dialog=AttributeDialog( label='Edit Basket Link', 
                                                                       customPanes=self.UniqueCallback('@EditDialogCustomPanes')),
                                               onRightClick = ContextMenu(self.UniqueCallback('@EditLinkContextMenuItem'), 
                                                                          self.UniqueCallback('@RemoveLinkContextMenuItem') ) ),
                                                                          
            'instrumentPrices'       : CalcVal(calcMapping = self.UniqueCallback('InstrumentsAsLot') + ':FDealSheet:Instrument Market Price'),

            'addInstrument'          : Action( label = "Add...",
                                               dialog=self.UniqueCallback('@ShowAddInstrumentSelectDialog'),
                                               action=self.UniqueCallback('@AddInstrument')),
            
            'removeInstrument'       : Action( label = "Remove",
                                               action=self.UniqueCallback('@RemoveInstrument'),
                                               enabled=self.UniqueCallback('@HasSelectedInstrument')),
                                            
            'editInstrument'         : Action( label = 'Edit...',
                                               dialog=AttributeDialog( label='Edit Combination Link', 
                                                                       customPanes=self.UniqueCallback('@EditDialogCustomPanes')),
                                               enabled=self.UniqueCallback('@HasSelectedInstrument'),
                                               visible = self.UniqueCallback('@CombMapColumnsExist'),
                                               action = self.UniqueCallback('@EditInstrument') ),
                                               
            'updateWeights'          : Action( label = 'Update Weights',
                                               action = self.UniqueCallback('@UpdateWeights'),
                                               enabled = self.UniqueCallback('@HasInstruments'),
                                               visible = self.UniqueCallback('@BasketValue')),
                                            
            # Attributes part of dialog, showing the Combination Instrument Map (CIM)
            'selectedCIM'            : Object( defaultValue=acm.FCombInstrMap(),
                                               domain='FCombInstrMap'),
            
            'selectedCIM_Ins'        : Object( label='Instrument',
                                               objMapping=self.UniqueCallback('SelectedCombInstrMap') + '.Instrument',
                                               enabled=False,
                                               choiceListSource=[])
        }
            
        # Create attributes based on the actual columns displayed...
        for column in self.CombMapColumns():
            attributeName = 'selectedCIM_%s' % (column['methodChain'])

            attributes[attributeName] = Object( objMapping  = self.UniqueCallback('SelectedCombInstrMap') + '.' + column['methodChain'],
                                                label       = column.get('label', column['methodChain']),
                                                onChanged   = self.UniqueCallback('@PerformTouch'),
                                                formatter   = column.get('formatter', None) )

        return attributes

    def OnInit(self, basketName, displayColumns = None, basketUpdateAction = None, totalBasketValue = None, **kwargs):
        self._instrumentName = basketName
        self._displayColumns = displayColumns
        self._basketUpdateAction = basketUpdateAction
        self._totalBasketValue = totalBasketValue

    def LabelInstruments(self, attrName, *rest):
        if attrName.find('underlying') >= 0:
            return 'Underlying instruments'
        else:
            return 'Instruments'

    def ToolTipInstruments(self, attrName, *rest):
        if attrName.find('underlying') >= 0:
            return 'Underlying instruments'
        else:
            return 'Instruments'

    def BasketUpdateAction(self, attrName, instruments = None):
        if self._basketUpdateAction is not None:
            self.GetMethod(self._basketUpdateAction)(attrName, instruments)

    def GetLayout(self):
        return self.UniqueLayout(
               """
                hbox(;
                    instruments;
                    vbox{;
                        addInstrument;
                        removeInstrument;
                        editInstrument;
                        fill;
                        updateWeights;
                    };
                );
                """ )

    def Basket(self):
        return self.GetMethod(self._instrumentName)()

    # ############################################
    # Methods needed for composite compoents
    # ############################################
    @classmethod
    def CreateInstrument(cls, insType = 'EquityIndex'):
        if insType not in ('EquityIndex', 'Combination'):
            raise DealPackageException ('Equity Index and Combination are the only allowed instrument types when creating a basket')
        ins = acm.DealCapturing().CreateNewInstrument(insType)
        ins.MtmFromFeed(False)
        return ins

    # ############################################
    # Methods for handling the grid columns
    # ############################################

    def CombMapColumns(self):
        combMapColumns = []
        for column in self.DisplayColumns():
            methodChain = column['methodChain']
            if len(methodChain.split('.')) == 1:
                combMapColumns.append(column)
        return combMapColumns

    def DefaultColumns(self):
        return [{'methodChain': 'Instrument.VerboseName', 'label': 'Instrument'},
                {'methodChain': 'Instrument.InsType',     'label': 'InsType'},
                {'methodChain': 'Instrument.Currency',    'label': 'InsCurrency'},
                {'methodChain': 'FixFxRate',              'label': 'FXRate'},
                {'methodChain': 'Weight',                 'label': 'Weight'}]

    def DisplayColumns(self, *rest):
        if self._displayColumns is not None:
            return self._displayColumns
        else:
            return self.DefaultColumns()

    def _BasketMaps(self):
        return self.Basket().InstrumentMaps()

    def ShowAddInstrumentSelectDialog(self, attrName):
        return UXDialogsWrapper(acm.UX().Dialogs().SelectObjectsInsertItems, acm.FInstrument, True)

    def SelectedCombInstrMap(self):
        return self.selectedCIM

    # ###################################
    # Attribute callbacks
    # ###################################

    def PerformTouch(self, *rest):
        self.GetMethod('DealPackage')().Touch()
        self.GetMethod('DealPackage')().Changed()

    def AddInstrument(self, attrName, instruments):
        if instruments:
            for ins in instruments:
                map = self.Basket().AddInstrument(ins, 1)
                map.FixFxRate(1.0)
                self.Basket().RegisterInStorage()
            self.PerformTouch()
            self.BasketUpdateAction(attrName, instruments)
    
    def RemoveInstrument(self, attrName):
        if self.HasSelectedInstrument():
            selectedIns = self.selectedCIM_Ins
            self.Basket().Remove(selectedIns)
            self.Basket().RegisterInStorage()
            self.PerformTouch()
            self.BasketUpdateAction(attrName, selectedIns)

    def EditInstrument(self, attrName, *rest):
        self.BasketUpdateAction(attrName, self.selectedCIM_Ins)

    def CombMapColumnsExist(self, attrName):
        return len(self.CombMapColumns()) != 0

    def SetSelectedUnderlying(self, attrName, selectedObj):
        index = self._BasketMaps().FindString(selectedObj) if selectedObj else -1
        if index >= 0:
            self.selectedCIM = self._BasketMaps()[index]
        else:
            self.selectedCIM = acm.FCombInstrMap()

    def EditDialogCustomPanes(self, attrName):
        layoutString = "selectedCIM_Ins;" + ';'.join(['selectedCIM_%s' % col['methodChain'] for col in self.CombMapColumns()])
        return [{'General' : self.UniqueLayout(layoutString)}]

    def EditLinkContextMenuItem(self, attrName):
        return ContextMenuCommand(commandPath = 'Custom/Edit..', 
                                  dialog      = AttributeDialog( label       = 'Edit Combination Link', 
                                                                 customPanes = self.UniqueCallback('@EditDialogCustomPanes')),
                                  default     = True,
                                  applicable  = self.UniqueCallback('@CombMapColumnsExist'),
                                  enabled     = self.UniqueCallback('@HasSelectedInstrument') )

    def RemoveLinkContextMenuItem(self, attrName):
        return ContextMenuCommand(commandPath = 'Custom/Remove', 
                                  invoke      = self.UniqueCallback('@RemoveInstrument'),
                                  default     = False,
                                  enabled     = self.UniqueCallback('@HasSelectedInstrument') )

    def HasSelectedInstrument(self, *args):
        return self.selectedCIM_Ins!= None
        
    def BasketValue(self, *args):
        return self._totalBasketValue and getattr(self.Owner(), self._totalBasketValue) 

    def HasInstruments(self, *args):
        return bool(self._BasketMaps())
        
    def InstrumentsAsLot(self, *args):
        return acm.FLot([insMap.Instrument() for insMap in self._BasketMaps()])
    
    def UpdateWeights(self, *args):
        if self.HasInstruments():
            constituentValue = self.BasketValue() / len(self._BasketMaps())
            for insMap, price in zip(self._BasketMaps(), getattr(self.Owner(), self.PrefixedName('instrumentPrices')).Value()):
                ins = insMap.Instrument()
                if price.Number():
                    weight = constituentValue / price.Number()
                    if str(price.Unit()) != self.Basket().Currency().Name():
                        fxRate = self.Basket().Currency().Calculation().FXRate(self.Owner()._GetStdCalcSpace(), price.Unit())
                        weight *=  fxRate.Number()
                    insMap.Weight = weight
            self.PerformTouch()
        

