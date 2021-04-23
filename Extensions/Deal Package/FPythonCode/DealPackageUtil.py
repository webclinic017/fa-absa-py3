import acm
from contextlib import contextmanager
import types
import re
import pickle

FUNCTION_DOMAIN_ATTRIBUTE = "_domain_"

def ReloadAllModules():
    ''' Trait Related Imports '''
    import DealPackageGridViewModelItem
    reload(DealPackageGridViewModelItem)
    import DealPackageCommandActionUtils
    reload(DealPackageCommandActionUtils)
    import DealPackageDialog
    reload(DealPackageDialog)
    import CompositeAttributeBase
    reload(CompositeAttributeBase)
    import CompositeAttributeDevKit
    reload(CompositeAttributeDevKit)
    import TraitUtil
    reload(TraitUtil)
    import traitlets
    reload(traitlets)
    import TraitBaseTypes
    reload(TraitBaseTypes)
    import AttributeMetaData
    reload(AttributeMetaData)
    import AttributeMetaDataFactory
    reload(AttributeMetaDataFactory)
    import TraitBase
    reload(TraitBase)
    import TraitDomainAndValueValidator
    reload(TraitDomainAndValueValidator)
    import DealPackageCalculations
    reload(DealPackageCalculations)
    import DealPackagePayoffGraphCalculations
    reload(DealPackagePayoffGraphCalculations)
    import TraitBasedDealPackage
    reload(TraitBasedDealPackage)
    import DealPackageBase
    reload(DealPackageBase)
    import DealPackageTradeActionCommands
    reload(DealPackageTradeActionCommands)
    import DealPackageDevKit
    reload(DealPackageDevKit)
    import FreeForm
    reload(FreeForm)
    import DealBase
    reload(DealBase)
    import DealDevKit
    reload(DealDevKit)
    import EditableObjectBase
    reload(EditableObjectBase)
    import EditableObjectDevKit
    reload(EditableObjectDevKit)    
    import EditableObjectDefault
    reload(EditableObjectDefault)
    import CompositeAttributes
    reload(CompositeAttributes)
    import DealPackageTradeActionBase
    reload(DealPackageTradeActionBase)
    import DealPackageTradeActionCorrect
    reload(DealPackageTradeActionCorrect)
    import DealPackageTradeActionCloseBase
    reload(DealPackageTradeActionCloseBase)
    import DealPackageTradeActionClose
    reload(DealPackageTradeActionClose)
    import DealPackageTradeActionNovate
    reload(DealPackageTradeActionNovate)
    import DealPackageSetUp
    reload(DealPackageSetUp)
    import UxWrapper
    reload(UxWrapper)
    import UxHelpers
    reload(UxHelpers)

    ''' Validation '''
    import DealPackageValidation
    reload(DealPackageValidation)


def IsPublicTrait(obj, traitName):
    return traitName in obj.traits() and not traitName.startswith("_")
    
def IsCallable(obj, attr):
    if hasattr(obj, attr):
        candidate = getattr(obj, attr)
        return hasattr(candidate, '__call__')
    return False
    
def IsIterable(candidate):
    try:
        iter(candidate)
    except:
        return False
    else:
        return True

def MakeIterable(obj):
    return obj if IsIterable(obj) else [obj]
    
def IsFObject(obj, aType=None):
    toReturn = False
    if hasattr(obj, 'IsKindOf'):
        if aType == None:
            toReturn = True
        else:
            toReturn = obj.IsKindOf(aType)
    return toReturn

def StringKeyOrVal(val):
    if IsFObject(val):
        val = val.StringKey()
    return str(val)
        
class DealPackageException(Exception):
    pass

class DealPackageUserException(Exception):
    pass

def FormatException(err):
    def removePre(msg):
        msg = msg.split("Exception:")[-1]
        msg = str(msg).split("Error:")[-1]
        return msg
        
    def removeStack(msg):
        msg = re.compile(": in '.*line [0-9]*").split(msg)[0] # removes c++ exception stacktrace
        msg = re.compile("\(\[.*\]/").split(msg)[0] # removes python exception (everything after first occurrence of([ABC00]/)
        msg = msg.strip()
        msg = msg[:-1] if len(msg) and msg[-1] == ':' else msg
        msg = msg.strip()
        return msg
    msg = removePre(str(err))
    msg = removeStack(msg)
    msg = msg.replace(': ', '\n')
    return msg.strip()
    
@contextmanager
def NoChange(acmObj):
    """
    Temporarily mute an object
    Example:
    
    with NoChange( myObj ):
        myObj.Clear()
        myObj.AddAll( myCollection )
    myObj.Changed()
    """
    oldMute = acmObj.IsMute()
    acmObj.Mute(True)
    try:
        yield None
        acmObj.Mute(oldMute)
    except:
        acmObj.Mute(oldMute)
        raise

class Settings(object):
    '''Decorator to sett DealPackageDefinition settings'''
    
    def __init__(self, **kwarg):
        self._kwarg = kwarg
        
    def __call__(self, definition):
        for k, v in self._kwarg.iteritems():
            self.CreateSettingFunction(definition, k, v)
        return definition
    
    def CreateSettingFunction(self, definition, publicSettingName, value):
        settingName = self.__TransformToInternalSetting( publicSettingName )
        func = lambda _: value
        func = types.MethodType( func, definition )
        setattr(definition, settingName, func)
    
    def __AssertPublicSetting(self, settingName):
        if not settingName in self.__PublicSettings():
            raise DealPackageException('%s is not a public setting' % settingName)
    
    def __PublicSettings(self):
        return ('SheetDefaultColumns',\
                'ShowGraphInitially',\
                'GraphApplicable',\
                'ShowSheetInitially',\
                'SheetApplicable',
                'LogMode',
                'IncludeTradeActionTrades',
                'MultiTradingEnabled')
    
    def __TransformToInternalSetting(self, settingName):
        self.__AssertPublicSetting(settingName)
        return '_%s' % settingName

class SalesTradingInteraction(object):
    SALES_NAME = 'Sales'
    MAIN_TRADING_COMPONENT_NAME = 'Main'
    
    @staticmethod
    def DefaultComponent(trade, dealPackage):
        componentsInfo = acm.FDictionary()
        if dealPackage and not dealPackage.IsDeal():
            tradeOrDealPackage = dealPackage
        else:
            tradeOrDealPackage = trade
        componentsInfo.AtPut(SalesTradingInteraction.MAIN_TRADING_COMPONENT_NAME, tradeOrDealPackage)
        return componentsInfo
    
    @staticmethod
    def UseQuantity(instrument, dealPackage):
        if dealPackage and not dealPackage.IsDeal():
            return True
        return not instrument.IsCashFlowInstrument() or instrument.IsRepoInstrument()
        
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        
    def __call__(self, definition):
        setattr(definition, self.VariableName(), self)
        return definition 
    
    def At(self, key):
        attr = self._kwargs.get(key)
        if not attr:
            if hasattr(self, key):
                attr = getattr(self, key)
        return attr
    
    def VariableName(self):
        return '_salesTradingInteraction'
    
    def QuoteRequestComponents(self, mainTrade, dealPackage):
        return SalesTradingInteraction.DefaultComponent(mainTrade, dealPackage)
    
    def QuantityFactor(self, dealPackage, componentName):
        return 1.0
    
    def TraderPrice(self, dealPackage, prices):
        return prices.Values().First()
    
    def TraderQuantity(self, dealPackage, quantities):
        return quantities.Values().First()
    
    def TraderNominal(self, dealPackage, nominals):
        return nominals.Values().First()

class SalesTradingInfo(object):
    @staticmethod
    def ObjectType(obj):
        if obj.IsKindOf('FDealPackage'):
            objType = 'DealPackage'
        elif obj.IsKindOf('FInstrumentPackage'):
            objType = 'InstrumentPackage'
        elif obj.IsKindOf('FTrade'):
            objType = 'Trade'
        elif obj.IsKindOf('FInstrument'):
            objType = 'Instrument'
        else:
            raise Exception('Object of type ' + obj.ClassName() + ' is not allowed in SalesTradingInfo extended data.')
        return objType
    
    @staticmethod
    def GetExtendedData(imObject, extendedDataName):
        extendedDataValue = ''
        try:
            extendedData = imObject.ExtendedData()
        except:
            try:
                extendedDataValue = imObject.GetExtendedData(extendedDataName)
            except:
                pass
        else:
            if hasattr(extendedData, extendedDataName):
                extendedDataValue = getattr(extendedData, extendedDataName)()
        return extendedDataValue
    
    @staticmethod
    def BackwardsCompatibleCreateDict(imObject):
        def Name(imObject):
            name = ''
            if hasattr(imObject, 'Role') and imObject.Role() == 'Trading':
                name = SalesTradingInteraction.MAIN_TRADING_COMPONENT_NAME
            else:
                name = SalesTradingInteraction.SALES_NAME
            return name
        
        def ObjectToQuote(imObject, tabTradeCreationSetting):
            objectToQuote = {}
            dpId = SalesTradingInfo.GetExtendedData(imObject, 'DealPackageId')
            tradeId = SalesTradingInfo.GetExtendedData(imObject, 'TradeId')
            if dpId:
                objType = 'InstrumentPackage' if tabTradeCreationSetting == 'Create New' else 'DealPackage'
                objectToQuote = {'type' : objType, 'oid' : str(dpId)}
            elif tradeId:
                objectToQuote = {'type' : 'Trade', 'oid' : str(tradeId)}
            else:
                ins = imObject.TradingInterface().Instrument()
                objectToQuote = {'type' : 'Instrument', 'oid' : str(ins.Oid())}
            return objectToQuote

        def TabTradeCreationSetting(imObject):
            return SalesTradingInfo.GetExtendedData(imObject, 'TABTradeCreationRule')

        def NumberOfComponents(imObject):
            return 1 # In previous versions, MultiRFQ was not supported

        salesTradingInfoDict = {}
        salesTradingInfoDict['name'] = Name(imObject)
        salesTradingInfoDict['tabTradeCreationSetting'] = TabTradeCreationSetting(imObject)
        salesTradingInfoDict['objectToQuote'] = ObjectToQuote(imObject, salesTradingInfoDict['tabTradeCreationSetting'])
        salesTradingInfoDict['numberOfComponents'] = NumberOfComponents(imObject)
        return salesTradingInfoDict
            
    @staticmethod
    def ExtractDict(imObject):
        salesTradingInfoDict = {}
        salesTradingInfoString = SalesTradingInfo.GetExtendedData(imObject, 'SalesTradingInfo')
        if salesTradingInfoString:
            salesTradingInfoDict = pickle.loads(salesTradingInfoString)
        else:
            salesTradingInfoDict = SalesTradingInfo.BackwardsCompatibleCreateDict(imObject)
        return salesTradingInfoDict
    
    @staticmethod
    def ApplyDict(imObject, salesTradingInfoDict):
        salesTradingInfoString = pickle.dumps(salesTradingInfoDict)
        try:
            extendedData = imObject.ExtendedData()
        except:
            imObject.SetExtendedData('SalesTradingInfo', salesTradingInfoString)
        else:
            extendedData.SalesTradingInfo(salesTradingInfoString)
            
    @staticmethod
    def SetSalesTradingExtendedData(imObject, componentName, customDict, numberOfComponents=None):
        salesTradingInfoDict = SalesTradingInfo.ExtractDict(imObject)
        salesTradingInfoDict['name'] = componentName
        if componentName == SalesTradingInteraction.SALES_NAME:
            salesObject = customDict.At('salesObject')
            tabTradeCreationSetting = customDict.At('tradeCreationSetting')
            if salesObject:
                salesTradingInfoDict['objectToQuote'] = {'type' : SalesTradingInfo.ObjectType(salesObject), 'oid' : str(salesObject.StorageId())}
            salesTradingInfoDict['tabTradeCreationSetting'] = tabTradeCreationSetting
            if numberOfComponents is not None:
                salesTradingInfoDict['numberOfComponents'] = numberOfComponents
        else:
            objectsToQuote = customDict.At('objectsToQuote')
            objectToQuote = objectsToQuote.At(componentName)
            if objectToQuote:
                salesTradingInfoDict['objectToQuote'] = {'type' : SalesTradingInfo.ObjectType(objectToQuote), 'oid' : str(objectToQuote.StorageId())}
        SalesTradingInfo.ApplyDict(imObject, salesTradingInfoDict)
    
    @staticmethod
    def ObjectToQuoteFromDict(objectToQuoteDict):
        objectToQuote = None
        objType = objectToQuoteDict['type']
        oid = int(objectToQuoteDict['oid'])
        if objType == 'DealPackage':
            objectToQuote = acm.FDealPackage[oid]
        elif objType == 'InstrumentPackage':
            objectToQuote = acm.FInstrumentPackage[oid]
        elif objType == 'Trade':
            objectToQuote = acm.FTrade[oid]
        elif objType =='Instrument':
            objectToQuote = acm.FInstrument[oid]
        else:
            raise Exception("Could not load object '%s' of type '%s'" % (oid, objType))
        return objectToQuote
    
    def __init__(self, imObject):
        self._objectToQuote = None
        self._imObject = imObject
        self._salesTradingInfoDict = SalesTradingInfo.ExtractDict(imObject)

    def ImObject(self):
        return self._imObject

    def SalesTradingInfoDict(self):
        return self._salesTradingInfoDict
    
    def Name(self):
        name = ''
        if self.SalesTradingInfoDict():
            name = self.SalesTradingInfoDict().get('name')
        return name
    
    def NumberOfComponents(self):
        nComponents = 0
        if self.SalesTradingInfoDict():
            nComponents = self.SalesTradingInfoDict().get('numberOfComponents')
        return nComponents
    
    def ObjectToQuote(self):
        if not self._objectToQuote:
            if self.SalesTradingInfoDict():
                objectToQuoteDict = self.SalesTradingInfoDict().get('objectToQuote')
                if objectToQuoteDict:
                    self._objectToQuote = SalesTradingInfo.ObjectToQuoteFromDict(objectToQuoteDict)
        return self._objectToQuote
    
    def TabTradeCreationSetting(self):
        tabTradeCreationSetting = None
        if self.SalesTradingInfoDict():
            tabTradeCreationSetting = self.SalesTradingInfoDict().get('tabTradeCreationSetting')
        return tabTradeCreationSetting
    
def FetchDefinition( definitionPath ):
    pathElements = str(definitionPath).split('.')
    module = pathElements[0]
    toReturn = __import__(module)
    for elem in pathElements[1:]:
        toReturn = getattr(toReturn, elem)
    
    return toReturn

def UnDecorate( acmObj ):
    if acmObj and hasattr(acmObj, 'DecoratedObject'):
        return acmObj.DecoratedObject()
    return acmObj

def ParseSuffixedFloat(input, suffix, formatter=None, ignoreCase=True):
    """ Helper method to parse suffixed strings to floats with formatter.

        The method will order suffixes by length, and loop through them.
        If a match is found, the parsed string before the suffix is parsed and returned.
        If no match could be found, None is returned.
        Example:
            >>> ParseSuffixedFloat("1000,0d", suffix=['delta', 'd'])
            1000.0

            >>> ParseSuffixedFloat("1000,0del", suffix=['delta', 'd'])
            None

            >>> ParseSuffixedFloat("1000,0delta", suffix=['delta', 'd'])
            1000.0

        The parser allows for the use of a mnemonic before the suffix.
        Example:
            >>> ParseSuffixedFloat("1 234,5kd", suffix=['d'])
            1234500.0
            
        Parser is not sensitive to whitespace between number and mnemonic,
        nor between mnemonic and suffix.
        Example:
            >>> ParseSuffixedFloat("1 234,5 k d", suffix=['d'])
            1234500.0

        Parameters
        ------------------
        input           String or float to be parsed
        formatter       Formatter to be used
            default: acm.GetDomain('double').DefaultFormatter()
        suffix          List of suffixes to match against.
        ignoreCase      Ignore case on 'suffix'
        
        Output
        -----------------
        None    If 'input' is not of type basestring,
                or 'suffix' could not be matched,
                or 'formatter' could not parse 'input' before 'suffix'
        Float   If 'suffix' could be matched and 'input' before could be parsed
    """
    if not isinstance(input, basestring):
        return None
    
    formatter = formatter or acm.GetDomain('double').DefaultFormatter()
    
                            # group0: the whole matched string (not used)
    regexp =  "(.*\d)"      # group1: beginning of string until last digit
    regexp += "(\s*)"       # group2: whitespace, 0 or more repetitions
    regexp += "([a-zA-Z]?)" # group3: any character, 0 or 1 repetitions (mnemonics)
    regexp += "(\s*)"       # group4: whitespace, 0 or more repetitions
    regexp += "(%s$)"       # group5: suffix at end of string

    flags = re.IGNORECASE if ignoreCase else 0
    
    # Try to match larger strings first
    orderedSuffix = suffix[:]
    orderedSuffix.sort(key=len, reverse=True)

    for sf in orderedSuffix:
        r = re.search(regexp%re.escape(sf), input.strip(), flags)
        if r is not None:
            numberStr, mnemonic = r.group(1), r.group(3)
            if not mnemonic:
                return ParseFloat(numberStr, formatter)
            elif ParseFloat(mnemonic, formatter):
                return ParseFloat(numberStr+mnemonic, formatter)
    return None

def ParseFloat(input, formatter=None):
    if isinstance(input, (int, long, float)):
        """
        Checking if 'input' is a python float/int/double is important as 
        most formatters will handle the python float 1.0 as a string "1.0". 
        This may lead to incorrect parsing in regions where . is considered 
        a thousand separator, as for example in Germany.
        """
        return input
    
    formatter = formatter or acm.GetDomain('double').DefaultFormatter()
    return formatter.Parse(input)
    
def InstrumentSetNew_Filter( ins ):
    return ins.InsType()=="Combination" or\
           ( ins.Otc() and not ins.MtmFromFeed() )

class RefreshDealPackageProxy(object):
    _instances = {}
    
    def __new__(cls, dp, *args, **kwargs):
        dp = UnDecorate(dp)
        if dp not in cls._instances:
            cls._instances[dp] = object.__new__(cls, *args, **kwargs)
            cls._instances[dp]._dp = dp
            cls._instances[dp]._observers = []
        return cls._instances[dp]
        
    def RegisterObserver(self, func):
        self._observers.append(func)
        
    def UnregisterObserver(self, func):
        if func in self._observers:
            self._observers.remove(func)
    
    def Refresh(self):
        if self._dp.Refresh():
            self.Notify()
            
    def Notify(self):
        for method in self._observers:
            method()
        self.NotifyChildPackages()
    
    def NotifyChildPackages(self):
        if not self._dp.IsKindOf(acm.FEditableObject):
            for child in self._dp.ChildDealPackages():
                rdpp = RefreshDealPackageProxy(child)
                rdpp.Notify()

def InstrumentPart(objMapping):
    ''' To be used in meta data key objMapping to indicate that it is an
        instrument package part. '''
    return ObjMappingSplitter().InstrumentPart(objMapping)

def DealPart(objMapping):
    ''' To be used in meta data key objMapping to indicate that it is a
        deal package part. '''
    return ObjMappingSplitter().DealPart(objMapping)

class ObjMappingSplitter(object):
    def __init__(self):
        self.m_trd = []
        self.m_ins = []
        self.m_originalOrder = []

    def __str__(self):
        return '|'.join(self.m_originalOrder)

    def __getattr__(self, value):
        return getattr(self.__str__(), value) #If method does not exist on self, search on the string

    def InstrumentPart(self, objMappingString):
        if objMappingString:
            self.m_originalOrder.append(objMappingString)
            self.m_ins.append(objMappingString)
        return self

    def DealPart(self, objMappingString):
        if objMappingString:
            self.m_originalOrder.append(objMappingString)
            self.m_trd.append(objMappingString)
        return self
    
    def _GetInstrumentPart(self):
        return '|'.join(self.m_ins)
    
    def _GetDealPart(self):
        return '|'.join(self.m_trd)
    
    @classmethod
    def Merge(cls, current, toMerge):
        toReturn = ObjMappingSplitter()
        if not isinstance(current, ObjMappingSplitter):
            current = ObjMappingSplitter().DealPart(current)
        if not isinstance(toMerge, ObjMappingSplitter):
            toMerge = ObjMappingSplitter().DealPart(toMerge)
            
        toReturn.InstrumentPart( 
            MergeMetaDataStrings(
                current._GetInstrumentPart(), 
                toMerge._GetInstrumentPart()))
                
        toReturn.DealPart( 
            MergeMetaDataStrings(
                current._GetDealPart(), 
                toMerge._GetDealPart()))
        return toReturn

def MergeMetaDataStrings(current, toMerge):
    if current == '':
        return toMerge
    if toMerge == '':
        return current
        
    prefix = ''
    if current.startswith('@'):
        prefix = '@'
        current = current.translate(None, '@')
    toMerge = toMerge.translate(None, '@')
    
    # Make sure no duplicates in toMerge
    toReturn = current.split('|')
    # Order is important. Iter toMerge backwards
    # and add as first in toReturn.
    for nextMethod in toMerge.split('|')[::-1]:
        if nextMethod not in toReturn:
            toReturn.insert(0, nextMethod)

    return prefix + '|'.join(toReturn)

def ReturnDomainDecorator(domain):
    def decorate(func):
        assert isinstance(domain, basestring)
        setattr(func, FUNCTION_DOMAIN_ATTRIBUTE, domain)
        return func
    return decorate

def UnpackPaneInfo(info):
    # Assumes only one key in dict.
    for key in info:
        return key, info[key]

def WrapAsTabControlList(layout):
    # For backwards compatibility, when only one tab control existed
    if layout and len(layout):
        paneInfo = layout[0]
        paneName, paneLayout = UnpackPaneInfo(paneInfo)
        if isinstance(paneLayout, basestring):
            layout = [{"Default": layout}]
    return layout

def IsAttributeInListDomain(dp, traitName):
    isList = False
    if dp.GetAttributeMetaData(traitName, 'type')() == 'list':
        isList = True
    elif dp.GetAttributeMetaData(traitName, 'type')() == 'FObject':
        domain = dp.GetAttributeMetaData(traitName, 'domain')()
        if domain.IsSubtype(acm.FCollection) and not domain.IsSubtype(acm.FString):
            isList = True
    return isList

def SetDealPackageSaveNew(dp, clearIdentifiers):
    if dp.IsStorageImage():
        dp.StorageSetNew()
        if clearIdentifiers:
            dp.OptionalId("")
    
def SetInstrumentPackageSaveNew(dp, clearIdentifiers):
    if dp.IsStorageImage():
        dp.StorageSetNew()
        if clearIdentifiers:
            dp.Name("")

def SetNewInstrument(ins, clearIdentifiers):
    if ins.IsStorageImage():
        ins.StorageSetNew()
        if clearIdentifiers:
            ins.InitializeUniqueIdentifiers()
    ins.PrepareSaveNew()
    
def SetNewTrade(trade, clearIdentifiers):
    if trade.IsStorageImage():
        trade.ClearTradeReferences()
    trade.PrepareSaveNew()
    if trade.IsInfant() and clearIdentifiers:
        trade.InitializeUniqueIdentifiers()

def SingleSetNew(acmObj, clearIdentifiers=True):
    if acmObj.IsKindOf( acm.FTrade ):
        SetNewTrade( acmObj, clearIdentifiers )
    elif acmObj.IsKindOf( acm.FInstrument ):
        SetNewInstrument( acmObj, clearIdentifiers )
    elif acmObj.IsKindOf( acm.FDealPackage ):
        SetDealPackageSaveNew( acmObj, clearIdentifiers )
    elif acmObj.IsKindOf( acm.FInstrumentPackage ):
        SetInstrumentPackageSaveNew( acmObj, clearIdentifiers )
    else:
        raise DealPackageException( 'Can not set new. Unsupported type %s' % (type(acmObj)) )

def SetNew(*listOfLists ):
    ''' To be used in OnSave to mark Trades, Instruments and
            Child dealpackages as new to get new instances.
            
            Example:
                def OnSave(self, config):
                    if not self.DealPackage().IsInfant():
                        SetNew( self.Trades(),
                                     self.Instruments(),
                                     self.ChildDealPackages()
                                    )
        '''
    for aList in listOfLists:
        for acmObj in aList:
            SingleSetNew( acmObj )

def SetNewWithoutClearingIdentifiers(*listOfLists ):
    ''' To be used in OnSave to mark Trades, Instruments and
            Child dealpackages as new to get new instances.
            Unique identifiers, such as name, external id etc are not cleared
            
            Example:
                def OnSave(self, config):
                    if not self.DealPackage().IsInfant():
                        SetNew( self.Trades(),
                                     self.Instruments(),
                                     self.ChildDealPackages()
                                    )
        '''
    for aList in listOfLists:
        for acmObj in aList:
            SingleSetNew( acmObj, clearIdentifiers=False )
    
def PrepareSaveOrSaveNew(obj):
    if obj.IsInfant():
        obj.PrepareSaveNew()
    else:
        obj.PrepareSave()
        
def SingleSetSave(acmObj):
    if acmObj.IsKindOf(acm.FInstrumentPackage):
        return
    if acmObj.IsKindOf(acm.FTrade) or acmObj.IsKindOf(acm.FInstrument) or acmObj.IsKindOf(acm.FDealPackage):
        PrepareSaveOrSaveNew( acmObj )
    else:
        raise DealPackageException( 'Can not prepare save. Unsupported type %s' % (type(acmObj)) )
            
def SetSave(*listOfLists ):
    ''' To be used in OnSave to prepare Trades, Instruments and
            Child dealpackages to be saved.
    '''
    for aList in listOfLists:
        for acmObj in aList:
            SingleSetSave( acmObj )
            
def FilterPackage(dp):
    for trade in reversed(dp.Trades()):
        if not dp.IsLiveTrade(trade):
            dp.RemoveTrade(trade)
            
    for childPackage in reversed(dp.ChildDealPackages()):
        if childPackage.Type() == "Life Cycle Event":
            dp.RemoveChildDealPackage(childPackage, True)
        else:
            if childPackage.AllOpeningTrades().Size() > 0:
                FilterPackage(childPackage)
                if childPackage.AllOpeningTrades().Size() == 0:
                    dp.RemoveChildDealPackage(childPackage, True)
    
def CreateCleanPackageCopy(origDp, fromOriginator=False, lockInTradeTime=False):
    def SingleMakeNew(dp):
        dp.StorageSetNew()
        dp.OptionalId('')
        for child in dp.OpeningDealPackages():
            SingleMakeNew(child)
    if origDp.IsDeal():
        definition = acm.DealCapturing.CustomInstrumentDefinition(origDp)
        trade = origDp.DealPackage().Trades().First()
        tradeCopy = trade.Originator() if fromOriginator else trade.StorageImage()
        copy = acm.Deal.WrapAsDecorator(tradeCopy, origDp.GUI(), definition)
        if lockInTradeTime:
            LockInTradeTime(copy)
        SetNew(copy.Trades())
    else:
        copy = origDp.Originator().Copy() if fromOriginator else origDp.Copy()
        if lockInTradeTime:
            LockInTradeTime(copy)
        SingleMakeNew(copy)
        SetNew(copy.AllOpeningTrades())
        FilterPackage(copy)
    return copy

def SetStatus(package, arguments):
    statusAttr = arguments.At('statusAttr', None)
    newStatus = arguments.At('newStatus', None)
    if newStatus:
        if statusAttr:
            package.SetAttribute(statusAttr, newStatus)
        else:
            raise DealPackageException("Argument 'statusAttr' not defined.")
    elif statusAttr:
        package.SetAttribute(statusAttr, 'Simulated')
    else:
        pass #Keep original status

def LockInTradeTime(correctPackage):
    ''' Lets the trade decorators know that trade time should not be updated at save '''
    if correctPackage.Trades().Size():
        tradeTime = correctPackage.Trades().First().TradeTime()
        for tradeDecorator in correctPackage.AllOpeningTrades():
            tradeDecorator.TradeTime(tradeTime)
    
def ValidateDealPackageToBeMirrored(dealPackage):
    # Multi trading possible
    if not dealPackage.MultiTradingEnabled():
        raise DealPackageException('Cannot mirror a non multi trading deal package')

    # Not infant
    if dealPackage.IsDeal():
        infantCheck = dealPackage.Trades().First()
    else:
        infantCheck = dealPackage
    if infantCheck.IsInfant():
        raise DealPackageException('Cannot mirror a deal / deal package that has not been saved')

    # Allowed trade Status
    hasNonVoidTrades = False
    for trade in dealPackage.AllOpeningTrades():
        if trade.Status() not in ['Void', 'Confirmed Void']:
            hasNonVoidTrades = True
            break
    if not hasNonVoidTrades:
        raise DealPackageException('Cannot mirror a deal package with only void trades')

    return True

def OpenTraitDialog(shell, obj, attribute, *dialogArgs):
    actionRetVal = None
    if obj:
        dialogRetVal = None
        actionRetVal = None
        dialogCb = obj.GetAttributeMetaData(attribute, 'dialog')
        if dialogCb:
            dialog = dialogCb(*dialogArgs)
            if dialog:
                dialogRetVal = dialog.ShowDialog(shell)
        action = obj.GetAttributeMetaData(attribute, 'action')
        if action:
            if dialogRetVal:
                actionRetVal = action(dialogRetVal)
            else:
                actionRetVal = action()
    return actionRetVal
