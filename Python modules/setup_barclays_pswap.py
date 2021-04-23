import acm
from at import addInfo
from at_ael_variables import AelVariableHandler
from PS_PswapCreator import convert_from_ael_date


def add_engineering_trade(pswap, portfolio, counterparty):
    trade = acm.FTrade()
    trade.Instrument(pswap)
    trade.Currency('ZAR')
    trade.Quantity(1)
    trade.Nominal(1)
    trade.TradeTime(pswap.StartDate())
    trade.ValueDay(pswap.StartDate())
    trade.AcquireDay(pswap.StartDate())
    trade.Counterparty(counterparty)
    trade.Acquirer(acm.FParty['PRIME SERVICES DESK'])
    trade.Portfolio(portfolio)
    trade.Status('Simulated') # To allow for delete in case of rollback.
    trade.Commit()
    return trade


def create_pswap(pswap_name, stock_portfolio, start_date):
    pswap = acm.FPortfolioSwap()
    pswap.Name(pswap_name)
    pswap.ValuationGrpChlItem(acm.FChoiceList.Select01("list='ValGroup' AND name='EQ_SAFEX_PB'", None))
    pswap.FundPortfolio(stock_portfolio)
    pswap.StartDate(start_date)
    pswap.OpenEnd('Open End')
    pswap.NoticePeriod('1m')
    pswap.Commit()
    addInfo.save(pswap, 'PSONPremIndex', 'ZAR-ZERO-1M')
    addInfo.save(pswap, 'PSSweepBaseDay',
                 convert_from_ael_date(start_date, "%Y-%m-%d"))
    addInfo.save(pswap, 'PSSweepFreq', '1')
    return pswap


ael_variables = AelVariableHandler()
ael_variables.add("pswap_name",
                  label="Portfolio Swap Name")
ael_variables.add("stock_portfolio",
                  label="Stock Portfolios",
                  cls=acm.FPhysicalPortfolio,
                  collection=sorted(acm.FPhysicalPortfolio.Select("")))
ael_variables.add("portfolio",
                  label="Trade Portfolio",
                  cls=acm.FPhysicalPortfolio,
                  collection=sorted(acm.FPhysicalPortfolio.Select("")))
ael_variables.add("counterparty",
                 label="Counterparty",
                 cls=acm.FCounterParty,
                 collection=sorted(acm.FCounterParty.Select("")))
ael_variables.add("start_date",
                  label="Start date")


def ael_main(config):
    pswap = create_pswap(config["pswap_name"], config["stock_portfolio"], config["start_date"])
    trade = add_engineering_trade(pswap, config["portfolio"], config["counterparty"])
    print("Trade {0} created.".format(trade.Oid()))

