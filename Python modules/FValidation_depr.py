"""FValidation - Deprecated module.

This module contains rules that have not (yet) been fully refactored
and integrated into the new FValidation modules.  No new rules should
be added to this module, only hotfixes if necessary.

Before changing the code, please consult the Developer's Guide available at
<https://confluence.barcapint.com/display/ABCAPFA/FValidation+Developer%27s+Guide>.

A list of the implemented FValidation rules is kept at
<http://confluence.barcapint.com/display/ABCAPFA/FValidation+Rules>.
If you change the code, please update also that list to keep it up to date.


-------------------------------------------------------------------------------
MODULE   FValidation

Version: 1.1

DESCRIPTION

This module is for adding extra validation rules to comitted data
to ensure data integrety.

History:
Date            Who                            What

2004-03-17      Hardus Jacobs                      Prevent party of type None to be used
2004-04-05      Kim Madley                         Updated
2005-01-12      Hardus                             Added Check for FICA Compliance
2005-09-28      Andries Brink                      Added Check for BESE Member Agreement Compliance
2006-03-24      Aaeda Salejee                      Added check for Bonds booked after 13:00
2006-08-12      Gavin                              Inflation Linked Instrument add info NACSRate
2006-09-22      Neil Retief                        Changed the quantity check on FXSwaps to check for all quantities != 1.0 & then make it 1.0
2007-02-05      Aaeda Salejee / Christo Rautenbach Added validations for Capital Market trades
2007-08-13      Aaeda Salejee                      Global context cannot be overwritten.
2007-09-19      Heinrich Cronje                    Can't book a trade against portfolio Call_. MM Project - Temporary
2007-12-08      Heinrich Cronje                    For Call Accounts: Can not update a cash flow or reset.
2008-02-21      Neil Retief                        Remedy Call 1932: No updates allowed trades with a status of VOID
2008-02-26      Zaakirah Kajee                     Amended the currency commit of FXSwap or Option when the underlying instrument changes.
2008-03-06      Heinrich Cronje                    Remedy Call 2138: All Call Accounts must have the add_info field Call_Region populated.
2008-03-11      Tshepo Mabena                      Setting the BO Confirm time stamp
2008-05-28      Heinrich Cronje                    Remedy Call 3000: Testing CP Code on Settlements & Confirmations on Settlements so that Netted payments will pass.
2008-05-29      Heinrich Cronje                    Remedy Call 2822: Added the validation for Fix Period on Call Accounts and Account Name on Call.
2008-07-15      Heinrich Cronje                    Remedy Call 3598: Added the validation Call Accounts should not have any other day count methods that Act/365.
2008-07-22      Heinrich Cronje                    CR 3662 & 3676 - Added the validation for voiding a call account and voiding a trade with acquirer Funding Desk.
2009-02-17      Tshepo Mabena                      CR 368506: All Funding Desk trades should be booked with a non zero rate
2009-02-17      Tshepo Mabena                      CR 369077: No Funding Desk trade in FO Confirmed status can be changed after the first day.
2009-03-05      Herman Hoon                        CR 373907: SOX Passwords - prohibit users to make changes if password has not been changed in the last 30 days.
2009-03-26      Herman Hoon                        CR 381702: Non ZAR Funding - validate the additional info fields and update the saved status if amendmends is made.
2009-06-04      Tshepo Mabena                      CR 13459 Blocking Traders From Updating BO Confirmed and BO-BO Confirmed Trades By Updating The Instrument.
2009-06-09      Zaakirah                           CR 17936 Ensure instruments that are mtm from feed had a price finding group
2009-07-23      Jaysen Naicker                     CR 62236 Prevent payment for Term trades which are ceeded
2009-08-06      Zaakirah Kajee                     CR 71265 Access Control around YC and Vols
2009-12-03      Anwar Banoo                        Upgrade - validate non zero price for non call deposits
2010-02-03      Jaysen Naicker                     Update code so other desks can change Portfolio and/or status for mirror trades
2010-02-05      Paul Jacot-Guillarmod              CR 220208: take into account that the mm trader groups have been changed
2010-02-05      Rohan van der Walt                 CR 218724: Fixed check for bond price in market range
2010-02-23      Aaeda Salejee                      CR 235546: Rules for access control for FO Call Traders (Modify Confirm)
2010-02-23      Ickin Vural                        CR 236870: Added check to prevent trades creating trades in portfolios SF1511 & SF9926 without adding Mentis Project Num
2010-03-04      Herman Hoon                        CR 240470: Create a broker fee additional payment for Stocks and ETF trades
2010-03-04      Willie van der Bank                CR 243496: Trades With Acquirer Funding Desk And Status Legally Confirmed Not Allowed
2010-03-09      Herman Hoon                        CR 248202: Exclude Portfolio 248179 from the equity brokerage fee calculation
2010-03-19      Paul Jacot-Guillarmod              CR 258995: Allow members FO PSSecLend Trader to amend certain fields on the instrument part of a BO Confirmed security loan
2010-04-06      Babalo Edwana                      CR 279366: FX Allowable Conversions check.
2010-04-14      Paul Jacot-Guillarmod              CR 282030: Prevent members of FO Call Trader from booking trades straight into a BO Confirmed status
2010-05-06      Willie van der Bank                CR 302675: If amount is captured in Sales Credit, Sales Person should be populated as well
2010-05-24      Babalo Edwana                      CR 320945: TMS Validations, should check portfolio add info only if prfnbr is valid.
2010-06-03      Paul Jacot-Guillarmod              CR 328189: Update the way the broker fee is calculated for stocks and ETF's
2010-06-03      Anwar Banoo                        CR 326265: Mirror payments need to be created on both trades of the mirror if we have both internal cpty
2010-06-15      Henk Nel                           CR 341208: If value is captured in Sales Person it can not be deleted
2010-06-28      Francois Truter                    CR 355193: Allow INTERNAL bond trades where BESA_Member_Agree == No (i.e. counterparty_ptynbr.type != Intern Dept)
2010-07-05      Rohan van der Walt                 CR 375280: Updated recent Password change check to include more users
2010-07-13      Rohan vd Walt                      CR 370303,374228: Exclude 'BSE NewGold' portfolio from automatic brokerage fee calculation
2010-08-13      Rohan van der Walt                 CR 401622: More auto brokerage calculation exclusions
2010-08-25      Anwar Banoo                        CR 414264: Update acquirer on jse trades fed in via adaptor to be the owner of the reported portfolio
2010-09-23      Aaeda Salejee                      CR 431665: FA to Midbase FX feed. Clearing of add_infos on Save New, change restriction of Midas_field_list & exclusion of Curr from Sales Credit validation.
2010-10-01      Anwar Banoo                        CR 447655: XTP/HERMES
2010-10-23      Herman Hoon                        CR 455227: CFD Project - Added Call CFD Funding to Money Market Validations
2010-11-01      Anwar Banoo                        CR 480842: Removed restriction of 18 chars for call account insid
2010-11-10      Ickin Vural                        CR 487627: If amount is captured in Value Added , Sales Person should be populated as well, A Sales Person may not be captured more than once
2010-11-11      Jaysen Naicker                     CR 486618: Add approximate loading check. If approx. load is set to Yes, approx. load ref must have a value.
2010-12-10      Herman Hoon                        CR 527235: Set the Trader ID to the current user if the trade status is changed from Simulated or FO Sales to FO Confirmed status
2011-01-21      Francois Truter                    CR 558419: Extracted the broker fee peyment code to SAEQ_BrokerFees
2011-04-14      Herman Hoon                        CR 628862: Add 32 Day notice Funding Instypes to Money Market Validations.
2011-04-19      Rohan van der Walt                 CR 651043: Added FValidation_MoneyMarket and moved/modified ZeroRate validation block, to exclude Bills as well
2011-05-19      Anil Parbhoo                       CR 651043: Moved the YieldCuve and Volatility access to another module
2011-05-19      Paul Jacot-Guillarmod              CR 651043: Allow security lending traders to update a Bo-Confirmed security loan trade so that they can terminate partial returns without changing the trade status
2011-05-21      Willie van der Bank                CR 655450: Updated "#Standard name for Contact Details" to include options
2011-05-26      Paul Jacot-Guillarmod              CR 665055: Added a condition so that trades in booked into a prime services general portfolioswap portfolio wont geta  broker fee
2011-07-01      Bhavnisha Sarawan                  CR 699989: Changed the user check for void updates to exclude Integration Process (System Users)
2011-07-05      Anil Parbhoo                       CR 632906: SAEQ_BrokerFess to no longer use the Broker_portfolio_exclusionList and chages to SAEQ_Broker_fees as well
2011-07-15      Zaakirah Kajee                     CR 713436: Exclude PB allocation portfolios from ACS brokerage fee calc. Allow for PB call accounts to be traded till 7PM
2011-09-05      Heinrich Cronje                    CR 759437: Removed the Additional Info selection on Settlements when adding SWIFT_MessageType to the settlement. This will increase the performance of Adjusting Deposits.
2011-10-07      Willie van der Bank                CR 789907: Updated for SWIFT_MessageType 202
2011-10-08      Willie van der Bank                CR 790154: Updated for NLD desk confirmations and affirmations
2011-10-17      Anwar Banoo                        CR 798204: Moved some money market validation into FValidation_MoneyMarket
2011-10-26      Heinrich Cronje                    CR 810518: Amendmed access around FO Call Trader profile.
2011-11-01      Rohan vd Walt                      CR 816158: FValidation_SecLending Module added
2011-11-17      Heinrich Momberg                   CR C828528: Override add info value 'MIDAS_MSG' for acm MMG user
2012-02-17      Heinrich Cronje                    CR 48574: Added Call Account Reset restriction in validate entity.
2012-05-10      Aaeda Salejee                      CR 180332: Added the Pricing and Risk system user group to allow YC updates.
2012-05-19      Willie van der Bank                CR 183633: Updated "#Standard name for Contact Details" to include Metals and Gold desk
2012-07-20      Aaeda Salejee                      CR 318335: Added product restriction check for Credit and Ccg
2012-08-16      Anwar Banoo                        CR ??????: ABITFA-1497 - Enhanced code to switch acquirer for adaptor trades to the correct desk
2012-10-10      Bhavnisha Sarawan/Tesslyn Pillay    CR 521939: Validation rules around the group FO FX Sales inc MM
2012-11-08      Anwar Banoo                        Remedy 521939: Corrected group access to allow MM Trading and Banking
2012-11-23      Kenneth Danielsson                 612553 Pension Fund Fee Split: fixed rate set to lender fee security loans
2012-12-07      Anwar Banoo                        CHNG0000662037  Final clarity on the FO FX Sales inc MM group access - allow FO Confirm for Deposit and FO Sales for all else
2013-02-05      Bhavnisha Sarawan                  CHNG0000778182 Removed the additional info PS_MsgSentDate from the trade upon a save new from an old ticket
2013-03-06      Ntuthtuko Matthews                 CHNG0000867181 Grant access to MO (pcg_mo) to amend Midbase trades
2013-03-06      Anwar Banoo                        CHNG0000867181 File-Merge: Removed convertible from the restricted list
2013-04-24      Anwar Banoo                        C975927 - ABITFA-1947 - Enhanced code to switch acquirer for adaptor trades to the correct desk coming in from Yield X
2013-05-16      Jan Sinkora                        C1024176 - ABITFA-1821 - Preventing cash-posting trades involved in the archiving process from being changed
2013-07-26      Lukas Paluzga, Heinrich Cronje     CHNG0001203303 Pricing for Pace FX Options
2013-08-06      Lukas Paluzga                      CHNG0001240250 Delivery date update for Pace FX Options (code refactored to FValidation_PaceFXO)
2013-10-28      Pavel Saparov                      CHNG0001483611 Move trade back to BO status iff there are any changes made to a trade in BO-BO status as part of UT
2014-01-07      Jan Sinkora                        CHNG0001629939 Refactoring - moved validate_entity rules to validate_transaction
                                                        Also some other minor tweaks:
                                                            ABITFA-2230 fixes connected to previous change by Pavel Saparov
                                                            Last traceback is saved so that the last exception and trace can be accessed
2014-01-21      Jan Sinkora                        CHNG0001663173 Moving some code back to validate_entity to re-enable some rules which got disabled by the previous move. This is a temporary fix and should be refactored/changed later.
2014-04-08      Peter Fabian                       CHNG0001830048 Modification to the SAEQ brokerage -- counterparty condition moved to SAEQ_BrokerFees module
2014-05-22      Peter Fabian                       CHNG0001979991 Adding mandatory add info for mirror deposits
2014-06-23      Andrei Conicov                     CHNG0002073680 Have fixed the way settlements amendment is checked
2014-08-31      Vojtech Sidorin                    CHNG0002210109 Mark as deprecated module
2014-09-30      Dmitry Kovalenko                   CHNG0002328679 (1) Removed msg_box functionality(it is now built-in into core exceptions). (2) Removed prints(now built-in into FV_core). (3) Replaced standard exceptions with FV_core exceptions.
2014-11-20      Vojtech Sidorin                    CHNG0002443195 Refactor rule 16 and move it to module FValidation_FixedIncome
2015-01-14      Dmitry Kovalenko                   Moved rule 13 to new module FValidation_SettleConf
2015-02-12      Vojtech Sidorin                    ABITFA-3354: Refactor rules 53, 54 and move them into FValidation_FOCallTrader.
2015-04-01      Vojtech Sidorin                    ABITFA-3280/FXFA-807 Move rules 46a, 46b to FValidation_General.
2015-06-09      Vojtech Sidorin                    ABITFA-3501 Move rule 7 to FValidation_YC_Vol_Access and refactor the rule; update rules 109, 110.
2015-06-09      Vojtech Sidorin                    Update rule 32: Merge code of Willie van der Bank (handle releasing positive settlement amounts).
2015-08-20      Vojtech Sidorin                    ABITFA-3743: Include rule numbers in messages.
2015-09-08      Vojtech Sidorin                    ABITFA-3734: Remove redundant rule 25. Its logic is already implemented in rule 44.
2015-09-17      Willie van der Bank                Adaptiv: Use add_info MM_Ceded_Amount instead of MM_Account_Ceded to indentify a cede trade
2015-11-06      Vojtech Sidorin                    ABITFA-3910: Refactor rules FV14, FV15 and move them to module FValidation_DatesTimes.py.
2016-02-18      Ondrej Bahounek                    ABITFA-3840: Change messages to be more specific
2016-02-25      Ondrej Bahounek                    FV21: allow booking of 2 PSBondBooking trades.
2016-04-05      Ondrej Bahounek                    Rules for Graveyard portfolios contain specific portfolio names.
2016-04-05      Vojtech Sidorin                    ABITFA-4121: FV36/FV37: Do credit limit checks only if a credit limit is set for the counterparty and department.
2016-08-19      Willie van der Bank                CHNG0003744247 Demat: Amended rule 32, very limited validation should be performed on demat settlements. Removed rule 31.
2016-09-06      Willie van der Bank                CHNG0003914707 Amended rule 12 to include the selected correspondent bank swift code instead of simply the first alias.
2016-10-10      Vojtech Sidorin                    ABITFA-4467: FV29, FV63: Move to FValidation_General and refactor
2016-12-07      Anwar Banoo/Vojtech Sidorin        ABITFA-4601: Add FV132: Forbid trades without a reference to an instrument
2016-12-14      Anwar Banoo/Vojtech Sidorin        ABITFA-4611: FV132: Forbid also trades without a portfolio
2017-03-28      Willie vd Bank                     ABITFA-4599: FV32-1: Removed this rule (check for desk in SettlementConstants.SETTLEMENT_ACQUIRERS)
2017-03-29      Vojtech Sidorin                    ABITFA-4668/ABITFA-4340: Remove part of FV21 that sets the portfolio to MM_Graveyard; move the rest of FV21 to FMirror.
2017-08-16      Vojtech Sidorin                    FAU-2933: FV37: Fix the Credit Limits logic: Forbid bypassing the check by booking trades via Simulated.
2017-10-17      Anil Parbhoo                       ABITFA-5091: Chnage notification to FV105.
2018-05-11      Willie vd Bank                     CHG1000406751: Rule 32: should apply only to MT103 and MT202s.
                                                                  Rule 12: account number from the 5th character should be included in name.
2018-05-24      Willie vd Bank                     CHG1000498896: Rule 12: Function modified to cater for any format of account number.
2018-06-05      Sihle Gaxa                         CHG1000534957: Rule 69: Amended rule 69 to cater for vice versa, i.e if approx ref exists,approx load must be set to Yes
2018-07-25      Jaysen Naicker                     Rule 71: Add new group FO_FX_OPT_HEAD to the check and using group number instead of group id
2018-11-20      Bhavnisha Sarawan                  ABITFA-5624: Extend Rule FV105 to exclude portfolio status Closed and Dormant.
2019-01-10      Bhavnisha Sarawan                  ABITFA-5659: Remove Dormant portfolio from Rule FV105.
2019-04-10      Jaysen Naicker                     FAOPS-477 - Fix rule 30 so manual adjustments on settlements is limited to accounts only
2019-02-12      Mighty Mkansi                      ABITFA-5678: Duplicate payments - USD67 and USD10 and proposed solution.
2019-04-15      Stuart Wilson                      FAOPS-369 - Fixed rule 32 to prevent positive amount 103, 202 messages from releasing.
2019-06-06      Bhavnisha Sarawan                  ABITFA-5705 Add Access Deposit Note 95d Note2 to Rule 34
2019-07-16      Tibor Reiss                        Add A2X to rule 17
2019-07-18      Tibor Reiss                        CHG1002020534, FAPE-92: fix rule 27 and 28
2020-06-03      Libor Svoboda                      Remove redundant SBL Fee validation (rule 73)
ENDDESCRIPTION
-------------------------------------------------------------------------------
"""

import sys
import math
import types
from datetime import datetime

import ael
import acm

import FCreditLimit
import TMS_Functions
import SAGEN_YC_VOL_ACCESS
import TMS_AMBA_Message
import TMS_Config_Trade
import SAEQ_BrokerFees
import FValidation_depr_General as FValidation_General

from FValidation_core import (ValidationError,
                              DataValidationError,
                              AccessValidationError)

from SettlementConstants import *
from SAGEN_IT_Functions import *
from demat_functions import is_demat
from at_time import acm_datetime


zeronom = {'Float Rate': lambda e: e.nominal_factor, 'Fixed Amount': lambda e: e.fixed_amount, 'Fixed Rate': lambda e: e.nominal_factor}

sys_proc = ael.Group[495]
int_proc = ael.Group[494]
ops_confos_cm = ael.Group[572]
pcg_mo_bond_split = ael.Group[566]      #PCG Mkt Bond Split
fo_tcu = ael.Group[639]
fo_tcu_management = ael.Group[646]

SETTLEMENT_RESTRICTED_FIELDS = {
    'Adjusted' : ['amount', 'curr', 'value_day', 'acquirer_ptyid', 'party_ptyid']
}   

SETTLEMENT_ALLOWED_FIELDS = ['Fair Value', 'Good Value']

sys_exclude = [sys_proc, int_proc]
graveyarding_groups = [pcg_mo_bond_split, fo_tcu, fo_tcu_management]

Midas_field_list = ['value_day', 'time', 'price', 'premium', 'quantity', 'curr', 'trader_usrnbr', \
                    'counterparty_ptynbr', 'prfnbr', 'add_info("Midas_ID")', 'add_info("Midas_ID_BTB")', \
                    'add_info("MIDAS_MSG")', 'add_info("Midas_Status")', 'add_info("Midas_Status_BTB")']

AMBA_USER = 130
JSE_CPTY = 18247
JSE_SA_CPTY = 7180
SAFEX_CPTY = 17961
A2X_CPTY = 53083
ABCAP_NON_ZAR_CFCI_DIV = 32708

Broker_CP_ptyid = 'JSE'

USER = ael.user()
USERGROUPID = USER.grpnbr.grpid
USERGROUPNBR = USER.grpnbr.grpnbr
keys =  acm.FChoiceList.Select('list = "TradeKey4"')
CurrDict = {}
for k in keys:
    CurrDict[k.Name()] = k.Oid()
#===========================================================================================================================================

def account_name_iterate(name, e, counter):
    name_modified = name + (str)(e.account[counter:])
    if e.curr:
        name_modified = name_modified[0:15]+ '/' + e.curr.insid + e.details_of_charges[0]
    else:
        name_modified = name_modified[0:15]+ '/' + 'ALL' + e.details_of_charges[0]
    name_modified = name_modified[0:21]
        
    return name_modified

def validate_entity(e, op):
    """ Moving everything into validate_transaction.

    Some rules were moved back here temporarily because they are bound to
    entities which don't come into validate_transaction (only their parent
    entities do). This is to be amended once a better solution is found.
    """

    # Rule 12
    #Setting the name of the account (all accounts)
    if e.record_type == 'Account' and op != 'Delete':
        if e.correspondent_bank_ptynbr:
            use_dalias = ''
            if e.bic_seqnbr and e.bic_seqnbr.alias:
                use_dalias = e.bic_seqnbr.alias[0:4]
            else:
                for al in e.correspondent_bank_ptynbr.aliases():
                    if al.type.alias_type_name == 'SWIFT':
                        use_dalias = al.alias[0:4]
            accounts = ael.Account.select("ptynbr = %d" %e.ptynbr.ptynbr)
            account_names = [a.name for a in accounts if a.accnbr != e.accnbr]
            account_numbers = [a.account for a in accounts if a.accnbr != e.accnbr]
            
            name_base = use_dalias + '/'
            #The default format is to use the account from the 7th character because this first
            #part will normally contain the branch number.
            name = account_name_iterate(name_base, e, 7)
            counter = 0
            while name in account_names and e.account not in account_numbers:
                #If the new proposed name is already used then ignore the default format
                #7th character rule and just use the characters from the first.
                name = account_name_iterate(name_base, e, counter)
                counter += 1
            
            e.name = name

    # Rule 105 and Rule 105a
    #No trades can be booked into a portfolio in Pending status
    if e.record_type == 'Trade' and e.prfnbr and e.prfnbr.add_info('Portfolio Status') == 'Pending' and op in ('Insert', 'Update'):
        raise ValidationError('FV105: Please contact TCU to change portfolio status from pending to active.')
    #No trades can be booked into a portfolio in Closed or Dormant status
    if e.record_type == 'Trade' and e.prfnbr and e.prfnbr.add_info('Portfolio Status') == 'Closed' and op in ('Insert', 'Update'):
        raise ValidationError('FV105a: Please contact TCU/PCT. Trades cannot be booked into portfolio with status Closed.')
        
    # Rule 106
    #A closed portfolio cannot be reopened
    if (e.record_type == 'AdditionalInfo' and
        e.addinf_specnbr.rec_type == 'Portfolio' and
        e.addinf_specnbr.field_name == 'Portfolio Status' and
        op == 'Update' and
        e.original().value == 'Closed' and
        e.value != 'Closed'):

        raise ValidationError('FV106-1: You are not allowed to reopen a closed portfolio.')

    if (e.record_type == 'AdditionalInfo' and
        e.addinf_specnbr.rec_type == 'Portfolio' and
        e.addinf_specnbr.field_name == 'Portfolio Status' and
        op == 'Delete' and
        e.original().value == 'Closed' and
        e.value != 'Closed'):

        raise ValidationError('FV106-2: You are not allowed to reopen a closed portfolio.')

    return

# The last thrown validation exception info and traceback are stored in a tuple
# in this global variable. The tuple is what sys.exc_info() returns.
last_exc_info = None

def validate_transaction(transaction_list, *rest):
    global last_exc_info

    last_exc_info = None

    try:
        return _validate_transaction(transaction_list, *rest)
    except Exception:
        # Store the traceback and exception info.
        last_exc_info = sys.exc_info()
        raise

def _validate_transaction(transaction_list, *rest):
    # Rule 1
    if ael.user().userid in ('FMAINTENANCE', 'UPGRADE43'):
        return transaction_list

    # FV132
    # ABITFA-4601/4611: Forbid trades without a reference to an instrument
    # and/or a portfolio. This rule was added to prevent badly formed AMBA
    # trade messages from hitting all the rules in FValidation.
    for entity, operation in transaction_list:
        if entity.record_type == "Trade" and entity.status != "Simulated":
            # Check missing instrument.
            if not entity.insaddr:
                msg = ("FV132-1: The transaction contains a trade that does "
                       "not reference any instrument. This may be caused by a "
                       "badly formed AMBA message.")
                raise DataValidationError(msg)
            # Check missing portfolio.
            if not entity.prfnbr:
                msg = ("FV132-2: The transaction contains a trade that does "
                       "not reference any portfolio. This may be caused by a "
                       "badly formed AMBA message.")
                raise DataValidationError(msg)

    mirror_event = 1            # 1 = no mirror event
    sp_mirror_event = 1         # 1 = Special -> Mirror Trade  (Front updates original trade trans ref with its own number)


    # ########################### Mirror Trades ########################### #
    # Rule 19
    mirror_trds = []
    sp_insert = 0
    sp_update = 0
    for (entity, operation) in transaction_list:
        if entity.record_type == 'Trade' and operation == 'Insert':
            mirror_trds.append(entity)

        # Rule 20
        if entity.record_type == 'Trade' and operation != 'Delete':
            if operation == 'Insert':
                sp_insert = 1
            if operation == 'Update':
                sp_update = 1
        if sp_insert and sp_update:
            sp_mirror_event = 0

    # Rule 113
    mirror_couples = [(t, t.mirror_trdnbr) for t in mirror_trds if t.mirror_trdnbr and t.mirror_trdnbr != t and t.mirror_trdnbr in mirror_trds]
    for (original, mirror) in mirror_couples:
        if not mirror.add_info('Funding Instype'):
            if original.insaddr.instype in ('Deposit', 'CD'):
                ai = ael.AdditionalInfo.new(mirror)
                ai.addinf_specnbr = ael.AdditionalInfoSpec['Funding Instype']
                ai.value = original.add_info('Funding Instype')

    # ########################### Mirror Trades ########################### #


    global trdstemp
    global funding
    funding = 0
    trdstemp={}

    for (entity, operation) in transaction_list:

        trds = []
        lgs = []
        ilb = 0     # flag used to determine if the Trade entity needs to have Guaranteed Amount calculated
        iilb = 0    # flag used to determine if the Instrument entity needs to have simple rate calculated

        # Rule 24
        if entity.record_type == 'Trade' and entity.status == 'Simulated':
            if entity.insaddr.instype != 'Deposit':
                continue


        # ########################### set BoConfirm timestamp ########################### #
        # Rule 27
        if entity.record_type == 'Trade' and operation == 'Update':
            old_entity = entity.original()
            if old_entity.status == 'FO Confirmed' and entity.status == 'BO Confirmed':
                if not (entity.trdnbr != entity.contract_trdnbr and entity.text1 == 'CR Trade'):
                    time_string = acm_datetime(datetime.now())
                    ai_found = None
                    for ai in entity.additional_infos():
                        if ai.addinf_specnbr.field_name == 'BoConfirm timestamp':
                            ai_found = ai
                            break
                    if ai_found is not None:
                        ai_clone = ai_found.clone()
                        ai_clone.value = time_string
                    else:
                        ai_new = ael.AdditionalInfo.new(entity)
                        ai_new.value = time_string
                        ais = ael.AdditionalInfoSpec['BoConfirm timestamp']
                        ai_new.addinf_specnbr = ais.specnbr

        # ########################### set FO-Confirm Timestamp ########################### #
        # Rule 28
        if entity.record_type == 'Trade' and operation == 'Update':
            old_entity = entity.original()
            if old_entity.status == 'FO Sales' and entity.status == 'FO Confirmed':
                if not (entity.trdnbr != entity.contract_trdnbr and entity.text1 == 'CR Trade'):
                    time_string = acm_datetime(datetime.now())
                    ai_found = None
                    for ai in entity.additional_infos():
                        if ai.addinf_specnbr.field_name == 'FOConfirm Timestamp':
                            ai_found = ai
                            break
                    if ai_found is not None:
                        ai_clone = ai_found.clone()
                        ai_clone.value = time_string
                    else:
                        ai_new = ael.AdditionalInfo.new(entity)
                        ai_new.value = time_string
                        ais = ael.AdditionalInfoSpec['FOConfirm Timestamp']
                        ai_new.addinf_specnbr = ais.specnbr

        callConfo = False
        if entity.record_type == 'Settlement':
            Settlement = acm.FSettlement[entity.seqnbr]

            # Rule 30
            if operation ==  'Insert' and entity.relation_type in SETTLEMENT_RESTRICTED_FIELDS:
                #When a settlement is amended by a user, only a few fields can be changed
                for (tr_entity, tr_operation) in transaction_list:
                    if tr_entity.record_type == entity.record_type and tr_operation != 'Delete' and tr_operation != operation and entity.type ==tr_entity.type:
                        if tr_entity.relation_type not in SETTLEMENT_ALLOWED_FIELDS:
                            for i in SETTLEMENT_RESTRICTED_FIELDS[entity.relation_type]:
                                entityField    = getattr(entity, i)
                                tr_entityField = getattr(tr_entity, i)
                                msg = 'FV30: You can not amend the %s of the settlement (%s -> %s), only account changes allowed.' %(str(i), str(entityField), str(tr_entityField))
                                if type(entityField) == types.FloatType:
                                    if abs(abs(round(entityField, 5)) - abs(round(tr_entityField, 5))) > 0.0001:
                                        raise DataValidationError(msg)
                                elif entityField != tr_entityField:
                                    raise DataValidationError(msg)

            # Rule 32
            if operation == 'Update' and entity.status == 'Released':
                if not is_demat(Settlement) and Settlement.MTMessages() in ('202', '103'):
                    if Settlement.Amount() > 0:
                        # 2015-06-09 Vojtech Sidorin: Merge code of Willie van der Bank.
                        # Handle releasing positive settlement amounts.
                        if entity.add_info('Authorise Debit') == 'Yes':
                            if Settlement.CounterpartyAccountRef().Bic().Name()[:8] != 'ABSAZAJJ':
                                raise DataValidationError('FV32-1: Can not release this settlement. Counterparty account not ABSA.')

                            else:
                                pass
                        else:
                            raise DataValidationError('FV32-2: Can not release this settlement. Debit not authorised.')
                    else:
                        #print "name = '%s' and party = '%s'" %(Settlement.CounterpartyAccName(), Settlement.CounterpartyName())
                        #check that the account has a valid BIC code
                        account = acm.FAccount.Select01("name = '%s' and party = '%s'" %(Settlement.CounterpartyAccName(), Settlement.CounterpartyName()), '')
                        if not account:
                            raise DataValidationError('FV32-3: Can not release this settlement. Please check counterparty account details.')
                        elif not account.Bic():
                            raise DataValidationError('FV32-4: Can not release this settlement. SWIFT code missing.')

                        #check that the trade(s) is not in graveyard portfolio
                        valid_port = []
                        low_set = get_lowest_settlement(entity.original(), [])

                        for s in low_set:
                            set = ael.Settlement[s]
                            if set.trdnbr:
                                t = set.trdnbr
                                if not t.prfnbr.prfid in valid_port:
                                    if not get_Port_Struct_from_Port(t.prfnbr, 'GRAVEYARD'):
                                        valid_port.append(t.prfnbr.prfid)
                                    else:
                                        raise DataValidationError('FV32-5: Settlement linked to GRAVEYARD Portfolio. Cannot release Settlement.')

                        if (Settlement.Type() == 'Stand Alone Payment') or (Settlement.Acquirer().Oid() != FUNDING_DESK):
                            callConfo = entity.add_info('Call_Confirmation') != ''
                        else:
                            if entity.trdnbr:
                                t = entity.trdnbr

                                #Term Trades with acquirer Funding Desk and additional info MM_Ceded_Amount != "" should not pay out capital
                                if Settlement.Trade().Instrument().Legs():
                                    if Settlement.Trade().add_info('MM_Ceded_Amount') != '':
                                        if Settlement.Trade().Instrument().Legs()[0].LegType() != 'Call Fixed Adjustable':
                                            for s in low_set:
                                                set = acm.FSettlement[s]
                                                if set.Type() == 'Fixed Amount':
                                                    raise DataValidationError('FV32-9: Can not release this settlement. Amount is ceeded.')

                                    #Funding Desk Call Account and EQ Derivatives Desk settlements should have been confirmed before released
                                    callConfo = (Settlement.Trade().Instrument().Legs()[0].LegType() != 'Call Fixed Adjustable') or \
                                                ((Settlement.Trade().Instrument().Legs()[0].LegType() == 'Call Fixed Adjustable') and \
                                                 (entity.add_info('Call_Confirmation') != ''))

                            else:
                                #Term Trades with acquirer Funding Desk and additional info MM_Ceded_Amount != "" should not pay out capital
                                for s in low_set:
                                    mSettlement = acm.FSettlement[s]

                                    if mSettlement.Trade():
                                        if mSettlement.Trade().Instrument().Legs():
                                            if mSettlement.Trade().add_info('MM_Ceded_Amount') != '':
                                                if mSettlement.Type() == 'Fixed Amount':
                                                    if mSettlement.Trade().Instrument().Legs()[0].LegType() != 'Call Fixed Adjustable':
                                                        raise DataValidationError('FV32-12: Can not release this settlement. Amount is ceeded.')

                                            #Funding Desk Call Account and EQ Derivatives Desk settlements should have been confirmed before released
                                            callConfo = (mSettlement.Trade().Instrument().Legs()[0].LegType() != 'Call Fixed Adjustable') or \
                                                ((mSettlement.Trade().Instrument().Legs()[0].LegType() == 'Call Fixed Adjustable') and \
                                                 (mSettlement.add_info('Call_Confirmation') != ''))

                        if not callConfo:
                            raise DataValidationError('FV32-6,7,8,10,11: Can not release this settlement. Confirmation missing.')

        # ******************************** CALL ******************************** #

        # Rule 34
        #Setting the insid for call accounts
        if entity.record_type == 'Trade' and operation != 'Delete':
            if entity.acquirer_ptynbr:
                funding_instype = entity.add_info('Funding Instype')
                if entity.acquirer_ptynbr.ptynbr == 2247: #Funding Desk
                    if entity.insaddr.instype == 'Deposit' and entity.insaddr.legs().members()!= [] and entity.insaddr.legs()[0].type == 'Call Fixed Adjustable':
                        temp_funding_instypes = ('Access Income Plus 35d', 'Access Deposit Note 95d Note 2', 'Access Deposit Note 370d', 'Access Deposit Note 95d', 'FDI Access Deposit Note 95d', 'FDI Access Deposit Note 370d',
                                                 'FDC 7 Day Notice', 'FDC 48 Hour Notice', 'Call Deposit NonDTI', 'Call Deposit DTI', 'Call Deposit Coll NonDTI', 'Call 7 Day notice', 'Call Deposit Coll DTI',
                                                 'Call 32 Day notice', 'Call I/div 32 day', 'Call 64 Day notice', 'Call I/div 64 day', 'Call 93 Day notice', 'Call I/div 93 day', 'Call 185 Day notice', 'Call I/div 185 day',
                                                 'Call 277 Day notice', 'Call I/div 277 day', 'Call 360 Day notice', 'Call I/div 360 day'
                                                )
                        if funding_instype in temp_funding_instypes:
                            funding = 2201
                        elif (funding_instype in ('Call Loan DTI', 'Call Loan Coll DTI')):
                            funding = 2202
                        elif (funding_instype in ('Call Loan NonDTI', 'Call Loan Coll NonDTI')):
                            funding = 2203
                        elif funding_instype == 'Call Bond Deposit':
                            funding = 2204
                        elif funding_instype == 'Call Bond Loan':
                            funding = 2205
                        elif funding_instype == 'Call I/Div SARB':
                            funding = 2233
                        elif funding_instype == 'Call I/Div':
                            funding = 2231
                        elif funding_instype == 'Call I/Div DTI':
                            funding = 2232
                elif entity.acquirer_ptynbr.ptynbr == 32708: #ABCAP NON ZAR CFCI DIV
                    if entity.insaddr.instype == 'Deposit' and entity.insaddr.legs().members()!= [] and entity.insaddr.legs()[0].type == 'Call Fixed Adjustable':
                        if funding_instype == 'Non Zar CFC I/Div':
                            funding = 1202

        # Rule 35
        #Standard name for Contact Details
        if entity.record_type == 'Party' and operation != 'Delete':
            for c in entity.contacts():
                ruleMemCount = c.rules().members().__len__()
                matchRuleCountMM = 0
                matchRuleCountIRD = 0
                matchRuleCountNLD = 0
                matchRuleCountMetal = 0
                matchRuleCountGold = 0
                fullname = entity.attention
                for cr in c.rules():
                    if cr.event_chlnbr:
                        if cr.event_chlnbr.entry == 'Money Market' and cr.instype == 'Deposit' and cr.curr.insid == 'ZAR':
                            matchRuleCountMM += 1
                            fullname = ('MM/Dep/Z/' + c.attention)[0:39]
                        if cr.event_chlnbr.entry in ('New Trade', 'Close', 'Partial Close') and cr.instype in ('Cap', 'CurrSwap', 'Floor', 'FRA', 'IndexLinkedSwap', 'Swap', 'Option'):
                            if cr.acquirer_ptynbr:
                                if cr.acquirer_ptynbr.ptyid == 'IRD DESK':
                                    matchRuleCountIRD += 1
                                    fullname = ('IRD/Affirmation/' + c.attention)[0:39]
                                elif cr.acquirer_ptynbr.ptyid == 'NLD DESK':
                                    matchRuleCountNLD += 1
                                    fullname = ('NLD/Affirmation/' + c.attention)[0:39]
                            else:
                                if entity.ptyid == 'IRD DESK':
                                    matchRuleCountIRD += 1
                                    fullname = ('IRD/Affirmation/' + c.attention)[0:39]
                                elif entity.ptyid == 'NLD DESK':
                                    matchRuleCountNLD += 1
                                    fullname = ('NLD/Affirmation/' + c.attention)[0:39]
                    if cr.acquirer_ptynbr:
                        if cr.acquirer_ptynbr.ptyid == 'Metals Desk':
                            matchRuleCountMetal += 1
                            fullname = ('MTL/Confirmations/' + c.attention)[0:39]
                        elif cr.acquirer_ptynbr.ptyid == 'Gold Desk':
                            matchRuleCountGold += 1
                            fullname = ('GLD/Confirmations/' + c.attention)[0:39]


        # Rule 36
        # Validate Adjust Deposit and cashflow adjustments
        if (entity.record_type == 'Instrument' and operation == 'Update' and
                entity.instype == 'Deposit' and entity.legs() and
                entity.legs()[0].type == 'Call Fixed Adjustable' and
                len(entity.original().trades()) == 1):
            t = entity.original().trades()[0]
            # 2016-03-02 ABITFA-4121: Check only if a credit limit is set for
            # the counterparty and department.
            counterparty = t.counterparty_ptynbr
            department = t.acquirer_ptynbr
            if FCreditLimit.get_credit_limits(counterparty, department):
                if t.status not in ('Simulated', 'Void', 'Terminated') and t.add_info('Funding Instype') in ('Call Loan DTI', 'Call Loan NonDTI'):
                    c1 = round(FCreditLimit.credit_tot_cp_A(t), 2)
                    cf = entity.legs()[0].cash_flows()
                    r = 0
                    for c in cf:
                        if c.type == 'Fixed Amount':
                            if ael.CashFlow[c.cfwnbr].fixed_amount != c.fixed_amount and (c.creat_time != 0):
                                r = r +(c1 + (ael.CashFlow[c.cfwnbr].fixed_amount - c.fixed_amount))
                            if c.creat_time == 0:
                                r = r + (c1 - (c.fixed_amount))

                    r = round(r, 2)
                    if (c1 < 0) and (r < c1):
                        raise ValidationError('FV36-1: Unable to adjust deposit. Please check the Credit Limit for the counterparty')

                    if (c1 >= 0) and (r < 0):
                        raise ValidationError('FV36-2: Unable to adjust deposit. Please check the Credit Limit for the counterparty')
            else:
                msg = ("Notice: FV36: Trade {0}: No credit limit set for counterparty '{1}' "
                       "and Department '{2}'. Skipping credit limit checks.")
                print(msg.format(t.trdnbr, counterparty.ptyid, department.ptyid))


        # Rule 37
        #Validate credit limit for trade
        if (entity.record_type == 'Trade' and operation != 'Delete' and
                entity.insaddr.instype == 'Deposit' and
                entity.status not in ('Simulated', 'Void', 'Terminated')):
            # 2016-03-02 ABITFA-4121: Check only if a credit limit is set for
            # the counterparty and department.
            counterparty = entity.counterparty_ptynbr
            department = entity.acquirer_ptynbr
            if FCreditLimit.get_credit_limits(counterparty, department):
                c1 = 0
                if entity.add_info('Funding Instype') in ('Call Loan DTI', 'Call Loan NonDTI'):
                    c1 = round(FCreditLimit.credit_tot_cp_A(entity), 2)
                if entity.add_info('Funding Instype') in ('FLI', 'FTL'):
                    x = round(FCreditLimit.credit_tot_cp_A(entity), 2)
                    if operation == 'Insert':
                        c1 = x
                    elif entity.original().status in ("Simulated", "Void", "Terminated"):
                        # NOTE: FAU-2933: This fixes a flaw in the logic that
                        # allowed booking a trade that breaks the limits as
                        # Simulated first and then FO/BO confirming it, hence
                        # causing a real credit limits break.
                        c1 = x + -1*entity.nominal_amount()
                    else:
                        c1 = x + -1*(entity.nominal_amount() - entity.original().nominal_amount())
                if c1 < 0:
                    raise ValidationError('FV37: Unable to update/insert trade. Please check the Credit Limit for the counterparty')
            else:
                msg = ("Notice: FV37: No credit limit set for Counterparty '{0}' "
                       "and Department '{1}'. Skipping credit limit checks.")
                print(msg.format(counterparty.ptyid, department.ptyid))




        # ******************************** CALL ******************************** #


        # Rule 38
        #if a SAVE NEW is done on an existing trade, CP ref is reset.
        if entity.record_type == 'Trade' and operation == 'Insert':

            #if trade is Closed, sales person and credits deleted on closed trade
            if entity.type == 'Closing':
                if (entity.sales_person_usrnbr != None) or (entity.sales_credit != 0):
                    entity.sales_person_usrnbr = ''
                    entity.sales_person_usrnbr = 0
                    print 'FV38: Sales person/credit set to blank for Closing trade'

                aDel = []     # arrays of add_infos to delete
                for a in entity.additional_infos():
                    if a.addinf_specnbr.field_name in ('Sales_Credit2', 'Sales_Credit3', 'Sales_Credit4', 'Sales_Credit5'):
                        aDel.append(a)
                    elif a.addinf_specnbr.field_name in ('Sales_Person2', 'Sales_Person3', 'Sales_Person4', 'Sales_Person5'):
                        aDel.append(a)

                # do the actual delete of the add_infos
                for a in aDel:
                    a.delete()


        # Rule 39, 40
        # Only Index Linked Bonds with a 0d rolling period and FreeDefCF instruments with
        # Fixed Rate cashflows with Nominal Scaling resets should be affected.
        if entity.record_type == 'Instrument' and operation in ('Insert', 'Update'):
            if entity.instype == 'IndexLinkedBond' and entity.legs()[0].rolling_period == '0d':
                i = entity
                iilb = 1
            elif entity.instype == 'IndexLinkedSwap':
                legs = entity.legs()
                for l in legs:
                    if l.nominal_scaling == 'CPI' and l.rolling_period == '0d':
                        i = entity
                        iilb = 1

        # Rule 41
        # Only trades on Index Linked Bonds with a 0d rolling period and FreeDefCF instruments
        # with Fixed Rate cashflows with Nominal Scaling resets should be affected.
        if entity.record_type == 'Trade' and operation in ('Insert', 'Update'):
            if entity.insaddr.instype == 'IndexLinkedBond' and entity.insaddr.legs()[0].rolling_period == '0d':
                trds.append(entity)
                i = entity.insaddr
                ilb = 1


        #print ilb, iilb
        # Get the legs and cashflows that will have the smple rate calculated and stored
        if iilb == 1:
            ai = 0
            if i.instype == 'IndexLinkedBond':
                l = i.legs()[0]
                cfs = l.cash_flows()
                lgs.append(l)
            elif i.instype == 'IndexLinkedSwap':
                legs = entity.legs()
                for l in legs:
                    if l.nominal_scaling == 'CPI' and l.rolling_period == '0d':
                        cfs = l.cash_flows()
                        lgs.append(l)



            # Calculate and store the simple rate at the leg level. This is done by taking the NACS rate
            # in the Additional Info field NACSRate on the instrument and converting it firstly to a
            # continuous rate and then to a simple rate.
            for l in lgs:
                if not i.add_info('NACSRate'):
                    raise DataValidationError('FV41: Enter the NACS rate in the Additional Info field NACSRate')
                NACS_rate = float(i.add_info('NACSRate')) /100.0 #l.fixed_rate / 100 #
                NACC_rate = 2 * math.log(1 + NACS_rate/2)
                years = l.start_day.years_between(l.end_day, l.daycount_method)
                NACSimple_rate = (math.exp(NACC_rate * years) -1) * 1/years * 100
                l.fixed_rate = NACSimple_rate

            # Calculate and store the simple rate at the cashflow level.
            for c in cfs:
                if c.type == 'Fixed Rate':
                    c.rate = NACSimple_rate

                    # Ensure the reset has the correct dates stored. If not, update it.
                    for r in c.resets():
                        if r.day != l.end_day or r.start_day != l.end_day or r.end_day != l.end_day:
                            r.day = l.end_day
                            r.start_day = l.end_day
                            r.end_day = l.end_day

        if ilb == 1:
            ai = 0
            if i.instype == 'IndexLinkedBond':
                l = i.legs()[0]
                cfs = l.cash_flows()
            elif i.instype == 'FreeDefCF':
                for l in i.legs():
                    for cf in l.cash_flows():
                        if cf.type == 'Fixed Rate':
                            for r in cf.resets():
                                if r.type == 'Nominal Scaling':
                                    cfs = l.cash_flows()

            # Get the fixed rate from the appropriate cashflow.
            fixed_rate = 0.0
            for c in cfs:
                if c.type == 'Fixed Rate':
                    fixed_rate = c.rate

            # Calculate and store the Guaranteed Amount into the Additional Field IL_GuaranteedAmount.
            for t in trds:
                nom = t.quantity * i.contr_size #t.nominal_amount()
                years = l.start_day.years_between(l.end_day, l.daycount_method)
                day_count = l.daycount_method

                # Calculate the guaranteed amount and round it to 2dp.
                ga = nom + (nom * fixed_rate/100 * years)
                ga = round(ga, 2)
                ga_str = str(ga)
                for addinfo in t.additional_infos():
                    if addinfo.addinf_specnbr.field_name == 'IL_GuaranteedAmount':
                        addinfo.value = ga_str
                        ai = 1

                if ai == 0:
                    ai_new = ael.AdditionalInfo.new(t)
                    ai_new.value = ga_str
                    ais = ael.AdditionalInfoSpec['IL_GuaranteedAmount']
                    ai_new.addinf_specnbr = ais.specnbr
                    # The ai is commited with the trade.
                    #ai_new.commit()
                    ai = 1



        # Rule 42
        #   Check Repo rate != 0
        if entity.record_type == 'Instrument' and operation in ('Insert', 'Update'):
            if entity.instype in ('Repo/Reverse', 'BuySellback') and entity.und_instype == 'Bond':
                if (entity.instype == 'Repo/Reverse' and entity.legs()[0].fixed_rate == 0.0 and entity.legs()[0].type == 'Fixed') or (entity.instype == 'BuySellback' and entity.rate == 0.0):
                    raise DataValidationError('FV42: Zero repo rate entered - please enter a valid repo rate > 0 - for free-of-value trades, enter zero 1st cash')

        # Rule 43
        # Set instrument spot days offset to 0 for BSBs.
        if entity.record_type in ('Instrument', 'Trade') and operation in ('Insert', 'Update'):
            if entity.record_type == 'Trade':
                if entity.insaddr.instype in ('BuySellback', 'Repo/Reverse') and entity.insaddr.und_instype in ('Bond', 'IndexLinkedBond'):
                    if entity.insaddr.spot_banking_days_offset == 2:
                        entity.insaddr.spot_banking_days_offset = 0
                        print 'FV43a: Instrument spot banking days offset set to zero'
            else:
                if entity.instype in ('BuySellback', 'Repo/Reverse') and entity.und_instype in ('Bond', 'IndexLinkedBond'):
                    if entity.spot_banking_days_offset == 2:
                        entity.spot_banking_days_offset = 0
                        print 'FV43b: Instrument spot banking days offset set to zero'


        # ####################### TMS VALIDATIONS ####################### #
        # Rule 47
        # Check if this is TMS related or not
        if entity.record_type == 'Trade' and operation in ('Update', 'Insert') and entity.prfnbr:
            if entity.prfnbr.add_info("BarCap_TMS_Feed") in ("Production", "Test"):
                # Rule 48
                #Allowable Conversion check for FX TMS Trades - FX Cash Instruments
                if operation == "Update" and entity.insaddr.instype == "Curr" and TMS_Config_Trade.isConsideredForTMS(entity):
                    TObject = entity
                    TObject_Previous = entity.original()

                    try:
                        if (TObject.trade_process in (4096, 8192) and TObject_Previous.trade_process in (16384, 32768)):
                            raise DataValidationError('FV48-1: UPDATE NOT ALLOWED - FrontTMS Trade Feed: Conversion from FXSwap to FXOutright\FXSpot not allowable.')

                        if (TObject.trade_process in (16384, 32768) and TObject_Previous.trade_process in (4096, 8192)):
                            raise DataValidationError('FV48-2: UPDATE NOT ALLOWED - FrontTMS Trade Feed: Conversion from FXOutright\FXSpot to FXSwap not allowable.')

                    except TypeError, e:
                        print 'FV48: FrontTMS Trade Feed - Allowable conversions , %s' % (e)


        # Rule 49
        #Allowable Conversion check for FX TMS Trades - FX Options
        if entity.record_type == "Instrument" and operation == "Update" and entity.instype == "Option" and entity.und_insaddr.instype == "Curr":
            try:
                IObject = entity
                IObject_Previous = entity.original()
                #changing to the following could yield a smaller number of trades returned
                trades = [trd for trd in IObject_Previous.trades() if not trd.status in ("Void", "Terminated") and trd.prfnbr]
                if len(trades):
                        for trd in trades:
                            if trd.prfnbr.add_info("BarCap_TMS_Feed") in ("Production", "Test") and TMS_Config_Trade.getTradeAssetClass(trd) and TMS_Config_Trade.isConsideredForTMS(trd):
                                if not TMS_AMBA_Message.AllowConversion(trd, trd, IObject, IObject_Previous):
                                    raise ValidationError('FV49: UPDATE NOT ALLOWED - FrontTMS Trade Feed: Conversion from %s to %s not allowable.' % ( TMS_AMBA_Message._fxSupportsTradeMessage_(IObject_Previous)._name(),  TMS_AMBA_Message._fxSupportsTradeMessage_(IObject)._name() ))

            except TypeError, e:
                print 'FV49: FrontTMS Trade Feed - Allowable conversions , %s' % (e)

        # ####################### TMS VALIDATIONS ####################### #


        # ####################### MONEY MARKET VALIDATIONS ####################### #

        # Rule 50
        #Traders in the group - FO FX Sales inc MM - are only allowed to FO Confirm Money Market trades but are allowed to FO Sales any other trade
        if entity.record_type == 'Trade' and operation != 'Delete':
            users = ael.user()
            if users.grpnbr.grpnbr == 626: #FO FX Sales inc MM
                if entity.insaddr.instype != 'Deposit':
                    if entity.status == 'FO Confirmed':
                        raise ValidationError("FV50: Traders in the group - FO FX Sales inc MM - cannot FO Confirm non Money Market trades")



        # Rule 51
        #Money Market Traders Not allowed To Amend Trades In FO confirmed Status After The First Day-End
        if entity.record_type == 'Trade' and operation == 'Update':
            if entity.acquirer_ptynbr:
                if entity.acquirer_ptynbr.ptyid == 'Funding Desk':
                    users = ael.user()
                    if users.grpnbr.grpnbr == 601: #FO MM Trader
                        if ael.date_today().days_between(ael.date_from_time(entity.creat_time)) < 0:
                            if entity.status in ('FO Confirmed'):
                                raise ValidationError("FV51: Money Market Traders Not Allowed To Amendment Trades After First Day End")

        # Rule 52
        if entity.record_type == 'Instrument' and operation == 'Update':
            if entity.original().trades():
                for t in entity.original().trades():
                    if t.acquirer_ptynbr:
                        if t.acquirer_ptynbr.ptynbr == 2247: # Funding Desk
                            users = ael.user()
                            if users.grpnbr.grpnbr == 601:
                                if ael.date_today().days_between(ael.date_from_time(entity.creat_time)) < 0:
                                    if t.status in ('FO Confirmed'):
                                        raise ValidationError("FV52: Money Market Traders Not Allowed To Amendment Trades After First Day End")


        # Modify Confirm Rules # #####################################################

        # Rule 55
        # (Change Request: 282030) When creating a trade for the first time FO Call Traders can only create trades in Simulated or FO Confirmed status
        # NOTE: This rule should go into FTradeStatus hook. (2015-02-11 Vojtech
        # Sidorin)
        if entity.record_type == 'Trade' and operation in ('Insert'):
            if ael.user().grpnbr.grpnbr in (601, 517, 592, 596, 978):
                if entity.status not in ('Simulated', 'FO Confirmed'):
                    raise ValidationError("FV55: FO Call Traders can only create trades in Simulated or FO Confirmed status")

        # Modify Confirm Rules # #####################################################


        # #################### NON ZAR FUNDING ################################# #
        # Rule 56
        if entity.record_type == 'Trade' and operation != 'Delete':
            if entity.acquirer_ptynbr:
                if entity.acquirer_ptynbr.ptynbr == 31756: #Non ZAR Desk
                    if entity.insaddr.instype == 'Deposit':
                        if entity.add_info('Funding Instype') == 'Non ZAR Funding':
                            if not entity.add_info('NonZAR_Deal Number'):
                                raise ValidationError('FV56: NonZAR_Deal Number not entered')

                            #get the original status
                            try:
                                addInfo = entity.original().add_info('NonZAR_Status')
                            except:
                                addInfo = ''

                            #Update the NonZAR_Status to Amended to keep track it the trade has been updated
                            #If original status is blank then do not update the status
                            if operation == 'Update' and addInfo != '':
                                status = 'Amended'
                                found = 0
                                spec = ael.AdditionalInfoSpec['NonZAR_Status']
                                for ai in entity.additional_infos():
                                    if ai.addinf_specnbr == spec:
                                        ai_c = ai.clone()
                                        ai_c.value = status
                                        # Addinfo is saved automatically with the trade.
                                        #ai_c.commit()
        # #################### NON ZAR FUNDING ################################# #

        # Rule 57
        # DEFAULT PRICE FINDING GROUP FOR INS WITH MTM_FROM_FEED
        if ael.user().grpnbr not in sys_exclude:
            if entity.record_type == 'Instrument' and operation != 'Delete':
                if entity.mtm_from_feed == 1 and not entity.price_finding_chlnbr:
                    raise ValidationError('FV57: ERROR: NO PRICE FINDING GROUP HAS BEEN SELECTED')

        # Rule 59
        #Broker fee additional payment for Stocks and ETFs
        if entity.record_type == 'Trade' and operation != 'Delete':
            if entity.insaddr.instype in ('Stock', 'ETF'):
                if entity.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                    #if entity.counterparty_ptynbr.ptyid == Broker_CP_ptyid: # this condition has been moved to SAEQ_BrokerFees.AddBrokerFee
                    if not(entity.add_info('Broker_Fee_Exclude') and entity.add_info('Broker_Fee_Exclude') == 'Yes'):
                        if not(entity.prfnbr.add_info('PS_PortfolioType')) or (entity.prfnbr.add_info('PS_PortfolioType') and entity.prfnbr.add_info('PS_PortfolioType') not in ['General', 'CFD Allocation', 'Cash Equity Allocation']):
                            SAEQ_BrokerFees.AddBrokerFee(entity)

        # Rule 60
        # Trades With Acquirer Funding Desk And Status Legally Confirmed Not Allowed
        if entity.record_type == 'Trade' and operation in ('Update', 'Insert'):
            if entity.acquirer_ptynbr:
                if entity.acquirer_ptynbr.ptynbr == 2247:         #Funding Desk
                    if entity.status == 'Legally Confirmed':
                        raise ValidationError("FV60: Trades With Acquirer Funding Desk And Status Legally Confirmed Not Allowed")

        # Rule 61
        # If amount is captured in Sales Credit or Value Added, Sales Person should be populated as well
        if ael.user().grpnbr.grpid not in ('Integration Process', 'System Processes'):
            if entity.record_type == 'Trade' and ((operation == 'Insert' and entity.type == 'Normal') or (operation == 'Update')):
                if entity.insaddr.instype != 'Curr':
                    if (((entity.sales_credit != 0 or entity.add_info('ValueAddCredits') != '') and entity.sales_person_usrnbr == None) or
                        ((entity.add_info('Sales_Credit2') != '' or entity.add_info('ValueAddCredits2') != '') and entity.add_info('Sales_Person2') == '') or
                        ((entity.add_info('Sales_Credit2') == '' and entity.add_info('ValueAddCredits2') == '') and entity.add_info('Sales_Person2') != '') or
                        ((entity.add_info('Sales_Credit3') != '' or entity.add_info('ValueAddCredits3') != '') and entity.add_info('Sales_Person3') == '') or
                        ((entity.add_info('Sales_Credit3') == '' and entity.add_info('ValueAddCredits3') == '') and entity.add_info('Sales_Person3') != '') or
                        ((entity.add_info('Sales_Credit4') != '' or entity.add_info('ValueAddCredits4') != '')  and entity.add_info('Sales_Person4') == '') or
                        ((entity.add_info('Sales_Credit4') == '' and entity.add_info('ValueAddCredits4') == '') and entity.add_info('Sales_Person4') != '') or
                        ((entity.add_info('Sales_Credit5') != '' or entity.add_info('ValueAddCredits5') != '') and entity.add_info('Sales_Person5') == '') or
                        ((entity.add_info('Sales_Credit5') == '' and entity.add_info('ValueAddCredits5') == '') and entity.add_info('Sales_Person5') != '')):
                        raise ValidationError("FV61: Blank Sales Person field not allowed with non-zero Sales Credit or Value Added Credit")

        # Rule 62
        #Only floating values allowed for Sales Credit and Value Add
        if ael.user().grpnbr.grpid not in ('Integration Process', 'System Processes'):
            if entity.record_type == 'Trade' and operation in ('Insert', 'Update'):
                #Value Add 1
                try:
                    sales = 'ValueAddCredits'
                    if entity.add_info(sales) != '':
                        float(entity.add_info(sales))
                except:
                    raise ValidationError('FV62: ' + sales + ' is invalid number: ' + entity.add_info(sales))
                #All other sales credit and value adds
                i = 2
                while i <= 5:
                    try:
                        sales = 'Sales_Credit' + str(i)
                        if entity.add_info(sales) != '':
                            float(entity.add_info(sales))
                        sales = 'ValueAddCredits' + str(i)
                        if entity.add_info(sales) != '':
                            float(entity.add_info(sales))
                    except:
                        raise ValidationError('FV62: ' + sales + ' is invalid number: ' + entity.add_info(sales))
                    i = i + 1

        # Rule 65
        # A Sales Person may not be captured more than once
        if ael.user().grpnbr.grpid not in ('Integration Process', 'System Processes'):
            if entity.record_type == 'Trade' and operation  in ('Insert', 'Update'):
                if(((entity.sales_person_usrnbr != None and entity.add_info('Sales_Person2') != '') and (entity.sales_person_usrnbr.userid == entity.add_info('Sales_Person2'))) or ((entity.sales_person_usrnbr != None and entity.add_info('Sales_Person3') != '') and (entity.sales_person_usrnbr.userid == entity.add_info('Sales_Person3'))) or ((entity.sales_person_usrnbr != None and entity.add_info('Sales_Person4') != '') and (entity.sales_person_usrnbr.userid == entity.add_info('Sales_Person4'))) or ((entity.sales_person_usrnbr != None and entity.add_info('Sales_Person5') != '') and (entity.sales_person_usrnbr.userid == entity.add_info('Sales_Person5')))
                    or ((entity.add_info('Sales_Person2') != '' and entity.add_info('Sales_Person3') != '') and (entity.add_info('Sales_Person2') == entity.add_info('Sales_Person3'))) or ((entity.add_info('Sales_Person2') != '' and entity.add_info('Sales_Person4') != '') and (entity.add_info('Sales_Person2') == entity.add_info('Sales_Person4'))) or ((entity.add_info('Sales_Person2') != '' and entity.add_info('Sales_Person5') != '') and (entity.add_info('Sales_Person2') == entity.add_info('Sales_Person5')))
                    or ((entity.add_info('Sales_Person3') != '' and entity.add_info('Sales_Person4') != '') and (entity.add_info('Sales_Person3') == entity.add_info('Sales_Person4'))) or ((entity.add_info('Sales_Person3') != '' and entity.add_info('Sales_Person5') != '') and (entity.add_info('Sales_Person3') == entity.add_info('Sales_Person5')))
                    or ((entity.add_info('Sales_Person4') != '' and entity.add_info('Sales_Person5') != '') and (entity.add_info('Sales_Person4') == entity.add_info('Sales_Person5')))):
                    raise ValidationError("FV65: Same Sales Person should not be populated in more than one field")

        # Rule 66
        # Stops amendments on trades already fed to Midbase FX except for system and middle office users (fo_tcu)
        if ael.user().grpnbr not in sys_exclude and ael.user().grpnbr != fo_tcu:
            if entity.record_type == 'Trade' and operation == 'Update' and entity.insaddr.instype in ('Curr'):
                old_entity = entity.original()
                if old_entity.add_info('MIDAS_MSG'):
                    if old_entity.add_info('MIDAS_MSG') == 'Sent':
                        for fl in Midas_field_list:
                            if eval("entity." + fl) <> eval("old_entity." + fl):
                                raise ValidationError("FV66: Amendment not allowed, trade already sent to Midbase FX")


        # ########### FX Trades Validations ########### #
        if entity.record_type == 'Trade' and operation == 'Update' and entity.insaddr.instype == 'Curr':
            if not acm.FTrade[entity.trdnbr].IsCashPayment():
                if  ael.user().grpnbr not in [fo_tcu, fo_tcu_management] and entity.status == 'Void':
                    today = ael.date_today()
                    value_day = entity.value_day
                    curr_pair = ael.CurrencyPair[entity.insaddr.insid + "/" + entity.curr.insid]
                    spot_date = curr_pair.spot_date()
                    spot_days_offset = today.days_between(spot_date)
                    days_to_settlement = today.days_between(value_day)
                    if  days_to_settlement <= spot_days_offset:
                        raise ValidationError("FV114: Cannot void FX trades settling in %s days, please contact FO TCU to void" %days_to_settlement)

        # ########### UT Portfolio checks ########### #

        # Rule 102
        # Stops booking trades into portfolios without any portfolio link (orphan portfolios)
        if entity.record_type == 'Trade' and operation in ('Insert', 'Update'):
            portfolio = entity.prfnbr
            portfolioLink = ael.PortfolioLink.select('member_prfnbr = %i' % portfolio.prfnbr)
            if not portfolioLink:
                raise ValidationError("FV102: Booking a trade into orphan portfolio '%s' not allowed" %portfolio.prfid)

        # Rule 103
        # Disable inserting portfolios from GRAVEYARD into regular portfolio structure
        if entity.record_type == 'PortfolioLink' and operation == 'Insert':
            if get_Port_Struct_from_Port(entity.member_prfnbr, 'GRAVEYARD'):
                raise ValidationError("FV103: Cannot link a portfolio from Graveyard into regular portfolio tree", popup=True)

        # Rule 107
        # Disable booking new trades into GRAVEYARD portfolio structure
        if entity.record_type == 'Trade' and operation == 'Insert':
            if get_Port_Struct_from_Port(entity.prfnbr, 'GRAVEYARD'):
                raise ValidationError("FV107: Unable to book a trade into Graveyard portfolio '%s'" %entity.prfnbr.prfid)
                
        # Rule 108
        # Disable moving trades from GRAVEYARD portfolio structure back into a live book
        if entity.record_type == 'Trade' and operation == 'Update':
            if (not get_Port_Struct_from_Port(entity.prfnbr, 'GRAVEYARD') and
                get_Port_Struct_from_Port(entity.original().prfnbr, 'GRAVEYARD')):
                raise ValidationError("FV108: Unable to move a trade from the Graveyard portfolio '%s'"
                    %entity.original().prfnbr.prfid + " into the live portfolio '%s'." %entity.prfnbr.prfid)

        # Rule 109
        # Only MO is allowed to move portfolios to GRAVEYARD
        if entity.record_type == 'PortfolioLink' and operation in ('Insert', 'Update'):
            if (get_Port_Struct_from_Port(entity.owner_prfnbr, 'GRAVEYARD') and
                not ael.user().grpnbr in graveyarding_groups):
                raise ValidationError("FV109: Only MO users can move portfolios to Graveyard.", popup=True)

        # rule 110
        # Only MO is allowed to move trades into GRAVEYARD
        if entity.record_type == 'Trade' and operation == 'Update':
            if bool(get_Port_Struct_from_Port(entity.prfnbr, 'GRAVEYARD')) and ael.user().grpnbr not in graveyarding_groups:
                raise ValidationError("FV110: Unable to move a trade into the Graveyard portfolio '%s'" %entity.prfnbr.prfid)

        # Rule 111
        # If a portfolio is in status Pending and is being moved to Active, the add info BMW Ref has to be filled in
        if (entity.record_type == 'Portfolio' and operation == 'Update'):
            add_inf_events = {}
            for e, op in transaction_list:
                if (e.record_type == 'AdditionalInfo' and
                    e.addinf_specnbr.rec_type == 'Portfolio' and
                    e.addinf_specnbr.field_name in ('BMW Ref', 'Portfolio Status')):
                    add_inf_events[e.addinf_specnbr.field_name] = e

            if (add_inf_events.has_key('Portfolio Status') and
                add_inf_events['Portfolio Status'].original().value == 'Pending' and
                add_inf_events['Portfolio Status'].value == 'Active'):
                if entity.add_info('BMW Ref') in (None, ''):
                    if (not add_inf_events.has_key('BMW Ref') or
                        (add_inf_events.has_key('BMW Ref') and
                         add_inf_events['BMW Ref'].value in (None, ''))):
                        raise ValidationError('FV111: Active Portfolios must have a BMW Ref')

        # Rule 112
        # If a portfolio is moved to the Graveyard, the status must be set to Closed
        if entity.record_type == 'PortfolioLink' and operation in ('Insert', 'Update'):
            if get_Port_Struct_from_Port(entity.owner_prfnbr, 'GRAVEYARD') and entity.member_prfnbr.add_info('Portfolio Status') != 'Closed':
                raise ValidationError('FV112: If a portfolio is moved to the Graveyard, the status must be set to Closed')

        # ############### CONFIRMATION VALIDATION ############### #
        # Rule 67
        VALID_CONFIRMATION_INSTYPES = ['Cap', 'CurrSwap', 'Floor', 'FRA', 'IndexLinkedSwap', 'Swap', 'Option']
        VALID_CONFIRMATION_ACQUIRERS = ['IRD DESK', 'NLD DESK']
        if entity.record_type == 'Trade' and operation != 'Delete':
            if entity.insaddr.instype in (VALID_CONFIRMATION_INSTYPES):
                if entity.acquirer_ptynbr:
                    if entity.acquirer_ptynbr.ptynbr in (VALID_CONFIRMATION_ACQUIRERS):
                        #If Affirmation is set to No - Affirmation Affirmation CP Ref needs to be filled in.
                        if entity.add_info('Affirmation') == 'No':
                            if entity.add_info('Affirmation CP Ref') == '':
                                raise ValidationError('FV67: This trade need a reason for not Affirming. Please fill in the reson in the field Affirmation CP Ref.')

        # Rule 68
        if entity.record_type == 'Confirmation' and operation == 'Insert':
            if entity.event_chlnbr.entry == 'Rate Fixing':
                transaction_list = []

        # Rule 69
        # Check if addinfo Approx. load is set and prompt for Approx. load ref addinfo to have a value set if not already set
        if ael.user().grpnbr not in sys_exclude:
            if entity.record_type == 'Trade' and operation in ('Insert', 'Update'):
                if entity.insaddr.instype != 'Curr':
                    if entity.add_info('Approx. load'):
                        if entity.add_info('Approx. load') == 'Yes':
                            if not (entity.add_info('Approx. load ref')):
                                raise ValidationError("FV69: Please enter a value for Approx. load ref.")
                    if  not (entity.add_info('Approx. load ref') == ''):
                        if not (entity.add_info('Approx. load') == 'Yes'):
                            raise ValidationError("FV69: Please set Approx. load field to 'Yes' ")
                            
        #FX OPTIONS
        # Rule 70
        if entity.record_type == 'Instrument' and operation != 'Delete':
            if entity.instype == 'Option' and entity.und_instype == 'Curr':
                if entity.add_info('Settlement_Curr') and entity.settlement != 'Cash':
                    entity.settlement = 'Cash'
	
        # Rule 71
	# 597 = "FO Rates Opt Trader" and 676 = "FO_FX_OPT_HEAD"
        if USERGROUPNBR in (597, 676):
            if entity.record_type == 'Instrument' and operation == 'Update':
                _flag = 0
                if entity.original().trades():
                    for t in entity.original().trades():
                        if t.status in ('BO Confirmed', 'BO-BO Confirmed'):
                            _flag = 1
                            break
                if _flag == 1:
                    if entity.instype == 'Option' and entity.und_instype == 'Curr':
                        if SAGEN_YC_VOL_ACCESS.check_attrfx(entity, entity.original()) == 1:
                            raise AccessValidationError('FV71-c: ERROR: YOU DO NOT HAVE ACCESS TO UPDATE AN INSTRUMENT WITH BO/BO-BO Confirmed TRADES.')
                        if entity.exotic() != None and entity.original().exotic() != None:
                            if SAGEN_YC_VOL_ACCESS.check_attrfx(entity.exotic(), entity.original().exotic()) == 1:
                                raise AccessValidationError('ERROR: YOU ONLY HAVE ACCESS TO CHANGE BARRIER CROSSED STATUS')
                    else:
                        raise AccessValidationError('FV71-a,b: ERROR: YOU DO NOT HAVE ACCESS TO UPDATE AN INSTRUMENT WITH BO/BO-BO Confirmed TRADES.')

            # Rule 72
            if entity.record_type == 'Trade' and operation == 'Update':
                if entity.original().status in ('BO Confirmed', 'BO-BO Confirmed'):
                    raise AccessValidationError('FV72: ERROR: YOU DO NOT HAVE ACCESS TO UPDATE A TRADE IN BO/BO-BO Confirmed STATUS.')


    # Here's where everything from validate_entity went.
    for e, op in list(transaction_list):
        # Rule 2
        if e.record_type == 'Trade' and e.status == 'Simulated':
            FValidation_General.validate_cash_posting_trade_lock(e, op)
            if e.insaddr.instype != 'Deposit':
                continue

        # Rule 5
        #FXO Currency pair on trade key
        if e.record_type == 'Trade' and op != 'Delete':
            if (e.insaddr.instype == 'Option' and e.insaddr.und_instype == 'Curr') or e.insaddr.instype == 'Curr':
                cp = acm.FTrade[e.trdnbr].CurrencyPair()
                if cp and cp.Name() in CurrDict.keys():
                    e.optkey4_chlnbr = CurrDict[acm.FTrade[e.trdnbr].CurrencyPair().Name()]

        # Rule 6
        # Deletes Midas add_infos on Save New
        if e.record_type == 'AdditionalInfo' and op == 'Insert' and ael.user().grpnbr not in sys_exclude:
            #MIDAS_MSG
            if e.addinf_specnbr.specnbr == 834:
                if ael.user().userid in ('ACM_MMGCFR'):
                    e.value = 'Sent'
                else:
                    e.value = 'Not Sent'
            #Midas_Status,  Midas_ID_BTB, Midas_Status_BTB, Midas_ID
            elif e.addinf_specnbr.specnbr in (836, 837, 838, 839):
                e.value = ' '


        # ******************************** CALL ******************************** #

        # Rule 8
        if e.record_type in ('CashFlow', 'Reset') and op in ('Insert', 'Update') and ael.user().grpnbr.grpid not in ('Integration Process', 'System Processes'):
            if e.parent():
                # Rules 8-abc were removed.
                # Rule 8d
                if e.record_type == 'CashFlow':
                    if e.type in zeronom and zeronom[e.type](e) == 0:
                        raise ValidationError('FV8-d: ERROR: YOU CANNOT CREATE A CASHFLOW WITH ZERO NOMINAL, PLEASE REMOVE ' + e.type + ' WITH START DAY '+ e.pay_day.to_string())

        # Rule 10
        #Setting the insid of the call accounts
        if e.record_type == 'Trade' and op == 'Insert':
            if e.acquirer_ptynbr:
                if e.acquirer_ptynbr.ptynbr in (FUNDING_DESK, ABCAP_NON_ZAR_CFCI_DIV):
                    if e.insaddr.instype == 'Deposit' and e.insaddr.legs().members()!= [] and e.insaddr.legs()[0].type == 'Call Fixed Adjustable':
                        if funding != 0:
                            ins = e.insaddr.clone()
                            ins.insid = (str(e.insaddr.insaddr) + '-' + str(ins.curr.insid) + '-' + str(funding) + '-01')
                            ins.insid = str(ins.insid)[0:39]
                            transaction_list.append((ins, 'Update'))
                            #ins.commit()

        # Rule 11
        if e.record_type == 'Trade' and op == 'Update':
            if e.acquirer_ptynbr:
                if e.acquirer_ptynbr.ptynbr in (FUNDING_DESK, ABCAP_NON_ZAR_CFCI_DIV):
                    if e.insaddr.instype == 'Deposit' and e.insaddr.legs().members()!= [] and e.insaddr.legs()[0].type == 'Call Fixed Adjustable':
                        if funding != 0:
                            ins = e.insaddr.clone()
                            ins.insid = str(e.insaddr.insid)[0:39]
                            transaction_list.append((ins, 'Update'))
                            #ins.commit()



        # ******************************** CALL ******************************** #


        if e.record_type == 'Trade' and op != 'Delete':
            # Rule 17
            #XTP/HERMES - Anwar - 2010-08-25
            #Change default acquirer from EQ Derivatives Desk to the owner of the portfolio on the trade
            #for trades coming in via adaptor for stocks or etfs / against jse
            #2013-04-24 - small refactor, needed to included jse sa counterparty so consolidated all instruments and exchanges in single check
            if e.optional_key and  e.creat_usrnbr:
                if ((e.insaddr.instype in ('Stock', 'ETF', 'Option', 'Future/Forward')) and \
                    (e.creat_usrnbr.usrnbr == AMBA_USER) and \
                    (e.counterparty_ptynbr.ptynbr in (JSE_CPTY, SAFEX_CPTY, JSE_SA_CPTY, A2X_CPTY))) or \
                (e.creat_usrnbr.usrnbr == AMBA_USER and e.add_info('MarkitWire') and e.add_info('MarkitWire').startswith('MW')):
                    if e.prfnbr.owner_ptynbr:
                        e.acquirer_ptynbr = e.prfnbr.owner_ptynbr

    return transaction_list


def four_eyes_needed(transaction_list,*rest):
    ret = 1 # Assume four eyes
    return ret
