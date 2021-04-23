import acm
from DealPackageUtil import DealPackageException, FormatException, UnDecorate
from DealCommands import SwitchLegsCommand

class HelperInterface(object):
    CreateFunc = None
    DEFAULT_DEFINITION = ''
    def Decorate(self, subject, gui): raise NotImplementedError
    def Open(self, subject, gui): raise NotImplementedError
    def Save(self, subject, config): raise NotImplementedError
    def DefinitionDisplayName(self, subject): raise NotImplementedError
    def MultiTradingEnabled(self, subject): raise NotImplementedError
    def Name(self, subject): raise NotImplementedError
    def DeleteSubject(self, subject, deleteTrades, trades): raise NotImplementedError
    def DeleteTrade(self, subject, trade): raise NotImplementedError
    def Trades(self, subject): raise NotImplementedError
    def IsDeletedMsg(self, subject): raise NotImplementedError
    def Originator(self, subject): raise NotImplementedError
    def Definition(self, subject): raise NotImplementedError
    def Commands(self, subject): return {}
    
    def CreateSubject(self, definition, gui, *optArgs):
        subject = None
        try:
            subject = self.CreateFunc(definition, gui, *optArgs)
        except Exception as e:
            acm.LogAll('Could not create subject from definition "%s": %s' % (definition, e))
            msg = FormatException(e)
            gui.GenericMessage(msg)
            subject = self.CreateFunc(self.DEFAULT_DEFINITION, gui, *optArgs)
        return subject  


class DealPackageHelper(HelperInterface):
    CreateFunc = acm.DealPackage.NewAsDecorator
    DEFAULT_DEFINITION = 'Free Form'

    def Decorate(self, subject, gui):
        decorator = acm.FBusinessLogicDecorator.WrapObject(UnDecorate(subject), gui)
        return decorator

    def Open(self, obj, gui, preserveObject=True):
        obj = UnDecorate( obj ) # to enssure we have the right GUI on the decorator
        fromInsPackage = False
        if obj.IsKindOf(acm.FTrade):
            package = obj.DealPackage()
        elif obj.IsKindOf(acm.FInstrumentPackage):
            package = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(obj, gui)
            fromInsPackage = True
        else:
            package = self.Decorate(obj, gui)
        if not package:
            raise DealPackageException('Could not create deal package from ' + obj.ClassName() + ' ' + str(obj.Originator().StorageId()))
        if not fromInsPackage:
            if not self.Originator(package):
                if preserveObject:
                    package = package.Copy()
            else:
                if preserveObject:
                    package = package.Edit()
                else:
                    package = self.Decorate(package.Originator(), gui).Edit()
        return package

    def Save(self, subject, config):
        if config is None:
            config = acm.FDealPackageSaveConfiguration()
            config.DealPackage('Save')
            config.InstrumentPackage('Save')
        self.__Validate(subject, config)
        return subject.Save(config)
    
    def __Validate(self, subject, config):
        aspect = "DealPackage"
        if config.DealPackage() == "Exclude":
            aspect = "InstrumentPackage"
        isValid = subject.IsValid(aspect)
        if not (isinstance(isValid, bool) and isValid == True):
            errorStr = 'Validation Errors:\n'
            for error in isValid:
                errorStr = errorStr + '- ' + str(error) + '\n'
            raise DealPackageException(errorStr)

    def DefinitionDisplayName(self, subject):
        return str(subject.DefinitionDisplayName())

    def MultiTradingEnabled(self, subject):
        return subject.GetAttribute('multiTradingEnabled')
        
    def Name(self, subject):
        return subject.Name()
    
    def ExcludeReference(self, reference):
        excludeRef = reference.IsKindOf(acm.FDealPackageTradeLink) or reference.IsKindOf(acm.FPayment) or reference.IsKindOf(acm.FMatchingTradeLink) or reference.IsKindOf(acm.FTradeAlias) or reference.IsKindOf(acm.FAdditionalInfo)
        return excludeRef

    def CheckTradeReferences(self, trade):
        referenced = False
        referencesStr = "Trade " + str(trade.OriginalOrSelf().Oid()) + " cannot be deleted, references exists: \n"
        referencesIn = trade.OriginalOrSelf().ReferencesIn()
        if referencesIn.Size():
            for reference in referencesIn:
                if not self.ExcludeReference(reference):
                    referencesStr += str(reference.RecordType()) + " " + str(reference.Oid()) + "\n"
                    referenced = True
        if referenced:
            raise DealPackageException(referencesStr)
    
    def DeleteSubject(self, subject, deleteTrades, trades): 
        toOpen = None
        if subject.IsInfant():
            raise DealPackageException('Not possible to delete unsaved dealpackage')
        
        if deleteTrades:
            for trade in trades:
                self.CheckTradeReferences(trade)
        
        if subject.IsKindOf(acm.FDealPackage):
            multiTrading = subject.GetAttribute('multiTradingEnabled')
            original = subject.Original()
            insPackage = original.InstrumentPackage()
            if str(subject.Definition().CustomApplicationName()) == 'FX Option Pricer':
                original = original.Edit()
            original.Delete(True, deleteTrades)
            if not insPackage.IsDeleted() and multiTrading:
                toOpen = insPackage
        else:
            subject.Delete()
        return toOpen
        
    def DeleteTrade(self, subject, trade):
        self.CheckTradeReferences(trade)
        if trade.IsInfant():
            subject.DeleteTrade(trade)
        else:
            if not subject.Original():
                raise DealPackageException('Not possible to delete unsaved dealpackage')
            if not trade.Original():
                raise DealPackageException('Not possible to delete unsaved trade')
            original = subject.Original()
            if str(subject.Definition().CustomApplicationName()) == 'FX Option Pricer':
                original = original.Edit()
            if not original.DeleteTrade(trade.Original()):
                raise DealPackageException('Not possible to delete trade')

    def Trades(self, subject):
        return subject.Trades()
        
    def IsDeletedMsg(self, subject):
        return "Deal Package '%s' has been deleted in the database." % self.Name(subject)
    
    def Originator(self, subject):
        if subject.Originator().Oid() > 0:
            return subject.Originator()
        elif subject.InstrumentPackage().Originator().Oid() > 0:
            return subject.InstrumentPackage().Originator()
        else:
            return None
    
    def Definition(self, subject):
        return subject.Definition()


class DealHelper(DealPackageHelper):
    CreateFunc = acm.Deal.NewAsDecorator
    DEFAULT_DEFINITION = 'Deal Default'

    def Open(self, obj, gui, preserveObject = True):
        obj = UnDecorate( obj ) # to enssure we have the right GUI on the decorator
        if obj.IsKindOf(acm.FTrade) or obj.IsKindOf(acm.FInstrument):
            package = acm.Deal.WrapAsDecorator(obj, gui, self.Definition(obj).Name())
        else:
            definition = self.Definition(obj)
            package = self.Decorate(obj, gui)
            if definition.BaseConfiguration().Name() == acm.FSymbol('FX Cash') or not self.Originator(package):
                if preserveObject:
                    package = package.Copy()
            else:
                if preserveObject:
                    package = package.Edit()
                else:
                    package = acm.Deal.WrapAsDecorator(self.Originator(obj), gui, definition.Name())        
        if not package:
            raise DealPackageException('Could not create deal from ' + obj.ClassName() + ' ' + str(obj.Originator().StorageId()))
        return package
        
    def IsDeletedMsg(self, subject):
        return "Instrument/Trade %s has been deleted in the database." % subject.Name()
    
    def Originator(self, subject):
        return self._OriginatorInsOrTrd(subject)
        
    def _OriginatorInsOrTrd(self, subject):
        instrumentOrTrade = None
        trade = self._Trade(subject)
        instrument = self._Instrument(subject)
        if trade and trade.Originator().Oid() > 0:
            instrumentOrTrade = trade.Originator()
        elif instrument and instrument.Originator().Oid() > 0:
            instrumentOrTrade = instrument.Originator()
        return instrumentOrTrade
        
    def _Trade(self, subject):
        return subject.Trades().First()
    
    def _Instrument(self, subject):
        return subject.Instruments().First()

    def Definition(self, subject):
        return acm.DealCapturing.CustomInstrumentDefinition(subject)
        
    def Commands(self, subject):
        return {'switchLegs':SwitchLegsCommand(dealPackage=subject)}
        
    def DeleteSubject(self, subject, deleteTrades, trades):
        trade = self._Trade(subject)
        ins = self._Instrument(subject) 
        toOpen = None
        if trade.IsInfant() and ins.IsInfant():
            raise DealPackageException('Not possible to delete unsaved trade/instrument.')
        if trade.IsInfant():
            ins.Delete()
        else:
            self.CheckTradeReferences(trade)
            subject.Delete(True, True)
            if not ins.Originator().IsDeleted() and subject.GetAttribute('multiTradingEnabled'):
                toOpen = ins.Originator()
        return toOpen


class EditableObjectHelper(HelperInterface):
    CreateFunc = acm.EditableObject.New
    DEFAULT_DEFINITION = 'Default'

    def Decorate(self, subject, gui):
        definitionName = subject.DefinitionName()
        subject = UnDecorate(subject.Object())
        return acm.EditableObject().Wrap(definitionName, subject, gui)
    
    def CreateSubjectFromObject(self, obj, gui):
        return self.Decorate(UnDecorate(obj), gui)

    def Open(self, subjectToOpen, gui, perserveObject = True):
        subject = None
        if subjectToOpen.IsKindOf(acm.FEditableObject):
            editObject = subjectToOpen.Object()
            if editObject and editObject.StorageId() > 0:
                subjectToOpen = editObject
            else:
                subject = subjectToOpen
        if not subject:
            subjectToOpen = UnDecorate(subjectToOpen)
            definition = acm.EditableObjectDefinition.DefinitionFromClass(subjectToOpen.Class())
            subject = acm.EditableObject().Wrap(definition.Name(), subjectToOpen, gui)
        return subject

    def Save(self, subject, config):
        if config and config.DealPackage() == "SaveNew":
            return subject.SaveNew()
        else:
            return subject.Save()

    def DefinitionDisplayName(self, subject):
        return subject.DefinitionDisplayName()

    def MultiTradingEnabled(self, subject):
        return False
        
    def Name(self, subject): 
        return subject.Object().Name()

    def DeleteSubject(self, subject, deleteTrades, trades):
        if subject.Object().IsInfant():
            raise DealPackageException('Not possible to delete unsaved editable object')
        else:
            subject.Object().Original().Delete()
            
    def Trades(self, subject):
        return []
        
    def Originator(self, subject):
        if subject.IsKindOf(acm.FEditableObject):
            subject = subject.Object()
        if subject.Originator().Oid() > 0:
            return subject.Originator()
        else:
            return None

    def IsDeletedMsg(self, subject):
        return "Object has been deleted in the database."

    def Definition(self, subject):
        return acm.EditableObjectDefinition.DefinitionFromClass(UnDecorate(subject.Object()).Class())

def CreateControlCallback(delegate):

    def ParseControlTokenCallback(delegate, entry, xArg):
        try:
            if entry == 'fill':
                delegate.HandleFill(xArg)
            elif entry[0:6] == 'space(':
                size = int(entry.split('(')[1].split(')')[0].strip())
                delegate.HandleSpace(xArg, size)
            elif ')' in entry or ']' in entry or '}' in entry:
                delegate.HandleEndBox(xArg)
            else:
                traitName = entry
                extraArg = None
                if '(' in entry:
                    raise Exception("'(' is not a valid delimiter for custom boxes.")
                elif '{' in entry:
                    traitName = entry.split('{')[0]
                    extraArg = '{'
                elif '[' in entry:
                    traitName = entry.split('[')[0]
                    extraArg = '['
                delegate.HandleControl(xArg, traitName, extraArg)
        except Exception as e:
            msg = "Failed to parse layout, name '%s' not recognized: '%s'" % (entry, e)
            raise DealPackageException(msg)

    # Bind delegate to callback signature
    import functools
    partial = functools.partial(ParseControlTokenCallback, delegate)
    
    # Wrap in lambda since ACM does not understand partial functions
    return lambda *args, **kwargs: partial(*args, **kwargs)

DEBUG = False

def Log(txt):
    if DEBUG:
        acm.Log(txt)

class ListAttributeWrapper(object):
    ''' Simplified access to column names, method chains, formatters etc '''

    def __init__(self, dealPackage, traitName):
        self._traitName = traitName
        self._dealPackage = dealPackage
        self._listColumnInfo = acm.FArray()
        self.CreateColumns()
        self._addNewItemRule = self.GetTraitMetaData('addNewItem')()

    def TraitName(self):
        return self._traitName

    def GetTraitMetaData(self, metaKey):
        return self._dealPackage.GetAttributeMetaData(self.TraitName(), metaKey)

    def AddNewItemLast(self):
        return 'Last' in self._addNewItemRule

    def ResortListOnChanged(self):
        return 'Sorted' in self._addNewItemRule

    def GetClassUiProperties(self):
        uiProperties = None
        try:
            domain = self.GetTraitMetaData('elementDomain')()
            uiProperties = 'Name' if domain == acm.FString else domain.UiProperties()
            if not uiProperties:
                uiProperties = 'Name'
        except Exception as e:
            msg = 'GetClassUiProperties failed: ' + str(e)
            Log(msg)
        return uiProperties

    def GetNameFromColumn(self, aClass, methodChain):
        colName = None
        colDef = acm.GetDefaultContext().GetExtension(acm.FColumnDefinition, aClass, methodChain)
        if colDef:
            colName = colDef.Value().At('ColumnName', None)
        return colName
    
    def GetNameFromMethod(self, aClass, methodChain):
        return acm.PropertyBinder().DisplayName(aClass, methodChain)
        
    def GetColumnName(self, domain, methodChain):
        columnName = self.GetNameFromColumn(domain, methodChain)
        if columnName is None:
            columnName = self.GetNameFromMethod(domain, methodChain)
        if columnName is None:
            columnName = methodChain
        return columnName

    def GetColumnFormatter(self, domain, methodChain):
        formatter = acm.PropertyBinder().FindFormatter(domain, methodChain, None)
        if not formatter:
            formatter = domain.DefaultFormatter() if domain else None
        return formatter

    def CreateColumnsFromUiProperties(self):
        try:
            domain = self.GetTraitMetaData('elementDomain')()
            for methodChain in self.GetClassUiProperties().split(' '):
                if methodChain:
                    columnName = self.GetColumnName(domain, methodChain)
                    formatter = self.GetColumnFormatter(domain, methodChain)
                    self._listColumnInfo.Add((methodChain, columnName, formatter))
        except Exception as e:
            msg = 'CreateColumnsFromUiProperties failed: ' + str(e)
            Log(msg)
        return self._listColumnInfo

    def CreateArrayFromMetaDataDict(self, columns):
        try:
            for column in columns:
                columnName = column.get('label')
                methodChain = column.get('methodChain')
                formatter = column.get('formatter')
                if formatter:
                    getStr = 'formats/' + formatter
                    formatter = acm.Get(getStr)
                else:
                    domain = self.GetTraitMetaData('elementDomain')()
                    formatter = acm.PropertyBinder().FindFormatter(domain, methodChain, None)
                self._listColumnInfo.Add((methodChain, columnName, formatter))
        except Exception as e:
            msg = 'CreateArrayFromMetaDataDict failed: ' + str(e)
            Log(msg)
        return self._listColumnInfo

    def CreateColumns(self):
        columns = self.GetTraitMetaData("columns")()
        if columns:
            columns = self.CreateArrayFromMetaDataDict(columns)
        if not columns:
            columns = self.CreateColumnsFromUiProperties()
        return columns

    def GetColumns(self):
        return self._listColumnInfo
        
    def GetColumnNames(self):
        return [columnName for _, columnName, _ in self.GetColumns()]
        
    def IsFObject(self, obj):
        return hasattr(obj, 'StringKey')

    def GetMethodValue(self, obj, methodChain):
        for method in methodChain.split('.'):
            if method:
                obj = getattr(obj, method)()
        return obj

    def GetValueFromMethod(self, obj, methodChain):
        try:
            if self.IsFObject(obj) and methodChain:
                obj = self.GetMethodValue(obj, methodChain)
        except Exception as e:
            msg = 'GetValueFromMethod failed: ' + str(e)
            Log(msg)        
            
        return obj

    def GetFormattedValueFromMethod(self, val, column):
        methodChain = column.At(0)
        formatter = column.At(2)
        val = self.GetValueFromMethod(val, methodChain)
        if formatter:
            val = formatter.Format(val)
        else:
            if self.IsFObject(val):
                if hasattr(val, 'Name'):
                    val = val.Name()
                elif hasattr(val, 'StringKey'):
                    val = val.StringKey()
                else:
                    val = str(val)
        return val
 
    def GetIconFromObject(self, obj):
        icon = None
        if self.IsFObject(obj):
            icon = obj.Icon()
        return icon
