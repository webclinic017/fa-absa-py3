"""
FValidation_FINRA_Reporting

History
=======
2020-08-25 Snowy Mabilu ARR-60 - Validation rules for FINRA reporting
"""
import acm
import TRACEUtils

from FValidation_core import (
    validate_entity,
    validate_transaction,
    ValidationError,
    RegulationValidationError,
)


@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def rule_for_finra_trades(entity, operation):
    """
    Rule for checking if FINRA eligible trades are booked on instrument that are marked with the correct 
    FINRA identifier
    """
    trade = acm.Ael.AelToFObject(entity)
    if TRACEUtils.is_trace_eligble(trade) and not TRACEUtils.has_finra_identifier(trade.Instrument()):
        msg = "TRACE eligible trades need to have a valid FINRA symbol or CUSIP. Contact TCU for assistance"
        raise RegulationValidationError(msg)


@validate_entity("InstrumentAlias", "Update")
@validate_entity("InstrumentAlias", "Delete")
def rule_on_finra_instruments_alias(entity, operation):
    """
    Rule for prohibiting the amendment of FINRA identifier on an instrument.
    The instrument must be deleted and new one must be created.
    This is with accordance with requirement from FINRA which prohibits the amendment of symbols(FINRA_SYMBOL or CUSIP)
    once trades are reported.
    """
    alias = acm.Ael.AelToFObject(entity)
    if alias.Type().Name() in (TRACEUtils.FINRA_SYMBOL, TRACEUtils.CUSIP):
        instrument = alias.Instrument()
        if TRACEUtils.has_finra_identifier(instrument) and TRACEUtils.has_finra_live_trades(instrument):
            msg = "FINRA_SYMBOL or CUSIP should not be updated on instruments with FINRA reported trades. \n "
            "Please void all FINRA trades before updating the instrument."
            raise RegulationValidationError(msg)
