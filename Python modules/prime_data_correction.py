import acm
from at_ael_variables import AelVariableHandler
from at_addInfo import save
from PS_Functions import get_pb_fund_counterparty


def fix_add_infos_nitroskyl():
    "Set additional infos correctly for NITROSKYL."
    counterparty = get_pb_fund_counterparty("NITROSKYL")
    call_account = acm.FInstrument["ZAR/NITROSKYL_CallAcc"]
    loan_account = acm.FInstrument["ZAR/NITROSKYL_Loan"]
    reporting_portfolio = acm.FPhysicalPortfolio["PB_NITROSKYL_CR"]
    
    save(counterparty, "PB_Call_Account", call_account)
    save(counterparty, "PB_Loan_Account", loan_account)
    save(counterparty, "PB_Reporting_Prf", reporting_portfolio)


def fix_add_infos_slmsec():
    "Set additional infos correctly for SLMSEC."
    counterparty = get_pb_fund_counterparty("SLMSEC")
    reporting_portfolio = acm.FPhysicalPortfolio["PB_SLMSEC_CR"]
    collateral_portfolio = acm.FPhysicalPortfolio["PB_COLL_SLMSEC_CR"]
    call_account = acm.FInstrument["ZAR/121120-121121"]
    
    save(counterparty, "PB_Call_Account", call_account)
    save(counterparty, "PB_Collateral_Prf", collateral_portfolio)
    save(counterparty, "PB_Reporting_Prf", reporting_portfolio)


def fix_reporting_portfolio_oakhaven():
    """Set 'new' reporting portfolio fro OAKAHAVEN."""
    counterparty = get_pb_fund_counterparty("OAKHAVEN")
    reporting_portfolio = acm.FPhysicalPortfolio["PB_OAKHAVEN_NEW_CR"]
    print("Setting reporting portfolio for OAKHAVEN to PB_OAKHAVEN_NEW_CR")
    save(counterparty, "PB_Reporting_Prf", reporting_portfolio)


def copy_loan_account_history_oakhaven():
    """Copy loan account history for OAKHAVEN to new reporting portfolio."""
    new_portfolio = acm.FPhysicalPortfolio["PB_OAKHAVEN_NEW_CR"]
    new_time_series_spec = acm.FTimeSeriesSpec()
    new_time_series_spec.Description('%s PnL History' % new_portfolio.Name())
    new_time_series_spec.FieldName("PB_OAKHAVEN_NEW_CR_PnL")
    new_time_series_spec.RecType(acm.EnumFromString('B92RecordType', 'Portfolio'))
    new_time_series_spec.Commit()

    time_series_spec = acm.FTimeSeriesSpec["PB_OAKHAVEN_CR_PnL"]
    acm.BeginTransaction()
    try:
        portfolio = acm.FPhysicalPortfolio["PB_OAKHAVEN_CR"]
        series = acm.FTimeSeries.Select("recaddr = {0} timeSeriesSpec = {1}".format(
            portfolio.Oid(), time_series_spec.Oid()))

        for record in series:
            new_record = record.Clone()
            print(new_record)
            new_record.Recaddr(new_portfolio.Oid())
            new_record.TimeSeriesSpec(new_time_series_spec.Oid())
            new_record.Commit()
        acm.CommitTransaction()
        print("Copying Successful")
    except Exception as ex:
        print("Copying Failed: {0}".format(ex))
        acm.AbortTransaction()


def link_marksol_option_portfolio():
    """Link marksol option portfolio to RISK CR."""
    parent_acm_portfolio = acm.FPhysicalPortfolio["PB_RISK_MARKSOL_CR"]
    acm_portfolio = acm.FPhysicalPortfolio["PB_OPTION_FI_MARKSOL_CR"]
    
    portfolio_link = acm.FPortfolioLink()
    portfolio_link.OwnerPortfolio(parent_acm_portfolio)
    portfolio_link.MemberPortfolio(acm_portfolio)
    portfolio_link.Commit()


def create_portfolio(parent_acm_portfolio,
                     portfolio_id,
                     portfolio_currency_id=None,
                     is_physical=True):
    """
    Create and return a new portfolio with the provided ID
    and make it a descendant of the provided parent portfolio.
    """
    acm_portfolio = acm.FPhysicalPortfolio[portfolio_id]
    if acm_portfolio:
        warning_message = ("Warning: A portfolio with the name "
                           "'{0}' already exists").format(portfolio_id)
        print(warning_message)
        return acm_portfolio
    if is_physical:
        acm_portfolio = acm.FPhysicalPortfolio()
    else:
        acm_portfolio = acm.FCompoundPortfolio()
    acm_portfolio.Name(portfolio_id)
    acm_portfolio.AssignInfo(portfolio_id)
    if not portfolio_currency_id:
        portfolio_currency_id = "ZAR"
    acm_portfolio.Currency(portfolio_currency_id)
    acm_portfolio.Commit()
    # Required by FValidation
    acm_portfolio.AdditionalInfo().Portfolio_Status("Active")
    acm_portfolio.AdditionalInfo().Commit()
    # FIXME: Not sure if this commit is required or not, but probably yes.
    acm_portfolio.Commit()
    portfolio_link = acm.FPortfolioLink()
    portfolio_link.OwnerPortfolio(parent_acm_portfolio)
    portfolio_link.MemberPortfolio(acm_portfolio)
    portfolio_link.Commit()
    return acm_portfolio


def create_new_portfolios():
    """
    Create some new portfolios into which
    some of the current Prime Brokerage trades
    from the CR subtree will be moved.
    """
    print("Creating new portfolios")
    new_pnames = {"PB_ABAXFIT_OTHER_CR": "PB_ABAXFIT_CR",
                  "PB_MAP100_OTHER_CR": "PB_MAP100_CR",
                  "PB_SAASPCV_OTHER_CR": "PB_SAASPCV_CR"}
    for portfolio_name, parent_portfolio_name in new_pnames.iteritems():
        parent_portfolio = acm.FPhysicalPortfolio[parent_portfolio_name]
        create_portfolio(parent_portfolio, portfolio_name)
        print("Created portfolio '{0}' as a parent of '{1}'.".format(
            portfolio_name, parent_portfolio_name))


def move_trades():
    """
    Move some trades around to test the behaviour
    of the portfolio-independent sweeping.
    """
    tasks_to_run = ["Move ABAXFIT trades",
                    "Move MAP100 trades",
                    "Move SAASPCV trades"]
    for task_name in tasks_to_run:
        task = acm.FAelTask[task_name]
        print("Running the task '{0}'".format(task_name))
        task.Execute()


ael_variables = AelVariableHandler()
def ael_main(config):
    fix_add_infos_nitroskyl()
    fix_add_infos_slmsec()
    fix_reporting_portfolio_oakhaven()
    copy_loan_account_history_oakhaven()
