import acm
import ChoicesExprInstrument
from DealPackageUtil import SetNew, SetSave
from DealPackageBase import (DealPackageBase,
    # Attributes
        Action, Bool, Box, CalcVal, Date, DatePeriod, Delegate, Float, Int, Label, Link, List, Object, Set, Str, Text,
    # Choices
        AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, ValGroupChoices, 
    # Exceptions
        DealPackageException, DealPackageUserException,
    # Dialog-related
        DealPackageDialog, UXDialogsWrapper, AttributeDialog, NoButtonAttributeDialog,
    # Command actions
        CommandActionBase, TradeActions, NoTradeActions, CustomActions, CorrectCommand, NovateCommand, CloseCommand, MirrorCommand, ContextMenu, ContextMenuCommand,
    # CompositeAttributeDefinition
        CompositeAttributeDefinition,
    # Misc
        DealPackageChoiceListSource, Settings, InstrumentSetNew_Filter, InstrumentPart, DealPart, ParseFloat, ParseSuffixedFloat, ReturnDomainDecorator, NoOverride,
    # SalesTradingInteraction
        SalesTradingInteraction
    )


class DealPackageDefinition(DealPackageBase):
    ''' Interface for dealpackage definitions'''
    
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    # =====v=v=v===== Override methods below  =====v=v=v=====
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    
    def LeadTrade(self):
        ''' Override this method to enable support for having a lead trade in the deal package.
            For example for usage in down stream reporting, confirmations etc.
        '''
        
    def OnInit(self):
        ''' Override this method to run code at initiation of a new DealPackageDefinition instance.
            For example to initiate member variables.
        '''

    def AssemblePackage(self, optArg = None):
        ''' Override this method to return the default structure of 
            the deal package after creation.
        '''
        
    def OnNew(self):
        ''' Use this method to dictate the behaviour when creating a new Deal Package. The 
            method is called after all the attribute default values are registered.
        '''
        
    def OnOpen(self):
        ''' Use this method to dictate the behaviour when Opening an 
            existing Deal Package. For instance to initialize non-objectmapping attributes.
        '''    
    
    def OnCopy(self, originalDealPackage, anAspectSymbol):
        ''' Use this method to dictate the behaviour when Copying an 
            existing Deal Package. For instance reset dealpackage instance specific values that 
            you don't want to be copied.
        '''        

    def OnSave(self, saveConfig):
        ''' Use this method to dictate the behaviour when saving deal package. Possible to return
            an array with objects that should be commited together with the dealpackage.
        '''
        saveTrades = []
        saveInstruments = []
        saveDealPackages = []
        saveInstrumentPackages = []
        saveAsNewTrades = []
        saveAsNewInstruments = []
        saveAsNewDealPackages = []
        saveAsNewInstrumentPackages = []
        
        if saveConfig.InstrumentPackage() == "SaveNew":
            saveAsNewInstruments = self.Instruments().Filter( InstrumentSetNew_Filter )
            saveAsNewInstrumentPackages = self.DealPackage().InstrumentPackage().ChildInstrumentPackages()
        elif saveConfig.InstrumentPackage() == "Save":
            saveInstruments = self.Instruments()
            saveInstrumentPackages = self.DealPackage().InstrumentPackage().ChildInstrumentPackages()
        if saveConfig.DealPackage() == "SaveNew" or saveConfig.InstrumentPackage() == "SaveNew":
            saveAsNewDealPackages = self.ChildDealPackages()
            saveAsNewTrades = self.Trades()
        elif saveConfig.DealPackage() == "Save":
            saveDealPackages = self.ChildDealPackages()
            saveTrades = self.Trades()
            
        SetSave( saveTrades,
                 saveInstruments,
                 saveDealPackages,
                 saveInstrumentPackages)
                     
        SetNew( saveAsNewTrades,
                saveAsNewInstruments,
                saveAsNewDealPackages,
                saveAsNewInstrumentPackages)
    
    def OnDismantle(self):
        ''' Use this method to dictate the behaviour when dismantling a deal package '''
    
    def IsLiveTrade(self, trade):
        ''' Use this method to filter which trades are to be included in Trade actions. The filter is
            also applied when using the method LiveTrades in the definition interface.
        '''
        return True
    
    def OpenAfterSave(self, config):
        ''' Override this method to dictate what deal package(s) to open after a succecssfull save.
        '''        
        return self.DealPackage()

    def OnDelete(self, allTrades):
        ''' Use this method to dictate the behaviour when deleting a deal package. 
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
              "DealPackage", used to validate both deal package and instrument package
              "InstrumentPackage", used to validate only the instrument package
            - if no validation errors are added to the exceptionAccumulator
              the validation is successful and the save will be successful
        '''
        
    def SuggestName(self):
        ''' Use this method return a suggested name for the instrument package '''
        
    def Refresh(self):
        ''' Called on any attribute change, and is good for smaller tasks that you need to do
            for many attributes. Avoid heavy calculations and performance intensive tasks here
            since the callback will be called often.
        '''
    
    def CustomPanes(self):
        ''' Return list of panes'''
        return []

    def GraphYValues(self, xValues):
        ''' Return a list of y-values, given x-values, used for Graph population.
            Used when overriding y-values.
            For example [1, 2, 3, 4, 5, 6].
        '''
        return DealPackageBase.GraphYValues(self, xValues)
        
    def GraphXValues(self):
        ''' Return a list of x-values used for Graph population.
            Used when overriding x values.
            For example [4, 8, 15, 16, 23, 42].
        '''
        return DealPackageBase.GraphXValues(self)
        
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
    
    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====
    # =====^=^=^===== Override methods above  =====^=^=^=====
    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====

    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    # =====v=v=v===== Do not override methods below =v=v=====
    # =====v=v=v=====v=v=v=====v=v=v=====v=v=v=====v=v=v=====
    
    def DealPackage(self):
        ''' Returns deal package instance'''
        return DealPackageBase.DealPackage(self)
    
    def RegisterCallbackOnAttributeChanged(self, callback, attributes = None, last=False):
        ''' Callback will be called when the attribute or attributes listed has been changed.
            If no attribute names are specified, callback will be called for all changes.
            The 'last' argument indicates if the callback should be run before (last=False) 
            or after (last=True) all attribute specific onChanged callbacks.
            NOTE! Registering a callback should be done in OnInit.
        '''
        return DealPackageBase.RegisterCallbackOnAttributeChanged(self, callback, attributes, last)
    
    def SetAttribute(self, name, value, silent=False):
        ''' Set attribute by name'''
        DealPackageBase.SetAttribute(self, name, value, silent)
    
    def GetCustomPanesFromExtValue(self, *panesName):
        ''' Used together with "CustomPanes" to define pane layout using FExtensionValue
            similar to how the layout in "Instrument Definition" app is done.
            Example:
                def CustomPanes(self):
                    return self.GetCustomPanesFromExtValue("CustomPanes_MyDealPackage")
        '''
        return DealPackageBase.GetCustomPanesFromExtValue(self, *panesName)
    
    def IsShowModeDetail(self, *args):
        ''' Returns True if show mode is detailed, else (when show mode is slim) False'''
        return DealPackageBase.IsShowModeDetail(self, *args)
    
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
        DealPackageBase.CreateCalculation(self, name, calcInfo, configurationCb)

    def RemoveCalculation(self, name):
        ''' Remove a calculation.
        
            name:
                The id of the calculation that should be removed
        
            Example:
                self.RemoveCalculation('strikeCalc')
        '''
        DealPackageBase.RemoveCalculation(self, name)

    def GetCalculation(self, name):
        ''' Get the FCalculation object for a calculation.
        
            name:
                The id of the calculation that should be retrieved
        
            Example:
                calc = self.GetCalculation('strikeCalc')
                return calc.FormattedValue()
                
        '''
        return DealPackageBase.GetCalculation(self, name)

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
        DealPackageBase.SimulateCalculation(self, name, newValue)

    def IsCalculationSimulated(self, name):
        ''' Returns True if calculation is simulated, else False.
        
            name:
                The id of the calculation for which the simulation status
                should be retrieved
        
            Example:
                isSimulated = self.IsCalculationSimulated('strikeCalc')
        '''
        return DealPackageBase.IsCalculationSimulated(self, name)
    
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
        return DealPackageBase.GetSimulatedCalculationValue(self, name)
        
    def RemoveAllSimulations(self):
        ''' Remove all simulations on all simulated attributes.
                
            Example:
                self.RemoveAllSimulations()
        '''    
        return DealPackageBase.RemoveAllSimulations(self)
    
    def Log(self):
        ''' To ease the development and error investigations in production it 
            often help to print log messages. See Deal Package Settings 
            in AEF Browser.

            Example:
                self.Log().Verbose("This text is logged")
                self.Log().Warning("This text is logged")
                self.Log().Error("This text is logged")
        '''
        return DealPackageBase.Log(self)
    
    def RestoreDefaultValues(self, *attributeNames):
        ''' Restores the provided attributes to its default value
            
            Example:
                self.RestoreDefaultValues('price', 'quantity')
        '''
        DealPackageBase.RestoreDefaultValues(self, *attributeNames)
        
    def SolverColor(self, attrName):
        ''' Method to set a yellow color on attributes that is 
            solverParameter. Only works if attribute has 
            solverParameter set and package contains at least 
            one attribute which is a solverTopValue.
            
            Example:
                mySolverAttr = Float(solverParameter=True,
                                     backgroundColor='@SolverColor')
        '''
        return DealPackageBase.SolverColor(self, attrName)
    
    def GetAttributes(self):
        ''' Return all attributes'''
        return DealPackageBase.GetAttributes(self)
    
    def GetAttribute(self, name):
        ''' Get attribute by name'''
        return DealPackageBase.GetAttribute(self, name)
        
    def GetAttributeMetaData(self, attrName, metaKey):
        ''' Get attribute meta data by name.
            Returns a callback to the metaData of a given attribute
        '''
        return DealPackageBase.GetAttributeMetaData(self, attrName, metaKey)
        
    def GetAttributeMetaDataKeys(self):
        ''' Returns the meta data keys available for attributes'''
        return DealPackageBase.GetAttributeMetaDataKeys(self)
    
    def Trades(self):
        ''' Get all trades in dealpackage'''
        return DealPackageBase.Trades(self)
        
    def Instruments(self):
        ''' Get all instruments in dealpackage'''
        return DealPackageBase.Instruments(self)
        
    def Confirmations(self):
        ''' Get all confirmations in the deal package'''    
        return DealPackageBase.Confirmations(self)
        
    def Settlements(self):
        ''' Get all settlements in the deal package'''    
        return DealPackageBase.Settlements(self)    
    
    def ChildDealPackages(self):
        ''' Get all child dealpackages in dealpackage'''
        return DealPackageBase.ChildDealPackages(self)
    
    def OpeningDealPackages(self):
        ''' Get all opening child dealpackages in dealpackage'''
        return DealPackageBase.OpeningDealPackages(self)
    
    def LifeCyclePackages(self):
        ''' Get all life cycle event child dealpackages in dealpackage'''
        return DealPackageBase.LifeCyclePackages(self)
    
    def InstrumentAt(self, name):
        ''' Get instrument part'''
        return DealPackageBase.InstrumentAt(self, name)
        
    def TradeAt(self, name):
        ''' Get trade part'''
        return DealPackageBase.TradeAt(self, name)
    
    def CombinationMapAt(self, name, combinationKey = None):
        ''' Get CombinationMap part'''
        return DealPackageBase.CombinationMapAt(self, name, combinationKey)

    def B2BTradeParamsAt(self, name):
        ''' Get B2B part'''
        return DealPackageBase.B2BTradeParamsAt(self, name)
        
    def DeltaHedgeParamsAt(self, name):
        ''' Get delta hedge part'''
        return DealPackageBase.DeltaHedgeParamsAt(self, name)
        
    def ChildDealPackageAt(self, name):
        ''' Get child dealpackage part'''
        return DealPackageBase.ChildDealPackageAt(self, name)
    
    def CloseDialog(self):
        ''' Programatic Close of Deal Package Dialog from Python code'''
        return DealPackageBase.CloseDialog(self)

    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====
    # =====^=^=^===== Do not override methods above =^=^=====
    # =====^=^=^=====^=^=^=====^=^=^=====^=^=^=====^=^=^=====

    # *- That's all folks... -*
            
