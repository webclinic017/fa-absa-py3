"""
Description
===========
Date                          :  2018-06-14
Purpose                       :  Bulk Bond Uploader
Department and Desk           :  FO Prime Services
Requester                     :  Naidoo, Eveshnee: Markets (JHB)
Developer                     :  Ondrej Bahounek

Details:
========
This script allows bulk trades booking from input file (CSV or XSL format).
"""

import xlrd
from collections import defaultdict

import acm

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import FRunScriptGUI
from at_feed_processing import (
    SimpleCSVFeedProcessor,
    SimpleXLSFeedProcessor,
    notify_log,
)


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()

BOOKING_TEXT1 = "PS_BulkBondUpload"
PARTY_FREE_TEXT = "PS_Bond_Upload"
RISK_PORTF = acm.FPhysicalPortfolio[12045]  # 'PB_RISK_FV_INTERMED_EUROCLEAR'
CHL_NO_FEES = acm.FChoiceList.Select01('list="TradeKey3" and name="PS No Fees"', "")
ACQUIRER = acm.FParty[32737]  # 'PRIME SERVICES DESK'
SIMULATED = "Simulated"
FO_CONFIRMED = "FO Confirmed"
BOOKING_STATUS = None
IS_PRIME_BROKER = "No"

fileFilter = (
    "CSV Files (*.csv)|*.csv|XLS Files (*.xls)|*.xls|XLSX Files (*.xlsx)|*.xlsx|"
)
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilter)

ael_variables = AelVariableHandler()
ael_variables.add(
    "input_file",
    label="File",
    cls=inputFile,
    default=inputFile,
    mandatory=True,
    multiple=True,
    alt="Input file in CSV or XLS format.",
)
ael_variables.add(
    "portfolio",
    label="Portfolio",
    cls=acm.FPhysicalPortfolio,
    default=None,
    mandatory=False,
    multiple=False,
    alt="Portfolio where all trades will be booked to.",
)
ael_variables.add(
    "trade_status",
    label="Trade Status",
    cls="string",
    collection=[SIMULATED, FO_CONFIRMED],
    default=SIMULATED,
    mandatory=False,
    alt="Trade Status of newly created trades",
)
ael_variables.add(
    "prime_broker",
    label="Prime Broker?",
    cls="string",
    collection=["No", "Yes"],
    default="No",
    mandatory=True,
    multiple=False,
    alt="Prime Broker?",
    hook=None,
    enabled=True
)


class Container(object):

    ADDINF_DELIM = "|"

    EXTRA_PS_NO_FEES = "PS NoFees"
    UNEXCOR_CP = "UnexCor"
    SETTLE_DATE = "Settle Date"
    EXTRA_DATA_NAMES = (
        EXTRA_PS_NO_FEES,
        UNEXCOR_CP,
        SETTLE_DATE,
    )

    def __init__(self):
        self.props = defaultdict(str)
        self.addinfs = defaultdict(str)
        self.extra_data = defaultdict(str)

    def add_prop(self, prop, val):
        if type(val) == str:
            val = str(val)

        prop_addinf = prop.split(self.ADDINF_DELIM)

        if len(prop_addinf) == 1:
            if prop in self.EXTRA_DATA_NAMES:
                self.extra_data.update({prop: val})  # obj property
            else:
                self.props.update({prop: val})  # extra data
        else:
            self.addinfs.update({prop_addinf[1]: val})  # addinfo

    def get_props(self):
        return self.props

    def get_addinfs(self):
        return self.addinfs

    def get_extras(self):
        return self.extra_data


class MainProcessor(object):

    PROP_DELIMITER = ":"
    NAME_TRD = "trade"

    # all extra column names stated here will be read
    # if a cloumn name is not in this list, then it won't be read
    SPECIAL_MAPPING = {
        "Instrument": "%s%s%s" % (NAME_TRD, PROP_DELIMITER, "Instrument"),
        "PS NoFees": "%s%s%s" % (NAME_TRD, PROP_DELIMITER, "PS NoFees"),
        "Quantity": "%s%s%s" % (NAME_TRD, PROP_DELIMITER, "Quantity"),
        "Price": "%s%s%s" % (NAME_TRD, PROP_DELIMITER, "Price"),
        "Settle Date": "%s%s%s" % (NAME_TRD, PROP_DELIMITER, "Settle Date"),
        "UnexCor": "%s%s%s" % (NAME_TRD, PROP_DELIMITER, "UnexCor"),
        "Companion Spread": "%s%s%s"
        % (NAME_TRD, PROP_DELIMITER, "FTrade|Companion_Spread"),
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
            LOGGER.info(
                "Reading properties: %s" % ", ".join(map(str, self._properties))
            )

        if not record_data["Instrument"]:
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
        except Exception as ex:
            LOGGER.exception("Line not processed.")
            raise

    def _format_date(self, the_date):
        """Convert xls date (float) to string in human readable format

        acm.Time.DateFromTime(the_date) can do the same
        """
        if isinstance(the_date, float):
            the_date = str(xlrd.xldate.xldate_as_datetime(the_date, 0).date())
        return the_date

    def _get_party(self, unexcor):
        addinfos = acm.FAdditionalInfo.Select(
            'addInf = "UnexCor Code" and fieldValue="%s"' % unexcor
        )
        party = None
        for ai in addinfos:
            party = ai.Parent()
            if party.Free3() == PARTY_FREE_TEXT:
                break
        return party

    def create_trade(self, trd_container):
        trd = acm.FTrade()
        instr = acm.FInstrument[trd_container.get_props()["Instrument"]]
        cal = instr.Currency().Calendar()
        trd.Instrument(instr)
        trd.Currency(instr.Currency())
        trd.Portfolio(RISK_PORTF)
        unexcor = trd_container.get_extras()["UnexCor"]
        party = self._get_party(unexcor)

        trd.Counterparty(party)
        trd.Acquirer(ACQUIRER)
        trd.Trader(acm.User())
        trd.Text1(BOOKING_TEXT1)
        # for backdating trades TradeTime needs to be set in the input file
        trd.TradeTime(acm.Time.TimeNow())
        settle_day = trd_container.get_extras()["Settle Date"]
        if not settle_day:
            settle_day = cal.AdjustBankingDays(TODAY, instr.SpotBankingDaysOffset())
        trd.ValueDay(settle_day)
        trd.AcquireDay(settle_day)
        trd.Status(BOOKING_STATUS)
        trd.AdditionalInfo().Prime_Broker(IS_PRIME_BROKER)

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
            trd.AddInfoValue(property, value)

        premium = (
            trd.Calculation()
            .PriceToPremium(self.calc_space, trd.ValueDay(), trd.Price())
            .Number()
        )
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


def unex_from_filename(filename):
    unexcor = filename[: filename.find("_")]
    return unexcor


def run_bulk_bond_booking(*args):
    acm.RunModuleWithParameters(__name__, acm.GetDefaultContext())


def ael_main(ael_dict):
    file_path = str(ael_dict["input_file"])
    portfolio = ael_dict["portfolio"]
    status = ael_dict["trade_status"]
    prime_broker = ael_dict["prime_broker"]
    global RISK_PORTF
    RISK_PORTF = portfolio
    global BOOKING_STATUS
    BOOKING_STATUS = status
    global IS_PRIME_BROKER
    IS_PRIME_BROKER = prime_broker

    LOGGER.info("Input file: %s", file_path)
    if file_path.endswith(".csv"):
        proc = CSVCreator(file_path)
    else:
        proc = XLSCreator(file_path)

    proc.add_error_notifier(notify_log)
    proc.process(False)

    LOGGER.info("Completed successfully.")
