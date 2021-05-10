"""
A module implementing the FundQuirk class and the derived classes,
most importantly QuirkAttribute class.
"""


# generic quirks


class FundQuirk(object):

    """
    A base class for all quirks that need a reference
    to the prime brokerage fund.
    """

    def __init__(self, pb_fund=None):
        self.pb_fund = pb_fund
        super(FundQuirk, self).__init__()


class QuirkAttribute(FundQuirk):

    """
    A base class defining an interface for getting and setting
    a certain property relevant for the referenced prime brokerage fund.
    """

    def getvalue(self):
        """
        Return a value of the represented property.
        """
        raise NotImplementedError


    def setvalue(self, value):
        """
        Set the provided value as the current value
        of the represented property.
        """
        raise NotImplementedError


class PortfolioSwapBasedQuirk(FundQuirk):

    """
    A generic quirk representing an attribute
    stored on the provided portfolio swap
    which is related to the represented fund.

    This quirk attribute should be *dynamic*
    in a sense that it can get and set attributes
    based on the *provided* portfolio swap.
    """

    def getvalue(self, acm_portfolio_swap):
        """
        Return a value of the represented property
        on the provided portfolio swap.
        """
        raise NotImplementedError


    def setvalue(self, acm_portfolio_swap, value):
        """
        Set the provided value as the current value
        of the represented property
        on the provided portfolio swap.
        """
        raise NotImplementedError


class PortfolioSwapSuggestionQuirk(FundQuirk):

    """
    A generic, read-only, suggestion quirk
    which is supposed to provide suggestions
    on the value of the represented property
    based on the provided product type details
    and the underlying prime brokerage fund.
    """

    def getvalue(self, sweeping_class, fully_funded):
        """
        Return the suggested value of the represented property
        based on the provided portfolio swap name.
        """
        raise NotImplementedError


class PortfolioSwapAddInfoBasedQuirk(PortfolioSwapBasedQuirk):

    """
    A generic quirk representing an attribute
    stored in an additional info on the provided portfolio swap
    which is related to the represented fund.

    This quirk attribute should be *dynamic*
    in a sense that it can get and set attributes
    based on the *provided* portfolio swap.
    """

    ADD_INFO_NAME = None


    def get_acm_object(self, acm_portfolio_swap):
        return acm_portfolio_swap


    def getvalue(self, acm_portfolio_swap):
        # This import requires acm,
        # so it has been moved here.
        from at_addInfo import get_value
        acm_object = self.get_acm_object(acm_portfolio_swap)
        return get_value(acm_object, self.ADD_INFO_NAME)


    def setvalue(self, acm_portfolio_swap, value):
        # This import requires acm,
        # so it has been moved here.
        from at_addInfo import save_or_delete
        acm_object = self.get_acm_object(acm_portfolio_swap)
        save_or_delete(acm_object, self.ADD_INFO_NAME, value)


class PSwapPortfolioBasedQuirk(PortfolioSwapAddInfoBasedQuirk):

    """
    A generic quirk representing an attribute
    stored on the swap portfolio (or fund portfolio,
    stock portfolio, etc.) of a portfolio swap.
    """

    def get_acm_object(self, acm_portfolio_swap):
        return acm_portfolio_swap.FundPortfolio()


class PSwapOnPremIndSpotPriceBasedQuirk(PortfolioSwapAddInfoBasedQuirk):

    """
    A generic quirk representing the value stored on the SPOT price
    of the overnight premium rate index of a portfolio swap.
    """

    ADD_INFO_NAME = "PSONPremIndex"


    def get_spot_price(self, acm_portfolio_swap):
        """
        Return the SPOT price of the rate index
        referenced from the provided portfolio swap
        which stores the overnight premium spreads.
        """
        acm_rate_index = super(PSwapOnPremIndSpotPriceBasedQuirk,
                               self).getvalue(acm_portfolio_swap)
        if acm_rate_index:
            return acm_rate_index.PriceFromMarket("SPOT")
        else:
            return None


    def getvalue(self, acm_portfolio_swap):
        raise NotImplementedError


    def setvalue(self, acm_portfolio_swap, value):
        raise NotImplementedError


class ExternalId1BasedQuirk(QuirkAttribute):

    """
    A generic quirk representing an attribute
    stored in ExternalId1 field on an instrument.
    """

    INSTRUMENT_ATTR_NAME = None


    def get_instrument(self):
        """
        Return an acm instrument holding the value represented by this quirk.
        """
        import acm
        instrument_name = getattr(self.pb_fund, self.INSTRUMENT_ATTR_NAME)
        if instrument_name is None:
            return None
        else:
            return acm.FInstrument[instrument_name]


    def getvalue(self):
        acm_instrument = self.get_instrument()
        if acm_instrument is None:
            return None
        else:
            return acm_instrument.ExternalId1()


    def setvalue(self, value):
        acm_instrument = self.get_instrument()
        if acm_instrument is None:
            raise NotImplementedError
        acm_instrument.ExternalId1(value)


class AddInfoBasedQuirk(QuirkAttribute):

    """
    A generic quirk representing an attribute stored in an additional info.
    """

    ADD_INFO_NAME = None


    def get_acm_object(self):
        """
        Return an acm object holding the additional info
        that is used by this quirk.
        """
        raise NotImplementedError


    def getvalue(self):
        # This import requires acm,
        # so it has been moved here.
        from at_addInfo import get_value
        acm_object = self.get_acm_object()
        if acm_object is None:
            return None
        return get_value(acm_object, self.ADD_INFO_NAME)


    def setvalue(self, value):
        # This import requires acm,
        # so it has been moved here.
        from at_addInfo import save_or_delete
        acm_object = self.get_acm_object()
        if acm_object is None:
            raise NotImplementedError
        save_or_delete(acm_object, self.ADD_INFO_NAME, value)


class CounterpartyBasedQuirk(AddInfoBasedQuirk):

    """
    A generic addinfo-based quirk stored on the main fund's counterparty.
    """

    def get_acm_object(self):
        from PS_Functions import get_pb_fund_counterparty
        return get_pb_fund_counterparty(self.pb_fund.fund_id)


    def getvalue(self):
        value = super(CounterpartyBasedQuirk, self).getvalue()
        if value is None:
            return value
        else:
            return value.Name()


class DepositRateIndexBasedQuirk(AddInfoBasedQuirk):

    """
    A generic addinfo-based quirk stored on a deposit instrument.
    """

    DEPOSIT_ATTR_NAME = None


    def get_acm_object(self):
        import acm
        deposit_name = getattr(self.pb_fund, self.DEPOSIT_ATTR_NAME)
        if deposit_name is None:
            return None
        else:
            return acm.FDeposit[deposit_name]


# the actual quirks


class CounterpartyQuirk(QuirkAttribute):

    """
    A read-only quirk representing the prime brokerage fund's main counterparty.
    """

    def getvalue(self):
        from PS_Functions import get_pb_fund_counterparty
        return get_pb_fund_counterparty(self.pb_fund.fund_id).Name()


class ReportingPortfolioQuirk(CounterpartyBasedQuirk):

    """
    A quirk representing the prime brokerage fund's reporting portfolio.
    """

    ADD_INFO_NAME = "PB_Reporting_Prf"


class CollateralPortfolioQuirk(CounterpartyBasedQuirk):

    """
    A quirk representing the prime brokerage fund's collateral portfolio.
    """

    ADD_INFO_NAME = "PB_Collateral_Prf"


class CallAccountQuirk(CounterpartyBasedQuirk):

    """
    A quirk representing the prime brokerage fund's call account.
    """

    ADD_INFO_NAME = "PB_Call_Account"


class CallAccountNumberQuirk(QuirkAttribute):

    """
    A read-only quirk representing the prime brokerage fund's
    call account number.
    """

    def getvalue(self):
        import acm
        from PS_Functions import get_instrument_trade
        instrument_name = getattr(self.pb_fund, "call_account")
        acm_instrument = acm.FInstrument[instrument_name]
        if acm_instrument is None:
            return None
        else:
            acm_trade = get_instrument_trade(acm_instrument)
            return acm_trade.Oid()


class CallAccountRateIndexQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    call account rate index.
    """

    ADD_INFO_NAME = "CallFloatRef"
    DEPOSIT_ATTR_NAME = "call_account"


class CallAccountSpreadQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    call account spread.
    """

    ADD_INFO_NAME = "CallFloatSpread"
    DEPOSIT_ATTR_NAME = "call_account"


class LoanAccountQuirk(CounterpartyBasedQuirk):

    """
    A quirk representing the prime brokerage fund's loan account.
    """

    ADD_INFO_NAME = "PB_Loan_Account"


class LoanAccountRateIndexQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    loan account rate index.
    """

    ADD_INFO_NAME = "CallFloatRef"
    DEPOSIT_ATTR_NAME = "loan_account"


class LoanAccountSpreadQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    loan account spread.
    """

    ADD_INFO_NAME = "CallFloatSpread"
    DEPOSIT_ATTR_NAME = "loan_account"


class CommoditiesCallAccountQuirk(CounterpartyBasedQuirk):

    """
    A quirk representing the prime brokerage fund's commodities call account.
    """

    ADD_INFO_NAME = "PB_APD_call_acc"


class CommoditiesCallAccountRateIndexQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    commodities call account's rate index.
    """

    ADD_INFO_NAME = "CallFloatRef"
    DEPOSIT_ATTR_NAME = "commodities_call_account"


class CommoditiesCallAccountSpreadQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    commodities call account's spread.
    """

    ADD_INFO_NAME = "CallFloatSpread"
    DEPOSIT_ATTR_NAME = "commodities_call_account"


class CommoditiesCodeQuirk(ExternalId1BasedQuirk):

    """
    A quirk representing the prime brokerage fund's commodities code.
    """

    INSTRUMENT_ATTR_NAME = "commodities_call_account"


class SafexCallAccountQuirk(CounterpartyBasedQuirk):

    """
    A quirk representing the prime brokerage fund's Safex call account.
    """

    ADD_INFO_NAME = "PB_SAFEX_call_acc"


class SafexCallAccountRateIndexQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    Safex call account's rate index.
    """

    ADD_INFO_NAME = "CallFloatRef"
    DEPOSIT_ATTR_NAME = "safex_call_account"


class SafexCallAccountSpreadQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    Safex call account's spread.
    """

    ADD_INFO_NAME = "CallFloatSpread"
    DEPOSIT_ATTR_NAME = "safex_call_account"


class SafexCodeQuirk(ExternalId1BasedQuirk):

    """
    A quirk representing the prime brokerage fund's Safex code.
    """

    INSTRUMENT_ATTR_NAME = "safex_call_account"


class YieldXCallAccountQuirk(CounterpartyBasedQuirk):

    """
    A quirk representing the prime brokerage fund's Yield-X call account.
    """

    ADD_INFO_NAME = "PB_YieldX_call_acc"


class YieldXCallAccountRateIndexQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    Yield-X call account's rate index.
    """

    ADD_INFO_NAME = "CallFloatRef"
    DEPOSIT_ATTR_NAME = "yieldx_call_account"


class YieldXCallAccountSpreadQuirk(DepositRateIndexBasedQuirk):

    """
    A quirk representing the prime brokerage fund's
    Yield-X call account's spread.
    """

    ADD_INFO_NAME = "CallFloatSpread"
    DEPOSIT_ATTR_NAME = "yieldx_call_account"


class YieldXCodeQuirk(ExternalId1BasedQuirk):

    """
    A quirk representing the prime brokerage fund's Yield-X code.
    """

    INSTRUMENT_ATTR_NAME = "yieldx_call_account"


# portfolio swap based quirks


class PortfolioSwapQuirk(PortfolioSwapBasedQuirk):

    """
    A read-only quirk representing the portfolio swap.
    """

    def getvalue(self, acm_portfolio_swap):
        return acm_portfolio_swap.Name()


class PortfolioSwapStartDateQuirk(PortfolioSwapBasedQuirk):

    """
    A quirk representing the start date of a portfolio swap.
    """

    def getvalue(self, acm_portfolio_swap):
        return acm_portfolio_swap.StartDate()


    def setvalue(self, acm_portfolio_swap, value):
        return acm_portfolio_swap.StartDate(value)


class PortfolioSwapPortfolioQuirk(PSwapPortfolioBasedQuirk):

    """
    A quirk representing the swap portfolio
    (or fund portfolio, stock portfolio, etc.) of a portfolio swap.
    """

    def getvalue(self, acm_portfolio_swap):
        swap_portfolio = self.get_acm_object(acm_portfolio_swap)
        if swap_portfolio:
            return swap_portfolio.Name()
        else:
            return None


    def setvalue(self, acm_portfolio_swap, value):
        acm_portfolio_swap.FundPortfolio(value)


class PortfolioSwapExecutionRateDMAQuirk(PSwapPortfolioBasedQuirk):

    """
    A quirk representing the DMA execution rate
    stored on a swap portfolio (or fund portfolio,
    stock portfolio, etc.) of a portfolio swap.
    """

    ADD_INFO_NAME = "PSExtExecPremRate"


class PortfolioSwapExecutionRateNonDMAQuirk(PSwapPortfolioBasedQuirk):

    """
    A quirk representing the non-DMA execution rate
    stored on a swap portfolio (or fund portfolio,
    stock portfolio, etc.) of a portfolio swap.
    """

    ADD_INFO_NAME = "PSExtExecPremNonDMA"


class PortfolioSwapExecutionRateVoiceQuirk(PSwapPortfolioBasedQuirk):

    """
    A quirk representing the voice execution rate
    stored on a swap portfolio (or fund portfolio,
    stock portfolio, etc.) of a portfolio swap.
    """

    ADD_INFO_NAME = "PSExtExecPremVoice"


class PortfolioSwapSimpleRateFactorQuirk(PSwapPortfolioBasedQuirk):

    """
    A quirk representing the simple rate factor
    stored on a swap portfolio (or fund portfolio,
    stock portfolio, etc.) of a portfolio swap.
    """

    ADD_INFO_NAME = "PSSimpleRateFactor"


class PortfolioSwapSweepingClassQuirk(PortfolioSwapAddInfoBasedQuirk):

    """
    A quirk representing the sweeping class of a portfolio swap.
    """

    ADD_INFO_NAME = "PB_Sweeping_Class"


class PortfolioSwapFullyFundedQuirk(PortfolioSwapAddInfoBasedQuirk):

    """
    A quirk representing the fully funded flag of a portfolio swap.
    """

    ADD_INFO_NAME = "PB_PS_Fully_Funded"


class PortfolioSwapOvernightPremiumIndexQuirk(PortfolioSwapAddInfoBasedQuirk):

    """
    A quirk representing the overnight premium rate index of a portfolio swap.
    """

    ADD_INFO_NAME = "PSONPremIndex"


    def getvalue(self, acm_portfolio_swap):
        # This import requires acm,
        # so it has been moved here.
        from at_addInfo import get_value
        acm_rate_index = get_value(acm_portfolio_swap, self.ADD_INFO_NAME)
        if acm_rate_index:
            return acm_rate_index.Name()
        else:
            return None


class PSwapOvernightPremiumSpreadLongQuirk(PSwapOnPremIndSpotPriceBasedQuirk):

    """
    A quirk representing the long overnight premium spread
    of a portfolio swap.
    """

    def getvalue(self, acm_portfolio_swap):
        spot_price = self.get_spot_price(acm_portfolio_swap)
        if spot_price:
            return spot_price.Bid()
        else:
            return None


    def setvalue(self, acm_portfolio_swap, value):
        spot_price = self.get_spot_price(acm_portfolio_swap)
        if not spot_price:
            raise NotImplementedError
        spot_price.Bid(value)
        spot_price.Commit()


class PSwapOvernightPremiumSpreadShortQuirk(PSwapOnPremIndSpotPriceBasedQuirk):

    """
    A quirk representing the short overnight premium spread
    of a portfolio swap.
    """

    def getvalue(self, acm_portfolio_swap):
        spot_price = self.get_spot_price(acm_portfolio_swap)
        if spot_price:
            return spot_price.Ask()
        else:
            return None


    def setvalue(self, acm_portfolio_swap, value):
        spot_price = self.get_spot_price(acm_portfolio_swap)
        if not spot_price:
            raise NotImplementedError
        spot_price.Ask(value)
        spot_price.Commit()


class PortfolioSwapShortPremiumTypeQuirk(PortfolioSwapAddInfoBasedQuirk):

    """
    A quirk representing the short premium type of a portfolio swap.
    """

    ADD_INFO_NAME = "PSShortPremiumType"


class PortfolioSwapShortPremiumRateQuirk(PortfolioSwapAddInfoBasedQuirk):

    """
    A quirk representing the short premium rate of a portfolio swap.
    """

    ADD_INFO_NAME = "PSShortPremRate"


class PortfolioSwapSweepingBaseDayQuirk(PortfolioSwapAddInfoBasedQuirk):

    """
    A quirk representing the sweeping base day of a portfolio swap.
    """

    ADD_INFO_NAME = "PSSweepBaseDay"


class PortfolioSwapSweepingFrequencyQuirk(PortfolioSwapAddInfoBasedQuirk):

    """
    A quirk representing the sweeping frequency of a portfolio swap.
    """

    ADD_INFO_NAME = "PSSweepFreq"


# portfolio swap name based suggestion quirks


class PortfolioSwapNameSQuirk(PortfolioSwapSuggestionQuirk):

    """
    A read-only suggestion quirk representing the name
    of a portfolio swap.
    """

    def getvalue(self, sweeping_class, fully_funded):
        return self.pb_fund.get_pswap_name(sweeping_class, fully_funded)


class PortfolioSwapStartDateSQuirk(PortfolioSwapSuggestionQuirk):

    """
    A read-only suggestion quirk representing the start date
    of a portfolio swap.
    """

    def getvalue(self, sweeping_class, fully_funded):
        from datetime import date
        return date.today().isoformat()


class PortfolioSwapPortfolioSQuirk(PortfolioSwapSuggestionQuirk):

    """
    A read-only suggestion quirk representing the name
    of the swap portfolio of a portfolio swap.
    """

    def getvalue(self, sweeping_class, fully_funded):
        return self.pb_fund.get_pswap_swap_portfolio_name(sweeping_class,
                                                          fully_funded)


class PortfolioSwapTradePortfolioSQuirk(PortfolioSwapSuggestionQuirk):

    """
    A read-only suggestion quirk representing the name of a portfolio
    of the only confirmed trade of a portfolio swap.
    """

    def getvalue(self, sweeping_class, fully_funded):
        return self.pb_fund.get_pswap_trade_portfolio_name(sweeping_class,
                                                           fully_funded)


class PortfolioSwapTradeStatusSQuirk(PortfolioSwapSuggestionQuirk):

    """
    A read-only suggestion quirk representing the status
    of the only confirmed trade of a portfolio swap.
    """

    def getvalue(self, sweeping_class, fully_funded):
        return "FO Confirmed"


# utility functions


def get_attribute_quirks(pb_fund):
    """
    Return a dictionary of all the available
    attribute quirks indexed by their ID.

    They will be initialized with a reference
    to the provided prime brokerage fund.
    """
    attribute_quirks = {}
    attribute_quirks["counterparty"] = CounterpartyQuirk(pb_fund)
    attribute_quirks["reporting_portfolio"] = ReportingPortfolioQuirk(pb_fund)
    attribute_quirks["collateral_portfolio"] = CollateralPortfolioQuirk(pb_fund)
    attribute_quirks["call_account"] = CallAccountQuirk(pb_fund)
    attribute_quirks["call_account_number"] = CallAccountNumberQuirk(pb_fund)
    attribute_quirks["call_account_rate_index"] = CallAccountRateIndexQuirk(pb_fund)
    attribute_quirks["call_account_spread"] = CallAccountSpreadQuirk(pb_fund)
    attribute_quirks["loan_account"] = LoanAccountQuirk(pb_fund)
    attribute_quirks["loan_account_rate_index"] = LoanAccountRateIndexQuirk(pb_fund)
    attribute_quirks["loan_account_spread"] = LoanAccountSpreadQuirk(pb_fund)
    attribute_quirks["commodities_call_account"] = CommoditiesCallAccountQuirk(pb_fund)
    attribute_quirks["commodities_call_account_rate_index"] = CommoditiesCallAccountRateIndexQuirk(pb_fund)
    attribute_quirks["commodities_call_account_spread"] = CommoditiesCallAccountSpreadQuirk(pb_fund)
    attribute_quirks["commodities_code"] = CommoditiesCodeQuirk(pb_fund)
    attribute_quirks["safex_call_account"] = SafexCallAccountQuirk(pb_fund)
    attribute_quirks["safex_call_account_rate_index"] = SafexCallAccountRateIndexQuirk(pb_fund)
    attribute_quirks["safex_call_account_spread"] = SafexCallAccountSpreadQuirk(pb_fund)
    attribute_quirks["safex_code"] = SafexCodeQuirk(pb_fund)
    attribute_quirks["yieldx_call_account"] = YieldXCallAccountQuirk(pb_fund)
    attribute_quirks["yieldx_call_account_rate_index"] = YieldXCallAccountRateIndexQuirk(pb_fund)
    attribute_quirks["yieldx_call_account_spread"] = YieldXCallAccountSpreadQuirk(pb_fund)
    attribute_quirks["yieldx_code"] = YieldXCodeQuirk(pb_fund)
    # portfolio-swap-based quirks
    attribute_quirks["ps_pswap"] = PortfolioSwapQuirk(pb_fund)
    attribute_quirks["ps_start_date"] = PortfolioSwapStartDateQuirk(pb_fund)
    attribute_quirks["ps_swap_portfolio"] = PortfolioSwapPortfolioQuirk(pb_fund)
    attribute_quirks["ps_execution_rate_dma"] = PortfolioSwapExecutionRateDMAQuirk(pb_fund)
    attribute_quirks["ps_execution_rate_nondma"] = PortfolioSwapExecutionRateNonDMAQuirk(pb_fund)
    attribute_quirks["ps_execution_rate_voice"] = PortfolioSwapExecutionRateVoiceQuirk(pb_fund)
    attribute_quirks["ps_sweeping_class"] = PortfolioSwapSweepingClassQuirk(pb_fund)
    attribute_quirks["ps_fully_funded"] = PortfolioSwapFullyFundedQuirk(pb_fund)
    attribute_quirks["ps_ov_prem_index"] = PortfolioSwapOvernightPremiumIndexQuirk(pb_fund)
    attribute_quirks["ps_ov_prem_spread_long"] = PSwapOvernightPremiumSpreadLongQuirk(pb_fund)
    attribute_quirks["ps_ov_prem_spread_short"] = PSwapOvernightPremiumSpreadShortQuirk(pb_fund)
    attribute_quirks["ps_short_premium_type"] = PortfolioSwapShortPremiumTypeQuirk(pb_fund)
    attribute_quirks["ps_short_premium_rate"] = PortfolioSwapShortPremiumRateQuirk(pb_fund)
    attribute_quirks["ps_simple_rate_factor"] = PortfolioSwapSimpleRateFactorQuirk(pb_fund)
    attribute_quirks["ps_sweeping_base_day"] = PortfolioSwapSweepingBaseDayQuirk(pb_fund)
    attribute_quirks["ps_sweeping_frequency"] = PortfolioSwapSweepingFrequencyQuirk(pb_fund)
    return attribute_quirks


def get_suggestion_quirks(pb_fund):
    """
    Return a dictionary of all the available
    suggestion quirks indexed by their ID.

    They will be initialized with a reference
    to the provided prime brokerage fund.
    """
    suggestion_quirks = {}
    suggestion_quirks["ps_pswap"] = PortfolioSwapNameSQuirk(pb_fund)
    suggestion_quirks["ps_start_date"] = PortfolioSwapStartDateSQuirk(pb_fund)
    suggestion_quirks["ps_swap_portfolio"] = PortfolioSwapPortfolioSQuirk(pb_fund)
    suggestion_quirks["ps_pswap_trade_portfolio"] = PortfolioSwapTradePortfolioSQuirk(pb_fund)
    suggestion_quirks["ps_pswap_trade_status"] = PortfolioSwapTradeStatusSQuirk(pb_fund)
    return suggestion_quirks
