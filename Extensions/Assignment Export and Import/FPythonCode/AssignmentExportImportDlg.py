""" Compiled: 2012-02-16 11:04:24 """

import acm
import FUxCore

parKeyAssignmentType = 'AssignemtType'
parKeyExportOrImport = 'ExportOrImport'
parKeyFilename = 'Filename'
parKeyOverwrite = 'Overwrite'

def StartDialog(eii):
    extObject = eii.ExtensionObject()
    shell = extObject.Shell()
    dialog = AssignmentExportDialog()
    if acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.createLayout(), dialog):

        parameters = dialog.parameters()
        exportOrImport = parameters.get(parKeyExportOrImport)
        assignmentType = parameters.get(parKeyAssignmentType)
        filename = parameters.get(parKeyFilename)
        overwrite = parameters.get(parKeyOverwrite)
        
        if "Export" == exportOrImport:
            performExport(assignmentType, filename, shell)
        else:
            performImport(assignmentType, filename, overwrite, shell)

def performExport(assignmentType, filename, shell):
    from AssignmentExport import AssignmentExporter
    if validateFile(filename, True):
        if "Routing" == assignmentType:
            if not AssignmentExporter.exportRouting(filename):
                acm.UX().Dialogs().MessageBoxInformation(shell, "Routing export encountered problems. See log for details.")

def performImport(assignmentType, filename, overwrite, shell):
    from AssignmentImport import AssignmentImporter
    if validateFile(filename, False):
        if "Routing" == assignmentType:
            if not AssignmentImporter.importRouting(filename, overwrite):
                acm.UX().Dialogs().MessageBoxInformation(shell, "Routing import encountered problems. See log for details.")
            
def validateFile(filename, write):
    result = True
    file = None
    try:
        file = open(filename, write and 'w' or 'r')
    except Exception as e:
        result = False
        readOrWrite = write and "writing" or "reading"
        acm.Log("Could not open file for %s: %s"%(readOrWrite, filename))
    finally:
        if file:
            file.close()
    return result

# ########################## Assignment Export Dialog #####################################
class AssignmentExportDialog(FUxCore.LayoutDialog):

    def __init__(self):
        self.m_bindings = None
        
        self.m_assignmentTypeCtrl = None
        self.m_fileOutputCtrl = None
        self.m_okBtn = None
        self.m_overwriteChk = None
        
        self.m_fuxDialog = None
        self.m_fileSelection = None
        self.m_parameters = {}
        self.initControls()
    
    def initControls(self):
        assTypesEnum = acm.FEnumeration["EnumAssignmentTypes"]
        assExportOrImportEnum = acm.FEnumeration["EnumAssignmentExportOrImport"]
        self.m_bindings = acm.FUxDataBindings()
        self.m_assignmentTypeCtrl = self.m_bindings.AddBinder('assignmentTypeCtrl', assTypesEnum)
        self.m_exportOrImportCtrl = self.m_bindings.AddBinder('exportImportCtrl', assExportOrImportEnum)

    def parameters(self):
        return self.m_parameters
    
    def HandleCreate(self, dialog, layout):
        self.m_fuxDialog = dialog
        self.m_bindings.AddLayout(layout)
        
        selectFileBtn = layout.GetControl('selectFile')
        selectFileBtn.AddCallback('Activate', onSelectFileButtonClicked, self)
        
        self.m_fileOutputCtrl = layout.GetControl('filename')
        self.m_fileOutputCtrl.Editable(False)
        
        self.m_okBtn = layout.GetControl('ok')
        self.m_okBtn.AddCallback('Activate', onOkButtonClicked, self)
        self.m_okBtn.Enabled(False)
        dialog.Caption("Assignment Export and Import")
        
        self.m_overwriteChk = layout.GetControl('overwrite')
        self.m_overwriteChk.Checked(True)
        
    def createLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.      BeginVertBox('EtchedIn', '')
        self.           m_assignmentTypeCtrl.BuildLayoutPart(b, "Assignment Type")
        self.           m_exportOrImportCtrl.BuildLayoutPart(b, "Export/Import")
        b.              AddCheckbox('overwrite', 'Overwrite members')
        b.              AddInput('filename', 'Filename', 40)
        b.              AddButton('selectFile', 'Select file...')
        b.      EndBox()
        b.      BeginVertBox('EtchedIn', '')
        b.              BeginHorzBox()
        b.                      AddFill()
        b.                      AddButton('ok', 'OK')
        b.                      AddButton('cancel', 'Cancel')
        b.              EndBox()
        b.      EndBox()
        b.EndBox()
        return b

    def updateFileSelection(self, fileSelection):
        self.m_fileSelection = fileSelection
        if self.m_fileSelection:
            filename = self.m_fileSelection.SelectedFile().StringKey()
            self.m_fileOutputCtrl.SetData(filename)
            self.m_okBtn.Enabled(None != filename)
            
    def storeParameters(self):
        self.m_parameters[parKeyAssignmentType] = self.m_assignmentTypeCtrl.GetValue()
        self.m_parameters[parKeyExportOrImport] = self.m_exportOrImportCtrl.GetValue()
        self.m_parameters[parKeyFilename] = self.m_fileOutputCtrl.GetData()
        self.m_parameters[parKeyOverwrite] = self.m_overwriteChk.Checked()
    
def onOkButtonClicked(self, arg):
    self.storeParameters()
    self.m_fuxDialog.CloseDialogOK()
    
def onSelectFileButtonClicked(self, arg):
    shell = self.m_fuxDialog.Shell()
    fileSelection = acm.FFileSelection()
    if acm.UX().Dialogs().BrowseForFile(shell, fileSelection):
        self.updateFileSelection(fileSelection)
