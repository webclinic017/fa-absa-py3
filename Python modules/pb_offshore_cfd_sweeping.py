"""-----------------------------------------------------------------------------
Daily sweeping of client funding and TPL for offshore CFD's

HISTORY
================================================================================
Date           Developer          Description
--------------------------------------------------------------------------------
2020-11-20     Marcus Ambrose     Implemented
2021-02-24     Marcus Ambrose     Updated to use daily MTM
-----------------------------------------------------------------------------"""
import string
import os
import sys

import acm

from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from PS_Functions import get_pb_fund_counterparty, SetAdditionalInfo
from PS_CallAccountSweeperFunctions import (
    get_call_account,
    get_brokers_call_account,
)
from PS_FundingSweeper import CreateCashFlow
from pb_offshore_cfd_utils import (
    csv_dict_list,
    get_fx_rate,
    get_previous_weekday,
    get_workdays_from_range,
    is_int,
    get_fa_date,
)
from pb_offshore_cfd_config import get_exchange_rates, get_absa_rate, BROKER_PORTFOLIOS
from sweeping_report import OffshoreFundingSweepingReport, OffshorePnLSweepingReport

LOGGER = getLogger(__name__)


class AbstractTplSweeper:
    COLUMN_CLIENT_ACCOUNT = None
    COLUMN_FUNDING_AMOUNT = None
    COLUMN_FUNDING_CURRENCY = None
    COLUMN_UNDERLYING_CURRENCY = None
    COLUMN_DAY_COUNT = None
    COLUMN_BROKER_SPREAD = None
    COLUMN_DAYS = None
    COLUMN_PAY_DATE = None
    COLUMN_REPORT_DATE = None
    COLUMN_UNDERLYING_CODE = None
    COLUMN_UNDERLYING_TICKER = None
    COLUMN_UNDERLYING_NAME = None
    COLUMN_BASE_RATE = None
    COLUMN_EFFECTIVE_RATE = None
    COLUMN_BROKER_FUNDING = None
    COLUMN_WEIGHTED_AVERAGE_PRICE = None
    COLUMN_WEIGHTED_AVERAGE_AMOUNT = None
    COLUMN_CLOSING_PRICE = None
    COLUMN_CLOSING_AMOUNT = None
    COLUMN_FEES = None
    COLUMN_MTM = None
    COLUMN_FUNDING = None
    COLUMN_REPORT_DATE_SYN = None
    COLUMN_QUANTITY = None
    COLUMN_MTM_TOTAL = None
    COLUMN_MTM_TOTAL_USD = None
    COLUMN_FX_RATE = None
    COLUMN_LAST_RESET_PAY_DATE = None
    BROKER_FULL_NAME = None

    ACCOUNTING_CURRENCY = acm.FCurrency["USD"]

    def __init__(
        self, funding_file, synthetic_file, client_short_name, broker, report_date,
    ):
        self.funding_dict = csv_dict_list(funding_file)
        self.synthetic_dict = csv_dict_list(synthetic_file)
        self.client_short_name = client_short_name
        self.broker = broker
        self.report_date = report_date
        self.counterparty = get_pb_fund_counterparty(self.client_short_name)
        self.client_broker_account = self._get_client_account()
        self.field_name = "PB_{}_CFD_TPL".format(self.broker)

        self.funding_report_content = []
        self.pnl_report_content = []
        self.report_line = None

        self.client_account = get_call_account(
            self.client_short_name, self.ACCOUNTING_CURRENCY
        )
        self.broker_account = get_brokers_call_account(
            self.client_short_name, self.ACCOUNTING_CURRENCY, self.broker
        )
        self.total_absa_funding = 0

    def sweep_funding(self):
        index = 0
        try:
            for index, record in enumerate(self.funding_dict):
                if self._is_correct_client(record):
                    if record[self.COLUMN_PAY_DATE] == record[self.COLUMN_REPORT_DATE]:
                        self._write_funding_report_line(record)
                    if self.is_reset_date():
                        self._calculate_absa_funding(record)

        except Exception as e:
            raise Exception(
                "ERROR while processing row {} for funding cost file: {}".format(
                    str(index + 1), e
                )
            )

        LOGGER.info(
            "Funding sweeping completed successfully for {}".format(self.report_date)
        )

    def sweep_tpl(self):
        daily_tpl = 0
        try:
            for index, record in enumerate(self.synthetic_dict):
                self._write_synthetic_record(record)
                daily_tpl += float(record[self.COLUMN_MTM_TOTAL_USD])

            leg = self.client_account.Legs()[0]
            self._save_amount_to_depo(daily_tpl, self.report_date, leg)

            # post to broker account
            daily_tpl *= -1
            leg = self.broker_account.Legs()[0]
            self._save_amount_to_depo(daily_tpl, self.report_date, leg)

        except Exception as ex:
            raise Exception(
                "ERROR while processing row {} of file {}: {}".format(
                    str(index + 1), "daily synthetic file", str(ex)
                )
            )

        LOGGER.info(
            "TPL sweeping completed successfully for {}".format(self.report_date)
        )

    def is_reset_date(self):
        first_record = self.synthetic_dict[0]
        return (
            first_record[self.COLUMN_REPORT_DATE_SYN]
            == first_record[self.COLUMN_LAST_RESET_PAY_DATE]
        )

    def get_tpl_data(self):
        return self.pnl_report_content

    def get_funding_data(self):
        return self.funding_report_content

    def get_total_absa_funding(self):
        return self.total_absa_funding

    def _get_execution_fees(self):
        total_execution_fees = 0
        portfolio = BROKER_PORTFOLIOS[self.broker]

        from_date = self._get_reset_from_date()

        query = acm.CreateFASQLQuery("FTrade", "AND")
        query.AddAttrNode("Counterparty.Name", "EQUAL", self.counterparty.Name())
        query.AddAttrNode("Instrument.InsType", "EQUAL", "CFD")
        query.AddAttrNode("Portfolio.Name", "EQUAL", portfolio)
        query.AddAttrNode("valueDay", "GREATER_EQUAL", from_date)
        query.AddAttrNode("valueDay", "LESS_EQUAL", self.report_date)
        query.AddAttrNode("contract.counterparty.Name", "EQUAL", self.BROKER_FULL_NAME)

        for trade in query.Select():
            for payment in trade.Payments():
                if payment.Type() == "CFD Execution Fee":
                    fx_rate = get_fx_rate(
                        "USD",
                        payment.Currency().Name(),
                        get_fa_date(self.report_date, "%Y-%m-%d", "%d-%m-%Y"),
                    )
                    total_execution_fees += payment.Amount() / fx_rate

        return total_execution_fees

    def _is_correct_client(self, record):
        return record[self.COLUMN_CLIENT_ACCOUNT].startswith(
            "ABSA " + self.client_broker_account
        )

    def _write_synthetic_record(self, record):
        self.report_line = [
            record[self.COLUMN_REPORT_DATE_SYN],
            record[self.COLUMN_CLIENT_ACCOUNT],
            record[self.COLUMN_UNDERLYING_CODE],
            record[self.COLUMN_UNDERLYING_TICKER],
            record[self.COLUMN_UNDERLYING_NAME],
            record[self.COLUMN_UNDERLYING_CURRENCY],
            record[self.COLUMN_FUNDING_CURRENCY],
            record[self.COLUMN_QUANTITY],
            record[self.COLUMN_WEIGHTED_AVERAGE_PRICE],
            record[self.COLUMN_WEIGHTED_AVERAGE_AMOUNT],
            record[self.COLUMN_CLOSING_PRICE],
            record[self.COLUMN_CLOSING_AMOUNT],
            record[self.COLUMN_MTM],
            self._get_exec_rate(
                record[self.COLUMN_UNDERLYING_CURRENCY],
                record[self.COLUMN_FUNDING_CURRENCY],
            ),
            record[self.COLUMN_FEES],
            record[self.COLUMN_FUNDING],
            record[self.COLUMN_MTM_TOTAL],
            record[self.COLUMN_FX_RATE],
            record[self.COLUMN_MTM_TOTAL_USD],
        ]
        self.pnl_report_content.append(self.report_line)

    def _calculate_absa_funding(self, record):
        absa_spread = get_absa_rate(self.client_short_name)
        spread = float(record[self.COLUMN_BROKER_SPREAD])
        coef = 1 if spread > 0 else -1

        absa_rate = float(record[self.COLUMN_EFFECTIVE_RATE]) + absa_spread * coef
        fx_rate = get_fx_rate(
            "USD", record[self.COLUMN_FUNDING_CURRENCY], record[self.COLUMN_PAY_DATE]
        )
        day_count = self._get_day_count(record)

        absa_funding = self._get_absa_finding_amount(record, absa_rate, day_count)

        self.total_absa_funding += absa_funding / fx_rate

    def _write_funding_report_line(self, record):
        absa_spread = get_absa_rate(self.client_short_name)
        spread = float(record[self.COLUMN_BROKER_SPREAD])
        coef = 1 if spread > 0 else -1

        absa_rate = float(record[self.COLUMN_EFFECTIVE_RATE]) + absa_spread * coef
        fx_rate = get_fx_rate(
            "USD", record[self.COLUMN_FUNDING_CURRENCY], record[self.COLUMN_PAY_DATE]
        )
        day_count = self._get_day_count(record)

        absa_funding = self._get_absa_finding_amount(record, absa_rate, day_count)

        self.report_line = [
            record[self.COLUMN_REPORT_DATE],
            record[self.COLUMN_PAY_DATE],
            record[self.COLUMN_CLIENT_ACCOUNT],
            record[self.COLUMN_UNDERLYING_CODE],
            record[self.COLUMN_UNDERLYING_TICKER],
            record[self.COLUMN_UNDERLYING_NAME],
            record[self.COLUMN_FUNDING_CURRENCY],
            record[self.COLUMN_FUNDING_AMOUNT],
            record[self.COLUMN_DAYS],
            record[self.COLUMN_BASE_RATE],
            float(record[self.COLUMN_BROKER_SPREAD]) / 100,
            record[self.COLUMN_EFFECTIVE_RATE],
            absa_spread,
            absa_rate,
            day_count,
            record[self.COLUMN_BROKER_FUNDING],
            absa_funding,
            fx_rate,
            absa_funding / fx_rate,
        ]

        self.funding_report_content.append(self.report_line)

    def _get_absa_finding_amount(self, record, absa_rate, day_count):
        return (
            (
                -1
                * float(record[self.COLUMN_FUNDING_AMOUNT])
                * int(record[self.COLUMN_DAYS])
                * absa_rate
            )
            / 100
        ) / day_count

    @staticmethod
    def _is_cash_flow_settled(cash_flow):
        return cash_flow.AdditionalInfo().Settle_Type() == "Settled"

    def _get_client_account(self):
        alias_type = "PB_{}_Account".format(self.broker)
        alias = acm.FPartyAlias.Select01(
            'type="%s" and party=%s' % (alias_type, self.counterparty.Name()), True
        )

        if not alias:
            raise RuntimeError(
                "Counterparty {} has no alias mapping for broker {}".format(
                    self.counterparty.Name(), self.broker
                )
            )

        return alias.Name()

    def _is_correct_client(self, record):
        return record[self.COLUMN_CLIENT_ACCOUNT].startswith(
            "ABSA " + self.client_broker_account
        )

    @staticmethod
    def _get_exec_rate(underlying_curr, funding_curr):
        exchange_rates = get_exchange_rates()

        rate_by_both = exchange_rates.get((underlying_curr, funding_curr))
        rate_by_underlying_curr = exchange_rates.get(underlying_curr)
        rate_by_funding_curr = exchange_rates.get(funding_curr)

        return rate_by_both or rate_by_underlying_curr or rate_by_funding_curr or 0

    def _get_day_count(self, record):
        return int(record[self.COLUMN_DAY_COUNT].split("/")[-1])

    def _save_amount_to_depo(self, value, pay_date, leg):
        cash_flow = self._get_call_account_cash_flow(leg, str(pay_date))

        if not cash_flow:
            if round(value, 6) == 0:
                LOGGER.info("Skipping saving to call account value of {}", str(value))
                return

            cash_flow = CreateCashFlow(leg, "Fixed Amount", None, None, pay_date, value)
            SetAdditionalInfo(cash_flow, "PS_DepositType", self.field_name)
            cash_flow.Commit()

        else:
            cash_flow.FixedAmount(value)
            cash_flow.Commit()

        LOGGER.info(
            "Call Account {}: cash flow amount {} of type {} saved.".format(
                self.client_account.Name(), cash_flow.FixedAmount(), self.field_name
            )
        )

    def _get_reset_from_date(self):
        months_cfs = self._get_unsettled_call_account_cash_flows()
        months_cfs = sorted(months_cfs, key=lambda x: x.PayDate())

        return months_cfs[0].PayDate()

    def _get_unsettled_call_account_cash_flows(self):
        leg = self.client_account.Legs()[0]

        query = acm.CreateFASQLQuery("FCashFlow", "AND")
        query.AddAttrNode("Leg.Oid", "EQUAL", leg.Oid())
        query.AddAttrNode("CashFlowType", "EQUAL", "Fixed Amount")
        query.AddAttrNode(
            "AdditionalInfo.PS_DepositType", "EQUAL", self.field_name,
        )
        query.AddAttrNode("AdditionalInfo.Settle_Type", "NOT_EQUAL", "Settled")
        query.AddAttrNode("PayDate", "LESS_EQUAL", self.report_date)
        return query.Select()

    def _get_call_account_cash_flow(self, leg, input_date):
        query = acm.CreateFASQLQuery("FCashFlow", "AND")
        query.AddAttrNode("Leg.Oid", "EQUAL", leg.Oid())
        query.AddAttrNode("PayDate", "EQUAL", str(input_date))
        query.AddAttrNode("CashFlowType", "EQUAL", "Fixed Amount")
        query.AddAttrNode("AdditionalInfo.PS_DepositType", "EQUAL", self.field_name)

        cash_flows = query.Select()
        if cash_flows:
            return cash_flows[0]
        return None

    def _get_previous_cash_flow(self, leg, input_date):
        query = acm.CreateFASQLQuery("FCashFlow", "AND")
        query.AddAttrNode("PayDate", "LESS", str(input_date))
        query.AddAttrNode("Leg.Oid", "EQUAL", leg.Oid())
        query.AddAttrNode("CashFlowType", "EQUAL", "Fixed Amount")
        query.AddAttrNode("AdditionalInfo.PS_DepositType", "EQUAL", self.field_name)

        cash_flows = query.Select()
        if cash_flows:
            return sorted(cash_flows, key=lambda x: x.PayDate())[-1]
        return None


class SocGenTplSweeper(AbstractTplSweeper):
    COLUMN_CLIENT_ACCOUNT = "DPS Reference"
    COLUMN_FUNDING_AMOUNT = "Aggregate Notional Funding Amount"
    COLUMN_FUNDING_CURRENCY = "Funding Currency"
    COLUMN_UNDERLYING_CURRENCY = "Underlying Currency"
    COLUMN_DAY_COUNT = "Day Count Fraction"
    COLUMN_BROKER_SPREAD = "Spread"
    COLUMN_DAYS = "Nb of days"
    COLUMN_PAY_DATE = "End Date"
    COLUMN_REPORT_DATE = "Report Date"
    COLUMN_UNDERLYING_CODE = "Underlying Code"
    COLUMN_UNDERLYING_TICKER = "Underlying Identifier (Ticker)"
    COLUMN_UNDERLYING_NAME = "Underlying Name"
    COLUMN_BASE_RATE = "Relevant Rate"
    COLUMN_EFFECTIVE_RATE = "Effective Rate"
    COLUMN_BROKER_FUNDING = "Daily Aggregate Interest Amount"
    COLUMN_WEIGHTED_AVERAGE_PRICE = "Weighted Average Funding Price"
    COLUMN_WEIGHTED_AVERAGE_AMOUNT = "Weighted Average Notional Funding Amount"
    COLUMN_CLOSING_PRICE = "MTM Closing Price"
    COLUMN_CLOSING_AMOUNT = "MTM Notional Funding Amount"
    COLUMN_FEES = "Derivatives Execution Fee"
    COLUMN_MTM = "Unrealised MTM Performance"
    COLUMN_FUNDING = "Unrealised Funding Cost"
    COLUMN_REPORT_DATE_SYN = "Report date"
    COLUMN_QUANTITY = "Aggregate Opening Quantity"
    COLUMN_MTM_TOTAL_USD = "Daily MTM USD"
    COLUMN_MTM_TOTAL = "Daily MTM"
    COLUMN_FX_RATE = "FX Rate"
    COLUMN_LAST_RESET_PAY_DATE = "Last Reset Pay Date"
    BROKER_FULL_NAME = "SOCIETE GENERALE"


ael_variables = AelVariableHandler()
ael_variables.add(
    "start_date",
    label="Start Date",
    cls="string",
    default="Previous Business day",
    mandatory=True,
    alt="Date to run, custom date format 'YYYY-M-D'",
)
ael_variables.add(
    "end_date",
    label="End Date",
    cls="string",
    default="Previous Business day",
    mandatory=True,
)
ael_variables.add(
    "cp_alias", label="Party Alias", cls="string", default="SENQGLO", mandatory=True,
)
ael_variables.add(
    "broker", label="Broker", cls="string", default="SocGen", mandatory=True,
)
ael_variables.add(
    "file_dir",
    label="Directory",
    default=r"Y:\Jhb\FAReports\AtlasEndOfDay\PrimeClients\SOCGEN\${DATE}",
    mandatory=True,
    alt='A Directory with variable DATE ("$DATE")',
)
ael_variables.add(
    "funding_file", label="Funding File", default="Funding-cost", alt="",
)
ael_variables.add(
    "synthetic_file", label="Synthetic File", default="Daily-Synthetic-MtM", alt="",
)

ael_variables.add(
    "funding_sweeping_report",
    label="Funding Sweeping Report",
    default=r"/services/frontnt/Task/${CLIENT}_FundingSweepingReport_${RUN_DATE}.csv",
    alt="",
)
ael_variables.add(
    "pnl_sweeping_report",
    label="PnL Sweeping Report",
    default=r"/services/frontnt/Task/${CLIENT}_PnLSweepingReport_${RUN_DATE}.csv",
    alt="",
)


def get_latest_funding_file(file_dir, file_name, selected_date):
    if file_name:
        # directory
        dir_template = string.Template(file_dir)
        file_dir = dir_template.substitute(DATE=selected_date)

        # file names
        file_names = []
        for filename in os.listdir(file_dir):
            if file_name in filename and filename.endswith(".csv"):
                file_names.append(os.path.join(file_dir, filename))

        file_names = [
            file_name
            for file_name in file_names
            if is_int(file_name[-5]) and not is_int(file_name[-6])
        ]
        sorted(file_names, key=lambda x: int(x[-5]))

        if file_names:
            return file_names[-1]


def get_latest_client_file(file_dir, client, file_name, selected_date):
    if file_name:
        # directory
        dir_template = string.Template(file_dir)
        file_dir = dir_template.substitute(CLIENT=client, DATE=selected_date)

        file_names = []
        for filename in os.listdir(file_dir):
            if (
                file_name in filename
                and client in filename
                and filename.endswith(".csv")
                and not filename.startswith("absa_")
            ):
                file_names.append(os.path.join(file_dir, filename))

        if file_names:
            return file_names[-1]


def get_broker_sweeper_class(broker):
    trade_class_string = "{}TplSweeper".format(broker.replace(" ", ""))
    return getattr(sys.modules[os.path.basename(__file__)], trade_class_string)


def get_reporting_file_name(file_name, alias, input_date):
    path_template = string.Template(file_name)
    return path_template.substitute(CLIENT=alias, RUN_DATE=input_date.replace("-", ""),)


def ael_main(ael_dict):
    start_date = ael_dict["start_date"]
    end_date = ael_dict["end_date"]
    alias = ael_dict["cp_alias"]
    broker = ael_dict["broker"]

    if start_date == "Previous Business day":
        start_date = get_previous_weekday(acm.Time().DateNow())

    if end_date == "Previous Business day":
        end_date = get_previous_weekday(acm.Time().DateNow())

    LOGGER.info(
        "Offshore sweeping started for {} on date {} for broker {}.".format(
            alias, start_date, broker
        )
    )

    for input_date in get_workdays_from_range(start_date, end_date):
        funding_file = get_latest_funding_file(
            ael_dict["file_dir"], ael_dict["funding_file"], input_date,
        )
        synthetic_file = get_latest_client_file(
            ael_dict["file_dir"],
            ael_dict["cp_alias"],
            ael_dict["synthetic_file"],
            input_date,
        )

        if funding_file and synthetic_file:
            # Sweep tpl and funding from files
            sweeper_class = get_broker_sweeper_class(broker)
            sweeper = sweeper_class(
                funding_file, synthetic_file, alias, broker, input_date,
            )
            sweeper.sweep_funding()
            sweeper.sweep_tpl()

            funding_file_path = get_reporting_file_name(
                ael_dict["funding_sweeping_report"], alias, input_date
            )
            pnl_file_path = get_reporting_file_name(
                ael_dict["pnl_sweeping_report"], alias, input_date
            )

            funding_report = OffshoreFundingSweepingReport(
                funding_file_path, sweeper.get_funding_data()
            )
            funding_report.create_report()

            pnl_report = OffshorePnLSweepingReport(
                pnl_file_path, sweeper.get_tpl_data()
            )
            pnl_report.create_report()

        else:
            LOGGER.error(
                "Missing files for {} on {}".format(ael_dict["cp_alias"], input_date)
            )

    if LOGGER.msg_tracker.warnings_counter:
        LOGGER.warning("Completed with some warnings.")
    else:
        LOGGER.info("Completed successfully.")
