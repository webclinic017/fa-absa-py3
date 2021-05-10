
import acm
import os
import glob
from subprocess import Popen, call, PIPE
import FLogger
import FAptReportUtils
import FAptReportCommon

logger = FLogger.FLogger.GetLogger('APT')



class AptLauncher(object):
    APT_PATH            = 'APT_INSTALLATION_PATH'
    APT_MODELS_PATH     = 'APT_MODELS_PATH'
    XDB_MANAGER_EXE     = 'APTXdbManager.exe'
    UNIVERSE_XDB        = 'Universe.xdb'
    APTPRO_EXE          = 'APTPro.exe'

    def __init__(self, composition_path, universe_path):
        self.comp_path = composition_path
        self.univ_path = universe_path
        self.apt_path = FAptReportUtils.FAptReportParameters().get(self.APT_PATH)
        
    def run(self, command, exe):
        p = Popen(command, shell=True, executable=exe, stdout=PIPE, stderr=PIPE)
        res = p.communicate()
        return res

        
    def get_xdb_arg(self):
        filename = self.UNIVERSE_XDB
        #removing dependency to UserPreferences
        #dir = FAptReportCommon.AptDatabasePath.get_database_files_path()
        dir = FAptReportUtils.FAptReportParameters().get(self.APT_MODELS_PATH)
        return os.path.join(dir, filename)
        
    def get_exe(self):
        os.chdir(self.apt_path)
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            for filename in (f for f in filenames if f == '%s' % self.XDB_MANAGER_EXE):
                return os.path.join(dirpath, filename)
        return
                
    def get_args(self):
        xdb_flag = '-xdb'
        xdb_arg = self.get_xdb_arg()
        import_flag = '-i'
        import_arg = self.univ_path
        return '%s "%s" %s "%s"' % (xdb_flag, xdb_arg, import_flag, import_arg)
    
    def create_universe_xdb_file(self):
        try:
            exe_file = self.get_exe()
            if not exe_file:
                raise Exception("%s no found in %s" % (self.XDB_MANAGER_EXE, self.apt_path))
            output, error = self.run(self.get_args(), exe_file)
            logger.debug(output)
            if error:
                logger.error(error)
        except Exception as err:
            raise Exception("Could not create Universe xdb reason: %s" % err)
            
    def get_apt_exe_path(self):
        os.chdir(self.apt_path)
        apt_exe_path = None
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            if apt_exe_path:
                break
            for filename in (f for f in filenames if f == '%s' % self.APTPRO_EXE):
                apt_exe_path = os.path.join(dirpath, filename)
        return apt_exe_path

    def run_apt_app(self):
        apt_exe_path = self.get_apt_exe_path()
        if not apt_exe_path:
            raise Exception("%s not found in %s" % (self.APTPRO_EXE, self.apt_path))
        try:
            thread = acm.FThread()
            thread.Run(self.run, [[apt_exe_path, self.comp_path], None])
            logger.info("Starting AptPro application...")
        except Exception as err:
            raise err

        
