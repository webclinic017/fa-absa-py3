import acm

import AdsComparator
import BuildPackage 
import PackageBuilderGUIAccPanes

# Use the native C++ dependency graph if available.
import DatabaseDependenciesNetworkX as DatabaseDependencies

import FLogger
import FUxCore
import os
import os.path
import PackageFileRepository
import PackageManager
import PackageInstallerParametersManager
import shutil
import subprocess
import time
import traceback
import xml.etree.ElementTree
import MenuPackager as Menu
import ael
META_INFO = ['name', 'version', 'contact', 'category', 'tag', 'status', 'description']
parameters = PackageInstallerParametersManager.ParametersManager()
verbosity = int(parameters.read('message_verbosity'))
logger = FLogger.FLogger(name=__name__, level=verbosity)
compileInReferencesDefault = True
dateTimeFormatter = acm.FDateTimeFormatter('DateOnly')
debug = False
modify_flag = False

def onSelectPackage(insQryDlgRef, arg):
    pass

def CreateApplicationInstance():
    logger.info('CreateApplicationInstance: %s' % (CreateApplicationInstance.func_code.co_argcount))
    # Hack to pass this information where a parameter cannot be passed.
    # TODO: This code is not multi-anything safe!
    return BuildPackageDialog(modify=modify_flag)
 
def subprocess_printlog(command, wait=True, shell=False):
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

def find_entity(treeitem, entity):
    if treeitem.GetData() == entity:
        treeitem.EnsureVisible()
        treeitem.Select()
        return
    for child in treeitem.Children():
        find_entity(child, entity)

def entity_for_key(key):
    class_name = key.split('[')[0]
    id = key.split('[')[1].split('|')[0]
    code = 'acm.%s["%s"]' % (class_name, id)
    logger.debug('code: %s' % code)
    object = eval(code)
    return object

def clean_list(oldlist):
    cleanlist = []
    for item in oldlist:
        if item != None:
            try:
                if item.IsKindOf(acm.FCommonObject):
                    if item not in cleanlist:
                        cleanlist.append(item)
            except:
                logger.error(traceback.format_exc())
    return cleanlist

def addUnique(objects, object):
    if object == None:
        logger.warn('Object is null, skipping.')
        return
    if object in objects:
        logger.warn('Already added, skipping: %s %s' % (object.ClassName(), object.StringKey()))
        return
    objects.append(object)

class FileAction:
    def __init__(self, action_type, transporter, pathname, update_status = None):
        self.action_type = action_type
        self.transporter = transporter
        self.pathname = pathname
        self.exclusions = set()
        self.update_status = update_status

    def fetch_ADS_objects(self, objects, restore=False):
        if   self.action_type == 'transporter':
            self.fetch_ADS_objects_transporter(objects)
        elif self.action_type == 'ambamsg':
            self.fetch_ADS_objects_ambamsg(objects, restore)
        elif self.action_type == 'extmod':
            self.fetch_ADS_objects_extmod(objects)
        elif self.action_type == 'workbook':
            self.fetch_ADS_objects_workbook(objects)

    def fetch_ADS_objects_transporter(self, objects):
        # The name must be found in the file.
        text = open(self.pathname, 'r').read()
        if   self.transporter == 'Extension Module':
            index = text.find('name')
            start_index = text.find('"', index + 1) + 1
            end_index = text.find('"', start_index + 1)
            name = text[start_index:end_index]
            extension = acm.FExtensionModule[name]
            if extension:
                addUnique(objects, extension)
            else:
                logger.warn('No extension module found named "%s".' % name)
        elif self.transporter == 'ASQL Query':
            name = os.path.basename(self.pathname)
            object = acm.FStoredASQLQuery[name]
            if object == None:
                logger.warn('Failed to retrieve ASQL query for: %s' % self.pathname)
            else:
                addUnique(objects, object)
        elif self.transporter == 'Trade Filter':
            text = open(self.pathname, 'r').read()
            root = xml.etree.ElementTree.fromstring(text)
            name = root.find('name').text
            owner = root.find('owner').text
            object = acm.FTradeFilter.Select01('name="%s" and owner="%s"' % (name, owner), None)
            if object:
                addUnique(objects, object)   
            else:
                logger.warn('Failed to retrieve ADS trade filter for "%s".' % self.pathname)
        elif self.transporter == 'Python':
            name = os.path.basename(self.pathname)
            name = os.path.splitext(name)[0]
            logger.debug('Python: %s %s %s.' % (self.pathname, type(name), name))
            object = acm.FAel[str(name)]
            if object == None:
                logger.warn('Failed to retrieve Python module for: %s' % self.pathname)
            else:
                addUnique(objects, object)   
        else:
            logger.warn('transporter "%s" not yet implemented.' % self.transporter)

    def fetch_ADS_objects_ambamsg(self, objects, restore=False):
        text = open(self.pathname, 'r').read()
        root = xml.etree.ElementTree.fromstring(text)
        for element in root.findall('MESSAGE'):
            try:
                message = xml.etree.ElementTree.tostring(element)
                if restore == False:
                    object = acm.AMBAMessage().CreatePreviousObjectFromMessage(message)
                else:
                    original_key = element.find('ORIGINAL_KEY')
                    code = 'acm.' + original_key.text
                    object = eval(code)
                reference_type = element.find('REFERENCE_TYPE')
                exclude_element = element.find('EXCLUDE_FROM_IMPORT')
                if exclude_element == None or exclude_element.text == '1':
                    exclude = True
                else:
                    exclude = False
                if exclude == True:
                    logger.info('Mark as "exclude from import": %s' % DatabaseDependencies.node_id(object))
                    self.exclusions.add(object)
                if reference_type != None:
                    if reference_type.text == 'root':
                        if object == None:
                            logger.warn('Failed to retrieve root object for:\n%s.' % message)
                        else:
                            #overwrite = PackageManager.message_older_than_object(element, object)
                            addUnique(objects, object) 
                            if self.update_status:
                                self.update_status('Retrieved: %s' % DatabaseDependencies.node_id(object))
                else:
                    if object == None:
                        logger.warn('Failed to retrieve object for:\n%s.' % message)
                    else:
                        addUnique(objects, object)   
            except:
                logger.error(traceback.format_exc())

    def fetch_ADS_objects_extmod(self, objects):
        text = open(self.pathname, 'r').read()
        index = text.find('name')
        start_index = text.find('"', index + 1) + 1
        end_index = text.find('"', start_index + 1)
        name = text[start_index:end_index]
        extension = acm.FExtensionModule[name]
        if extension:
            addUnique(objects, extension)   
        else:
            logger.warn('No extension module found named "%s".' % name)

    def fetch_ADS_objects_workbook(self, objects):
        text = open(self.pathname, 'r').read()
        root = xml.etree.ElementTree.fromstring(text)
        name = root.find('name').text
        owner = root.find('owner').text
        object = acm.FWorkbook.Select01('name="%s" and owner="%s"' % (name, owner), None)
        if object:
            addUnique(objects, object)   
        else:
            logger.warn('Failed to retrieve ADS workbook for "%s".' % self.pathname)

    def __str__(self):
        return 'type: %-15s transporter: %-15s pathname: %s' % (self.action_type, self.transporter, self.pathname)

def OnTimer(self):
    self.m_timerValue = self.m_timerValue + 1
    logger.info('timer: %s', self.m_timerValue)


class BuildPackageDialog(FUxCore.LayoutApplication):
    def __init__(self, repository = PackageFileRepository.PackageFileRepository(buildIndex = False), packageInfo = acm.FDictionary(), objects = [], modify=False):
        #traceback.print_stack()
        FUxCore.LayoutApplication.__init__(self)
        self.m_packageManager = PackageManager.PackageManager()    
        self.modify = modify
        self.m_packageFileRepository = repository
        self.m_packageInfo = packageInfo
        self.m_packageObjects = objects
        self.m_insertItemsDialog = None
        self.m_insertQueryItemsDialog = None
        self.m_package_objects = set()
        self.m_timerValue = 0
        self.graph = None
        self.m_statusBarTextPane = None
        self.m_defaultDirectoryCtrl = None
        self.m_queryFolderContent = False
        self.m_selected_path = None
        self.m_exclusions = acm.FList()
        self.m_exclusion_types = set()
        self.m_original_message = None
        
    def __get_date_time_val(self, date_time_val = None):
        actual_date_time_val = None
        if not date_time_val:
            actual_date_time_val = acm.Time().TimeNow().split('.')[0]
        return actual_date_time_val

    def InitialiseValues(self):
        self.m_versionCtrl.SetData('1')
        self.m_minorVersionCtrl.SetData('0')
        self.m_updateNumberCtrl.Editable(False)
        self.m_layout.GetControl('nameCtrl').SetData('')
        self.m_layout.GetControl('contactCtrl').SetData('')
        self.m_layout.GetControl('tagCtrl').SetData('')
        self.m_layout.GetControl('categoryCtrl').SetData('')
        self.m_layout.GetControl('statusCtrl').SetData('')
        self.m_layout.GetControl('descriptionCtrl').SetData('')
        self.m_layout.GetControl('updateUser').SetData('')
        self.m_layout.GetControl('updateDateTime').SetData(self.__get_date_time_val())
        

    def InitControls(self):
        self.m_exclusions = acm.FList()
        self.m_dependencies_items = set()
        self.m_original_message  = None
        self.m_packageObjectsTree = self.m_layout.GetControl("packageObjectsTree")
        self.m_versionCtrl = self.m_layout.GetControl('versionCtrl')
        self.m_minorVersionCtrl = self.m_layout.GetControl('minorVersionCtrl')
        self.m_updateNumberCtrl = self.m_layout.GetControl('updateNumberCtrl')
        self.m_updateDateTime = self.m_layout.GetControl('updateDateTime')
        self.m_updateUser = self.m_layout.GetControl('updateUser')
        #self.m_inspectPackageObjectBtn = self.m_layout.GetControl("inspectPackageObjectBtn")
        #self.m_openPackageObjectBtn = self.m_layout.GetControl("openPackageObjectBtn")
        self.InitialiseValues()
        self.m_packageObjectsTree.AddCallback("DefaultAction", self.FindEntityInDependencies, None)
        self.m_packageObjectsTree.ShowHierarchyLines(True)
        self.m_packageObjectsTree.ShowColumnHeaders(True)
        self.m_packageObjectsTree.ShowColumnHeaders(True)
        self.m_packageObjectsTree.ColumnLabel(0, "Name")
        self.m_packageObjectsTree.ColumnWidth(0, 200)
        self.m_packageObjectsTree.AddColumn("Class", 100)
        self.m_packageObjectsTree.ColumnLabel(1, "Class")
        self.m_packageObjectsTree.AddColumn("Table", 100)
        self.m_packageObjectsTree.ColumnLabel(2, "Table")
        self.m_packageObjectsTree.AddColumn("Oid", 50)
        self.m_packageObjectsTree.ColumnLabel(3, "Oid")
        self.m_packageObjectsTree.EnableMultiSelect(True)
        # Begin dependencies objects to show/hide.
        self.m_packageDependenciesBox = self.m_layout.GetControl('packageDependenciesBox')
        self.m_dependencies_items.add(self.m_packageDependenciesBox)
        self.m_packageDependenciesTree = self.m_layout.GetControl("packageDependenciesTree")
        self.m_dependencies_items.add(self.m_packageDependenciesTree)
        self.m_packageDependenciesTree.AddCallback("DefaultAction", self.ExpandDependencies, None)
        self.m_packageDependenciesTree.EnableMultiSelect(True)
        self.m_packageDependenciesTree.ShowHierarchyLines(True)
        self.m_packageDependenciesTree.ShowColumnHeaders(True)
        self.m_packageDependenciesTree.ShowColumnHeaders(True)
        self.m_packageDependenciesTree.ColumnLabel(0, "Name")
        self.m_packageDependenciesTree.ColumnWidth(0, 200)
        self.m_packageDependenciesTree.AddColumn("Class", 100)
        self.m_packageDependenciesTree.ColumnLabel(1, "Class")
        self.m_packageDependenciesTree.AddColumn("Table", 100)
        self.m_packageDependenciesTree.ColumnLabel(2, "Table")
        self.m_packageDependenciesTree.AddColumn("Oid", 60)
        self.m_packageDependenciesTree.ColumnLabel(3, "Oid")
        self.m_packageDependenciesTree.AddColumn("Reference", 60)
        self.m_packageDependenciesTree.ColumnLabel(4, "Reference")
        self.m_packageDependenciesTree.AddColumn("Include", 80)
        self.m_packageDependenciesTree.ColumnLabel(5, "Include")
        #self.m_inspectObjectBtn = self.m_layout.GetControl('inspectObjectBtn')
        #self.m_dependencies_items.add(self.m_inspectObjectBtn)
        #self.m_openObjectBtn = self.m_layout.GetControl('openObjectBtn')
        #self.m_dependencies_items.add(self.m_openObjectBtn)
        self.m_rememberExcludedDependencies = self.m_layout.GetControl('rememberExcludedDependencies')
        self.m_rememberExcludedDependencies.Checked(False)
        self.m_dependencies_items.add(self.m_rememberExcludedDependencies)
        # End dependencies objects.
        
        
        self.m_layout.GetControl("addObjectBtn").AddCallback("Activate", self.AddObject, None)
        self.m_layout.GetControl("addQueryFolderBtn").AddCallback("Activate", self.AddQueryFolderObject, None)
        #self.m_layout.GetControl("addMarketParams").AddCallback("Activate", self.AddMarketParams, None)
        #self.m_layout.GetControl("removeObjectBtn").AddCallback("Activate", self.RemoveObject, None)
        self.m_layout.GetControl("addUpdatedObjects").AddCallback("Activate", self.AddUpdatedObjects, None)
        
        # -----------
        #self.m_inspectPackageObjectBtn.AddCallback("Activate", self.InspectListObject, None)#left
        #self.m_inspectObjectBtn.AddCallback("Activate", self.InspectObject, None)#right
        #self.m_openPackageObjectBtn.AddCallback("Activate", self.OpenListObject, None) #this is on the left list control
        #self.m_openObjectBtn.AddCallback("Activate", self.OpenObject, None)#this is on te right tree control
        
        
        self.m_packageObjectsTree.AddCallback("ContextMenu", self.OnListContextMenu, None)
        # ----------
        self.m_packageDependenciesTree.AddCallback("ContextMenu", self.OnTreeContextMenu, None)
        self.m_layout.GetControl("closeBtn").AddCallback("Activate", self.CloseDialog, None)
        self.m_layout.GetControl("createBtn").AddCallback("Activate", self.BuildPackage, None)
        self.m_rememberExcludedDependencies.AddCallback("Activate", self.OnRememberExcludedDependencies, None)
        self.m_layout.GetControl("openRepoBtn").AddCallback("Activate", self.OpenRepositoryDir, None)
        self.m_packageDependenciesBox = self.m_layout.GetControl('packageDependenciesBox')
        if self.modify == True:
            self.m_layout.GetControl("diffBtn").AddCallback("Activate", self.DiffPackage, None)
            self.m_layout.GetControl("diffTargetBtn").AddCallback("Activate", self.DiffTarget, None)
        for field in ['Category', 'Status']:
            ctrl = self.m_layout.GetControl("%sCtrl" % field.lower())
            for value in str(parameters.read(field)).split(';'):
                ctrl.AddItem(value)
        self.SetShowDependencyTree()

    def SetShowDependencyTree(self):
        ShowDependencyTree = str(parameters.read('ShowDependencyTree'))
        for depend_object in self.m_dependencies_items:
            depend_object.Visible(ShowDependencyTree)

    def HandleCreateStatusBar(self, sb):
        self.m_statusBarTextPane = sb.AddTextPane(100)      

    @FUxCore.aux_cb
    def UpdateStatus_(self, text):
        self.m_statusBarTextPane.SetText(text, True)

    @FUxCore.aux_cb
    def UpdateStatus(self, text):
        acm.SynchronizedCall(self.UpdateStatus_, [text])

    def CloseDialog(self, *params):
        self.Frame().Close()

    def MenuAction(self):
        return Menu.IncludeExcludeItem(self)

    def ListMenuAction(self):
        return Menu.ListItem(self)

    def OnListContextMenu(self, ud, cd):
        commands = [
                    ['Remove', '', 'Remove', '', '', '', self.ListMenuAction, True],
                    ['Open', '', 'Open', '', '', '', self.ListMenuAction, True],
                    ['Properties', '', 'Properties', '', '', '', self.ListMenuAction, True]]
        
        menuBuilder = cd.At('menuBuilder')
        menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))
                
    def OnTreeContextMenu(self, ud, cd):
        b_excluded = False
        b_included = False
        b_exclude_class = False
        b_include_class = False
        try:
            if cd.IsKindOf(acm.FDictionary):
                selected_items = self.m_packageDependenciesTree.GetSelectedItems()
                for selected_item in selected_items:
                    exclude = ''
                    if selected_item.GetData():
                        exclude = DatabaseDependencies.get_attribute(self.graph, selected_item.GetData(), 'exclude', '+')
                    else:
                        if selected_item.Children()[0].GetData().ClassName().AsString() in self.m_exclusion_types:
                            b_exclude_class = True
                        else:
                            b_include_class = True
                            #exclude = '-'
                    if exclude == '-':
                        b_excluded = True
                    elif exclude == '+':
                        b_included = True
                commands = []
                if b_excluded and b_included:
                    commands = [
                    ['Remove', '', 'Remove', '', '', '', self.MenuAction, True],
                    ['Remove All of Class', '', 'Remove All of Class', '', '', '', self.MenuAction, True],
                    ['Include', '', 'Include', '', '', '', self.MenuAction, True], 
                    ['Include All of Class', '', 'Include All of Class', '', '', '', self.MenuAction, True],
                    ['Open', '', 'Open', '', '', '', self.MenuAction, True],
                    ['Properties', '', 'Properties', '', '', '', self.MenuAction, True]]
                elif b_excluded:
                    commands = [['Include', '', 'Include', '', '', '', self.MenuAction, True], 
                                ['Include All of Class', '', 'Include All of Class', '', '', '', self.MenuAction, True],
                                ['Open', '', 'Open', '', '', '', self.MenuAction, True],
                                ['Properties', '', 'Properties', '', '', '', self.MenuAction, True]]
                elif b_included:
                    commands = [['Remove', '', 'Remove', '', '', '', self.MenuAction, True], 
                                ['Remove All of Class', '', 'Remove All of Class', '', '', '', self.MenuAction, True],
                                ['Open', '', 'Open', '', '', '', self.MenuAction, True],
                                ['Properties', '', 'Properties', '', '', '', self.MenuAction, True]]
                elif b_exclude_class and (not b_excluded) and (not b_included):
                    if b_include_class:
                        commands = [['Include', '', 'Include', '', '', '', self.MenuAction, True],
                                    ['Remove', '', 'Remove', '', '', '', self.MenuAction, True],]
                    else:
                        commands = [['Include', '', 'Include', '', '', '', self.MenuAction, True],]
                elif b_include_class and (not b_excluded) and (not b_included):
                    commands = [['Remove', '', 'Remove', '', '', '', self.MenuAction, True],]
                menuBuilder = cd.At('menuBuilder')
                menuBuilder.RegisterCommands(FUxCore.ConvertCommands(commands))
        except:
            pass

    @FUxCore.aux_cb
    def PopulatePackageObjectsTree(self, package_objects):
        try:
            logger.debug('PopulatePackageObjectsTree()...')
            self.UpdateStatus('Popuplating package objects tree...')
            rootItem = self.m_packageObjectsTree.GetRootItem()
            for child in rootItem.Children():
                child.Remove()
            self.m_package_objects = package_objects
            if package_objects == None or len(package_objects) == 0:
                return
            objects = sorted(clean_list(self.m_package_objects), key=DatabaseDependencies.node_id)
            for acm_object in objects:
                treeitem = rootItem.AddChild()
                treeitem.SetData(acm_object)
                treeitem.Label(acm_object.StringKey(), 0)
                treeitem.Label(acm_object.ClassName(), 1)
                treeitem.Label(acm_object.Table().Name(), 2)
                treeitem.Label(acm_object.Oid(), 3)
        except:
            logger.error(traceback.format_exc())
            traceback.print_exc()
        finally:
            self.UpdateStatus('Finished populating package objects tree.')
            logger.debug('PopulatePackageObjectsTree().')

    @FUxCore.aux_cb
    def PopulateObjectList(self, objects, exclusions = None, update_status = None):
        logger.debug('PopulateObjectList()...')
        rootItem = self.m_packageDependenciesTree.GetRootItem()
        self.graph = DatabaseDependencies.PopulateFuxTreeControl(objects, rootItem, exclusions, self.m_exclusion_types, update_status)

    @FUxCore.aux_cb
    def GetPackageObjects(self, package, update_status = None):
        try:
            package_path = package['path']
            logger.debug('package_path: %s %s' % (type(package_path), package_path))        
            package_def = self.m_packageManager.get_repository()._get_package_def(package_path)
            logger.debug('package_def: %s %s' % (type(package_def), package_def))
            for field in package['meta'].Keys():
                value = package['meta'][field]
                logger.debug('field: %s value: %s' % (field, value))
                if field in META_INFO:
                    if field != 'version':
                        self.m_layout.GetControl("%sCtrl" % field).SetData(value)
            complete_version = package['meta']['version']
            logger.debug('complete_version: %s' % str(complete_version))
            if complete_version != None:
                parts = complete_version.split('.')
                self.m_versionCtrl.SetData(parts[0])
                if len(parts) >= 2:
                    self.m_minorVersionCtrl.SetData(parts[1])
                if len(parts) >= 3:
                    self.m_updateNumberCtrl.SetData(parts[2])
            if self.m_package_objects:
                self.m_package_objects.clear()
            else:
                self.m_package_objects = set()
            for key in package_def['objects']:
                key = key.encode('latin-1')
                logger.debug('key: %s' % key)
                acm_object = entity_for_key(key)
                if update_status != None:
                    update_status('Retrieved package object: %s...' % key)
                try:
                    self.m_package_objects.add(acm_object)
                except:
                    pass
            if update_status != None:
                update_status('Finished retrieving package objects.')
            return self.m_package_objects
        except:
            logger.error(traceback.format_exc())

    def GetActionsPerFile(self, package):
        file_actions = []
        package_path = package['path']
        logger.debug('package_path: %s %s' % (type(package_path), package_path))        
        package_def = self.m_packageManager.get_repository()._get_package_def(package_path)
        logger.debug('package_def: %s %s' % (type(package_def), package_def))
        actions = package_def['actions']
        logger.debug('actions: %s %s' % (type(actions), actions))
        for action in actions:    
            logger.debug('GetActionsPerFile(): action: %s' % action)
            action_type = action['type']
            transporter = action.get('transporter', '')
            packages_path = package['path']
            folder = action.get('folder', '')
            if folder != '':
                package_path = os.path.join(packages_path, folder)
            else:
                package_path = packages_path
            pathnames = []
            if folder == '':
                file_path = os.path.join(package_path, action['file'])
                pathnames.append(file_path)
            else:
                files = os.listdir(package_path)
                for each_file in files:
                    file_path = os.path.join(package_path, each_file)
                    if os.path.isfile(file_path):
                        pathnames.append(file_path)
            for file_path in pathnames:
                # May add other extensions to tuple.
                if file_path.endswith(('.bak')):
                    logger.warn('Skipping: %s.' % file_path)
                    continue
                file_action = FileAction(action_type, transporter, file_path, self.UpdateStatus)
                file_actions.append(file_action)
        return file_actions

    '''
    Read the package, get the action, and retrieve the referenced objects -- 
    not from the file system, but from the ADS. Sometimes the action is for a file,
    sometimes it is for a directory that contains any number of files of the same 
    type of object. In this case, we use the actual entity key recorded in the AMBA message
    to get the entity from the ADS instead of creating it with the AMBAMessage namespace.
    '''
    def GetPreviousObjects(self, package):
        logger.debug('GetPreviousObjects()...')
        # Resets package to be used!
        self.m_package = package
        actions_per_file = self.GetActionsPerFile(package)
        for action_per_file in actions_per_file:
            logger.info(action_per_file)
        objects = []
        exclusions = set()
        for action_per_file in actions_per_file:
            try:
                action_per_file.fetch_ADS_objects(objects, True)
                exclusions.update(action_per_file.exclusions)
            except:
                logger.error(traceback.format_exc())
        logger.info('Objects retrieved from ADS for files in package: %d.\n' % len(objects))
        if len(objects) < 1:
            self.ErrorMessage("No objects for package found in ADS.")            
        for acm_object in objects:
            try:
                logger.info('%-20s: %s' % (acm_object.ClassName(), acm_object.StringKey()))
            except:
                logger.error(traceback.format_exc())
        self.m_packageObjects = objects
        logger.debug('GetPreviousObjects().')
        return objects, exclusions

    def AddQueryFolderObject(self, *params):
        self.m_queryFolderContent = True
        if self.m_insertQueryItemsDialog:
            try:
                self.m_insertQueryItemsDialog.Shell()
                self.m_insertQueryItemsDialog.Activate()
                return
            except RuntimeError:
                pass
        self.m_insertQueryItemsDialog = acm.StartFASQLEditor('Add Objects', InsertItemsPanel.GetQueryFolderArray(), None, None, None, '', False, InsertItemsPanel(self))
        logger.debug('%s %s' % (type(self.m_insertQueryItemsDialog), dir(self.m_insertQueryItemsDialog)))

    def AddObject(self, *params):
        self.m_queryFolderContent = False
        if self.m_insertItemsDialog:
            try:
                self.m_insertItemsDialog.Shell()
                self.m_insertItemsDialog.Activate()
                return
            except RuntimeError:
                pass
        self.m_insertItemsDialog = acm.StartFASQLEditor('Add Objects', InsertItemsPanel.GetSortedClassArray(), None, None, None, '', False, InsertItemsPanel(self))
        logger.debug('%s %s' % (type(self.m_insertItemsDialog), dir(self.m_insertItemsDialog)))

    # def AddMarketParams(self,*params):
    #     objects = PackageBuilderGUIAccPanes.StartIIExtendedCB()
    #     self.accelerator_objects = objects
    #     logger.info("This feature is currently not supported.")

    def __get_date(self, date_val):
        original_date_val = date_val
        actual_date = None
        try:
            date_string_input = date_val.upper()
            if date_string_input == 'Y' or date_string_input == 'YESTERDAY':
                actual_date = ael.date_today().add_days(-1)
            elif date_string_input == 'TODAY':
                actual_date = ael.date_today()
            else:
                try:
                    actual_date = ael.date_from_string(date_val)
                except:
                    date_string = date_val.lstrip('-0123456789')
                    days = date_val[:len(date_string) * -1]
                    period_val = None
                    if date_string.upper() not in ['D', 'Y', 'M', 'DAY', 'DAYS', 'MONTH', 'MONTHS', 'YEAR', 'YEARS', 'W', 'WEEK', 'WEEKS']:
                        date_string = date_string[0].upper()
                    if date_string.upper() in ['D', 'DAY', 'DAYS']:
                        period_val = 'd'
                    if date_string.upper() in ['W', 'WEEK', 'WEEKS']:
                        period_val = 'w'
                    if date_string.upper() in ['M', 'MONTH', 'MONTHS']:
                        period_val = 'm'
                    if date_string.upper() in ['Y', 'YEAR', 'YEARS']:
                        period_val = 'y'
                    if period_val:
                        actual_date = ael.date_today().add_period(days + period_val)
                    date_val = days + date_string
            if actual_date:
                actual_date = actual_date.to_string(ael.DATE_ISO)
        except:
            pass
        if actual_date and original_date_val != date_val:
            logger.info('Considering update time from: %s only.'%date_val)
        return actual_date

    def AddUpdatedObjects(self, *params):
        date_time = self.m_updateDateTime.GetData()
        actual_date_time = ''
        try:
            if acm.Time().IsValidDateTime(date_time):
                actual_date_time = date_time
        except:
            actual_date_time = self.__get_date(date_time)
            if not actual_date_time:
                actual_date_time = ''
            else:
                actual_date_time = actual_date_time + ' 12:00:00'
        self.m_updateDateTime.SetData(actual_date_time)
        if actual_date_time:
            logger.debug('Considering update time as: %s'%actual_date_time)
        update_user = self.m_updateUser.GetData()
        user_name = ''
        if update_user:
            user = acm.FUser[update_user.upper()]
            if user:
                user_name = user.Name()
            else:
                logger.warn('User %s does not exist in the ADS'%update_user)
        message = None
        if actual_date_time and user_name:
            message = 'Add objects updated on/after %s by %s.'%(actual_date_time, user_name)
        elif actual_date_time:
            message = 'Add objects updated on/after %s.'%(actual_date_time)
        elif user_name:
            message = 'Add objects updated by %s.'%(user_name)
        self.m_updateUser.SetData(user_name)
        if user_name:
            logger.debug('Considering update User as: %s'%user_name)
        if message:
            process_message = False
            if not self.m_original_message:
                self.m_original_message = message
                process_message = True
            else:
                if self.m_original_message != message:
                    process_message = True
                else:
                    process_message = False
            if process_message:
                user_response = acm.UX().Dialogs().MessageBoxOKCancel(acm.UX().SessionManager().Shell(), 'Question', message)
                if user_response == 'Button1':
                    self.get_all_updated_objects(actual_date_time, user_name)
        else:
            logger.info('Provide valid update datetime/user to get details.')

    def RemoveObject(self):
        logger.debug('RemoveObject()...')
        exclusions = set()
        for each_object in self.m_packageDependenciesTree.GetRootItem().Children():
            exclude = DatabaseDependencies.get_attribute(self.graph, each_object.GetData(), 'exclude', '+')
            if exclude == '-':
                exclusions.add(each_object.GetData())
        try:
            # Only package objects can be removed.
            # The dependency graph is then recomputed.
            selectedItems = self.m_packageObjectsTree.GetSelectedItems()
            if selectedItems:
                for selectedItem in selectedItems:
                    package_object = selectedItem.GetData()
                    try:
                        self.m_package_objects.remove(package_object)
                    except:
                        self.m_package_objects.Remove(package_object)
                self.m_packageDependenciesTree.RemoveAllItems()
                self.PopulatePackageObjectsTree(self.m_package_objects)
                self.PopulateObjectList(self.m_package_objects, exclusions, update_status = None)
            else:
                logger.info('RemoveObject will not work without selecting object.')
        except:
            logger.error(traceback.format_exc())
        finally:
            logger.debug('RemoveObject().')

    def UpdateFuxTreeControlFromGraph_(self, graph, treeitem, update_status):    
        acm_object = treeitem.GetData()
        if not acm_object:
            for eachChild in treeitem.Children():
                acm_object = eachChild.GetData()
                eachChild.Label(acm_object.StringKey(), 0)
                eachChild.Label(acm_object.ClassName(), 1)
                eachChild.Label(acm_object.Table().Name(), 2)
                eachChild.Label(acm_object.Oid(), 3)
                reference = DatabaseDependencies.get_attribute(graph, acm_object, 'reference')
                treeitem.Label(reference, 4)
                exclude = DatabaseDependencies.get_attribute(graph, acm_object, 'exclude', '+')
                eachChild.Label(exclude, 5)
                if exclude == '-':
                    if str(parameters.read('ShowExcludedInDependencyTree')).upper() == 'TRUE':
                        i = 0
                        while i <= 5:#updating all columns
                            eachChild.Style(i, False, \
                            acm.UX().Colors().Create(200, 200, 200).ColorRef(), \
                            acm.UX().Colors().Create(255, 255, 255).ColorRef())
                            i = i + 1
                    else:
                        eachChild.Visible(False)
                for child in eachChild.Children():
                    self.UpdateFuxTreeControlFromGraph_(graph, child, update_status)
    ''' 
    Assuming that the structure of the tree has not changed, update the 
    values displayed in the tree control.
    '''
    def UpdateFuxTreeControlFromGraph(self, graph, update_status = None):
        began_update_fux_tree_control_from_graph = time.clock()
        logger.debug('Began UpdateFuxTreeControlFromGraph()...')
        root = self.m_packageDependenciesTree.GetRootItem()
        for child in root.Children():
            self.UpdateFuxTreeControlFromGraph_(graph, child, update_status)
        ended_update_fux_tree_control_from_graph = time.clock()
        elapsed_update_fux_tree_control_from_graph = ended_update_fux_tree_control_from_graph - began_update_fux_tree_control_from_graph
        logger.debug('Ended UpdateFuxTreeControlFromGraph(%12.4f).' % elapsed_update_fux_tree_control_from_graph)

    def __open_object(self, acm_object, action_param):
        if acm_object:
            if action_param == 'INSPECT':
                acm_object.Inspect()
            else:
                if acm_object.ClassName().AsString() == 'FAdditionalInfo':
                    logger.info('Opening of the object for details is not supported for FAdditionalInfo')
                else:
                    acm.StartApplication('', acm_object)

    def __open_objects(self, selected_objects, action_param):
        acm_object = None
        try:
            log_action = 'Open'
            if action_param == 'INSPECT':
                log_action = 'Properties'
            if selected_objects:
                for selected_object in selected_objects:
                    acm_object = selected_object.GetData()
                    if acm_object:
                        log_msg = '%s object: %s'%(log_action, DatabaseDependencies.node_id(acm_object))
                        logger.debug(log_msg)
                        self.UpdateStatus(log_msg)
                        # TODO: Use FObject.Inspect if no application?
                        self.__open_object(acm_object, action_param)
                    else:
                        logger.info('%s will not work without selecting specific object(s).'%log_action)
            else:
                logger.info('%s will not work without selecting object.'%log_action)
        except:
            logger.error(traceback.format_exc())
            logger.error(str(acm_object))

    def InspectListObject(self, *params):
        self.__open_objects(self.m_packageObjectsTree.GetSelectedItems(), 'INSPECT')

    def OpenListObject(self, *params):
        self.__open_objects(self.m_packageObjectsTree.GetSelectedItems(), 'OPEN')

    def InspectObject(self):
        self.__open_objects(self.m_packageDependenciesTree.GetSelectedItems(), 'INSPECT')

    def OpenObject(self):
        self.__open_objects(self.m_packageDependenciesTree.GetSelectedItems(), 'OPEN')

    def __refresh_graphical_tree(self):
        self.m_packageDependenciesTree.RemoveAllItems()
        self.PopulateObjectList(self.m_package_objects, self.m_exclusions, update_status = None)

    def __remove_item(self, acm_object):
        DatabaseDependencies.difference(self.graph, acm_object, True)
        self.UpdateFuxTreeControlFromGraph(self.graph, True)
        for object in DatabaseDependencies.get_all_nodes(self.graph):
            exclude = DatabaseDependencies.get_attribute(self.graph, object, 'exclude', '+')
            if exclude == '-':
                if object not in self.m_exclusions:
                    self.m_exclusions.Add(object)
        parameters.write('NonDependencies', self.m_exclusions)

    def __include_item(self, acm_object):
        DatabaseDependencies.set_attribute(self.graph, acm_object, 'exclude', '+', True)
        if self.m_exclusions.Includes(acm_object):
            try:
                self.m_exclusions.Remove(acm_object)
            except Exception, e:
                pass
        parameters.write('NonDependencies', self.m_exclusions)

    def IncludeSpecificObject(self, *params):
        selectedItems = self.m_packageDependenciesTree.GetSelectedItems()
        for selectedItem in list(selectedItems):
            try:
                if selectedItem.GetData():
                    self.__include_item(selectedItem.GetData())
                else:
                    self.IncludeAllSpecificObject(params)
            except Exception, e:
                pass
        self.__refresh_graphical_tree()

    def RemoveSpecificObject(self, *params):
        selectedItems = self.m_packageDependenciesTree.GetSelectedItems()
        non_dependencies = parameters.read('NonDependencies')
        if not non_dependencies:
            non_dependencies = []
        for selectedItem in list(selectedItems):
            try:
                if selectedItem.GetData():
                    self.__remove_item(selectedItem.GetData())
                else:
                    self.RemoveAllSpecificObject(params)
            except:
                pass
        parameters.write('NonDependencies', self.m_exclusions)

    def IncludeAllExcludedObjects(self, *params):
        parameters.write('NonDependencies', [])        
        self.m_packageDependenciesTree.RemoveAllItems()
        self.PopulateObjectList(self.m_package_objects)
        self.UpdateFuxTreeControlFromGraph(self.graph)
        self.m_packageObjectsTree.AddDependent(self)

    def IncludeAllSpecificObject(self, *params):
        record_types = []
        selectedItems = self.m_packageDependenciesTree.GetSelectedItems()
        for selectedItem in list(selectedItems):#type: FUxTreeItem
            if selectedItem.GetData():
                record_types.append(selectedItem.GetData().ClassName().AsString())
            else:
                for eachItem in selectedItem.Children():
                    record_types.append(eachItem.GetData().ClassName().AsString())
        tree_elements = self.m_packageDependenciesTree.GetRootItem().Children()
        for each_item in list(tree_elements):
            if each_item.GetData():
                if each_item.GetData().ClassName().AsString() in record_types:
                    self.__include_item(each_item.GetData())
            else:
                for each_object in each_item.Children():
                    if each_object.GetData().ClassName().AsString() in record_types:
                        self.__include_item(each_object.GetData())
        for record_type in record_types:
            if record_type in self.m_exclusion_types:
                self.m_exclusion_types.remove(record_type)
        self.__refresh_graphical_tree()

    def IncludeAllSpecificObject1(self, *params):
        record_types = []
        selectedItems = self.m_packageDependenciesTree.GetSelectedItems()
        for selectedItem in list(selectedItems):#type: FUxTreeItem
            record_types.append(selectedItem.GetData().ClassName().AsString())
        tree_elements = self.m_packageDependenciesTree.GetRootItem().Children()
        for each_item in list(tree_elements):
            if each_item.GetData().ClassName().AsString() in record_types:
                self.__include_item(each_item.GetData())
        self.__refresh_graphical_tree()

    def __get_record_type(self):
        record_types = []
        selectedItems = self.m_packageDependenciesTree.GetSelectedItems()
        for selectedItem in list(selectedItems):#type: FUxTreeItem
            className = None
            if selectedItem.GetData():
                record_types.append(selectedItem.GetData().ClassName().AsString())
            else:
                for eachChild in selectedItem.Children():
                    class_type = eachChild.GetData().ClassName().AsString()
                    record_types.append(class_type)
                    self.m_exclusion_types.add(class_type)
        return record_types

    def remove_all_of_specific_type(self, record_types):
        tree_elements = self.m_packageDependenciesTree.GetRootItem().Children()
        for each_item in list(tree_elements):
            if each_item.GetData():
                if each_item.GetData().ClassName().AsString() in record_types:
                    self.__remove_item(each_item.GetData())
            else:
                if each_item.ClassName().AsString() in record_types:
                    for every_item in each_item.Children():
                        self.__remove_item(every_item.GetData())
        self.__refresh_graphical_tree()        

    def RemoveAllSpecificObject(self, *params):
        record_types = self.__get_record_type()
        self.remove_all_of_specific_type(record_types)

    def ErrorMessage(self, msg):
        acm.UX().Dialogs().MessageBox(self.Shell(), 'Error', msg, 'OK', None, None, 'Button1', 'Button1')

    def __update_exclusion_list(self):
        exclusion_type = set()
        inclusion_type = set()
        for object in DatabaseDependencies.get_all_nodes(self.graph):
            exclude = DatabaseDependencies.get_attribute(self.graph, object, 'exclude', '+')
            if exclude == '-':
                exclusion_type.add(object.ClassName().AsString())
            elif exclude == '+':
                inclusion_type.add(object.ClassName().AsString())
        for each_type in inclusion_type:
            if each_type in list(exclusion_type):
                exclusion_type.remove(each_type)
        self.m_exclusion_types = exclusion_type
        
    def OnRememberExcludedDependencies(self, *params):
        try:
            rememberExcludedDependencies = self.m_rememberExcludedDependencies.Checked()
            logger.debug('RememberExcludedDependencies: %s %s' % (type(rememberExcludedDependencies), rememberExcludedDependencies))
            if rememberExcludedDependencies:
                self.__update_exclusion_list()
            else:
                self.m_exclusion_types.clear()
        except:
            traceback.print_exc()

    def OpenRepositoryDir(self, *params):
        defaultFolder = parameters.read('DefaultFolder')
        name = self.m_layout.GetControl('nameCtrl').GetData()
        print 'Open', "%s\%s"%(defaultFolder, name) if name else defaultFolder
        if name and os.path.exists("%s\%s"%(defaultFolder, name)):
            subprocess.Popen(r'explorer /select,"%s\%s"'%(defaultFolder, name), shell=True)
        elif os.path.exists(defaultFolder):
            subprocess.Popen(r'explorer /n,"%s"'%(defaultFolder), shell=True)
        else:
            print "%s\%s"%(defaultFolder, name) if name else defaultFolder, "does not exist!"
            #self.ErrorMessage("%s\%s does not exist!"%(defaultFolder, name) if name else defaultFolder):

    def BuildPackage(self, *params):
        self.UpdatePackage(local = False, update_status = self.UpdateStatus)

    def UpdatePackage(self, local = False, update_status = None):
        began_update_package = time.clock()
        name = self.m_layout.GetControl('nameCtrl').GetData()
        if name == None or name == '':
            self.ErrorMessage('You have to give the package a name.')
            return
        packageInfo = {}
        for field in META_INFO:
            data = self.m_layout.GetControl("%sCtrl" % field).GetData()
            if data:
                packageInfo[field] = data
        if not self.m_package_objects or len(self.m_package_objects) == 0:
            self.ErrorMessage('You have to select package objects.')
            return        
        major_version = self.m_versionCtrl.GetData()
        minor_version = self.m_minorVersionCtrl.GetData()
        update_number = self.m_packageFileRepository.increment_update_number(packageInfo)
        self.m_updateNumberCtrl.SetData(update_number)
        complete_version = '%s.%s.%s' % (major_version, minor_version, update_number)
        packageInfo['version'] = complete_version
        folder = BuildPackage.BuildPackageFromGraph(self.graph, self.m_package_objects, self.m_exclusions, self.m_exclusion_types, update_status)
        logger.debug('Build package from graph at folder: %s' % folder)
        defaultFolder = str(parameters.read('DefaultFolder'))
        self.m_packageFileRepository.set_folder(defaultFolder)
        if self.m_packageFileRepository.src_folder[:2] == r'\\':
            self.m_packageFileRepository.build_package_index()
        self.m_packageFileRepository.add_package(packageInfo, folder, True)
        self.UpdateStatus('Added package: %s' % packageInfo['name'])
        logger.info('Removing temporary folder: %s.' % folder)
        ended_update_package = time.clock()
        elapsed_update_package = ended_update_package - began_update_package
        logger.info('Ended updating package: %s (%12.f seconds).' % (packageInfo['name'], elapsed_update_package))
        shutil.rmtree(folder)
        self.m_packageObjectsTree.Changed()
        return packageInfo

    def SetDependenciesVisible(self, *args):
        DependenciesVisible = parameters.read('DependenciesVisible') == 'True'
        for object in self.m_dependencies_items:
            object.SetVisible(DependenciesVisible)

    def HandleCreate(self, creation_context):
        layout_builder = self.CreateLayout()
        #if self.modify == False:
        #    self.Frame().Caption('Build Package')
        #else:
        #    self.Frame().Caption('Modify or Update Package')
        self.m_layout = creation_context.AddPane(layout_builder, 'Dependencies')
        self.InitControls()
        self.EnableOnIdleCallback(True)

    def HandleOnIdle(self):
        pass

    def HandleCancel(self):
        self.m_insertItemsDialog and self.m_insertItemsDialog.Close()
        return True

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginHorzBox('None')
        b.    BeginVertBox('None')
        b.      AddInput('nameCtrl', 'Name')
        b.      AddInput('contactCtrl', 'Contact')
        b.      AddInput('tagCtrl', 'Tags')
        b.    EndBox()
        b.    AddSpace(5)
        b.    BeginVertBox('None')
        b.      BeginHorzBox('None')
        b.        AddInput('versionCtrl', 'Major version')
        b.        AddInput('minorVersionCtrl', 'Minor version')
        b.        AddInput('updateNumberCtrl', 'Update')
        b.      EndBox()
        b.      AddComboBox('categoryCtrl', 'Category')
        b.      AddComboBox('statusCtrl', 'Status')
        b.    EndBox()
        b.  EndBox()
        b.  AddInput('descriptionCtrl', 'Description', 120)
        b.  AddSpace(5)
        b.  BeginHorzBox('None', '', 'packageObjectsBox')
        b.    BeginVertBox('EtchedIn', 'Selected Objects (all objects selected for package)', 'packageObjectsTreeBox')
        b.      AddTree('packageObjectsTree', 460, 400, -1, -1)
        b.      AddSpace(5)
        b.      BeginHorzBox('None', '', 'packageObjectsButtonsBox')
        b.        AddButton('addObjectBtn', 'Add...')
        b.        AddButton('addQueryFolderBtn', 'Add Query Folder contents', False, True)
        #b.        AddButton('addMarketParams', 'Accelerator...')
        #b.        AddButton('removeObjectBtn', 'Remove')
        #b.        AddButton('inspectPackageObjectBtn', 'Properties...')
        #b.        AddButton('openPackageObjectBtn', 'Open...')
        b.      EndBox()
        b.      AddSpace(5)
        b.      BeginHorzBox('None', '', 'packageObjectsButtonsBox1')

        b.        AddInput('updateDateTime', 'Export object beyond Update DateTime >')
        b.        AddInput('updateUser', 'By User')
        b.        AddButton('addUpdatedObjects', 'Add Updated...')        
        b.      EndBox()
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'All dependencies of Selected Objects (objects without dependencies are roots of their trees)', 'packageDependenciesBox')
        b.      AddTree("packageDependenciesTree", 620, 400, -1, -1)
        b.      AddSpace(5)
        b.      BeginHorzBox('None', '', 'inspectObjectBox')
        #b.        AddButton('inspectObjectBtn', 'Properties...')
        #b.        AddButton('openObjectBtn', 'Open...')
        b.        AddCheckbox('rememberExcludedDependencies', 'Remember excluded dependency classes for all additions')
        b.      EndBox()
        b.    EndBox()
        b.  EndBox()
        b.  AddSpace(5)
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('openRepoBtn', 'Open repository')
        if self.modify == False:
            b.    AddButton('createBtn', 'Create Package')
        else:
            b.    AddButton('createBtn', 'Update Package')
            b.    AddButton('diffBtn', 'Diff with Package')
            b.    AddButton('diffTargetBtn', 'Diff with Target')
        b.    AddButton('closeBtn', 'Close')
        b.  EndBox()
        b.EndBox()
        return b

    def FindEntityInDependencies(self, *params):
        logger.debug('FindEntityInDependencies...')
        selected_item = self.m_packageObjectsTree.GetSelectedItem()
        dependencies_root = self.m_packageDependenciesTree.GetRootItem()        
        find_entity(dependencies_root, selected_item.GetData())

    def ExpandDependencies(self, *params):
        logger.debug('ExpandDependencies...')
        treeitem = self.m_packageDependenciesTree.GetSelectedItem()
        DatabaseDependencies.ExpandFuxTreeNode(self.graph, treeitem)

    def DiffTarget(self, *params):
        try:
            saveParameters = True
            #loginDlg = TargetLoginDialog(self.m_packageManager.parameters)
            
            AdsComparator.compare_ads_entities(self.m_packageObjects, parameters.read('TargetServer'), parameters.read('TargetUser'), parameters.read('TargetPassword'))
        except:
            logger.error(traceback.format_exc())

    def DiffPackage(self, *params):
        try:
            package = self.UpdatePackage(local = True, update_status = self.UpdateStatus)
            packageName = package['name'].replace(' ', '')
            remoteRepository = str(parameters.read('DefaultFolder'))
            remotePackagePath = os.path.join(remoteRepository, packageName)
            localRepository = str(parameters.read('DefaultFolderLocal'))
            localPackagePath = os.path.join(localRepository, packageName)
            template = str(parameters.read('MergeToolCommandTemplate'))
            command = template % (localPackagePath, remotePackagePath)
            logger.info('Diff command: %s' % command)
            self.UpdateStatus('Running diff command: %s' % command)
            subprocess.Popen(command)
        except:
            logger.error(traceback.format_exc())

    def UpdatePackageObjectsTree(self):
        try:
            rootItem = self.m_packageObjectsTree.GetRootItem()
            for child in rootItem.Children():
                child.Remove()
            objects = sorted(self.m_package_objects, key=DatabaseDependencies.node_id)
            for object in objects:
                treeitem = rootItem.AddChild()
                treeitem.SetData(object)
                treeitem.Label(object.StringKey(), 0)
                treeitem.Label(object.ClassName(), 1)
                treeitem.Label(object.Table().Name(), 2)
                treeitem.Label(object.Oid(), 3)
        except:
            logger.error(traceback.print_exc())    

    def HandleRegisterCommands(self, builder):
        openPackageWindowCmd = Menu.OpenPanelCommandsHandler(self, 'Package', onSelectPackage).Instance
        ListOfSupportedCommands = [
        ['NewPackage', 'File', 'New/Package',          'New Package window', 'Ctrl+N',  'N', openPackageWindowCmd, True ],
        ['OpenPackage', 'File', 'Open/Package',          'Opens Package window', 'Ctrl+P',  'P', openPackageWindowCmd, True ],
        ['UnZipOpenPackage', 'File', 'Unzip & Open/Package',          'Unzips and Opens Package window', 'Ctrl+P',  'P', openPackageWindowCmd, True ],
        ['SaveAsPackage', 'File', 'SaveAs/Package',          'Save As Package window', 'Ctrl+Alt+S',  'S', openPackageWindowCmd, True ],
        ['DeletePackage', 'File', 'Delete/Package',          'Delete Package', 'Ctrl+D',  'D', openPackageWindowCmd, True ],]
        fileCommands = acm.FSet()
        fileCommands.Add('FileNew')
        fileCommands.Add('FileOpen')
        fileCommands.Add('FileOpenAdvanced')
        fileCommands.Add('FileSaveAs')
        fileCommands.Add('FileDelete')
        builder.RegisterCommands(FUxCore.ConvertCommands(ListOfSupportedCommands), fileCommands)

    def OnFileUnzipOpen(self):
        OldDefaultFolder = parameters.read('DefaultFolder')
        fileSelection = acm.FFileSelection()
        #fileSelection.PickDirectory(True)
        fileSelection.SelectedDirectory = OldDefaultFolder
        fileSelection.FileFilter = ('ZIP Files (*.zip)|*.zip',)
        result =  acm.UX().Dialogs().BrowseForFile(acm.UX().SessionManager().Shell(), fileSelection)
        if result:
            fileName = self.m_packageFileRepository.get_file_name(str(fileSelection))
            self.m_layout.GetControl('nameCtrl').SetData(fileName)
            NewDefaultFolder = str(fileSelection)
            logger.debug('OldDefaultFolder: %s  NewDefaultFolder: %s' % (OldDefaultFolder, NewDefaultFolder))
            unzipFolder = self.m_packageFileRepository.unzip_folder_content(NewDefaultFolder)
            NewDefaultFolder = unzipFolder+"//"+str(unzipFolder).split('\\')[-1]
            package = self.m_packageFileRepository.get_meta_data(NewDefaultFolder)
            if not package:
                self.InitialiseValues()
                return
            meta_package = acm.FVariantDictionary()
            for each_key in package:
                meta_package[each_key] = package[each_key]
            total_package = acm.FVariantDictionary()
            total_package['meta'] = meta_package
            total_package['path'] = NewDefaultFolder
            #self.m_package_objects = self.m_packageFileRepository.add_package_to_index(NewDefaultFolder, total_package)
            package_objects = self.GetPackageObjects(total_package, update_status = self.UpdateStatus)
            self.PopulatePackageObjectsTree(package_objects)#This populates the left panel
            previousObjects, exclusions = self.GetPreviousObjects(total_package)
            if len(previousObjects) < 1:
                raise Exception("Package must contain at least one object.")
            self.m_packageDependenciesTree.RemoveAllItems()
            self.PopulateObjectList(previousObjects)#This populates the right panel
            #logger.debug('Marking objects to be excluded from import...')
            self.m_packageFileRepository.delete_folder(NewDefaultFolder)
            for excluded_object in exclusions:
                DatabaseDependencies.difference(self.graph, excluded_object, True)
            self.UpdateFuxTreeControlFromGraph(self.graph)
            self.m_packageObjectsTree.AddDependent(self)

    def OnFileOpen(self):
        OldDefaultFolder = parameters.read('DefaultFolder')
        fileSelection = acm.FFileSelection()
        fileSelection.PickDirectory(True)
        fileSelection.SelectedDirectory = OldDefaultFolder
        result =  acm.UX().Dialogs().BrowseForFile(acm.UX().SessionManager().Shell(), fileSelection)
        if result:
            fileName = self.m_packageFileRepository.get_file_name(str(fileSelection))
            self.m_layout.GetControl('nameCtrl').SetData(fileName)
            NewDefaultFolder = str(fileSelection)
            logger.debug('OldDefaultFolder: %s  NewDefaultFolder: %s' % (OldDefaultFolder, NewDefaultFolder))
            package = self.m_packageFileRepository.get_meta_data(NewDefaultFolder)
            if not package:
                self.InitialiseValues()
                return
            meta_package = acm.FVariantDictionary()
            for each_key in package:
                meta_package[each_key] = package[each_key]
            total_package = acm.FVariantDictionary()
            total_package['meta'] = meta_package
            total_package['path'] = NewDefaultFolder
            #self.m_package_objects = self.m_packageFileRepository.add_package_to_index(NewDefaultFolder, total_package)
            package_objects = self.GetPackageObjects(total_package, update_status = self.UpdateStatus)
            self.PopulatePackageObjectsTree(package_objects)#This populates the left panel
            previousObjects, exclusions = self.GetPreviousObjects(total_package)
            if len(previousObjects) < 1:
                raise Exception("Package must contain at least one object.")
            self.m_packageDependenciesTree.RemoveAllItems()
            self.PopulateObjectList(previousObjects)#This populates the right panel
            logger.debug('Marking objects to be excluded from import...')
            for excluded_object in exclusions:
                DatabaseDependencies.difference(self.graph, excluded_object, True)
            self.UpdateFuxTreeControlFromGraph(self.graph)
            logger.info('Adding all constituents into the object Tree')
            self.m_packageObjectsTree.AddDependent(self)
            self.m_exclusions.Clear()
            for object in DatabaseDependencies.get_all_nodes(self.graph):
                exclude = DatabaseDependencies.get_attribute(self.graph, object, 'exclude', '+')
                if exclude == '-':
                    if object not in self.m_exclusions:
                        self.m_exclusions.Add(object)
            self.__update_exclusion_list()
            if self.m_exclusion_types:
                self.m_rememberExcludedDependencies.Checked(True)

    def OnFileNew(self):
        self.InitialiseValues()
        self.m_packageDependenciesTree.RemoveAllItems()#left child panel
        self.m_packageObjectsTree.RemoveAllItems()#right parent panel
        self.m_package_objects = set()
        self.graph = None
        self.InitControls()

    def validateCB(self, *args):
        return True

    def OnFileSaveAs(self):
        res = acm.UX().Dialogs().SaveObjectAs(acm.UX().SessionManager().Shell(), 'Save Package as', '', '', None, self.validateCB, None)
        if res:
            self.m_layout.GetControl('nameCtrl').SetData(res)
            self.UpdatePackage(local = False, update_status = self.UpdateStatus)

    def OnFileDelete(self):
        if self.m_packageFileRepository.src_folder and self.m_layout.GetControl('nameCtrl').GetData():
            action_status = acm.UX().Dialogs().MessageBoxYesNo(self.Shell(), 'Information', 'Do you really want to delete package %s?'%self.m_layout.GetControl('nameCtrl').GetData())
            if action_status == 'Button1':
                folder_name = os.path.join(self.m_packageFileRepository.src_folder, self.m_layout.GetControl('nameCtrl').GetData())
                if os.path.exists(folder_name):
                    logger.debug('Deleting package %s....'%folder_name)
                    self.m_packageFileRepository.delete_folder(folder_name)
                self.OnFileNew()
        else:
            logger.info('Select a valid package to be deleted.')

    def HandleStandardFileCommandInvoke(self, commandName):
        if commandName == 'FileOpen':
            self.OnFileOpen()
        if commandName == 'FileOpenAdvanced':
            self.OnFileUnzipOpen()
        if commandName == 'FileNew':
            self.OnFileNew()
        if commandName == 'FileSaveAs':
            self.OnFileSaveAs()
        if commandName == 'FileDelete':
            self.OnFileDelete()

    def PopulateValues(self):
        logger.debug('PopulateValues()...')
        self.UpdateStatus('Populating packages... please wait...')
        self.PopulatePackageList(True)
        self.UpdateStatus('Finished populating packages.')
        logger.debug('PopulateValues().')

    def UpdateStatus_(self, text):
        self.m_statusBarTextPane.SetText(text)    

    def UpdateStatus(self, text):
        acm.SynchronizedCall(self.UpdateStatus_, [text])

    @FUxCore.aux_cb
    def PopulatePackageList(self, getPackages = False):
        began_populate_package_list = time.clock()
        logger.debug('Began PopulatePackageList(%s)...' % (getPackages))
        if getPackages == True:
            self.m_packages = self.m_packageManager.get_all_packages(False, True, self.UpdateStatus)
        rootItem = self.m_packageListCtrl.GetRootItem()
        for child in rootItem.Children().AsList():
            child.Remove()
        for package in sorted(self.m_packages.values(), cmp=lambda x, y: cmp(x.lower(), y.lower()), key=methodcaller('get', 'name', 'zzzzzzzzzz')):
            logger.debug('package: %s %s' % (type(package), package))
            package.setdefault('selected_version', package['latest_version'])
            metaData = package['versions'][package['latest_version']]['meta']
            if filter:
                for v in (metaData.values() if not filterOption else [metaData.get(filterOption, '')]):
                    if filter in (v if caseSensitive else v.upper()):
                        break
                else:
                    continue
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
    
    def get_all_updated_objects(self, from_date_time_val = None, user = None):
        acm_object_types = InsertItemsPanel.AddSubClasses()
        ignore_object_types = parameters.read('AlwaysIgnoreObjectTypes')
        updated_objects = []
        updated_object_types = []
        if from_date_time_val and user:
            utc_from_date_time_val = acm.Time.LocalToUtc(from_date_time_val)
            for each_acm_type in acm_object_types:
                try:
                    objects = []
                    if each_acm_type.Name().AsString() not in ignore_object_types:
                        update_user_query_part = " and updateUser = '" + user + "'"
                        query = 'acm.' + str(each_acm_type.Name().AsString()) + '.Select("' + "updateTime > '" + utc_from_date_time_val + "'" + update_user_query_part + '")'
                        objects = eval(query)
                        if objects:
                            updated_objects.extend(objects)
                except Exception, e:
                    pass
        elif from_date_time_val:
            utc_from_date_time_val = acm.Time.LocalToUtc(from_date_time_val)
            for each_acm_type in acm_object_types:
                try:
                    objects = []
                    if each_acm_type.Name().AsString() not in ignore_object_types:
                        objects = eval('acm.' + str(each_acm_type.Name().AsString()) + ".Select('updateTime > " + utc_from_date_time_val + "')")
                        if objects:
                            updated_objects.extend(objects)
                except Exception, e:
                    pass
        elif user:
            update_user_query_part = "updateUser = '" + user + "'"
            for each_acm_type in acm_object_types:
                try:
                    objects = []
                    if each_acm_type.Name().AsString() not in ignore_object_types:
                        objects = eval('acm.' + str(each_acm_type.Name().AsString()) + ".Select(" + update_user_query_part + ")")
                        if objects:
                            updated_objects.extend(objects)
                except Exception, e:
                    pass
        
        updated_objects = set(updated_objects)
        try:
            self.m_package_objects = self.m_package_objects.union(updated_objects)
        except:#this code gets called if you are extending an existing Package
            try:
                for object in updated_objects[0]:
                    self.m_package_objects.Add(object)
            except:
                pass

        self.UpdatePackageObjectsTree()
        rootItem = self.m_packageDependenciesTree.GetRootItem()
        for child in rootItem.Children():
            child.Remove()
        self.graph = DatabaseDependencies.PopulateFuxTreeControl(DatabaseDependencies.clean_list(self.m_package_objects), rootItem, self.m_exclusions, self.m_exclusion_types, update_status = self.UpdateStatus)

class InsertItemsPanel (FUxCore.LayoutPanel):

    def __init__(self, buildPackageDialog = None):
        self.m_buildPackageDialog = buildPackageDialog

    def UpdateControls(self):
        self.selection = self.Owner().Selection()
        self.m_selectedCount.SetData(self.selection.Size())
        self.m_addObjectsBtn.Enabled(self.selection.Size() > 0)

    def ServerUpdate(self, sender, aspect, parameter ):
        if str(aspect) == 'SelectionChanged':
            self.UpdateControls()

    def HandleCreate(self):
        layout = self.SetLayout(self.BuildLayout())
        self.m_addObjectsBtn = layout.GetControl('addObjectsBtn')
        self.m_addObjectsBtn.AddCallback( "Activate", self.OnAddObjectsClicked, None)
        self.m_selectedCount = layout.GetControl('selectedCount')
        self.m_selectedCount.Editable(False)
        self.Owner().AddDependent(self)
        self.UpdateControls()

    def HandleDestroy(self):
        self.Owner().RemoveDependent(self)

    def BuildLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('EtchedIn', '')
        b.  AddInput('selectedCount', 'Selected items', 5, 6)
        b.  AddFill()
        b.  AddButton('addObjectsBtn', 'Add Objects')
        b.EndBox()
        return b

    def OnAddObjectsClicked(self, *params):
        DatabaseDependencies.AddObjectsToPackage(self, self.selection)

    @staticmethod
    def GetSortedClassArray():
        arr = InsertItemsPanel.AddSubClasses(acm.FCommonObject, acm.FArray())
        arr.SortByProperty('StringKey', True)
        return arr

    @staticmethod
    def GetQueryFolderArray():
        arr = acm.FArray()
        arr.Add(acm.FStoredASQLQuery)
        arr.SortByProperty('StringKey', True)
        return arr

    @staticmethod
    def AddSubClasses(cls = acm.FCommonObject, arr = acm.FArray()):
        """ Only Add classes which is not "owned" by another class 
            e.g. YieldCurve -> YieldCurvePoint, only YieldCurve added
        """
        for subClass in cls.Subclasses():
            arr.Add(subClass)
            InsertItemsPanel.AddSubClasses(subClass, arr)
        return arr

def Run(eii = None):
    acm.UX().SessionManager().StartApplication('Package Builder', None).Activate()

