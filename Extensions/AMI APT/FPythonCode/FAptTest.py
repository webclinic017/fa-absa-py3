
import glob
import os
import re
import acm
import FAptLauncher
import FAptReportCommon
import FAptReportUtils
import FLogger

logger = FLogger.FLogger.GetLogger('APT')

class AptTest(object):
    UNIV_PATH = FAptReportUtils.FAptPath.get_universe_path()
    COMP_PATH = FAptReportUtils.FAptPath.get_composition_path()

    @classmethod
    def _show_details(cls, details):
        print ("#"*20)
        print ("#", " "*3, "DETAILS", " "*4, "#" )
        print ("#"*20)
        print (details)
        print ("#"*20)

    @classmethod
    def _test_apt_pro_installed(cls):
        MESSAGE = 'Checking that APTPro is installed...'
        DETAILS = 'Please, install APTPro and try again'
        if FAptLauncher.AptLauncher(cls.COMP_PATH, cls.UNIV_PATH).get_apt_exe_path():
            logger.info('%s\t%s', MESSAGE, 'OK')
        else:
            logger.info('%s\t%s', MESSAGE, 'NOT OK')
            cls._show_details(DETAILS)
            
    @classmethod
    def _test_apt_utilities_installed(cls):
        MESSAGE = 'Checking that AptXdbManager is installed...'
        DETAILS = 'Please, install APTUtils and try again'
        if FAptLauncher.AptLauncher(cls.COMP_PATH, cls.UNIV_PATH).get_exe():
            logger.info('%s\t%s', MESSAGE, 'OK')
        else:
            logger.info('%s\t%s', MESSAGE, 'NOT OK')
            cls._show_details(DETAILS)
    
    @classmethod
    def _test_apt_user_preferences_file_exists(cls):
        MESSAGE = 'Checking that APT UserPreferences file exists...'
        DETAILS = 'The UserPreferences file was not found. APTPro needs to have been started at least once for it to be created.\nPlease start APTPro, close it and try again'
        if FAptReportCommon.AptDatabasePath.get_user_preferences_path():
            logger.info('%s\t%s', MESSAGE, 'OK')
        else:
            logger.info('%s\t%s', MESSAGE, 'NOT OK')
            cls._show_details(DETAILS)
            
    @classmethod
    def _get_database_files_path(cls):
        return FAptReportCommon.AptDatabasePath.get_database_files_path()
        
    @classmethod
    def _get_default_model_name(cls):
        return FAptReportUtils.FAptReportParameters().get('DEFAULT_FACTOR_MODEL')
    
    @classmethod
    def _get_apt_models_path(cls):
        return FAptReportUtils.FAptReportParameters().get('APT_MODELS_PATH')
        
    @classmethod
    def get_used_model_date(cls):
        MODEL_NAME = cls._get_default_model_name()
        #removing dependency to UserPreferences
        #model_path = cls._get_database_files_path()
        model_path = cls._get_apt_models_path()
        model_name = re.sub(' ', '', MODEL_NAME)
        os.chdir(model_path)
        fnames = [os.path.splitext(filename)[0][-8:] for filename in glob.glob('*.fdb') if os.path.splitext(filename)[0][:-8] == model_name]
        if fnames:
            return sorted(fnames)[-1]

    @classmethod        
    def _test_access_apt_database_files_path(cls):
        MESSAGE = 'Checking access to fdb path...'
        DETAILS = 'Please, start APTPro, select Edit\\Preferences...\nand make sure that you have read/write access to \nthe Database Files path set. If not, please \nchange the path, move all Database Files to new path \nand try again'
        #removing dependency to UserPreferences
        #fdb_path = cls._get_database_files_path()
        fdb_path = cls._get_apt_models_path()
        path = os.path.join(fdb_path, 'dummy.txt')
        try:
            with open(path, 'w') as file:
                file.write('dummy test, please remove')
            file.close()
            os.remove(path)
            logger.info('%s\t%s', MESSAGE, 'OK')
        except:
            logger.info('%s\t%s', MESSAGE, 'NOT OK')
            cls._show_details(DETAILS)
    
    @classmethod
    def _test_default_model_exists(cls):
        MODEL_NAME = cls._get_default_model_name()
        MESSAGE = 'Checking that APT default model %s exists...' % MODEL_NAME
        DETAILS = 'Please, make sure that the DEFAULT_MODEL parameter \nin FAptReportParameters points to the right model or\nthat the model has been downloaded and moved to the \npath set in APTPro->Edit->Preferences...\\Database Files\npath and try again'
        USER_PREF_MISSING = 'UserPreferences file needs to be find to \n determine whether the default model exists'
        #removing dependency to UserPreferences
        #model_path = cls._get_database_files_path()
        model_path = cls._get_apt_models_path()
        model_name = re.sub(' ', '', MODEL_NAME)
        try:
            os.chdir(model_path)
            fnames = [filename for filename in glob.glob('*.fdb') if os.path.splitext(filename)[0][:-8] == model_name]
            if fnames:
                logger.info('%s\t%s', MESSAGE, 'OK')
            else:
                logger.info('%s\t%s', MESSAGE, 'NOT OK')
                cls._show_details(DETAILS)
        except WindowsError:
            logger.info(USER_PREF_MISSING)
            
    @classmethod
    def _test_apt_recon_id_file(cls):
        MESSAGE = 'Checking that Recon id file for default model exists...'
        DETAILS = 'Please, make sure that the reconciliation id file\ncontaining all ids in the used APT model has been \ndownloaded, named the same as the APT factor model, moved \nto the path set in APTPro\\Edit\\Preferences...\\Database Files\npath and try again'
        import FAptIdRecon
        if FAptIdRecon.FAptIdRecon.get_id_file_name():
            logger.info('%s\t%s', MESSAGE, 'OK')
        else:
            logger.info('%s\t%s', MESSAGE, 'NOT OK')
            cls._show_details(DETAILS)
        
    @classmethod
    def _test_prime_restarted(cls):
        MESSAGE = 'Checking that Prime has been re-started after APT Setup...'
        DETAILS = 'Please, re-start Prime and try again'
        ins = acm.FInstrument.Select(None).First()
        try:
            ins.AdditionalInfo().APT_Export_Type()
            ins.AdditionalInfo().APT_Recon_Id_Type()
            # ins.AdditionalInfo().DATASTREAM()
            logger.info('%s\t%s', MESSAGE, 'OK')
        except:
            logger.info('%s\t%s', MESSAGE, 'NOT OK')
            cls._show_details(DETAILS)
            
    @classmethod
    def test(cls):
        cls._test_apt_pro_installed()
        cls._test_apt_utilities_installed()
        cls._test_apt_user_preferences_file_exists()
        cls._test_access_apt_database_files_path()
        cls._test_default_model_exists()
        cls._test_apt_recon_id_file()
        cls._test_prime_restarted()
        
def test(eii):
    AptTest.test()
            
        
