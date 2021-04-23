"""Deprecated FValidation module.

This module contains rules that have not (yet) been fully refactored
and integrated into the new FValidation modules.  No new rules should
be added to this module, only hotfixes if necessary.

Please consult the Developer's Guide before changing the code.  The guide can
be found at
<http://confluence.barcapint.com/display/ABCAPFA/FValidation+Developer's+Guide>.


Purpose               :  Money Market FValidationModule
Department and Desk   :  Money Market Desk
Requester             :  Jansen Van Vuuren, Correy; Haroon Mansoor
Developer             :  Rohan vd Walt, Anwar Banoo
CR Number             :  651043, ????? (ABITFA-973)

2014-08-31 Vojtech Sidorin      CHNG0002210109      Mark as deprecated module
2014-09-30 Dmitry Kovalenko     CHNG0002328679      Updated imports (FValidation_depr_Helper is removed)
2015-05-13 Vojtech Sidorin      FAU-738             Rule 94: Replace nominal_amount() with quantity * contract size
2015-08-20 Vojtech Sidorin      ABITFA-3743         Include rule numbers in messages.
2015-05-25 Lawrence Mucheka     CHNG0003038330      Exclude Curr Instrument in Rules 93 and 94
2015-11-26 Vojtech Sidorin      ABITFA-3969         Rule FV94: Don't set trade premium.
2016-01-28 Vojtech Sidorin      ABITFA-4023         FV94: Include "NCD" in instrument subtypes; improve coding style
2016-03-11 Lawrence Mucheka     ABITFA-4161         Remove rules: FV93 and FV94-1
2016-05-26 Vojtech Sidorin      ABITFA-4326         FV95-2b: Update the message shown to the user; refactor test for Nan.
"""

import math

import ael, acm
from FValidation_depr_General import FUNDING_DESK

from FValidation_core import (DataValidationError,
                              validate_entity)

INT_PROC_GROUP = ael.Group['Integration Process']
SYS_PROC_GROUP = ael.Group['System Processes']
BACKEND_USERGROUPS = [INT_PROC_GROUP, SYS_PROC_GROUP]

# Rule 94
@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def fv94_validate_mm_trade(e, op):
    FIXED_RATE_SUBTYPES = (
            'Call CFD Funding',
            'SNR',
            'Call Bond Deposit',
            'Call Bond Loan',
            'Call Deposit DTI',
            'Call Deposit NonDTI',
            'Call I/Div',
            'Call I/Div DTI',
            'Call I/Div SARB',
            'Call Loan DTI',
            'Call Loan NonDTI',
            'Call 32 Day notice',
            'Call I/div 32 day',
            'Call 64 Day notice',
            'Call I/div 64 day',
            'Call 93 Day notice',
            'Call I/div 93 day',
            'Call 185 Day notice',
            'Call I/div 185 day',
            'Call 277 Day notice',
            'Call I/div 277 day',
            'Call 360 Day notice',
            'Call I/div 360 day',
            'NCD'
            )

    if (ael.user().grpnbr not in BACKEND_USERGROUPS and
            e.acquirer_ptynbr and e.acquirer_ptynbr == FUNDING_DESK):
        # Get instrument subtype.
        subType =''
        ads = e.additional_infos()
        for a in ads:
            if a.addinf_specnbr.field_name in ('Funding Instype', 'MM_Instype'):
                subType = a.value

        # FV94-2
        if e.insaddr.instype in ('CD', 'Deposit') and op == 'Insert':
            if subType not in FIXED_RATE_SUBTYPES:
                e.price = e.insaddr.legs()[0].fixed_rate

       # FV94-3
        if (not subType.startswith('Call') and subType != 'SNR' and
                e.add_info('MM_DEREC_TRADE') != "Yes" and
                ael.date_from_time(e.time) > e.value_day):
            # ABITFA-973 - if backdated trade ie time > valueday then trade time needs to equal value day
            e.time = e.value_day.to_time()

        # FV94-4
        if subType == 'FDI':
            if e.insaddr.legs()[0].fixed_coupon != 1:
                #e.insaddr.legs()[0].fixed_coupon = 'Yes'
                print('Fixed period must be set on FDI instruments')
                raise DataValidationError('FV94-4: Fixed period must be set on FDI instruments')

# Rule 95
@validate_entity("Instrument", "Insert", caller="validate_transaction")
@validate_entity("Instrument", "Update", caller="validate_transaction")
def validate_call_float_instrument(e, op):
    if e.instype == 'Deposit' and e.legs().members() != [] and e.legs()[0].type == 'Call Fixed Adjustable':
        #when CallFloatRef is set to <blank> in InsDef, we have to delete it.
        aisp = ael.AdditionalInfoSpec['CallFloatRef']
        for ai in e.additional_infos():
            if ai.addinf_specnbr.specnbr == aisp.specnbr and ai.value == '':
                ai.delete()

        if e.add_info('CallFloatRef') <> '':
            #set the FixedRate based on CallFloatRef + CallFloatSpread
            float_ref_name = e.add_info('CallFloatRef')
            float_ref = acm.FInstrument[float_ref_name]
            if not float_ref or float_ref.InsType() <> 'RateIndex':
                raise DataValidationError('FV95-2a: CallfloatRef is not a valid Rate Index')

            rate_from_float_ref = float_ref.used_price()
            if math.isnan(rate_from_float_ref):
                msg = ('FV95-2b: The rate retrieved from CallFloatRef({0}) is NaN. '
                       'This may indicate that the user has no access to the '
                       'SPOT prices. Please consult RTB.'
                       .format(float_ref_name))
                raise DataValidationError(msg)

            spread_from_insdef =  e.add_info('CallFloatSpread')
            new_rate = float(rate_from_float_ref) + float(spread_from_insdef)

            leg = e.legs()[0]
            leg.fixed_rate=new_rate
        else:
            #if no CallFloatRef set, set CallFlaotSpread to 0.0
            aisp = ael.AdditionalInfoSpec['CallFloatSpread']
            ais = e.additional_infos()
            for ai in ais:
                if ai.addinf_specnbr.specnbr == aisp.specnbr:
                    ai.value = '0.0'


        if op == 'Insert':
            #delete and recreate cashflows to ensure it is using the calculated fixed rate (else it is based on 0.0)
            for l in e.legs():
                for cf in list(l.cash_flows()):
                    cf.delete()
                l.regenerate(False)
