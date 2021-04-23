"""-----------------------------------------------------------------------------
MODULE
    pcg_option_uploader_file

DESCRIPTION
    Date                : 2017-08-17
    Purpose             : Upload instruments from file and book trades on them.
    Department and Desk : PCG Valuations
    Requester           : Ryan Fagri (ryan.fagri@barclays.com)
    Developer           : Ondrej Bahounek
    CR Number           : 
ENDDESCRIPTION

Template instrument taken from VCG_TOTEM_INDEX and VCG_TOTEM_SSO trade filters.

Required columns (expected values):
OptionType: ['Put', 'Call']
ExerciseType: ['American', 'European']
StrikeType: ['Absolute', 'Rel Spot Pct 100']
QuantoOptionType: ['None', 'Compo']

HISTORY
=============================================================================================
Date        Change no    Developer          Description
---------------------------------------------------------------------------------------------
2017-09-19  4954857      Ondrej Bahounek    Initial implementation
------------------------------------------------------------------------------------------"""

from datetime import datetime
import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from PS_Functions import modify_asql_query
import FRunScriptGUI
from at_feed_processing import SimpleCSVFeedProcessor, notify_log


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()

fileFilter = "*.csv"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label = 'File',
    cls = inputFile,
    default = inputFile,
    mandatory = True,
    multiple = True,
    alt = 'Input file.'
    )
    
    
class Creator(SimpleCSVFeedProcessor):

    
    def __init__(self, file_path):
        self.eof = False
        self._properties = []
        super(Creator, self).__init__(file_path, do_logging=False)
        
    def _process_record(self, record, dry_run):
        (_index, record_data) = record
        
        if self.eof:
            return
        
        if not self._properties:
            self._properties = list(record_data.keys())
            LOGGER.info("Reading properties: %s" % ", ".join(map(str, self._properties)))
        
        if not record_data['Name']:
            self.eof = True
            return
        
        LOGGER.info("LINE #%d: %s" % (_index, record_data))
        
        try:
            instr = create_instrument(record_data)
            LOGGER.info("Created instrument: '%s'" % instr.Name())
            
            trade = create_trade(instr)
            LOGGER.info("Created trade: '%s'" % trade.Name())
        except Exception as exc:
            LOGGER.exception(exc)
            raise


def create_instrument(prop_val_dict):

    ins_name = prop_val_dict['Name']
    ins = acm.FInstrument[ins_name]
    if ins:
        LOGGER.warning("Instrument '%s' already exists", ins_name)
        return ins
        
    _option = acm.FOption()
    optdec = acm.FOptionDecorator(_option, None)
    for property, value in list(prop_val_dict.items()):
        optdec.SetProperty(property, value)
    
    optdec.Commit()    
    return optdec


def create_trade(instr):
    t = acm.FTrade()
    t.Instrument(instr)
    t.Currency(instr.Currency())
    t.Status('Simulated')
    
    spot_days = instr.SpotBankingDaysOffset()
    cal = instr.Currency().Calendar()
    val_date = cal.AdjustBankingDays(TODAY, spot_days)
    t.TradeTime(TODAY)
    t.ValueDay(val_date)
    t.AcquireDay(val_date)
    t.Commit()
    return t


def ael_main(ael_dict):
    file_path = str(ael_dict['input_file'])
    LOGGER.info("Input file: %s", file_path)
    proc = Creator(file_path)
    proc.add_error_notifier(notify_log)
    proc.process(False)
    
    LOGGER.info("Completed successfully.")
