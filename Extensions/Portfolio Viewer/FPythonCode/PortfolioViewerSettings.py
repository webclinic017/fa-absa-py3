""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/PortfolioViewer/etc/PortfolioViewerSettings.py"
"""--------------------------------------------------------------------------
MODULE
    PortfolioViewerSettings

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Help File to the Portfolio Viewer Application that handles application 
    settings and column selections in the GUI.

-----------------------------------------------------------------------------"""
import FUxCore
import acm

""" --- VIEW SETTINGS DIALOG --- """
class ViewSettingsDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.application = None
        self.dlg = None
    
    def HandleApply(self):
        #Portfolio or Depot
        self.application.userSettings.AtPut('defDataType', self.dTypeCtrl.GetData())

        if not CheckLoadRange(self, self.loadRangeCtrl.GetData()):
            acm.UX.Dialogs().MessageBoxInformation(self.dlg.Shell(), 'Please enter an integer between 1-1000.')
            return None
        self.application.userSettings.AtPut('loadRange', int(self.loadRangeCtrl.GetData()))
        self.application.userSettings.AtPut('showDepotTreeExpanded', self.depTreeExpCtrl.Checked())
        self.application.userSettings.AtPut('depWithoutParentTree', self.displayWOParentInTreeCtrl.Checked())
        self.application.userSettings.AtPut('useSlopeInSearch', self.slopeSearchCtrl.Checked())

        self.application.userSettings.AtPut('saveColumnSelections', self.colSaveCtrl.Checked())

        self.application.userSettings.AtPut('showCurrentConditions', self.showCurrentConCtrl.Checked())
        self.application.userSettings.AtPut('fillConditionsAutomatically', self.showCondAutoCtrl.Checked())
        #Commission Types
        modelCategories = []
        if self.showAMSLimitsCtrl.Checked():
            modelCategories.append('AMS Limits')
        if self.showCollateralCtrl.Checked():
            modelCategories.append('Collateral')
        if self.showMarginCtrl.Checked():
            modelCategories.append('Margin')
        if self.showAllocFeeCtrl.Checked():
            modelCategories.append('Allocation Fee')
        if self.showCommissionCtrl.Checked():
            modelCategories.append('Commission')
        if self.showCsaCtrl.Checked():
            modelCategories.append('Commission Sharing')
        if self.showFillFeeCtrl.Checked():
            modelCategories.append('Fill fee')

        self.application.userSettings.AtPut('modelCategories', modelCategories)

        self.application.userSettings.AtPut('showListGridlines', self.listGridLinesCtrl.Checked())
        return True

    def HandleCreate(self, dlg, layout):
        self.dlg = dlg
        self.dlg.Caption('Portfolio Viewer Settings')
        self.dTypeCtrl = layout.GetControl('dType')
        self.dTypeCtrl.AddItem('Portfolio')
        self.dTypeCtrl.AddItem('Depot')
        self.dTypeCtrl.SetData(self.application.userSettings.At('defDataType'))
        self.dTypeCtrl.ToolTip('When clicking Save the Current Windows Size and Appearance as Default this will be saved as default start up type.')
        self.dTypeCtrl.AddCallback('Changed', ShowDepotViewSettings, self)

        self.colSaveCtrl = layout.GetControl('colSave')
        self.colSaveCtrl.Checked(self.application.userSettings.At('saveColumnSelections'))
        self.colSaveCtrl.ToolTip('Save column selection when saving the Current Windows Size and Appearance as Default and only displays items matching the search criterias.')

        self.listGridLinesCtrl = layout.GetControl('listGridLines')
        self.listGridLinesCtrl.Checked(self.application.userSettings.At('showListGridlines'))

        self.loadRangeCtrl = layout.GetControl('LoadRange')
        self.loadRangeCtrl.SetData(self.application.userSettings.At('loadRange'))
        self.loadRangeCtrl.ToolTip('Please use an integer between 1-1500')

        self.depTreeExpCtrl = layout.GetControl('showTreeExpanded')
        self.depTreeExpCtrl.Checked(self.application.userSettings.At('showDepotTreeExpanded'))
        self.displayWOParentInTreeCtrl = layout.GetControl('displayWOParentInTree')
        self.displayWOParentInTreeCtrl.Checked(self.application.userSettings.At('depWithoutParentTree'))
        self.slopeSearchCtrl = layout.GetControl('slopeSearch')
        self.slopeSearchCtrl.Checked(self.application.userSettings.At('useSlopeInSearch'))

        self.showCondAutoCtrl = layout.GetControl('showConditionsAuto')
        self.showCondAutoCtrl.Checked(self.application.userSettings.At('fillConditionsAutomatically'))
        self.showCondAutoCtrl.Label('Show conditions automatically when selecting a %s'%(self.application.userSettings.At('defDataType')).lower())
        self.showCurrentConCtrl = layout.GetControl('showCurrentCon')
        self.showCurrentConCtrl.Checked(self.application.userSettings.At('showCurrentConditions'))

        self.showAMSLimitsCtrl = layout.GetControl('showAMSLimits')
        self.showCollateralCtrl = layout.GetControl('showCollateral')
        self.showMarginCtrl = layout.GetControl('showMargin')
        self.showAllocFeeCtrl = layout.GetControl('showAllocFee')
        self.showCommissionCtrl = layout.GetControl('showCommission')
        self.showCsaCtrl = layout.GetControl('showCsa')
        self.showFillFeeCtrl = layout.GetControl('showFillFee')
        if 'AMS Limits' in self.application.userSettings.At('modelCategories'):
            self.showAMSLimitsCtrl.Checked(True)
        if 'Collateral' in self.application.userSettings.At('modelCategories'):
            self.showCollateralCtrl.Checked(True)
        if 'Margin' in self.application.userSettings.At('modelCategories'):
            self.showMarginCtrl.Checked(True)
        if 'Allocation Fee' in self.application.userSettings.At('modelCategories'):
            self.showAllocFeeCtrl.Checked(True)
        if 'Commission' in self.application.userSettings.At('modelCategories'):
            self.showCommissionCtrl.Checked(True)
        if 'Commission Sharing' in self.application.userSettings.At('modelCategories'):
            self.showCsaCtrl.Checked(True)
        if 'Fill fee' in self.application.userSettings.At('modelCategories'):
            self.showFillFeeCtrl.Checked(True)

        self.defSettings = layout.GetControl('useDefaultSettings')
        self.defSettings.AddCallback('Activate', DefaultSettings, self)
        ShowDepotViewSettings(self, None)

    def BuildLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'Settings')
        b.    AddOption('dType', 'Show type')
        b.    AddCheckbox('colSave', 'Save Column Selection')
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    BeginVertBox('EtchedIn', 'List View Settings')
        b.      AddCheckbox('listGridLines', 'Show Grid Lines')
        b.      AddInput('LoadRange', 'Load Range')
        b.      BeginVertBox('EtchedIn', 'Depot Settings')
        b.        AddCheckbox('showTreeExpanded', 'Automatically Expand Party Tree')
        b.        AddCheckbox('displayWOParentInTree', 'Show Depots Without Client in Tree')
        b.        AddCheckbox('slopeSearch', 'Use Curve Slope When Searching')
        b.      EndBox()
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'Condition View Settings')
        b.      AddCheckbox('showConditionsAuto', 'Show Conditions Automatically When Selecting a Portfolio')
        b.      AddCheckbox('showCurrentCon', 'Only Show Current Conditions')
        b.      BeginVertBox('EtchedIn', 'Conditional Model Types')
        b.        AddCheckbox('showAMSLimits', 'Include AMS Limits')
        b.        AddCheckbox('showCollateral', 'Include Collateral')
        b.        AddCheckbox('showMargin', 'Include Margin')
        b.        AddCheckbox('showAllocFee', 'Include Allocation Fee')
        b.        AddCheckbox('showCommission', 'Include Commission')
        b.        AddCheckbox('showCsa', 'Include Commission Sharing')
        b.        AddCheckbox('showFillFee', 'Include Fill fee')
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  AddSpace(10)
        b.  BeginHorzBox('None')
        b.    AddButton('useDefaultSettings', 'Use Default')
        b.    AddFill()
        b.    AddButton('ok', 'Save')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

def DefaultSettings(dialog, cd):
    #Default Settings for P-V application (read from dictionary)
    dialog.dTypeCtrl.SetData(dialog.application.defaultSettings.At('defDataType'))
    dialog.colSaveCtrl.Checked(dialog.application.defaultSettings.At('saveColumnSelections'))
    dialog.listGridLinesCtrl.Checked(dialog.application.defaultSettings.At('showListGridlines'))
    dialog.loadRangeCtrl.SetData(dialog.application.defaultSettings.At('loadRange'))
    dialog.depTreeExpCtrl.Checked(dialog.application.defaultSettings.At('showDepotTreeExpanded'))
    dialog.showCurrentConCtrl.Checked(dialog.application.defaultSettings.At('showCurrentConditions'))
    dialog.showCondAutoCtrl.Checked(dialog.application.defaultSettings.At('fillConditionsAutomatically'))
    dialog.displayWOParentInTreeCtrl.Checked(dialog.application.defaultSettings.At('depWithoutParentTree'))
    dialog.slopeSearchCtrl.Checked(dialog.application.defaultSettings.At('useSlopeInSearch'))
    dialog.showAMSLimitsCtrl.Checked(False)
    dialog.showCollateralCtrl.Checked(False)
    dialog.showMarginCtrl.Checked(False)
    dialog.showAllocFeeCtrl.Checked(False)
    dialog.showCommissionCtrl.Checked(False)
    dialog.showCsaCtrl.Checked(False)
    dialog.showFillFeeCtrl.Checked(False)
    if 'AMS Limits' in dialog.application.defaultSettings.At('modelCategories'):
        dialog.showAMSLimitsCtrl.Checked(True)
    if 'Collateral' in dialog.application.defaultSettings.At('modelCategories'):
        dialog.showCollateralCtrl.Checked(True)
    if 'Margin' in dialog.application.defaultSettings.At('modelCategories'):
        dialog.showMarginCtrl.Checked(True)
    if 'Allocation Fee' in dialog.application.defaultSettings.At('modelCategories'):
        dialog.showAllocFeeCtrl.Checked(True)
    if 'Commission' in dialog.application.defaultSettings.At('modelCategories'):
        dialog.showCommissionCtrl.Checked(True)
    if 'Commission Sharing' in dialog.application.defaultSettings.At('modelCategories'):
        dialog.showCsaCtrl.Checked(True)
    if 'Fill fee' in dialog.application.defaultSettings.At('modelCategories'):
        dialog.showFillFeeCtrl.Checked(True)
    #Update fields to be shown/hidden
    ShowDepotViewSettings(dialog, None)

def CheckLoadRange(dialog, nbrInput):
    try: 
        s = int(nbrInput)
        if s < 1:
            return False
        elif s > 1500:
            return False
        return s
    except:
        return False

def ShowDepotViewSettings(dialog, _):
    b = False
    if dialog.dTypeCtrl.GetData() == 'Depot':
        b = True
    dialog.depTreeExpCtrl.Visible(b)
    dialog.showCondAutoCtrl.Label('Show Conditions Automatically When Selecting a %s'%((dialog.dTypeCtrl.GetData())))
    dialog.displayWOParentInTreeCtrl.Visible(b)
    dialog.slopeSearchCtrl.Visible(b)


def StartViewSettingsDialog(application):
    dlg = ViewSettingsDialog()
    dlg.application = application
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Shell(), dlg.BuildLayout(), dlg)


""" --- COLUMN SELECTION DIALOG --- """
class columnSelectionDialog(FUxCore.LayoutDialog):
    def __init__(self):
        self.application = None
        self.selection = None
        self.availableCol = None
        self.settingsName = ''
        self.datatype = None

    def HandleApply( self ):
        selectedItems = []
        if self.datatype == 'Portfolio' or self.datatype == 'Depot' or self.datatype == "Client":
            selectedItems.append('Name')
        for row in self.cCList.GetRootItem().Children(): #Get all selected columns
            selectedItems.append(row.GetData())
        #Save as correct userSettings
        self.application.userSettings.AtPut(self.settingsName, selectedItems)
        return True

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Select columns')
        self.aCList = layout.GetControl('availableCol')
        self.aCList.AddColumn('Name')
        self.aCList.ShowColumnHeaders()
        self.aCList.ShowGridLines()
        aRoot = self.aCList.GetRootItem()
        for c in self.availableCol:
            i = aRoot.AddChild()
            i.Label(c)
            i.SetData(c)
        self.aCList.EnableHeaderSorting(True)
        self.aCList.AddCallback('SelectionChanged', ACListChanged, self)
        self.aCList.AddCallback('DefaultAction', AddToCurrent, self)

        self.cCList = layout.GetControl('currCol')
        self.cCList.AddColumn('Name')
        self.cCList.ShowColumnHeaders()
        self.cCList.ShowGridLines()
        cRoot = self.cCList.GetRootItem()
        for c in self.application.userSettings.At(self.settingsName):
            if c == 'Name':
                continue
            i = cRoot.AddChild()
            i.Label(c)
            i.SetData(c)
        self.cCList.AddCallback('SelectionChanged', CCListChanged, self)
        self.cCList.AddCallback('DefaultAction', RemoveCurrent, self)
        self.cCList.EnableHeaderSorting(False)

        self.addBtn = layout.GetControl('add')
        self.addBtn.Editable(False)
        self.addBtn.AddCallback('Activate', AddToCurrent, self)
        self.removeBtn = layout.GetControl('remove')
        self.removeBtn.Editable(False)
        self.removeBtn.AddCallback('Activate', RemoveCurrent, self)
        self.upBtn = layout.GetControl('up')
        self.upBtn.Editable(False)
        self.upBtn.AddCallback('Activate', MoveUp, self)
        self.downBtn = layout.GetControl('down')
        self.downBtn.Editable(False)
        self.downBtn.AddCallback('Activate', MoveDown, self)

    def createColumnSelectionLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b. BeginHorzBox('None')
        b.  BeginVertBox('EtchedIn', 'Available Columns')
        b.   AddList('availableCol', 10, 35, 40)
        b.  EndBox()
        b.  AddSpace(5)
        b.  BeginVertBox('None')
        b.   AddFill()
        b.   AddButton('add', 'Add')
        b.   AddSpace(10)
        b.   AddButton('remove', 'Remove')
        b.   AddFill()
        b.  EndBox()
        b.  AddSpace(5)
        b.  BeginVertBox('EtchedIn', 'Current Columns')
        b.   AddList('currCol', 10, 35, 40)
        b.   BeginHorzBox('None')
        b.    AddButton('up', 'Up')
        b.    AddButton('down', 'Down')
        b.   EndBox()
        b.  EndBox()        
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox('None')
        b.  AddFill()
        b.  AddButton('ok', 'Ok')
        b.  AddButton('cancel', 'Cancel')
        b. EndBox()
        b.EndBox()
        return b

def CCListChanged(dialog, _):
    selItem = dialog.cCList.GetSelectedItem()
    if selItem:
        if selItem.Sibling():
            dialog.downBtn.Editable(True)
        else:
            dialog.downBtn.Editable(False)
        if selItem.Sibling(False):
            dialog.upBtn.Editable(True)
        else:
            dialog.upBtn.Editable(False)
        dialog.removeBtn.Editable(True)
        dialog.addBtn.Editable(False)
    else:
        NothingSelected(dialog)

def ACListChanged(dialog, _):
    selItem = dialog.aCList.GetSelectedItem()
    if selItem:
        dialog.removeBtn.Editable(False)
        dialog.addBtn.Editable(True)
        dialog.downBtn.Editable(False)
        dialog.upBtn.Editable(False)
    else:
        NothingSelected(dialog) 

def NothingSelected(dialog):
    dialog.downBtn.Editable(False)
    dialog.upBtn.Editable(False)
    dialog.removeBtn.Editable(False)
    dialog.addBtn.Editable(False)

def AddToCurrent(dialog, _):
    item = dialog.aCList.GetSelectedItem()
    if item == None:
        return
    sib1 = item.Sibling()
    sib2 = item.Sibling(False)
    i = dialog.cCList.GetRootItem().AddChild()
    i.Label(item.GetData())
    i.SetData(item.GetData())
    item.Remove()
    if sib1:
        dialog.aCList.SetSelectedItems([sib1])
    elif sib2:
        dialog.aCList.SetSelectedItems([sib2])

def RemoveCurrent(dialog, _):
    item = dialog.cCList.GetSelectedItem()
    if item == None:
        return
    sib1 = item.Sibling()
    sib2 = item.Sibling(False)
    i = dialog.aCList.GetRootItem().AddChild()
    i.Label(item.GetData())
    i.SetData(item.GetData())
    item.Remove()
    if sib1:
        dialog.cCList.SetSelectedItems([sib1])
    elif sib2:
        dialog.cCList.SetSelectedItems([sib2])

def MoveUp(dialog, _):
    Move(dialog, False)

def MoveDown(dialog, _):
    Move(dialog, True)

def Move(dialog, down):
    #Switch labels and data for each FUXListItem.
    selItem = dialog.cCList.GetSelectedItem()
    name = selItem.GetData()
    sibling = selItem.Sibling(down)
    name2 = sibling.GetData()
    selItem.Label(name2)
    selItem.SetData(name2)
    selItem.Select(False)
    sibling.Label(name)
    sibling.SetData(name)
    sibling.Select()


def StartColumnSelection(application, columns, settngsName, datatype):
    """ Starts the column selection dialog. Application is the Portfolio Viewer instance, 
        columns the available and unused columns, settingsName is the name of the key in 
        the userSettings dictionary which stores the selected columns. Datatype is which 
        supported type (portfolio, depot, client, condition) that columns are being 
        selected for. """
    colDialog = columnSelectionDialog()
    colDialog.application = application
    colDialog.availableCol = columns
    colDialog.settingsName = settngsName
    colDialog.datatype = datatype
    builder = colDialog.createColumnSelectionLayout()
    return acm.UX().Dialogs().ShowCustomDialogModal(application.Frame().Shell(), builder, colDialog)

""" End of file """
