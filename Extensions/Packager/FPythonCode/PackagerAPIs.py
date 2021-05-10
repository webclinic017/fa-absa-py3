import os
import acm
import traceback
import FLogger
import PackageInstallerParametersManager
import PackageFileRepository
import PackageManager
import BuildPackage
import DatabaseDependenciesNetworkX as DatabaseDependencies
parameters = PackageInstallerParametersManager.ParametersManager()
verbosity = int(parameters.read('message_verbosity'))
logger = FLogger.FLogger(name=__name__, level=verbosity)

class PackagerAPIs(object):
    def __init__(self):
        self.m_packageFileRepository = PackageFileRepository.PackageFileRepository()

    def CreatePackage(self, package_name, acm_objects, major_version = 1, minor_verison = 0, ignore_object_types = None):
        graph = DatabaseDependencies.GetDependencyGraph(acm_objects)
        DatabaseDependencies.find_roots(graph)
        folder = BuildPackage.BuildPackageFromGraph(graph, acm_objects, None, ignore_object_types)
        package_info = {}
        package_info['name'] = package_name
        package_info['version'] = major_version
        update_number = self.m_packageFileRepository.increment_update_number(package_info)
        complete_version = '%s.%s.%s' % (str(major_version), str(minor_verison), update_number)
        package_info['version'] = complete_version
        self.m_packageFileRepository.add_package(package_info, folder, True)

    def DeletePackage(self, package_name):
        if os.path.exists(package_name):#it means the entire path is given
            logger.debug('Deleting package %s....'%package_name)
            self.m_packageFileRepository.delete_folder(package_name)
        else:#it means only the name of pacakge is given with/without extension - both should be checked
            package_path = os.path.join(parameters.read('DefaultFolder'), package_name)
            if os.path.exists(package_path):
                logger.debug('Deleting package %s....'%package_path)
                self.m_packageFileRepository.delete_folder(package_path)
            else:
                logger.info('Package <%s> not found in %s'%(package_name, parameters.read('DefaultFolder')))

    def CreatePackageBeyondDateTime(self, package_name, date_time_val):
        #This support needs to be added
        pass

    def ImportPackage(self, package_path):
        #This support needs to be added
        package_manager = PackageManager.PackageManager() 
        package_manager.TestMode = False
        file_repository = PackageFileRepository.PackageFileRepository(False)
        result = file_repository.get_meta_data(package_path)
        package_manager.install_package(result['name'], result['version'], False)

