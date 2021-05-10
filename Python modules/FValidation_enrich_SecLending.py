"""Enrichment rules related to Security Loans.

History
=======

2014-11-12 Nada Jasikova   CHNG0002443195 Rule 116 - counterparty auto-population
2015-02-06 Manan Ghosh     CHNG0002570575 Rule 98 - moved from FValidation_depr_SecLending to this module
2015-08-20 Vojtech Sidorin ABITFA-3743: Include rule numbers in messages.
2020-01-06 Bhavnisha Sarawan Update Trade settle category based on SL_SWIFT
2020-05-25 Bhavnisha Sarawan Remove functions to change counterparty and give ID to previous change
2020-06-03 Libor Svoboda     Remove redundant SBL Fee validation
"""
import acm
from FValidation_core import validate_transaction, validate_entity


@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def set_trade_settle_category(entity, operation):
    """ FV116a and FV116b Update Trade settle category based on SL_SWIFT """
    trade = entity
    if trade.add_info('SL_SWIFT') == "SWIFT":
        trade.settle_category_chlnbr = acm.FChoiceList.Select01(
        "list = 'TradeSettleCategory' and name='SL_STRATE'",
          'FV116a: Error trying to retrieve SL_STRATE settle category choicelist').Oid()

    if trade.add_info('SL_SWIFT') == "DOM":
        trade.settle_category_chlnbr = acm.FChoiceList.Select01(
        "list = 'TradeSettleCategory' and name='SL_CUSTODIAN'",
          'FV116b: Error trying to retrieve SL_CUSTODIAN settle category choicelist').Oid()

