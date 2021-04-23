"""FValidation - General rules that don't belong to any specific group.

Before changing the code, please consult the Developer's Guide available at
<https://confluence.barcapint.com/display/ABCAPFA/FValidation+Developer%27s+Guide>.

A list of the implemented FValidation rules is kept at
<http://confluence.barcapint.com/display/ABCAPFA/FValidation+Rules>.
If you change the code, please update also that list to keep it up to date.


History
=======

2014-08-31      Vojtech Sidorin      CHNG0002210109 Initial implementation.
2014-09-11      Vojtech Sidorin      CHNG0002277788 Bugfix: Rule 81b: Check price only for deposit with leg other than "Float".
2014-09-23      Pavel Saparov        CHNG0002347014 Rule #115: Validating Instrument's Product Type choice entry.
2014-09-30      Dmitry Kovalenko     CHNG0002328679 Refactoring: removed msg_box functionality(it is now built in FValidation_core exceptions).
2014-11-25      Pavel Saparov        CHNG0002497219 Updating rule #115: Reverting validation back to InsOverride instead of Product Type field.
2015-02-11      Dmitry Kovalenko     ABITFA-2957 Added rules 121 and 122: Closing or graveyarding a portfolio with live risk is forbidden.
2015-02-24      Vojtech Sidorin      ABITFA-3415 Remove rules 121, 122 until the performance issue is solved.
2015-03-23      Vojtech Sidorin      FXFA-262 Move rule 58 from FValidation_FixedIncome and update: Allow booking non-simulated FXOptionDatedFwd.
2015-03-23      Vojtech Sidorin      Introduce new naming convention: Rule functions start with 'fv##'.
2015-04-01      Vojtech Sidorin      ABITFA-3280/FXFA-807 Move rules 46a, 46b from FValidation_depr and patch 46a to allow voiding FX Cash.
2015-07-21      Christo Rautenbach/Vojtech Sidorin ABITFA-3704 Add rule 123 to protect server resources for distributed sheets.
2015-08-20      Vojtech Sidorin      ABITFA-3743: Include rule numbers in messages.
2015-09-08      Vojtech Sidorin      ABITFA-3734: In rule 44, use default caller, and print notice when rule applies.
2015-09-23      Lawrence Mucheka     CHNG0003134082   Validate Party swift code (BIC) on entry.
2015-09-09      Vojtech Sidorin      ABITFA-3161: Add rule FV124: Forbid terminating trades with an unsettled premium.
2016-03-01      Frantisek Jahoda     ABITFA-2818 Move part of rule 22 into FUser.PasswordCheck method
2016-04-21      Vojtech Sidorin      ABITFA-2845: Add rule FV129: Forbid special characters in instrument names.
2016-05-03      Vojtech Sidorin      ABITFA-4266: Hotfix: Disable FV129.
2016-05-24      Vojtech Sidorin      ABITFA-4316: Update FV123: Exclude APS_* users from the rule.
2016-06-16      Vojtech Sidorin      DEMAT: Unify and improve coding style; follow naming conventions; improve docstrings.
2016-08-23      Manan Ghosh          CHNG0003898744 MM Demat validations fv130 and fv131 added.
2016-08-25      Manan Ghosh          CHNG0003908106 Added import of check_entity_amendments.
2016-09-06      Willie vd Bank       CHNG0003914707 Amended rule FV130 to allow portfolio changes and to exclude trades where the acqr and cpty BPIDs are the same.
2016-09-08      Vojtech Sidorin      ABITFA-2845: Reactivate rule FV129.
2016-10-10      Vojtech Sidorin      ABITFA-4467: FV29, FV63: Move to FValidation_General and refactor
2017-01-26      Willie van der Bank  Modified rule fv130 to use trade iso instrument
2017-12-11      Manan Ghosh          CHNG0005220511: Added rule fv132 for nominal validation of DIS trades
2018-03-06      Jaco Moulder         CHG1000227308: Disbale rule fv123_forbid_using_calc_env
2018-03-08      Sihle Gaxa           CHG1000212955: Removing rule on Party "Not trading" checkbox
2018-03-13      Sihle Gaxa           CHG1000256275: Updating Client Static rules in FValidation to ensure all fields are in Upper case and "FICA SBU" field is not manadatory
2018-04-19      Tibor Reiss          CHG1000393583, ABITFA-5359: Block creation of multiple portfolio links
2018-05-03      Tibor Reiss          CHG1000436602, ABITFA-5248: New rule fv139_prevent_booking_certain_backdated_trades for handling backdated trades (if acquirer=PRIME SERVICES DESK)
2018-07-05      Cuen Edwards         FAOPS-127: New rule FV140 to prevent changes to simulated trades created to own multi-trade confirmations.
2018-09-15      Sadanand Upase       FAOPS-222: Modified rule 135 for FICC accounts, this mandates that DetailsOfCharges field be set to OUR for a specific condition.
2019-11-01      Cuen Edwards         FAOPS-460: Added rule FV142 to allow for finer-grained access control to business processes based on state chart.
2020-05-15      Cuen Edwards         FAOPS-794: Replaced hard-coded DEMAT and DIS superusers with component check.  Some refactoring.
2020-05-19      Tawanda Mukhalela    FAOPS-798: Added rule FV143 to auto set the MM_Ceded_amount for call account
2020-05-05      Cuen Edwards         FAOPS-746: Added access control for SARB Sec Transfer Instruction business processes.
2020-10-09      Ncediso Nkambule     FAOPS-859: Added rule FV145 to restrictions on trading with non trading or non compliant counterparty.
"""

import ael
import acm

from FValidation_core import (validate_entity,
                              validate_transaction,
                              ValidationError,
                              DataValidationError,
                              AccessValidationError)
from FValidation_Utils import is_allowed, validate_payment_trading_party, validate_trading_counterparty
from FSwiftCheckBic import check_party_bics
from at_type_helpers import to_acm
from password_policy import PasswordPolicy
from demat_functions import is_demat, is_dis
from demat_isin_mgmt_menex import current_ins_available_amount, current_ins_authorised_amount
from at_time import datetime_from_string, to_date, date_today
from math import fabs

TIME_NOW = acm.Time.DateToday()
TIME_THREE_BDAYS_AGO = acm.FCalendar["ZAR Johannesburg"].AdjustBankingDays(TIME_NOW, -3)

@validate_transaction
def fv22_check_password_expiry(transaction_list):
    """Check expired passwords.

    If the password of the current user has expired, do not allow any
    transaction other than setting a new password.
    """
    if PasswordPolicy(acm.User()).is_password_expired():
        # Check if the transaction updates the expired password.
        for entity, operation in transaction_list:
            if ((entity.record_type == "AdditionalInfo" and
                    entity.record_type.addinf_specnbr.field_name ==
                    "PasswordResetDate" and operation == "Update") or
                    (entity.record_type == "User" and operation == "Update")):
                # Allow transaction that is setting a new password.
                break
        else:
            # Stop transaction and notify user.
            msg = ("FV22:\n"
                   "Your password has expired!\n"
                   "You will not be able to make changes to the database.\n"
                   "Please change your password under File>Preferences>"
                   "Passwords>ADS to regain change permission.")

            raise ValidationError(msg)

    return transaction_list


@validate_entity("Trade", "Insert", caller="validate_transaction")
def fv29_clear_ps_msgsentdate_addinfo(entity, operation):
    """Clear the PS_MsgSentDate add info on new trades."""
    EXCLUDE_GROUP_OIDS = [494,  # 494 = "Integration Process"
                          495]  # 495 = "System Processes"
    if ael.user().grpnbr.grpnbr in EXCLUDE_GROUP_OIDS:
        return
    for ai in entity.additional_infos():
        if ai.addinf_specnbr.field_name == "PS_MsgSentDate":
            ai.delete()
            print("FV29: The 'PS_MsgSentDate' Add Info was cleared.")


@validate_entity("Trade", "Update")
def fv44_set_trader_to_current_user(entity, operation):
    """Set Trader to the current user when confirming the trade.

    Set Trader to the current user when changing the trade status from
    'Simulated' or 'FO Sales' to 'FO Confirmed'.
    """
    trade = entity
    old_status = trade.original().status
    new_status = trade.status
    if (old_status in ("Simulated", "FO Sales") and
            new_status == "FO Confirmed" and
            trade.trader_usrnbr != ael.user()):
        trade.trader_usrnbr = ael.user()
        print("Notice: FV44: Trade {0}: The trader was set to {1}."
              .format(trade.trdnbr, ael.user().userid))


@validate_entity("Trade", "Insert", caller="validate_transaction")
def fv63_clear_sales_credits(entity, operation):
    """Clear sales credits on new non-Normal trades."""
    EXCLUDE_GROUP_OIDS = [494,  # 494 = "Integration Process"
                          495]  # 495 = "System Processes"
    ADD_INFOS_TO_CLEAR = [
            "Sales_Credit2", "Sales_Credit3", "Sales_Credit4", "Sales_Credit5",
            "Sales_Person2", "Sales_Person3", "Sales_Person4", "Sales_Person5",
            "ValueAddCredits", "ValueAddCredits2", "ValueAddCredits3",
            "ValueAddCredits4", "ValueAddCredits5"
            ]
    if ael.user().grpnbr.grpnbr in EXCLUDE_GROUP_OIDS:
        return
    if entity.type == "Normal":
        return

    cleared = False  # Flag: Whether any sales credit field was cleared.

    # Clear the built-in fields.
    if entity.sales_person_usrnbr:
        entity.sales_person_usrnbr = None
        cleared = True
    if entity.sales_credit:
        entity.sales_credit = 0
        cleared = True

    # Clear the Add Info fields.
    delete = []  # Add Infos to be deleted.
    for a in entity.additional_infos():
        if a.addinf_specnbr.field_name in ADD_INFOS_TO_CLEAR:
            delete.append(a)
    for a in delete:
        a.delete()
        cleared = True

    if cleared:
        print("FV63: Sales Credit data cleared.")


@validate_entity("Trade", "Update", caller="validate_transaction")
def fv80_forbid_updating_archived_and_aggregate_trades(entity, operation):
    """Forbid updating archived and aggragate trades."""
    trade = entity
    if trade.archive_status == 1:
        raise ValidationError("FV80: No changes allowed to archived trades.")
    if trade.aggregate in (1, 2):
        raise ValidationError("FV80: No changes allowed to aggregate trades.")


@validate_entity("Trade", "Insert")
def fv81_validate_deposits(entity, operation):
    """Validate new trades on non-open-ended deposits.

    Forbid trading non-open-ended deposits if
        (a) float_rate is not set for deposits with float leg; or
        (b) price is <= 0 for deposits with other leg types.
    """
    trade = entity
    instrument = trade.insaddr
    if instrument.instype == "Deposit" and instrument.open_end == "None":
        if instrument.legs() and instrument.legs()[0].type == "Float":
            # Rule 81a
            if instrument.legs()[0].float_rate in (None, ""):
                raise ValidationError("FV81a: Invalid float rate index.")
        elif trade.price <= 0:
            # Rule 81b
            raise ValidationError("FV81b: Invalid price; must be > 0.")


@validate_entity("Trade", "Insert")
def fv82_clear_counterparty_reference(entity, operation):
    """Clear counterparty reference (your_ref) on new trades."""
    trade = entity
    if trade.your_ref:
        trade.your_ref = ""
        print("FV82: Counterparty reference cleared.")


@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def fv115_validate_addinfo_insoverride(entity, operation):
    """Require InsOverride to be set in given cases.

    The add info InsOverride must be set if
        (1) instrument type is 'Combination'; or
        (2) add info 'Approx. load' is set to 'Yes'.
    """
    if ((entity.insaddr.instype == 'Combination' or
                entity.add_info('Approx. load') == 'Yes') and
            not entity.add_info('InsOverride')):
        raise ValidationError("FV115: Please select a value for InsOverride "
                              "in Add Info tab.")


@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def fv58_only_simulated_allowed(entity, operation):
    """Allow booking only simulated trades for given instruments."""
    RESTRICTED_INSTRUMENTS = (
            "BasketSecurityLoan",
            "CreditIndex",
            "Depositary Receipt",
            "DualCurrBond",
            "Fund",
            "Fx Rate",
            "MBS/ABS",
            "PriceIndex",
            "PromisLoan"
            )
    trade = entity
    if (trade.status != "Simulated"
            and trade.insaddr.instype in RESTRICTED_INSTRUMENTS):
        raise ValidationError("FV58: You can only book a simulated {0}"
                              .format(trade.insaddr.instype))


@validate_entity("Trade", "Update")
@validate_entity("Trade", "Delete")
def fv46_forbid_editing_voided_trades(entity, operation):
    """Forbid updating or deleting voided trades."""
    EXCLUDE_USER_OIDS = [130]   # 130 = "AMBA"
    EXCLUDE_GROUP_OIDS = [494]  # 494 = "Integration Process"
    trade = entity
    user = acm.User()
    group = user.UserGroup()
    # Don't apply the rule to excluded users and groups.
    if user.Oid() in EXCLUDE_USER_OIDS or group.Oid() in EXCLUDE_GROUP_OIDS:
        return
    if operation == "Update":
        # Rule 46a
        orig_trade = trade.original()
        orig_status = orig_trade.status
        forbid_msg = "FV46a: You are not allowed to update voided trades."
        # FXFA-807 Apply patch to trade status.
        # FIXME Remove once fixed Prime is deployed (>= 2015.3).
        orig_status = _patch_46a_p1_override_status(orig_trade) or orig_status
    elif operation == "Delete":
        # Rule 46b
        orig_status = trade.status
        forbid_msg = "FV46b: You are not allowed to delete voided trades."
    else:
        raise ValueError("Unhandled operation '{0}'.".format(operation))
    if orig_status == "Void":
        raise DataValidationError(forbid_msg)


# FIXME Remove once fixed Prime is deployed (>= 2015.3).
def _patch_46a_p1_override_status(trade):
    """FXFA-807 Patch 46a-p1 to allow voiding trade constellations.

    Return the status of the parent trade if the trade is a child in a
    trade constellation, the status of the trade is 'Void' and the parent's
    status is other than 'Void'.  Otherwise return False.

    This patch is a workaround to fix a bug in Prime 2014.4 introduced by
    SPR 365654.  SPR 373528 and AR 692551 were logged to fix this.  The fix
    was implemented into Prime 2015.3 (build 4.21.217.0).  Once we deploy
    Prime 2015.3 or newer this patch should be removed.

    Bug description:  When voiding an FX trade constellation, some child
    trades come to FValidation as already voided.  Therefore rule 46a
    complains and won't allow voiding the constellation.  This patch
    replaces the status of the affected child trades with the status of the
    parent trade.
    """
    trade = acm.FTrade[trade.trdnbr]
    if trade.Status() == "Void":
        parent = trade.GroupTrdnbr()
    else:
        return False
    if parent is None or parent is trade or parent.Status() == "Void":
        return False
    else:
        print("Info: Patch 46a-p1 applied to the status of trade {0}."
                .format(trade.Oid()))
        return parent.Status()

'''
@validate_entity("TextObject", "Update")
@validate_entity("TextObject", "Insert")
def fv123_forbid_using_calc_env(entity, operation):
    """Forbid using certain Calculation Environments.

    To protect server resources, forbid users from using the Calc Envs in
    Distributed sheets that have a name starting with "CE_".

    Users with a name starting with "APS_" are not restricted by this rule.
    """
    # Exclude APS_* users.
    if ael.user().userid.startswith("APS_"):
        return

    # Restrict access to relevant object types.
    relevant_types = ["Portfolio sheet",
                      "Risk Sheet",
                      "Vertical Portfolio Sheet"]
    if entity.type in relevant_types:
        acm_o = acm.Ael.AelToFObject(entity)
        if (acm_o.CalculationEnvironmentName() and
                acm_o.CalculationEnvironmentName().AsString().startswith('CE_')):
            msg = ("FV123: "
                   "You cannot save a sheet with Distributed Processing that "
                   "uses Calculation Environment: {0}. "
                   "Please check with RTB."
                   .format(acm_o.CalculationEnvironmentName()))
            raise DataValidationError(msg)
'''


@validate_entity("Party", "Insert", caller="validate_transaction")
@validate_entity("Party", "Update", caller="validate_transaction")
def fv125_validate_bic(entity, operation):
    """Validate Party Swift (BIC) code.

    Both the BIC field and Swift Alias are validated.
    """
    if check_party_bics(entity) == 0:
        msg = ("FV125: Either the BIC or Swift Alias is invalid. "
               "Please correct the value(s) or remove them completely.")
        raise DataValidationError(msg)


@validate_entity("Trade", "Insert")
@validate_entity("Trade", "Update")
def fv124_forbid_unsettled_premium(entity, operation):
    """Forbid terminating trades with an unsettled premium."""
    trade = entity
    today = ael.date_today()
    if (trade.status == "Terminated" and
            trade.value_day >= today and trade.premium != 0):
        msg = ("FV124: Trade '{0}' has an unsettled premium. "
               "You are not allowed to terminate or update terminated trades "
               "with an unsettled premium. "
               "Consider using additional payments."
               .format(trade.trdnbr))
        raise AccessValidationError(msg)


@validate_entity("Instrument", "Insert", caller="validate_transaction")
@validate_entity("Instrument", "Update", caller="validate_transaction")
def fv129_forbid_spec_chars_in_instrument_names(entity, operation):
    """FV129: Forbid special characters in instrument names."""
    FORBIDDEN_CHARS = [
            ("\\", "backslash"),
            (";", "semicolon"),
            (",", "comma"),
            ("|", "vertical bar"),
            ]
    insname = entity.insid
    for char, charname in FORBIDDEN_CHARS:
        if char in insname:
            msg = ("FV129: Instrument '{0}': Forbidden character in the name: "
                   "'{1}' ({2}). The name cannot contain any of the following "
                   "characters: {3}"
                   .format(insname, char, charname,
                           " ".join(c[0] for c in FORBIDDEN_CHARS)))
            raise DataValidationError(msg)


@validate_entity("Trade", "Update")
def fv130_restrict_amending_demat_trade(trade, operation):
    """Forbid amending confirmed and Void Demat trades."""
    if not is_demat(trade):
        return
    if trade.add_info("Demat_Acq_BPID") == trade.add_info("MM_DEMAT_CP_BPID"):
        return
    if is_allowed(ael.user(), 'Demat Restricted Access', 'Operation'):
        return
    original_trade = trade.original()
    original_status = original_trade.status
    if original_status not in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        return
    status = trade.status
    if status != "Void":
        #add_info amendments also need to be blocked
        if trade.prfnbr == original_trade.prfnbr:
            msg = ("FV130: Trade '{0}' is Demat Trade. "
                   "You are not allowed to amend a Demat trade"
                   .format(trade.trdnbr))
            raise AccessValidationError(msg)
    elif original_status == "BO-BO Confirmed":
        msg = ("FV130: Trade '{0}' is Demat Trade. "
               "You are not allowed to amend a Demat trade "
               "in 'BO-BO Confirmed'"
               .format(trade.trdnbr))
        raise AccessValidationError(msg)
                    

@validate_entity("Instrument", "Update", caller="validate_transaction")
def fv131_forbid_demat_instrument_update(entity, operation):
    """Restrict updating economic details for Demat instruments.

    Forbid updating the economic details for Demat instruments which have been
    inserted into the ISIN Manangement Business Process.
    """

    modified_ins = entity
    original_ins = modified_ins.original()

    if modified_ins.instype in ['CD', 'FRN'] \
        and (modified_ins.add_info("Demat_Instrument") == original_ins.add_info("Demat_Instrument") == "Yes"):

        orig_leg = original_ins.legs()[0]
        modified_leg = modified_ins.legs()[0]

        MMSS_ISIN_REQUEST_STATE_CHART_NAME = 'MM ISIN Management'
        state_chart = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]
        processes = acm.BusinessProcess.FindBySubjectAndStateChart(to_acm(original_ins, 'FInstrument'), state_chart)

        if len(processes) > 0 \
            and processes[0].CurrentStep().State().Name().find('Failed') == -1:

            if modified_ins.instype == 'CD':
                #Start or end date updated
                if (orig_leg.start_day != modified_leg.start_day) or (orig_leg.end_day != modified_leg.end_day):
                    raise AccessValidationError('Cannot modify Demat Instrument Start/End Day')
                #Rate updated
                if orig_leg.fixed_rate != modified_leg.fixed_rate:
                    raise AccessValidationError('Cannot modify rate')
                #rolling day check
                if orig_leg.rolling_base_day != modified_leg.rolling_base_day:
                    raise AccessValidationError('Cannot modify Demat Instrument Rolling Base Day')
                #rolling period rolling_period.count rolling_period
                if orig_leg.rolling_period != modified_leg.rolling_period:
                    raise AccessValidationError('Cannot modify Demat Instrument Rolling Period')
                #ISIN check
                if original_ins.isin != '' and original_ins.isin != modified_ins.isin:
                    raise AccessValidationError('Cannot modify Demat Instrument ISIN Number')
                #Issuer check
                if original_ins.issuer != modified_ins.issuer:
                    raise AccessValidationError('Cannot modify Demat Instrument Issuer')
                #Currency Check
                if original_ins.curr.insaddr != modified_ins.curr.insaddr:
                    raise AccessValidationError('Cannot modify Demat Instrument Currency')
                #Day count check
                if original_ins.daycount_method != modified_ins.daycount_method:
                    raise AccessValidationError('Cannot modify Demat Instrument Daycount Method')
                #DEMAT fields check
                if (original_ins.add_info('Demat_Ins_SOR_Acc') != modified_ins.add_info('Demat_Ins_SOR_Acc')) \
                    or (original_ins.add_info('Demat_Issuer_BPID') != modified_ins.add_info('Demat_Issuer_BPID')) \
                    or (original_ins.add_info('Demat_MinTrdDeno') != modified_ins.add_info('Demat_MinTrdDeno')) \
                    or (original_ins.add_info('Demat_WthhldTax') != modified_ins.add_info('Demat_WthhldTax')) \
                    or (original_ins.add_info('Demat_WthhldTx_Rate') != modified_ins.add_info('Demat_WthhldTx_Rate')) \
                    or (original_ins.add_info('MM_MMInstype') != modified_ins.add_info('MM_MMInstype')):

                    raise AccessValidationError('Cannot modify Instrument Demat specific Additional Infos')

            if modified_ins.instype == 'FRN':
                #Start or end date updated
                if (orig_leg.start_day != modified_leg.start_day) or (orig_leg.end_day != modified_leg.end_day):
                    raise AccessValidationError('Cannot modify Demat Instrument Start/End Day')
                #Float ref
                if orig_leg.float_rate.insaddr != modified_leg.float_rate.insaddr:
                    raise AccessValidationError('Cannot modify Demat Instrument Float Rate Reference')
                #Spread
                if orig_leg.spread != modified_leg.spread:
                    raise AccessValidationError('Cannot modify Demat Instrument Spread')
                #rolling day
                if orig_leg.rolling_base_day != modified_leg.rolling_base_day:
                    raise AccessValidationError('Cannot modify Demat Instrument Rolling Base Day')
                #rolling period rolling_period.count rolling_period.unit
                if orig_leg.rolling_period != modified_leg.rolling_period:
                    raise AccessValidationError('Cannot modify Demat Instrument Rolling Period')
                #ISIN check
                if original_ins.isin != '' and original_ins.isin != modified_ins.isin:
                    raise AccessValidationError('Cannot modify Demat Instrument ISIN Number')
                #Issuer
                if original_ins.issuer != modified_ins.issuer:
                    raise AccessValidationError('Cannot modify Demat Instrument Issuer')
                #Currency
                if original_ins.curr.insaddr != modified_ins.curr.insaddr:
                    raise AccessValidationError('Cannot modify Demat Instrument Currency')
                #Day count
                if original_ins.daycount_method != modified_ins.daycount_method:
                    raise AccessValidationError('Cannot modify Demat Instrument Daycount Method')
                #and all the fields on the DEMAT Tab
                #DEMAT fields check
                if (original_ins.add_info('Demat_Ins_SOR_Acc') != modified_ins.add_info('Demat_Ins_SOR_Acc')) \
                    or (original_ins.add_info('Demat_Issuer_BPID') != modified_ins.add_info('Demat_Issuer_BPID')) \
                    or (original_ins.add_info('Demat_MinTrdDeno') != modified_ins.add_info('Demat_MinTrdDeno')) \
                    or (original_ins.add_info('Demat_WthhldTax') != modified_ins.add_info('Demat_WthhldTax')) \
                    or (original_ins.add_info('Demat_WthhldTx_Rate') != modified_ins.add_info('Demat_WthhldTx_Rate')) \
                    or (original_ins.add_info('MM_MMInstype') != modified_ins.add_info('MM_MMInstype')):

                    raise AccessValidationError('Cannot modify Instrument Demat specific Additional Infos')


@validate_entity("Party", "Insert", caller="validate_transaction")
@validate_entity("Party", "Update", caller="validate_transaction")
def fv135_party_client_static_validation_rules(entity, operation):

    #dev by Kunal & Sihle for Client Static data quality project
    party = entity
        
    user = acm.User()
    if user.UserGroup().Oid() == 544:      #This is so the Validation only applies to the group "OPS Client Services" - which is client static
        if party.fullname == '':
            msg = ("No Full Name specified")
            raise DataValidationError(msg)
                
        if party.attention == '':
            msg = ("No Attention specified")
            raise DataValidationError(msg)
                    
        if party.address == '':
            msg = ("No Address specified")
            raise DataValidationError(msg)
        
        if party.zipcode == '':
            msg = ("No Zipcode specified")
            raise DataValidationError(msg)
            
        if party.city == '':
            msg = ("No City specified")
            raise DataValidationError(msg)

        if party.country == '':
            msg = ("No Country specified")
            raise DataValidationError(msg)

        if party.contact1 == '':
            msg = ("No Contact1 specified")
            raise DataValidationError(msg)

        if party.telephone == '':
            msg = ("No Telephone specified")
            raise DataValidationError(msg)


        # The below is to force values to become capitilized upon a save
        party.fullname = party.fullname.upper()
        #party.ptyid =  party.ptyid.upper()
        party.attention = party.attention.upper()
        party.address = party.address.upper()
        party.address2 = party.address2.upper()
        party.zipcode = party.zipcode.upper()
        party.city = party.city.upper()
        party.country = party.country.upper()
        party.jurisdiction_country_code = party.jurisdiction_country_code.upper()
        party.contact1 = party.contact1.upper()
        party.telephone = party.telephone.upper()
        party.email = party.email.upper()
        
        #Requirements that are tied to the correspondent bank
        if party.correspondent_bank == 1:
            party.time_zone = "Africa/Johannesburg"
            party.external_cutoff = 1600
            party.internal_cutoff = 0017
            if party.swift == '':
                msg = ("No BIC Specified")
                raise DataValidationError(msg)

        import FBDPCommon
        acm_party = FBDPCommon.ael_to_acm(party)
        
        if acm_party.AdditionalInfo().FICA_Compliant() == None:
            msg = ("No FICA Compliance Specified on Add Info")
            raise DataValidationError(msg)
        
        if party.hostid != '':
            if acm_party.AdditionalInfo().UnexCor_Code() in ('', None): 
                msg = ("UnexCor Code Not Specified on Add Info")
                raise DataValidationError(msg)
        
        #validation check of party accounts
        party_accounts = acm_party.Accounts()

        for party_account in party_accounts:

            if party_account.NetworkAliasType() == None:
                msg = ("No Network Selected for Account: ", party_account)
                raise DataValidationError(msg)

            if party_account.NetworkAliasType() != None and party_account.CorrespondentBank() == None:
                msg = ("No Correspondent bank Defined for Account: ", party_account)
                raise DataValidationError(msg)

            if party_account.NetworkAliasType() != None and party_account.Account() == '':
                msg = ("No Account Number defined for: ", party_account)
                raise DataValidationError(msg)

            #This part of the rule applies only for FICC accounts. When correspondent BIC is DTCYUS33 and intermediary 2's BIC is FRNYUS33 then DetailsOfCharges field
            #should be set to OUR. This makes sure that duplicate account names are not created.
            if party_account.NetworkAliasType().Name() == "SWIFT" and party_account.AccountType() == "Cash and Security":
                if party_account.Bic() and party_account.Bic3() and \
                        party_account.Bic().Name() == "DTCYUS33" and party_account.Bic3().Name() == "FRNYUS33":
                    if party_account.DetailsOfCharges() <> "OUR":
                        msg = ("When correspondent bank BIC is DTCYUS33 and intermediary 2 BIC is FRNYUS33 then set Details of Charges 'OUR': ", party_account)
                        raise DataValidationError(msg)
            
 
@validate_entity("Trade", "Insert")
@validate_entity("Trade", "Update")
def fv136_dis_trade_nominal_check(trade, operation):
    """Restrict updating nominal of DIS trade if ,
         1. The trade nominal is less than Available Amount if it is a sell trade .
         2. The trade nominal is more than trade nominal + Avaliable amount is more than authorised amount
    """
    if not is_dis(trade):
        return
    if is_allowed(ael.user(), 'DIS Restricted Access', 'Operation'):
        return
    if trade.status not in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        return
    # Not sure why this check is necessary but retaining original functionality to be safe.
    original_trade = trade.original()
    original_status = None
    if original_trade is not None:
        original_status = original_trade.status
    if original_status not in [None, 'Simulated', 'FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        return
    acm_trade = to_acm(trade)
    # Validate instrument availability.
    available_amount = current_ins_available_amount(acm_trade.Instrument(), acm_trade.Oid())
    if acm_trade.Quantity() < 0:
        # Sell trade.
        trade_nominal = acm_trade.Nominal() * -1
        if trade_nominal > available_amount:
            raise ValidationError('Trade nominal greater than instrument value available.')
    elif acm_trade.Quantity() > 0:
        # Buy trade.
        authorised_amount = current_ins_authorised_amount(acm_trade.Instrument())
        if acm_trade.Nominal() + available_amount > authorised_amount:
            raise ValidationError('Instrument not available in the market, please book sell trades first.')
    # Validate trade denomination.
    abs_nominal_in_cents = int(fabs(acm_trade.Nominal()) * 100)
    min_denomination_in_cents = int(acm_trade.Instrument().AdditionalInfo().Demat_MinTrdDeno() * 100)
    if abs_nominal_in_cents % min_denomination_in_cents != 0:
        raise ValidationError('Trade nominal is not a trade-able denomination.')


@validate_entity("PortfolioLink", "Insert")
def fv137_duplicate_portfolio_link(entity, operation):
    pf_links = to_acm(entity).MemberPortfolio().MemberLinks()
    delete_confirmed = False
    if len(pf_links) > 0:
        if str(acm.Class()) == "FTmServer":
            shell = acm.UX().SessionManager().Shell()
            msg = "More than 1 link exists - delete previous links?"
            answer = acm.UXDialogs().MessageBoxYesNo(shell, "Question", msg)
            if answer == "Button1":
                delete_confirmed = True
        if delete_confirmed:
            for i in pf_links:
                i.Delete()
        else:
            msg = "Already existing links:"
            for i in pf_links:
                msg += i.OwnerPortfolio().Name()
            raise ValidationError(msg)


@validate_entity("Trade", "Insert")
@validate_entity("Trade", "Update")
def fv139_prevent_booking_certain_backdated_trades(entity, operation):
    #Applies to trades with acquirer = PRIME SERVICES DESK
    #  new trades: backdating forbidden into previous month
    #  update trades:
    #    - trade from previous month - from Simulated to FO Confirmed/BO Confirmed/... forbidden
    #    - amendments allowed, but only after confirming the popup
    INCLUDE_GROUP_OIDS = [667,  # 667 = "FO PSExchExe Trader (Eveshnee Naidoo)"
                          666]  # 666 = "FO Eq ACS Trader (Raymond Phillips)"
    if str(acm.Class()) == "FTmServer":
        if acm.User().UserGroup().Oid() in INCLUDE_GROUP_OIDS:
            shell = acm.UX().SessionManager().Shell()
            trade = to_acm(entity)
            ins_type = trade.Instrument().InsType()
            if ins_type not in ['Swap', 'FRA']:
                if trade.Acquirer():
                    acquirer = trade.Acquirer().Name()
                    if acquirer == "PRIME SERVICES DESK":
                        msg = ""
                        time_trade = acm.Time.DateFromTime(trade.TradeTime())
                        if (
                             time_trade < TIME_NOW and
                             datetime_from_string(time_trade).month != datetime_from_string(TIME_NOW).month and
                             ( operation == "Insert" or
                               ( operation == "Update" and
                                 trade.Original() is not None and
                                 trade.Original().Status() == "Simulated" and
                                 trade.Status() not in ["Simulated", "Void"] )
                             )
                        ):
                            msg = "FV139 - Booking of backdated %s trade\n" % ins_type
                            msg += "into previous month not allowed!"
                            acm.UX().Dialogs().MessageBoxInformation(shell, msg)
                            raise ValidationError('Could not book trade')
                        elif ( 
                             ( time_trade < TIME_THREE_BDAYS_AGO and 
                               datetime_from_string(time_trade).month == datetime_from_string(TIME_NOW).month )
                             or
                             ( time_trade < TIME_NOW and
                               datetime_from_string(time_trade).month != datetime_from_string(TIME_NOW).month and
                               operation == "Update" )
                        ):
                            msg = "FV139 - Are you sure you want to book/update a backdated trade?"
                            answer = acm.UX().Dialogs().MessageBoxYesNo(shell, "Question", msg)
                            if answer != "Button1":
                                raise ValidationError('FV139 - Could not book trade')


@validate_entity("Trade", "Update", caller="validate_transaction")
def fv140_prevent_changes_to_simulated_confirmation_owner_trades(entity, operation):
    """
    Prevent changes to simulated trades created to own multi-trade 
    confirmations (e.g. term statements, loan notices, etc.).
    
    Such trades are identified by having the trader ATS_CONFO.  Only 
    the ATS_CONFO user is permitted to update these trades.
    """
    if entity.original().status != 'Simulated':
        return
    trader = entity.original().trader_usrnbr
    if trader is None or trader.userid != 'ATS_CONFO':
        return
    if entity.updat_usrnbr.userid != 'ATS_CONFO':                               
        error_message = "FV140: Trade {trdnbr} is a multi-trade confirmation "
        error_message += "owner and may not be updated."
        raise AccessValidationError(error_message.format(trdnbr=entity.trdnbr))


# FIXME - Temporarily disabled until further business testing can be conducted.
# @validate_entity("BusinessProcess", "Insert", caller="validate_transaction")
# @validate_entity("BusinessProcess", "Update", caller="validate_transaction")
# @validate_entity("BusinessProcess", "Delete", caller="validate_transaction")
def fv142_restrict_business_process_access_by_state_chart(entity, operation):
    """
    Restrict access to business processes by state chart.
    """
    required_operation_by_state_chart_name = {
        'Alloc_Matching_wf_v1_02': 'Deprecated BP',
        'AmendOrCancelDirectDeal': 'Markitwire BP',
        'Broker Note Bulk': 'Broker Note Bulk BP',
        'deprecated_T2_CB': 'Deprecated BP',
        'deprecated_T2_Client': 'Deprecated BP',
        'deprecated_T2_EB': 'Deprecated BP',
        'DirectDeal': 'Markitwire BP',
        'DirectDealNovationRemaining': 'Markitwire BP',
        'DirectDealNovationStepOut': 'Markitwire BP',
        'DIS ISIN Management': 'ISIN Management BP',
        'GenericMandates_MandateStates': 'Generic Mandates BP',
        'GenericMandates_ViolationStates': 'Generic Mandates BP',
        'GenericMandatesAuthorization_v3': 'Generic Mandates BP',
        'LCH_Clearnet_T2_CB': 'Markitwire BP',
        'LCH_Clearnet_T2_Client': 'Markitwire BP',
        'LCH_Clearnet_T2_EB': 'Markitwire BP',
        'Limits': 'Deprecated BP',
        'MM ISIN Management': 'ISIN Management BP',
        'Pre-settlement Advice': 'Pre-settlement Advice BP',
        'SARB Sec Transfer Instruction': 'SARB Sec Transfer Instruction BP',
        'Statements': 'Valuation Statement BP',
        'T3 Allocations': 'Deprecated BP'
    }
    state_chart_name = entity.state_chart_seqnbr.name
    required_operation = required_operation_by_state_chart_name.get(state_chart_name)
    if required_operation is None:
        error_message = "FV142: No required operation defined for "
        error_message += "'{state_chart_name}' business processes."
        raise AccessValidationError(error_message.format(state_chart_name=state_chart_name))
    if not is_allowed(ael.user(), required_operation, 'Operation'):
        error_message = "FV142: You do not have write access to "
        error_message += "'{state_chart_name}' business processes."
        raise AccessValidationError(error_message.format(state_chart_name=state_chart_name))


@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def fv143_align_pledged_amount_with_ceded_amount_add_info(entity, operation):
    """
    Align pledged amount with ceded amount add info
    """
    trade = to_acm(entity)
    instrument = trade.Instrument()
    if instrument.InsType() == 'Deposit' and instrument.IsCallAccount():
        is_pladged_amount = instrument.Incomplete()
        pladged_amount = instrument.FaceValue()
        ceded_amount = trade.AdditionalInfo().MM_Ceded_Amount()

        if pladged_amount > 0 and is_pladged_amount == 'Pledged' and pladged_amount != ceded_amount:
            trade.AdditionalInfo().MM_Ceded_Amount(pladged_amount)
            if not trade.AdditionalInfo().MM_Account_Ceded():
                trade.AdditionalInfo().MM_Account_Ceded('Yes')


@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def fv145_restrict_trades_on_non_trading_non_compliant_counterparty(trade, operation):
    """
    Restrict booking trades with and/or adding payments on a non trading / non fica compliant Counterparty.
    """

    exclude_status_list = ["Simulated", "Void", "Terminated"]
    acm_trade = to_acm(trade)
    if acm_trade.Status() in exclude_status_list:
        return

    counterparty = acm_trade.Counterparty()
    all_counterparties = [counterparty]
    borrower = acm_trade.AdditionalInfo().SL_G1Counterparty1()
    if borrower and isinstance(borrower, str):
        borrower = acm.FParty[borrower]
    if borrower is not None:
        all_counterparties.append(borrower)

    lender = acm_trade.AdditionalInfo().SL_G1Counterparty2()
    if lender and isinstance(lender, str):
        lender = acm.FParty[lender]
    if lender is not None:
        all_counterparties.append(lender)

    for _counterparty in all_counterparties:
        validation_results = validate_trading_counterparty(_counterparty, acm_trade)
        if validation_results['status'] is False:
            raise ValidationError(validation_results['message'])

    for payment in acm_trade.Payments():
        if operation in ["Update", "Insert"] and payment.IsInfant() is False:
            continue
        validation_results = validate_payment_trading_party(payment, acm_trade)
        if validation_results['status'] is False:
            raise ValidationError(validation_results['message'])
