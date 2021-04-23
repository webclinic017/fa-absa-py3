import acm
import BuildPackageGUI
import DatabaseDependenciesNetworkX as DatabaseDependencies
import datetime
import FLogger
import FUxCore
import tempfile
from operator import methodcaller
import os
import os.path
import PackageManager
import PackageInstallerParametersManager
import subprocess
import time
import traceback

parameters = PackageInstallerParametersManager.ParametersManager()
verbosity = int(parameters.read('message_verbosity'))
logger = FLogger.FLogger(name=__name__, level=verbosity)
verbosity_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
def subprocess_printlog(command, wait=True, replace=True, shell=False):
    if replace == True:
        command = command.replace('\\\\', '/');
        command = command.replace('\\', '/');
    logger.debug('subprocess command: %s' % command)
    if wait == True:
        sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        out, err = sp.communicate()
        if out:
            logger.info("Standard output of subprocess:")
            logger.info(out)
        if err:
            logger.info("Standard error of subprocess:")
            logger.info(err)
        logger.debug("returncode of subprocess: %s" % sp.returncode)        
    else:
        sp = subprocess.Popen(command, shell=shell)
        logger.debug("returncode of subprocess: %s" % sp.returncode)        

def GetDefaultPackage(package):
    logger.debug('GetDefaultPackage():')
    versions = package['versions']
    version = versions['default_version']
    if version:
        logger.info('default_version: %s' % version)
        return version
    version = versions['latest_version']
    version = versions[version]
    logger.info('default_version: %s' % version)
    return version
    
def CreateApplicationInstance():
    return PackageManagerDialog()

class PackageManagerDialog(FUxCore.LayoutApplication):
    def __init__(self):
        FUxCore.LayoutApplication.__init__(self)
        self.m_packageManager = PackageManager.PackageManager()   
        self.m_statusBarTextPane = None

    def InitControls(self):
        self.m_packageListCtrl = self.m_layout.GetControl("packageListCtrl")
        self.m_packageListCtrl.AddCallback("DefaultAction", self.PackageSelectedCallback, 'OpenSelected')
        self.m_packageListCtrl.AddCallback("SelectionChanged", self.PackageSelectedCallback, 'SelectionChanged')
        self.m_packageListCtrl.ShowColumnHeaders(True)
        self.m_packageListCtrl.ShowHierarchyLines(True)
        self.m_packageListCtrl.ColumnLabel(0, "Package")
        self.m_packageListCtrl.ColumnWidth(0, 200)
        self.m_packageListCtrl.AddColumn('Version', 75)
        self.m_packageListCtrl.AddColumn('Description', 300)
        self.m_packageListCtrl.AddColumn('Installed', 25)
        self.m_docBtn = self.m_layout.GetControl("docBtn")
        self.m_layout.GetControl("installBtn").AddCallback("Activate", self.InstallPackage, None)
        self.m_receivingServer = self.m_layout.GetControl('receivingServer')
        self.m_receivingServer.Editable(False)
        self.m_testModeCheckbox = self.m_layout.GetControl("testModeCheckbox")
        # Configuration controls - to be shown or hidden.
        self.m_configurationButton = self.m_layout.GetControl('configurationButton')
        self.m_configurationButton.AddCallback("Activate", self.OnConfigurationButton, None)
        self.configuration_controls = set()
        self.m_verbosity = self.m_layout.GetControl('verbosityCtrl')
        verbose_val = parameters.read('Verbosity')
        for each_verbosity in verbosity_levels:
            self.m_verbosity.AddItem(each_verbosity)
        self.m_verbosity.SetData(verbose_val)
        self.m_verbosity.AddCallback("Changed", self.OnVerbosity, None)
        self.configuration_controls.add(self.m_verbosity)
        #self.m_configurationBox = self.m_layout.GetControl('configurationBox')
        #self.configuration_controls.add(self.m_configurationBox)
        self.m_repositoryBox = self.m_layout.GetControl('repositoryBox')
        self.configuration_controls.add(self.m_repositoryBox)
        self.m_defaultDirectoryButton = self.m_layout.GetControl('defaultDirectoryButton')
        self.m_defaultDirectoryButton.AddCallback("Activate", self.OnDefaultFolder, None)
        self.configuration_controls.add(self.m_defaultDirectoryButton)
        self.m_defaultDirectoryCtrl = self.m_layout.GetControl('defaultDirectoryCtrl')
        self.m_defaultDirectoryCtrl.Editable(False)
        self.configuration_controls.add(self.m_defaultDirectoryCtrl)
        self.m_packageInstallationBox = self.m_layout.GetControl('packageInstallationBox')
        self.configuration_controls.add(self.m_packageInstallationBox)
        self.m_noOverWriteNewerCheckbox = self.m_layout.GetControl("noOverWriteNewerCheckbox")
        self.configuration_controls.add(self.m_noOverWriteNewerCheckbox)
        self.m_noOverWriteNewerCheckbox.AddCallback("Activate", self.InstallationBehaviorCallback, self.m_noOverWriteNewerCheckbox)
        self.m_noOverWriteExistingCheckbox = self.m_layout.GetControl("noOverWriteExistingCheckbox")
        self.configuration_controls.add(self.m_noOverWriteExistingCheckbox)
        self.m_noOverWriteExistingCheckbox.AddCallback("Activate", self.InstallationBehaviorCallback, self.m_noOverWriteExistingCheckbox)
        self.m_packageBuildingBox = self.m_layout.GetControl('packageBuildingBox')
        self.configuration_controls.add(self.m_packageBuildingBox)
        self.m_showDependencyTree = self.m_layout.GetControl('showDependencyTree')
        self.m_showDependencyTree.AddCallback("Activate", self.OnShowDependencyTree, None)
        self.configuration_controls.add(self.m_showDependencyTree)
        self.m_showExcludedDependencyTree = self.m_layout.GetControl('showExcludedDependencyTree')
        self.m_showExcludedDependencyTree.AddCallback("Activate", self.OnShowExcludedDependencyTree, None)
        self.configuration_controls.add(self.m_showExcludedDependencyTree)
        self.m_modifyConfigBtn = self.m_layout.GetControl('modifyConfigSettings')
        self.m_modifyConfigBtn.AddCallback("Activate", self.SaveModifiedConfigSettings, 'ONCE')
        self.configuration_controls.add(self.m_modifyConfigBtn)
        # End of configuration controls.
        self.m_docBtn.AddCallback("Activate", self.OpenDocumentation, None)
        self.m_layout.GetControl("modifyBtn").AddCallback("Activate", self.ModifyPackage, None)
        self.m_docBtn.AddCallback("Activate", self.OpenDocumentation, None)
        self.m_layout.GetControl("closeBtn").AddCallback("Activate", self.CloseDialog, None)
        '''self.m_filterCtrl = self.m_layout.GetControl("filterCtrl")
        self.m_filterOptionCtrl = self.m_layout.GetControl("filterOptionCtrl")
        self.m_filterCaseCtrl = self.m_layout.GetControl("filterCaseCtrl")
        self.m_filterOptionCtrl.Populate(['', 'Status', 'Category', 'Name', 'Tag', 'Version', 'Description'])
        self.m_filterCtrl.AddCallback('Changed', self.PopulatePackageList, False)
        self.m_filterOptionCtrl.AddCallback('Changed', self.PopulatePackageList, False)
        self.m_filterCaseCtrl.AddCallback('Changing', self.PopulatePackageList, False)'''
        self.PackageSelectedCallback('SelectionChanged')
        self.SetConfigurationVisible(str(parameters.read('ConfigurationVisible')) == 'True')
        self.UpdateParametersFields()

    def UpdateParametersFields(self):
        DefaultFolder = parameters.read('DefaultFolder')
        self.m_defaultDirectoryCtrl.SetData(DefaultFolder)
        self.m_verbosity.SetData(verbosity)
        self.m_receivingServer.SetData(acm.FACMServer().ADSAddress())
        self.m_noOverWriteNewerCheckbox.Checked(str(parameters.read('NoOverWriteNewerEntities')) == 'True')
        self.m_noOverWriteExistingCheckbox.Checked(str(parameters.read('NoOverWriteExistingEntities')) == 'True')
        self.m_showDependencyTree.Checked(str(parameters.read('ShowDependencyTree')) == 'True')
        self.m_showExcludedDependencyTree.Checked(str(parameters.read('ShowExcludedInDependencyTree')) == 'True')

    def OnShowDependencyTree(self, *args):
        try:
            showDependencyTree = self.m_showDependencyTree.Checked()
            logger.debug('ShowDependencyTree: %s %s' % (type(showDependencyTree), showDependencyTree))
            parameters.write('ShowDependencyTree', showDependencyTree)
        except:
            traceback.print_exc()


    def OnShowExcludedDependencyTree(self, *args):
        try:
            showExcludedDependencyTree = self.m_showExcludedDependencyTree.Checked()
            logger.debug('ShowExcludedInDependencyTree: %s %s' % (type(showExcludedDependencyTree), showExcludedDependencyTree))
            parameters.write('ShowExcludedInDependencyTree', showExcludedDependencyTree)
        except:
            traceback.print_exc()

    def OnVerbosity(self, *args):
        verbosity = PackageInstallerParametersManager.enum.getAttributeValue(self.m_verbosity.GetData())
        parameters.write('message_verbosity', verbosity)
        parameters.write('Verbosity', self.m_verbosity.GetData())
        logger.logger.level = parameters.read('message_verbosity')

    def OnDefaultFolder(self, *args):
        try:
            OldDefaultFolder = parameters.read('DefaultFolder')
            logger.debug('OldDefaultFolder: %s' % OldDefaultFolder)
            shell = self.Shell()
            fileSelection = acm.FFileSelection()
            fileSelection.PickDirectory(True)
            fileSelection.SelectedDirectory = OldDefaultFolder
            result =  acm.UX().Dialogs().BrowseForFile(shell, fileSelection)
            if result == True:
                NewDefaultFolder = str(fileSelection)
                logger.debug('OldDefaultFolder: %s  NewDefaultFolder: %s' % (OldDefaultFolder, NewDefaultFolder))
                parameters.write('DefaultFolder', NewDefaultFolder)
                self.m_defaultDirectoryCtrl.SetData(NewDefaultFolder)
                if OldDefaultFolder != NewDefaultFolder:
                    self.PopulateValues()
        except:
            logger.debug(traceback.format_exc())

    def SetConfigurationVisible(self, ConfigurationVisible):
        logger.debug('SetConfigurationVisible: %s %s' % (type(ConfigurationVisible), ConfigurationVisible))
        if ConfigurationVisible == True:
            self.m_configurationButton.Label('Hide Config')
            
        else:
            self.m_configurationButton.Label('Show Config')
        for control in self.configuration_controls:
            control.Visible(ConfigurationVisible)
        parameters.write('ConfigurationVisible', ConfigurationVisible)

    def OnConfigurationButton(self, *args):
        ConfigurationVisible = str(parameters.read('ConfigurationVisible'))
        if ConfigurationVisible == 'True':
            parameters.write('ConfigurationVisible', False)
        else:
            parameters.write('ConfigurationVisible', True)
        ConfigurationVisible = parameters.read('ConfigurationVisible')
        self.SetConfigurationVisible(ConfigurationVisible)

    def InstallationBehaviorCallback(self, *args):
        checkbox = args[0]
        if checkbox == self.m_noOverWriteNewerCheckbox:
            self.m_noOverWriteExistingCheckbox.Checked(False)       
        if checkbox == self.m_noOverWriteExistingCheckbox:
            self.m_noOverWriteNewerCheckbox.Checked(False)
        parameters.write('NoOverWriteNewerEntities', self.m_noOverWriteNewerCheckbox.Checked())
        parameters.write('NoOverWriteExistingEntities', self.m_noOverWriteExistingCheckbox.Checked())

    def UpdateUseGoldEntityIds(self, *params):
        logger.debug('UpdateUseGoldEntityIds()...')
    '''
    Command is ONCE, DAILY, ENABLE, or DISABLE.
    '''
    def SaveModifiedConfigSettings(self, command='ONCE',*params):
        extension_list = ['PackageInstallerParameters']
        context = acm.GetDefaultContext()
        for extn in extension_list:
            config_extension = context.GetExtension("FParameters", "FObject", extn)
            if config_extension:
                config_extension_clone = config_extension.Clone()
                config_extension_value = config_extension_clone.Value()
                for key in config_extension.Value().Keys():
                    config_extension_value.AtPut(key, str(parameters.read(key.AsString())))
                module = context.EditModule()
                module.AddExtension(config_extension_clone)
                module.Commit()

    def HandleCreateStatusBar(self, sb):
        self.m_statusBarTextPane = sb.AddTextPane(400)      

    def UpdateStatus_(self, text):
        self.m_statusBarTextPane.SetText(text)    

    def UpdateStatus(self, text):
        acm.SynchronizedCall(self.UpdateStatus_, [text])

    def CloseDialog(self, *params):
        self.Frame().Close()

    def ErrorMessage(self, msg):
        acm.UX().Dialogs().MessageBox(self.Shell(), 'Error', msg, 'OK', None, None, 'Button1', 'Button1')

    def GetDocumentation(self):
        documentation = []
        package = self.GetSelectedPackage()
        if package != None:
            path = os.path.join(package['path'], 'Doc')
            if os.path.isdir(path):
                for file in os.listdir(path):
                    file = os.path.join(path, file)
                    if not os.path.isdir(file):
                        documentation.append(file)
        return documentation

    def OpenDocumentation(self, *params):
        for file in self.GetDocumentation():
            os.startfile(file)

    def InstallPackage(self, *params):
        logger.debug('InstallPackage()...')
        package = self.GetSelectedPackage()
        self.m_packageManager.TestMode = self.m_testModeCheckbox.Checked()
        self.m_packageManager.install_package(package['meta']['name'], package['meta']['version'], False)
        logger.debug('InstallPackage().')

    def ModifyPackage(self, *params):
        logger.debug('ModifyPackage()...')
        package = self.GetSelectedPackage()
        metaData = package['meta']
        version = metaData['version']
        logger.debug('package: %s %s' % (type(package), package))
        self.RunBuildPackageGUI(version)            

    def GetSelectedPackage(self):
        selectedItem = self.m_packageListCtrl.GetSelectedItem()
        if selectedItem == None:
            return None
        package = selectedItem.GetData()
        logger.debug('package: %s %s' % (type(package), package))
        return package

    def PopulateValues(self):
        logger.debug('PopulateValues()...')
        self.UpdateStatus('Populating packages... please wait...')
        self.PopulatePackageList(True)
        self.UpdateStatus('Finished populating packages.')
        logger.debug('PopulateValues().')

    def HandleCreate(self, creation_context):
        self.m_layout = self.CreateLayout()
        self.m_layout = creation_context.AddPane(self.m_layout, 'Packages')
        self.InitControls()
        self.PopulateValues()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginHorzBox('None')
        b.    AddTree("packageListCtrl", 600, 400)
        b.    AddSpace(5)
        b.    BeginVertBox('None')
        b.      AddInput('receivingServer', 'Server')
        b.      AddButton('installBtn', 'Install Here', -1)
        b.      AddCheckbox('testModeCheckbox', 'Test only (no commit)')
        b.      AddButton('modifyBtn', 'Modify Here', -1)
        b.      AddButton('docBtn', 'View Docs', -1)
        b.      AddSpace(10)
        b.      AddButton('configurationButton', 'Configure')
#        b.      BeginVertBox('EtchedIn', 'Configuration', 'configurationBox')#
        b.      BeginVertBox('None')
        b.        AddOption('verbosityCtrl', 'Verbosity')
        b.        BeginVertBox('EtchedIn', 'Repository', 'repositoryBox')
        b.            AddButton('defaultDirectoryButton', 'Select')
        b.            AddInput('defaultDirectoryCtrl', None)
        b.        EndBox()
        b.        BeginVertBox('EtchedIn', 'Package Installer', 'packageInstallationBox')
        b.          AddCheckbox('noOverWriteNewerCheckbox', 'Do not update newer objects')
        b.          AddCheckbox('noOverWriteExistingCheckbox', 'Do not update any existing objects')
        b.        EndBox()
        b.        BeginVertBox('EtchedIn', 'Package Builder', 'packageBuildingBox')
        b.          BeginVertBox('Invisible', '', 'goldEntitiesFileBox')
        b.          EndBox()
        b.          AddCheckbox('showDependencyTree', 'Show dependency tree')
        b.          AddCheckbox('showExcludedDependencyTree', 'Show excluded in dependency tree')
        b.            AddButton('modifyConfigSettings', 'Save Changes')
        b.        EndBox()
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  AddSpace(5)
        #b.  BeginHorzBox('EtchedIn', 'Filter')
        #b.    AddInput('filterCtrl', 'Filter')
        #b.    AddOption('filterOptionCtrl', '', 20, 20)
        #b.    AddSpace(5)
        #b.    AddCheckbox('filterCaseCtrl', 'Case sensitive')
        #b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('closeBtn', 'Close')
        b.  EndBox()
        b.EndBox()
        return b

    def PackageSelectedCallback(self, action, *params):
        logger.debug('PackageSelectedCallback()...')
        try:
            selectedItem = self.GetSelectedPackage()
            logger.debug('selectedItem: action: %s %s %s' % (action, type(selectedItem), selectedItem))
            if selectedItem != None:
                #source = selectedItem #.GetData()
                if action == 'SelectionChanged':
                    self.m_docBtn.Enabled(bool(self.GetDocumentation()))
        except:
            logger.error(traceback.format_exc())
        finally:
            logger.debug('PackageSelectedCallback().')

    @FUxCore.aux_cb
    def PopulatePackageList(self, getPackages = False):
        began_populate_package_list = time.clock()
        logger.debug('Began PopulatePackageList(%s)...' % (getPackages))
        parameters.write('refresh_package_list', True)
        if getPackages == True:
            self.m_packages = self.m_packageManager.get_all_packages(False, True, self.UpdateStatus)
        #filter = self.m_filterCtrl.GetData()
        #caseSensitive = self.m_filterCaseCtrl.Checked()
        #filterOption = self.m_filterOptionCtrl.GetData()
        #filterOption = filterOption and filterOption.lower()
        #if filter and not caseSensitive:
        #    filter = filter.upper()
        rootItem = self.m_packageListCtrl.GetRootItem()
        for child in rootItem.Children().AsList():
            child.Remove()
        for package in sorted(self.m_packages.values(), cmp=lambda x, y: cmp(x.lower(), y.lower()), key=methodcaller('get', 'name', 'zzzzzzzzzz')):
            logger.debug('package: %s %s' % (type(package), package))
            package.setdefault('selected_version', package['latest_version'])
            metaData = package['versions'][package['latest_version']]['meta']
            '''if filter:
                for v in (metaData.values() if not filterOption else [metaData.get(filterOption, '')]):
                    if filter in (v if caseSensitive else v.upper()):
                        break
                else:
                    continue'''
            child = rootItem.AddChild()
            child.Label(metaData['name'], 0)
            child.Label(metaData['version'] + ('*' if package['selected_version'] != package['latest_version'] else ''), 1)
            child.Label(metaData.get('description', ''), 2)
            child.SetData(package['versions'][metaData['version']])
            # Show versions as child nodes here.
            version_keys = []
            for version in package['versions'].keys():
                version_keys.append(version)
            version_keys.sort()
            for version in version_keys:
                data = package['versions'][version]
                if version != 'default_version':
                    versioned_metadata = data['meta']
                    versioned_child = child.AddChild()
                    versioned_child.Label(versioned_metadata['name'], 0)
                    versioned_child.Label(version, 1)
                    versioned_child.Label(versioned_metadata.get('description', ''), 2)
                    versioned_child.SetData(data)
            child = child.Sibling()
        ended_populate_package_list = time.clock()
        elapsed_populate_package_list = ended_populate_package_list - began_populate_package_list
        logger.debug('Ended PopulatePackageList (%12.4f seconds).' % elapsed_populate_package_list)

    def ServerUpdate(self, sender, aspect, parameter):
        logger.debug('PackageManagerGUI.ServerUpdate: %s %s %s %s' % (type(sender), sender, aspect, parameter))
        try:
            self.PopulateValues()
        except:
            logger.error(traceback.format_exc())
        finally:
            logger.debug('PackageManagerGUI.ServerUpdate.')

    def RunBuildPackageGUI(self, package):
        try:
            package = self.GetSelectedPackage()
            logger.debug('RunBuildPackageGUI: package: %s %s' % (type(package), package))
            package_path = package['path']
            logger.debug('package_path: %s %s' % (type(package_path), package_path))        
            package_def = self.m_packageManager.get_repository()._get_package_def(package_path)
            logger.debug('package_def: %s %s' % (type(package_def), package_def))            
            if package_def['source_ads'] != acm.ADSAddress():
                self.ErrorMessage('Sorry, you cannot modify a package except in its source ADS. Consider installing the package first and then modifying it.')
                return
            BuildPackageGUI.modify_flag = True
            frame = acm.UX().SessionManager().StartApplication('Package Builder', True)
            BuildPackageGUI.modify_flag = False
            bpd = frame.CustomLayoutApplication()
            logger.debug('frame: %s %s' % (type(frame), frame))
            bpd.SetContentCaption('Modify or Update Package')
            logger.debug('bpd: %s %s' % (type(bpd), bpd))
            package_objects = bpd.GetPackageObjects(package, update_status = bpd.UpdateStatus)
            bpd.PopulatePackageObjectsTree(package_objects)
            previousObjects, exclusions = bpd.GetPreviousObjects(package)
            if len(previousObjects) < 1:
                raise Exception("Package must contain at least one object.")
            bpd.PopulateObjectList(previousObjects, update_status = bpd.UpdateStatus)
            # Restore exclusion state.
            logger.debug('Marking objects to be excluded from import...')
            for excluded_object in exclusions:
                DatabaseDependencies.difference(bpd.graph, excluded_object, True)
            bpd.UpdateFuxTreeControlFromGraph(bpd.graph)
            bpd.m_packageObjectsTree.AddDependent(self)
        except:
            logger.error(traceback.format_exc())
        finally:
            logger.debug('RunBuildPackageGUI().')
            
def Run(eii = None):
    acm.UX().SessionManager().StartApplication('Package Installer', None).Activate()

