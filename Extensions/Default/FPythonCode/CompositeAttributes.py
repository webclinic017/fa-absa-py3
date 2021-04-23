
import acm
import sys
from DealPackageDevKit import CompositeAttributeDefinition, Object, Str, Action, Float, Date, AttributeDialog, NoButtonAttributeDialog, DealPackageChoiceListSource, DealPackageUserException, CounterpartyChoices, DealPackageException, ReturnDomainDecorator, List, Bool, Label
from ChoicesExprInstrument import getAmortGenerationChoices
from DealPackageDialog import DealPackageAttributeDialog
from TraitUtil import CallableMultiMethodChain
from DealPackageUtil import UnDecorate

INT_FORMATTER = acm.GetDomain('int').DefaultFormatter()

def GetFromDict(d, key):
    if hasattr(d, 'At'):
        return d.At(key)
    else:
        return d.get(key, None)

COLOR_MAP = {(1) :'BkgTickerOwnBuyTrade', 
            (-1) :'BkgTickerOwnSellTrade', 
             (0) :None}

def SafeCall(self, method, *args, **kwargs):
    if hasattr(method, '__call__'):
        result = method(*args, **kwargs)
    else:
        methods = method.split('.')
        if len(methods) > 1:
            callableMethod = CallableMultiMethodChain(self.Owner(), '.'.join(methods))
        else:
            callableMethod = self.GetMethod(method)
        result = callableMethod(*args, **kwargs)
    return result
    
class OpenObject(CompositeAttributeDefinition):
    
    def OnInit(self, label, subjectId):
        self._label = label
        self._subjectId = subjectId
        self._tempId = ''
        self._subjectIdMethod = None
        self._domain = None
        self._isOid = True
    
    def InitOwnerDependentVariables(self):
        mappedObject, self._subjectIdMethod = self.Owner().GetCallableMethodsFromChain(self._subjectId, self.get_name())[0]
        mappedObject = UnDecorate(mappedObject)
        self._domain = mappedObject.Domain()
        aClass = mappedObject.Class()
        methodDomain = aClass.GetMethod(self._subjectId.split('.')[-1], 0).Domain()
        self._isOid = methodDomain.IsIntegerDomain()
    
    def IsInitiated(self):
        return self._domain is not None

    def Attributes(self):
        return { 'id'     :  Str(    label=self._label,
                                     validate=self.UniqueCallback('@ValidateId'),
                                     objMapping=self.UniqueCallback('Id'))
               }
    
    def ValidateId(self, name, value):
        if not self.IsInitiated():
            self.InitOwnerDependentVariables()
        tempId = self.IdStringToId(value)
        if tempId and tempId != self.SubjectIdOrEmpty():
            obj = self._domain[tempId]
            if not obj and self._isOid:
                objType = str(self._domain.Name())
                raise DealPackageUserException('No ' + objType[1:] + ' with number ' + str(value) + ' was found.')
    
    @ReturnDomainDecorator('string')
    def Id(self, value = '*Reading*'):
        if not self.IsInitiated():
            self.InitOwnerDependentVariables()
        if value == '*Reading*':
            id = self._tempId
            if id == 0 or (isinstance(id, basestring) and len(id) == 0):
                id = self.SubjectIdOrEmpty()
            return id
        else:
            self._tempId = self.IdStringToId(value)
            try:
                if self._tempId != self.SubjectIdOrEmpty():
                    obj = self._domain[self._tempId]
                    if obj:
                        self.OpenObject(obj)
                    else:
                        self.SubjectId(self._tempId)
            except Exception, e:
                self._tempId = self.SubjectIdOrEmpty()

    def OpenObject(self, obj):
        uxCallbacks = self.Owner().GetAttribute('uxCallbacks')
        if uxCallbacks:
            openCb = uxCallbacks.At('open')
            if openCb:
                acm.AsynchronousCall(openCb, [obj, self.OnOpenFail])

    def OnOpenFail(self):
        self.id = self.SubjectIdOrEmpty()

    def SubjectId(self, value='*Reading*'):
        if self._subjectIdMethod:
            if value == '*Reading*':
                return self._subjectIdMethod()
            else:
                self._subjectIdMethod(value)
        else:
            return None
    
    def IdStringToInt(self, id):
        if isinstance(id, basestring):
            id = INT_FORMATTER.Parse(id)
        id = int(id)
        if id > sys.maxint:
            raise 
        return id
    
    def IdStringToId(self, idString):
        if self._isOid:
            try:
                tempId = self.IdStringToInt(idString)
            except:
                return
        else:
            tempId = idString
        return tempId
    
    def SubjectIdOrEmpty(self):
        id = self.SubjectId()
        if isinstance(id, (int, long)) and id <= 0:
            id = ''
        return id
    
    def GetLayout(self):
        return self.UniqueLayout(""" 
            vbox(;
                id;
            );
            """)

class MultiEnum(CompositeAttributeDefinition):

    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def OnInit(self, objMapping=None, domain=None, label='', **kwargs):
        if not objMapping:
            raise DealPackageException('objMapping missing for MultiEnum')
        if not domain:
            raise DealPackageException('domain missing for MultiEnum')
        self._label = label
        self._objMapping = objMapping
        self._domain = domain
        self._kwargs = kwargs
        
    def Attributes(self):
        a = dict()
        choiceList = sorted([e for e in acm.FEnumeration[self._domain].Enumerators() if e != 'None'])
        a['checkList']     = List(    label='',
                                      elementDomain='FString',
                                      defaultValue=choiceList,
                                      onItemCheckStateChanged=self.UniqueCallback("@OnItemCheckStateChanged"),
                                      checkedItems=self.UniqueCallback('@CheckedItems'),
                                      width=50,
                                      height=8,
                                      **self._kwargs )
        
        a['dropdownField'] = Object(  label=self._label,
                                      objMapping=self.UniqueCallback('SingleEnum'),
                                      visible=self.UniqueCallback('@IsSingleEnum'),
                                      choiceListSource=choiceList,
                                      domain=self._domain,
                                      **self._kwargs)
        
        a['stringField']   = Object(  label=self._label,
                                      objMapping=self.UniqueCallback('MultiEnum'),
                                      visible=self.UniqueCallback('@IsMultiEnum'),
                                      editable=False,
                                      **self._kwargs )
                                    
        a['openDialog']    = Action(  label='>',
                                      sizeToFit=True,
                                      dialog=self.UniqueCallback('@StartDialog'),
                                      **self._kwargs )
        return a

    def GetLayout(self):
        return self.UniqueLayout(""" 
            hbox(;
                dropdownField;
                stringField;
                openDialog;
            );
            """)

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def ObjMapping(self, *args):
        return SafeCall(self, self._objMapping, *args)

    def SingleEnum(self, value='*Reading*'):
        if value == '*Reading*':
            if self.IsSingleEnum():
                return self.ObjMapping()
            else:
                return 'None'
        else:
            self.ObjMapping(value)
    
    def IsSingleEnum(self, *args):
        return len(self.CheckedItems()) <= 1
    
    def MultiEnum(self, *args):
        return self.ObjMapping(*args)
    
    def IsMultiEnum(self, *args):
        return not self.IsSingleEnum()
    
    def StartDialog(self, *args):
        dealPackage = self.GetMethod('DealPackage')()
        label = 'Select ' + self._label
        layout = [{' ': self.UniqueLayout('checkList;')}]
        return DealPackageAttributeDialog(dealPackage, label, layout, 'Ok')
    
    def OnItemCheckStateChanged(self, attr, item, checked):
        checkedItems = self.CheckedItems()
        if not checked:
            checkedItems.remove(item)
        elif item not in checkedItems:
            checkedItems.append(item)
        self.ObjMapping(','.join(checkedItems))
        
    def CheckedItems(self, *args):
        enum = self.ObjMapping()
        if enum and isinstance(enum, basestring):
            return enum.split(',')
        return []
    
    
class SearchList(CompositeAttributeDefinition):

    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def OnInit(self, label, source, collectionType, onDoubleClick, visible=True):
        self._label = label
        self._sourceCb = source
        self._source = None
        self._collectionType = collectionType
        self._choices = acm.FArray()
        self._visible = visible
        self._onDoubleClick = onDoubleClick
        self.selected = None
        
    def Attributes(self):
        return {'label'    : Label(  label=self._label,
                                     visible=self._visible),

                'search'   : Str(    label='',
                                     onChanged=self.UniqueCallback('@Filter'),
                                     visible=self._visible),

                'choices'  : Object( objMapping=self.UniqueCallback('Choices'),
                                     label='',
                                     width=50,
                                     onSelectionChanged=self.UniqueCallback('@UpdateSelected'),
                                     onDoubleClick=self.UniqueCallback('@OnDoubleClick'),
                                     visible=self._visible)
                }

    def GetLayout(self):
        return self.UniqueLayout(""" 
            vbox(;
                label;
                search;
                choices;
            );
            """)

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    @ReturnDomainDecorator('FArray')
    def Choices(self, *args):
        return self._choices

    def UpdateSelected(self, attributeName, selectedItem):
        self.selected = selectedItem

    def Filter(self, *args):
        if not self._source:
            return # Exit
        filter = None
        if self.search and self.search != '*':
            searchStr = self.search
            if ('*' not in searchStr
               or (searchStr.startswith('*') and '*' not in searchStr[1:])):
                searchStr += '*'
            filter = acm.Filter.SimpleAndQuery(self._collectionType, 'Name', 'RE_LIKE_NOCASE', searchStr)
        else:
            filter = acm.Filter.SimpleAndQuery(self._collectionType, [], [], [])
        
        self._choices.Clear()
        self._choices.AddAll( self._source.Filter(filter).Sort() )
        
    def OnDoubleClick(self, attributeName, item):
        self.selected = item
        SafeCall(self, self._onDoubleClick, attributeName, item)

    # ####################### #
    #   Convenience Methods   #
    # ####################### #

    def UpdateSource(self, *args):
        self._source = SafeCall(self, self._sourceCb)
        self.Filter()
        self.selected = None
        
class AliasTableBase(CompositeAttributeDefinition):
    
    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def OnInit(self, label, entity, **kwargs):
        self._label = label
        self._entity = entity
        self._selectedAlias = None
        
    def Attributes(self):
        attributes = {
            # Main GUI Attributes
            'aliasTable' : Object( 
                label = self._label,
                objMapping = self._entity + '.Aliases',
                onSelectionChanged = self.UniqueCallback('@SetSelected'),
                addNewItem = ['First', 'Sorted'],
                sortIndexCallback= self.UniqueCallback('@_SortList'),
                columns = self.UniqueCallback('@_ListColumns'),
                dialog = NoButtonAttributeDialog( 
                    label = 'Set Value',
                    customPanes = self.UniqueCallback('@UpdateAliasDialog'))),
            'addBttn' : Action(
                label = 'Add...',
                dialog=NoButtonAttributeDialog( 
                    label = 'Set Value',
                    customPanes = self.UniqueCallback('@AddAliasDialog'))),
            'updateBttn' : Action(
                label = 'Update...',
                enabled = self.UniqueCallback('@SelectionSet'),
                dialog = NoButtonAttributeDialog( 
                    label = 'Set Value',
                    customPanes = self.UniqueCallback('@UpdateAliasDialog'))),
            'removeBttn' : Action(
                label='Remove',
                enabled = self.UniqueCallback('@SelectionSet'),
                action = self.UniqueCallback('@RemoveAlias') ),
            # Dialog Attributes
            'typeDialogField' : Object( 
                label = 'Type',
                choiceListSource = self._GetAliasTypeList()),
            'nameDialogField' : Object(
                label = 'Name'),
            'addDialogBttn' : Action(
                label = 'Add',
                enabled = self.UniqueCallback('@AddEnable'),
                action = self.UniqueCallback('@OnAdd')),
            'closeDialogBttn' : Action(
                label = 'Close',
                action = self.UniqueCallback('@OnClose')),
            'updateDialogBttn' : Action(
                label = 'Update',
                enabled = self.UniqueCallback('@UpdateEnable'),
                action = self.UniqueCallback('@OnUpdate')),
            'removeDialogBttn' : Action(
                label = 'Remove',
                enabled = self.UniqueCallback('@RemoveEnable'),
                action = self.UniqueCallback('@OnRemove'))                       
        }
        return attributes

    def GetLayout(self):
        layout = self._AliasTableLayout()
        return layout

    def Entity(self):
        return self.GetMethod(self._entity)()

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def SelectionSet(self, *args):
        selected = False
        if self._selectedAlias:
            selected = True
        return selected

    def SetSelected(self, attrName, selectedObj):
        self._selectedAlias = selectedObj

    def AddEnable(self, *args):
        enable = True
        if self.Entity().Aliases():
            alias = self._QueryAlias(self.typeDialogField)
            if alias in self.Entity().Aliases():
                enable = False
        if not self.nameDialogField:
            enable = False
        return enable
    
    def UpdateEnable(self, *args):
        enable = False
        if self.Entity().Aliases():
            alias = self._QueryAlias(self.typeDialogField)
            if alias in self.Entity().Aliases():
                if self.nameDialogField and self.nameDialogField != alias.Alias():
                    enable = True
        return enable
        
    def RemoveEnable(self, *args):
        enable = False
        if self.Entity().Aliases():
            alias = self._QueryAlias(self.typeDialogField)
            if alias in self.Entity().Aliases():
                enable = True
        return enable

    def AddAliasDialog(self, attrName):
        self.typeDialogField = ''
        self.nameDialogField = ''
        return self._DialogLayout()

    def UpdateAliasDialog(self, attrName):
        self.typeDialogField = self._selectedAlias.Type().Name()
        self.nameDialogField = self._selectedAlias.Alias()
        return self._DialogLayout()

    def OnAdd(self, *args):
        if self.nameDialogField:
            self.TouchAlias(self.typeDialogField, self.nameDialogField)

    def OnUpdate(self, *args):
        if self.nameDialogField:
            alias = self._QueryAlias(self.typeDialogField)
            if alias in self.Entity().Aliases():
                self.TouchAlias(self.typeDialogField, self.nameDialogField)

    def OnRemove(self, *args):
        self.TouchAlias(self.typeDialogField, '')

    def OnClose(self, *args):
        self.CloseDialog()

    def RemoveAlias(self, attrName):
        if self._selectedAlias:
            self._selectedAlias.Unsimulate()
            self._selectedAlias = None

    def TouchAlias(self, aliasType, aliasName):
        if aliasType:
            alias = self._QueryAlias(aliasType)
            if aliasName:
                if not alias:
                    alias = self._CreateAlias(aliasType, aliasName)
                else:
                    alias.Alias = aliasName
            elif alias:
                alias.Unsimulate()

    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def _SortList(self, attrName, columnNbr, value1, formatter, obj):
        return value1.Name()

    def _ListColumns(self, *args):
        cols = [
            {'methodChain': 'Type', 'label': 'Type'},
            {'methodChain': 'Alias', 'label': 'Name'}
        ]
        return cols

    def _AliasTableLayout(self):
        layout = self.UniqueLayout(
            "hbox["
            + self._label
            + """;
                aliasTable;
                vbox(;
                    addBttn;
                    updateBttn;
                    removeBttn;
                );
            ];
           """
        )
        return layout

    def _DialogLayout(self):
        layout = self.UniqueLayout(
            """
                typeDialogField;
                nameDialogField;
                hbox{;
                    addDialogBttn;
                    updateDialogBttn;
                    removeDialogBttn;
                    closeDialogBttn;
                };
            """
        )
        return [{'Edit Value' : layout}]



    # ####################### #
    #   Overridable Methods   #
    # ####################### #

    def _QueryAlias(self, aliasType):
        pass

    def _GetAliasTypeList(self):
        pass

    def _AliasFClass(self):
        pass

    def _CreateAlias(self, aliasType, aliasName):
        pass


class AliasTableInst(AliasTableBase):
    def OnInit(self, label, instrument, **kwargs):
        super(AliasTableInst, self).OnInit(label, instrument, **kwargs)

    def _QueryAlias(self, aliasType):
        alias = None
        if aliasType:
            q = ( 
                "type='" 
                + aliasType
                + "' and instrument='" 
                + str( self.Entity().Oid() ) 
                + "'" 
            )
            alias = self._AliasFClass().Select(q)
            alias = alias[0] if len(alias) else None
        return alias

    def _GetAliasTypeList(self):
        return acm.FInstrAliasType.Instances()

    def _AliasFClass(self):
        return acm.FInstrumentAlias

    def _CreateAlias(self, aliasType, aliasName):
        alias = (self._AliasFClass())()
        alias.RegisterInStorage()
        alias.Type = aliasType
        alias.Alias = aliasName
        alias.Instrument = self.Entity()
    


class AliasTableTrade(AliasTableBase):
    def OnInit(self, label, trade, **kwargs):
        super(AliasTableTrade, self).OnInit(label, trade, **kwargs)

    def _QueryAlias(self, aliasType):
        alias = None
        if aliasType:
            q = ( 
                "type='" 
                + aliasType
                + "' and trade='" 
                + str( self.Entity().Oid() ) 
                + "'" 
            )
            alias = self._AliasFClass().Select(q)
            alias = alias[0] if len(alias) else None
        return alias

    def _GetAliasTypeList(self):
        return acm.FTradeAliasType.Instances()

    def _AliasFClass(self):
        return acm.FTradeAlias

    def _CreateAlias(self, aliasType, aliasName):
        alias = (self._AliasFClass())()
        alias.RegisterInStorage()
        alias.Type = aliasType
        alias.Alias = aliasName
        alias.Trade = self.Entity() 


class SelectInstrumentsDialog(CompositeAttributeDefinition):

    # ####################### #
    #   Interface Overrides   #
    # ####################### #
                                
    def OnInit(self, objMapping, selectSingleInstrument=False, **kwargs):
        self._objMapping = objMapping
        self._selectSingleInstrument = selectSingleInstrument
        self._extraArguments = kwargs
        
        self._showOptions = False
        self._available = acm.FArray()
        self._availableSource = acm.FArray()
        self._selected = acm.FArray()
        self._undTypes = DealPackageChoiceListSource()

    def Attributes(self):
        return {'insType'            : Str(    label='Ins Type',
                                               choiceListSource=acm.FEnumeration['enum(InsType)'].Enumerators().Sort(),
                                               onChanged=self.UniqueCallback('@UpdateAvailable')),

                'undType'            : Object( label='Und Type',
                                               choiceListSource=self.UniqueCallback('@UndTypes'),
                                               visible=self.UniqueCallback('@UndTypeVisible'),
                                               onChanged=self.UniqueCallback('@FilterAvailable')),

                'available'          : SearchList( label='Instruments:',
                                                   source=self.UniqueCallback('Available'),
                                                   collectionType=acm.FInstrumentId,
                                                   onDoubleClick=self.UniqueCallback('OnDoubleClickAvailable')),

                'selected'           : SearchList( label='Selected:',
                                                   source=self.UniqueCallback('Selected'),
                                                   collectionType=acm.FInstrument,
                                                   visible=not self._selectSingleInstrument,
                                                   onDoubleClick=self.UniqueCallback('Remove')),
                
                'optionsShow'        : Action( label="Options >>",
                                               action=self.UniqueCallback('@ToggleShowOptions'),
                                               visible=self.UniqueCallback('@IsOptionsHidden')),

                'optionsHide'        : Action( label="Options <<",
                                               action=self.UniqueCallback('@ToggleShowOptions'),
                                               visible=self.UniqueCallback('@IsOptionsShown')),

                'add'                : Action( label='>',
                                               action=self.UniqueCallback('@Add'),
                                               sizeToFit=True,
                                               visible=not self._selectSingleInstrument),

                'remove'             : Action( label='<',
                                               action=self.UniqueCallback('@Remove'),
                                               sizeToFit=True,
                                               visible=not self._selectSingleInstrument),

                'gen'                : Bool(   label='Generic',
                                               defaultValue=True,
                                               onChanged=self.UniqueCallback('@FilterAvailable'),
                                               visible=self.UniqueCallback('@IsOptionsShown')),
                
                'nongen'             : Bool(   label='Non-generic',
                                               defaultValue=True,
                                               onChanged=self.UniqueCallback('@FilterAvailable'),
                                               visible=self.UniqueCallback('@IsOptionsShown')),
                
                'exp'                : Bool(   label='Expired',
                                               defaultValue=False,
                                               onChanged=self.UniqueCallback('@FilterAvailable'),
                                               visible=self.UniqueCallback('@IsOptionsShown')),
                
                'nonexp'             : Bool(   label='Live',
                                               defaultValue=True,
                                               onChanged=self.UniqueCallback('@FilterAvailable'),
                                               visible=self.UniqueCallback('@IsOptionsShown')),
                
                'expDate'            : Date(   label='',
                                               defaultValue=acm.Time.DateToday(),
                                               onChanged=self.UniqueCallback('@FilterAvailable'),
                                               visible=self.UniqueCallback('@IsOptionsShown')),
                
                'currency'           : Object( label='Currency',
                                               choiceListSource=acm.FCurrency.Instances(),
                                               domain='FCurrency',
                                               onChanged=self.UniqueCallback('@FilterAvailable'),
                                               visible=self.UniqueCallback('@IsOptionsShown')),
                
                # instruments is an attribute to facilitate setting and getting instruments programmatically.
                'instruments'        : Action( action=self.UniqueCallback('@Instruments') ),
                
                'dialogButton'       : Action( dialog=self.UniqueCallback('@StartDialog'),
                                               action=self.UniqueCallback('@HandleClose'),
                                               **self._extraArguments)
                }

        return attrs
    
    def GetLayout(self):
        return self.UniqueLayout("dialogButton;")
    
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def StartDialog(self, *args):
        self._selected = self.GetObjMapping()
        if not self._selectSingleInstrument:
            self.selected.UpdateSource()
        return DealPackageAttributeDialog(self.GetMethod('DealPackage')(), 'Select Instruments', self.GetSelectInstrumentsPanes(), 'Ok')
    
    def HandleClose(self, attributeName, applyChanges):
        if applyChanges:
            self.ApplyToObjMapping()

    def Available(self, *args):
        return self._available
    
    def Selected(self, *args):
        return self._selected
    
    def UpdateAvailable(self, *args):
        self._availableSource = acm.FInstrumentId.Select('insType="%s"' % str(self.insType))
        self.UpdateUndTypes()
        self.FilterAvailable()

    def FilterAvailable(self, *args):
        queryCls = acm.FInstrumentId
        filter = 'Show All'
    
        if (   not (self.gen or self.nongen)
            or not (self.exp or self.nonexp)):
            filter = None # None means show none
        else:
            queries = []
            
            def create_and_query(func, op, cond):
                return acm.Filter.SimpleAndQuery(queryCls, [func], [op], [cond])
            
            if self.currency and self.currency != 'All':
                queries.append(create_and_query('Currency', 'EQUAL', self.currency))
            
            if not (self.gen and self.nongen):
                queries.append(create_and_query('Generic', 'EQUAL', self.gen))
            
            if self.undType and self.undType != 'All':
                queries.append(create_and_query('UnderlyingType', 'EQUAL', self.undType))
            
            if self.expDate and self.exp != self.nonexp:
                expCond = [
                    ['Generic', 'ExpiryDate',         'ExpiryDate'],
                    ['EQUAL',   'LESS_EQUAL',         'LESS' if self.exp else 'GREATER_EQUAL'],
                    [True,      acm.Time.SmallDate(), self.expDate]]
            
                queries.append(
                    acm.Filter.SimpleOrQuery(queryCls,
                        expCond[0],
                        expCond[1],
                        expCond[2]))
            if queries:
                filter = queries[0]
                if len(queries) > 1:
                    for q in queries[1:]:
                        filter = acm.Filter.CompositeAndQuery(queryCls, filter, q)
        
        self._available = self._availableSource
        if filter != 'Show All':
            self._available = self._available.Filter(filter)
        self.available.UpdateSource()
    
    def GetSelectInstrumentsPanes(self, *args):
        return [{' ': self.GetSelectInstrumentsLayout()}]

    def OnDoubleClickAvailable(self, attrName, item):
        if self._selectSingleInstrument:
            self.GetMethod('CloseDialog')()
        else:
            self.Add(attrName, item)

    def Add(self, *args):
        if self._selectSingleInstrument:
            return # Do nothing
        selected = self.available.selected
        if selected:
            if (selected in self.available_choices
               and selected.SourceObject() not in self.selected_choices):
                self._selected.Add(selected.SourceObject())
                self.selected.UpdateSource()
        
    def Remove(self, *args):
        selected = self.selected.selected
        if selected:
            if selected in self.selected_choices:
                self._selected.Remove(selected)
                self.selected.UpdateSource()
        
    def IsOptionsShown(self, *args):
        return self._showOptions

    def IsOptionsHidden(self, *args):
        return not self.IsOptionsShown()

    def ToggleShowOptions(self, *args):
        self._showOptions = self._showOptions != True

    def UpdateUndTypes(self, *args):
        undTypes = []
        default = None
        if not self._availableSource.IsEmpty():
            if acm.DealCapturing.HasUnderlying(self.insType):
                validUnderlyingTypes = acm.DealCapturing.ValidUnderlyingTypes(self.insType)
                if validUnderlyingTypes:
                    undTypes = validUnderlyingTypes.Sort()
                    undTypes.Add('All')
                    default = 'All'
        self._undTypes.Populate(undTypes)
        self.SetAttribute('undType', default, silent=True)

    def UndTypes(self, *args):
        if self._undTypes.IsEmpty():
            self.UpdateUndTypes()
        return self._undTypes.Source()

    def UndTypeVisible(self, *args):
        return not self._undTypes.IsEmpty()

    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def Instruments(self, *args):
        if len(args) == 2:
            self.ApplyToObjMapping(args[1])
        else:
            return self.GetObjMapping()
    
    def ApplyToObjMapping(self, *args):
        if len(args) == 1:
            item = args[0]
        else:
            if self._selectSingleInstrument:
                item = self.available.selected
            else:
                item = self.CopyArray(self._selected)
        SafeCall(self, self._objMapping, item)

    def GetObjMapping(self):
        item = SafeCall(self, self._objMapping)
        isIterable = hasattr(item, '__iter__')
        msg = None
        if self._selectSingleInstrument and isIterable:
            msg = "Composite attribute 'SelectInstrumentsDialog' expects a single object when "
            msg += "selectSingleInstrument is True. Got: %s" %(str(item))
        elif not self._selectSingleInstrument and not isIterable:
            msg = "Composite attribute 'SelectInstrumentsDialog' expects a list of objects when "
            msg += "selectSingleInstrument is False. Got: %s" %(str(item))
        if msg:
            raise DealPackageException(msg)
        return item if self._selectSingleInstrument else self.CopyArray(item)
    
    def CopyArray(self, arr):
        result = acm.FArray()
        result.AddAll([a for a in arr])
        return result
    
    def GetSelectInstrumentsLayout(self):
        return self.UniqueLayout("""
            hbox(;
                vbox(;
                    hbox(;
                        insType;
                        undType;
                        optionsShow;
                    );
                    hbox(;
                        vbox(;
                            available_label;
                            available_search;
                            available_choices;
                        );
                        vbox(;
                            space(46);
                            fill;
                            add;
                            remove;
                            fill;
                        );
                        vbox(;
                            selected_label;
                            selected_search;
                            selected_choices;
                        );
                        vbox(;
                            space(350);
                        );
                    );
                );
                vbox(;
                    hbox(;
                        fill;
                        optionsHide;
                    );
                    space(20);
                    vbox[Instrument Filter;
                        hbox(;
                            gen;
                            nongen;
                        );
                        hbox(;
                            exp;
                            nonexp;
                            expDate;
                        );
                        currency;
                    ];
                );
            );
               """)


class SelectInstrumentField(CompositeAttributeDefinition):
    ''' If setting instrument from python, just set "ins".
        "insName" and "selectInstrument" are just convenience methods
        for the GUI.'''

    def OnInit(self, label, objMapping, **kwargs):
        self._objMapping = objMapping
        self._label = label
        self._kwargs = kwargs
        
    def Attributes(self):
        return {'ins'              : Object(                    objMapping=self._objMapping),
                'insName'          : Object(                    label=self._label,
                                                                objMapping=self.UniqueCallback('InstrumentName'),
                                                                editable=False,
                                                                **self._kwargs),
                'selectInstrument' : SelectInstrumentsDialog(   label='...',
                                                                objMapping=self.UniqueCallback('SelectInstrument'),
                                                                selectSingleInstrument=True,
                                                                sizeToFit=True,
                                                                **self._kwargs)
               }
 
    @ReturnDomainDecorator('string')
    def InstrumentName(self, *args):
        return self.ins.Name() if self.ins else ''

    def SelectInstrument(self, *args):
        if len(args) == 1:
            obj = args[0]
            if hasattr(obj, 'IsKindOf') and obj.IsKindOf(acm.FInstrumentId):
                obj = obj.SourceObject()
            self.ins = obj
        else:
            return self.ins

    def GetLayout(self):
        return self.UniqueLayout(
                   """
                     hbox(;
                        insName;
                        selectInstrument;
                     );
                   """
               )


class AmortisingDialog(CompositeAttributeDefinition):

    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def OnInit(self, leg, **kwargs):
        self._legName = leg
        self._extraArguments = kwargs
        
    def Attributes(self):
        return {'amortTypeCfPane'       : Object(   label='Amortisation',
                                                    objMapping=self._legName + '.AmortType',
                                                    choiceListSource=self.UniqueCallback('@AmortTypeChoices')),
                
                'amortTypeInDialog'     : Object(   label='Type',
                                                    objMapping=self._legName + '.AmortType',
                                                    choiceListSource=self.UniqueCallback('@AmortTypeChoices')),
                                            
                'amortPeriod'           : Object(   label='Periodicity',
                                                    objMapping=self._legName + '.AmortPeriod',
                                                    visible=self.UniqueCallback('@AmortControlsVisible')),
                                                
                'amortStartDay'         : Date  (   label='Start',
                                                    objMapping=self._legName + '.AmortStartDay',
                                                    transform=self.UniqueCallback('@TransformStartDay'),
                                                    visible=self.UniqueCallback('@AmortControlsVisible')),
                                                
                'amortStartPeriod'      : Object(   label='',
                                                    objMapping=self._legName + '.AmortStartPeriod',
                                                    enabled=False,
                                                    visible=self.UniqueCallback('@AmortControlsVisible')),
                                                
                'amortEndDay'           : Date  (   label='End',
                                                    objMapping=self._legName + '.AmortEndDay',
                                                    transform=self.UniqueCallback('@TransformEndDay'),
                                                    enabled=self.UniqueCallback('@AmortEndDayEnabled'),
                                                    visible=self.UniqueCallback('@AmortControlsVisible')),
                                                
                'amortEndPeriod'        : Object(   label='',
                                                    objMapping=self._legName + '.AmortEndPeriod',
                                                    enabled=False,
                                                    visible=self.UniqueCallback('@AmortControlsVisible')),
                                                
                'amortStartNominal'     : Object(   label='Start Nom',
                                                    objMapping=self._legName + '.AmortStartNominal',
                                                    visible=self.UniqueCallback('@AmortNominalsVisible')),
                                                
                'amortEndNominal'       : Object(   label='End Nom',
                                                    objMapping=self._legName + '.AmortEndNominal',
                                                    visible=self.UniqueCallback('@AmortNominalsVisible')),
                
                'annuityRate'           : Object(   label='Rate',
                                                    objMapping=self._legName + '.AnnuityRate',
                                                    formatter='FullPrecision',
                                                    visible=self.UniqueCallback('@AnnuityVisible')),
                                                
                'amortDaycountMethod'   : Object(   label='Day Count',
                                                    objMapping=self._legName + '.AmortDaycountMethod',
                                                    visible=self.UniqueCallback('@DaycountVisible')),
                                                
                'rateInput'             : Object(   label='Rate',
                                                    objMapping=self._legName + '.RateInput',
                                                    formatter='FullPrecision',
                                                    visible=self.UniqueCallback('@AmortControlsVisible')),
                
                'amortGeneration'       : Object(   label='Method',
                                                    objMapping=self._legName + '.AmortGeneration',
                                                    choiceListSource=self.UniqueCallback('@AmortGenerationChoices'),
                                                    enabled=self.UniqueCallback('@AnnuityVisible'),
                                                    visible=self.UniqueCallback('@AmortControlsVisible')),
                
                'dialogButton'          : Action(   label='...',
                                                    enabled=self.UniqueCallback('@ButtonEnabled'),
                                                    dialog=AttributeDialog( 
                                                        label=self.WindowLabel(), 
                                                        customPanes=self.UniqueCallback('@GetAmortPane')),
                                                    **self._extraArguments
                                            )
               }
    
    def GetLayout(self):
        return self.UniqueLayout("""
                                    hbox(;
                                        amortTypeCfPane;
                                        dialogButton;
                                    );
                                """)
    
    
    def GetAmortPane(self, *args):
        return [{'Amortising': self.GetAmortLayout()}]
    
    def WindowLabel(self, *args):
        ins = self.Leg().Instrument()
        if ins.IsSwap():
            return "Amortising Swap/" + ("Pay" if self.Leg().PayLeg() else "Receive")
        else:
            return "Amortising"
    
    def ButtonEnabled(self, *args):
        return self.Leg().AmortType() not in ['None', 'Manual']
        
    def AmortControlsVisible(self, *args):
        return self.Leg().AmortType() != 'None'
    
    def AnnuityVisible(self, *args):
        return self.Leg().AmortType() == 'Annuity'
    
    def DaycountVisible(self, *args):
        return self.AnnuityVisible() and self.Leg().LegType() != 'Fixed'
    
    def AmortNominalsVisible(self, *args):
        return self.Leg().AmortType() != 'None' and self.Leg().AmortGeneration() == 'Target End'
    
    def AmortEndDayEnabled(self, *args):
        return self.Leg().AmortType() != 'Annuity'
        
    def AmortTypeChoices(self, *args):
        return self.Leg().AmortTypeChoices()
        
    def AmortGenerationChoices(self, *args):
        return getAmortGenerationChoices(self.Leg().Leg())

    def TransformStartDay(self, attrName, value):
        value = self._PeriodToDateTransform(value, 'Start')
        return value
    
    def TransformEndDay(self, attrName, value):
        value = self._PeriodToDateTransform(value, 'End')
        return value
    
    def _PeriodToDateTransform(self, newDate, dateName):
        date = newDate
        if dateName == 'End':
            try:
                date = self.Leg().Instrument().LegEndDateFromPeriod(newDate, self.Leg().AmortStartDay())
            except:
                pass
        else:
            try:
                date = self.Leg().Instrument().LegStartDateFromPeriod(newDate)
            except:
                pass
        return date
    
    def Leg(self):
        return self.GetMethod(self._legName)()
    
    def GetAmortLayout(self):
        return self.UniqueLayout("""
                    vbox{;
                        hbox{;
                            amortTypeInDialog;        
                        };
                        hbox[Period Data;
                            vbox(;
                                amortPeriod;
                                hbox(;
                                    vbox(;
                                        hbox(;
                                            amortStartDay;
                                            amortStartPeriod;
                                        );
                                        hbox(;
                                            amortEndDay;
                                            amortEndPeriod;
                                        );
                                    );
                                );
                            );
                        ];
                        hbox[Annuity;
                            annuityRate;
                            amortDaycountMethod;
                        ];
                        vbox[Amortisation Rate;
                            amortGeneration;
                            amortStartNominal;
                            amortEndNominal;
                            rateInput;
                        ];
                    );
               """)

class BuySell(CompositeAttributeDefinition):
    
    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    
    def OnInit(self, label, showBuySell=True, choiceListWidth=0, buySellLabels=None, **kwargs):
        self._label = label
        self._showBuySell = showBuySell
        self._buySellLabels = buySellLabels or ['B', 'S', '-']
        if choiceListWidth:
            self._choiceListWidth = choiceListWidth
        else:
            self._choiceListWidth = max(len(max(self._buySellLabels, key=len)) + 4, 6)
        self._metaData = kwargs
        
        if len(self._buySellLabels) != 3:
            raise DealPackageException('buySellLabels should be list of three strings. ["buyLabel", "sellLabel", "zeroLabel"]. Got %s', str(buySellLabels))
       
        self.TWO_WAY_SIGN_MAP = {self._buySellLabels[0]:  1, (1): self._buySellLabels[0], 
                                 self._buySellLabels[1]: -1,(-1): self._buySellLabels[1],  
                                 self._buySellLabels[2]:  0, (0): self._buySellLabels[2]}
        
    def Attributes(self):
        self._metaData['formatter'] = GetFromDict(self._metaData, 'formatter') or (self._showBuySell and 'PackageAbsNominal') or 'InstrumentDefinitionNominal'
        self._metaData['backgroundColor'] = GetFromDict(self._metaData, 'backgroundColor') or self.UniqueCallback('@ValueBackgroundColor')
        self._metaData['label'] = self._label if self._showBuySell == False else ''
        self.MergeMetaData('transform', 'TransformValue')
        buySellMetaData = self.GetBuySellMetaData()
        return {
                    'value':Object( **self._metaData ),
                                    
                    'buySell':Object( label=self._label,
                                      objMapping=self.UniqueCallback("BuySellString"),
                                      choiceListSource=self._buySellLabels,
                                      maxWidth=self._choiceListWidth,
                                      width=self._choiceListWidth,
                                      **buySellMetaData)
                    
                }

    def GetBuySellMetaData(self):
        md = {}
        def copy_md(mdName):
            if mdName in self._metaData:
                md[mdName] = self._metaData[mdName]
            
        if self._showBuySell == False:
            md['visible'] = False
        else:
            copy_md('visible')
        copy_md('editable')
        copy_md('enabled')
        for mdName in self._metaData:
            if mdName.startswith('_'):
                copy_md(mdName)
        return md

    def GetLayout(self):
        return self.UniqueLayout( """
                                    hbox(;
                                        buySell;
                                        value;
                                    );""")

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    @ReturnDomainDecorator('string')
    def BuySellString(self, value='*Reading*'):
        if value == '*Reading*':
            return self.TWO_WAY_SIGN_MAP[self._ValueSign()]
        else:
            self.UpdateValue(value)

    def UpdateValue(self, buySell=None):
        if self.value:
            self.value = self._BuySellSign(buySell) * abs(self.value)
    
    def TransformValue(self, name, input):
        if not isinstance(input, basestring):
            return input
        
        parsed = self.GetMethod('GetFormatter')(name).Parse(input)
        if parsed is None:
            return input
        elif self._showBuySell == False:
            return parsed
        else:
            if input.startswith( ('+', '-') ):
                sign = {'+':1, '-':-1}[input[0]]
            else:
                sign = self._BuySellSign() if self._BuySellSign() else 1
            
            return sign * abs(parsed)
        
    def ValueBackgroundColor(self, attributeName):
        return COLOR_MAP[self._BuySellSign()]

    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def MergeMetaData(self, attrName, toMerge):
        if not attrName in self._metaData:
            self._metaData[attrName] = '@' + self.UniqueCallback(toMerge)
        elif not self._metaData[attrName].endswith(toMerge):
            self._metaData[attrName] = self._metaData[attrName] + '|' + self.UniqueCallback(toMerge)
            
    def _BuySellSign(self, buySell=None):
        if buySell is None:
            buySell = self.BuySellString()
        return self.TWO_WAY_SIGN_MAP[buySell]
    
    def _ValueSign(self, value = None):
        cmpValue = self.value if value is None else value
        return cmp(cmpValue, 0)
    

class PaymentsDialog(CompositeAttributeDefinition):

    # ####################### #
    #   Interface Overrides   #
    # ####################### #

    def OnInit(self, trade, **kwargs):
        self._tradeName = trade
        self._ourAccountChoices = DealPackageChoiceListSource()
        self._counterAccountChoices = DealPackageChoiceListSource()
        self._extraArguments = kwargs
        
    def Attributes(self):
        return {'counterparty': Object( label='Counterparty',
                                            domain="FParty",
                                            choiceListSource=CounterpartyChoices(),
                                            transform=self.UniqueCallback('@TransformToDomain'),
                                            onChanged=self.UniqueCallback('@UpdateCptyAccountChoices')),
                'type': Str(    defaultValue="Premium",
                                            label='Type',
                                            domain='enum(PaymentType)'),
                'amount': Float(  label='Amount' ),
                'currency': Object( label='Currency',
                                            domain='FCurrency',
                                            transform=self.UniqueCallback('@TransformToDomain'),
                                            onChanged=self.UniqueCallback('@UpdateOurAccountChoices|UpdateCptyAccountChoices')),
                'payDay': Date(   label='Pay Day',
                                            objMapping=self.UniqueCallback("PrivatePayDay"),
                                            transform=self.UniqueCallback("@TransformPayDay")),
                'validFrom': Date(   label='Valid From',
                                            objMapping=self.UniqueCallback("PrivateValidFrom"),
                                            transform=self.UniqueCallback("@TransformValidFromDate")),
                'privatePayDay': Date(   ),
                'privateValidFrom': Date(   ),
                'cptyAccount': Object( label='Cpty Account',
                                            domain="FAccount",
                                            transform=self.UniqueCallback('@TransformToDomain'),
                                            choiceListSource=self.UniqueCallback('@CptyAccountChoices')),
                'ourAccount': Object( label='Our Account',
                                            domain="FAccount",
                                            transform=self.UniqueCallback('@TransformToDomain'),
                                            choiceListSource=self.UniqueCallback('@OurAccountChoices') ),
                'text': Str(    label='Text' ),
                'add': Action( label='Add',
                                            action=self.UniqueCallback("@AddPayment")),
                'remove': Action( label='Remove',
                                            action=self.UniqueCallback("@RemovePayment")),
                'update': Action( label='Update',
                                            action=self.UniqueCallback("@UpdatePayment")),
                'paymentsList': Object( label='',
                                            objMapping=self._tradeName+'.Payments',
                                            domain="FPersistentSet",
                                            elementDomain="FPayment",
                                            columns=self.UniqueCallback('@PaymentColumns'),
                                            onSelectionChanged=self.UniqueCallback('@SetSelectedPayment')),
                'selectedPayment': Object( domain='FPayment',
                                            transform=self.UniqueCallback('@TransformToDomain'),
                                            onChanged=self.UniqueCallback('@SetFieldsFromSelectedPayment')),
                'dialogButton': Action( label=self.UniqueCallback('@ButtonLabel'),
                                            dialog=AttributeDialog( 
                                               label='Payments', 
                                               customPanes=self.UniqueCallback('@GetPaymentsPanes')),
                                            **self._extraArguments
                                            ),
               }
    
    def GetLayout(self):
        return self.UniqueLayout("dialogButton;")
    
    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #

    def ButtonLabel(self, *args):
        return 'Payments...*' if self.paymentsList else 'Payments...'
    
    def GetPaymentsPanes(self, *args):
        return [{'Payments': self.GetPaymentsLayout()}]
    
    def PaymentColumns(self, *args):
        columns =  [{'methodChain': 'Party'     , 'label': 'Counterparty'},  
                    {'methodChain': 'Type'      , 'label': 'Type'},
                    {'methodChain': 'Amount'    , 'label': 'Amount'},       
                    {'methodChain': 'Currency'  , 'label': 'Currency'},       
                    {'methodChain': 'PayDay'    , 'label': 'Pay Day'},     
                    {'methodChain': 'ValidFrom' , 'label': 'Valid From'},
                    {'methodChain': 'Account'   , 'label': 'Cpty Account'},      
                    {'methodChain': 'OurAccount', 'label': 'Our Account'},         
                    {'methodChain': 'Text'      , 'label': 'Text'}]
        if self._HasFxPayments():
            columns.insert(6, {'methodChain': 'FxTransaction' , 'label': 'FX'})
        return columns

    def AddPayment(self, *args):
        self._CreateOrUpdatePayment()
    
    def RemovePayment(self, *args):
        if self._AssertSelectedPayment():
            selected = self.selectedPayment
            self.selectedPayment = None
            selected.Unsimulate()
    
    def UpdatePayment(self, *args):
        if self._AssertSelectedPayment():
            self._CreateOrUpdatePayment(self.selectedPayment)
    
    def SetSelectedPayment(self, attributeName, selectedElement):
        self.selectedPayment = selectedElement

    def SetFieldsFromSelectedPayment(self, *args):
        selectedPayment = self.selectedPayment
        if selectedPayment:
            self.amount       = selectedPayment.Amount()
            self.counterparty = selectedPayment.Party()
            self.currency     = selectedPayment.Currency()
            self.privatePayDay    = selectedPayment.PayDay()
            self.type         = selectedPayment.Type()
            self.privateValidFrom = selectedPayment.ValidFrom()
            self.cptyAccount  = selectedPayment.Account()
            self.ourAccount   = selectedPayment.OurAccount()
            self.text         = selectedPayment.Text()

    def TransformPayDay(self, attrName, value):
        value = self._PeriodToDateTransform(value)
        value = self._ValidateDate(value, 'Pay')
        return value
   
    def TransformValidFromDate(self, attrName, value):
        value = self._PeriodToDateTransform(value)
        value = self._ValidateDate(value, 'Valid From')
        return value

    def TransformToDomain(self, attrName, value):
        if value and isinstance(value, basestring):
            domain = self.GetMethod("GetAttributeMetaData")(attrName, "domain")()
            try:
                value = domain[value]
            except:
                pass
        return value

    def CptyAccountChoices(self, attributeName):
        if self._counterAccountChoices.IsEmpty():
            self.UpdateCptyAccountChoices()
        return self._counterAccountChoices
    
    def UpdateCptyAccountChoices(self, *args):
        self._counterAccountChoices.Clear()
        self._counterAccountChoices.AddAll(self._ValidAccounts(self.counterparty))
    
    def OurAccountChoices(self, attributeName):
        if self._ourAccountChoices.IsEmpty():
            self.UpdateOurAccountChoices()
        return self._ourAccountChoices
    
    def UpdateOurAccountChoices(self, *args):
        self._ourAccountChoices.Clear()
        acquirer = self.Trade().Acquirer() if self.Trade() else None
        self._ourAccountChoices.AddAll(self._ValidAccounts(acquirer))

    # ####################### #
    #   Convenience Methods   #
    # ####################### #
    
    def PrivatePayDay(self, value="Reading"):
        if value == "Reading":
            return self.privatePayDay
        else:
            self.privatePayDay = value
    
    def PrivateValidFrom(self, value="Reading"):
        if value == "Reading":
            return self.privateValidFrom
        else:
            self.privateValidFrom = value
    
    def Trade(self):
        return self.GetMethod(self._tradeName)()
    
    def GetPaymentsLayout(self):
        return self.UniqueLayout("""
                    hbox(;
                        paymentsList;
                        vbox(;
                            add;
                            update;
                            remove;
                        );
                    );
                    hbox(;
                    vbox(;
                        counterparty;
                        type;
                    );
                    vbox(;
                        amount;
                        currency;
                    );
                    vbox(;
                        payDay;
                        validFrom;
                    );
                    vbox(;
                        cptyAccount;
                        ourAccount;
                    );
                        text;
                    );
               """)
    
    def _AssertSelectedPayment(self, *args):
        if self.selectedPayment is not None:
            if self._IsFxPayment(self.selectedPayment):
                raise DealPackageUserException('Not possible to edit fx payments')
            return True
        
    def _HasFxPayments(self):
        payments = self.Trade().Payments() if self.Trade() else []
        for payment in payments:
            if self._IsFxPayment(payment):
                return True
        return False
        
    def _IsFxPayment(self, payment):
        return payment.FxTransaction() != 'None'
    
    def _CreateOrUpdatePayment(self, payment=None):
        if not self.counterparty:
            raise DealPackageUserException('Counterparty required')
        if not self.privatePayDay:
            raise DealPackageUserException('Pay day required')
        if not self.currency:
            raise DealPackageUserException('Currency required')
            
        if not payment:
            payment = self.Trade().CreatePayment()
        payment.Amount(self.amount)
        payment.Party(self.counterparty)
        payment.Currency(self.currency)
        payment.PayDay(self.privatePayDay)
        payment.Type(self.type)
        payment.ValidFrom(self.privateValidFrom)
        payment.Account(self.cptyAccount)
        payment.OurAccount(self.ourAccount)
        payment.Text(self.text)
        return payment

    def _GetPaymentOrTradeCurrency(self):
        currency = self.currency
        if not currency and self.Trade():
            currency = self.Trade().Currency()
        if not currency:
            mappedValuationParameter = acm.GetFunction('mappedValuationParameters', 0)
            currency = mappedValuationParameter().Parameter().AccountingCurrency()
        return currency

    def _GetPaymentOrTradeCalendar(self):
        return self._GetPaymentOrTradeCurrency().Calendar()

    def _ValidateDate(self, date, dateName):
        adjustedDate = date
        calendar = self._GetPaymentOrTradeCalendar()
        if date and calendar and calendar.IsNonBankingDay(None, None, date):
            if self._ShowAdjustDateDialog(dateName, calendar, date):
                adjustedDate = calendar.ModifyDate(None, None, date, "Following")
        return adjustedDate
    
    def _ShowAdjustDateDialog(self, name, calendar, date):
        return self.GetMethod('DealPackage')().GUI().AskAdjustDate(name, calendar, date)
    
    def _PeriodToDateTransform(self, newDate):
        date = newDate
        if acm.Time().PeriodSymbolToDate(newDate):
            date = acm.Time().PeriodSymbolToDate(newDate)
        return date
    
    def _BuildQuery(self, party, currency):
        query = acm.CreateFASQLQuery(acm.FAccount, 'AND')
        query.AddAttrNode('Party.Oid', 'EQUAL', party.Oid())
        currNode = query.AddOpNode('OR')
        currNode.AddAttrNode('Currency.Oid', 'EQUAL', currency.Oid())
        currNode.AddAttrNode('Currency.Oid', 'EQUAL', 0)
        typeNode = query.AddOpNode('OR')
        typeNode.AddAttrNode('AccountType', 'EQUAL', "Cash and Security")
        typeNode.AddAttrNode('AccountType', 'EQUAL', "Cash")
        typeNode.AddAttrNode('AccountType', 'EQUAL', None)
        return query
    
    def _ValidAccounts(self, party):
        validAccounts = None
        currency = self._GetPaymentOrTradeCurrency()
        if party and currency:
            validAccounts = self._BuildQuery(party, currency).Select()
        return validAccounts if validAccounts else acm.FArray()


class OperationsPanel(CompositeAttributeDefinition):
    
    def OnInit(self, panelName = 'Operations', **kwargs):
        assert panelName and isinstance(panelName, ''.__class__)
        self.panelName = panelName
        self._kwargs = kwargs
        self.allConfirmations = acm.FSortedCollection()
        self.allSettlements = acm.FSortedCollection() 
        self.toolTip = 'All trade %s belonging to the deal package'  
               
    def Attributes(self):
        return {'confirmations':    Object( label='',
                                             domain = 'FSortedCollection(FConfirmation)',
                                             objMapping = self.UniqueCallback("AllConfirmations"),
                                             toolTip = self.toolTip % 'confirmations',
                                             columns = self.ConfirmationDefaultColumns(),
                                             **self._kwargs),
                                           
                'settlements':    Object( label='',
                                             domain = 'FSortedCollection(FSettlement)',                
                                             objMapping = self.UniqueCallback("AllSettlements"),
                                             toolTip = self.toolTip % 'settlements',
                                             columns = self.SettlementDefaultColumns(),
                                             **self._kwargs),
                                            
                'update':    Action( label = 'Refresh',
                                             action = self.UniqueCallback("@Regenerate"),
                                             toolTip = 'Regenerate list of confirmations and settlements',
                                             **self._kwargs),
               }               
               
    def OperationsPane(self, *args):
        return [ 
                    {
                        self.panelName: self.GetLayout(), 
                    } 
                ] 
    
    def GetLayout(self):
        return self.UniqueLayout(
                   """
                     vbox[Settlements;
                        settlements;
                     ];                   
                     vbox[Confirmations;
                        confirmations;
                     ];
                     hbox(;
                         fill;
                         update;
                     );
                   """
               )
               
    def SettlementDefaultColumns(self, *args):
        return    [
                        {'methodChain': 'Name',                                   'label': 'Name'},
                        {'methodChain': 'Currency',                               'label': 'Currency'},                                
                        {'methodChain': 'Amount',                                 'label': 'Amount'},      
                        {'methodChain': 'ValueDay',                               'label': 'Value Day'},
                        {'methodChain': 'Status',                                 'label': 'Status'},
                        {'methodChain': 'Type',                                   'label': 'Type'},
                        {'methodChain': 'Trade',                                  'label': 'Trade'},
                        {'methodChain': 'Trade.ContractTrdnbr',                   'label': 'Contract Trade'},
                        {'methodChain': 'AcquirerAccName',                        'label': 'Account'},
                        {'methodChain': 'CounterpartyAccName',                    'label': 'Account'},                                   
                        {'methodChain': 'CreateUser',                             'label': 'Create User'},                
                        {'methodChain': 'CreateTime',                             'label': 'Create Time'},                
                        {'methodChain': 'UpdateUser',                             'label': 'Update User'},                
                        {'methodChain': 'UpdateTime',                             'label': 'Update Time'},     
                  ]
                  
    def ConfirmationDefaultColumns(self, *args):
        return    [
                        {'methodChain': 'Name',                                   'label': 'Name'},
                        {'methodChain': 'Status',                                 'label': 'Status'},                                
                        {'methodChain': 'EventChlItem',                           'label': 'Event'},      
                        {'methodChain': 'ConfTemplateChlItem',                    'label': 'Template'},
                        {'methodChain': 'ConfInstruction',                        'label': 'Confirmation Rule'},
                        {'methodChain': 'DocumentIds',                            'label': 'Documents'},
                        {'methodChain': 'Transport',                              'label': 'Transport'},
                        {'methodChain': 'Stp',                                    'label': 'STP'},           
                        {'methodChain': 'SignOffStatus1',                         'label': 'Sign Off Status 1'},                
                        {'methodChain': 'SignOffStatus2',                         'label': 'Sign Off Status 2'},                
                        {'methodChain': 'ChaserCutoff',                           'label': 'Chaser Cut-off Date'},                
                        {'methodChain': 'CounterpartyContact',                    'label': 'Counterparty Contact'},                
                        {'methodChain': 'AcquirerContact',                        'label': 'Acquirer Contact'},      
                        {'methodChain': 'StatusExplanationText',                  'label': 'Status Explanation'},                
                        {'methodChain': 'CreateUser',                             'label': 'Create User'},                
                        {'methodChain': 'CreateTime',                             'label': 'Create Time'},                
                        {'methodChain': 'UpdateUser',                             'label': 'Update User'},                
                        {'methodChain': 'UpdateTime',                             'label': 'Update Time'},     
                  ]                         

    def AllConfirmations(self, *args):
        if not self._IsEmpty():
            return self.allConfirmations
        else:
            self._ClearAndRepopulateLists()
            return self.allConfirmations
        
    def AllSettlements(self, *args):
        if not self._IsEmpty():
            return self.allSettlements
        else:
            self._ClearAndRepopulateLists()
            return self.allSettlements 
            
    def Regenerate(self, *args):
        self._ClearAndRepopulateLists()            

    def _IsEmpty(self):
        return self.allConfirmations.IsEmpty() and self.allSettlements.IsEmpty()
 
    def _ClearAndRepopulateLists(self):
        self.allConfirmations.Clear()
        self.allSettlements.Clear()
        dp = self.GetMethod('DealPackage')()
        confirmations = getattr(dp, 'Confirmations')()
        settlements = getattr(dp, 'Settlements')()        
        self.allConfirmations.AddAll(confirmations)
        self.allSettlements.AddAll(settlements)        
