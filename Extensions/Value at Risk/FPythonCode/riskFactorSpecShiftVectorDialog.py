import acm
import FUxCore
import FUxUtils
import os.path


def OnSetRiskType(self, cd):
    self.m_riskFactorGroup.Populate(self.RiskFactorGroups())

def OnSetGroup(self, cd):
    self.m_riskFactorSpec.Populate(self.RiskFactorSpecs())

def OnSelectShifts(self, cd):
    str = "relative,double,Relative %;absolute,double,Absolute"
    if self.m_shifts:
        shifts = \
            acm.UX().Dialogs().CreateNamedParametersVector(self.m_fuxDlg.Shell(),
                                    str, self.m_shifts, None,
                                    'Select Shifts', 'Shifts')
    else:
        shifts = \
            acm.UX().Dialogs().CreateNamedParametersVector(self.m_fuxDlg.Shell(),
                                    str, acm.FArray(), None,
                                    'Select Shifts', 'Shifts')
    if shifts:
        self.m_shifts = shifts
    self.UpdateControls()

class RiskFactorScenarioVectorDialog(FUxCore.LayoutDialog):

    def __init__(self):
        self.m_bindings = None
        self.m_initialData = None
        self.m_specHeader = None
        self.m_riskType = None
        self.m_riskFactorGroup = None
        self.m_riskFactorSpec = None
        self.m_shifts = None
        self.m_shiftsBtn = None
        self.m_shiftsEdit = None
        
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('Invisible')
        b.    AddComboBox('specHeader', 'Risk Factor Spec Header')
        b.    AddComboBox('riskType', 'Risk Factor Type')
        b.    AddComboBox('riskFactorGroup', 'Risk Factor Group')
        b.    AddComboBox('riskFactorSpec', 'Risk Factor Spec')
        b.    BeginHorzBox('None')
        b.      AddInput('shifts', 'Shifts' )
        b.      AddButton('shiftsBtn', '>', False, True )
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddSpace(50)
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
    
    def CreateToolTip(self):
        self.m_specHeader.ToolTip('Specify the Risk Factor Specification header')
        self.m_riskType.ToolTip('Specify the Risk Factor Type of the shift vector')
        self.m_riskFactorGroup.ToolTip('Specify the Risk Factor Group of the shift vector')
        self.m_riskFactorSpec.ToolTip('Specify the Risk Factor Spec of the shift vector')
        self.m_shiftsBtn.ToolTip('Define the relative and absolute shifts')
        self.m_shiftsEdit.ToolTip('Define the relative and absolute shifts')
    
    def DisplayErrorMessage(self, information):
        acm.UX().Dialogs().MessageBox(self.m_fuxDlg.Shell(), 'Information', information, 'Ok', None, None, 'Button1', 'Button1')
        
    def HandleApply(self):
        if not self.m_bindings.Validate(True):
            return None

        dictResult = self.m_bindings.GetValuesByName()        

        if not self.m_shifts:
            return None
        else:
            dictResult.AtPut('shifts', self.m_shifts)
            
        riskType = self.m_riskType.GetData()
        riskFactorGroup = self.m_riskFactorGroup.GetData()
        riskFactorSpec = self.m_riskFactorSpec.GetData()
        specHeader = self.m_specHeader.GetData()
        if not (riskType or riskFactorGroup or riskFactorSpec or specHeader):
            return None
        dictResult.AtPut('riskType', riskType)
        dictResult.AtPut('riskFactorGroup', riskFactorGroup)
        dictResult.AtPut('riskFactorSpec', riskFactorSpec)
        dictResult.AtPut('specHeader', specHeader)
        return dictResult
    
    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Risk Factor Scenario Shift Vector')
        
        self.m_specHeader = layout.GetControl('specHeader')
        self.m_specHeader.Populate(acm.FRiskFactorSpecHeader.Select(""))
        mappedSpecHeader = acm.GetFunction("mappedRiskFactorSpecHeader", 0)()
        self.m_specHeader.SetData(mappedSpecHeader.Parameter())
        
        self.m_riskType = layout.GetControl('riskType')
        enums = acm.FEnumeration['EnumRiskFactorTypes'].Values()
        self.m_riskType.Populate(enums.Slice(1, enums.Size()))

        self.m_riskFactorGroup = layout.GetControl('riskFactorGroup')
        self.m_riskFactorGroup.Populate(self.RiskFactorGroups())

        self.m_riskFactorSpec = layout.GetControl('riskFactorSpec')
        self.m_riskFactorSpec.Populate(self.RiskFactorSpecs())

        self.m_specHeader.AddCallback('Changed', OnSetRiskType, self)
        self.m_riskType.AddCallback('Changed', OnSetRiskType, self)
        self.m_riskFactorGroup.AddCallback('Changed', OnSetGroup, self)
        
        self.m_shiftsEdit = layout.GetControl('shifts')
        self.m_shiftsEdit.Editable(False)
        
        self.m_shiftsBtn = layout.GetControl('shiftsBtn')
        self.m_shiftsBtn.AddCallback('Activate', OnSelectShifts, self)
        self.m_bindings.AddLayout(layout)
        
        if self.m_initialData :
            self.m_specHeader.SetData(self.m_initialData["specHeader"])
            self.m_riskType.SetData(self.m_initialData["riskType"])
            self.m_riskFactorGroup.SetData(self.m_initialData["riskFactorGroup"])
            self.m_riskFactorSpec.SetData(self.m_initialData["riskFactorSpec"])
            self.m_shifts = self.m_initialData["shifts"]
        self.CreateToolTip()
        self.UpdateControls()

    def RiskFactorGroups(self):
        constr = "list = 'RiskFactorGroup'"
        if self.m_riskType.GetData():
            members_constr = "riskFactorGrpType = '%s'" %self.m_riskType.GetData()
            members = acm.FRiskFactorMember.Select(members_constr)
            groups = acm.FSet()
            for member in members:
                groups.Add(member.RiskFactorGroup())
            groupsArray = groups.AsArray()
            return groupsArray.SortByProperty("Name")
        return acm.FChoiceList.Select(constr)

    def RiskFactorSpecs(self):
        constr = ""
        if self.m_specHeader.GetData():
            constr = "rfspec = '%s'" % self.m_specHeader.GetData().Name()
            specs = acm.FRiskFactorSpec.Select(constr)
            act_specs = acm.FArray()
            if self.m_riskFactorGroup.GetData():
                group = self.m_riskFactorGroup.GetData()
                for spec in specs:
                    if spec.Rfg() == group:
                        act_specs.Add(spec)
                return act_specs.SortByProperty("Bucket")
            return specs
        else:
            return []
    
    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        self.UpdateControls()
    
    def ShiftsAsString(self):
        string = ""
        if self.m_shifts:
            for shift in self.m_shifts:
                if string:
                    string += " "
                string += str(shift.Parameter('relative'))
                string += " "
                string += str(shift.Parameter('absolute'))
        return string

    def UpdateControls(self):
        if self.m_shifts:
            self.m_shiftsEdit.SetData(self.ShiftsAsString())
        else:
            self.m_shiftsEdit.Clear()

def ael_custom_dialog_show(shell, parameters):
    dialog = RiskFactorScenarioVectorDialog()
    initData = FUxUtils.UnpackInitialData(parameters)
    if initData:
        dialog.m_initialData = initData.At('dialogData')
    dialog.InitControls()
    dialogData = acm.UX().Dialogs().ShowCustomDialogModal(shell, 
        dialog.CreateLayout(), dialog)
    if dialogData:
        resultDict = acm.FDictionary()
        resultDict.AtPut('dialogData', dialogData)
        return resultDict
    return None

def ael_custom_dialog_main(parameters, dictExtra):
    resultVector = []
    dialogData = parameters.At('dialogData')
    specHeader = dialogData.At('specHeader')
    riskType = dialogData.At('riskType')
    if not riskType:
        riskType = 0
    riskFactorGroup = dialogData.At('riskFactorGroup')
    riskFactorSpec = dialogData.At('riskFactorSpec')
    shifts = dialogData.At('shifts')
    builder = acm.CreateWithParameter('FRiskFactorScenarioBuilder', specHeader)
    rel = []
    abs = []
    for shift in shifts:
        rel.append(1.0 + shift.Parameter('relative') / 100)
        abs.append(shift.Parameter('absolute'))
    
    today = acm.Time().DateToday()
    entity = None
    if riskFactorSpec:
        entity = riskFactorSpec
    else:
        entity = riskFactorGroup
    return builder.CreateShiftVector(riskType, entity, rel, abs)
