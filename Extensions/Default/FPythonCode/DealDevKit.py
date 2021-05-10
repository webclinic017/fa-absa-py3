import acm
from DealBase import (DealBase,
    # Attributes
        Action, Bool, CalcVal, Date, DatePeriod, Delegate, Float, Int, Label, Link, List, Object, Set, Str, Text,
    # Choices
        AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, ValGroupChoices, 
    # Exceptions
        DealPackageException, DealPackageUserException,
    # Dialog-related
        DealPackageDialog, UXDialogsWrapper, AttributeDialog, NoButtonAttributeDialog,
    # Command actions
        CommandActionBase, TradeActions, NoTradeActions, CustomActions, CorrectCommand, NovateCommand, CloseCommand, ContextMenu, ContextMenuCommand,
    # Misc
        DealPackageChoiceListSource, Settings, InstrumentSetNew_Filter, InstrumentPart, DealPart, ParseFloat, ParseSuffixedFloat, ReturnDomainDecorator, NoOverride,
    # SalesTradingInteraction
        SalesTradingInteraction
    )
from DealTradeActionCommands import DealCloseCommand, DealCorrectCommand, DealNovateCommand, DealMirrorCommand

@TradeActions( correct = DealCorrectCommand(statusAttr='trade_status', newStatus='FO Confirmed'),
               novate = DealNovateCommand(),
               close  = DealCloseCommand(),
               mirror = DealMirrorCommand(statusAttr='trade_status', newStatus='Simulated'))
class DealDefinition(DealBase):
    ''' Interface for deal definitions. 
        Also see imports in DealPackageDevKit'''
    
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    # =====v=v=v===== Override methods below  =====v=v=v=====
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    
    def OnInit(self):
        ''' Override this method to run code at initiation of a new deal instance.
            For example to initiate member variables.
        '''

    def OnNew(self):
        ''' Use this method to dictate the behaviour when creating a new deal. The 
            method is called after all the attribute default values are registered.
        '''
        
    def OnOpen(self):
        ''' Use this method to dictate the behaviour when Opening an 
            existing deal. For instance to initialize non-objectmapping attributes.
        '''    
    
    def OnCopy(self, originalDeal, anAspectSymbol):
        ''' Use this method to dictate the behaviour when Copying an 
            existing deal. For instance reset deal instance specific values that 
            you don't want to be copied.
        '''     
        
    def OnSave(self, saveConfig):
        ''' Use this method to dictate the behaviour when saving a deal . Possible to return
            an array with objects that should be commited together with the deal.
        '''
        return DealBase.OnSave(self, saveConfig)
    
    def OnDismantle(self):
        ''' Use this method to dictate the behaviour when dismantling a deal package '''
        
    def OnDelete(self, allTrades):
        ''' Use this method to dictate the behaviour when deleting a deal. 
            Return an object or a list of objects that should be deleted.
        '''    
   
    def IsValid(self, exceptionAccumulator, aspect):
        ''' Override this method if Pre-Save Validation should be applied.
            - use exceptionAccumulator object to append validation errors
              e.g.: 
                    if (aTrade.Counterparty() == None):
                        exceptionAccumulator('Missing Counterparty')
            - aspect is used to indicate if instrument package of both packages are validated
              Valid values for aspect are enum(IsValidAspect) as:
              "DealPackage", used to validate both trade and instrument
              "InstrumentPackage", used to validate only the instrument
            - if no validation errors are added to the exceptionAccumulator
              the validation is successful and the save will be successful
        '''
   
    def InstrumentPanes(self):
        ''' Override this method to return FExtensionValue holding the instrument pane layout
        '''
        return None
        
    def TradePanes(self):
        ''' Override this method to return FExtensionValue holding the trade pane layout
        '''
        return None
    
    def AttributeOverrides(self, overrideAccumulator):
        ''' Important: Do not call super-classes. That is handled automatically.
        
            Override this method in order to modify meta data on attributes.
            
            overrideAccumulator:
                Call the object in order to add overrides of meta data on attributes.
                The argument should be a dictionary with,
                    Key: Name of attribute
                    value: Dict where,
                            Key: Meta data key
                            Value: Meta data to be added/replaced
                                
                
            Example:
                def AttributeOverrides(self, overrideAccumulator)
                    # Important: Do not call super-classes. That is handled automatically.
                    overrideAccumulator(
                        {'attrName': dict(label='My New Label',
                                          onChanged='@MyAdditionalCallback'),
                         'compositeAttrName_attrName2': dict(visible=False)
                        }
                    )
        '''
        pass
    
    @classmethod
    def SetUp(cls, definitionSetUp):
        ''' Override this class method to specify additional data needed for deployment, 
            e.g. Additional Info, Choice List, Context Link, Custom Methods. See the 
            Deal Package Examples module for more information .
            
            definitionSetUp:
                Call the method AddSetupItems to add a specification of the 
                additional data needed. E.g:
                                
                definitionSetUp.AddSetupItems( AddInfoSetUp( recordType='DealPackage',
                                                            fieldName='DPEx_Beta',
                                                            dataType='Double',
                                                            description='DealPackageExample Double Test',
                                                            dataTypeGroup='Standard',
                                                            subTypes=[],
                                                            defaultValue=None,
                                                            mandatory=False ) )
        '''
        pass
    
    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====
    # =====^=^=^===== Override methods above  =====^=^=^=====
    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====

    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    # =====v=v=v===== Do not override methods below =v=v=====
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    
    def Instrument(self):
        ''' Return the instrument.
        '''
        return DealBase.Instrument(self)
        
    def Leg(self):
        ''' Return the first leg.
        '''
        return DealBase.Leg(self)
    
    def PayLeg(self):
        ''' Return the first pay leg.
        '''
        return DealBase.PayLeg(self)
    
    def ReceiveLeg(self):
        ''' Return the first pay leg.
        '''
        return DealBase.ReceiveLeg(self)
    
    def Trade(self):
        ''' Return the trade.
        '''
        return DealBase.Trade(self)
    
    def IsShowModeInstrumentDetail(self, *args):    
        ''' Return True if instrument visibility mode is set to Detail 
        '''
        return DealBase.IsShowModeInstrumentDetail(self, args)
        
    def IsShowModeTradeDetail(self, *args):
        ''' Return True if trade visibility mode is set to Detail 
        '''
        return DealBase.IsShowModeTradeDetail(self, args)
    
    def RegisterCallbackOnAttributeChanged(self, callback, attributes = None, last = False):
        ''' Callback will be called when the attribute or attributes listed has been changed.
            If no attribute names are specified, callback will be called for all changes.
            The 'last' argument indicates if the callback should be run before (last=False) 
            or after (last=True) all attribute specific onChanged callbacks.
            NOTE! Registering a callback should be done in OnInit.
        '''
        return DealBase.RegisterCallbackOnAttributeChanged(self, callback, attributes, last)
    
    def SetAttribute(self, name, value, silent=False):
        ''' Set attribute by name'''
        DealBase.SetAttribute(self, name, value, silent)
    
    def SolverColor(self, attrName):
        ''' Method to set a yellow color on attributes that is 
            solverParameter. Only works if attribute has 
            solverParameter set and package contains at least 
            one attribute which is a solverTopValue.
            
            Example:
                mySolverAttr = Float(solverParameter=True,
                                     backgroundColor='@SolverColor')
        '''
        return DealBase.SolverColor(self, attrName)
     
    def GetAttributes(self):
        ''' Return all attributes'''
        return DealBase.GetAttributes(self)
    
    def GetAttribute(self, name):
        ''' Get attribute by name'''
        return DealBase.GetAttribute(self, name)
        
    def GetAttributeMetaData(self, attrName, metaKey):
        ''' Get attribute meta data by name.
            Returns a callback to the metaData of a given attribute
        '''
        return DealBase.GetAttributeMetaData(self, attrName, metaKey)
        
    def GetAttributeMetaDataKeys(self):
        ''' Returns the meta data keys available for attributes'''
        return DealBase.GetAttributeMetaDataKeys(self)
    
    def Confirmations(self):
        ''' Get all confirmations in the deal'''    
        return DealBase.Confirmations(self)
        
    def Settlements(self):
        ''' Get all settlements in the deal'''    
        return DealBase.Settlements(self)    

    def B2BTradeParamsAt(self, name):
        ''' Get B2B part'''
        return DealBase.B2BTradeParamsAt(self, name)
        
    def DeltaHedgeParamsAt(self, name):
        ''' Get delta hedge part'''
        return DealBase.DeltaHedgeParamsAt(self, name)

    def CreateCalculation(self, name, calcInfo, configurationCb = None):
        ''' Create a new calculation. These are 'additional'
            calculations that can be used to calculate ad-hoc values when needed. 
            
            name:    
                The id of this calculation
                    
            calcInfo:
                Description of the calculation with the syntax 
                'CalcObjectMethodName:SheetName:ColumnName' in the same way as when 
                using CalcVal attributes.
                    
            configurationCb (optional):
                A method that returns an FCalculationConfiguration object in the
                same way as when using CalcVal attributes.
                    
            Note:   
                Use CalcVal attribute instead if the calculation is going to
                be presented as a calculation field in a UI. This will make it 
                possible to access the valuation information, solver functionality
                and simulation capabilities.
            
            Example:
                self.CreateCalculation('strikeCalc', 'MyTrade:FDealSheet:Strike Price')
            
                def MyTrade(self):
                    return self.TradeAt('myTrade')
                
        '''
        DealBase.CreateCalculation(self, name, calcInfo, configurationCb)

    def RemoveCalculation(self, name):
        ''' Remove a calculation.
        
            name:
                The id of the calculation that should be removed
        
            Example:
                self.RemoveCalculation('strikeCalc')
        '''
        DealBase.RemoveCalculation(self, name)

    def GetCalculation(self, name):
        ''' Get the FCalculation object for a calculation.
        
            name:
                The id of the calculation that should be retrieved
        
            Example:
                calc = self.GetCalculation('strikeCalc')
                return calc.FormattedValue()
                
        '''
        return DealBase.GetCalculation(self, name)

    def SimulateCalculation(self, name, newValue):
        ''' Simulate a calculation.
            
            name:
                The id of the calculation that should be simulated.
                
            newValue:
                The value that should be simulated for the calculation.
                To unsimulate, set newValue to an empty string.
            
            Example:
                self.SimulateCalculation('strikeCalc', 47)
            
        '''
        DealBase.SimulateCalculation(self, name, newValue)

    def IsCalculationSimulated(self, name):
        ''' Returns True if calculation is simulated, else False.
        
            name:
                The id of the calculation for which the simulation status
                should be retrieved
        
            Example:
                isSimulated = self.IsCalculationSimulated('strikeCalc')
        '''
        return DealBase.IsCalculationSimulated(self, name)
    
    def GetSimulatedCalculationValue(self, name):
        ''' Returns the simulated value of calculation. This is the actual
            value that was set as newValue in SimulateCalculation and it 
            might be different than the value retieved by a call to 
            GetCalculation().Value() due to formatting of the calculation.
        
            name:
                The id of the calculation for which the simulated value
                should be retrieved
                
            Example:
                simulatedValue = self.GetSimulatedCalculationValue('strikeCalc')
        '''
        return DealBase.GetSimulatedCalculationValue(self, name)
        
    def RemoveAllSimulations(self):
        ''' Remove all simulations on all simulated attributes.
                
            Example:
                self.RemoveAllSimulations()
        '''    
        return DealBase.RemoveAllSimulations(self)
    
    

    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====
    # =====^=^=^===== Do not override methods above =^=^=====
    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====

    # *- Eso es todo amigos... -*
