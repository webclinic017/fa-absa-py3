
import FUxUtils
import FUxCore
import acm

def flatten( l ):
    return  [item for sublist in l for item in sublist]

class FieldInfo(object):
    
    def __init__(self, columnParameterDefinition, populator, is_mandatory, counter):
        self.m_columnParameterDefinition = columnParameterDefinition
        self.m_name = self.m_columnParameterDefinition.Name()
        self.m_isMandatory = is_mandatory
        self.m_counter = counter
        
    def Name(self):
        return self.m_name
        
    def IsMandatory(self):
        return self.m_isMandatory
        
    def DisplayName(self):
        name = self.ColumnParameterDefinition().DisplayName() if self.ColumnParameterDefinition().IsValid() else self.ColumnParameterDefinition().Name()
        if self.IsMandatory():
            name += "*"
        return name
        
    def ColumnParameterDefinition(self):
        return self.m_columnParameterDefinition

    def _hasError(self):
        return self.m_error is not None
        
    def _initialValue(self, all_values):
        try:
            initial_value = all_values[self.Name()]
        except Exception as e:
            return None
        else:
            return initial_value
    
class StandardFieldInfo( FieldInfo ):
    DEFAULT_DOMAIN = "string"
    ebTag = acm.CreateEBTag()
    
    def __init__(self, columnParameterDefinition, customPopulator, is_mandatory, counter):
        FieldInfo.__init__( self, columnParameterDefinition, customPopulator, is_mandatory, counter )
        populator = None
        try:
            self.m_columnParameterDefinition.Validate()
        except Exception as e:
            self.m_error = e
            self.m_description = None
            self.m_domain = StandardFieldInfo.DEFAULT_DOMAIN
            formatter = None
        else:
            self.m_error = None
            self.m_description = self.m_columnParameterDefinition.LiveColumnDefinition().ColumnDescription()
            self.m_domain = self.m_columnParameterDefinition.ParameterDomain()
            formatter = self.m_columnParameterDefinition.Formatter()
            if customPopulator:
                populator = customPopulator
            else:
                populator = self.m_columnParameterDefinition.LiveColumnDefinition().ChoiceListSource( None, self.ebTag )
        
        self.m_binder = acm.FUxDataBindings().AddBinder(self.m_name, acm.GetDomain(self.m_domain), formatter, populator)
        self.m_binder.AddDependent(self)

    def Init(self, layout, initialValues):
        self.m_binder.InitLayout(layout)
        self.m_binder.ToolTip(self.m_description)
        
        if self._hasError():
            self.m_binder.SetValue(self.m_error, False)
            self.m_binder.Enabled(False)
        else:
            self.m_binder.SetValue(self._initialValue(initialValues), False)
            self.m_binder.Enabled(True)

    def GetValue(self):
        if not self.m_binder.Validate(True):
            raise Exception("Invalid value.")        
        return self.m_binder.GetValue()
    
    def BuildLayoutPart(self, builder):
        builder.BeginHorzBox()
        self.m_binder.BuildLayoutPart(builder, self.DisplayName())
        builder.EndBox()
    
    def Clear(self):
        self.m_binder.SetValue(None, False)
        
    def Enabled(self, isEnabled):
        self.m_binder.Enabled(isEnabled)

    def AddChangedCallback( self, callbackFunction, layout ):
        ctrl = layout.GetControl( self.Name() )
        ctrl.AddCallback( str(self.m_domain) == 'bool' and 'Activate' or 'Changed', callbackFunction, 0 )
        
class CustomFieldInfo( FieldInfo ):
    
    def __init__(self, parent, columnParameterDefinition, populator, is_mandatory, counter):
        FieldInfo.__init__( self, columnParameterDefinition, populator, is_mandatory, counter )
        self.m_parent = parent
        
        try:
            self.m_columnParameterDefinition.Validate()
        except Exception as e:
            self.m_error = e
            self.m_description = None
        else:
            self.m_error = None
            self.m_description = self.m_columnParameterDefinition.LiveColumnDefinition().ColumnDescription()

    def Init(self, layout, initialValues):
        if self._hasError():
            self.m_objectText.SetData(self.m_error)
            self.m_objectText.Editable( False )
            self.m_objectBtn.Enabled( False )
            self.m_value = self.m_error
        else:
            self.m_objectBtn = layout.GetControl( "selectButton" + str(self.m_counter) )
            self.m_objectText = layout.GetControl( "objectText" + str(self.m_counter) )
            self.m_value = self._initialValue(initialValues)
            self.m_objectText.SetData( self.m_value if self.m_value is not None else "" )
            self.m_objectText.Editable( False )
            self.m_objectBtn.ToolTip(self.m_description)
            self.m_objectText.ToolTip(self.m_description)

    def BuildLayoutPart(self, builder):
        builder.BeginHorzBox()
        builder.AddInput('objectText' + str(self.m_counter), self.DisplayName(), 20, -1, 40, "Default", False)
        builder.AddButton('selectButton' + str(self.m_counter), '...', False, True)
        builder.EndBox()
       
    def Enabled(self, isEnabled):
        self.m_objectBtn.Enabled(isEnabled)

    def GetValue(self):
        return self.m_value
    
    def Clear(self):
        self.m_value = None
        self.m_objectText.SetData( "" )
        
    def AddChangedCallback( self, callbackFunction, layout ):
        self.m_objectText.AddCallback( 'Changed', callbackFunction, 0 )
        
def OnTimeBucketsClicked(self, ad):
    timeBuckets = acm.UX().Dialogs().SelectTimeBuckets(self.m_parent.m_fuxDlg.Shell(),
        self.m_value )
    if timeBuckets:
        self.m_value = timeBuckets
        self.m_objectText.SetData( timeBuckets.Name() )

class TimeBucketsFieldInfo( CustomFieldInfo ):
    
    def __init__(self, parent, columnParameterDefinition, populator, is_mandatory, counter):
        CustomFieldInfo.__init__( self, parent, columnParameterDefinition, populator, is_mandatory, counter )
        
    def Init(self, layout, initialValues):
        CustomFieldInfo.Init( self, layout, initialValues )
        self.m_objectBtn.AddCallback( "Activate", OnTimeBucketsClicked, self )

def OnScenarioClicked(self, ad):
    explicitScenario = acm.UX().Dialogs().SelectScenario(self.m_parent.m_fuxDlg.Shell())
    if explicitScenario:
        self.m_value = explicitScenario.ScenarioStorage()
        if self.m_value:
            self.m_objectText.SetData( self.m_value.Name() )

class ScenarioFieldInfo( CustomFieldInfo ):
    
    def __init__(self, parent, columnParameterDefinition, populator, is_mandatory, counter):
        CustomFieldInfo.__init__( self, parent, columnParameterDefinition, populator, is_mandatory, counter )
        
    def Init(self, layout, initialValues):
        CustomFieldInfo.Init( self, layout, initialValues )
        self.m_objectBtn.AddCallback( "Activate", OnScenarioClicked, self )

def OnFileSelectionClicked(self, ad):
    file = acm.FFileSelection()
    isSelected = acm.UX().Dialogs().BrowseForFile(self.m_parent.m_fuxDlg.Shell(), file)
    if isSelected:
        self.m_objectText.SetData(file.SelectedFile())
        self.m_value = file
        
def OnTextChangedCB(self, ad):
    file = acm.FFileSelection()
    file.SelectedFile( self.m_objectText.GetData() )
    self.m_value = file
    
class FileSelectionFieldInfo( CustomFieldInfo ):
    
    def __init__(self, parent, columnParameterDefinition, populator, is_mandatory, counter):
        CustomFieldInfo.__init__( self, parent, columnParameterDefinition, populator, is_mandatory, counter )
   
    def Init(self, layout, initialValues):
        CustomFieldInfo.Init( self, layout, initialValues )
        self.m_objectText.Editable(True)
        self.m_objectText.SetData( self.m_value.SelectedFile() if self.m_value is not None else "" )
        self.m_objectText.AddCallback( "Changed", OnTextChangedCB, self )
        self.m_objectBtn.AddCallback( "Activate", OnFileSelectionClicked, self )

class ColumnParameterizationDialog(FUxCore.LayoutDialog):
    def __init__(self, params):
        self.m_parameters = params
        self.m_controls, self.m_groups = self._createDynamicControls()
        
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        dlg.Caption('Apply Parameters')
        
        for control in self._flatControls():
            control.Init(layout, self._initalControlValues())
            if control.IsMandatory():
                control.AddChangedCallback( self.UpdateControls, layout )

        self.m_okBtn = layout.GetControl("ok")
        self.m_nameInput = layout.GetControl("name")
        self.UpdateControls()
    
    def HandleApply(self):
        try:
            params = {}
            for control in self._flatControls():
                value = control.GetValue()
                if value is not None:
                    params[acm.FSymbol(control.ColumnParameterDefinition().Name())] = value
                    
            config = acm.Sheet().Column().CreatorConfigurationFromColumnParameterDefinitionNamesAndValues( params )
            if self.EnableLabelInput():
                config = acm.Sheet().Column().CreatorConfigurationFromInitialCustomLabel( acm.FSymbol(self.m_nameInput.GetData()), config )
            return {acm.FSymbol("columnCreatorConfiguration") : config}
        except Exception:
            return None

    def OkButtonEnabled( self ):
        for control in self._flatControls():
            if control.IsMandatory():
                if control.GetValue() is None:
                    return False
        return True

    def EnableLabelInput( self ):
        enable = self.m_parameters.At( acm.FSymbol('enableLabelInput') )
        return enable != False

    def UpdateControls(self, *args, **kwargs):
        self.m_okBtn.Enabled( self.OkButtonEnabled() )
        self.m_nameInput.Visible( self.EnableLabelInput() )
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        for groupLabel in self.m_groups:
            b.BeginVertBox( 'EtchedIn', groupLabel )
            for control in self.m_controls[groupLabel]:
                control.BuildLayoutPart(b)
            b.EndBox()
        b.  BeginVertBox('Invisible')
        b.    AddInput("name", "Column Label", 17)
        b.  EndBox()
        b.  BeginHorzBox()
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddSpace(2)
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
        
    def _customFieldInfo( self, colParam, is_mandatory, counter ):
        return None
 
    def _customPopulator( self, colParam ):
        return None
       
    def _initalControlValues(self):
        return self.m_parameters.At(acm.FSymbol('columnParameterNamesAndInitialValues'))
    
    def _columnParameterDefinitions(self):
        return self.m_parameters.At(acm.FSymbol('columnParameters'))
    
    def _flatControls( self ):
        return flatten( self.m_controls.values() )
        
    def _createDynamicControls(self):
        ctrls = {}
        groups = []
        
        mandatoryParameterDefinitions = self.m_parameters.At( acm.FSymbol('mandatoryColumnParameters') )
        counter = 0
        for col_param in self._columnParameterDefinitions():
            try:
                col_param.Validate()
            except:
                pass
            is_mandatory = mandatoryParameterDefinitions and col_param in mandatoryParameterDefinitions
            fieldInfo = None
            customFieldInfo = self._customFieldInfo(col_param, is_mandatory, counter )
            if customFieldInfo:
                fieldInfo = customFieldInfo
            elif col_param.ParameterDomain() == acm.FStoredTimeBuckets:
                fieldInfo = TimeBucketsFieldInfo( self, col_param, None, is_mandatory, counter )
            elif col_param.ParameterDomain() == acm.FStoredScenario:
                fieldInfo = ScenarioFieldInfo( self, col_param, None, is_mandatory, counter )
            elif col_param.ParameterDomain() == acm.FFileSelection:
                fieldInfo = FileSelectionFieldInfo( self, col_param, None, is_mandatory, counter )
            else:
                fieldInfo = StandardFieldInfo(col_param, self._customPopulator( col_param ), is_mandatory, counter )
            counter += 1
            groupLabel = col_param.GroupLabel()
            if groupLabel in ctrls:
                ctrls[ groupLabel ].append( fieldInfo )
            else:
                groups.append( groupLabel )
                ctrls[ groupLabel ] = [fieldInfo]
        return ctrls, groups


def ael_custom_dialog_show(shell, params):
    dlg = ColumnParameterizationDialog(FUxUtils.UnpackInitialData(params))
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
    
    
def ael_custom_dialog_main(parameters, dictExtra):
    return parameters
