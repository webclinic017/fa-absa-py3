"""FValidation - Rules related to the Volcker Rule.

Please consult the Developer's Guide before changing the code:
<https://confluence.barcapint.com/display/ABCAPFA/FValidation+Developer%27s+Guide>.

The list of rules is available at
<http://confluence.barcapint.com/display/ABCAPFA/FValidation+Rules>.
Please keep it in sync with the code.


History
=======
2016-03-22 Vojtech Sidorin  Initial implementation; ABITFA-4064
"""

import acm

from FValidation_core import (
        validate_entity,
        RegulationValidationError,
        )
from at_portfolio import create_tree as create_port_tree


def is_us_party(party):
    """Return True if party is a US party in relation to the Volcker Rule."""
    return party.add_info("US_Party") == "Yes"


def is_restricted_port(portfolio):
    """Return True if portfolio is Volcker-restricted.

    Volcker-restricted portfolios are those in the tree under portfolio
    'Money Market Desk'.
    """
    MONEY_MARKET_OID = 915  # Money Market Desk
    money_market_port = acm.FPhysicalPortfolio[MONEY_MARKET_OID]
    money_market_tree = create_port_tree(money_market_port)
    return (portfolio.prfnbr == MONEY_MARKET_OID or
            money_market_tree.has(portfolio.prfid))


def has_us_repr_letter(party):
    """Return True if repr. letter exists in relation to the Volcker Rule.

    Return True if a valid representation letter exists for party.  The
    representation letter allows us to trade with US counterparties.
    """
    return party.add_info("US_Repr_Letter") == "Yes"


@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def fv128_restrict_trading_with_us_counterparties(entity, operation):
    """Restrict trading with US counterparties. (Volcker Rule)

    To trade with a US counterparty, there must be a valid representation
    letter allowing us to trade with the counterparty.
    """
    counterparty = entity.counterparty_ptynbr
    portfolio = entity.prfnbr
    if (is_us_party(counterparty) and is_restricted_port(portfolio) and
            not has_us_repr_letter(counterparty)):
        msg = ("FV128: Trade {0}: Trading forbidden (Volcker Rule). "
               "A valid representation letter is required to book trades with "
               "a US counterparty into a portfolio in the tree under "
               "'Money Market Desk'.".format(entity.trdnbr))
        raise RegulationValidationError(msg)
