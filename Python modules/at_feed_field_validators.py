"""
Part of the AT Feed processing framework providing validation functionality.

Provides validators for primitive types as well as ACM entities and helper
functions for validation configuration.
"""

import acm


def instrument_validator(ins_id):
    """Checks if an instrument exists for ins_id"""
    instr = acm.FInstrument[ins_id]
    if instr is None:
        raise ValueError("The instrument [%s] does not exist" % (ins_id))
    return instr


def portfolio_validator(portfolio_id):
    """Checks if a portfolio exists for portfolio_id"""
    portfolio = acm.FPhysicalPortfolio[portfolio_id]
    if portfolio is None:
        raise ValueError("The portfolio [%s] does not exist" % (portfolio_id))
    return portfolio


def party_validator(party_id):
    """Checks if a party exists for party_id"""
    party = acm.FParty[party_id]
    if party is None:
        raise ValueError("The party [%s] does not exist" % (party_id))
    return party


# Dictionary of available validators of ACM entities
_acm_validators = {
    acm.FInstrument: instrument_validator,
    acm.FPhysicalPortfolio: portfolio_validator,
    acm.FParty: party_validator,
}


def create_type_validator(v_type, replace=True):
    """Helper function that simplifies validator configuration

        Replace defaults to true, because it almost always makes
        sense to replace the string values in the records
        to objects of appropriate types.
    """

    validator = None

    if v_type in (int, str, float):
        validator = v_type
    elif v_type in list(_acm_validators.keys()):
        validator = _acm_validators[v_type]
    else:
        raise TypeError('Validator for type %s is not implemented' %
                        type(v_type))

    return {
        'validator': validator,
        'replace': replace
    }


def custom_validator_function(validator, replace=True):
    return {
        'validator': validator,
        'replace': replace
    }
