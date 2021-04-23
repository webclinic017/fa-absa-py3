"""--------------------------------------------------------------------------------------
MODULE
    sbl_collateral_file_uploader

DESCRIPTION
    Date                : 2019-07-18
    Purpose             : This script will be used to book bonds, ncds and equity
                          collateral trades from a file
    Department and Desk : PCG
    Requester           : Shaun Du Plessis
    Developer           : Sihle Gaxa
    CR Number           : CHG1001992765

HISTORY
=========================================================================================
Date            Change no       Developer               Description
-----------------------------------------------------------------------------------------
2019-07-18      CHG1001283051   Sihle Gaxa              Initial implementation.

2019-10-24      CHG0061162      Sihle Gaxa              Changed to book a collateral
                                                        trade entry instrument
2021-02-19      PCGDEV-663      Sihle Gaxa              Added original trade ID in text2
ENDDESCRIPTION
------------------------------------------------------------------------------------------"""
import acm
import xlrd

import FRunScriptGUI
from at_logging import getLogger
import sbl_booking_utils as sbl_utils
import sbl_booking_validator as sbl_validator

from FUploaderParams import REPORT_STATUS
import FUploaderFunctions as pcg_uploader
from at_ael_variables import AelVariableHandler
from at_feed_processing import (SimpleCSVFeedProcessor,
                                SimpleXLSFeedProcessor,
                                notify_log)

DELIMITER = ':'
LOGGER = getLogger(__name__)
fileFilter = "CSV Files (*.csv)|*.csv|XLS Files (*.xls)|*.xls|XLSX Files (*.xlsx)|*.xlsx|"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)


ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label='File',
    cls=inputFile,
    default=inputFile,
    mandatory=True,
    multiple=True,
    alt='Input file in CSV or XLS format.'
    )
ael_variables.add(
    'email_address',
    label='Email address',
    default='xraeqdcollateralmana@absa.africa',
    mandatory=False,
    multiple=True,
    alt='Email results to these recipients'
    )


class Container(object):

    extra_mirror_party = "CustodyCounterparty"
    extra_data_names = (extra_mirror_party, )

    def __init__(self):
        self.props = {}
        self.addinfos = {}
        self.extra_data = {}

    def add_prop(self, prop, val):
        if type(val) == unicode:
            val = str(val)

        prop_addinf = prop.split(DELIMITER)

        if len(prop_addinf) == 1:
            if prop in self.extra_data_names:
                self.extra_data.update({prop: val})
            else:
                self.props.update({prop: val})
        else:
            self.addinfos.update({prop_addinf[1]: val})

    def get_props(self):
        return self.props

    def get_addinfos(self):
        return self.addinfos


class TradeUploader(object):

    error_rows = {}
    report_row = 1
    trade_object = "trade"
    custody_counterparty = None
    
    special_mapping = {
        "CustodyCounterparty": "%s%s%s" % (trade_object, DELIMITER, "CustodyCounterparty"),
        }

    def __init__(self):

        self.eof = False
        self._properties = []

    def _process_record(self, record, dry_run):

        (_index, record_data) = record

        if self.eof:
            return

        if not self._properties:
            self._properties = record_data.keys()
            LOGGER.info("Reading object fields from file: %s" % ", ".join(map(str, self._properties)))

        if not record_data['trade:Instrument']:
            self.eof = True
            return

        row_data = sbl_validator.InputFileValidator(self.report_row, record_data)

        if not (row_data.is_number(self.error_rows) and
                row_data.is_not_zero(self.error_rows) and
                row_data.is_banking_day(self.error_rows) and
                row_data.is_valid_status(self.error_rows) and
                row_data.is_valid_value_day(self.error_rows) and
                row_data.is_valid_portfolio(self.error_rows) and
                row_data.is_valid_instrument(self.error_rows) and
                row_data.is_valid_swift_flag(self.error_rows) and
                row_data.is_active_portfolio(self.error_rows) and
                row_data.is_valid_counterparty(self.error_rows)):

                add_failure_row(self.report_row, record_data, self.error_rows)
                self.report_row += 1
                return

        trade_container = Container()

        try:
            for column_name, column_value in record_data.items():
                column_data = self.special_mapping.get(column_name, column_name)
                column_data = column_data.split(DELIMITER, 1)

                if len(column_data) > 1:
                    trade_field = column_data[1]
                    trade_container.add_prop(trade_field, column_value)

            if trade_container.extra_mirror_party in record_data.keys():
                custody_counterparty_name = trade_container.extra_data[trade_container.extra_mirror_party]
                custody_counterparty = acm.FParty[custody_counterparty_name]
            
            trade = self.create_trade(trade_container)
            LOGGER.info("Trade {trd} successfully created".format(trd=trade.Oid()))

            if trade and custody_counterparty:
                try:
                    add_original_trade(trade)
                    custody_trade = trade.Clone()
                    custody_trade.ContractTrade(trade)
                    custody_trade.ConnectedTrade(None)
                    custody_trade.FaceValue(-1*trade.FaceValue())
                    custody_trade.Counterparty(custody_counterparty)

                    if trade.AddInfoValue("SL_IsCorpAction"):
                        custody_trade.AddInfoValue("SL_IsCorpAction", "True")

                    custody_trade.Text2(trade.Oid())
                    custody_trade.Commit()
                    add_original_trade(custody_trade)
                    LOGGER.info("Custody trade {custody_trd} successfully created".format(custody_trd=custody_trade.Oid()))
                    add_success_row(self.report_row, trade, REPORT_STATUS["success_status"], custody_trade)
                    self.report_row += 1
                except Exception as e:
                    raise Exception("Could not create custody trade for {trade} because {error}".format(
                                    trade=trade.Oid(), error=str(e)))
            else:
                add_original_trade(trade)
                add_success_row(self.report_row, trade, REPORT_STATUS["success_status"])
                self.report_row += 1

        except Exception as e:
            raise Exception("Could not process file because {error}".format(error=str(e)))


    def create_trade(self, trade_container):
    
        try:
            trade = acm.FTrade()
            instrument = acm.FInstrument[trade_container.get_props()['Instrument']]
            trade.Type("Normal")
            trade.Trader(acm.User())
            trade.Instrument(instrument)
            trade.Acquirer(sbl_utils.ACQUIRER)
            trade.Currency(instrument.Currency())
            trade.TradeCategory(sbl_utils.COLLATERAL_CATEGORY)
            trade.ValueDay(get_date(trade_container.get_props()["AcquireDay"]))
            trade.AcquireDay(get_date(trade_container.get_props()["AcquireDay"]))
            
            for property, value in trade_container.get_props().items():
            
                if property == "TradeTime":
                    if value == "":
                        trade.TradeTime(acm.Time.TimeNow())
                    else:
                        trade_date = get_date(value)
                        trade_time = ("{date} {time_now}".format(
                                      date=trade_date, time_now=acm.Time().TimeOnlyMs()))
                        trade.TradeTime(trade_time[:-4])

                elif value != "":
                    trade.SetProperty(property, value)
            
            trade.RegisterInStorage()

            add_infos = trade.AdditionalInfo()
            for property, value in trade_container.get_addinfos().items():
            
                if value != "":
                    if property == "SL_SWIFT" and value in sbl_utils.SETTLE_CATEGORY:
                        trade.SettleCategoryChlItem(sbl_utils.SETTLE_CATEGORY[value])
                    
                    add_infos.SetProperty(property, value)

            if instrument.InsType() == "CD":
                trade.AddInfoValue("Funding Instype", sbl_utils.NCD_ADD_INFO)

            if not trade.Price():
                price = instrument.UsedPrice(sbl_utils.PREVIOUS_DAY, instrument.Currency(), sbl_utils.MARKET.Name())/100
                trade.Price(price)
            trade.Text2(trade.Oid())
            trade.Commit()
            return trade

        except Exception as e:
            raise Exception("Could not book trade because {error}".format(error=str(e)))


def get_date(trade_date):
    if isinstance(trade_date, float):
        trade_date = str(xlrd.xldate.xldate_as_datetime(trade_date, 0).date())
    date = acm.Time.DateAddDelta(trade_date, 0, 0, 0)
    return date

def email_uploaded_trades(email_addresses):
    email_sender = 'xraeqdcollateralmana@absa.africa'
    report_header = 'Uploaded collateral trades'
    email_subject = 'Uploaded collateral trades on %s' % acm.Time.DateToday()
    table_headings = 'Portfolio', 'Counterparty', 'Custody Counterparty', 'Security', 'Trade', 'Custody Trade', 'Quantity', 'Status', 'Failure reason'
    pcg_uploader.add_header(table_headings)
    pcg_uploader.send_report(email_addresses, email_sender, email_subject, report_header)


def add_email_data(row_number, trade, status, custody_trade=None):
    if custody_trade:
        email_row = [str(row_number), trade.Portfolio().Name(), trade.Counterparty().Name(),
                    custody_trade.Counterparty().Name(), trade.Instrument().Name(), 
                    str(trade.Oid()), str(custody_trade.Oid()), str(trade.FaceValue()), status, '-']
    else:
        email_row = [str(row_number), trade.Portfolio().Name(), trade.Counterparty().Name(),
                    '-', trade.Instrument().Name(), str(trade.Oid()), '-',
                    str(trade.FaceValue()), status, '-']
    return email_row


def add_success_row(row_number, trade, status, custody_trade=None):
    row_info_list = add_email_data(row_number, trade, status, custody_trade)
    pcg_uploader.add_row(str(row_number), row_info_list)


def add_failure_row(row_number, record_data, error_rows):
    row_info_list = [str(row_number), str(record_data['trade:Portfolio']), 
                    str(record_data['trade:Counterparty']), str(record_data['CustodyCounterparty']),
                    str(record_data['trade:Instrument']), '-', '-', str(record_data['trade:FaceValue']),
                    REPORT_STATUS["failure_status"], error_rows[row_number]]
    pcg_uploader.add_row(str(row_number), row_info_list)


def add_original_trade(trade):
    trade.Text2(trade.Oid())
    trade.Commit()


class CSVCreator(TradeUploader, SimpleCSVFeedProcessor):

    def __init__(self, file_path):
        TradeUploader.__init__(self)
        SimpleCSVFeedProcessor.__init__(self, file_path, do_logging=False)


class XLSCreator(TradeUploader, SimpleXLSFeedProcessor):

    def __init__(self, file_path):
        TradeUploader.__init__(self)
        SimpleXLSFeedProcessor.__init__(self, file_path, sheet_index=0, sheet_name=None)


def ael_main(dictionary):

    file_path = str(dictionary['input_file'])

    LOGGER.info("Processing input file: %s", file_path)

    if file_path.endswith(".csv"):
        proc = CSVCreator(file_path)
    else:
        proc = XLSCreator(file_path)

    proc.add_error_notifier(notify_log)
    proc.process(False)

    email_addresses = dictionary['email_address']
    if email_addresses:
        email_uploaded_trades(email_addresses)

    LOGGER.info("Completed successfully.")
