"""-------------------------------------------------------------------------------------------------------
MODULE
    FAptReport - RunScriptGui
    
    (c) Copyright 2010 by Sungard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import os
import glob
import re
import acm
import FRunScriptGUI
import FLogger
import FAptTest
import FAptReportUtils
import FAptReportGenerate
import FAptReportCommon

logger = FLogger.FLogger.GetLogger('APT')

falseTrue = ['False', 'True']

class FAptReport(FRunScriptGUI.AelVariablesHandler):
    """class representing gui"""
    
    GUI_PARAMS = {'runButtonLabel':   '&&Run Report',
                  'hideExtraControls': False,
                  'windowCaption' : __name__}
    
    class Parameters( object ):
        """class holding gui parameter names and values"""
        
        REPORT_NAME           = 'report_name' 
        FACTOR_MODEL          = 'factor_model' 
        PORTFOLIO             = 'portfolio'
        TRADE_FILTER          = 'trade_filter'
        HIDE_ZERO_UNIT_ROWS   = 'hide_zero_unit_rows'
        HIDE_ZERO_PRICE_ROWS  = 'hide_zero_price_rows'
        LAUNCH_APT            = 'launch_apt'
        FUND_OF_FUNDS         = 'fund_of_funds'
        SUB_PORT_JOB          = 'sub_port_job'
        GROUPER               = 'grouper'
        COMPOSITION_FILE      = 'composition_file'
        UNIVERSE_FILE         = 'universe_file'
        
        LOG_LEVEL             = 'log_level'
        LOG_FILE              = 'log_file'

        
        LOG_LEVEL_MAP         = {'info':1, 'debug':2, 'warn':3, 'error':4, 'critical':5}

        
        def __init__( self, p):
            self.report_name = p.get(FAptReport.Parameters.REPORT_NAME)
            self.factor_model = p.get(FAptReport.Parameters.FACTOR_MODEL)
            self.portfolios = list(p.get(FAptReport.Parameters.PORTFOLIO))
            self.trade_filters = list(p.get(FAptReport.Parameters.TRADE_FILTER))
            self.groupers = p.get(FAptReport.Parameters.GROUPER)
            self.hide_zero_unit_rows = p.get(FAptReport.Parameters.HIDE_ZERO_UNIT_ROWS)
            self.hide_zero_price_rows = p.get(FAptReport.Parameters.HIDE_ZERO_PRICE_ROWS)
            self.launch_apt = p.get(FAptReport.Parameters.LAUNCH_APT)
            
            self.composition_file = p.get(FAptReport.Parameters.COMPOSITION_FILE)
            self.universe_file = p.get(FAptReport.Parameters.UNIVERSE_FILE)

            self.log_level = p.get(FAptReport.Parameters.LOG_LEVEL)
            self.log_file = p.get(FAptReport.Parameters.LOG_FILE)

            self.validate_params()
            self.init_logger()
            
        def validate_params(self):
            """validate parameter from gui"""
            FAptReport.validate_report_contents(self.portfolios, self.trade_filters)
            FAptReport.validate_output_file(self.composition_file)
            FAptReport.validate_output_file(self.universe_file)
            FAptReport.validate_log_file(self.log_file)
            self.validate_log_level()
                            

        def validate_log_level(self):
            """map log level"""
            self.log_level = self.__class__.LOG_LEVEL_MAP.get(self.log_level)
            if not self.log_level:
                raise FAptReportUtils.RunScriptGuiValidationError("Invalid log level.") 

        def init_logger(self):
            """reinitialize logger with user preferences"""
            logger.Reinitialize(level=self.log_level, logToFileAtSpecifiedPath=self.log_file) 



    @classmethod
    def get_gui_params( cls ):
        return cls.GUI_PARAMS
        
    @classmethod
    def validate_log_file(cls, filename):
        log_dir, file = os.path.split(filename)
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
                logger.info("Created log directory %s.", log_dir)
            except Exception as err:
                logger.error("Failed to created log directory %s.", log_dir)
                raise err
                
    @classmethod
    def validate_output_file(cls, filename):
        directory, file = os.path.split(filename)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
                logger.info("Created directory %s.", directory)
            except Exception as err:
                logger.error("Failed to created directory %s.", directory)
                raise err
                
    @classmethod
    def validate_report_contents(cls, portfolios, trade_filters):
        if len(portfolios) == 0 and len(trade_filters) == 0:
            raise FAptReportUtils.RunScriptGuiValidationError("Portfolio or Trade Filter must be entered to run Apt Report")
            
    
    def get_factor_models(self):
        #removing dependency to UserPreferences
        #self.factor_models_path = FAptReportCommon.AptDatabasePath.get_database_files_path()
        self.factor_models_path = FAptTest.AptTest._get_apt_models_path()
        try:
            os.chdir(self.factor_models_path)
            return [os.path.splitext(filename)[0] for filename in glob.glob('*.fdb')]

        except WindowsError as err:
            logger.warn('The system cannot find the file specified: "%s"', str(self.factor_models_path))
            return []
    
    def get_factor_models_names(self):
        factor_models = list(set([re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z])|(?=[(]))', ' ', name[:-8]).lstrip() for name in self.get_factor_models()]))
        if not factor_models:
            factor_models = ['']
            logger.warn("Cannot find any Apt factor model file (.fdb) in the specified path: '%s'. Using default factor model '%s'", self.factor_models_path, self.default_factor_model)
        return factor_models
       
    def get_default_factor_model_name(self):
        default_factor_model = FAptReportUtils.FAptReportParameters().get('DEFAULT_FACTOR_MODEL')
        default_factor_model = re.sub(' ', '', default_factor_model)
        if default_factor_model:
            return re.sub('((?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z])|(?=[(]))', ' ', default_factor_model).lstrip()
        return self.get_factor_models_names()[0]

    def __init__(self):
        self.default_factor_model = self.get_default_factor_model_name()
        factor_models = self.get_factor_models_names()
        vars = [
                 #Report tab
                 [FAptReport.Parameters.REPORT_NAME, 'Report Name_Report', 'string',
                  None, "APT Report", 1, 0, 'Enter report name', None, 1],   
                 [FAptReport.Parameters.FACTOR_MODEL, 'Factor Model_Report', 'string',
                  factor_models, self.default_factor_model, 1, 0, 'Select factor model', None, 1],
                 [FAptReport.Parameters.PORTFOLIO, 'Portfolio_Report', 'FPhysicalPortfolio',
                  "", None, 0, 1, 'Select Portfolio', None, 1],
                 [FAptReport.Parameters.TRADE_FILTER, 'Trade Filter_Report', 'FTradeSelection',
                  "", None, 0, 1, 'Select Trade Filter', None, 1],
                 [FAptReport.Parameters.GROUPER, 'Grouper_Report', 'FStoredPortfolioGrouper',
                  "", None, 0, 1, 'Select Grouper', None, 1],
                 [FAptReport.Parameters.HIDE_ZERO_UNIT_ROWS, 'Exclude Zero Unit Rows_Report', 'string', falseTrue, 'True', 1, 0, 
                  'Excludes zero unit rows from the Apt Report ', None, 1],
                 [FAptReport.Parameters.HIDE_ZERO_PRICE_ROWS, 'Exclude Zero Price Rows_Report', 'string', falseTrue, 'True', 1, 0,
                  'Excludes invalid price rows from the Apt Report ', None, 1],
                 [FAptReport.Parameters.LAUNCH_APT, 'Start APTPro_Report', 'string', falseTrue, 'True', 1, 0,
                  'Starts APTPro ', None, 1],
                  
                 #Output tab
                 [FAptReport.Parameters.COMPOSITION_FILE, 'Composition File_Output:', 'string',
                  "", FAptReportUtils.FAptPath.get_composition_path(), 1, 0, 'Path for writing the composition file.', None, 1],
                 [FAptReport.Parameters.UNIVERSE_FILE, 'Universe File_Output:', 'string',
                  "", FAptReportUtils.FAptPath.get_universe_path(), 1, 0, 'Path for writing the universe file.', None, 1],
                  
                 #Log tab
                 [FAptReport.Parameters.LOG_LEVEL, 'Log Level_Log:', 'string',
                  ['info', 'debug', 'warn', 'error', 'critical'], 'info', 1, 0, 'Log level', None, 1],
                 [FAptReport.Parameters.LOG_FILE, 'Log File_Log:', 'string',
                  "", FAptReportUtils.FAptPath.get_apt_report_log_path(), 1, 0, 'Log file path', None, 1],
                  
               ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, vars)
           
        
ael_variables = FAptReport()
ael_variables.LoadDefaultValues(__name__)
ael_gui_parameters = FAptReport.get_gui_params()
                 
def ael_main(parameters):
    try:
        params = FAptReport.Parameters(parameters)
        FAptReportGenerate.generate(params)
    except ImportError as err:
        logger.error(str(err))
    except Exception as err:
        logger.ELOG( str(err), exc_info=1 )
    

def startRunScript(eii):
    acm.RunModuleWithParameters("FAptReport", acm.GetDefaultContext())

