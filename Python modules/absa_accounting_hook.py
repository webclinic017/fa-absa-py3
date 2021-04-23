"""AEL Accounting Hook - include custom payments in TPL calculations.

This module contains a hook function fee_alloc_method that determines
which fee allocation method will be used for a given custom payment in
the TPL calculations.

History
=======

2015-01-20 Vojtech Sidorin      ABITFA-3130     Initial implementation
2015-10-07 Bhavnisha Sarawan    ABITFA-3708     Added committment fee to realise on trade day
2018-12-08 Jaco Swanepoel       Prime Broking aggregation       Include payments SET, INS, STT, DWT, Brokerage Vatable into cash
2019-02-07 Jakub Tomaga         FAPE-49         Move is_child_portf from PS_Function here to fix the problem with ATS version prior to upgrade.
2019-02-15 Jaco Swanepoel       Prime Broking aggregation       Include payments new Execution Fee payment type into cash
"""

import ael, acm

prime_portfolio = acm.FCompoundPortfolio['PB_CR_LIVE']


def is_child_portf(portfolio, parent_portfolio):
    """Return True if portfolio is a give of given parent."""
    parent = portfolio
    while True:
        current_portfolio = parent
        member_links = current_portfolio.MemberLinks()
        parent_links = [link for link in member_links
                        if link.MemberPortfolio() == current_portfolio]
        if not parent_links:
            return False
        parent = parent_links[0].OwnerPortfolio()
        if not parent:
            return False
        if parent == parent_portfolio:
            return True
    return False


def fee_alloc_method(payment, accpar):
    """Hook function: Return method to use for TPL calculations.

    Positional arguments:
    payment -- (ael entity Payment) Payment that Profit and Loss is
               calculated for.
    accpar -- (ael entity AccountingParameters) Accounting Parameters
              in which the hook module is defined.

    Return integer representing the method to use for TPL calculations.
    """
    # ABITFA-3130: Dividend Adjustment payments.
    if payment.type == "Dividend Adjustment":
        return ael.enum_from_string("FeeAllocMethod", "As Fee on Pay Day")
    # ABITFA-3780: Commitment Fee.
    if payment.type == "Commitment Fee":
        return ael.enum_from_string("FeeAllocMethod", "As Fee on Trade Day")
    # ABITFA-5183: CFC Interest.
    if payment.type == "CFC Interest":
        return ael.enum_from_string("FeeAllocMethod", "As Fee on Trade Day")
    # ABITFA-5234: RTM Dividend Suppression.
    if payment.type == "Dividend Suppression":
        return ael.enum_from_string("FeeAllocMethod", "As Dividend")
    # ABITFA-4721: Exchange Fee.
    if payment.type == "Exchange Fee":
        return ael.enum_from_string("FeeAllocMethod", "As Fee on Trade Day")
    # ABITFA-3780: Commitment Fee.
    if payment.type == "Utilisation Fee":
        return ael.enum_from_string("FeeAllocMethod", "As Fee on Trade Day")
    # Prime Broking aggregation
    if payment.type == "SET":
        return ael.enum_from_string("FeeAllocMethod", "As Fee on Trade Day")  
    # Prime Broking aggregation
    if payment.type == "INS":
        return ael.enum_from_string("FeeAllocMethod", "As Fee on Trade Day")  
    # Prime Broking aggregation
    if payment.type == "DWT":
        return ael.enum_from_string("FeeAllocMethod", "As Fee on Trade Day")
    
    # Prime Broking aggregation: 
    #   Include "Brokerage Vatable" and "STT" in cash for Prime Broking only!
    if payment.type == "Brokerage Vatable" or payment.type == "STT":
        try:
            trade = payment.trdnbr
            trade_prf = acm.FPhysicalPortfolio[trade.prfnbr.prfnbr]
            is_prime_trade = is_child_portf(trade_prf, prime_portfolio)
        
            if is_prime_trade:
                return ael.enum_from_string("FeeAllocMethod", "As Fee on Trade Day")
        except Exception as ex:
            return None

    # Prime Broking aggregation
    if payment.type == "Execution Fee":
        return ael.enum_from_string("FeeAllocMethod", "As Fee on Trade Day")

    # Do not include the custom payment by default.
    return None
