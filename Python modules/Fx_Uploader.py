"""--------------------------------------------------------------------------
MODULE
   FUploaderUtils

DESCRIPTION
    This module houses common funstionality of uploaders

HISTORY 
Date: 2019-10-10 
Author: Snowy Mabilu
Jira:  FAFO-23 - Code for booking Fx Cash trades

-----------------------------------------------------------------------------"""
import acm
import FRunScriptGUI
import FUxCore
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_feed_processing import (SimpleXLSFeedProcessor, notify_log)
from FTradeCreator import DecoratedTradeCreator
from FUploaderUtils import CreateOutput
from at_ux import msg_box

ael_variables = AelVariableHandler()
fileFilter = "XLSX Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)
LOGGER = getLogger(__name__)
ael_variables.add('input_file',
                  label='File',
                  cls=inputFile,
                  default=inputFile,
                  mandatory=True,
                  multiple=True,
                  alt='Input file in CSV or XLS format.')

ael_variables.add('acquirer',
                  label='Acquirer',
                  mandatory=True,
                  default="Gold Desk")

ael_variables.add('doc_type',
                  label='Document Type',
                  mandatory=False,
                  default="")

class CreateFXTradesFromExcel(SimpleXLSFeedProcessor):
    SPOTPROCESS_BIT = 4096
    FORWARDPROCESS_BIT = 8192

    def __init__(self, file_path, acquirer, doc_type):
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)
        self.acquirer = acquirer
        self.doc_type = doc_type
        self.trades = []

    def reformat_input(self, record_data):
        try:
            formatted_dict = dict()
            formatted_dict["Instrument"] = str(record_data["Instrument"])
            formatted_dict["Currency"] = str(record_data["Currency"])
            formatted_dict["Quantity"] = float(record_data["Quantity"])
            formatted_dict["ValueDay"] = acm.Time.AsDate((record_data["Value day"]))
            formatted_dict["Price"] = float(record_data["Price"])
            formatted_dict["Portfolio"] = str(record_data["Portfolio"])
            formatted_dict["Guarantor"] = str(record_data["Cpty"])
            formatted_dict["Counterparty"] = str(record_data["Cpty"])
            formatted_dict["MirrorPortfolio"] = str(record_data["Cpty portfolio"])
            formatted_dict["Acquirer"] = self.acquirer
            formatted_dict["AcquireDay"] = acm.Time.AsDate((record_data["Value day"]))
            formatted_dict["DocumentType"] = self.doc_type
            formatted_dict["Type"] = "Normal"
            pair = acm.FCurrencyPair[formatted_dict["Instrument"] + '/' + formatted_dict["Currency"]]
            date = pair.SpotDate(acm.Time.DateNow())
            if formatted_dict["ValueDay"] > date:
                formatted_dict['TradeProcess'] = self.FORWARDPROCESS_BIT
            else:
                formatted_dict['TradeProcess'] = self.SPOTPROCESS_BIT
            return formatted_dict
        except Exception as exc:
            LOGGER.exception(str(exc))
            raise exc

    def _process_record(self, record, dry_run):
        (_index, record_data) = record
        try:
            formatted_dict = self.reformat_input(record_data)
            creator = DecoratedTradeCreator(formatted_dict)
            trade = creator.CreateTrade()
            trade.Commit()
            self.trades.append(trade)
            LOGGER.info("Successfully booked FX Cash trade {}".format(trade.Oid()))
        except Exception as exc:
            msg = 'Row #%d: Failed to read data from file: row{}, reason: {}'.format(_index, str(exc))
            LOGGER.exception(msg)
            raise exc


def ael_main(ael_dict):
    try:
        proc = CreateFXTradesFromExcel(str(ael_dict['input_file']), str(ael_dict['acquirer']), str(ael_dict['doc_type']))
        proc.process(False)
        # Render output
        shell = acm.UX().SessionManager().Shell()
        dlg = CreateOutput('FX Trades', proc.trades)
        acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
        LOGGER.info("Succesfully booked FX Cash trades from file {}".format(str(ael_dict['input_file'])))
    except Exception as exc: 
        msg = "Failed to book trades from file {}, because {} ".format(str(ael_dict['input_file']), exc)
        msg_box(msg)
        LOGGER.exception(msg)            

