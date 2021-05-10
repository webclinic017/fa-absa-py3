import os
import string
import datetime

import acm
import at_addInfo
from at_feed_processing import notify_log
from at_ael_variables import AelVariableHandler
from PS_Functions import get_pb_fund_counterparty
from at_logging import getLogger
import pb_gpp_general
from pb_gpp_upload import (
                           InputProperties,
                           GenericContainer,
                           PositionsCSV,
                           InstrumentHelper,
                           Future,
                           Stock,
                           Option,
                           CFD,
                           get_file_object,
                           sanitize_code,
                           get_fa_date,
                           FORBIDDEN_CHARS_EXT,
                           remove_nonascii
                           )

                           
UPDATE_INSTR = False

LOGGER = getLogger(__name__)
TRADE_DATE = ""


def generate_trdref(alias, insid, quantity):
    """Get unique ID - max 31 chars
        GPP/ONB/alias/insid/[BS]:
    """
    bs = "B"
    if float(quantity) < 0:
        bs = "S"
    trdref = "{0}/{1}/{2}/{3}/{4}".format("GPP", "ONB", alias[:9], insid[:11], bs)
    return trdref


class PositionsOnboardCSV(PositionsCSV):
    FILE_INDEX = "positions_file_name"
    LOAD_THIS_INDEX = "load_positions"
    
    col_trd_qty = "Quantity"
    col_wap = "WAP"
    col_ins_contrsize = "Multiplier"
    col_trd_qty = "Quantity"
    col_description = "SecurityDesc"
    
    
    _required_columns = PositionsCSV._required_columns + [
        col_wap, col_ins_contrsize,
        col_trd_qty, col_description]
        
    # ins types that have underlyings
    UNDERLYING_TYPES = (pb_gpp_general.GPP_FUT_TYPE,
                        pb_gpp_general.GPP_OPT_TYPE)
    
    def __init__(self, file_path):
        super(PositionsOnboardCSV, self).__init__(file_path)
        LOGGER.info("%s processing %s", "-" * 16, self.__class__.__name__)
        
    def _get_underlying(self, product_type, bloom_code):
        if product_type not in self.UNDERLYING_TYPES:
            return None
        und_ins_name = pb_gpp_general.get_underlying(bloom_code)
        if not und_ins_name:
            raise RuntimeError("Product type '%s' with code '%s' not recognised. "
                               "Please update Instrument file." % (product_type, bloom_code))
        instr = acm.FInstrument[und_ins_name]
        if not instr:
            raise RuntimeError("Can't map product type '%s' (code: '%s') to any existing "
                               "underlying instrument" % (product_type, bloom_code))
        return instr
        
    def _process_record(self, record, dry_run):
        (_index, record_data) = record
        
        try:
            alias = pb_gpp_general.get_account_alias(record_data[self.col_account_name])
            if not alias:
                LOGGER.warning("Skipping account '%s' (alias not recognised)...",
                    record_data[self.col_account_name])
                return
                
            gpp_type = record_data[self.col_ins_type]
            if not pb_gpp_general.is_valid_gpp_instype(gpp_type):
                LOGGER.warning("Invalid GPP instype: '%s'", gpp_type)
                return
            
            bloom_code = sanitize_code(record_data[self.col_ins_code_bloom])
            underlying = self._get_underlying(gpp_type, bloom_code)

            container = GenericContainer()
            
            container.ins_gpp_instype = gpp_type
            container.acm_underlying = underlying
            container.acm_currency = acm.FCurrency[record_data[self.col_currency]]
            container.ins_expiry_date = get_fa_date(record_data[self.col_ins_exp_date])
            container.ins_ext_code = InstrumentHelper.process_raw_ins_code(record_data[self.col_ins_code_bloom])
            container.option_type = record_data[self.col_put_call]
            container.strike_price = record_data[self.col_strike]
            
            container.trade_qty = record_data[self.col_trd_qty]
            container.ins_contract_size = record_data[self.col_ins_contrsize]
            container.trade_price = float(record_data[self.col_wap])
            
            container.trade_opt_key = generate_trdref(alias, container.ins_ext_code, container.trade_qty)
            
            container.trade_date = TRADE_DATE
            container.value_date = TRADE_DATE
            
            
            container.acm_portf = pb_gpp_general.get_trading_portf()
            container.acm_cparty = get_pb_fund_counterparty(alias)
            container.acm_extern_curr = acm.FCurrency["USD"]
            container.ins_description = remove_nonascii(record_data[self.col_description])
            container.isin = record_data[self.col_ins_code_isin]
            container.exchange = remove_nonascii(record_data[self.col_exchange])
            
            
            builder = None
            if gpp_type == pb_gpp_general.GPP_FUT_TYPE:
                builder = Future(container)
            elif gpp_type == pb_gpp_general.GPP_STO_TYPE:
                builder = Stock(container)
            elif gpp_type == pb_gpp_general.GPP_OPT_TYPE:
                builder = Option(container)
            elif gpp_type == pb_gpp_general.GPP_CFD_TYPE:
                builder = CFD(container)
                
            if not builder:
                raise RuntimeError("GPP Instrument type '%s' not recognised." % gpp_type)
                
            builder.check_instrument()
            ins = builder.get_instrument()
            if not ins or UPDATE_INSTR:
                ins = builder.create_ins()

            builder.book_trades()
            
            eod_price = float(record_data[self.col_eod_price])
            eod_date = get_fa_date(record_data[self.col_report_date])
            InstrumentHelper.save_prices(ins, eod_price, eod_date)
            
        
        except Exception as exc:
            LOGGER.exception(exc)
            raise self.RecordProcessingException(
                "ERROR while processing row #%d of file '%s': %s" \
                    % (_index, os.path.basename(self._file_path), str(exc)))


def enable_custom_start_date(selected_variable):
    cust = ael_variables.get("custom_date")
    cust.enabled = (selected_variable.value == 'Custom Date')

ael_variables = AelVariableHandler()
ael_variables.add("date",
                  label="Date",
                  cls="string",
                  default="Custom Date",
                  collection=pb_gpp_general.DATE_KEYS,
                  hook=enable_custom_start_date,
                  mandatory=True,
                  alt=("A date for which files will be taken."))
ael_variables.add("custom_date",
                  label="Custom Date",
                  cls="string",
                  default="2017-10-19",
                  enabled=False,
                  alt=("Format: '2016-09-30'."))
ael_variables.add("file_dir",
                  label="Directory",
                  default=r"c:\DEV\Perforce\FA\features\ABITFA-4916 - GPP - go live.br\input\2017-10-19",
                  alt=("A Directory template with all input files. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYY-MM-DD)"))
ael_variables.add(PositionsOnboardCSV.FILE_INDEX,
                  label="Positions file",
                  default="",
                  alt=("A path to the positions input file. "
                       "Should include WAP column"
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date (format YYYYMMDD)"))
ael_variables.add(PositionsOnboardCSV.LOAD_THIS_INDEX,
                  label="Load Positions File?",
                  cls="bool",
                  collection=(True, False),
                  default=True)
                       
# ##################################
# SETTINGS TAB
ael_variables.add("update_instr",
                  label="Update instruments?_Settings",
                  default=False,
                  cls="bool",
                  collection=(True, False),
                  alt=("Update instruments during the run? "
                      "Only applicable for TradesExecuted runs."))
ael_variables.add("trade_date",
                  label="Trades Date",
                  cls="date",
                  default="2017-10-19",
                  mandatory=False,
                  alt=("If set, this date will be used for trades value dates "
                       "and instruments prices."
                       "If empty, dates from report will be used. "
                       "Use only in special cases - very rarely. "
                       "Format: '2016-09-30'"))

pb_gpp_general.add_common_aelvars(ael_variables)
                      
def ael_main(ael_dict):

    pb_gpp_general.set_general_input(ael_dict)
    
    dry_run = False
    InputProperties.reset()
    
    global UPDATE_INSTR
    UPDATE_INSTR = ael_dict["update_instr"]
    
    global TRADE_DATE
    if ael_dict['trade_date']:
        TRADE_DATE = ael_dict['trade_date'].to_string("%Y-%m-%d")
    else:
        TRADE_DATE = None
        
    file_path_pos = get_file_object(ael_dict, PositionsOnboardCSV)
    if file_path_pos:
        processor = PositionsOnboardCSV(file_path_pos)
        processor.add_error_notifier(notify_log)
        processor.add_error_notifier(InputProperties.add_error)
        processor.process(dry_run)

    if InputProperties.has_errors():
        LOGGER.error("Errors occurred.")
    else:
        LOGGER.info("Completed successfully.")
        
