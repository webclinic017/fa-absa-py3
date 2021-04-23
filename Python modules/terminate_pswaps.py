import ael
import acm
from at_addInfo import save as save_additional_info
from at_ael_variables import AelVariableHandler
from PS_Functions import is_child_portf


def set_status(trades, status):
    """Set given status on a set of trades."""
    acm.BeginTransaction()
    try:
        for trade in trades:
            msg = "Changing status on trade {0} ({1}) to {2}"
            print(msg.format(trade.Oid(), trade.Instrument().Name(), status))
            trade.Status(status)
            trade.Commit()
        acm.CommitTransaction()
        print("Statuses successfully changed")
    except Exception as ex:
        print("Failed to change statuses on pswap trades: {0}".format(ex))
        acm.AbortTransaction()


def change_oakhaven_pswap_trades(status):
    """Terminate unused OAKHAVEN pswap trades.

    Portfolios containing substring 'OLD' in their names are not used for
    trading any more. These portfolios are connected to pswaps catergorized
    by instrument class. To avoid duplicated sweeping engineering trades for
    'OLD' pswaps need to be terminated.

    """
    print("Processing pswaps for OAKHAVEN")
    portfolio = acm.FPhysicalPortfolio["PB_PSWAP_OAKHAVEN_CR"]
    trades = [t for t in portfolio.Trades() if "OLD" in t.Instrument().Name()]
    set_status(trades, status)


def change_coro_granite_pswap_trades(status):
    """Terminate unused CORO_GRANITE pswap trades.

    Client CORO_GRANITE has extra portfolios setup to support strategies.
    These strategies were never used (and there is no plan to support them)
    and pswaps connected to these portfolios need to be terminated to avoid
    duplicated sweeping. Active pswaps contain substring "SWITCH" in their
    names.
    
    """
    print("Processing pswaps for CORO_GRANITE")
    portfolio = acm.FPhysicalPortfolio["PB_PSWAP_CORO_GRANITE_CR"]
    trades = [t for t in portfolio.Trades()
              if "SWITCH" not in t.Instrument().Name()]
    set_status(trades, status)
    
    
def change_map290_safex_pswap_trades(status):
    """Terminate unused safex pswap trade(s) for XFM_MAP290.

    Second SAFEX account, portfolio and connected pswap were open for the
    client but never used and pswap needs to be terminated to avoid duplicated
    sweeping.
    
    """
    print("Processing pswaps for XFM_MAP290")
    pswap = acm.FPortfolioSwap["PB_XFM_MAP290_SAFEX2"]
    trades = [t for t in pswap.Trades()]
    set_status(trades, status)


def change_map501_pswap_trades(status):
    """Terminate pswap trades if connected portfolio is in graveyard."""
    print("Processing pswaps for MAP501")
    portfolio = acm.FPhysicalPortfolio["PB_PSWAP_MAP_501_CR"]
    graveyard = acm.FPhysicalPortfolio["GRAVEYARD"]
    trades = [t for t in portfolio.Trades()
              if is_child_portf(t.Instrument().FundPortfolio(), graveyard)]
    set_status(trades, status)


def change_nitro_trust_pswap_trades(status):
    """Terminate pswap trades if connected portfolio is in graveyard."""
    print("Processing pswaps for NITRO_TRUST")
    portfolio = acm.FPhysicalPortfolio["PB_PSWAP_Nitrogen_Trust_CR"]
    graveyard = acm.FPhysicalPortfolio["GRAVEYARD"]
    trades = [t for t in portfolio.Trades()
              if is_child_portf(t.Instrument().FundPortfolio(), graveyard)]
    set_status(trades, status)


def change_cfd_pswap_trades(status):
    """Terminate pswap trades if connected portfolio is in graveyard."""
    print("Processing CFD pswaps")
    ps_names = ["PB_ATPOINT1_CFD",
                "PB_BLUEINK_FF_CFD",
                "PB_CAFM_MAP280_CFD",
                "PB_KAIZSOF_CFD",
                "PB_MAP_106_CFD",
                "PB_SLMSEC_CFD"]
    portfolio_swaps = [acm.FPortfolioSwap[ps_name] for ps_name in ps_names]
    graveyard = acm.FPhysicalPortfolio["GRAVEYARD"]
    for portfolio_swap in portfolio_swaps:
        trades = [t for t in portfolio_swap.Trades()
                  if is_child_portf(t.Instrument().FundPortfolio(), graveyard)]
        set_status(trades, status)


def update_cfd_portfolios():
    """
    Set the 'PS_MirrorCRBook' additional info
    of certain on-tree portfolios
    to their off-tree counterparts.
    """
    print("Processing CFD portfolios")
    portfolio_mapping = {"40675": "PB_CFD_SLMSEC_CR"}
    portfolios = [acm.FPhysicalPortfolio[pname]
                  for pname in portfolio_mapping]
    for portfolio in portfolios:
        target_portfolio_name = portfolio_mapping[portfolio.Name()]
        target_portfolio = acm.FPhysicalPortfolio[target_portfolio_name]
        save_additional_info(portfolio,
                             "PS_MirrorCRBook",
                             target_portfolio)


def change_map501_pswap_strategy_trades(status):
    """Collapse strategies for MAP501."""
    print("Processing strategy pswaps for MAP501")
    active_pswap_names = ["PB_M501_L/O_FF_CE",
                          "PB_M501_S/O_CE", 
                          "PB_M501_SAFEX"]
                          
    portfolio = acm.FPhysicalPortfolio["PB_PSWAP_M501_CR"]
    trades = [t for t in portfolio.Trades()
              if t.Instrument().Name() not in active_pswap_names]
    set_status(trades, status)
    
    portfolio = acm.FPhysicalPortfolio["PB_PSWAP_MAP_501_CR"]
    set_status(portfolio.Trades(), status)


def change_nitro_trust_pswap_strategy_trades(status):
    """Collapse strategies for NITRO_TRUST."""
    print("Processing strategy pswaps for NITRO_TRUST")
    active_pswap_names = ["PB_NIT_TR_LT_BK_LO_FF_CE",
                          "PB_NIT_TR_LT_BK_SO_CE"]
                          
    portfolio = acm.FPhysicalPortfolio["PB_PSWAP_NIT_TR_CR"]
    trades = [t for t in portfolio.Trades()
              if t.Instrument().Name() not in active_pswap_names]
    set_status(trades, status)
    
    portfolio = acm.FPhysicalPortfolio["PB_PSWAP_Nitrogen_Trust_CR"]
    set_status(portfolio.Trades(), status)


ael_variables = AelVariableHandler()
ael_variables.add("status",
    label="Status",
    default="Terminated")


def ael_main(config):
    import FValidation
    FValidation.ENABLE_VALIDATION = False
    status = config["status"]
    change_oakhaven_pswap_trades(status)
    change_coro_granite_pswap_trades(status)
    change_map290_safex_pswap_trades(status)
    change_map501_pswap_trades(status)
    change_map501_pswap_strategy_trades(status)
    change_nitro_trust_pswap_trades(status)
    change_nitro_trust_pswap_strategy_trades(status)
    change_cfd_pswap_trades(status)
    update_cfd_portfolios()
