"""FValidation - Main module.

Before changing the code, please consult the Developer's Guide available at
<https://confluence-agl.absa.co.za/display/ABCAPFA/FValidation+Developer%27s+Guide>.

The list of implemented FValidation rules is kept at
<https://confluence-agl.absa.co.za/display/ABCAPFA/FValidation+rules>.
Please keep it in sync with the code.


This is the main FValidation module that defines three Front Arena hook
functions: validate_transaction, four_eyes_needed, and validate_entity.  Front
Arena will pass data to these functions before the data are written to the
underlying database.

You should not normally need to edit this module.  FValidation rules are
defined in other modules (e.g. FValidation_General).  This main module
implements functionality that loads those rules and then calls them at the
right time.


Emergency recovery
==================

It may happen that there is a bug, say a syntax error, in an FValidation
module; and that bug prevents you from saving the module itself, i.e. fixing
it.  In that case, follow these steps:

    (1) Set constant ENABLE_VALIDATION to False (module FValidation_settings)
        and reload module FValidation_settings.
    (2) Reload the main module FValidation.
    (3) Fix the broken module, save it and reload it.
    (4) Set ENABLE_VALIDATION back to True and reload module
        FValidation_settings.
    (5) Reload the main module FValidation.


History
=======

2014-08-31 Vojtech Sidorin      CHNG0002210109 Initial implementation.
2014-10-21 Andrei Conicov       CHNG0002365110 Have removed the FValidation_Trade_Amend module.
2014-11-20 Vojtech Sidorin      CHNG0002443195 Add module FValidation_FixedIncome.
2014-11-12 Nada Jasikova        CHNG0002443195 Added FValidation_enrich_SecLending.
2015-06-09 Vojtech Sidorin      ABITFA-3501 Replace FValidation_depr_YC_Vol_Access with FValidation_YC_Vol_Access.
2015-09-17 Willie van der Bank  Adaptiv: Added FValidation_Adaptiv_Conf_Stlm.
2015-11-06 Vojtech Sidorin      ABITFA-3910 Add module FValidation_DatesAndTimes.
2016-03-16 Vojtech Sidorin      ABITFA-4064: Add module FValidation_Volcker.
2016-05-09 Vojtech Sidorin      ABITFA-3286: Move constants to module FValidation_settings.
2016-06-22 Vojtech Sidroin      DEMAT: Merge module FValidation_Adaptiv_Conf_Stlm to FValidation_SettleConf.
2017-01-06 Vojtech Sidorin      ABITFA-3288: Move helper functions to the FValidation_core module.
2018-07-05 Cuen Edwards         FAOPS-127: Changed bypass validation of simulated trades to exclude confirmation owner trades.
2019-10-15 Stuart Wilson        FAOPS-607: Added ability to force super user to validate against particular validations.
"""

import sys
import ael

# NOTE: For security reasons, the imports are done as "from module import
# something" to create local copies of the objects.  This means any change in
# an external module will be reflected in FValidation only after the main
# FValidation module is reloaded.  Since the FValidation module is a "safe"
# module, "...any local changes (reloads) will only be used by the system if
# the user has write access to the module".  See FCA3724 (AEF Basic Extensions)
# for more information about safe modules.
from FValidation_settings import (
        ENABLE_VALIDATION,
        SUPERUSERS,
        ENRICHMENT_MODULES,
        VALIDATION_MODULES,
        SUPERUSER_VALIDATIONS
        )
from FValidation_core import (
        load_rules,
        debug_msg,
        handle_current_exception,
        )

# Old FValidation (deprecated module) with not-yet-refactored rules.
import FValidation_depr

# Information about the last FValidation exception that occured after
# (re)loading this module: a tuple with values (type, value, traceback).
# This global variable can be used by external code to retrieve the info.
# See also the docstring of the handle_current_exception function.
last_exc_info = sys.exc_info()


# Load validation rules when (re)loading the module.
try:
    modules = ENRICHMENT_MODULES + VALIDATION_MODULES
    rules = load_rules(modules)
except:
    last_exc_info = handle_current_exception()
    raise
else:
    debug_msg("Registered {0} transaction validation rule(s) and {1} entity "
              "validation rule(s)."
              .format(len(rules["transaction"]), len(rules["entity"])))


def validate_transaction(transaction_list):
    """Front Arena hook function."""
    global last_exc_info
    try:
        return _validate_transaction(transaction_list)
    except:
        last_exc_info = handle_current_exception()
        raise


def four_eyes_needed(transaction_list):
    """Front Arena hook function."""
    # Return:
    #     0 = Disable four-eyes checks for the transaction.
    #     1 = Perform standard four-eyes checks for the transaction.
    return 1


def validate_entity(entity, operation):
    """Front Arena hook function."""
    global last_exc_info
    try:
        return _validate_entity(entity, operation)
    except:
        last_exc_info = handle_current_exception()
        raise


def _validate_transaction(transaction_list):
    """
    Implementation of FValidation.validate_transaction hook.
    """
    if _should_bypass_all_validation():
        # Bypass transaction validation all together.
        return transaction_list
    # Apply deprecated FValidation validate_transaction.
    transaction_list = _apply_deprecated_validate_transaction(transaction_list)
    # Hook (1):  Validate the entire transaction.
    transaction_list = _apply_transaction_validation_rules(transaction_list)
    # Hook (2):  Validate individual entities within the transaction.
    for entity, operation in transaction_list:
        # Bypass validation of simulated trades unless they are
        # confirmation owner trades.
        if (_is_simulated_trade(entity) and
                not _is_modification_of_confirmation_owner_trade(entity, operation)):
            continue
        for entity_rule in _get_entity_validation_rules(entity, operation, "validate_transaction"):
            _apply_entity_validation_rule(entity_rule, entity, operation)
    return transaction_list


def _validate_entity(entity, operation):
    """
    Implementation of FValidation.validate_entity hook.
    """
    if _should_bypass_all_validation():
        # Bypass entity validation all together.
        return
    if _is_simulated_trade(entity):
        # Bypass entity validation all together.
        return
    # Apply deprecated FValidation validate_entity.
    _apply_deprecated_validate_entity(entity, operation)
    # Hook (3):  Validate entities in validate_entity.
    for entity_rule in _get_entity_validation_rules(entity, operation, "validate_entity"):
        _apply_entity_validation_rule(entity_rule, entity, operation)


def _should_bypass_all_validation():
    """
    Determine whether or not to bypass all FValidation.

    This function will return True if validation is disabled in
    FValidation_settings or if the current user is defined as a
    super user in FValidation_settings and has no enforced super
    user validations.
    """
    # Check if validation is disabled.
    if not ENABLE_VALIDATION:
        debug_msg("FValidation has been disabled in FValidation_settings")
        return True
    # Check if current user is a superuser without any superuser validations.
    userid = ael.user().userid
    _super_user_validation_debug_message(userid)
    if userid in SUPERUSERS and userid not in list(SUPERUSER_VALIDATIONS.keys()):
        debug_msg("Super User: {userid} is bypassing all FValidations".format(userid=userid))
        return True
    # Otherwise validation should not be bypassed.
    return False


def _apply_deprecated_validate_transaction(transaction_list):
    """
    Applies deprecated legacy transaction validations defined in
    FValidation_depr.

    Please note that super user validations are not supported for
    deprecated validations.
    """
    if ael.user().userid in SUPERUSERS:
        return transaction_list
    debug_msg("validate_transaction: Validating transaction by "
              "FValidation_depr.validate_transaction.")
    return FValidation_depr.validate_transaction(transaction_list)


def _apply_deprecated_validate_entity(entity, operation):
    """
    Applies deprecated legacy entity validations defined in
    FValidation_depr.

    Please note that super user validations are not supported for
    deprecated validations.
    """
    if ael.user().userid in SUPERUSERS:
        return
    debug_msg("validate_entity: Validating {entity_type}@{operation} by "
              "FValidation_depr.validate_entity."
              .format(entity_type=entity.record_type, operation=operation))
    FValidation_depr.validate_entity(entity, operation)


def _apply_transaction_validation_rules(transaction_list):
    """
    Applies transaction validation rules.
    """
    for transaction_rule in _get_transaction_validation_rules():
        debug_msg("validate_transaction: Validating transaction by "
                  "{module}.{function}."
                  .format(module=transaction_rule.__module__,
                          function=transaction_rule.__name__))
        transaction_list = transaction_rule(transaction_list)
    return transaction_list


def _apply_entity_validation_rule(entity_rule, entity, operation):
    """
    Applies the specified entity validation rule.
    """
    debug_msg("validate_entity: Validating {entity_type}@{operation} by "
              "{module}.{function}."
              .format(entity_type=entity.record_type,
                      operation=operation,
                      module=entity_rule.__module__,
                      function=entity_rule.__name__))
    entity_rule(entity, operation)


def _get_transaction_validation_rules():
    """
    Gets all transaction validation rules to be enforced for the
    current user.
    """
    transaction_rules = []
    userid = ael.user().userid
    for transaction_rule in rules["transaction"]:
        if userid in SUPERUSERS and transaction_rule.__name__ not in SUPERUSER_VALIDATIONS[userid]:
            continue
        transaction_rules.append(transaction_rule)
    return transaction_rules


def _get_entity_validation_rules(entity, operation, caller):
    """
    Gets all entity validation rules to be enforced for the
    current user.
    """
    entity_rules = []
    userid = ael.user().userid
    for entity_rule, entity_type, rule_operation, rule_caller in rules["entity"]:
        if userid in SUPERUSERS and entity_rule.__name__ not in SUPERUSER_VALIDATIONS[userid]:
            continue
        if entity_type != entity.record_type:
            continue
        if rule_operation != operation:
            continue
        if rule_caller != caller:
            continue
        entity_rules.append(entity_rule)
    return entity_rules


def _is_simulated_trade(entity):
    """
    Determine whether or not an entity is a simulated trade.
    """
    return entity.record_type == "Trade" and entity.status == "Simulated"


def _is_modification_of_confirmation_owner_trade(entity, operation):
    """
    Determine whether or not an operation being performed is the
    modification of a confirmation owner trade.

    Confirmation owner trades are created to own confirmations that are
    related to multiple trades (e.g. term statements, loan notices, etc.).

    Such trades are identified by being in simulated status and having
    the trader ATS_CONFO.
    """
    if entity.record_type != 'Trade':
        return False
    if operation != 'Update':
        return False
    if entity.original().status != 'Simulated':
        return False
    trader = entity.original().trader_usrnbr
    if trader is None or trader.userid != 'ATS_CONFO':
        return False
    return True


def _super_user_validation_debug_message(userid):
    """debug message for super user validation only to be called when
    debug mode is enabled"""

    if userid in list(SUPERUSER_VALIDATIONS.keys()):
        functions = SUPERUSER_VALIDATIONS[userid]
        debug_message = "Super User: {userid} will validate against: {functions}".format(
                                        userid=userid,
                                        functions=functions)
        debug_msg(debug_message)

