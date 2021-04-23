'''
Module mode ATS for mirroring the Prime Services trades from on-tree to
off-tree. Replaces stand-alone tasks for each fund.
Subscribes to trades updated today and filters based on portfolio,
status, counterparty, etc.
After restarting the ATS intraday, all relevant trades from today are
resent so that none of the updates are missed.
'''

from Queue import Queue
from logging import INFO

import acm

from at_classes import Singleton
from at_logging import getLogger
from PS_Functions import (
    Memoize,
    get_pb_reporting_portfolio,
    get_pb_fund_counterparties
)
from PS_MirrorToCR import (
    PORTFOLIO_MAP,
    VALID_INS_TYPE_FOR_CFD,
    hasValidMirrorTrade,
    StockToCFD, StockToCFDUpdate,
    MirrorTrade, MirrorTradeUpdate,
    GetCRPortfolio,
    AddDividendSuppression)
from PS_new_fees import add_cfd_execution_fee


LOGGER = getLogger(__name__, level=INFO)
COUNTERPARTY_NON_CFD = []
COUNTERPARTY_CFD = [209,  # ABSA BANK LTD
                    9710,  # EQ Derivatives Desk
                    18247,  # JSE
                    32737  # PRIME SERVICES DESK
                    ]
VALID_COMPOUNDS = ["PB_RISK", "ACS RTM Prime - Prime Broking"]
EXCLUDED_PORTFOLIOS = ["PB_RISK_FV_INTERMED_AGIB",
                       "PB_RISK_FV_INTERMED_AG_CAPITAL",
                       "PB_RISK_FV_INTERMED_BGC",
                       "PB_RISK_FV_INTERMED_EUROCLEAR",
                       "PB_RISK_FV_INTERMED_KEPLER",
                       "PB_RISK_FV_INTERMED_OAKHAVEN",
                       "PB_RISK_FV_INTERMED_RIDGCAP",
                       "PB_RISK_FV_INTERMED_SIYANDA",
                       "PB_RISK_FV_INTERMED_TRADITION"
                      ]
SKIP_STATUS = ["Simulated"]
SKIP_INS_TYPE = ["Deposit", "Portfolio Swap"]
QUERY_FOLDER_CHECK_TRADES_TODAY = "PS_MirrorToCR_RestartATS"


def init_counterparties(cp_list):
    all_counterparties = get_pb_fund_counterparties()
    for cp in all_counterparties:
        cp_list.append(cp.Name())


def is_valid_counterparty(trade, is_cfd, cp_list):
    counterparty = trade.Counterparty()
    if is_cfd and counterparty.Oid() in COUNTERPARTY_CFD:
        return True
    if not is_cfd and counterparty.Name() in cp_list:
        return True
    return False


def get_parent_portfolio_name(pf):
    parent = pf.MemberLinks()[0].OwnerPortfolio()
    if parent:
        return parent.Name()
    return None


@Memoize
def is_valid_portfolio(pf_name):
    if pf_name in EXCLUDED_PORTFOLIOS:
        return False
    pf = acm.FPhysicalPortfolio[pf_name]
    parent_pf_name = get_parent_portfolio_name(pf)
    if parent_pf_name is not None and parent_pf_name not in EXCLUDED_PORTFOLIOS:
        if parent_pf_name in VALID_COMPOUNDS:
            return True
        else:
            return is_valid_portfolio(parent_pf_name)
    return False


def is_valid_trade(trade):
    if trade.Status() in SKIP_STATUS:
        return False
    if trade.Instrument().InsType() in SKIP_INS_TYPE:
        return False
    if trade.Aggregate() != 0:
        return False
    return True


def get_is_cfd(trade, portfolio):
    portfolio_type = portfolio.add_info('PS_PortfolioType')
    if portfolio_type == "CFD" and trade.Instrument().InsType() in VALID_INS_TYPE_FOR_CFD:
        return True
    elif portfolio_type == "General":
        return False
    return None


def get_default_portfolio(reporting_portfolio):
    all_physical_portfolios = reporting_portfolio.AllPhysicalPortfolios()
    for pf in all_physical_portfolios:
        if pf.add_info("PS_FullyFunded"):
            return pf
    if all_physical_portfolios:
        return all_physical_portfolios[0]
    return None


def portfolio_mapping(portfolio, counterparty, is_cfd):
    pf_name = portfolio.Name()
    if pf_name in PORTFOLIO_MAP:
        return PORTFOLIO_MAP[pf_name]
    default_portfolio = None
    if is_cfd:
        call_acc = portfolio.add_info("PSClientCallAcc")
        if call_acc:
            cp = acm.FDeposit[call_acc].Trades()[0].Counterparty()
            if cp:
                reporting_portfolio = get_pb_reporting_portfolio(cp)
                for pf in reporting_portfolio.AllPhysicalPortfolios():
                    if pf.Name().find('CFD') > 0:
                        default_portfolio = pf
                if default_portfolio is None:
                    default_portfolio = get_default_portfolio(reporting_portfolio)
    else:
        reporting_portfolio = get_pb_reporting_portfolio(counterparty)
        default_portfolio = get_default_portfolio(reporting_portfolio)
    mapped_cr_portfolio = GetCRPortfolio(portfolio, default_portfolio)
    if mapped_cr_portfolio is None:
        LOGGER.error("Did not find appropriate CFD portfolio for {}".format(pf_name))
    PORTFOLIO_MAP[portfolio.Name()] = GetCRPortfolio(portfolio, mapped_cr_portfolio)
    return mapped_cr_portfolio


class MirrorToCR(object, metaclass=Singleton):
    def __init__(self):
        init_counterparties(COUNTERPARTY_NON_CFD)
        self._trade_queue = Queue()
        self._trades = acm.FTrade.Select("updateTime >= {}".format(acm.Time.DateNow()))
        self._subscribe()
        LOGGER.info("ATS started...")

    def _subscribe(self):
        self._trades.AddDependent(self)

    def unsubscribe(self):
        self._trades.RemoveDependent(self)

    @staticmethod
    def _log_error(oid, is_new=True):
        temp_text = "created" if is_new else "updated"
        LOGGER.error("Mirror was not {} for trade {}".format(temp_text, oid))

    @staticmethod
    def _log_ontree(oid, ins_name, pf_name, is_new=True):
        temp_text = "New" if is_new else "Update"
        LOGGER.info("On-tree - {} {} {} {}".format(temp_text, oid, ins_name, pf_name))

    @staticmethod
    def _log_offtree(oid, ins_name, pf_name, is_new=True, exec_fee=None):
        temp_text = "New" if is_new else "Update"
        msg = "Off-tree - {} {} {} {}".format(temp_text, oid, ins_name, pf_name)
        if exec_fee:
            msg += " execution fee: {}".format(exec_fee)
        LOGGER.info(msg)

    @staticmethod
    def _cfd_add_fee_and_payment(t_ontree, t_offtree, is_new=True):
        execution_fee = add_cfd_execution_fee(t_offtree)
        AddDividendSuppression(t_ontree, t_offtree)
        MirrorToCR._log_offtree(t_offtree.Oid(),
                                t_offtree.Instrument().Name(),
                                t_offtree.Portfolio().Name(),
                                exec_fee=execution_fee, is_new=is_new)

    def check_trades_today(self):
        query_folder = acm.FStoredASQLQuery[QUERY_FOLDER_CHECK_TRADES_TODAY]
        candidate_trades = query_folder.Query().Select()
        LOGGER.info("Number of candidate trades = {}".format(candidate_trades.Size()))
        for trade in candidate_trades:
            portfolio = trade.Portfolio()
            is_cfd = get_is_cfd(trade, portfolio)
            if is_cfd is not None and is_valid_counterparty(trade, is_cfd, COUNTERPARTY_NON_CFD):
                LOGGER.info("Resending trade {}".format(trade.Oid(), is_cfd))
                self._trade_queue.put([trade, is_cfd])

    def process_candidate_trades(self):
        while not self._trade_queue.empty():
            (t_ontree, is_cfd) = self._trade_queue.get()
            oid_ontree = t_ontree.Oid()
            cp_ontree = t_ontree.Counterparty()
            pf_ontree = t_ontree.Portfolio()
            pf_name_ontree = pf_ontree.Name()
            ins_name_ontree = t_ontree.Instrument().Name()
            pf_offtree = portfolio_mapping(pf_ontree, cp_ontree, is_cfd)
            if pf_offtree is None:
                LOGGER.error("Can't process trade {}, off-tree portfolio missing".format(oid_ontree))
            if not hasValidMirrorTrade(t_ontree):
                self._log_ontree(oid_ontree, ins_name_ontree, pf_name_ontree)
                if is_cfd:
                    t_offtree = StockToCFD(t_ontree)
                    if t_offtree:
                        self._cfd_add_fee_and_payment(t_ontree, t_offtree)
                    else:
                        self._log_error(oid_ontree)
                else:
                    t_offtree = MirrorTrade(t_ontree)
                    if t_offtree:
                        self._log_offtree(t_offtree.Oid(),
                                          t_offtree.Instrument().Name(),
                                          t_offtree.Portfolio().Name())
                    else:
                        self._log_error(oid_ontree)
            else:
                self._log_ontree(oid_ontree, ins_name_ontree, pf_name_ontree, is_new=False)
                if is_cfd:
                    t_offtree = StockToCFDUpdate(t_ontree)
                    if t_offtree:
                        self._cfd_add_fee_and_payment(t_ontree, t_offtree, is_new=False)
                    else:
                        self._log_error(oid_ontree, is_new=False)
                else:
                    t_offtree = MirrorTradeUpdate(t_ontree)
                    if t_offtree:
                        self._log_offtree(t_offtree.Oid(),
                                          t_offtree.Instrument().Name(),
                                          t_offtree.Portfolio().Name(),
                                          is_new=False)
                    else:
                        self._log_error(oid_ontree, is_new=False)

    def ServerUpdate(self, sender, operation, entity):
        _operation = str(operation)
        LOGGER.debug("{} {}".format(_operation, entity.Oid()))
        portfolio = entity.Portfolio()
        if not is_valid_portfolio(portfolio.Name()):
            LOGGER.debug("Invalid portfolio: {}".format(portfolio.Name()))
            return
        if not is_valid_trade(entity):
            LOGGER.debug("Invalid trade: status={} ins_type={} aggregate={}"
                         .format(entity.Status(), entity.Instrument().InsType(), entity.Aggregate()))
            return
        is_cfd = get_is_cfd(entity, portfolio)
        if is_cfd is not None and is_valid_counterparty(entity, is_cfd, COUNTERPARTY_NON_CFD):
            self._trade_queue.put([entity, is_cfd])
            LOGGER.info("Candidate trade: {}".format(entity.Oid()))
        else:
            LOGGER.debug("Skipping trade: {}".format(entity.Oid()))


def start():
    mirror_ats = MirrorToCR()
    mirror_ats.check_trades_today()


def stop():
    mirror_ats = MirrorToCR()
    mirror_ats.unsubscribe()
    LOGGER.info("ATS stopped...")


def work():
    mirror_ats = MirrorToCR()
    mirror_ats.process_candidate_trades()
