"""
Description
===========
Date                          :  2018-04-12
Purpose                       :  Bond Uploader
Department and Desk           :  FICC
Requester                     :  Milutinovic, Marko: Absa Capital
Developer                     :  Ondrej Bahounek

Details:
========
This script replaces extenal Bond_Upload_Internal_Linker.xlsm that used AMBA meesages.
The Uploader will be completely built into FA which allows faster booking
and better error handling.
Script expects input file in CSV or XSL format.
Result is one trade (+1 possible mirror) for every row of the file.
"""

import xlrd
import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import FRunScriptGUI
from at_feed_processing import (SimpleCSVFeedProcessor,
                                SimpleXLSFeedProcessor,
                                notify_log)


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()

CHL_NO_FEES = acm.FChoiceList.Select01('list="TradeKey3" and name="PS No Fees"', '')

fileFilter = "CSV Files (*.csv)|*.csv|XLS Files (*.xls)|*.xls|XLSX Files (*.xlsx)|*.xlsx|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label = 'File',
    cls = inputFile,
    default = inputFile,
    mandatory = True,
    multiple = True,
    alt = 'Input file in CSV or XLS format.'
    )

    
class Container(object):
    
    ADDINF_DELIM = ':'
    
    EXTRA_PS_NO_FEES = 'PS NoFees'
    EXTRA_DATA_NAMES = (EXTRA_PS_NO_FEES, )
    def __init__(self):
        self.props = {}
        self.addinfs = {}
        self.extra_data = {}
        
    def add_prop(self, prop, val):
        if type(val) == unicode:
            val = str(val)
        
        prop_addinf = prop.split(self.ADDINF_DELIM)

        if len(prop_addinf) == 1:
            if prop in self.EXTRA_DATA_NAMES:
                self.extra_data.update({prop:val})  # obj property
            else:
                self.props.update({prop:val})  # extra data
        else:
            self.addinfs.update({prop_addinf[1]:val})  # addinfo
        
    def get_props(self):
        return self.props
        
    def get_addinfs(self):
        return self.addinfs


class MainProcessor(object):

    PROP_DELIMITER = ':'
    NAME_TRD = 'trade'
    
    SPECIAL_MAPPING = {
        'CP_Portfolio': "%s%s%s"%(NAME_TRD, PROP_DELIMITER, "MirrorPortfolio"),
        'PS NoFees': "%s%s%s"%(NAME_TRD, PROP_DELIMITER, "PS NoFees"),
        }
        
    def __init__(self):
        self.eof = False
        self._properties = []
        self.calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
    def _process_record(self, record, dry_run):
        (_index, record_data) = record
        
        if self.eof:
            return
        
        if not self._properties:
            self._properties = record_data.keys()
            LOGGER.info("Reading properties: %s" % ", ".join(map(str, self._properties)))
        
        print record_data
        if not record_data['trade:Portfolio']:
            self.eof = True
            return
        
        LOGGER.info("LINE #%d: %s" % (_index, record_data))
        trd_container = Container()
        
        try:
            for prop, val in record_data.items():
                props = self.SPECIAL_MAPPING.get(prop, prop)
                splits = props.split(self.PROP_DELIMITER, 1)
                if len(splits) > 1:
                    prop_type = splits[0]
                    prop_name = splits[1]
                    trd_container.add_prop(prop_name, val)
            
            trade = self.create_trade(trd_container)
            LOGGER.info("Created new trade: %s" % trade.Name())
        except Exception as exc:
            LOGGER.exception(exc)
            raise
            
    def _format_date(self, the_date):
        """Convert xls date (float) to string in human readable format
        
        acm.Time.DateFromTime(the_date) can do the same
        """
        if isinstance(the_date, float):
            the_date = str(xlrd.xldate.xldate_as_datetime(the_date, 0).date())
        return the_date
            
    def create_trade(self, trd_container):
        trd = acm.FTrade()
        instr = acm.FInstrument[trd_container.get_props()['Instrument']]
        trd.Instrument(instr)
        trd.Currency(instr.Currency())
        # for backdating trades TradeTime needs to be set in the input file
        trd.TradeTime(acm.Time.TimeNow())
        trd.Trader(acm.User())
        trd.Text1("SAFI_BondUploader")
        
        for property, value in trd_container.get_props().items():
            if value == "":
                continue
            trd.SetProperty(property, value)
        
        if trd_container.extra_data[trd_container.EXTRA_PS_NO_FEES]:
            trd.OptKey3(CHL_NO_FEES)
        
        trd.RegisterInStorage()
        
        add_infs = trd.AdditionalInfo()
        for property, value in trd_container.get_addinfs().items():
            if value == "":
                continue
            add_infs.SetProperty(property, value)
        
        premium = trd.Calculation().PriceToPremium(self.calc_space, 
            trd.ValueDay(), trd.Price()).Number()
        trd.Premium(premium)
        
        trd.Commit()
        return trd


class CSVCreator(MainProcessor, SimpleCSVFeedProcessor):
  
    def __init__(self, file_path):
        MainProcessor.__init__(self)
        SimpleCSVFeedProcessor.__init__(self, file_path, do_logging=False)


class XLSCreator(MainProcessor, SimpleXLSFeedProcessor):
  
    def __init__(self, file_path):
        
        MainProcessor.__init__(self)
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)


def ael_main(ael_dict):
    file_path = str(ael_dict['input_file'])
    LOGGER.info("Input file: %s", file_path)
    if file_path.endswith(".csv"):
        proc = CSVCreator(file_path)
    else:
        proc = XLSCreator(file_path)
    
    proc.add_error_notifier(notify_log)
    proc.process(False)
    
    LOGGER.info("Completed successfully.")
