import acm
import FUxCore

def ClrEnabled():
    return acm.GetClass("ExternalPrimeApplication") != None
    
def ReallyStartDialog(shell):
    builder = CreateLayout()
    customDlg = myCustomDialog()    
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )

def StartDialog(eii):
    shell = eii.ExtensionObject().Shell()
    if not ClrEnabled():
        acm.UX().Dialogs().MessageBoxInformation(self.Shell(), 'useclrinacm flag is not enabled, please check the commandline flag')
    else:    
        ReallyStartDialog(shell);



def GetSelectedSignKeyFile(shell):    
    fs = acm.FFileSelection()
    fs.FileFilter = "SNK Files (*.snk)|*.snk"
    fs.PickExistingFile = True    
    result = acm.UX().Dialogs().BrowseForFile( shell, fs)
    if not result:
        return None
    fname = str(fs.SelectedFile())
    return fname
    
def GetSelectedExternalPrimeApplicationCommonLibraryPath(shell):    
    fs = acm.FFileSelection()    
    fs.PickDirectory = True
    result = acm.UX().Dialogs().BrowseForFile( shell, fs)
    if not result:
        return None
    dirname = str(fs.SelectedDirectory())
    return dirname
    
    
def OnSelectSignKeyFileClicked(self, cd):    
    file = GetSelectedSignKeyFile(self.m_fuxDlg.Shell())
    if file:
        self.m_SignKeyLocationText.SetData(file)

def OnSelectExternalPrimeApplicationCommonLibraryClicked(self, cd):        
    dirname = GetSelectedExternalPrimeApplicationCommonLibraryPath(self.m_fuxDlg.Shell())
    if dirname:
        self.m_ExtPrimeAppCommonLibPathValueText.SetData(dirname)    
    
def OnAddButtonClicked(self, cd):
    componentName = self.m_RemotingApplicationComponentText.GetData()
    try:
        acm.ExternalPrimeApplication.AddExternalApplicationComponent(componentName)
    except Exception as err:
        acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), str(err))
    
def OnRemoveButtonClicked(self, cd):
    componentName = self.m_RemotingApplicationComponentText.GetData()
    try:
        acm.ExternalPrimeApplication.RemoveExternalApplicationComponent(componentName)    
    except Exception as err:
        acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), str(err))
    
def OnStartAdminConsoleClicked(self, cd):
    acm.StartApplication("Administration Console", None)
        
def OnGenerateClicked(self, cd):
    version = self.m_AssemblyVersionValueText.GetData()
    assemblyName = self.m_AssemblyNameValueText.GetData()
    extappcommonlibpath = self.m_ExtPrimeAppCommonLibPathValueText.GetData()
    signkeyLocation = self.m_SignKeyLocationText.GetData()
    optimize = self.m_OptimizedModeChbox.Checked()
    versbose = self.m_VerboseModeChbox.Checked()    
    
    acm.ExternalPrimeApplication.GenerateRemoteAssembly(version, assemblyName, signkeyLocation, extappcommonlibpath, optimize, versbose)

    
class myCustomDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_remotingServerAddressLbl = None
        self.m_remotingServerAddressValueText = None
        self.m_remotingServerStatusLbl = None
        self.m_remotingServerStatusValueLbl = None
                
        self.m_AddBtn = None
        self.m_RemoveBtn = None
        self.m_StartAdminConsoleBtn = None        
        self.m_RemotingApplicationComponentText = None
        
        self.m_AssemblyVersionLbl = None
        self.m_AssemblyVersionValueText = None
        self.m_AssemblyNameLbl = None
        self.m_AssemblyNameValueText = None
        self.m_SignKeyLocationLbl = None
        self.m_SignKeyLocationText = None
        self.m_SignKeyLocationSelectBtn = None
        self.m_OptimizedModeChbox = None
        self.m_VerboseModeChbox = None
        self.m_ExtPrimeAppCommonLibPathLbl = None
        self.m_ExtPrimeAppCommonLibPathValueText = None
        self.m_ExtPrimeAppCommonLibPathSelectBtn = None
        self.m_GenerateAssemblyBtn = None
        
        
    def HandleApply( self ):        
        return None
    
    def UpdateControls(self):
        pass
        

    def PopulateData(self):        
        server = acm.ExternalPrimeApplication.MainApplicatonServer()        
        if server:        
            self.m_remotingServerAddressValueText.SetData(str(server.Address()))                    
            self.m_remotingServerStatusValueLbl.SetData(server.Status())
        else:
            exception = acm.ExternalPrimeApplication.MainApplicatonServerException()
            if exception:
                self.m_remotingServerAddressValueText.SetData(exception.Message())                    
                self.m_remotingServerStatusValueLbl.SetData("down")
        
        self.m_remotingServerAddressValueText.Editable(False)
        
        
        extprimeappcommonlibpath = acm.GetFunction("getInstallDir", 0)()
        self.m_ExtPrimeAppCommonLibPathValueText.SetData(extprimeappcommonlibpath)        
        self.m_AssemblyNameValueText.SetData("ACMNetClassesRemote.dll")
        self.m_AssemblyVersionValueText.SetData(acm.InternalVersion())
        self.m_AssemblyVersionValueText.Editable(False)
        
        
                
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('External Application Options')                        
        self.m_remotingServerAddressLbl = layout.GetControl("address")
        self.m_remotingServerAddressValueText = layout.GetControl("addressvalue")
        self.m_remotingServerStatusLbl = layout.GetControl("status")
        self.m_remotingServerStatusValueLbl = layout.GetControl("statusvalue")
        
        self.m_ExtPrimeAppCommonLibPathValueText = layout.GetControl("externalprimeapplicationcommonlibraryvalue")
        self.m_ExtPrimeAppCommonLibPathSelectBtn = layout.GetControl('selectcommonlib')
        self.m_ExtPrimeAppCommonLibPathSelectBtn.AddCallback('Activate', OnSelectExternalPrimeApplicationCommonLibraryClicked, self)
        
        self.m_AssemblyNameValueText = layout.GetControl("assemblynamevalue")
        self.m_AssemblyVersionValueText = layout.GetControl('assemblyversionvalue')
        
        self.m_GenerateAssemblyBtn = layout.GetControl("generate")
        self.m_SignKeyLocationText = layout.GetControl('signkeylocationvalue')           
        self.m_SignKeyLocationSelectBtn = layout.GetControl('selectsignkey')
        self.m_SignKeyLocationSelectBtn.AddCallback('Activate', OnSelectSignKeyFileClicked, self)
        
        self.m_RemotingApplicationComponentText = layout.GetControl('name')
        self.m_AddBtn = layout.GetControl('add')
        self.m_AddBtn.AddCallback('Activate', OnAddButtonClicked, self)
        self.m_RemoveBtn = layout.GetControl('remove')
        self.m_RemoveBtn.AddCallback('Activate', OnRemoveButtonClicked, self)
        self.m_StartAdminConsoleBtn = layout.GetControl('startadminconsole')
        self.m_StartAdminConsoleBtn.AddCallback('Activate', OnStartAdminConsoleClicked, self)
        self.m_OptimizedModeChbox = layout.GetControl('optimized')
        self.m_VerboseModeChbox = layout.GetControl('verbose')
        self.m_GenerateAssemblyBtn = layout.GetControl('generate')
        self.m_GenerateAssemblyBtn.AddCallback('Activate', OnGenerateClicked, self)
        self.PopulateData()


def CreateLayout():
    b = acm.FUxLayoutBuilder()
    #main
    b.BeginVertBox()    
    b.BeginHorzBox()
    b.  BeginVertBox('EtchedIn', 'External Application Server:')
    b.    BeginHorzBox()
    b.          AddLabel('address', 'Address:')    
    b.          AddInput('addressvalue', '')                
    b.    EndBox()
    b.    BeginHorzBox()
    b.          AddLabel('status', 'Status:')
    b.          AddLabel('statusvalue', '')
    b.    EndBox()    
    b.  EndBox()
    
    
    b.  BeginVertBox('EtchedIn', 'External Application Component (External Application Executable Name):')    
    b.    AddInput('name', 'Name')
    b.    BeginHorzBox()
    b.          AddButton('add', 'Add')
    b.          AddButton('remove', 'Remove') 
    b.          AddFill()
    b.          AddButton('startadminconsole', 'Start Admin Console', False, True)
    b.    EndBox()
    b.  EndBox()   
    b.  EndBox()
    
    
    b.BeginHorzBox('EtchedIn', 'External ACM.NET Assembly:')
    b.  BeginVertBox()    
    b.          BeginHorzBox()
    b.                  AddLabel('assemblyname', 'Assembly Name:')
    b.                  AddInput('assemblynamevalue', '')
    b.                  AddLabel('signkeylocation', 'Sign Key Path:')
    b.                  AddInput('signkeylocationvalue', '')
    b.                  AddButton('selectsignkey', '...', False, True)
    b.          EndBox()
    b.          BeginHorzBox()
    b.                  AddLabel('assemblyversion', 'Assembly Version:')
    b.                  AddInput('assemblyversionvalue', '')
    b.                  AddLabel('externalprimeapplicationcommonlibrary', 'ExternalPrimeApplicationCommon Library Path:')
    b.                  AddInput('externalprimeapplicationcommonlibraryvalue', '', 40)
    b.                  AddButton('selectcommonlib', '...', False, True)
    b.          EndBox()
    b.  EndBox()
    b.  BeginVertBox()
    b.          AddCheckbox('optimized', 'Optimized Mode:')
    b.          AddCheckbox('verbose', 'Verbose Mode:')
    b.  EndBox()
    b.  BeginVertBox()
    b.          AddButton('generate', 'Generate Assembly', False, True)
    b.  EndBox() 
    b.EndBox()  
    b.EndBox()
    return b
    
