
import acm
from DealPackageUtil import DealPackageException, UnDecorate

CALC_SPACES = acm.FIdentityDictionary()
TAGGED_CALC_SPACES = acm.FIdentityDictionary()
def GetCalcSpaceCollection(dealPackage, tag):
    dealPackage = UnDecorate(dealPackage)
    if hasattr(dealPackage, 'TopParentDealPackage'):
        dealPackage = dealPackage.TopParentDealPackage()
    cache = GetCalcSpaceCache(tag)
    calcSpaceCollection = cache[dealPackage]
    if not calcSpaceCollection:
        calcSpaceCollection = acm.Calculations().CreateCalculationSpaceCollection()
        cache.AtPutWeak(dealPackage, calcSpaceCollection)
    return calcSpaceCollection
    
def ClearCalcSpaceCollection(dealPackage, tag):
    dealPackage = UnDecorate(dealPackage)
    cache = GetCalcSpaceCache(tag)
    space = cache.RemoveKey(dealPackage)
    if space:
        space.Clear()
        
def GetCalcSpaceCache(tag):
    cache = CALC_SPACES
    if tag != None:
        cache = TAGGED_CALC_SPACES[tag]
        if not cache:
            cache = acm.FIdentityDictionary()
            TAGGED_CALC_SPACES.AtPutWeak(tag, cache, True, False)
    return cache
        
class DealPackageCalculations():
    def __init__(self, parent, tag=None):
        self._calcSpaceCollection = None
        self._calculations = acm.FOrderedDictionary()
        self._simulations = acm.FOrderedDictionary()
        self._parent = parent
        self._tag = tag
        
    def Calculations(self):
        return self._calculations
        
    def DealPackage(self):
        return self._parent
        
    def Simulations(self):
        return self._simulations
        
    def Tag(self):
        return self._tag
        
    def CalcSpaceCollection(self):
        self._calcSpaceCollection = GetCalcSpaceCollection(self.DealPackage().DealPackage(), self.Tag())
        return self._calcSpaceCollection
        
    def CalcSpace(self, sheetType):
        return self.CalcSpaceCollection().GetSpace(sheetType, acm.GetDefaultContext())
    
    def AnyCalcObjectReplaced(self):
        for calc in self.Calculations().Values():
            if calc.CalcObjectReplaced():
                return True

    def UpdateCalcSpaceCollection(self):
        ClearCalcSpaceCollection(self.DealPackage().DealPackage(), self.Tag())
            
    def CreateCalculation(self, name, calcObjectCB, sheetType, columnId, columnIdCb, configurationCB):
        if name in self.Calculations().Keys():
            raise DealPackageException("A calculation named '%s' is already registered" % name)
        calc = DealPackageCalculation(name, self, calcObjectCB, sheetType, columnId, columnIdCb, configurationCB)
        self.Calculations().AtPut(name, calc)
        
    def RegisterCalculations(self):
        self.UpdateCalcSpaceCollection()
        for calc in self.Calculations().Values():
            calc.RegisterCalculation()
        self.ApplySimulations(self.Simulations())
        
    def Calculation(self, name):
        return self.Calculations().At(name)
           
    def SimulateValue(self, name, value):
        if value not in ["", None]:
            if self.Calculation(name).Simulate(value):
                self.Simulations()[name] = value
        elif self.IsSimulated(name):
            self.Simulations().RemoveKey(name)
            self.Calculation(name).RemoveSimulation()
            
    def IsSimulated(self, name):
        return self.Simulations().Includes(name)
    
    def HasCalculation(self, name):
        return self.Calculations().Includes(name)
        
    def RecalculateAll(self):
        for calc in self.Calculations().Values():
            try:
                calc.Value().Value()
            except Exception as e:
                msg = "Failed to get Value() on calculation %s : %s"
                self.DealPackage().Log().Verbose(msg % (calc.Name(), str(e)))
            
    def ApplySimulations(self, simulations):
        for name in simulations.Keys():
            value = simulations.At(name)
            self.SimulateValue(name, value)
            self.RecalculateAll()
            
    def SimulatedValue(self, name):
        return self.Simulations().At(name, "")
    
    def Value(self, name):
        value = None
        if self.HasCalculation(name):
            value = self.Calculation(name).Value()
        return value
        
    def RefreshCalculation(self, name):
        value = None
        if self.HasCalculation(name):
            value = self.Calculation(name).RefreshCalculation()
        return value
        
    def RemoveCalculation(self, name):
        if self.HasCalculation(name):
            self.SimulateValue(name, "")
            self.Calculation(name).DestroyCalculation(True)
            self.Calculations().RemoveKey(name)
            
    def CreateMissingCalculations(self, calculations):
        for name in calculations.Keys():
            if not self.Calculations().At(name):
                calc = calculations.At(name)
                columnId = calc._columnId
                columnIdCb = calc._columnIdCb
                calcObjectCB = getattr(self._parent, calc.CalcObjectCB().__name__)
                sheetType = calc.SheetType()
                configurationCB = getattr(self._parent, calc.ConfigurationCB().__name__) if calc.Configuration() else None
                self.CreateCalculation( name, calcObjectCB, sheetType, columnId, columnIdCb, configurationCB)
        
    def RemoveAllSimulations(self):
        for name in self.Simulations().Keys()[:]:
            self.SimulateValue(name, None)
            
    def TearDown(self):
        if self.Calculations():
            for name in self.Calculations().Keys()[:]:
                self.RemoveCalculation(name)
        
        if self._calcSpaceCollection:
            ClearCalcSpaceCollection(self.DealPackage().DealPackage(), self.Tag())
            
        self._calcSpaceCollection = None
        self._calculations = None
        self._simulations = None
        self._parent = None
        self._tag = None
        
class DealPackageCalculation():
    def __init__(self, name, parent, calcObjectCB, sheetType, columnId, columnIdCb, configurationCB):
        self._name = name
        self._parent = parent
        self._columnId = columnId
        self._columnIdCb = columnIdCb
        self._calcObjectCB = calcObjectCB
        self._currentCalcObject = None
        self._currentCalcConfig = None
        self._currentCalcSpace = None
        self._invalidated = False
        self._calculation = None
        self._sheetType = sheetType
        self._configurationCB = configurationCB
        self.CreateCalculation()
    
    def Name(self):
        return self._name
    
    def DealPackage(self):
        return self._parent.DealPackage()
    
    def CalcSpace(self):
        return self._parent.CalcSpace(self._sheetType)
        
    def CalcObject(self):
        calcObject = None
        if self._calcObjectCB:
            try:
                calcObject = self._calcObjectCB(self._name)
            except:
                calcObject = self._calcObjectCB()
        return UnDecorate(calcObject) if calcObject else None
        
    def CalcObjectCB(self):
        return self._calcObjectCB
        
    def CalcObjectReplaced(self):
        def IsDifferentObject(x, y):
            x = UnDecorate(x) if x else x
            y = UnDecorate(y) if y else y
            return bool((x != y) and (x or y))
        newCalcObject = self.CalcObject()
        currentCalcObject = self._currentCalcObject
        newCalcSpace = self.CalcSpace()
        currentCalcSpace = self._currentCalcSpace
        return IsDifferentObject(newCalcObject, currentCalcObject) or IsDifferentObject(newCalcSpace, currentCalcSpace)
        
    def Configuration(self):
        configuration = self._configurationCB() if self._configurationCB else None
        return configuration
        
    def ConfigurationCB(self):
        return self._configurationCB
        
    def CreateCalculation(self):
        try:
            self._currentCalcObject = self.CalcObject()
            self._currentCalcSpace = self.CalcSpace()
            self._currentCalcConfig = self.Configuration()
            if self._currentCalcObject:
                self._currentCalcSpace.SimulateValue(self._currentCalcObject, "Standard Calculations Include All Trades", True)
                self._calculation = self._currentCalcSpace.CreateCalculation(self._currentCalcObject, self.ColumnId(), self._currentCalcConfig)
                self._calculation.AddDependent(self)
            else:
                self._calculation = None
                self.DealPackage().Log().Verbose("{} returned None.".format(self._calcObjectCB))
        except Exception as e:
            msg = "Failed to create calculation for %s : %s"
            self.DealPackage().Log().Error(msg % (self.Name(), str(e)))
        
    def DestroyCalculation(self, clearAll=False):
        if self._calculation:
            self._calculation.RemoveDependent(self)
        if clearAll:
            self._parent = None
            self._calculation = None
            self._calcObjectCB = None
            self._currentCalcObject = None
            self._currentCalcConfig = None
            self._configurationCB = None
            
    def RegisterCalculation(self):
        self.DestroyCalculation()
        self.CreateCalculation()
        
    def IsInvalidated(self):
        return self._invalidated
    
    def Invalidate(self, invalid):
        self._invalidated = invalid
        
    def Simulate(self, value):
        try:
            self._currentCalcSpace.SimulateValue(self._currentCalcObject, self.ColumnId(), value, self._currentCalcConfig)
            return True
        except:
            pass
        return False
            
    def RemoveSimulation(self):
        if self._currentCalcSpace.RemoveSimulation(self._currentCalcObject, self.ColumnId(), self._currentCalcConfig):
            self.Invalidate(True)
            
    def Value(self):
        return self._calculation
        
    def RefreshCalculation(self):
        value = None
        if self.IsInvalidated():
            value = self.Value()
            self.Invalidate(False)
        return value
    
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        self.Invalidate(True)
        
    def SheetType(self):
        return self._sheetType
    
    def ColumnId(self):
        if self._columnIdCb:
            columnId = self._columnIdCb()
        else:
            columnId = self._columnId
        return columnId
