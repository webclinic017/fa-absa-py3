import time
from datetime import datetime

import acm

from at_ael_variables import AelVariableHandler
from pb_storage_fund import PrimeBrokerageFundStorage
from pb_quirk import PortfolioSwapBasedQuirk
from at_logging import getLogger

LOGGER = getLogger()
TODAY = acm.Time.DateToday()

ATTR_ID_FIELD_NAME = 'PSSweepBaseDay'
ATTR_ID_NAME = 'ps_sweeping_base_day'

INVALID_DATE_FORMATS = ['%Y/%m/%d', '%d/%m/%Y', '%d-%m-%Y']

ael_variables = AelVariableHandler()

ael_variables.add(
    name="dry_run",
    label="Dry Run",
    cls="bool",
    collection=(True, False),
    default="bool",
    mandatory=False,
    multiple=False,
    alt="Tell which Primary Brokerage funds are to be removed but do not remove them yet"
)


def correct_date_format(pb_fund, dry_run):
    """Correct PSwap sweep base date formats"""
    quirk = pb_fund.quirks.get(ATTR_ID_NAME)
    if isinstance(quirk, PortfolioSwapBasedQuirk):
        for acm_portfolio_swap in pb_fund.get_product_type_pswaps():
            portfolio_swap_addinfo = acm_portfolio_swap.AdditionalInfo()
            try:
                portfolio_swap_addinfo.PSSweepBaseDay()
            except RuntimeError as err:
                ps_sweep_base_date = convert_sweep_base_date(str(err))
                # Set the property value value/date
                if ps_sweep_base_date and not dry_run:
                    portfolio_swap_addinfo.SetProperty(ATTR_ID_FIELD_NAME, ps_sweep_base_date)
                    LOGGER.info("Sweep base date corrected to %s for PB fund %s, ACM portfolio swap %s",
                                ps_sweep_base_date, pb_fund.fund_id, acm_portfolio_swap.Name())
                else:
                    LOGGER.warning("Sweep base date should be corrected to %s for PB fund %s, "
                                   "ACM portfolio swap %s", ps_sweep_base_date, pb_fund.fund_id,
                                   acm_portfolio_swap.Name())


def convert_sweep_base_date(error_message):
    """Extract the date from error_message and convert it to YYYY-MM-DD format.

    :param error_message: str like "expected datetime, got '2018/10/17'"
    """

    # Extract the date from the exception message and strip it off apostrophes
    ps_sweep_base_date = error_message.split()[3].replace("'", "")

    for invalid_date_format in INVALID_DATE_FORMATS:
        try:
            return datetime.strptime(ps_sweep_base_date, invalid_date_format).strftime("%Y-%m-%d")
        except ValueError:
            LOGGER.warning("Swap base does not have the %s format", invalid_date_format)

    LOGGER.error("Swap base date will not be changed, none of date formats expected: %s", ps_sweep_base_date)


def is_decommissioned(pb_fund):
    """Determine whether Primary Brokerage Fund is decommissioned or not"""
    is_decommissioned = False

    instrument_name = pb_fund.call_account
    acm_instrument = acm.FInstrument[instrument_name]

    if acm_instrument is not None:
        trades = acm_instrument.Trades()
        ignored_statuses = ["Simulated", "Terminated", "Void"]
        relevant_trades = [trade for trade in trades
                           if trade.Status() not in ignored_statuses]
        if len(relevant_trades) != 1:
            is_decommissioned = True
            LOGGER.info("Instrument '{0}' does not have "
                        "exactly one relevant trade! It was decommissioned. "
                        "Scheduling it to be removed from PB funds storage".format(acm_instrument.Name()))

    return is_decommissioned


def remove_fund_from_storage(pb_fund_storage, fund_id, dry_run):
    """Remove decommissioned Primary Brokerage fund from Primary Brokerage Funds Storage"""
    if not dry_run:
        pb_fund_storage.delete_fund(fund_id)
        LOGGER.info("Deleting PB fund %s from Primary Brokerage Funds Storage", fund_id)
        pb_fund_storage.clean_up()
        pb_fund_storage.save()
    else:
        LOGGER.warning("PB fund %s should be deleted from Primary Brokerage Funds Storage", fund_id)


def ael_main(ael_dict):
    """ Clean up Primary Brokerage Funds Storage"""
    start = time.time()

    pb_fund_storage = PrimeBrokerageFundStorage()
    pb_fund_storage.load()

    dry_run = ael_dict["dry_run"]

    for fund_id in sorted(pb_fund_storage.stored_funds):
        pb_fund = pb_fund_storage.load_fund(fund_id)

        correct_date_format(pb_fund, dry_run)
        if is_decommissioned(pb_fund):
            remove_fund_from_storage(pb_fund_storage, fund_id, dry_run)

    end = time.time()

    LOGGER.info("Completed successfully in %s", end - start)
