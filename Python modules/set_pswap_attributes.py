"""
Add some additional infos to the current
prime brokerage portfolio swaps and trades.

Requested by:       IT BTB
Developer:          Peter Basista
Code reviewer:      ?
CR:                 ?
Deployment date:    2015-06-11
"""
from datetime import datetime as dt
import sys

import acm
from at_addInfo import save as save_additional_info
from at_ael_variables import AelVariableHandler
from PS_Functions import (get_instrument_trade,
                          get_pb_call_account,
                          get_pb_collateral_portfolio,
                          get_pb_fund_counterparties,
                          get_pb_fund_pswaps,
                          get_pb_fund_shortname,
                          get_pb_loan_account,
                          get_pb_reporting_portfolio,
                          get_pb_trade_ff_flag,
                          NotExactlyOneTrade)


class PortfolioLookupError(RuntimeError):
    """
    Base class used for exceptions which could be raised
    during the portfolio look-up.
    """
    pass


class NoSuchPortfolio(PortfolioLookupError):
    """
    Custom exception class which indicates that
    it was not possible to look up the provided portfolio by name.
    """
    def __init__(self, portfolio_name):
        exception_message = ("Portfolio '{0}' "
                             "does not seem to exist.").format(
                                 portfolio_name)
        super(NoSuchPortfolio, self).__init__(exception_message)


class NoFundingPortfolio(PortfolioLookupError):
    """
    Custom exception class which indicates that
    the provided portfolio swap does not have its funding portfolio set.
    """
    def __init__(self, portfolio_swap_name):
        exception_message = ("Portfolio swap '{0}' "
                             "does not have its funding "
                             "portfolio set!").format(
                                 portfolio_swap_name)
        super(NoFundingPortfolio, self).__init__(exception_message)


class EmptyAdditionalInfoCRLink(PortfolioLookupError):
    """
    Custom exception class which indicates that
    an additional info which links the on-tree portfolio
    to its off-tree counterpart in the CR subtree is empty.
    """
    def __init__(self, portfolio_name):
        exception_message = ("Portfolio '{0}' "
                             "does not have any value "
                             "for the additional info "
                             "'PS_MirrorCRBook' set!").format(
                                 portfolio_name)
        super(EmptyAdditionalInfoCRLink, self).__init__(exception_message)


class NoPortfolioProvided(PortfolioLookupError):
    """
    Custom exception class which indicates that no portfolio
    has been provided to the lookup function.
    """
    def __init__(self):
        exception_message = ("No portfolio has been provided, "
                             "so no lookup could have been done.")
        super(NoPortfolioProvided, self).__init__(exception_message)


class NotWithinTheReportingPortfolioTree(PortfolioLookupError):
    """
    Custom exception class which indicates that a portfolio
    is not a descendant of the main client reporting portfolio.
    """
    def __init__(self, portfolio_name, cr_portfolio_name):
        exception_message = ("The portfolio '{0}' is not "
                             "a descendant of the main "
                             "client reporting portfolio '{1}'.").format(
                                 portfolio_name,
                                 cr_portfolio_name)
        super(NotWithinTheReportingPortfolioTree, self).__init__(
            exception_message)


class MoreThanOneParentLink(PortfolioLookupError):
    """
    Custom exception class which indicates that a portfolio
    has more than one parent link.
    """
    def __init__(self, portfolio_name):
        exception_message = ("The portfolio '{0}' has "
                             "more than one parent link!").format(
                                 portfolio_name)
        super(MoreThanOneParentLink, self).__init__(exception_message)


class NoOwnerPortfolio(PortfolioLookupError):
    """
    Custom exception class which indicates that a portfolio link
    does not have the owner portfolio set.
    """
    def __init__(self, portfolio_name):
        exception_message = ("The portfolio '{0}' has a member link "
                             "which does not have the owner "
                             "portfolio set.").format(
                                 portfolio_name)
        super(NoOwnerPortfolio, self).__init__(exception_message)


ael_variables = AelVariableHandler()
ael_variables.add("portfolio_swaps_qf",
                  label="Portfolio Swaps QF",
                  alt=("A query folder containing the Portfolio Swaps "
                       "to be updated. All the trades "
                       "which are in funding portfolios "
                       "of these portfolio swaps "
                       "will be updated as well."),
                  cls=acm.FStoredASQLQuery,
                  collection=acm.FStoredASQLQuery.Select(
                      "subType='FInstrument'"))
ael_variables.add_bool("update_all_active_pswaps",
                       label=("Update all active prime brokerage "
                              "portfolio swaps"),
                       alt=("Update all the portfolio swaps "
                            "of all the currently active "
                            "prime brokerage funds."))
ael_variables.add_bool("use_counterparty_attributes",
                       label="Utilize the counterparty attributes",
                       alt=("Make use of the attributes which might have "
                            "already been set on the funds' counterparties. "
                            "Useful mainly for copying the metadata "
                            "to the CFD portfolio swaps."))
ael_variables.add("transaction_size",
                  label="Transaction size",
                  cls="int",
                  alt=("The maximum number of trades which will be "
                       "committed in one transaction."))
ael_variables.add_output_file("log_file_path",
                              label="Log file path",
                              alt=("A path to the log file "
                                   "where the detailed information "
                                   "about what has been done "
                                   "will be printed. If not specified, "
                                   "this information will be printed "
                                   "to the standard output."))


def determine_sweeping_class(portfolio_swap_name):
    """
    Return the best guess on the sweeping class of a portfolio swap
    based on its name and its funding portfolio's name.
    """
    sweeping_class = "Unknown"
    portfolio_swap_name = portfolio_swap_name.upper()
    if ("_REPOBOND" in portfolio_swap_name or
            "_GOVIBOND" in portfolio_swap_name):
        sweeping_class = "Government bonds"
    elif "_CORPBOND" in portfolio_swap_name:
        sweeping_class = "Corporate bonds"
    elif "_CE" in portfolio_swap_name:
        sweeping_class = "Cash equity"
    elif "_MONEYMARKET" in portfolio_swap_name:
        sweeping_class = "Money market"
    elif "_YIELDX" in portfolio_swap_name:
        sweeping_class = "YieldX exchange"
    elif "_SAFEX" in portfolio_swap_name:
        sweeping_class = "SAFEX exchange"
    elif "_IRS" in portfolio_swap_name:
        sweeping_class = "Swaps"
    elif "_FRA" in portfolio_swap_name:
        sweeping_class = "FRAs"
    elif "_CFD" in portfolio_swap_name:
        sweeping_class = "CFDs"
    elif "_OTCFIOPT" in portfolio_swap_name:
        sweeping_class = "FI Options"
    return sweeping_class


def determine_fully_funded_flag(portfolio_swap_name):
    """
    Return the best guess on the fully funded flag
    of a portfolio swap based on its name.
    """
    portfolio_swap_name = portfolio_swap_name.upper()
    if "_CFD" in portfolio_swap_name:
        return "No" # All CFD portfolio swpas are supposed to be financed.
    elif "_FF" in portfolio_swap_name:
        return "Yes"
    else:
        return "No"


def get_main_reporting_portfolio(acm_portfolio):
    """
    Return an ancestor of the provided portfolio
    which is the direct descendant of the 'PB_CR_LIVE' portfolio.
    If no such ancestor can be found, raise an exception.
    """
    if not acm_portfolio:
        raise NoPortfolioProvided()
    # FIXME: Hardcoded
    desired_parent_portfolio = acm.FPhysicalPortfolio["PB_CR_LIVE"]
    # Using a different variable to have the original portfolio available.
    parent = acm_portfolio
    found = False
    while not found:
        current_portfolio = parent
        member_links = current_portfolio.MemberLinks()
        parent_links = [link for link in member_links
                        if link.MemberPortfolio() == current_portfolio]
        if not parent_links:
            raise NotWithinTheReportingPortfolioTree(
                acm_portfolio.Name(),
                desired_parent_portfolio.Name())
        if len(parent_links) > 1:
            raise MoreThanOneParentLink(acm_portfolio.Name())
        # From now on, we can be sure that len(parent_links) == 1
        parent = parent_links[0].OwnerPortfolio()
        if not parent:
            raise NoOwnerPortfolio(current_portfolio.Name())
        found = parent == desired_parent_portfolio
    return current_portfolio


def get_collateral_portfolio(fund_id):
    """
    Return a portfolio which is supposed to be
    the main collateral portfolio of a Prime Brokerage fund
    with the provided ID.
    If no such portfolio exists, raise an exception.
    """
    portfolio_name = "PB_COLL_{0}_CR".format(fund_id)
    portfolio = acm.FPhysicalPortfolio[portfolio_name]
    if not portfolio:
        raise NoSuchPortfolio(portfolio_name)
    return portfolio


def get_cfd_cr_portfolio(acm_portfolio_swap,
                         use_counterparty_attributes):
    """
    Return a portfolio which is supposed to be
    the CR portfolio for off-tree CFD trades
    which are counterparts to the stock trades
    in the provided portfolio swap's funding portfolio.

    If no such portfolio exists, raise an exception.
    """
    funding_portfolio = acm_portfolio_swap.FundPortfolio()
    if not funding_portfolio:
        raise NoFundingPortfolio(acm_portfolio_swap.Name())
    portfolio = funding_portfolio.AdditionalInfo().PS_MirrorCRBook()
    if not portfolio and use_counterparty_attributes:
        print("Portfolio swap: '{0}'".format(acm_portfolio_swap.Name()))
        trade = get_instrument_trade(acm_portfolio_swap)
        counterparty = trade.Counterparty()
        reporting_portfolio = get_pb_reporting_portfolio(counterparty)
        for cr_portfolio in reporting_portfolio.AllPhysicalPortfolios():
            if cr_portfolio.Name().find("CFD") > 0:
                portfolio = cr_portfolio
                break
    if not portfolio:
        raise EmptyAdditionalInfoCRLink(funding_portfolio.Name())
    return portfolio


def update_portfolio_swap(acm_portfolio_swap,
                          sweeping_class,
                          fully_funded,
                          log_file):
    """
    Update the provided portfolio swap's additional infos
    based on the type of trades it holds positions for.
    """
    portfolio_swap_name = acm_portfolio_swap.Name()
    # Using sys.stdout.write, because we do not want
    # to implicitly print the newline character at the end.
    sys.stdout.write("Updating portfolio swap '{0}' ... ".format(
        portfolio_swap_name))

    save_additional_info(acm_portfolio_swap,
                         "PB_Sweeping_Class",
                         sweeping_class)
    save_additional_info(acm_portfolio_swap,
                         "PB_PS_Fully_Funded",
                         fully_funded)
    print("done.")
    print("Portfolio swap '{0}' updated.".format(
        portfolio_swap_name), file=log_file)


def already_updated(acm_trade, fully_funded):
    """
    Return True if the provided acm trade
    already has its fully funded flag set to the desired value.
    Otherwise return False.
    """
    if get_pb_trade_ff_flag(acm_trade) == fully_funded:
        return True
    else:
        return False


def update_trades(acm_portfolio,
                  fully_funded,
                  log_file,
                  transaction_size=1000):
    """
    Update the trades in the provided portfolio
    and set their attributes according to
    the the provided parameters.

    Update at most 'transaction_size' trades in one transaction.
    """
    if not acm_portfolio:
        warning_message = ("Warning: No portfolio has been provided, "
                           "so no trades could have been updated.")
        print(warning_message, file=log_file)
        print(warning_message, file=sys.stderr)
        return
    trades = acm_portfolio.Trades()
    number_of_trades = len(trades)
    portfolio_name = acm_portfolio.Name()
    print("Updating {0} trades in portfolio '{1}'".format(
        number_of_trades,
        portfolio_name))

    i = 0
    chunk_of_trades = trades[:transaction_size]
    while chunk_of_trades:
        chunk_size = len(chunk_of_trades)
        try:
            acm.BeginTransaction()
            for acm_trade in chunk_of_trades:
                if already_updated(acm_trade, fully_funded):
                    continue
                save_additional_info(acm_trade,
                                     "PB_Fully_Funded",
                                     fully_funded)
            acm.CommitTransaction()
            info_message = "Updated {0} trades up to {1}.th.".format(
                chunk_size,
                i * transaction_size + chunk_size)
            print(info_message, file=log_file)
            print(info_message)
        except RuntimeError as exc:
            acm.AbortTransaction()
            error_message = ("Error: Unable to commit trades from {0} "
                             "(inclusive) to {1} (inclusive) "
                             "in portfolio {2}. Reason: {3}").format(
                                 i * transaction_size + 1,
                                 i * transaction_size + chunk_size,
                                 acm_portfolio.Name(),
                                 str(exc))
            print(error_message, file=log_file)
            print(error_message, file=sys.stderr)
            #raise
        i += 1
        chunk_of_trades = trades[
            i * transaction_size:(i + 1) * transaction_size]
    info_message = "Updated all {0} trades in portfolio '{1}'.".format(
        number_of_trades,
        portfolio_name)
    print(info_message, file=log_file)
    print(info_message)


def update_time_series(old_time_series_spec,
                       new_time_series_spec,
                       acm_portfolio,
                       acm_portfolio_swap,
                       log_file):
    """
    Copy all the entries from the provided old time series
    which are linked to the provided portfolio
    into a new time series and link them
    to the provided portfolio swap.
    """
    selection_string = "timeSeriesSpec = {0} and recaddr = {1}".format(
        old_time_series_spec.Oid(), acm_portfolio.Oid())
    old_values = acm.FTimeSeries.Select(selection_string)
    number_of_values = len(old_values)
    new_tss_oid = new_time_series_spec.Oid()
    pswap_oid = acm_portfolio_swap.Oid()
    sys.stdout.write(("Copying {0} values from time series '{1}' "
                      "to time series '{2}'... ").format(
                          number_of_values,
                          old_time_series_spec.FieldName(),
                          new_time_series_spec.FieldName()))
    acm.BeginTransaction()
    try:
        for value in old_values:
            cloned_value = value.Clone()
            cloned_value.TimeSeriesSpec(new_tss_oid)
            cloned_value.Recaddr(pswap_oid)
            cloned_value.Commit()
        acm.CommitTransaction()
    except RuntimeError as exc:
        print("NOT done.")
        acm.AbortTransaction()
        error_message = ("Error: Unable to commit values "
                         "in a time series '{0}'. "
                         "Reason: {1}").format(
                             new_time_series_spec.FieldName(),
                             str(exc))
        print(error_message, file=log_file)
        print(error_message, file=sys.stderr)
        return
    print("done.")
    print(("Copied {0} values "
                        "from time series '{1}' "
                        "to time series '{2}'.").format(
                            number_of_values,
                            old_time_series_spec.FieldName(),
                            new_time_series_spec.FieldName()), file=log_file)


def update_counterparty(acm_counterparty,
                        acm_call_account,
                        acm_loan_account,
                        acm_reporting_portfolio,
                        acm_collateral_portfolio,
                        log_file):
    """
    Update the provided counterparty's additional infos
    based on the supplied parameters.
    """
    if not acm_counterparty:
        if acm_call_account:
            call_account_name = acm_call_account.Name()
        else:
            call_account_name = "Unknown"
        if acm_loan_account:
            loan_account_name = acm_loan_account.Name()
        else:
            loan_account_name = "Unknown"
        if acm_reporting_portfolio:
            reporting_portfolio_name = acm_reporting_portfolio.Name()
        else:
            reporting_portfolio_name = "Unknown"
        if acm_collateral_portfolio:
            collateral_portfolio_name = acm_collateral_portfolio.Name()
        else:
            collateral_portfolio_name = "Unknown"
        warning_message = ("Warning: No counterparty has been provided. "
                           "NOT setting the other "
                           "supplied attributes:\n"
                           "Call account: {0}\n"
                           "Loan account: {1}\n"
                           "Reporting portfolio: {2}\n"
                           "Collateral portfolio: {3}\n").format(
                               call_account_name,
                               loan_account_name,
                               reporting_portfolio_name,
                               collateral_portfolio_name)
        print(warning_message, file=log_file)
        print(warning_message, file=sys.stderr)
        return
    counterparty_name = acm_counterparty.Name()
    fund_attributes = (acm_counterparty,
                       acm_call_account,
                       acm_loan_account,
                       acm_reporting_portfolio,
                       acm_collateral_portfolio)
    printable_fund_attributes = format_fund_attributes(fund_attributes)
    print(("Setting the following "
                        "attributes:\n{0}").format(
                            printable_fund_attributes), file=log_file)
    # Using sys.stdout.write, because we do not want
    # to implicitly print the newline character at the end.
    sys.stdout.write("Updating counterparty '{0}' ... ".format(
        counterparty_name))
    if acm_call_account:
        save_additional_info(acm_counterparty,
                             "PB_Call_Account",
                             acm_call_account)
    if acm_loan_account:
        save_additional_info(acm_counterparty,
                             "PB_Loan_Account",
                             acm_loan_account)
    if acm_reporting_portfolio:
        save_additional_info(acm_counterparty,
                             "PB_Reporting_Prf",
                             acm_reporting_portfolio)
    if acm_collateral_portfolio:
        save_additional_info(acm_counterparty,
                             "PB_Collateral_Prf",
                             acm_collateral_portfolio)
    print("done.")
    print("Counterparty '{0}' updated.".format(
        counterparty_name), file=log_file)


def get_pswap_attributes(acm_portfolio_swap,
                         use_counterparty_attributes,
                         log_file):
    """
    Get the relevant attributes about the provided portfolio swap.
    """
    portfolio_swap_name = acm_portfolio_swap.Name()
    sweeping_class = determine_sweeping_class(portfolio_swap_name)
    fully_funded = determine_fully_funded_flag(portfolio_swap_name)
    print(("Portfolio swap '{0}' has been classified "
                        "as '{1}', FF={2}").format(portfolio_swap_name,
                                                   sweeping_class,
                                                   fully_funded), file=log_file)
    funding_portfolio = acm_portfolio_swap.FundPortfolio()
    if sweeping_class == "CFDs":
        funding_portfolio = get_cfd_cr_portfolio(
            acm_portfolio_swap,
            use_counterparty_attributes)
    if not funding_portfolio:
        warning_message = ("Warning: portfolio swap '{0}' "
                           "does not have its funding "
                           "portfolio set!").format(
                               portfolio_swap_name)
        print(warning_message, file=log_file)
        print(warning_message, file=sys.stderr)
    pswap_attributes = (funding_portfolio,
                        sweeping_class,
                        fully_funded)
    return pswap_attributes


def format_fund_attributes(fund_attributes):
    """
    Return a string describing the provided fund attributes.
    """
    (counterparty,
     call_account,
     loan_account,
     reporting_portfolio,
     collateral_portfolio) = fund_attributes
    if counterparty:
        counterparty_name = counterparty.Name()
    else:
        counterparty_name = "Unknown"
    if call_account:
        call_account_name = call_account.Name()
    else:
        call_account_name = "Unknown"
    if loan_account:
        loan_account_name = loan_account.Name()
    else:
        loan_account_name = "Unknown"
    if reporting_portfolio:
        reporting_portfolio_name = reporting_portfolio.Name()
    else:
        reporting_portfolio_name = "Unknown"
    if collateral_portfolio:
        collateral_portfolio_name = collateral_portfolio.Name()
    else:
        collateral_portfolio_name = "Unknown"
    output_string = ("Counterparty: {0}\n"
                     "Call account: {1}\n"
                     "Loan account: {2}\n"
                     "Reporting portfolio: {3}\n"
                     "Collateral portfolio: {4}\n").format(
                         counterparty_name,
                         call_account_name,
                         loan_account_name,
                         reporting_portfolio_name,
                         collateral_portfolio_name)
    return output_string

def get_fund_attributes(acm_portfolio_swap, acm_funding_portfolio, log_file):
    """
    Get the relevant attributes about the prime brokerage fund
    from the provided portfolio swap.
    """
    try:
        trade = get_instrument_trade(acm_portfolio_swap)
        counterparty = trade.Counterparty()
        fund_id = get_pb_fund_shortname(counterparty)
    except NotExactlyOneTrade as exc:
        exception_message = ("Unable to find the only relevant trade "
                             "of the portfolio swap '{0}'. "
                             "Error message:\n{1}").format(
                                 acm_portfolio_swap.Name(), exc)
        print(exception_message, file=log_file)
        print(exception_message, file=sys.stderr)
        counterparty = None
        fund_id = "Unknown"
    if acm_funding_portfolio:
        call_account = acm_funding_portfolio.AdditionalInfo().PSClientCallAcc()
    else:
        call_account = None
    try:
        reporting_portfolio = get_main_reporting_portfolio(
            acm_funding_portfolio)
    except PortfolioLookupError as exc:
        exception_message = ("Unable to find the main reporting portfolio "
                             "of the fund '{0}'. "
                             "Error message:\n{1}").format(fund_id, exc)
        print(exception_message, file=log_file)
        print(exception_message, file=sys.stderr)
        reporting_portfolio = None
    if reporting_portfolio:
        loan_account = reporting_portfolio.AdditionalInfo().PSClientCallAcc()
    else:
        loan_account = None
    try:
        collateral_portfolio = get_collateral_portfolio(fund_id)
    except PortfolioLookupError as exc:
        exception_message = ("Unable to find the collateral portfolio "
                             "of the fund '{0}'. "
                             "Error message:\n{1}").format(fund_id, exc)
        print(exception_message, file=log_file)
        print(exception_message, file=sys.stderr)
        collateral_portfolio = None
    fund_attributes = (counterparty,
                       call_account,
                       loan_account,
                       reporting_portfolio,
                       collateral_portfolio)
    printable_fund_attributes = format_fund_attributes(fund_attributes)
    print(("Fund '{0}' has been classified as having "
                        "the following attributes:\n{1}").format(
                            fund_id, printable_fund_attributes), file=log_file)
    fund_attributes = (fund_id,
                       counterparty,
                       call_account,
                       loan_account,
                       reporting_portfolio,
                       collateral_portfolio)
    return fund_attributes


def get_current_fund_attributes(acm_counterparty):
    """
    Return the current attributes of a Prime Brokerage fund
    represented by the provided counterparty.

    If no attribute is currently set, return None.
    """
    fund_id = get_pb_fund_shortname(acm_counterparty)
    call_account = get_pb_call_account(acm_counterparty)
    loan_account = get_pb_loan_account(acm_counterparty)
    reporting_portfolio = get_pb_reporting_portfolio(acm_counterparty)
    collateral_portfolio = get_pb_collateral_portfolio(acm_counterparty)
    if not (call_account or
            loan_account or
            reporting_portfolio or
            collateral_portfolio):
        return None
    fund_attributes = (fund_id,
                       acm_counterparty,
                       call_account,
                       loan_account,
                       reporting_portfolio,
                       collateral_portfolio)
    return fund_attributes


def main(portfolio_swaps,
         use_counterparty_attributes,
         transaction_size,
         log_file_path):
    """
    Update the additional infos on the provided portfolio swaps,
    on counterparties on their relevant trades
    and on trades in their funding portfolios.

    If 'use_counterparty_attributes' is set to True,
    then no counterparty attributes are set.
    Instead, they are just checked for consistency.
    Moreover, their values are utilized
    during the calculation of the portfolio swap and trade attributes.
    """
    # If no portfolio swaps have been provided,
    # do not just silently finish,
    # but print a warning message about it first.
    if not portfolio_swaps:
        warning_message = ("Warning: No portfolio swaps have been provided, "
                           "so nothing has been done.")
        print(warning_message, file=sys.stderr)
        return
    number_of_pswaps = len(portfolio_swaps)
    new_time_series_nondma = acm.FTimeSeriesSpec["pb_exec_prem_nondma"]
    new_time_series_rate = acm.FTimeSeriesSpec["pb_exec_prem_rate"]
    new_time_series_voice = acm.FTimeSeriesSpec["pb_exec_prem_voice"]
    print("Setting attributes for {0} portfolio swaps...".format(
        number_of_pswaps))
    with open(log_file_path, "wb") as log_file:
        pb_funds = {}
        print("Updating the portfolio swaps...")
        info_message = "Start time: {0}".format(dt.now())
        print(info_message, file=log_file)
        print(info_message, file=sys.stdout)
        for i, portfolio_swap in enumerate(portfolio_swaps, start=1):
            info_message = "Start time: {0}".format(dt.now())
            print(info_message, file=log_file)
            print(info_message, file=sys.stdout)
            sys.stdout.write("{0}/{1}: ".format(i, number_of_pswaps))
            pswap_attributes = get_pswap_attributes(
                portfolio_swap,
                use_counterparty_attributes,
                log_file)
            (funding_portfolio,
             sweeping_class,
             fully_funded) = pswap_attributes
            update_portfolio_swap(portfolio_swap,
                                  sweeping_class,
                                  fully_funded,
                                  log_file)
            info_message = "Timestamp: {0}".format(dt.now())
            print(info_message, file=log_file)
            print(info_message, file=sys.stdout)
            update_trades(funding_portfolio,
                          fully_funded,
                          log_file,
                          transaction_size)
            info_message = "Timestamp: {0}".format(dt.now())
            print(info_message, file=log_file)
            print(info_message, file=sys.stdout)
            update_time_series(acm.FTimeSeriesSpec["PSExtExecPremNonDMA"],
                               new_time_series_nondma,
                               funding_portfolio,
                               portfolio_swap,
                               log_file)
            update_time_series(acm.FTimeSeriesSpec["PSExtExecPremRate"],
                               new_time_series_rate,
                               funding_portfolio,
                               portfolio_swap,
                               log_file)
            update_time_series(acm.FTimeSeriesSpec["PSExtExecPremVoice"],
                               new_time_series_voice,
                               funding_portfolio,
                               portfolio_swap,
                               log_file)
            fund_attributes = get_fund_attributes(portfolio_swap,
                                                  funding_portfolio,
                                                  log_file)
            fund_id = fund_attributes[0]
            if fund_id in pb_funds:
                pb_funds[fund_id].append(fund_attributes[1:])
            else:
                pb_funds[fund_id] = [fund_attributes[1:]]
            if use_counterparty_attributes:
                counterparty = fund_attributes[1]
                current_fund_attributes = get_current_fund_attributes(
                    counterparty)
                if current_fund_attributes:
                    if fund_id in pb_funds:
                        pb_funds[fund_id].append(current_fund_attributes[1:])
                    else:
                        pb_funds[fund_id] = [current_fund_attributes[1:]]
                    warning_message = ("Warning: The current attributes "
                                       "of a Prime Brokerage fund '{0}' "
                                       "have been added "
                                       "to the list of attributes "
                                       "determined for that fund, "
                                       "to check the consistency "
                                       "with the current setup.").format(
                                           fund_id)
                else:
                    warning_message = ("Warning: The Prime Brokerage "
                                       "fund '{0}' does not have "
                                       "any attribute set.").format(
                                           fund_id)
                print(warning_message, file=log_file)
                print(warning_message, file=sys.stderr)
        print("Portfolio swaps have been updated.")
        print("Updating the counterparties...")
        number_of_funds = len(pb_funds)
        for i, fund_id in enumerate(pb_funds, start=1):
            sys.stdout.write("{0}/{1}: ".format(i, number_of_funds))
            fund_attributes_list = pb_funds[fund_id]
            if len(fund_attributes_list) > 1:
                warning_message = ("Warning: More than one set of attributes "
                                   "has been found for fund '{0}'. "
                                   "Checking whether "
                                   "they are the same...").format(fund_id)
                print(warning_message, file=log_file)
                print(warning_message, file=sys.stderr)
            fund_attributes_set = set(fund_attributes_list)
            if len(fund_attributes_set) != 1:
                printable_fund_attributes = [
                    format_fund_attributes(attributes)
                    for attributes in fund_attributes_set]
                error_message = ("Error: There are at least two different "
                                 "lists of attributes for fund '{0}'. "
                                 "All of them are listed below:").format(
                                     fund_id)
                for single_attributes in printable_fund_attributes:
                    error_message += "\n{0}".format(single_attributes)
                print(error_message, file=log_file)
                print(error_message, file=sys.stderr)
            (counterparty,
             call_account,
             loan_account,
             reporting_portfolio,
             collateral_portfolio) = fund_attributes_set.pop()
            update_counterparty(counterparty,
                                call_account,
                                loan_account,
                                reporting_portfolio,
                                collateral_portfolio,
                                log_file)
        print("Counterparties have been updated.")
        info_message = "End time: {0}".format(dt.now())
        print(info_message, file=log_file)
        print(info_message, file=sys.stdout)
    print("Done with setting up the attributes.")


def ael_main(parameters):
    """
    Get the parameters from the Run Script window
    and call the main function.
    """
    update_all_active_pswaps = parameters["update_all_active_pswaps"]
    use_counterparty_attributes = parameters["use_counterparty_attributes"]
    transaction_size = parameters["transaction_size"]
    if update_all_active_pswaps:
        fund_counterparties = get_pb_fund_counterparties()
        portfolio_swaps = []
        for acm_counterparty in fund_counterparties:
            fund_portfolio_swaps = get_pb_fund_pswaps(acm_counterparty)
            portfolio_swaps.extend(fund_portfolio_swaps)
    else:
        portfolio_swaps_qf = parameters["portfolio_swaps_qf"]
        portfolio_swaps = list(portfolio_swaps_qf.Query().Select())

    log_file_path = parameters["log_file_path"]
    return main(portfolio_swaps,
                use_counterparty_attributes,
                transaction_size,
                str(log_file_path))
