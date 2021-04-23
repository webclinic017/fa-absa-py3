"""FMirror - This module implements the mirrored_trade hook function.

See FCA4033 (AEF Browser) and/or FCA3724 (AEF Basic Extensions) for
documentation.

The list of implemented FMirror rules is kept at
<https://confluence.barcapint.com/display/ABCAPFA/FMirror+rules>.
Please keep it in sync with the code.


History
=======

2012-03-28 Willie van der Bank  Updated to correctly handle sales credits.
2012-05-17 Anwar Banoo          193543 - Added try catch block when checking add infos on mirror trade.
2015-04-30 Nada Jasikova        Fix ValueAdd cleanup.
2015-04-30 Nada Jasikova        Portfolio mismatch hotfix.
2015-06-18 Juraj Balazs         Setting YourRef on mirror trades created automatically when a constellation is committed (4Front only).
2017-03-21 Vojtech Sidorin      Label rules and describe them at <https://confluence.barcapint.com/display/ABCAPFA/FMirror+rules>.
2017-05-10 Vojtech Sidorin      FAU-768: Remove the portfolio mismatch hotfix FM3.
2017-05-22 Vojtech Sidorin      ABITFA-4668: Move the logic to mirror payments from FValidation to this module (FM5).
2017-09-26 Libor Svoboda        ABITFA-5052: Added logic for empty Sales Person.
2017-10-04 Kevin Kistan         Removing yourRef on mirror trades created automatically when a constellation is committed (4Front only, now been hadled on 4Front).
2018-01-23 Heinrich Cronje      Adding FM6. Autoroll trader needs to be set to a valid user, KAYSIMO2.
2018-02-05 Heinrich Cronje      Full Autoroll Automation requires KAYSIMO2 to be changed to HEWITTEN.
2018-06-12 Libor Svoboda        Added FM7 to link ReAcquire Day on mirror trades.
2020-11-13 Amit Kardile         Added rule to set FX PnL Sweep trades' trader to HEWITTEN
"""

import ael


def mirrored_trade(original, mirror):

    # FM1
    if ael.user().userid in ('ATS_AMWI_PRD', 'ATS_AMWI_TST',): 
        return 0

    # FM2 - this now being handled in 4Front(bicikvla)
    # resolves the issue for BXA Interdesks in FA(Mirror trade update)
    '''if ael.user().userid in ('FORE_FRONT_TST', 'FORE_FRONT_PRD'):
        mirror.your_ref = original.your_ref
        mirror.trader_usrnbr = original.trader_usrnbr'''

    # FM4
    if original.sales_person_usrnbr is not None:
        if original.sales_person_usrnbr == mirror.sales_person_usrnbr:
            mirror.sales_person_usrnbr = None
    else:
        if (not mirror.sales_person_usrnbr and mirror.original() and 
                mirror.original().sales_person_usrnbr):
            mirror.sales_person_usrnbr = mirror.original().sales_person_usrnbr
            
    if original.sales_credit != 0:
        if original.sales_credit == mirror.sales_credit:
            mirror.sales_credit = 0

    try:
        for a in mirror.additional_infos():
            field_name = a.addinf_specnbr.field_name
            if field_name.startswith('Sales') or field_name.startswith('ValueAdd'):
                if mirror.add_info(field_name) == original.add_info(field_name):
                    a.value = ''
                    a.delete()
    except Exception, e:
        pass
        #print 'FMirror: Exception when querying additional infos on mirror', e

    # FM5
    fm5_mirror_payments(original, mirror)

    # FM6 - If an Autoroll is being booked by the ATS user and the original trade's
    # trader is HEWITTEN then the mirror's trader should be HEWITTEN as well.
    if ael.user().userid == 'ATS':
        if mirror.type == 'Spot Roll':
            if mirror.trader_usrnbr.userid == 'ATS' and original.trader_usrnbr.userid == 'HEWITTEN':
                mirror.trader_usrnbr = original.trader_usrnbr
    
    # If FX Sales PnL sweep is being booked by the UPGRADE43 user and the original trade's
    # trader is HEWITTEN then the mirror's trader should be HEWITTEN as well.
    if ael.user().userid == 'UPGRADE43':
        if mirror.type == 'PL Sweep':
            if mirror.trader_usrnbr.userid == 'UPGRADE43' and original.trader_usrnbr.userid == 'HEWITTEN':
                mirror.trader_usrnbr = original.trader_usrnbr    
    
    # FM7 (can be removed as soon as SPR 416169 is implemented)
    mirror.re_acquire_day = original.re_acquire_day
    
    return 0


def fm5_mirror_payments(original, mirror):
    """Mirror payments from the original trade to the mirror trade."""

    # Check if trades are new.
    if original.trdnbr >= 0 or mirror.trdnbr >= 0:
        return

    # Check if counterparties are internal.
    if (original.counterparty_ptynbr.type != "Intern Dept"
            or mirror.counterparty_ptynbr.type != "Intern Dept"):
        return

    # Check if payments can be accessed.
    original_payments = None
    try:
        original_payments = original.payments()
    except:
        pass
    mirror_payments = None
    try:
        mirror_payments = mirror.payments()
    except:
        pass
    if original_payments is None or mirror_payments is None:
        return

    # Don't mirror payments if the mirror trade has already some.
    if mirror_payments:
        return

    # Inform the user about mirroring.
    if original_payments:
        print "FM5: Mirroring payments."

    # Mirror the original payments.
    for payment in original_payments:
        # Mirror only payments to/from the original trade's counterparty;
        # i.e. don't mirror payments to/from a third party.
        if payment.ptynbr is not original.counterparty_ptynbr:
            continue
        mpayment = ael.Payment.new(mirror)
        mpayment.ptynbr = original.acquirer_ptynbr
        mpayment.amount = payment.amount*-1
        mpayment.accnbr = payment.our_accnbr
        mpayment.our_accnbr = payment.accnbr
        mpayment.type = payment.type
        mpayment.payday = payment.payday
        mpayment.curr = payment.curr
        mpayment.text = payment.text
        mpayment.archive_status = payment.archive_status
        mpayment.original_curr = payment.original_curr
        mpayment.fx_transaction = payment.fx_transaction
        mpayment.valid_from = payment.valid_from
        mpayment.manual_update = payment.manual_update
