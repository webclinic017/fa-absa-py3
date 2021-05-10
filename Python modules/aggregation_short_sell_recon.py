"""
Module
    aggregation_short_sell_recon.py

Description


History
Date          Developer          Description
--------------------------------------------------------------------------------
2020-10-02    Marcus Ambrose     Implement
"""

import acm

from at_ael_variables import AelVariableHandler
from at_transaction_history import TransactionHistoryHelper
from at_email import EmailHelper
from at_logging import getLogger


LOGGER = getLogger(__name__)
MAIL_SUBJECT = "Bond Aggregation ShortSell Reversion Failure!"


class AggregationShortSellChecker:
    def get_unreverted_bonds(self):
        active_filters = self._get_active_filters()
        restricted_bonds = self._get_bond_instruments(active_filters)
        return self._get_unreverted_bonds(restricted_bonds)

    def _get_active_filters(self):
        active_filters = set()

        for task in acm.FAelTask.Select('moduleName = "FAggregation"'):
            task_params = task.ParametersText().split(";")
            for param in task_params:
                if param.startswith("aggrule_filters"):
                    for condition in param.split("=")[1].split(","):
                        if self._is_bond_filter(condition):
                            active_filters.update([condition])
        return active_filters

    @staticmethod
    def _is_bond_filter(filter_id):
        trade_filter = acm.FTradeSelection[filter_id]
        for condition in trade_filter.FilterCondition():
            if (
                str(condition[2]) == "Instrument.Type"
                and str(condition[3]) == "equal to"
                and str(condition[4]) == "Bond"
            ):
                return True
        return False

    @staticmethod
    def _get_bond_instruments(filters):
        bond_instruments = set()
        for trade_filter in filters:
            instruments = [
                trade.Instrument().Name()
                for trade in acm.FTradeSelection[trade_filter].Trades()
                if trade.Instrument().ShortSell() == "Forbidden"
            ]
            bond_instruments.update(instruments)
        return bond_instruments

    def _get_unreverted_bonds(self, bonds):
        unreverted_bonds = []
        for bond in bonds:
            trans_hist_helper = TransactionHistoryHelper(
                "Instrument", acm.FInstrument[bond].Oid()
            )
            if self.is_bond_unreverted(
                trans_hist_helper.get_latest_transaction_details()
            ):
                unreverted_bonds.append(bond)
        return unreverted_bonds

    @staticmethod
    def is_bond_unreverted(last_update):
        return (
            "Short Sell" in last_update
            and last_update["Update User"] == "AGGREGATION"
            and last_update["Short Sell"]["New"] == "Allowed"
        )


def send_mail(recipients, unreverted_bonds):
    email_helper = EmailHelper(
        format_email_data(unreverted_bonds), MAIL_SUBJECT, recipients,
    )
    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()

    try:
        email_helper.send()
    except Exception as exc:
        LOGGER.error("Error while sending e-mail: {}".format(exc))


def format_email_data(instrument_list):
    msg = "Hello RTB Core and Prime Services, <br /><br />"
    msg += "Aggregation failed to revert the short sell on total of {} bond instruments.  ".format(
        len(instrument_list)
    )
    msg += "Short sell attribute should be set to Forbidden for these instruments.<br /><br />"

    for instrument_name in instrument_list:
        msg += "{}<br />".format(instrument_name)

    msg += "<br />"
    msg += "Best regards,<br />{0}".format("CIB Africa TS Dev - Prime and Equities")
    msg += (
        "<br /><br /><br /><small>This is an automated message from '%s'.py</small>"
        % __name__
    )

    return msg


ael_variables = AelVariableHandler()
ael_variables.add(
    "recipients",
    label="Email Addresses",
    cls="string",
    default="CIBAfricaFrontCore@absa.africa,CIBAfricaPrimeandEquitiesDev@absa.africa",
    mandatory=True,
    multiple=True,
    alt="Email address failed report will be set to",
)


def ael_main(ael_dict):
    LOGGER.info(
        "Starting check for unreverted short sell restricted bonds post aggregation..."
    )

    recipients = ael_dict["recipients"]
    short_sell_checker = AggregationShortSellChecker()
    unreverted_bonds = short_sell_checker.get_unreverted_bonds()

    if len(unreverted_bonds) > 0:
        LOGGER.info(
            "A total of {} bonds were not reverted back to forbidden".format(
                len(unreverted_bonds)
            )
        )
        LOGGER.info("Send mail to the following recipients: {}")
        send_mail(recipients, unreverted_bonds)

    LOGGER.info("Completed")
