"""Deprecated FValidation module.

This module contains rules that have not (yet) been fully refactored
and integrated into the new FValidation modules.  No new rules should
be added to this module, only hotfixes if necessary.


Purpose               : This updates the necessary additional info fields when a SL Trade is booked
Department and Desk   : Securities Lending Desk
Requester             : Linda Breytenbach
Developer             : Rohan vd Walt
CR Number             : 816158
=============================================================================
Date       Change no Developer              Description
-----------------------------------------------------------------------------
2011-11-15 829804    Rohan van der Walt     Fix issue where consecutive trade booking of SL causes Trade number not to show/open.
2011-11-22 837244    Rohan van der Walt     Fix issue where partial return booking didn't copy additional infos to new trade correctly.
2012-11-08 582907    Hynek Urban            Use the correct minimum fee rate when validating. Minor refactors.
2012-11-23 612553    Kenneth Danielsson     Pension Fund Fee Split: fixed rate set to lender fee security loans
2013-02-07 785557    Kenneth Danielsson     Dont recalculate and change lender fee when using partial return functionality.
2014-08-31 CHNG0002210109 Vojtech Sidorin   Mark as deprecated module
2014-11-07           Manan Ghosh            Change to the update trade logic to block the Fee to be updated of the
                                            G1 Fee calculated is same as the Leg fixed rate. This is to prevent
                                            fee being split repeatedly if update is invoked multiple times.
2015-08-20           Vojtech Sidorin        ABITFA-3743: Include rule numbers in messages.
2017-03-10           Matthew French         Resolve 2017.2 missing dependency (so we can run aggregation on new version).
2020-02-25           Sihle Gaxa             Bypass fee validation for full return trades, which dont have fees on them
-----------------------------------------------------------------------------
"""

import ael, acm


from FValidation_core import (ValidationError,
                              validate_entity, validate_transaction)

INT_PROC_GROUP = ael.Group['Integration Process']
SYS_PROC_GROUP = ael.Group['System Processes']
BACKEND_USERGROUPS = [INT_PROC_GROUP, SYS_PROC_GROUP]


def _get_min_fee_field(trade):
    """
    Copied from 2017.1 Securities Lending extension module
    """
    if trade.Instrument().UnderlyingType() == 'Bond':
        return 'SL_LenderMinFee_Bd'
    return 'SL_LenderMinFee_Eq'
    
    
def calculateLenderCalculatedFee(e):
    """
    Calculates the lending feed based on Lender
    of the Security Loan trade.
    """

    ailist = ['SL_G1Counterparty2']
    aiDict = getAddInfos(e, ailist)
    val = None
    fixed_rate = 0.0
    
    # Upgrade 2017: FAU-2953:
    # Trades with 'PARTIAL_RETURN' don't change fees
    # Full return trades have no fees
    if not e.text1 in ["PARTIAL_RETURN", "FULL_RETURN"] and aiDict['SL_G1Counterparty2']:
        lender = ael.Party[aiDict['SL_G1Counterparty2']]
        if lender:
            min_fee_field = _get_min_fee_field(acm.FTrade[e.trdnbr])
            ailist = [min_fee_field, 'SL_LenderSplitFee']
            aiDict = getAddInfos(lender, ailist)
            mf = float(aiDict[min_fee_field])
            sf = float(aiDict['SL_LenderSplitFee'])

            if mf != 0 and sf != 0:
                # Calculates the fee if the Minimum fee and Split fee is populated
                for leg in e.insaddr.legs():
                    if leg.payleg:
                        fixed_rate = leg.fixed_rate
                        if fixed_rate != 0 and fixed_rate < mf:
                            raise Exception("CLCF1: Trade not allowed at current fee:"
                                            " Trade fee less than lender's minimum fee")
                val = max(mf, (sf / 100) * fixed_rate)
            elif mf != 0:
                # Calculates the fee if the Minimum fee is populated only
                for leg in e.insaddr.legs():
                    if leg.payleg:
                        fixed_rate = leg.fixed_rate
                        if fixed_rate != 0 and fixed_rate < mf:
                            raise Exception("CLCF2: Trade not allowed at current fee:"
                                            " Trade fee less than lender's minimum fee")
                val = mf
            else:
                val = None

    return val, fixed_rate


def getAddInfos(e, ailist):
    result = dict(list(zip(ailist,[0]*len(ailist))))
    ael.poll()
    for ai in e.additional_infos():
        specnbr = ai.addinf_specnbr
        for requiredAI in ailist:
            if specnbr and specnbr.field_name == requiredAI:
                result[requiredAI] = str(ai.value)
    return result


def process_insert_sl_trade(e, op):
    """Validate SL trade - insert Trade."""
    if ael.user().grpnbr not in BACKEND_USERGROUPS:
        if e.insaddr.instype == 'SecurityLoan':
            val, fixed_rate = calculateLenderCalculatedFee(e)
            if val != None:
                for ai in e.additional_infos():
                    specnbr = ai.addinf_specnbr
                    if specnbr and specnbr.field_name == 'SL_G1Fee2':
                        ai_new = ai
                        break
                else:
                    ai_new = ael.AdditionalInfo.new(e)
                    ais = ael.AdditionalInfoSpec['SL_G1Fee2']
                    ai_new.addinf_specnbr = ais.specnbr

                if ai_new:
                    ai_new.value = str(val)



# Rule 99
@validate_entity("Instrument", "Update", caller="validate_transaction")
def process_update_sl_ins(e, op):
    """Validate SL trade - update Instrument."""
    if ael.user().grpnbr not in BACKEND_USERGROUPS:
        if e.instype == 'SecurityLoan':
            for t in e.original().trades():
                ailist = ['SL_G1Counterparty2']
                aiDict = getAddInfos(t, ailist)
                if aiDict['SL_G1Counterparty2']:
                    lender = ael.Party[aiDict['SL_G1Counterparty2']]
                    if lender:
                        min_fee_field = _get_min_fee_field(acm.FTrade[t.trdnbr])
                        ailist = [min_fee_field]
                        aiDict = getAddInfos(lender, ailist)
                        mf = float(aiDict[min_fee_field])
                        fixedRate = 0
                        for leg in e.legs():
                            if leg.payleg:
                                fixedRate = leg.fixed_rate
                                if fixedRate != 0 and fixedRate < mf:
                                    raise Exception("FV99: Trade not allowed at current fee:"
                                                    " Trade fee less than lender's minimum fee")


def process_insert_sl_trade2(transaction_list,e, op):
    """Validate SL trade - insert Trade."""
    if ael.user().grpnbr not in BACKEND_USERGROUPS:
        if e.insaddr.instype == 'SecurityLoan':
            val, fixed_rate = calculateLenderCalculatedFee(e)
            if val != None:
                for ai in e.additional_infos():
                    specnbr = ai.addinf_specnbr
                    if specnbr and specnbr.field_name == 'SL_G1Fee2':
                        ai_new = ai
                        break
                else:
                    ai_new = ael.AdditionalInfo.new(e)
                    ais = ael.AdditionalInfoSpec['SL_G1Fee2']
                    ai_new.addinf_specnbr = ais.specnbr

                if ai_new:
                    ai_new.value = str(val)

                for l in e.insaddr.legs():
                    lclone = l.clone()
                    lclone.fixed_rate = val
                    transaction_list.append((lclone, "Update"))

                    for cf in l.cash_flows():
                        cfclone = cf.clone()
                        cfclone.rate = val
                        transaction_list.append((cfclone,"Update"))
    return transaction_list
