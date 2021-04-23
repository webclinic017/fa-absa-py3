import acm
from DealPackageUtil import DealPackageException, FormatException, UnDecorate, RefreshDealPackageProxy
from UxHelpers import DealPackageHelper, DealHelper, EditableObjectHelper

def ServerUpdateCB(self):
    self.DoServerUpdate()
    
def EndBlockUpdatesCB2(self):
    self.DoEndBlockUpdates()
    
def EndBlockUpdatesCB(self):
    acm.AsynchronousCall(EndBlockUpdatesCB2, [self])


class UxWrapper(object):
    
    def __init__(self, uxHelperClass, defaultDefinition=None):
        self.helper = uxHelperClass()
        self.defaultDefinition = defaultDefinition or self.helper.DEFAULT_DEFINITION
        self.subject = None
        self.initObject = None
        self.blGUI = acm.FBusinessLogicGUIDefault()
        self.isModified = None
        self.allTrades = None
        self.refreshProxy = None
        self.subscribedOriginators = []
        self.blockUpdates = False
        self.uiSettings = None
        self.originatorChangedCb = None
        self.originatorDeletedCb = None
        self.restoreUiSettingsCb = None
        self.storeUiSettingsCb = None
        self.setEntityCb = None
        self.dialogCb = None
        self.openCb = None
        self.commands = None
        self._getAttributeCallback = None
        self._getAttributeMetaDataCallback = None
        
    # #################
    # API
    # #################
    def Subject(self):
        return self.subject
    
    def InitObject(self, obj):
        self.initObject = obj
    
    def HasShell(self):
        hasShell = False
        if self.blGUI:
            hasShell = not self.blGUI.IsKindOf(acm.FBusinessLogicGUIDefault)    
        return hasShell
        
    def Originator(self):
        ''' Get originator if originator of subject is not infant, else None'''
        originator = None
        if self.subject:
            originator = self.helper.Originator(self.subject)
        return originator
    
    def GetAttribute(self, traitName):
        return self.Subject().GetAttribute(traitName)
    
    def GetAttributeMetaData(self, traitName, metaKey):
        return self.Subject().GetAttributeMetaData(traitName, metaKey)
    
    def RegisterOnOriginatorChanged(self, callback):
        self.originatorChangedCb = callback

    def RegisterOnOriginatorDeleted(self, callback):
        self.originatorDeletedCb = callback
        
    def RegisterOnStoreUiSettings(self, callback):
        self.storeUiSettingsCb = callback

    def RegisterOnRestoreUiSettings(self, callback):
        self.restoreUiSettingsCb = callback

    def RegisterOnSetEntity(self, callback):
        self.setEntityCb = callback
    
    def RegisterOpenCallback(self, callback):
        self.openCb = callback
    
    def RegisterOpenCbOnSubject(self):
        if self.openCb:
            uxCallbacks = self.subject.GetAttribute('uxCallbacks')
            if not uxCallbacks:
                uxCallbacks = acm.FDictionary()
            uxCallbacks.AtPut('open', self.openCb)
            self.subject.SetAttribute('uxCallbacks', uxCallbacks)

    def RegisterDialogCallback(self, callback):
        self.dialogCb = callback

    def RegisterDialogCbOnSubject(self):
        if self.dialogCb:
            uxCallbacks = self.subject.GetAttribute('uxCallbacks')
            if not uxCallbacks:
                uxCallbacks = acm.FDictionary()
            uxCallbacks.AtPut('dialog', self.dialogCb)
            self.subject.SetAttribute('uxCallbacks', uxCallbacks)

    def DefaultDefinition(self):
        ''' Get default definition '''
        return self.defaultDefinition
        
    def SetDefaultDefinition(self, defaultDefinition):
        ''' Update default definition to be used for example when doing delete
            on current subject. '''
        self.defaultDefinition = defaultDefinition

    def RefreshProxy(self):
        return self.refreshProxy

    def SetShell(self, shell):
        ''' Set FUxShell and use FBusinessLogicGUIShell '''
        self.blGUI = acm.FBusinessLogicGUIShell()
        self.blGUI.SetFUxShell(shell)
        if not self.initObject:
            self.Open( self.CreateSubject(), None, False )
        else:
            if hasattr(self.subject, 'IsDeal') and self.subject.IsDeal():
                self.Open( UnDecorate(self.initObject) )
            else:
                self.Open( UnDecorate(self.initObject).Originator() )
            self.initObject = None
    
    def IsModified(self):
        return self.isModified and self.subject.IsModified()

    def AppCaption(self):
        return self.subject.AppCaption()

    def DefinitionName(self):
        return self.subject.DefinitionName()

    def Name(self):
        return self.helper.Name(self.subject)

    def AdditionalSubject(self, subject):
        if subject.IsKindOf('FTrade'):
            return subject.Instrument()
        elif subject.IsKindOf('FDealPackage'):
            return subject.InstrumentPackage()
        else:
            return None

    def Subscribe(self):
        self.Unsubscribe()
        if self.subject:
            self.subject.AddDependent(self)
            self.isModified = False
        originator = UnDecorate(self.Originator())
        if originator:
            self.subscribedOriginators.append(originator)
            originator.AddDependent(self)
            additionalSubject = self.AdditionalSubject(originator)
            if additionalSubject:
                self.subscribedOriginators.append(additionalSubject)
                additionalSubject.AddDependent(self)

    def Unsubscribe(self):
        if self.subject:
            self.subject.RemoveDependent(self)
            self.isModified = False
        for originator in self.subscribedOriginators:
            originator.RemoveDependent(self)
        self.subscribedOriginators = []
            
    def Dismantle(self):
        if self.subject:
            self.subject.Dismantle()

    def BlockUpdates(self):
        self.blockUpdates = True
        self.__StoreUiSettings()
        acm.AsynchronousCall(EndBlockUpdatesCB, [self])

    def UpdatesBlocked(self):
        return self.blockUpdates

    def CreateSubject(self, definition=None, *optArgs):
        ''' Create new subject of definition. '''
        helper = self.helper
        if definition and not isinstance(definition, str):
            helper = self.__GetHelperForDefinition(definition)
            definition = str(definition.Name())
        definition = definition or self.DefaultDefinition()
        return helper.CreateSubject(definition, self.blGUI, *optArgs)
    
    def DeleteSubject(self):
        ''' Delete current subject and create one of default type '''
        self.Delete(deleteTrades=False)
        
    def Open(self, obj, onExceptionCb = None, preserveObject=True):
        ''' Open subject '''
        self.__UpdateHelperFromObject(obj)
        try:
            subject = self.helper.Open(obj, self.blGUI, preserveObject)
        except Exception as e:
            if onExceptionCb:
                onExceptionCb()
            raise DealPackageException(str(e))
        self.__Subject(subject)
    
    def SetSubject(self, obj):
        self.__StoreUiSettings()
        self.__UpdateHelperFromObject(obj)
        self.__Subject(obj)

    def Save(self, config=None):
        self.__StoreUiSettings()
        self.RegisterDialogCbOnSubject()
        result = self.helper.Save(self.subject, config)
        self.isModified = False
        if result:
            self.Open(result.First(), None, False)

    def DefinitionDisplayName(self):
        return self.helper.DefinitionDisplayName(self.subject)
            
    def MultiTradingEnabled(self):
        return self.helper.MultiTradingEnabled(self.subject)
    
    def Commands(self):
        if not self.commands:
            self.commands = self.helper.Commands(self.subject)
        return self.commands
    
    # #################
    # End of API
    # #################
    # DealPackage/Deal Specifics
    # #################

    def AllTrades(self):
        return self.allTrades

    def InstrumentPackageName(self):
        name = ''
        if hasattr(self.subject, 'InstrumentPackage') and self.subject.InstrumentPackage():
            name = self.subject.InstrumentPackage().Name()
        return name

    def SortedTradeActionKeys(self):
        return self.subject.TradeActionKeys().Sort()

    def TradeActionAt(self, key):
        return self.subject.TradeActionAt(key)

    def TradeActions(self):
        return [self.TradeActionAt(key) for key in self.SortedTradeActionKeys()]
        
    def SortedCustomActionKeys(self):
        return self.subject.CustomActionKeys().Sort()

    def CustomActionAt(self, key):
        return self.subject.CustomActionAt(key)

    def CustomActions(self):
        return [self.CustomActionAt(key) for key in self.SortedCustomActionKeys()]

    def AddTrade(self, trade):
        if self.subject.IncludesTrade(trade):
            raise DealPackageException('Trade already included in Deal Package')
        else:
            trade = self.subject.AddTrade(trade)
            self.AllTrades().Add(trade)

    def VoidTrades(self):
        for trade in self.AllTrades():
            trade.Status('Void')

    def RemoveTrade(self, trade):
        self.subject.RemoveTrade(trade)
        self.AllTrades().Remove(trade)
        
    def DeleteTrade(self, trade):
        self.helper.DeleteTrade(self.subject, trade)
        self.RemoveTrade(trade)

    def IsDealPackageEmpty(self):
        return self.AllTrades().Size() == 0

    def Delete(self, deleteTrades):
        toOpen = self.helper.DeleteSubject(self.subject, deleteTrades, self.AllTrades())
        if toOpen:
            self.Open(toOpen)
        else:
            self.SetSubject( self.CreateSubject() )

    # #################
    # End of DealPackage/Deal Specifics
    # #################

    def DoEndBlockUpdates(self):
        self.blockUpdates = False
    
    def DoServerUpdate(self):
        originator = self.Originator()
        if originator and originator.IsDeleted():
            self.SetSubject( self.CreateSubject() )
            if self.originatorDeletedCb:
                self.originatorDeletedCb( self.helper.IsDeletedMsg(originator) )
            return # Exit
        
        revert = True
        if self.originatorChangedCb and self.IsModified():
            revert = self.originatorChangedCb()
        if revert:
            self.Revert()

    def Revert(self):
        self.BlockUpdates()
        revertSubject = self.Originator()
        if not revertSubject:
            revertSubject = self.subject
        self.Open(revertSubject)
        
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        changeDueToDependentSet = True if parameter and parameter.IsKindOf(acm.FPersistentSet) else False
        if sender in self.subscribedOriginators:
            if not changeDueToDependentSet:
                if not self.blockUpdates or str(aspectSymbol) == 'delete':
                    self.BlockUpdates()
                    acm.AsynchronousCall(ServerUpdateCB, [self])
        else:
            self.isModified = True
            
    def __Subject(self, subject):
        self._getAttributeMetaDataCallback = None
        self._getAttributeCallback = None
        subject.CalculationRefreshPeriod(1000)
        self.Unsubscribe()
        self.Dismantle()
        self.subject = self.helper.Decorate(subject, self.blGUI)
        self.allTrades = acm.FSet()
        for trade in self.helper.Trades(subject):
            self.AllTrades().Add(trade.Trade())
        self.SetDefaultDefinition( self.helper.Definition(self.subject).Name() )
        self.Subscribe()
        self.__RestoreUiSettings()
        self.__UpdateCommands()
        self.refreshProxy = RefreshDealPackageProxy(self.subject)
        if self.setEntityCb:
            self.setEntityCb()
        self.RegisterOpenCbOnSubject()
        self.RegisterDialogCbOnSubject()

    def __StoreUiSettings(self):
        if self.subject:
            self.uiSettings = {'definition'          : self.subject.Definition(),
                                'uiViewModeIsSlim'    : self.subject.GetAttribute('uiViewModeIsSlim'),
                                'autoRefreshCalc'     : self.subject.GetAttribute('autoRefreshCalc')}
            self.uiSettings.update(self.__CallStoreUiSettings())
        
    def __RestoreUiSettings(self):
        if self.uiSettings and self.subject and self.uiSettings['definition'] == self.subject.Definition():
            self.subject.SetAttribute('uiViewModeIsSlim', self.uiSettings['uiViewModeIsSlim'])
            self.subject.SetAttribute('autoRefreshCalc', self.uiSettings['autoRefreshCalc'])
            if 'showGraphInitially' in self.uiSettings:
                self.subject.SetAttribute('showGraphInitially', self.uiSettings['showGraphInitially'])
            if 'showSheetInitially' in self.uiSettings:
                self.subject.SetAttribute('showSheetInitially', self.uiSettings['showSheetInitially'])
            self.__CallRestoreUiSettings()

    def __CallStoreUiSettings(self):
        if self.storeUiSettingsCb:
            return self.storeUiSettingsCb()
        else:
            return {}

    def __CallRestoreUiSettings(self):
        if self.restoreUiSettingsCb:
            self.restoreUiSettingsCb(self.uiSettings)
    
    def __UpdateCommands(self):
        for key in self.Commands():
            cmd = self.Commands()[key]
            cmd.SetDealPackage(self.subject)
    
    def __GetHelperForDefinition(self, definition):
        helper = None
        if definition and hasattr(definition, 'IsKindOf'):
            if definition.IsKindOf(acm.FEditableObjectDefinition): # Has to be before check for FDealPackageDefinition
                helper = EditableObjectHelper()
            elif definition.IsKindOf(acm.FDealPackageDefinition):
                helper = DealPackageHelper()
            elif definition.IsKindOf(acm.FCustomInstrumentDefinition):
                helper = DealHelper()
        return helper
    
    def __UpdateHelperFromObject(self, obj):
        helper = None
        if obj.IsKindOf(acm.FTrade) or obj.IsKindOf(acm.FInstrument) or obj.IsKindOf(acm.FPackageBase):
            isDeal  = obj.IsKindOf(acm.FTrade) and not obj.OpeningDealPackage()
            isDeal |= obj.IsKindOf(acm.FInstrument)
            isDeal |= (obj.IsKindOf(acm.FPackageBase) and obj.IsDeal())
            if isDeal:
                helper = DealHelper
            else:
                helper = DealPackageHelper
        else:
            helper = EditableObjectHelper
        if helper and (not self.helper or self.helper.__class__ != helper):
            self.commands = None
            self.helper = helper()
