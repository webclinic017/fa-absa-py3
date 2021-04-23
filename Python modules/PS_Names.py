"""-----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  Naming conventions for Prime Services.
DEPATMENT AND DESK      :  Middle Office
REQUESTER               :
DEVELOPER               :  Hynek Urban
CR NUMBER               :  1019492
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer              Description
--------------------------------------------------------------------------------
2013-16-05 1019492   Hynek urban           Initial Implementation


Functions used for getting names of different objects in the Prime Services space.

Since a lot of code and processes in Prime Brokerage depends on various naming
conventions, functions in this module try to summarize the logic around them.

"""

from PS_AssetClasses import COMMODITIES, SAFEX, YIELDX


def get_portfolio_name(product, client_name, cr=False, fullyfunded=False):
    """
    Get the name of the physical portfolio using the provided criteria.

    <product> is the given asset class.
    <client_name> is the client's short name.
    <cr> determines whether the portfolio is on the client reporting side of the tree.

    """
    ff_infix = 'FF' if fullyfunded else ''
    cr_suffix = 'CR' if cr else ''
    prf_infix = product.portfolio_infix
    name_parts = list(filter(bool, ['PB', prf_infix, ff_infix, client_name, cr_suffix]))
    return '_'.join(name_parts)


def get_portfolio_name_by_id(identifier, client_name, cr=False):
    """
    Get the name of the compound/physical portfolio using the provided criteria.
    
    <identifier> is one of [RISK_FV, RISK, AGENCY, FINANCED, FULLY_FUNDED, CALLACCNT, FINANCING, COLL]
    <client_name> is the client's short name
    <cr> determines whether the portfolio is on the client reporting side of the tree.
    """
    cr_suffix = 'CR' if cr else ''
    name_parts = list(filter(bool, ['PB', identifier, client_name, cr_suffix]))
    return '_'.join(name_parts)


def get_pswap_name(product, client_name, fully_funded=False):
    """
    Get the name of the PortfolioSwap using the provided criteria.

    <product> is the given asset class.
    <client_name> is the client's short name.

    """
    ff_infix = 'FF' if fully_funded else ''
    name_parts = list(filter(bool, ['PB', client_name, ff_infix, product.pswap_suffix]))
    return '_'.join(name_parts)


CALLACCNT_GENERAL = 'CallAcc'
CALLACCNT_LOAN = 'Loan'
CALLACCNT_COMMODITIES = 'CallAcc_APD'
CALLACCNT_SAFEX = 'CallAcc_Safex'
CALLACCNT_YIELDX = 'CallAcc_Yieldx'
CALLACCNT_TYPES = (CALLACCNT_GENERAL,
                   CALLACCNT_LOAN,
                   CALLACCNT_COMMODITIES,
                   CALLACCNT_SAFEX,
                   CALLACCNT_YIELDX)


def get_callaccnt_name(client_name, type_):
    """Get the name of client's call account of the given type."""
    if type_ not in CALLACCNT_TYPES:
        raise ValueError('Unknown call account type: %s.' % type_)
    return 'ZAR/%s_%s' % (client_name, type_)


def get_rate_index_name(product, client_name, fullyfunded):
    """
    Get the name of the rate index using the provided criteria.

    <product> is the given asset class.
    <client_name> is the client's short name.

    """
    if fullyfunded:
        return 'Overnight-ZAR-CFD-ZERO'
    if product in (COMMODITIES, SAFEX, YIELDX):
        return 'ZAR-CFD-ZERO'
    return 'Overnight-%s_%s' % (client_name, product.index_suffix)


def get_pswap_portfolio_name(short_name):
    """Get name of the client's portfolioswap portfolio."""
    return '_'.join(['PB_PSWAP', short_name, 'CR'])


def get_top_cr_portfolio_name(short_name):
    """Get the name of the top-level CR portfolio for the given client."""
    return 'PB_%s_CR' % short_name


def get_top_coll_portfolio_name(short_name):
    """Get the name of the top-level COLL portfolio for the given client."""
    return 'PB_COLL_%s_CR' % short_name


def get_call_accnt_portfolio_name(short_name):
    """Get the name of the _CALLACCNT_ portfolio for the given client."""
    return 'PB_CALLACCNT_%s' % short_name


def get_call_margin_trdnbr(short_name):
    """
    Get the trade number of the call margin account
    for the given client.
    """
    prf_name = get_call_accnt_portfolio_name(short_name)
    import acm
    prf = acm.FPhysicalPortfolio[prf_name]
    try:
        return prf.Trades()[0].Oid()
    except IndexError:
        # This should actually never happen, because the trade is created in the
        # PS_MO_Onboarding script.
        raise RuntimeError('No call margin account trade found!')
