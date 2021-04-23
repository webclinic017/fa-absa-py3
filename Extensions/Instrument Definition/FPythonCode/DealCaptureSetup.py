

import acm

'''**************************************************************************
* 
* Usage:
*    Intended to run from 
*        - Deal Package Create Function
*        - When running start application for a Custom Instrument Definition
* 
* Data Specification:
* 
* - Additional Info Specifications:
*      Definition:
*         ('Record Type', 'Field Name', 'Data Type', 'Description', 'Data Type Group', ['Record Sub Type'], 'DefaultValue', 'Mandatory')
*      Example:
*        [('Instrument', 'LeveragedNotional', 'Double', 'Notional Amount 2', 'Standard', [], None, False)]
*      Note:
*        Data Type should be specified with the name, not the enum value
* 
* - Choice List Specifications
*      Definition:
*         ('List', 'Entry', 'Description')
*      Example:
*        [('MASTER', 'Valuation Extension', ''),
*         ('Valuation Extension', 'udmcSF', 'Target Redemption Forward')]
* 
* - Context Links
*      Definition:
*         ('Context', 'Type', 'Name', 'Mapping Type', 'Item')
*      Example:
*         [('Global', 'Valuation Extension', 'udmcSF', 'Val Group', 'valGroupSF')]
*         
* - Custom Methods
*      Definition
*         ('Class Name', 'FCustomMethod Name', 'Method Name')
*      Example:
*         [('FTrade', 'TradeDirection', 'Direction')]
*
* - FComponents
*      Definition
*         ('Component Name', 'Comp Type')
*      Example:
*         [('Straddle', 'Application')]
*
**************************************************************************'''

def _PrivateRunSetupFunction(definitionName, shell, functionPath):
    try:
        pathElements = str(functionPath).split('.')
        module = pathElements[0]
        func = __import__(module)
        for elem in pathElements[1:]:
            func = getattr(func, elem)
            
        setUp = DataSetUpUxShell(definitionName, shell)
        func(setUp)
        setUp.SetUp()
    except Exception as e:
        msg = 'Could not open %s:\n%s' %(definitionName, str(e))
        acm.UX().Dialogs().MessageBoxInformation(shell, msg)
        raise
    

'''**************************************************************************
* SetUpBase Base Class
**************************************************************************'''
class SetUpBase(object):
    def _GetExisting(self):
        raise Exception('_GetExisting must be implemented')
        
    def _CreateNew(self):
        raise Exception('_CreateNew must be implemented')
        
    def _RestartNeeded(self):
        raise Exception('_RestartNeeded must be implemented')
    
    def Description(self):
        raise Exception('Description must be implemented')

    def IsSetUp(self):
        return self._GetExisting() != None

    def DoSetUp(self):
        if not self.IsSetUp():
            self._CreateNew()   
    
    def IsRestartNeeded(self):
        restartNeeded = False
        if self.IsSetUp():
            restartNeeded = self._RestartNeeded()   
        return restartNeeded
        
'''**************************************************************************
* AddInfoSetUp
**************************************************************************'''
class AddInfoSetUp(SetUpBase):
    def __init__(self, recordType, fieldName, dataType, description, dataTypeGroup, subTypes, defaultValue, mandatory):
        self._recordType = recordType
        self._fieldName = fieldName
        self._dataType = dataType
        self._descr = description
        self._dataTypeGroup = dataTypeGroup
        self._defaultValue = defaultValue
        self._subTypes = subTypes
        self._dataTypeType = acm.GetDomain('enum(B92%sType)' % dataTypeGroup.replace('Ref', '')).Enumeration(dataType)
        self._mandatory = mandatory
        
    def _GetExisting(self):
        return acm.FAdditionalInfoSpec[self._fieldName]
        
    def _CreateNew(self):
        spec = acm.FAdditionalInfoSpec()
        spec.FieldName(self._fieldName)
        spec.DefaultValue(self._defaultValue)
        spec.Description(self._descr)
        spec.RecType(self._recordType)
        for subType in self._subTypes:
            spec.AddSubType(subType)
        spec.DataTypeGroup(self._dataTypeGroup)
        spec.DataTypeType(self._dataTypeType)
        spec.Mandatory(self._mandatory)
        spec.Commit()
        acm.Log('Created Additional info %s' % self._fieldName)
        
    def _RestartNeeded(self):
        restartNeeded = False
        method = self._fieldName.replace(' ', '_')
        if method and len(method):
            method = method[0].upper() + method[1:]
        if self._subTypes:
            for subType in self._subTypes:
                klass = getattr(acm, 'F%sAdditionalInfo' % subType)
                if not acm.FSymbol(method) in [m.Name() for m in klass.AllMethods()]:
                    restartNeeded = True
        else:
            klass = getattr(acm, 'F%sAdditionalInfo' % self._recordType)
            if not acm.FSymbol(method) in [m.Name() for m in klass.AllMethods()]:
                restartNeeded = True
        return restartNeeded
    
    def Description(self):
        return 'Addinfo( %s )' % self._fieldName
        
'''**************************************************************************
* ContextLinkSetUp
**************************************************************************'''
class ContextLinkSetUp(SetUpBase):
    def __init__(self, context, type, name, mappingType, chlItem):
        self._context = context
        self._type = type
        self._name = name
        self._mappingType = mappingType
        self._chlItem = chlItem

    def __GetChoiceListOid(self):
        query = "list = '%s' and name = '%s'" % (self._mappingType.replace(' ', ''), self._chlItem)
        chlItem = acm.FChoiceList.Select01(query, None)
        return chlItem.Oid() if chlItem else 0
        
    def _GetExisting(self):
        return acm.FContextLink.Select01("context = '%s' and type = '%s' and name = '%s' and mappingType = '%s' and groupChlItem = %d" % (self._context, self._type, self._name, self._mappingType, self.__GetChoiceListOid()), '')
    
    def _CreateNew(self):
        cl = acm.FContextLink()
        cl.Context(self._context)
        cl.Type(self._type)
        cl.Name(self._name)
        cl.MappingType(self._mappingType)
        cl.GroupChlItem(self.__GetChoiceListOid())
        cl.Commit()
        acm.Log("Creating context link in context '%s' to map %s '%s' to %s '%s'" % (self._context, self._type, self._name, self._mappingType, self.__GetChoiceListOid()))

    def _RestartNeeded(self):
        return False
    
    def Description(self):
        return 'ContextLink( %s )' % self.self._name
         
'''**************************************************************************
* ChoiceListSetUp
**************************************************************************'''
class ChoiceListSetUp(SetUpBase):
    def __init__(self, list, entry, descr):
        self._list = list
        self._entry = entry
        self._descr = descr
    
    def __GetChoiceList(self, list, entry):
        return acm.FChoiceList.Select01("list = '%s' and name = '%s'" % (list, entry), None)

    def __GetMasterList(self):
        return self.__GetChoiceList('MASTER', self._list)

    def __CreateChoiceListEntry(self, list, entry, descr):
        cl = acm.FChoiceList()
        cl.List(list)
        cl.Name(entry)
        cl.Description(descr)
        cl.Commit()    
        
    def _GetExisting(self):
        return self.__GetChoiceList(self._list, self._entry)

    def _CreateNew(self):
        clParent = self.__GetMasterList()
        if not clParent:
            self.__CreateChoiceListEntry('MASTER', self._list, None)
            acm.Log("Created choice list list '%s'" % self._list)
        self.__CreateChoiceListEntry(self._list, self._entry, self._descr)
        acm.Log("Created %s '%s'" % (self._list, self._entry))

    def _RestartNeeded(self):
        restart = False
        if self._list == 'Additional Payments' and not self._entry in acm.GetDomain("enum(PaymentType)").Enumerators():
            restart = True
        return restart 
    
    def Description(self):
        return 'ChoiceList( %s )' % self._list
  
'''**************************************************************************
* CustomMethodSetUp
**************************************************************************'''
class CustomMethodSetUp(SetUpBase):
    def __init__(self, className, customMethodName, methodName):
        self._customMethodName = customMethodName
        self._methodName = methodName
        self._klass = getattr(acm, className)
        
    def _GetExisting(self):
        return acm.GetDefaultContext().GetExtension('FCustomMethod', self._klass, self._customMethodName)
        
    def _CreateNew(self):
        acm.AEF().RegisterCustomMethods()
        
    def _RestartNeeded(self):
        restart = True
        customMethod = self._GetExisting()
        if customMethod:
            if acm.FSymbol(self._methodName) in [m.Name() for m in self._klass.GetMethods(self._methodName)]:
                restart = False
        return restart
    
    def Description(self):
        return 'CustomMethod( %s )' % self._customMethodName
        
'''**************************************************************************
* ComponentSetUp
**************************************************************************'''
class ComponentSetUp(SetUpBase):
    def __init__(self, compName, compType):
        self._compName = compName
        self._compType = compType
        
    def _GetExisting(self):
        q = 'name="%s" and type="%s"' % (self._compName, self._compType)
        return acm.FComponent.Select01(q, None)
        
    def _CreateNew(self):
        component = acm.FComponent()
        component.CompName(self._compName)
        component.Type(self._compType)
        component.Commit()
        acm.Log('Created Component %s of type %s' % (self._compName, self._compType))
        acm.Log('IMPORTANT: An Administrator has to manually add the %s component to User Profiles where applicable.' % (self._compName))
        
    def _RestartNeeded(self):
        return not bool(self._GetExisting())
    
    def Description(self):
        return 'Component( %s )' % self._compName
        
'''**************************************************************************
* DataSetUp Base Class
**************************************************************************'''
class DataSetUp(object):

    def __init__(self):
        self._setUpItems = []
        
    def _NotifyWithDialog(self):
        raise Exception('_NotifyWithDialog should be implemented on base class')
        
    def _Name(self):
        raise Exception('_Name should be implemented on base class')

    def _NotifySetupWithDialog(self, msg):
        raise Exception('_NotifySetupWithDialog should be implemented on base class')

    def __NotifyInLogWnd(self, msg):
        print (msg)
    
    def __ComponentManualSteps(self):
        msg = ''
        components = []
        for i in self._setUpItems:
            if isinstance(i, ComponentSetUp):
                components.append(i)
        if components:
            msg = 'An administrator has to manually add '
            msg += ', '.join([c.Description() for c in components[:-1] or components])
            if len(components) > 1:
                msg += ' and %s' % components[-1].Description()
            msg += " to User Profiles. "
        return msg
    
    def __NextManualStep(self):
        msg = ''
        if self.__IsRestartNeeded():
            name = self._Name()
            msg = name + ' definition is set up. '
            msg += self.__ComponentManualSteps()
            msg += 'Please restart PRIME.'
        return msg
        
    def __NotifySetupNeeded(self, forceSetup):
        runSetup = forceSetup
        name = self._Name()
        if self._NotifyWithDialog():
            msg = name + ' definition is not set up. Would you like to run setup now?'
            runSetup = self._NotifySetupWithDialog(msg)
        else:
            msg = name + ' definition is not set up. Please run setup!'
            self.__NotifyInLogWnd(msg)
        return runSetup
    
    def __DoSetUp(self):
        for item in self._setUpItems:
            item.DoSetUp()
        return self.__IsSetUp()
        
    def __IsRestartNeeded(self):
        for item in self._setUpItems:
            if item.IsRestartNeeded():
                return True
        return False
   
    def __IsSetUp(self):
        for item in self._setUpItems:
            if not item.IsSetUp():
                return False
        return True
        
    def __AssertIsSetUp(self):
        msg = ''
        for item in self._setUpItems:
            if not item.IsSetUp():
                msg += '%s is not set up\n' % item.Description()
        
        msg = msg.strip()
        if msg:
            raise Exception( msg )
            
    '''******************************************************
    * PUBLIC CLASS METHODS
    ******************************************************'''
    def AddSetupItem(self, setupItem):
        self._setUpItems.append( setupItem )
    
    def AddSetupItems(self, *args):
        for setupItem in args:
            self.AddSetupItem( setupItem )
        
    def SetUp(self, forceSetup = False):
        msg = 'Need to run setup'
        setUpOk = self.__IsSetUp()
        if not setUpOk:
            if self.__NotifySetupNeeded(forceSetup):
                setUpOk = self.__DoSetUp()
                self.__AssertIsSetUp()
        if setUpOk:
            msg = self.__NextManualStep()
            
        if msg:
            raise Exception(msg)


class DataSetUpUxShell(DataSetUp):
    def __init__(self, definitionName, uxShell):
        self._uxShell = uxShell
        self._definitionName = definitionName
        DataSetUp.__init__(self)
        
    def _Name(self):    
        return self._definitionName
        
    def _NotifyWithDialog(self):
        return self._uxShell != 0
        
    def _NotifySetupWithDialog(self, msg):
        btnClicked = acm.UX().Dialogs().MessageBoxYesNo(self._uxShell, 'Question', msg )
        return btnClicked == 'Button1'

class DataSetUpDecorator(DataSetUp):
    def __init__(self, definitionName, blGUI):
        self._definitionName = definitionName
        self._blGUI = blGUI
        DataSetUp.__init__(self)

    def _Name(self):    
        return self._definitionName
        
    def _NotifyWithDialog(self):
        return self._blGUI != 0
        
    def _NotifySetupWithDialog(self, msg):
        return self._blGUI.GenericYesNoQuestion(msg)
