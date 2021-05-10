"""-----------------------------------------------------------------------------
Run Monthly to settle offshore cash flows on broker reset date.

HISTORY
================================================================================
Date           Developer          Description
--------------------------------------------------------------------------------
2020-11-20     Marcus Ambrose     Implemented
-----------------------------------------------------------------------------"""
import acm

from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from PS_Functions import SetAdditionalInfo
from PS_CallAccountSweeperFunctions import (
    get_call_account,
    get_brokers_call_account,
)
from pb_offshore_cfd_utils import get_previous_weekday

LOGGER = getLogger(__name__)


class MonthlyReset(object):
    ACCOUNTING_CURRENCY = "USD"

    def __init__(self, client_short_name, broker, reset_date):
        self.client_short_name = client_short_name
        self.reset_date = reset_date
        self.broker = broker

        self.deposit_type = "PB_{}_CFD_TPL".format(self.broker)
        self.client_account = get_call_account(
            self.client_short_name, self.ACCOUNTING_CURRENCY
        )
        self.broker_account = get_brokers_call_account(
            self.client_short_name, self.ACCOUNTING_CURRENCY, self.broker
        )

    def perform_reset(self):
        self._settle_client_account()
        self._settle_broker_account()

    def _settle_client_account(self):
        cash_flows = self._get_unsettled_call_account_cash_flows(self.client_account)
        self._settle_cash_flows(cash_flows)

    def _settle_broker_account(self):
        cash_flows = self._get_unsettled_call_account_cash_flows(self.broker_account)
        self._settle_cash_flows(cash_flows)

    def _get_unsettled_call_account_cash_flows(self, account):
        leg = account.Legs()[0]

        query = acm.CreateFASQLQuery("FCashFlow", "AND")
        query.AddAttrNode("Leg.Oid", "EQUAL", leg.Oid())
        query.AddAttrNode("CashFlowType", "EQUAL", "Fixed Amount")
        query.AddAttrNode(
            "AdditionalInfo.PS_DepositType", "EQUAL", self.deposit_type,
        )
        query.AddAttrNode("AdditionalInfo.Settle_Type", "NOT_EQUAL", "Settled")
        query.AddAttrNode("PayDate", "LESS_EQUAL", self.reset_date)

        return query.Select()

    @staticmethod
    def _settle_cash_flows(call_account_cash_flows):
        for cash_flow in call_account_cash_flows:
            SetAdditionalInfo(cash_flow, "Settle_Type", "Settled")


ael_variables = AelVariableHandler()
ael_variables.add(
    "date",
    label="Date",
    cls="string",
    default="Previous Business day",
    mandatory=True,
    alt="Date to run, custom date format 'YYYY-M-D'",
)
ael_variables.add(
    "client_short_name", label="Party Alias", cls="string", mandatory=True,
)
ael_variables.add(
    "broker", label="Broker", cls="string", mandatory=True,
)


def ael_main(ael_dict):
    reset_date = ael_dict["date"]
    client_short_name = ael_dict["client_short_name"]
    broker = ael_dict["broker"]

    if reset_date == "Previous Business day":
        reset_date = get_previous_weekday(acm.Time().DateNow())

    LOGGER.info("Reset process starter for the {}".format(reset_date))

    processor = MonthlyReset(client_short_name, broker, reset_date)
    processor.perform_reset()

    LOGGER.info("Completed successfully.")
