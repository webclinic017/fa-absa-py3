"""
A module implementing the PrimeBrokerageFund class.
"""

from at_logging import getLogger
from pb_attribute import ChronicleAttributeEncoder
from pb_fund_core import (PrimeBrokerageFundCore,
                          QuirkDescriptor)


LOGGER = getLogger()


class PrimeBrokerageFund(PrimeBrokerageFundCore):

    """
    A class representing a single prime brokerage fund.

    NOTE: When possible, use the caching factory function get_pb_fund
    from the pb_fund module to get the desired instance of this class.
    """

    # Descriptors for convenient access to quirks and attributes

    # Main
    # FIXME: no attributes here

    # References
    counterparty = QuirkDescriptor()
    reporting_portfolio = QuirkDescriptor()
    collateral_portfolio = QuirkDescriptor()
    call_account = QuirkDescriptor()
    call_account_number = QuirkDescriptor()
    call_account_rate_index = QuirkDescriptor()
    loan_account = QuirkDescriptor()
    loan_account_rate_index = QuirkDescriptor()
    commodities_call_account = QuirkDescriptor()
    commodities_call_account_rate_index = QuirkDescriptor()
    safex_call_account = QuirkDescriptor()
    safex_call_account_rate_index = QuirkDescriptor()
    yieldx_call_account = QuirkDescriptor()
    yieldx_call_account_rate_index = QuirkDescriptor()

    # IDs
    commodities_code = QuirkDescriptor()
    safex_code = QuirkDescriptor()
    yieldx_code = QuirkDescriptor()

    # Rates
    # FIXME: no rates yet

    # Spreads
    call_account_spread = QuirkDescriptor()
    loan_account_spread = QuirkDescriptor()
    commodities_call_account_spread = QuirkDescriptor()
    safex_call_account_spread = QuirkDescriptor()
    yieldx_call_account_spread = QuirkDescriptor()


    sweeping_class_to_shortcuts = {
        "Cash equity": "CE",
        "CFDs": "CFD",
        "Commodities": "APD",
        "Corporate bonds": "CORPBOND",
        "FI Options": "OTCFIOPT",
        "FRAs": "FRA",
        "Government bonds": "GOVIBOND",
        "Money market": "MONEYMARKET",
        "PBA Cash equity": "CE",
        "SAFEX exchange": "SAFEX",
        "Swaps": "IRS",
        "Unknown": "?",
        "YieldX exchange": "YIELDX"}


    def get_execution_rate(self, acm_trade):
        """
        Return the appropriate execution rate
        based on the provided trade's instrument class.
        """
        # TODO


    def get_product_type_name(self, sweeping_class, fully_funded):
        """
        Return the name of the product type
        represented by the product type
        with the provided properties.
        """
        fully_funded_string = "fully funded" if fully_funded else "financed"
        return "{0} ({1})".format(sweeping_class, fully_funded_string)


    def get_pswap_product_type_name(self, acm_pswap):
        """
        Return the name of the product type
        represented by the provided portfolio swap.
        """
        sweeping_class = self.quirks["ps_sweeping_class"].getvalue(acm_pswap)
        fully_funded = self.quirks["ps_fully_funded"].getvalue(acm_pswap)
        return self.get_product_type_name(sweeping_class, fully_funded)


    def get_product_type_pswaps(self):
        """
        Return all the portfolio swaps used by this fund
        for sweeping of all the enabled product types.
        """
        import acm
        from PS_Functions import get_pb_fund_pswaps
        acm_counterparty = acm.FCounterParty[self.counterparty]
        return sorted(get_pb_fund_pswaps(acm_counterparty),
                      key=lambda pswap: pswap.Name())


    def get_pswap_name(self,
                       sweeping_class,
                       fully_funded):
        """
        Return an ideal name of a portfolio swap
        which corresponds to a product type
        with the provided properties.
        """
        name = "PB_{0}".format(self.fund_id)
        if fully_funded:
            name += "_FF"
        name += "_{0}".format(self.sweeping_class_to_shortcuts[sweeping_class])
        return name


    def get_pswap_swap_portfolio_name(self,
                                      sweeping_class,
                                      fully_funded):
        """
        Return an ideal name of a swap portfolio
        (or fund portfolio, stock portfolio, etc.)
        which corresponds to a product type
        with the provided properties.
        """
        name = "PB_{0}".format(self.sweeping_class_to_shortcuts[sweeping_class])
        if fully_funded:
            name += "_FF"
        name += "_{0}_CR".format(self.fund_id)
        return name


    def get_pswap_trade_portfolio_name(self,
                                       sweeping_class,
                                       fully_funded):
        """
        Return an ideal name of a portfolio
        with the only confirmed trade of a portfolio swap
        which corresponds to a product type
        with the provided properties.
        """
        return "PB_PSWAP_{0}_CR".format(self.fund_id)


    def add_product_type_pswap(self,
                               sweeping_class,
                               fully_funded,
                               pswap_name=None,
                               start_date=None,
                               swap_portfolio_name=None,
                               trade_portfolio_name=None,
                               trade_status=None):
        """
        Add a new portfolio swap, which corresponds to a product type
        with the provided properties, to this fund.
        Then return the newly added portfolio swap.
        """
        import acm
        if pswap_name is None:
            pswap_name = self.get_pswap_name(sweeping_class, fully_funded)
        if start_date is None:
            start_date = acm.Time.DateToday()
        if swap_portfolio_name is None:
            swap_portfolio_name = self.get_pswap_swap_portfolio_name(
                sweeping_class, fully_funded)
        if trade_portfolio_name is None:
            trade_portfolio_name = self.get_pswap_trade_portfolio_name(
                sweeping_class, fully_funded)
        if trade_status is None:
            trade_status = "Simulated"

        pswap = acm.FPortfolioSwap[pswap_name]
        if pswap is None:
            pswap = acm.FPortfolioSwap()
            pswap.Name(pswap_name)
        valgroup = acm.FChoiceList.Select01(
            "list='ValGroup' AND name='EQ_SAFEX_PB'", None)
        pswap.ValuationGrpChlItem(valgroup)
        swap_portfolio = acm.FPhysicalPortfolio[swap_portfolio_name]
        if swap_portfolio is None:
            swap_portfolio = acm.FPhysicalPortfolio()
            swap_portfolio.Name(swap_portfolio_name)
            swap_portfolio.AssignInfo(swap_portfolio_name)
            swap_portfolio.Currency("ZAR")
            swap_portfolio.PortfolioOwner("PRIME SERVICES DESK")
            swap_portfolio.TypeChlItem("Held For Trading")
            swap_portfolio.Commit()
            parent_portfolio_name = self.reporting_portfolio
            from PS_Functions import link_portfolios
            link_portfolios(parent_portfolio_name, swap_portfolio_name)
            LOGGER.info("New portfolio '%s' "
                        "has been created as a descendant "
                        "of '%s' portfolio.",
                        swap_portfolio_name,
                        parent_portfolio_name)
        pswap.FundPortfolio(swap_portfolio)
        pswap.StartDate(start_date)
        pswap.OpenEnd("Open End")
        pswap.NoticePeriod("5y")
        pswap.Commit()
        self.quirks["ps_sweeping_class"].setvalue(pswap, sweeping_class)
        self.quirks["ps_fully_funded"].setvalue(pswap, fully_funded)
        # the most common default value
        self.quirks["ps_short_premium_type"].setvalue(pswap, "Fixed")

        trade = acm.FTrade()
        trade.Instrument(pswap)
        trade.Currency("ZAR")
        trade.Quantity(1)
        trade.Nominal(1)
        trade.TradeTime(pswap.StartDate())
        trade.ValueDay(pswap.StartDate())
        trade.AcquireDay(pswap.StartDate())
        trade.Counterparty(self.counterparty)
        trade.Acquirer("PRIME SERVICES DESK")
        trade.Portfolio(trade_portfolio_name)
        trade.Status(trade_status)
        trade.Commit()

        return pswap


    def remove_product_type_pswap(self, acm_portfolio_swap):
        """
        Remove the provided portfolio swap,
        which corresponds to a certain product type
        that is currently enabled for this fund.
        """
        from PS_Functions import get_instrument_trade
        relevant_trade = get_instrument_trade(acm_portfolio_swap)
        relevant_trade.Status("Void")
        relevant_trade.Commit()
        acm_portfolio_swap.OpenEnd("Terminated")
        acm_portfolio_swap.Commit()


class PrimeBrokerageFundEncoder(ChronicleAttributeEncoder):

    """
    A class which supports encoding of PrimeBrokerageFund objects to JSON.
    """

    def default(self, obj):
        """
        Return a serializable version of the provided object.
        """
        if isinstance(obj, PrimeBrokerageFund):
            pb_fund_s = {"type": type(obj).__name__,
                         "fund_id": obj.fund_id,
                         "attributes": obj.attributes}
            return pb_fund_s
        else:
            return super(PrimeBrokerageFundEncoder, self).default(obj)
