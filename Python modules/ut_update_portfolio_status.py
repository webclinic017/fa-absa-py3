"""Update portfolio status according to activity.

Portfolio status is an additional info field with possible values given
by a choice list of the same name.  Currently, the possible values are:

    Active, Closed, Dormant, NonStandard, Pending.

If a compound portfolio is passed to the script, it is first expanded to
all physical portfolios contained in its tree, then all these physical
portfolios are processed.

Requestor: Lohan Neethling/Marisa Fraser (PCG)


History
=======

2014-03-07 Pavel Saparov      ABITFA-2422 Initial implementation
2014-08-22 Vojtech Sidorin    ABITFA-2892 Refactoring, update logic
2014-10-10 Vojtech Sidorin    AFRICAFA-372 Update SQL to consider trade acquire day when checking if trade is live
2015-02-26 Vojtech Sidorin    AFRICAFA-457 Add possibility to exclude portfolios by suffix.
2015-03-03 Vojtech Sidorin    AFRICAFA-459 Refactor
2015-03-06 Vojtech Sidorin    AFRICAFA-467 Use case-insensitive string comparison for portfolio name prefix and suffix.
"""

import ael
import acm
import datetime

import at_addInfo
import at_time
from at_ael_variables import AelVariableHandler

# Default values for ael_variables.
DEFAULT_PORTFOLIO = "ABSA BANK LTD"
DEFAULT_DORMANCY_START = "TODAY-6m"
DEFAULT_EXCLUDE_PORTFOLIO_PREFIXES = ("Allocate", "Simulate")
DEFAULT_EXCLUDE_PORTFOLIO_SUFFIXES = ()
DEFAULT_EXCLUDE_TRADE_STATUSES = ("Simulated", "Void")
DEFAULT_PROCESS_PORTFOLIO_STATUSES = ("Active", "Dormant")
DEFAULT_DRY_RUN = False

ael_variables = AelVariableHandler()
ael_variables.add(
        name="portfolio",
        label="Portfolio",
        cls="FPhysicalPortfolio",
        collection=acm.FPhysicalPortfolio.Select(""),
        default=DEFAULT_PORTFOLIO,
        mandatory=True,
        multiple=False,
        alt="Physical or compound portfolio to update. If a "
            "compound portfolio is selected, it will be expanded "
            "to all physical portfolios within its tree."
        )
ael_variables.add(
        name="dormancy_start",
        label="Dormancy start date",
        cls="string",
        collection=None,
        default=DEFAULT_DORMANCY_START,
        mandatory=True,
        multiple=False,
        alt="If a portfolio doesn't show any signs of activity "
            "after this date, it will be marked as dormant."
        )
ael_variables.add(
        name="exclude_portfolio_prefixes",
        label="Exclude portfolios with prefixes",
        cls="string",
        collection=acm.FPhysicalPortfolio.Select("compound = FALSE"),
        default=",".join(DEFAULT_EXCLUDE_PORTFOLIO_PREFIXES),
        mandatory=False,
        multiple=True,
        alt="Don't update physical portfolios with these prefixes."
        )
ael_variables.add(
        name="exclude_portfolio_suffixes",
        label="Exclude portfolios with suffixes",
        cls="string",
        collection=acm.FPhysicalPortfolio.Select("compound = FALSE"),
        default=",".join(DEFAULT_EXCLUDE_PORTFOLIO_SUFFIXES),
        mandatory=False,
        multiple=True,
        alt="Don't update physical portfolios with these suffixes."
        )
ael_variables.add(
        name="exclude_trade_statuses",
        label="Exclude trades with statuses",
        cls="string",
        collection=acm.FEnumeration["enum(TradeStatus)"].Enumerators(),
        default=",".join(DEFAULT_EXCLUDE_TRADE_STATUSES),
        mandatory=False,
        multiple=True,
        alt="Trades with these statuses are excluded when testing "
            "if a portfolio is active."
        )
ael_variables.add(
        name="process_portfolio_statuses",
        label="Process portfolios in these statuses.",
        cls="string",
        collection=acm.FChoiceList["Portfolio Status"].Choices(),
        default=",".join(DEFAULT_PROCESS_PORTFOLIO_STATUSES),
        mandatory=True,
        multiple=True,
        alt="Only portfolios in these statuses will be updated."
        )
ael_variables.add(
        name="dry_run",
        label="Dry run",
        cls="bool",
        collection=(True, False),
        default=DEFAULT_DRY_RUN,
        mandatory=True,
        multiple=False,
        alt="Tell what would be done but don't do it."
        )


def ael_main(kwargs):
    """Front Arena hook function."""
    if kwargs["dry_run"]:
        print("Starting (dry run).")
    else:
        print("Starting.")
    _update_portfolio_tree(kwargs["portfolio"],
                           kwargs["dormancy_start"],
                           kwargs["dry_run"],
                           kwargs["exclude_portfolio_prefixes"],
                           kwargs["exclude_portfolio_suffixes"],
                           kwargs["exclude_trade_statuses"],
                           kwargs["process_portfolio_statuses"])
    print("Completed successfully.")


def _update_portfolio_tree(portfolio,
                           dormancy_start,
                           dry_run,
                           exclude_portfolio_prefixes,
                           exclude_portfolio_suffixes,
                           exclude_trade_statuses,
                           process_portfolio_statuses):
    """Update status of all physical portfolios in the tree.

    Argument portfolio is expected to be an instance of FPhysicalPortfolio,
    i.e. it can be either a physical portfolio or a compound portfolio.
    (FCompoundPortfolio is derived from class FPhysicalPortfolio.)
    If portfolio is a compound portfolio, it is expanded to all physical
    portfolios in its tree.  Physical portfolios with prefixes and suffixes
    given in exclude_portfolio_prefixes and exclude_portfolio_suffixes,
    respectively, are not updated.  The prefix and suffix matching is case-
    insensitive.
    """

    # Expand compound portfolio.
    if portfolio.Compound():
        all_physical_portfolios = portfolio.AllPhysicalPortfolios()
    else:
        all_physical_portfolios = [portfolio]

    # Exclude physical portfolios with given prefixes and suffixes.
    # Do case-insensitive string matching.
    # NOTE: Empty lprefixes or lsuffixes will work, because the built-in
    # methods startswith and endswith return false if passed an empty tuple.
    lprefixes = tuple(p.lower() for p in exclude_portfolio_prefixes)
    lsuffixes = tuple(s.lower() for s in exclude_portfolio_suffixes)
    selected_portfolios = []
    for portfolio in all_physical_portfolios:
        lname = portfolio.Name().lower()
        if lname.startswith(lprefixes) or lname.endswith(lsuffixes):
            continue
        else:
            selected_portfolios.append(portfolio)

    # Update the selected physical portfolios.
    for portfolio in sorted(selected_portfolios):
        _update_physical_portfolio(portfolio, dormancy_start, dry_run,
                                   exclude_trade_statuses,
                                   process_portfolio_statuses)


class _PortfolioActivity(object):
    """Define portfolio activity states."""
    inactive = 1
    recently_created = 2
    active_trades = 3
    active_instruments = 4


def _update_physical_portfolio(portfolio, dormancy_start, dry_run,
                               exclude_trade_statuses,
                               process_portfolio_statuses):
    """Update status of physical portfolio."""
    status_map = {
        _PortfolioActivity.recently_created:
            ("Active", "Recently created portfolio."),
        _PortfolioActivity.active_trades:
            ("Active", "Contains active trades."),
        _PortfolioActivity.active_instruments:
            ("Active", "Contains active instruments."),
        _PortfolioActivity.inactive:
            ("Dormant", "No activity since dormancy start date.")
        }
    old_status = portfolio.AdditionalInfo().Portfolio_Status()
    if old_status in process_portfolio_statuses:
        activity_status = _is_active(portfolio, dormancy_start,
                                     exclude_trade_statuses)
        new_status, msg = status_map[activity_status]
        if new_status != old_status:
            print(("{0}: {1} --> {2} ({3})"
                    .format(portfolio.Name(), old_status, new_status, msg)))
            # Update addinfo only if not in dry-run.
            if not dry_run:
                at_addInfo.save(portfolio, "Portfolio Status", new_status)


def _is_active(portfolio, dormancy_start, exclude_trade_statuses):
    """Indicate whether portfolio is active.

    Return the activity state of a given portfolio.  The states are
    defined in class _PortfolioActivity.
    """
    if _is_recently_created(portfolio, dormancy_start):
        return _PortfolioActivity.recently_created
    elif _contains_active_trades(portfolio, dormancy_start,
                                 exclude_trade_statuses):
        return _PortfolioActivity.active_trades
    elif _contains_active_instruments(portfolio, dormancy_start,
                                      exclude_trade_statuses):
        return _PortfolioActivity.active_instruments
    else:
        return _PortfolioActivity.inactive


def _is_recently_created(portfolio, dormancy_start):
    """Return True if portfolio was created recently."""
    create_date = at_time.to_date(portfolio.CreateTime())
    recent_date = at_time.to_date(dormancy_start)
    return create_date > recent_date


def _contains_active_trades(portfolio, dormancy_start, exclude_trade_statuses):
    """Return True if portfolio contains active trades.

    Trades with statuses in exclude_trade_statuses are excluded.
    """
    prfnbr = int(portfolio.Oid())
    dormancy_start_date = at_time.to_date(dormancy_start)
    exclude_ts = _get_exclude_ts_predicate(exclude_trade_statuses, "t")
    sql_query = """
                SELECT
                    t.trdnbr
                FROM
                    trade t
                WHERE
                    t.prfnbr = '{prfnbr}' AND
                    (t.time > '{dormancy_start_date}' OR
                        t.acquire_day > '{dormancy_start_date}') AND
                    {exclude_ts} AND
                    t.archive_status <> 1 AND
                    t.aggregate <> 1
                """.format(prfnbr=prfnbr,
                           dormancy_start_date=dormancy_start_date,
                           exclude_ts=exclude_ts)
    return _exists_in_database(sql_query)


def _contains_active_instruments(portfolio, dormancy_start,
                                 exclude_trade_statuses):
    """Return True if portfolio contains active instruments.

    Instruments booked through trades with statuses in
    exclude_trade_statuses are excluded.
    """
    prfnbr = int(portfolio.Oid())
    dormancy_start_date = at_time.to_date(dormancy_start)
    exclude_ts = _get_exclude_ts_predicate(exclude_trade_statuses, "t")
    sql_query = """
                SELECT
                    t.trdnbr
                FROM
                    trade t,
                    instrument i
                WHERE
                    t.prfnbr = '{prfnbr}' AND
                    t.insaddr = i.insaddr AND
                    i.exp_day > '{dormancy_start_date}' AND
                    {exclude_ts} AND
                    t.archive_status <> 1 AND
                    t.aggregate <> 1
                """.format(prfnbr=prfnbr,
                           dormancy_start_date=dormancy_start_date,
                           exclude_ts=exclude_ts)
    return _exists_in_database(sql_query)


def _get_exclude_ts_predicate(trade_statuses, trade_table_alias="trade"):
    """Return SQL predicate for excluding given trade statuses.

    Arguments:
    trade_statuses -- iterable with trade statuses to exclude
    trade_table_alias -- alias of the trade table that should be used in
                         the predicate
    """
    sql_statuses = []
    for ts in trade_statuses:
        ts_key = _get_trade_status_key(ts)
        sql_statuses.append("'{0}'".format(ts_key))
    if sql_statuses:
        joined = ", ".join(sql_statuses)
        predicate = "{0}.status NOT IN ({1})".format(trade_table_alias, joined)
    else:
        predicate = "1 = 1"
    return predicate


def _exists_in_database(sql_query):
    """Return true if sql_query returns at least one record."""
    exists_query = """
                   SELECT 1 WHERE EXISTS (
                       {sql_query}
                       )
                   """.format(sql_query=sql_query)
    result = ael.dbsql(exists_query)
    record = result[0]
    if record:
        return True
    else:
        return False


def _make_get_trade_status_key():
    """Make closure with function to get trade status key."""
    value_to_key_map = {}
    trade_status_enum = acm.FEnumeration["enum(TradeStatus)"]
    for value in trade_status_enum.Enumerators():
        key = trade_status_enum.Enumeration(value)
        value_to_key_map[value] = key
    return value_to_key_map.__getitem__
_get_trade_status_key = _make_get_trade_status_key()
