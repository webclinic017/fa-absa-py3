"""
Package Manager - Install and manage packages
"""
import acm
import DatabaseDependenciesNetworkX as DatabaseDependencies
from datetime import datetime
import FLogger
import os
import PackageFileRepository
import PackageInstallerParametersManager
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import xml.etree.ElementTree
from xml.etree import cElementTree
import zipfile
debug = True
parameters = PackageInstallerParametersManager.ParametersManager()
verbosity = int(parameters.read('message_verbosity'))
amba_message_datetime_format = parameters.read('AmbaMessageDatetimeFormat')
logger = FLogger.FLogger(name=__name__, level=verbosity)

"""
try:
    import PackageInstallerReferences
except ImportError:
    try:
        import PackageInstallerReferencesTemplate as PackageInstallerReferences
    except:
        logger.error(traceback.format_exc())
"""
PackageInstallerReferences = DatabaseDependencies.PackageInstallerReferences

def size_of_fileobj(f):
    f.seek(0, os.SEEK_END) 
    res = f.tell() 
    f.seek(0) 
    return res
    
def recursivly_create_directory(dirname):
    # TODO there are nicer ways of doing this without exception handling
    try:
        os.makedirs(dirname)
    except Exception, err:
        if "Error 183" in str(err):
            pass
        else:
            raise

def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)
        
def install_action(type_name):
    """Decorator for registrign new isntaller actions"""
    def _install(handler_func):
        PackageManager.install_actions[type_name] = handler_func
        return handler_func
    return _install
    
def message_older_than_object(message, fobject):
    message_time = ''
    message_times = list(message.getiterator('UPDAT_TIME'))
    if message_times != None:
        if len(message_times) > 0:
            message_time = message_times[0].text
    logger.debug('message_time: %s %s' % (type(message_time), message_time))
    #message_time = datetime.strptime(message_time, '%Y-%m-%d %I:%M:%S %p %Z')
    message_time = datetime.strptime(message_time, amba_message_datetime_format)
    fobject_time = fobject.UpdateTime()
    fobject_time = acm.Time().DateTimeFromTime(fobject_time)
    fobject_time_utc = acm.Time().LocalToUtc(fobject_time)
    fobject_time_utc = datetime.strptime(fobject_time_utc, '%Y-%m-%d %H:%M:%S')
    result_text = ''
    if message_time < fobject_time_utc:
        result = True
        result_text = 'message is older than object'
    elif message_time > fobject_time_utc:
        result = False    
        result_text = 'object is older than message'
    else:
        result = False
    logger.debug('fobject updated: %s %s' % (fobject_time_utc, DatabaseDependencies.node_id(fobject)))
    logger.debug('message updated: %s %s' % (message_time, result_text))
    
    return result
'''
Handles fetching, installing and uninstalling packages from within PRIME.
'''
class PackageManager(object):
    install_actions = {}  # {typename : handler}   
    def __init__(self, localRepository = None, repository = None, context = acm.GetDefaultContext(), update_status = None):
        self.context = context
        self.package_repository = PackageFileRepository.PackageFileRepository(parameters.read('DefaultFolder'), False)
        self.update_status = update_status

    def get_repository(self, useLocal = False):
        """Return the used package repository"""
        return self.package_repository

    def get_all_packages(self, getFromLocal = False, rebuildIndex = False, update_status = None):
        return self.get_repository(getFromLocal).get_all_packages(rebuildIndex, update_status)

    def install_package(self, package_name, version, installFromLocal = False):
        """Download and install package"""
        began_installing_package = time.clock()
        logger.info("Installing package: %s." % package_name)
        package_dir = self._download_package(package_name, version)
        logger.debug("package_dir: %s." % package_dir)
        self.NoOverWriteExistingEntities = parameters.read('NoOverWriteExistingEntities') == 'True'
        logger.debug("NoOverWriteExistingEntities: %s." % self.NoOverWriteExistingEntities)
        self.NoOverWriteNewerEntities = parameters.read('NoOverWriteNewerEntities') == 'True'
        logger.debug("NoOverWriteNewerEntities: %s." % self.NoOverWriteNewerEntities)
        logger.debug("TestMode: %s." % self.TestMode)
        self._run_package_install_actions_from_directory(package_dir)
        if debug == True:
            logger.info("Downloaded files saved in: %s." % package_dir)
        else:
            logger.info("Removing downloaded files in: %s." % package_dir)
            shutil.rmtree(package_dir)
        ended_installing_package = time.clock()
        elapsed_installing_package = ended_installing_package - began_installing_package
        logger.info('Ended installing package: %s (%12.4s seconds).' % (package_name, elapsed_installing_package))

    def run_test_code(self, package_name):
        """Run automatic tests for already installed package"""
        raise NotImplementedError    

    def get_installed_packages(self):
        """Get information about installed packages

        return [{'name', pck name, 'version', version}]
        """
        raise NotImplementedError   

    def install_context(self):
        """Return context to be used for installations"""
        return acm.GetDefaultContext()

    def _get_package(self, package_name, version, getFromLocal = False):
        return self.package_repository.get_package(package_name, version)

    def _download_package(self, package_name, version, folder = tempfile.mkdtemp()):
        """Download package and return directory"""
        package = self._get_package(package_name, version) 
        repository_path = package['path']    
        logger.info('Package version: "%s" repository path: "%s"' % (version, repository_path))
        pack_zip = PackageFileRepository.zip_archive(repository_path)
        logger.info("Downloaded package. Size = %s." % size_of_fileobj(pack_zip))
        zip_file = zipfile.ZipFile(pack_zip)
        logger.info("Unpacking to: %s." % folder)
        zip_file.extractall(folder)
        return folder

    def _run_package_install_actions_from_directory(self, path):
        """Install package from directory"""
        package_def = self.get_repository()._get_package_def(path)
        if not package_def:
            return
        if not 'actions' in package_def:
            logger.error("'actions' are not defined in the definition file %s in %s. Nothing will be installed." % (package_def, path))
            return
        for action in package_def['actions']:
            self._run_action(path, action)

    def _run_action(self, path, action):
        """Execute one installer action"""
        type_name = action["type"]
        handler = PackageManager.install_actions.get(type_name, None)
        if not handler:
            logger.error("Error, action %s not found." % type_name)
            return # Should be a raised error once done
        handler(path, action, self)

@install_action("addextmod")
def AddExtensionModuleToContext(path, action, package_manager):
    context = package_manager.install_context()
    try:
        module = str(action['module'])
        modules = list(context.ModuleNames())
        if module in modules:
            logger.error("Extension module '%s' already in context '%s'." % (module, context.Name()))
            return False
        removeModules = [modules.pop()]
        for mod in reversed(modules):
            if mod[0] == '%':
                removeModules.insert(0, mod)
            else:
                break
        for mod in removeModules:
            context.RemoveModule(mod)
        context.AddModule(module)
        for mod in removeModules:
            context.AddModule(mod)
    except Exception, e:
        logger.error("Failed to load module '%s'.\n%s" % (module, traceback.format_exc()))
        context.Undo()
        raise
    if package_manager.TestMode == False:
        context.Commit()
    return True

def entity_for_key(key):
    class_name = key.split('[')[0]
    oid = key.split('[')[1].split(']')[0]
    code = 'acm.%s[%s]' % (class_name, oid)
    object = eval(code)    
    return object
    
def commit_with_amba_namespace(pathname, package_manager):
    text = open(pathname, 'r').read()
    root = xml.etree.ElementTree.fromstring(text)
    message = None
    for element in root.findall('MESSAGE'):
        try:
            exclude = False
            exclude_element = element.find('EXCLUDE_FROM_IMPORT')
            if str(parameters.read('NoOverWriteExistingEntities')) == 'True':
                original_key = element.find('ORIGINAL_KEY')
                entity_for_original_key = entity_for_key(original_key.text)
                if entity_for_original_key != None:
                    logger.info('%s already exists, not overwriting...' % original_key.text)
                    continue
            if exclude_element:
                if exclude_element.text == '1':
                    exclude == True
            if exclude: 
                logger.info('Marked for exclusion, not overwriting...')
                continue
            else:
                message = xml.etree.ElementTree.tostring(element, encoding = 'latin-1')
                age = None
                object = acm.AMBAMessage().CreateCloneFromMessage(message)
                if object == None:
                    object = acm.AMBAMessage().CreateObjectFromMessage(message)
                    if object == None:
                        logger.error('Failed to retrieve object for:\n%s.' % message)
                        continue
                    else:
                        age = 'new'
                else:
                    age = 'existing'
                logger.info('Retrieved %s object: %s' % (age, DatabaseDependencies.node_id(object)))
                if PackageInstallerReferences.should_import_link_record(object):
                    do_commit = True
                    if str(parameters.read('NoOverWriteNewerEntities')) == 'True':
                        if message_older_than_object(element, object) == True:
                            do_commit = False
                            logger.info('ADS object %s is newer than message, not overwriting.' % DatabaseDependencies.node_id(object))
                    if do_commit == True:
                        if package_manager.TestMode == False:
                            object.Commit()
                            logger.info('Committed %s.' % DatabaseDependencies.node_id(object))
                        else:
                            logger.info('Test commit %s.' % DatabaseDependencies.node_id(object))
                else:
                    logger.info('Skipping import of redundant message for %s.' % DatabaseDependencies.node_id(object))
        except:
            logger.error('Failed to commit object for:\n%s.' % message)
            logger.error(traceback.format_exc())
            
def subprocess_printlog(command, shell=False):
    logger.debug('AMBA command: %s' % command)
    sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    out, err = sp.communicate()
    if out:
        logger.info("Standard output of subprocess:")
        logger.info(out)
    if err:
        logger.info("Standard error of subprocess:")
        logger.info(err)
    logger.debug("returncode of subprocess: %s" % sp.returncode)        

@install_action("ambamsg")
def action_ambamsg(path, action, package_manager):
    testmode = ''
    if package_manager.TestMode:
        testmode = '-db_writes_off=1'
    folder = os.path.join(path, action.get('folder', ''))
    for fileName in [action['file']] if 'file' in action else sorted(os.listdir(folder)):
        logger.info("Installing amba message from file: %s." % fileName)
        logger.info("test_mode: %s." % testmode)
        #fail_file = os.path.join(path, fileName + '.fail')
        #log_file = os.path.join(path, fileName + '.log')
        file = os.path.join(folder, fileName)
        commit_with_amba_namespace(file, package_manager)
        
@install_action("transporter")
def action_transporter(path, action, package_manager):
    """Installer action for importing using the transporter"""
    import Transporters
    handler = Transporters.Transporter.all_handlers[action['transporter']]
    if 'folder' in action:
        path = os.path.join(path, str(action['folder']))
    for file in [str(action['file'])] if 'file' in action else os.listdir(path):
        #Updated needed to transporter to return object
        name = file.rsplit('.', 1)[0].split('@')[0]
        with open(os.path.join(path, file)) as f:
            input = f.read()
        try:
            params = {}
            params['SplitModules'] = False
            object = handler.ImportSingle(params, name, input)
        except:
            logger.error('Action: %s import failed.\n%s' %  (action['transporter'], traceback.format_exc()))
            continue

        if str(action['transporter']) == 'Workbook' and eval(action.get('setDefaultContext', 'False')):
            if not object:
                logger.warn("No workbook returned from transporter, can't set column context.")
                continue
            contextName = package_manager.install_context().Name()
            logger.info('Setting column context in workbook %s to %s' % (name, contextName))
            for sheet in object.Sheets():
                xml = sheet.FromArchiveAsString()
                sheet_xml = cElementTree.fromstring(xml)
                for node in sheet_xml.findall('.//FColumnCreators'):
                    for context_node in node.findall('.//contextSym'):
                        context_node.find("./FSymbol/Text/string").text = contextName
                sheet.Text('%s\n%s' % (xml[:xml.find('\n')], cElementTree.tostring(sheet_xml)))
                if package_manager.TestMode == False:
                    sheet.Commit()

        if str(action['transporter']) == 'Extension Module':
            if not object:
                logger.warn("No module returned from transporter, can't add to default context.")
                continue
            if AddExtensionModuleToContext('', {'module':object.Name()}, package_manager):
                logger.info("Installed module '%s' in context '%s'" % (object.Name(), package_manager.install_context().Name()))

@install_action("extmod")
def action_extmod(path, action, package_manager):
    action['transporter'] = 'Extension Module'
    action_transporter(path, action, package_manager)

@install_action("workbook")
def action_workbook(path, action, package_manager):
    action['transporter'] = 'Workbook'
    action_transporter(path, action, package_manager)

@install_action("python")
def run_python(path, action, package_manager):
    if 'file' in action:
        if 'folder' in action:
            path = os.path.join(path, action['folder'])
        sys.path.insert(0, path)
        try:
            exec 'import %s' % action['file']
            exec 'reload(%s)' % action['file']
        except ImportError:
            logger.error("Failed to import: %s.\n%s" % (action['file'], traceback.format_exc()))
        except:
            logger.error('Error when importing: %s.\n%s.' % (action['file'], traceback.format_exc()))
    try:
        if package_manager.TestMode == False:
            exec action['command']
    except:
        logger.error("Error when executing command '%s'.\n%s" % (action['command'], traceback.format_exc()))
    if 'file' in action:
        sys.path.remove(path)

@install_action("file")
def action_filecopy(path, action, package_manager):
    """Installer action for just copying a file, .dll, directory etc"""
    logger.info("Installing file action:%s." % action)
    target_dir = package_manager.get_repository()    
    if 'folder' in action:
        path = os.path.join(path, action['folder'])
        target_dir = os.path.join(target_dir, action['folder'])
    recursivly_create_directory(target_dir)
    for fileName in [action['file']] if 'file' in action else sorted(os.listdir(path)):        
        full_name = os.path.join(path, fileName)
        target_name = os.path.join(target_dir, fileName)
        logger.info(' : %s -> %s.' % (full_name, target_name))
        #shutil.copyfile(full_name, target_name )
        recursive_overwrite(full_name, target_name)

def _get_latest_filename(path):
    import glob
    class NoFileFoundError(Exception):
        pass

    files = filter(os.path.isfile, glob.glob(path))
    files.sort(key=lambda x: os.path.getmtime(x))

    if len(files) == 0:
        raise NoFileFoundError(path)

    return files[-1]

def check_msi(path, fileName):
    """Check action msi files"""
    # This scripts allows to get a list of all installed products in a windows
    # machine. The code uses ctypes becuase there were a number of issues when
    # trying to achieve the same with win32com.client
    from collections import namedtuple
    from ctypes import byref, create_unicode_buffer, windll
    from ctypes.wintypes import DWORD
    from itertools import count
    import msilib
     
    # defined at http://msdn.microsoft.com/en-us/library/aa370101(v=VS.85).aspx
    UID_BUFFER_SIZE = 39
    PROPERTY_BUFFER_SIZE = 256 
    ERROR_MORE_DATA = 234
    #ERROR_INVALID_PARAMETER = 87
    ERROR_SUCCESS = 0
    ERROR_NO_MORE_ITEMS = 259 
    #ERROR_UNKNOWN_PRODUCT = 1605 
     
    # diff propoerties of a product, not all products have all properties
    PRODUCT_PROPERTIES = [u'Language', u'ProductName', u'PackageCode', u'Transforms', u'AssignmentType',
                          u'PackageName', u'InstalledProductName', u'VersionString', u'RegCompany',
                          u'RegOwner', u'ProductID', u'ProductIcon', u'InstallLocation', u'InstallSource',
                          u'InstallDate', u'Publisher', u'LocalPackage', u'HelpLink', u'HelpTelephone',
                          u'URLInfoAbout', u'URLUpdateInfo',] 
     
    # class to be used for python users :)
    Product = namedtuple('Product', PRODUCT_PROPERTIES)

    def get_property_for_product(product, property, buf_size=PROPERTY_BUFFER_SIZE):
        """Retruns the value of a fiven property from a product."""
        property_buffer = create_unicode_buffer(buf_size)
        size = DWORD(buf_size)
        result = windll.msi.MsiGetProductInfoW(product, property, property_buffer,
                                               byref(size))
        if result == ERROR_MORE_DATA:
            return get_property_for_product(product, property,
                    2 * buf_size)
        elif result == ERROR_SUCCESS:
            return property_buffer.value
        else:
            return None
     
    def populate_product(uid):
        """Return a Product with the different present data."""
        properties = []
        for property in PRODUCT_PROPERTIES:
            properties.append(get_property_for_product(uid, property))
        return Product(*properties) 
    def get_installed_products_uids():
        """Returns a list with all the different uid of the installed apps."""
        # enum will return an error code according to the result of the app
        products = []
        for i in count(0):
            uid_buffer = create_unicode_buffer(UID_BUFFER_SIZE)
            result = windll.msi.MsiEnumProductsW(i, uid_buffer)
            if result == ERROR_NO_MORE_ITEMS:
                # done interating over the collection
                break
            products.append(uid_buffer.value)
        return products

    def get_installed_products():
        """Returns a collection of products that are installed in the system."""
        products = []
        for puid in  get_installed_products_uids():
            products.append(populate_product(puid))
        return products 

    def get_property(path):
        db = msilib.OpenDatabase(path, msilib.MSIDBOPEN_READONLY)
        si = db.GetSummaryInformation(0)
        return si.GetProperty(msilib.PID_REVNUMBER)

    cwd = os.getcwd()
    try:
        os.chdir(path)

        if '*' in fileName:
            fileName = _get_latest_filename(fileName)

        retvalue = get_property(fileName)[:-1]+ '}' in [prod.PackageCode for prod in  get_installed_products()]

    finally:
        os.chdir(cwd)
    return (fileName, 'msi', retvalue)

@install_action("msi")
def action_msi(path, action, package_manager):
    """Installer action msi files"""
    import subprocess
    cwd = os.getcwd()
    try:
        os.chdir(path)
        for fileName in [action['file']]:
            if '*' in fileName:
                logger.info("Installing the latest msi from: %s." % fileName)
                fileName = _get_latest_filename(fileName)
            else:
                logger.info("Installing msi: %s." % fileName)
            if package_manager.TestMode == False:
                msicommand =  'msiexec /i "%s" AGREETOLICENSE="yes" /qb' % (fileName)
            else:
                msicommand =  'msiexec /j "%s"' % (fileName)            
            returncode = subprocess.call(msicommand)
            logger.info("returning %s." % str(returncode))
    finally:
        os.chdir(cwd)

@install_action("RunScriptCMD")
def action_RunScriptCMDxml(path, action, package_manager):
    """Installer action to call RunScriptCMD"""
    def dict2xml(d, root_node=None):
        wrap          =     False if None == root_node or isinstance(d, list) else True
        root          = 'objects' if None == root_node else root_node
        root_singular = root[:-1] if 's' == root[-1] and None == root_node else root
        xml           = ''
        children      = []
        if isinstance(d, dict):
                for key, value in dict.items(d):
                        if isinstance(value, dict):
                                children.append(dict2xml(value, key))
                        elif isinstance(value, list):
                                children.append(dict2xml(value, key))
                        elif str(key)[0] not in ('-', '@'):
                            children.append(dict2xml(value, key))
                        else:
                            xml = xml + ' ' + key[1:] + '="' + str(value) + '"'
        elif isinstance(d, list):
                for value in d:
                        children.append(dict2xml(value, root_singular))
        else:
            children.append( str(d) )
        end_tag = '>' if 0 < len(children) else '/>'
        if wrap or isinstance(d, dict):
                xml = '<' + root + xml + end_tag
        if 0 < len(children):
                for child in children:
                        xml = xml + child
                if wrap or isinstance(d, dict):
                        xml = xml + '</' + root + '>'
        return xml
    logger.info("RunScriptCMD action...")
    try:
        import RunScriptCMD
        ipath=None
    except ImportError:
        import itertools
        for ipath in itertools.product( [os.environ['ProgramFiles(x86)'], os.environ['ProgramFiles']],
                                        [r'Front\Front Arena\extras\RunScriptCMD',
                                        r'Front\Front Arena\Front Arena Upgrade Suite\RunScriptCMD',
                                        r'Front\Front Arena\Front Arena Migration Suite\RunScriptCMD']):
            ipath = os.path.join(*ipath)
            if os.path.exists(ipath):
                sys.path.insert(0, ipath)
            break
        import RunScriptCMD
    finally:
        if ipath and (ipath in sys.path):
            sys.path.remove(ipath)
    """
    import StringIO
    try: # prepare for python 3.x
        import ConfigParser
    except ImportError:
        import configparser as ConfigParser
    """
    cwd = os.getcwd()
    try:
        os.chdir(path)
        if action.get('xml', None):
            for fileName in [action['xml']]:
                run_script_cmd_parameters = {'xmlfile':fileName}
                if package_manager.TestMode == True:
                    run_script_cmd_parameters['testmode'] = 1
                returncode = RunScriptCMD.ael_main(run_script_cmd_parameters)
        if action.get('Command', None):
            xml = dict2xml({'Command':action['Command']}, 'RunScriptCMD')
            xmlfile = os.path.split(path)[-1]+".xml"#StringIO.StringIO(xml)
            with open(xmlfile, 'wb') as fh:
                fh.write(xml)
            run_script_cmd_parameters = {'xmlfile':xmlfile}
            if package_manager.TestMode == True:
                run_script_cmd_parameters['testmode'] = 1
            returncode = RunScriptCMD.ael_main(run_script_cmd_parameters)
    finally:
        os.chdir(cwd)
        
def validate_transaction(transactions):
    logger.info('validate_transaction()...')
    result = []
    for transaction in transactions:
        operation = transaction[1]
        ael_clone = transaction[0]
        acm_clone = acm.Ael().AelToFObject(ael_clone)
        acm_original = acm_clone.Original()
        acm_clone_updated = acm_clone.UpdateTime()
        acm_clone_updated = acm.Time().DateTimeFromTime(acm_clone_updated)
        acm_original_updated = acm_original.UpdateTime()
        acm_original_updated = acm.Time().DateTimeFromTime(acm_original_updated)
        logger.info('  %s:' % operation)
        logger.info('    original: %s %s' % (acm_original_updated, DatabaseDependencies.node_id(acm_original)))
        logger.info('    upd ael:  %s' % acm.Time().DateTimeFromTime(ael_clone.updat_time))
        logger.info('    updated:  %s %s' % (acm_clone_updated, DatabaseDependencies.node_id(acm_clone)))
        result.append((ael_clone, operation))
    return result

