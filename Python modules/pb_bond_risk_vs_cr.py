import acm
from PS_Functions import get_pb_fund_counterparties, is_child_portf


NAMES = [cp.Name() for cp in get_pb_fund_counterparties()]

    
def party_in_names(_table, party, *args):
    if party in NAMES:
        return 1
    return 0

def bond_risk_portf(trade):
    portf_name = trade.PortfolioId()
    if trade.PortfolioId() in ["PB_RISK_FV_CLIENTBONDS", "PB_RISK_FV_INTERMED_RIDGCAP"]:
        return trade.PortfolioId()
    if is_child_portf(trade.Portfolio(), acm.FPhysicalPortfolio["PB_CR_LIVE"]):
        return "CLIENT CR PORTF"
    return "Not Applicable"
