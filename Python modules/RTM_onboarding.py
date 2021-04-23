import traceback

import acm
from at import addInfo
from at_ael_variables import AelVariableHandler
from PS_PswapCreator import convert_from_ael_date


def create_portfolio(parent_portfolio, portfolio_name, is_physical=True, portfolio_currency_name=None):
    """Create a portfolio."""
    portfolio = acm.FPhysicalPortfolio[portfolio_name]
    if portfolio:
        msg = "INFO: A portfolio with the name '{0}' already exists. Using existing one."
        print(msg.format(portfolio_name))
        return portfolio
    if is_physical:
        portfolio = acm.FPhysicalPortfolio()
    else:
        portfolio = acm.FCompoundPortfolio()
    portfolio.Name(portfolio_name)
    portfolio.AssignInfo(portfolio_name)
    if not portfolio_currency_name:
        portfolio_currency_name = "ZAR"
    portfolio.Currency(portfolio_currency_name)
    portfolio.Commit()
    portfolio.AdditionalInfo().Portfolio_Status("Active") # Switch to Active when Chorus request is closed.
    portfolio.AdditionalInfo().Commit()
    portfolio.Commit()
    portfolio_link = acm.FPortfolioLink()
    portfolio_link.OwnerPortfolio(parent_portfolio)
    portfolio_link.MemberPortfolio(portfolio)
    portfolio_link.Commit()
    return portfolio


def create_pswap(pswap_name, stock_portfolio, start_date):
    """Create a portfolio swap."""
    pswap = acm.FPortfolioSwap[pswap_name]
    if pswap:
        msg = "INFO: A portfolio swap with the name '{0}' already exists. Using existing one."
        print(msg.format(pswap_name))
        return pswap
    pswap = acm.FPortfolioSwap()
    pswap.Name(pswap_name)
    pswap.ValuationGrpChlItem(acm.FChoiceList.Select01("list='ValGroup' AND name='EQ_SAFEX_PB'", None))
    pswap.FundPortfolio(stock_portfolio)
    pswap.StartDate(start_date)
    pswap.OpenEnd('Open End')
    pswap.NoticePeriod('5y')
    pswap.Commit()
    addInfo.save(pswap, 'PSONPremIndex', 'ZAR-ZERO-3M')
    addInfo.save(pswap, 'PSSweepBaseDay',
                 convert_from_ael_date(start_date, "%Y-%m-%d"))
    addInfo.save(pswap, 'PSSweepFreq', '1')
    return pswap


def add_engineering_trade(pswap, portfolio, counterparty, acquirer, quantity):
    """Create an engineering trade."""
    trade = acm.FTrade()
    trade.Instrument(pswap)
    trade.Currency('ZAR')
    trade.Quantity(quantity)
    trade.Nominal(quantity)
    trade.TradeTime(pswap.StartDate())
    trade.ValueDay(pswap.StartDate())
    trade.AcquireDay(pswap.StartDate())
    trade.Counterparty(counterparty)
    trade.Acquirer(acquirer)
    trade.Portfolio(portfolio)
    trade.Status('Simulated') # To allow for delete in case of rollback.
    trade.Commit()
    return trade


ael_variables = AelVariableHandler()
ael_variables.add("pswap_name",
                  label="Portfolio swap name")
ael_variables.add("main_acs_portfolio",
                  label="Main ACS portfolio",
                  cls=acm.FPhysicalPortfolio,
                  collection=sorted(acm.FCompoundPortfolio.Select("")))
ael_variables.add("acs_compound_portfolio",
                  label="ACS compound portfolio name")
ael_variables.add("stock_portfolio",
                  label="ACS stock portfolio name")
ael_variables.add("acs_pswap_portfolio",
                  label="ACS pswap portfolio name")
ael_variables.add("acs_counterparty",
                  label="ACS counterparty",
                  cls=acm.FParty,
                  collection=sorted(acm.FParty.Select("")))
ael_variables.add("main_bank_portfolio",
                  label="Main bank portfolio",
                  cls=acm.FPhysicalPortfolio,
                  collection=sorted(acm.FCompoundPortfolio.Select("")))
ael_variables.add("bank_compound_portfolio",
                  label="Bank compound portfolio name")
ael_variables.add("bank_pswap_portfolio",
                  label="Bank pswap portfolio name")
ael_variables.add("bank_counterparty",
                  label="Bank counterparty",
                  cls=acm.FParty,
                  collection=sorted(acm.FParty.Select("")))
ael_variables.add("start_date",
                  cls="date",
                  label="Start date")


def ael_main(config):
    """Entry point of the script."""
    pswap_name = config["pswap_name"]
    main_acs_portfolio = config["main_acs_portfolio"]
    acs_compound_portfolio_name = config["acs_compound_portfolio"]
    stock_portfolio_name = config["stock_portfolio"]
    acs_pswap_portfolio_name = config["acs_pswap_portfolio"]
    acs_counterparty = config["acs_counterparty"]
    main_bank_portfolio = config["main_bank_portfolio"]
    bank_compound_portfolio_name = config["bank_compound_portfolio"]
    bank_pswap_portfolio_name = config["bank_pswap_portfolio"]
    bank_counterparty = config["bank_counterparty"]
    start_date = config["start_date"]
    
    try:
        # Create ACS compound portfolio
        print("Creating ACS compound portfolio {0}....".format(acs_compound_portfolio_name))
        acs_compound_portfolio = create_portfolio(main_acs_portfolio, acs_compound_portfolio_name, False)
        print("Done")
        
        # Create ACS stock portfolio
        print("Creating ACS stock portfolio {0}....".format(stock_portfolio_name))
        stock_portfolio = create_portfolio(acs_compound_portfolio, stock_portfolio_name)
        print("Done")

        # Create ACS pswap portfolio
        print("Creating ACS pswap portfolio {0}....".format(acs_pswap_portfolio_name))
        acs_pswap_portfolio = create_portfolio(acs_compound_portfolio, acs_pswap_portfolio_name)
        print("Done")

        # Create bank compound portfolio
        print("Creating bank compound portfolio {0}....".format(bank_compound_portfolio_name))
        bank_compound_portfolio = create_portfolio(main_bank_portfolio, bank_compound_portfolio_name, False)
        print("Done")
        
        # Create bank pswap portfolio
        print("Creating bank pswap portfolio {0}....".format(bank_pswap_portfolio_name))
        bank_pswap_portfolio = create_portfolio(bank_compound_portfolio, bank_pswap_portfolio_name)
        print("Done")

        # Create portfolio swap
        print("Creating portfolio swap {0}....".format(pswap_name))
        pswap = create_pswap(pswap_name, stock_portfolio, start_date)
        print("Done.")

        # Create ACS engineering trade
        print("Creating ACS enigneering trade....")
        acs_trade = add_engineering_trade(pswap, acs_pswap_portfolio, bank_counterparty, acs_counterparty, -1)
        print("Done (Oid: {0})".format(acs_trade.Oid()))

        # Create bank engineering trade
        print("Creating bank enigneering trade....")
        bank_trade = add_engineering_trade(pswap, bank_pswap_portfolio, acs_counterparty, bank_counterparty, 1)
        print("Done (Oid: {0})".format(bank_trade.Oid()))

        print("Completed successfully")
    except Exception as ex:
        print("Error on-boarding {0}: {1}".format(pswap_name, ex))
        traceback.print_exc()
    
