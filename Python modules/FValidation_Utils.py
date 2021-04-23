"""Utilities for FValidation.

This module contains utilities that can be used by the FValidation
modules.  Only utilities should be put into this module, no decorated
functions that represent individual rules.

History
=======
2015-02-04 Vojtech Sidorin   Initial implementation.
2015-02-11 Dmitry Kovalenko  Add function check_if_portofolio_has_flat_risk.
2015-02-24 Vojtech Sidorin   ABITFA-3415 Remove function check_if_portofolio_has_flat_risk until the performance issue is solved
2015-06-05 Vojtech Sidorin   ABITFA-3501 Add function get_user_groups.
2019-04-18 Cuen Edwards      FAOPS-425: Add function get_updated_columns.
"""

import acm

from at_type_helpers import to_acm


class NoRecordFoundError(Exception):
    """Raised when an expected record is not found in the database."""


def has_trades_of_statuses(instrument, statuses):
    """Indicate if instrument has any trades with given statuses.

    Return True if the instrument has at least one trade with a status
    given in statuses, False otherwise.

    Arguments:
    instrument -- (acm.FInstrument | ael_entity) the instrument
    statuses -- (iterable) (str) trade statuses

    Example call:
    has_trades_of_statuses(instrument, ['Simulated', 'FO Confirmed'])
    """
    acm_instrument = to_acm(instrument)
    for trade in acm_instrument.Trades():
        if trade.Status() in statuses:
            return True
    else:
        return False


def has_all_trades_of_statuses(instrument, statuses):
    """Indicate if instrument has all trades with given statuses.

    Return True if the trades on the instrument are all in given statuses.
    Return False if at least one trade is in a status other than the given
    statuses.

    Arguments:
    instrument -- (acm.FInstrument | ael_entity) the instrument
    statuses -- (iterable) (str) trade statuses

    Example call:
    has_all_trades_of_statuses(instrument, ['BO Confirmed', 'Void'])
    """
    acm_instrument = to_acm(instrument)
    for trade in acm_instrument.Trades():
        if trade.Status() not in statuses:
            return False
    else:
        return True


def get_user_groups(user):
    """Return set of user's groups.

    Return a set of all user groups the user is a member of.  It includes
    both the user's main group and friend groups.

    Arguments:
    user -- (acm.Fuser | ael_entity) the user
    """
    acm_user = to_acm(user)
    groups = set()
    # NOTE: The main user group can be None.
    if acm_user.UserGroup():
        groups.add(acm_user.UserGroup())    # Main user group.
    groups.update(acm_user.FriendGroups())  # Friend groups.
    return groups


def get_user_profiles(user):
    """Return set of profiles mapped to user.

    Return a set of user profiles (acm.FUserProfile) that are mapped to a
    given user.

    Arguments:
    user -- (acm.FUser | ael_entity) the user
    """

    acm_user = to_acm(user)

    groups = get_user_groups(acm_user)

    # Get all profile links.
    upls = set(acm_user.Links())  # User-profile links.
    gpls = set()                  # Group-profile links.
    for group in groups:
        links = acm.FGroupProfileLink.Select("userGroup={0}".format(group.Oid()))
        gpls.update(links)
    # Merge all profile links.
    pls = set.union(upls, gpls)

    # Extract profiles.
    profiles = {pl.UserProfile() for pl in pls}

    return profiles


def user_has_profile(user, profname):
    """Return True if user has given profile, False otherwise.

    Arguments:
    user -- (acm.FUser | ael_entity) the user
    profname -- (str) name of the profile

    Raise an exception if the profile doesn't exist.

    Example call:
    if user_has_profile(acm.User(), "FO Call Trader"):
        pass  # The user has mapped profile "FO Call Trader"
    """
    acm_user = to_acm(user)
    profile = acm.FUserProfile.Select01("name='{0}'".format(profname), None)
    if profile is None:
        msg = "Profile '{0}' doesn't exist.".format(profname)
        raise NoRecordFoundError(msg)
    return profile in get_user_profiles(acm_user)


def is_allowed(user, compname, comptype="Operation"):
    """Return True if user has given component, False otherwise.

    This function corrects the behaviour of the built-in method
    acm.FUser.IsAllowed().  The built-in IsAllowed() returns True when
    asked for a component that doesn't exist, which is dangerous behaviour.

    Arguments:
    user -- (acm.Fuser | ael_entity) the user
    compname -- (str) name of the component, e.g. "FO Confirm"
    comptype -- (str) type of the component, e.g. "Operation"

    Raise an exception if the component doesn't exist.

    Example call:
    if is_allowed(acm.User(), "FO Confirm"):
        pass  # The user can FO Confirm.
    """

    acm_user = to_acm(user)

    # Check if the component exists.
    component = acm.FComponent.Select01(
            "name='{0}' and type='{1}'".format(compname, comptype), None)
    if component is None:
        msg = ("Component '{0}' of type '{1}' doesn't exist."
               .format(compname, comptype))
        raise NoRecordFoundError(msg)

    # Delegate to built-in IsAllowed.
    return acm_user.IsAllowed(compname, comptype)


def get_updated_columns(updated_entity):
    """Return set of updated columns.

    Return a set of columns updated on an entity.  This function may only
    be called during FValidation for an 'Update' operation.

    Arguments:
    updated_entity -- (ael_entity) the updated entity
    """
    updated_columns = set()
    original_entity = updated_entity.original()
    for column in updated_entity.columns():
        original_value = getattr(original_entity, column)
        updated_value = getattr(updated_entity, column)
        if original_value != updated_value:
            updated_columns.add(column)
    return updated_columns


def is_block_trade(acm_trade):
    if acm_trade.OptKey1() and acm_trade.OptKey1().Name() == "Block Trade":
        return True
    return False


def is_all_party_no(acm_party):
    if acm_party.NotTrading() is False and acm_party.AdditionalInfo().RegulatedAstMngBulk() in [False, None]:
        if acm_party.AdditionalInfo().FICA_Compliant() in ["No", None]:
            return True
    return False


def is_reg_asset_management_bulk(acm_party):
    if acm_party.NotTrading() is False and acm_party.AdditionalInfo().RegulatedAstMngBulk():
        if acm_party.AdditionalInfo().FICA_Compliant() in ["No", None]:
            return True
    return False


def validate_payment_trading_party(payment, acm_trade):
    validation_results = {'status': False}
    party = payment.Party()

    if party and party.NotTrading():
        message = ("FV145: Additional Payment Booking cannot be completed. The party {party_type} "
                   "'{client_name}' marked as  Not Trading. 1p")
        validation_results['message'] = message.format(party_type="Trade Counterparty", client_name=party.Name())
        return validation_results

    if party and is_block_trade(acm_trade) and is_all_party_no(party):
        message = ("FV145: Additional Payment Booking cannot be completed. The party {party_type} "
                   "'{client_name}' is either Non FICA Compliant or RegulatedAstMngBulk is No. 3p")
        validation_results['message'] = message.format(party_type="Trade Counterparty", client_name=party.Name())
        return validation_results

    if party and is_reg_asset_management_bulk(party) and is_block_trade(acm_trade) in [False, True]:
        message = ("FV145: Additional Payment Booking cannot be completed. The party {party_type} "
                   "'{client_name}' is Non FICA Compliant. 4p, 5p")
        validation_results['message'] = message.format(party_type="Trade Counterparty", client_name=party.Name())
        return validation_results

    validation_results['status'] = True
    validation_results['message'] = "Is Valid Payment"
    return validation_results


def validate_trading_counterparty(counterparty, acm_trade):
    validation_results = {'status': False}

    if counterparty is None:
        validation_results['message'] = "Is Invalid Counterparty"
        return validation_results

    message = ("FV145: Trade Booking cannot be completed. The {party_type} '{client_name}' is either Not Trading or "
               "Non FICA Compliant or Not Regulated Asset Mng Bulk trades. 1")
    if counterparty and counterparty.NotTrading():
        validation_results['message'] = message.format(party_type="Trade Counterparty", client_name=counterparty.Name())
        return validation_results

    message = ("FV145: Trade Booking cannot be completed. The {party_type} '{client_name}' is either Not Trading or "
               "Non FICA Compliant or Not Regulated Asset Mng Bulk trades. 2, 3")
    if counterparty and is_block_trade(acm_trade) in [False, True] and is_all_party_no(counterparty):
        validation_results['message'] = message.format(party_type="Trade Counterparty", client_name=counterparty.Name())
        return validation_results

    message = ("FV145: Additional Payment Booking cannot be completed. The party {party_type} "
               "'{client_name}' is Non FICA Compliant. 4")
    if counterparty and is_reg_asset_management_bulk(counterparty) and is_block_trade(acm_trade) is False:
        validation_results['message'] = message.format(party_type="Trade Counterparty", client_name=counterparty.Name())
        return validation_results

    validation_results['status'] = True
    validation_results['message'] = "Is Valid Counterparty"
    return validation_results
