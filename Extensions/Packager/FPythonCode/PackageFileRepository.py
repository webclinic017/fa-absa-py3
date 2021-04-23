import acm
import ael
import cStringIO
import FLogger
import json
import os
import os.path
import PackageInstallerParametersManager

import shutil
import traceback
import types
import urllib

from xml.etree import cElementTree
import zipfile

PACKAGE_META_FILE = 'package_meta.json'
PACKAGE_DEF_FILE  = 'package_def.json'

_packages = {}   # { name : ('meta' : meta_data , 'location' : file_location) }
_timestamps_for_meta_data = {} # {timestamp : desc_file}
_cached_meta_data = {} # {desc_file : meta_data}

parameters = PackageInstallerParametersManager.ParametersManager()
verbosity = int(parameters.read('message_verbosity'))
logger = FLogger.FLogger(name=__name__, level=verbosity)

def get_amba_object_desc(msg_xml):
    def get_primary_key_attribute(table):
        for i in eval('ael.%s.keys()' % table):
            if i[1] == 'primary':
                return i[0].upper()

    def get_unique_key_attributes(table):
        for i in eval('ael.%s.keys()' % table):
            if i[1] == 'unique':
                return [k.upper() for k in i[2]]
        return []

    table = msg_xml.find('TYPE').text
    table_node = msg_xml.find(table)
    table = dict((i.upper(), i) for i in dir(ael) if isinstance(getattr(ael, i), type(ael.Trade)))[table.upper()]
    pk_node = table_node.find(get_primary_key_attribute(table))
    if pk_node != None:
        id = pk_node.text
    else:
        id = ','.join([table_node.find(k).text for k in get_unique_key_attributes(table) if table_node.find(k) != None])
    return id, table, acm.AMBAMessage.CreateSimulatedObject(cElementTree.tostring(msg_xml))

def zip_archive(path):
    res = cStringIO.StringIO()
    zip = zipfile.ZipFile(res, 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            arc_path = os.path.relpath(full_path, path)
            zip.write(full_path, arc_path)
    zip.close()
    res.seek(0)
    return res

class PackageFileRepository:

    """File based Front Arena package repository

    Note : may not support simultaneous access by different clients
    """

    def __init__(self, src_folder = None, buildIndex = True):
        self.src_folder = parameters.read('DefaultFolder')
        if self.src_folder.find('~') != -1:
            self.src_folder = os.path.expanduser(self.src_folder)
        if buildIndex:
            self.build_package_index()
        
    # If the modification timestamp has not changed,
    # get the meta_data from the cache. Otherwise, get it from the filesystem.
    def get_meta_data(self, package_path):
        result = None
        desc_file = os.path.join(package_path, PACKAGE_META_FILE)
        if os.path.exists(desc_file):
            current_timestamp = os.lstat(desc_file).st_mtime
            cached_timestamp = _timestamps_for_meta_data.get(desc_file)
            if cached_timestamp == None or current_timestamp > cached_timestamp:
                with open(desc_file) as f: 
                    try:
                        meta = json.loads(f.read())
                        #convert dictionary from unicode to string
                        result = dict([(str(key), str(val)) for key, val in meta.items()])
                        _timestamps_for_meta_data[desc_file] = current_timestamp
                        _cached_meta_data[desc_file] = result
                        # logger.debug('Using metadata read from from %s: %s' % (desc_file, result))
                    except:
                        logger.error('Failed to load package meta data from: %s.\n%s' % (desc_file, traceback.format_exc()))
            else:
                result = _cached_meta_data.get(desc_file)
                logger.debug('Using cached metadata for %s: %s' % (desc_file, result))
        else:
            logger.info('%s not found. Hence not processing further'%desc_file)
        return result
            
    def _get_package_def(self, path):
        file = os.path.join(path, PACKAGE_DEF_FILE)
        try:
            install_json = open(file).read()
            package_def = json.loads(install_json)
            return package_def
        except ValueError, e:
            logger.error("Failed to read package definition file: '%s'\n%s" % (file, traceback.format_exc()))
        except IOError, e:
            logger.error("Failed to open package definition file: '%s'\n%s" % (file, traceback.format_exc()))

    def add_package_to_index(self, package_path, package_meta):
        if 'name' in package_meta:
            logger.debug('Adding package to index from "%s": "%s".' % (package_path, package_meta))
            name = package_meta['name']
            version = package_meta.setdefault('version', '')
            package_data = {'meta': package_meta, 
                            'path': package_path}
            _packages.setdefault(name, {}).setdefault('versions', {})[version] = package_data
            # TODO: Fix this to base on major.minor.UPDATE.
            _packages[name]['latest_version'] = max(_packages[name].get('latest_version', ''), version)
            if package_path.find(version) == -1:
                _packages[name]['versions']['default_version'] = package_data
            _packages[name]['name'] = name
            for version, package in _packages[name].items():
                logger.debug('version: %s package: %s' % (version, package))
        return _packages

    def build_package_index(self, update_status = None):
        """Completely rebuild package index by scanning directory"""
        refresh_list = False
        try:
            refresh_list = parameters.read('refresh_package_list')           
        except:
            pass
        parameters.write('refresh_package_list', False)
        if refresh_list:
            global _packages
            _packages = {}
        self.src_folder = parameters.read('DefaultFolder')
        if self.src_folder.find('~') != -1:
            self.src_folder = os.path.expanduser(self.src_folder)
            parameters.write('DefaultFolder', self.src_folder)
        if not os.path.isdir(self.src_folder):
            return
        for folder in sorted(os.listdir(self.src_folder), cmp=lambda x, y: cmp(x.lower(), y.lower())):
            package_path = os.path.join(self.src_folder, folder)
            if not os.path.isdir(package_path ):
                continue
            package_meta = self.get_meta_data(package_path)
            if package_meta != None:
                self.add_package_to_index(package_path, package_meta)
                if update_status is not None:
                    update_status('Indexed package "%s"...' % package_meta['name'])
            else:
                #global _packages
                #_packages = {}
                logger.error("No valid meta data package file %s in %s: " % (PACKAGE_META_FILE, package_path))

    def set_folder(self, src_folder = None):
        self.src_folder = parameters.read('DefaultFolder')
        self.build_package_index()

    def get_all_packages(self, rebuildIndex = False, update_status = None):
        if rebuildIndex:
            self.build_package_index(update_status) 
        return _packages

    def get_all_packages_metadata(self, only_latest_version=True):
        metaData = []
        if only_latest_version:
            metaData = [package['versions'][package['latest_version']]['meta'] for package in _packages.values()]
        else:
            for package in _packages.values():
                metaData.extend([data['meta'] for data in package['versions'].values()])
        return metaData

    def write_meta_data(self, folder, meta_data):
        meta_data = json.dumps(meta_data, indent=4, separators=(',', ': '))
        with open(os.path.join(folder, PACKAGE_META_FILE), 'w') as f:
            f.write(meta_data)

    def get_package(self, package_name, version='default_version'):
        logger.info('get_package: name: %s version: %s' % (package_name, version))
        package = _packages.get(package_name)
        # logger.debug('package: %s' % package)
        if package:
            versions = package['versions']
            #for version_ in versions:
            #    logger.info('version: "%s"' % version_)
            result = versions.get(version)
            #logger.debug('result: %s' % result)
            if result != None:
                return result
            else:
                latest_version = package.get('latest_version')
                if type(latest_version) == types.StringType:
                    return versions[latest_version]
                else:
                    return latest_version

    def register_user_action(self, action, win_user_name, ads_user, machine_name,
            prime_version, action_time, extra_data):
        raise NotImplementedError
        
    '''
    The update number is incremented every time a package is saved from the 
    Package Installer. This number increments without respect to the major and 
    minor version numbers. Therefore, the most recently updated package is the 
    one with the highest update number, even if it was an earlier version that 
    was updated.
    '''
    def increment_update_number(self, package_info):
        maximum_update_number = 0
        if package_info != None:
            package_name = package_info['name']
            package = _packages.get(package_name)
            if package != None:
                versions = package['versions']
                for version in versions:
                    logger.debug('version: %s' % version)
                    version_parts = version.split('.')
                    if len(version_parts) >= 3:
                        update_number = int(version_parts[2])
                        if update_number > maximum_update_number:
                            maximum_update_number = update_number
        return maximum_update_number + 1

    def validate_package(self, package_info, upgrade_if_exists = False):
        version = package_info.get('version')
        #repositoryVersion = None
        name = package_info.get('name')
        logger.debug('validate_package: name: %s version: %s upgrade_if_exists: %s' % (name, version, upgrade_if_exists))
        if not name:
            logger.error("Can't add a package without a name.")
            return False
        if name in _packages:
            #repositoryVersion = _packages[name]['latest_version']
            package_info['version'] = version
        if version:
            try:
                [int(n) for n in version.split('.')]
            except:
                logger.error('%s is not a valid version number' % version)
                return False
        return True

    def delete_package(self, package_name, version):
        package = self.get_package(package_name, version)
        if not package:
            return
        version = package['meta'].get('version', '')
        logger.info('Deleting package %s version %s [%s]' % (package_name, version, package['path']))
        shutil.rmtree(package['path'])
        del _packages[package_name]['versions'][version]
        if not _packages[package_name]['versions']:
            del _packages[package_name]
    
    def unzip_folder_content(self, zip_file):
        file_name = self.get_file_name(zip_file)
        folder_location = os.path.dirname(zip_file)
        folder_name = os.path.join(folder_location, file_name)
        try:
            os.stat(folder_name)
        except:
            os.mkdir(folder_name) 
        zip_ref = zipfile.ZipFile(zip_file, 'r')
        zip_ref.extractall(folder_name)
        zip_ref.close()
        return folder_name

    def get_file_name(self, file_name):
        """get only the name of the file"""
        file_name_only = ''
        file_name = os.path.basename(file_name)
        try:
            file_name_only = os.path.splitext(file_name)[0]
            file_name_only = file_name_only.strip()
        except Exception, e:
            pass
        return file_name_only
    
    def get_file_extension(self, file_name):
        """get the extension of a file for a given file name"""
        file_extension = ''
        try:
            file_extension = os.path.splitext(file_name)[1]
        except:
            pass
        return file_extension

    def delete_folder(self, folder_location):
        shutil.rmtree(folder_location) 
    
    def delete_file(self, file_with_path):
        os.remove(file_with_path)

    def create_zip_file(self, file_location):
        one_level_up = os.path.dirname(file_location)
        file_name = os.path.basename(file_location)
        save_location = os.path.join(one_level_up, file_name + '.zip')
        zipf = zipfile.ZipFile(save_location, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(file_location):
            for file in files:
                full_path = os.path.join(root, file)
                zipf.write(full_path, os.path.basename(full_path))
        zipf.close()
        self.delete_folder(file_location)

    def add_package(self, package_info, package_path, upgrade_if_exists = False):
        from PackageManager import size_of_fileobj
        if not self.validate_package(package_info, upgrade_if_exists):
            logger.error('Failed to validate package.')
            return
        pack_zip = zip_archive(package_path) 
        name = package_info.get('name')
        logger.info("  Uploading package '%s' version '%s'. Size = %s" % (name, package_info.get('version', ''), size_of_fileobj(pack_zip)))
        folder = os.path.join(self.src_folder, name)
        if os.path.exists(folder):
            metaData = self.get_meta_data(folder)            
            newFolder = '%s_%s' % (folder, metaData.get('version', '')) if metaData.get('name') == name else folder
            while os.path.exists(newFolder):
                if newFolder[-1] == ')':
                    i = newFolder.rfind('(') + 1
                    try:
                        newFolder = newFolder[:i] + str(int(newFolder[i:-1]) + 1) + ')'
                        continue
                    except:
                        pass
                newFolder += '(1)'
            if metaData.get('name') == name:
                os.rename(folder, newFolder)
            else:
                folder = newFolder
        logger.info('Extracting package to: %s.' % folder)
        zipfile.ZipFile(pack_zip).extractall(folder)
        self.write_meta_data(folder, package_info)
        self.add_package_to_index(folder, package_info)
        logger.info('Ended extracting package to: %s.' % folder)

    def get_package_content(self, package_name, version):
        import Transporters
        import PackageManager
        package_objects = []
        package_data = self.get_package(package_name, version)
        if package_data:
            path = package_data['path']
            package_def = self._get_package_def(path)
            if package_def and 'actions' in package_def:
                for action in package_def['actions']:
                    if action['type'] == 'extmod':
                        action['type'] = 'transporter'
                        action['transporter'] = 'Extension Module'
                    if action['type'] == 'workbook':
                        action['type'] = 'transporter'
                        action['transporter'] = 'Workbook'
                    folder = os.path.join(path, str(action.get('folder', '')))
                    for fileName in [str(action['file'])] if 'file' in action else sorted(os.listdir(folder)):
                        file = os.path.join(folder, fileName)
                        if action['type'] == 'ambamsg':
                            try:
                                xml_tree = cElementTree.parse(file)
                            except Exception, e:
                                logger.error('ERROR when parsing amba file: %s.' % fileName, exc_info=True)
                                continue
                            for msg_node in xml_tree.findall('MESSAGE'):
                                package_objects.append(get_amba_object_desc(msg_node))
                        elif action['type'] == 'transporter':
                            name = fileName.rsplit('.', 1)[0]
                            nameSplit = name.rsplit('.', 1)
                            if len(nameSplit) == 2 and nameSplit[1] == 'xml':
                                name = nameSplit[0]
                            name = urllib.unquote(name)
                            handler = Transporters.Transporter.all_handlers[action['transporter']]
                            package_objects.append((name, handler.ClassName(), handler.SelectSingle(name)))
                        elif action['type'] == 'file':
                            installedFile = None
                            package_objects.append((fileName, 'File', installedFile))
                        elif action['type'] in ('addextmod', 'python'):
                            pass
                        elif action['type'] == 'msi':
                            package_objects.append(PackageManager.check_msi(folder, fileName))
                        else:
                            logger.warn("Unhandled install action '%s' in package" % action['type'])
                            break
        return package_objects

