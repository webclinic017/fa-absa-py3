"""Core components of FValidation.

History
=======

2014-08-31 Vojtech Sidorin   CHNG0002210109 Initial implementation
2014-09-30 Dmitry Kovalenko  CHNG0002328679 Added exception classes
2015-03-18 Vojtech Sidorin   ABITFA-4064: Add exception class RegulationValidationError.
2017-01-06 Vojtech Sidorin   ABITFA-3288: Move helper functions to the FValidation_core module.
"""

import sys
import traceback

from FValidation_settings import DEBUG
import importlib


# Validation rules are collected in this dict.
rules = {"transaction": [], "entity": []}


def load_rules(modules):
    """Load validation rules and return them in dict.

    First, validation rules from modules are loaded into the global dict
    'rules', then the dict is returned.
    """
    # Clean the dict to allow reloading.
    rules.update({"transaction": [], "entity": []})
    # Import/reload rules from the validation modules.
    for module in modules:
        if module in sys.modules:
            importlib.reload(sys.modules[module])
        else:
            __import__(module)
    return rules


def validate_entity(entity_type, operation, caller="validate_entity"):
    """Return a decorator that registers an entity validation rule.

    Keyword arguments:
    entity_type -- Type of entity handled by the decorated function, e.g.
                   'Trade' or 'Instrument'.
    operation   -- Type of operation handled by the decorated function.
                   Possible values are 'Insert', 'Update', 'Delete'.
    caller      -- Who calls the decorated function.  Possible values are
                   'validate_entity' -- the decorated function will be
                       called within the body of validate_entity hook
                       function;
                   'validate_transaction' -- the decorated function will be
                       called inside a loop over entities within the body of
                       validate_transaction hook function.
    """
    assert operation in ("Insert", "Update", "Delete"), \
        "Invalid argument operation. Must be one of 'Insert', 'Update' " \
        "or 'Delete'."
    assert caller in ("validate_entity", "validate_transaction"), \
        "Invalid argument caller. Must be either 'validate_entity' or " \
        "'validate_transaction.'"

    def decorator(function):
        """Register the function as an entity validation rule."""
        rules["entity"].append((function, entity_type, operation, caller))
        return function
    return decorator


def validate_transaction(function):
    """Register the function as a transaction validation rule."""
    rules["transaction"].append(function)


def show_validation_warning(message, popup=True, type_="Warning"):
    """Function to safely show message boxes and log error."""
    import acm
    if popup and str(acm.Class()) == "FTmServer":
        message_box = acm.GetFunction("msgBox", 3)
        message_box(type_, message, 0)
    print("{t}: {m}".format(t=type_, m=message))


def debug_msg(message):
    """Print the message if the global constant DEBUG is set to True."""
    if DEBUG:
        print("DEBUG: {0}".format(message))


def handle_current_exception():
    """Handle the current exception and return exc_info.

    Prints the stack trace of the currently-handled exception and returns info
    about that exception.  The info about the exception is taken from
    sys.exc_info().

    If the constant DEBUG is set to True, the stack trace is printed for every
    exception.  If it is False, the stack trace is printed only for exceptions
    other than ValidationError (and derived).

    Justification:
    When an exception is raised by FValidation, Front Arena throws a
    RuntimeError and details about the original exception, namely the stack
    trace, are lost.  This function prints the stack trace of the original
    exception and also returns info about it.  This info can be stored and
    retrieved later if needed.
    """
    # NOTE: Do not store the returned value of sys.exc_info(), namely the
    # traceback object, in a local variable to prevent creating a circular
    # reference.  (See the documentation of the sys module.)
    if DEBUG or not isinstance(sys.exc_info()[1], ValidationError):
        traceback.print_exc()
    return sys.exc_info()


class ValidationError(Exception):
    """Base class for all validation errors."""
    # NOTE: Some versions of FA Prime (including the one we use at the time of
    # writing this comment, i.e. 2014.4.8) show a popup message box
    # automatically when FValidation raises an exception. Therefore, we set
    # popup=False by default not to show duplicate message boxes.
    def __init__(self, message, popup=False):
        super(ValidationError, self).__init__(message)
        show_validation_warning(message, popup)


class DataValidationError(ValidationError):
    """Validation error that concerns data."""


class AccessValidationError(ValidationError):
    """Validation Error that concerns access violation."""


class RegulationValidationError(ValidationError):
    """Validation Error that originates in a regulation."""
