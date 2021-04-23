
import acm
import re
from TraitBasedDealPackage import TraitBasedDealPackage, SetSolverParametersWithSafeExit, Date, DatePeriod, Str, Object, Float, Bool, Box, Int, CalcVal, List, Set, Delegate, Action, Text, Label, Link
from DealPackagePayoffGraphCalculations import PayoffGraphCalculations
from DealPackageUtil import NoChange, UnpackPaneInfo, WrapAsTabControlList
from collections import OrderedDict

# Needed for DevKit
from AttributeMetaData import AcquirerChoices, CounterpartyChoices, PortfolioChoices, TradeStatusChoices, ValGroupChoices, AttributeDialog, NoButtonAttributeDialog, ContextMenu, ContextMenuCommand, NoOverride
from DealPackageUtil import DealPackageException, DealPackageUserException, Settings, InstrumentSetNew_Filter, InstrumentPart, DealPart, ParseFloat, ParseSuffixedFloat, ReturnDomainDecorator, SalesTradingInteraction
from DealPackageDialog import DealPackageDialog, UXDialogsWrapper
from DealPackageCommandActionUtils import CommandActionBase, TradeActions, NoTradeActions, CustomActions
from CompositeAttributeDevKit import CompositeAttributeDefinition 
from DealPackageTradeActionCommands import CorrectCommand, NovateCommand, CloseCommand, MirrorCommand


class DealPackageBase(TraitBasedDealPackage):
    
    # Global traits needed fo ALL trait based Deal Packages
    autoRefreshCalc =              Bool(   noDealPackageRefreshOnChange=True )
    refreshCalcCounter =           Int(    onChanged='@_OnRefreshCalcCounterChanged' ) # Apply refresh when changed
    sheetNeedsRefresh =            Bool(   noDealPackageRefreshOnChange=True,
                                           silent=True)
    sheetDefaultColumns =          List(   noDealPackageRefreshOnChange=True )
    multiTradingEnabled =          Bool(   noDealPackageRefreshOnChange=True )
    graphCoordinatesNeedsRefresh = Bool(   noDealPackageRefreshOnChange=True,
                                           silent=True )
    graphCoordinates =             Action( action='@_GraphCoordinates',
                                           noDealPackageRefreshOnChange=True )
    customPanes =                  List(   noDealPackageRefreshOnChange=True )
    transformLayout =              Action( noDealPackageRefreshOnChange=True,
                                           action='@TransformLayout')
    showGraphInitially =           Bool(   noDealPackageRefreshOnChange=True )
    graphApplicable =              Bool(   noDealPackageRefreshOnChange=True )
    showSheetInitially =           Bool(   noDealPackageRefreshOnChange=True )
    sheetApplicable =              Bool(   noDealPackageRefreshOnChange=True )
    
    updateParentDelegateTraits =   Action( action='@_UpdateParentDelegateTraits',
                                           noDealPackageRefreshOnChange=True )
    
    solverParameter =              Str(    label="Solve For",
                                           choiceListSource="@_SolverParameterChoices",
                                           noDealPackageRefreshOnChange=True )
    solverTopValue =               Str(    label="Goal Value",
                                           choiceListSource="@_SolverTopValueChoices",
                                           noDealPackageRefreshOnChange=True,
                                           onChanged='@_OnSolverTopValueChanged' )
    solverValue =                  Float(  label="Value",
                                           noDealPackageRefreshOnChange=True,
                                           onChanged='@_OnSolverValueChanged' )
    solverAction =                 Action( label='Solve',
                                           action='@_Solve',
                                           noDealPackageRefreshOnChange=True )
    uxCallbacks =                  Object( objMapping='_UxCallbacks',
                                           domain='FDictionary',
                                           noDealPackageRefreshOnChange=True)
    salesTradingInteraction  =     Object( objMapping='_SalesTradingInteraction',
                                           noDealPackageRefreshOnChange=True)
    uiViewModeIsSlim =             Object( objMapping='UiViewModeIsSlim',
                                           domain='FDictionary',
                                           noDealPackageRefreshOnChange=True)
    toggleAllShowModes =           Action( label="@_SlimDetailLabel",
                                           action='@_ToggleShowMode')
    
    def __init__(self,   dealPackage):
        TraitBasedDealPackage.__init__(self, dealPackage)
        self._payoffGraphCalculations = PayoffGraphCalculations(self, self._GetCalcSpace)
        self._blockSolve = False
        self._graphCoordinates = []
        self._tradeActionInstances = {}
        self._customActionInstances = {}
        self._uxCallbacks = acm.FDictionary()
        self._uiViewModeIsSlim = acm.FDictionary()
        self._uiViewModeIsSlim.AtPut("DetailedMode1", True)
        self._uiViewModeIsSlim.AtPut("DetailedMode2", True)
        
    def _SalesTradingInteraction(self, input='NoInputVal', *args):
        if input == 'NoInputVal':
            if not hasattr(self, '_salesTradingInteraction'):
                self._salesTradingInteraction = SalesTradingInteraction()
            return self._salesTradingInteraction

    def _UxCallbacks(self, input='NoInputVal'):
        if input == 'NoInputVal':
            return self._uxCallbacks
        else:
            for key in input.Keys():
                self._uxCallbacks.AtPut(key, input.At(key))

    def UiViewModeIsSlim(self, input='NoInputVal'):
        if input == 'NoInputVal':
            return self._uiViewModeIsSlim
        else:
            for key in input.Keys():
                self._uiViewModeIsSlim.AtPut(key, input.At(key))

    def CloseDialog(self):
        closeDialogCallback = self._uxCallbacks.At('closeDialogCb')
        if closeDialogCallback:
            closeDialogCallback()
        else:
            raise DealPackageException('CloseDialog only applicable from Dialog')

    def _autoRefreshCalc_default(self):
        return True
           
    def _OnRefreshCalcCounterChanged(self, attrRefreshCalc, oldValue, newValue,*args):
        self._RegisterAllCalculations()
        self._RefreshAllCalculations()
        if not getattr(self, 'autoRefreshCalc'):
            self.SetAttribute('graphCoordinatesNeedsRefresh', True)
        setattr(self, attrRefreshCalc, newValue)
    
    def _uxCallbacks_default(self):
        return self._UxCallbacks()
        
    def _sheetDefaultColumns_default(self):
        return self._SheetDefaultColumns()
    
    def _showGraphInitially_default(self):
        return self._ShowGraphInitially() and self._GraphApplicable()

    def _graphApplicable_default(self):
        return self._GraphApplicable()
        
    def _showSheetInitially_default(self):
        return self._ShowSheetInitially() and self._SheetApplicable()

    def _multiTradingEnabled_default(self):
        return self._MultiTradingEnabled()

    def _sheetApplicable_default(self):
        return self._SheetApplicable()
       
    def _customPanes_default(self):
        return self.TransformLayout(None, self.CustomPanes())
    
    def _SlimDetailLabel(self, attrName):
        isSlim = self.uiViewModeIsSlim.At('DetailedMode1')
        return "Detail Mode" if isSlim else "Slim Mode"
    
    def _RecursiveUpdateChildShowModes(self, childDp):
        childDp.GetAttribute('toggleAllShowModes')()
        
    def _ToggleShowMode(self, attrName):
        # Need to make copy of dict, else messing with defaultValue 
        # (class variable for attributes of type Object)
        newMode = self.uiViewModeIsSlim.At('DetailedMode1') != True
        self.uiViewModeIsSlim.AtPut('DetailedMode1', newMode)
        self.uiViewModeIsSlim.AtPut('DetailedMode2', newMode)
        for child in self.ChildDealPackages():
            self._RecursiveUpdateChildShowModes(child)
    
    '''******************************** 
    Layout Util
    ********************************''' 
    def TransformLayout(self, attrName, layout):
        if not isinstance(layout, basestring): # if string, do nothing
            layout = WrapAsTabControlList(layout)
        layout = self.__SearchReplaceCompositeAttributes(layout)
        return layout
    
    def __SearchReplaceCompositeAttributes(self, layout):
        if isinstance(layout, basestring):
            layout = self.__ReplaceWithCompositeAttributeNames(layout)
        else:
            for tabCtrlPaneInfo in layout:
                tabCtrlName, tabCtrlLayout = UnpackPaneInfo(tabCtrlPaneInfo)
                for paneInfo in tabCtrlLayout:
                    paneName, paneLayout = UnpackPaneInfo(paneInfo)
                    paneInfo[paneName] = self.__ReplaceWithCompositeAttributeNames(paneInfo[paneName])
        return layout
    
    def __ReplaceWithCompositeAttributeNames(self, layout):
        compositeAttributes = self._CompositeAttributes()
        for attrName in compositeAttributes:
            attrLayout = compositeAttributes[attrName].GetLayout()
            if isinstance(attrLayout, basestring):
                layout = re.sub((r'\b%s\b')%(attrName), attrLayout.strip().rstrip(';'), layout)
        return layout
    
    '''******************************** 
    Trait Changed
    ********************************''' 
    def RegisterCallbackOnAttributeChanged(self, callback, attributes = None, last = False):
        if last:
            self.on_post_trait_change(callback, attributes)
        else:
            self.on_trait_change(callback, attributes)
    
    '''******************************** 
    UI View Mode Helper Functions
    ********************************''' 
        
    def IsShowModeDetail(self, *args):
        return self.uiViewModeIsSlim.At("DetailedMode1") == False
        
    def IsShowModeDetail2(self, *args):
        return self.uiViewModeIsSlim.At("DetailedMode2") == False
        
    '''******************************** 
    CUSTOM PANDS/LAYOUT
    ********************************'''
    def GetCustomPanesFromExtValue(self, *layouts):
        if len(layouts) == 1 and isinstance(layouts[0], basestring):
            # Backwards compatibility, before tab sections
            return self._GetLayoutFromExtValue(layouts[0])
        else:
            retValue = []
            for nameAndExtValue in layouts:
                assert len(nameAndExtValue) == 2, "GetCustomPanesFromExtValue, failed to parse layout. Expected arguments as (['Pane Name 1', 'extValueName1'], ['Pane Name 2', 'extValueName2'], ...), got " + str(layouts)
                paneName = nameAndExtValue[0]
                customPane = self._GetLayoutFromExtValue(nameAndExtValue[1])
                retValue.append({paneName: customPane})
            return retValue

    def _GetLayoutFromExtValue(self, extValueName):
        retValue = []
        extCustomPanes = acm.GetDefaultContext().GetExtension(acm.FExtensionValue, acm.FObject, extValueName)
        if extCustomPanes is None:
            raise DealPackageException("DealPackageBase, " + extValueName + ", no such extension value")              
        customPanes = extCustomPanes.Value()
        customPanes = customPanes.rstrip(';') # drop terminating ';'
        
        layoutsAndPanes = customPanes.split(';')
        for pane in layoutsAndPanes:
            layoutNamePane = pane.split(',')
            if len(layoutNamePane) == 2:
                ext = acm.GetDefaultContext().GetExtension(acm.FExtensionValue, acm.FObject, layoutNamePane[0])
                if ext is None:
                    error = "DealPackageBase::GetCustomPanesFromExtValue FObject:"
                    raise DealPackageException(error + layoutNamePane[0] + ", no such layout")          
                layout = ext.Value()
                if not layoutNamePane[1]:
                    raise DealPackageException("DealPackageBase::GetCustomPanesFromExtValue pane name missing")           
                retValue.append( {layoutNamePane[1]: layout} )
            else:
                raise DealPackageException("DealPackageBase::GetCustomPanesFromExtValue corrupt " + layoutsAndPanes)
        return retValue
    
    
    '''******************************** 
    Deal Package on Deal Package only:
        When a deal package child is updated directly, and not via the parent deal package, 
        the parent Delegate traits need to be re-read
    ********************************'''  
    def _UpdateParentDelegateTraits(self, *args):
        if (not self._muteParentNotifications):
            self._DelegateAttributeMappingDefaultValuesToParent()
            self._RegisterAllObjectMappings()
        
    '''******************************** 
    Solver
    ********************************'''  
    
    def SolverColor(self, attrName): # API-method in DealPackageDevKit
        solverParam = self.GetAttributeMetaData(attrName, 'solverParameter')()
        if solverParam and self.__HasSolverTopValue():
            return 'BkgDealSolver'
        else:
            return None
    
    def __HasSolverTopValue(self):
        for attrName in self.GetAttributes():
            if self.GetAttributeMetaData(attrName, 'solverTopValue')():
                return True
        return False
    
    def _solverTopValue_default(self):
        return self.__GetFirstChoiceItem(self._SolverTopValueChoices())
        
    def _solverParameter_default(self):
        return self.__GetFirstChoiceItem(self._SolverParameterChoices())
        
    def _solverValue_default(self):
        value = None
        topValue = self.__GetFirstChoiceItem(self._SolverTopValueChoices())
        if topValue:
            value = self.__GetDefaultSolverValue(topValue)
        return value
    
    def _OnSolverValueChanged(self, traitName, *args):
        self._Solve()
        
    def _OnSolverTopValueChanged(self, traitName, *args):
        self._blockSolve = True
        try:
            self.solverValue = self.__GetDefaultSolverValue(self.solverTopValue)
        except:
            pass
        self._blockSolve = False
        
    def __GetDefaultSolverValue(self, attr):
        attr = self.solverParameter if self.__IsSolverAttribute(attr) else None
        value = self.__GetActualValue(attr)
        return value
        
    def __GetActualValue(self, attr):
        value = self.get_trait_value(attr)
        if value and self._GetCalcMapping(attr):
            value = value.Value()
        return value
        
    def __IsSolverAttribute(self, attr):
        return self._GetSolverTopValue(attr) or self._GetSolverParameter(attr)
    
    def _SolverTopValueChoices(self, *args):
        topValues = self.__GetAllWithMatchingProperty("solverTopValue")
        return topValues
    
    def _SolverParameterChoices(self, *args):
        parameters = self.__GetAllWithMatchingProperty("solverParameter")
        return parameters
        
    def __GetAllWithMatchingProperty(self, filterProperty):
        values = acm.FArray()
        for attr in self.get_trait_names():
            filterPropertyValue = self._GetAttributeMetaDataCallback(attr, filterProperty)()
            if filterPropertyValue:
                    values.Add(attr)
        return values

    def __GetFirstChoiceItem(self, choices):
        value = None
        if not choices.IsEmpty():
            value = choices.First()
        return value

    def __IsSolved(self, currentValue, solverValue, precision):
        asArray = acm.GetFunction('doubleArray', 1)
        currentValue = asArray(currentValue)
        solverValueList = list(asArray(solverValue))
        if len(solverValueList) == 1:
            for currentTopValue in currentValue:
                if abs(currentTopValue - solverValue) <= precision:
                    return True
            return False
        else:
            if len(currentValue) != len(solverValueList):
                return False
            for currentTopValue, value in zip(currentValue, solverValueList):
                if abs(currentTopValue - value) > precision:
                    return False
            return True

    def Solve(self, topValue = None, parameter = None, solverValue = None):
        with SetSolverParametersWithSafeExit(self, topValue, parameter, solverValue):
            result = self._DoSolve()
        return result
                
    def _DoSolve(self):
        topValue = self.solverTopValue if self.__IsSolverAttribute(self.solverTopValue) else None
        parameter = self.solverParameter if self.__IsSolverAttribute(self.solverParameter) else None
        if parameter and topValue:
            parameterValue = self.__GetActualValue(parameter)
            minValue = None
            maxValue = None
            precision = 0.001
            maxIterations = 100
            solverParameters = self._GetSolverParameter(parameter)
            if not isinstance(solverParameters, list):
                solverParameters = [solverParameters]
            for solverBoundaries in solverParameters:
                if isinstance(solverBoundaries, dict):
                    if "minValue" in solverBoundaries:
                        minValue = solverBoundaries["minValue"]
                    if "maxValue" in solverBoundaries:
                        maxValue = solverBoundaries["maxValue"]
                    if "precision" in solverBoundaries:
                        precision = solverBoundaries["precision"]
                    if "maxIterations" in solverBoundaries:
                        maxIterations = solverBoundaries["maxIterations"]
                if minValue is None:
                    minValue = 0.1 * parameterValue
                if maxValue is None:
                    maxValue = 10.0* parameterValue
                
                if self.__IsSolved(self.__GetActualValue(topValue), self.solverValue, precision):
                    return self.__GetActualValue(parameter)
                
                result = self.DealPackage().Solve(parameter, topValue, self.solverValue, minValue, maxValue, precision, maxIterations)
                isFinite = acm.Math.IsFinite(result)
                if hasattr(isFinite, 'IsKindOf') and isFinite.IsKindOf(acm.FArray):
                    isFinite = reduce(lambda x, y: x and y, isFinite)
                if isFinite:
                    return result
            raise DealPackageException("No solution found for '%s' that gives expected '%s' of %s. "
                                        "(Using boundary conditions min = %.2f, max = %.2f, precision = %f, max iterations = %d)."
                                        %(self.solverParameter, self.solverTopValue, self.solverValue, minValue, maxValue, precision, maxIterations))

    def _Solve(self, *args):
        result = None
        if not self._blockSolve:
            result = self._DoSolve()
            if result is not None:
                parameter = self.solverParameter if self.__IsSolverAttribute(self.solverParameter) else None
                self.DealPackage().SetAttribute(parameter, result)
                self.Refresh()
        return result
            
    def _SolveForTrait(self, traitName, value):
        value = self._GetTransform(traitName)(value)
        self.solverTopValue = traitName
        previousSolverValue = self.solverValue
        f = self.__ColumnFormatter(traitName)
        self.solverValue = ParseFloat(value, formatter=f)
        if self.solverValue == previousSolverValue:
            self._Solve()
    
    def __ColumnFormatter(self, traitName):
        formatter = acm.FReal.DefaultFormatter()
        calcInfo = self._GetCalcMapping(traitName)
        if calcInfo:
            _, sheetType, columnId = calcInfo.split(":")
            context = acm.GetDefaultContext()
            for colDef in acm.GetColumns(columnId, sheetType, context):
                if colDef.Formatter():
                    formatter = colDef.Formatter()
                    break
        return formatter
    
    def GetFormatter(self, attrName):
        return self.GetAttributeMetaData(attrName, 'formatter')()
    
    '''******************************** 
    GENERAL GRAPH COORDINATES
    ********************************''' 
    def _GraphCoordinates(self, *args):
        if self.get_trait_value('graphCoordinatesNeedsRefresh'):
            self._graphCoordinates = self.__CalculateGraphCoordinates()
            self.SetAttribute('graphCoordinatesNeedsRefresh', False)
        return self._graphCoordinates
    
    def __CalculateGraphCoordinates(self):
        xValues = self.GraphXValues()
        yValues = self.GraphYValues(xValues)
        if len(xValues) != len(yValues):
            raise DealPackageException("Mismatching x- and y-values. Number of x-values: %s, Number of y-values: %s", len(xValues), len(yValues))
        return [[x, y] for x, y in map(None, xValues, yValues)]
        
    def GraphYValues(self, xValues):
        return self._payoffGraphCalculations.GraphYValues(xValues)
        
    def GraphXValues(self):
        return self._payoffGraphCalculations.GenerateXValues()
     
    def _TradeActionAt(self, key):
        stringKey = str(key) 
        tradeAction = self._tradeActionInstances.get(stringKey)
        if not tradeAction:
                cls = self.__class__._TradeActionHandlers().get(stringKey)
                if cls:
                    tradeAction = cls(dealPackage = self.DealPackage())
                    self._tradeActionInstances[stringKey] = tradeAction
        return tradeAction
        
    def _CustomActionAt(self, key):
        stringKey = str(key) 
        customAction = self._customActionInstances.get(stringKey)
        if not customAction:
                cls = self.__class__._CustomActionHandlers().get(stringKey)
                if cls:
                    customAction = cls(dealPackage = self.DealPackage())
                    self._customActionInstances[stringKey] = customAction
        return customAction
 
    @classmethod
    def _SheetDefaultColumns(cls):
        return []
        
    @classmethod
    def _MultiTradingEnabled(cls):
        return False

    @classmethod
    def _ShowGraphInitially(cls):
        return True
    
    @classmethod
    def _GraphApplicable(cls):
        return True
    
    @classmethod
    def _ShowSheetInitially(cls):
        return True
    
    @classmethod
    def _SheetApplicable(cls):
        return True
        
    @classmethod
    def _IncludeTradeActionTrades(cls):
        return False
    
    @classmethod
    def _TradeActionHandlers(cls):
        return {}
        
    @classmethod
    def _CustomActionHandlers(cls):
        return {}
    
    @classmethod
    def _SalesTradingInteractionSetting(cls, settingName, *args):
        if hasattr(cls, '_salesTradingInteraction') and cls._salesTradingInteraction:
            return cls._salesTradingInteraction.At(settingName)
    
    @classmethod
    def _Create(cls, dealPackage):
        return cls(dealPackage)
            
    
class DealPackageChoiceListSource(object):
    def __init__(self):
        self._source = acm.FArray()
        
    def __getattr__(self, attr):
        try:
            return getattr(self._source, attr)
        except AttributeError:
            return object.__getattr__(self, attr)
            
    def AddAll(self, coll):
        with NoChange(self._source):
            self._source.AddAll(coll)
        self._source.Changed()
        
    def Populate(self, coll):
        with NoChange(self._source):
            self._source.Clear()
            self._source.AddAll(coll)
        self._source.Changed()
        
    def Source(self):
        return self._source
