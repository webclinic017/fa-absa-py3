"""Restrict access to Yield Curves and Volatility Structures.

History
=======

0000-00-00 Anil Parbhoo     Initial implementation; requester: MO (Dirk Strauss); CR 651043.
2014-08-31 Vojtech Sidorin  CHNG0002210109 Mark as deprecated module
2015-04-28 Vojtech Sidorin  Start refactoring; unmark as deprecated.
2015-06-05 Vojtech Sidorin  ABITFA-3501 Refactor and update rules 7, 100, 101.
2015-08-20 Vojtech Sidorin  ABITFA-3743: Include rule numbers in messages.
"""

import acm

from FValidation_core import (validate_entity,
                              AccessValidationError)
from FValidation_Utils import is_allowed
from SAGEN_YC_VOL_ACCESS import check_attr


@validate_entity("YCAttribute", "Insert")
@validate_entity("YCAttribute", "Update")
@validate_entity("YCAttribute", "Delete")
def rule_7a_restrict_access_to_yc_attributes(entity, operation):
    """Rule 7a: Restrict access to Yield Curve Attribute Spread Data.

    Only users with the following components can edit Yield Curve Attribute
    Spread Data: 'FV_YC_full_access', 'FV_YCAttribute_full_access'.
    """
    user = acm.User()
    if not (is_allowed(user, "FV_YC_full_access")
            or is_allowed(user, "FV_YCAttribute_full_access")):
        msg = ("FV7a: You are not allowed to edit Yield Curve Attribute "
               "Spread Data. Please contact TCU.")
        raise AccessValidationError(msg)


@validate_entity("Benchmark", "Insert")
@validate_entity("Benchmark", "Update")
@validate_entity("Benchmark", "Delete")
def rule_7b_restrict_access_to_yc_benchmarks(entity, operation):
    """Rule 7b: Restrict access to Yield Curve Benchmarks.

    Only users with the following components can edit Yield Curve
    Benchmarks: 'FV_YC_full_access', 'FV_Benchmark_full_access'.
    """
    user = acm.User()
    if not (is_allowed(user, "FV_YC_full_access")
            or is_allowed(user, "FV_Benchmark_full_access")):
        msg = ("FV7b: You are not allowed to edit Yield Curve Benchmarks. "
               "Please contact TCU.")
        raise AccessValidationError(msg)


@validate_entity("YieldCurve", "Insert")
@validate_entity("YieldCurve", "Update")
def rule_100_restrict_access_to_yc_def(entity, operation):
    """Rule 100: Restrict access to Yield Curve definitions.

    Users with component 'FV_YC_full_access' can edit Yield Curve
    definitions without restrictions.  Other users cannot create new Yield
    Curves and can update only unimportant fields, which are defined in
    module SAGEN_YC_VOL_ACCESS.
    """
    user = acm.User()
    if not is_allowed(user, "FV_YC_full_access"):
        if operation == "Insert":
            # Forbid creating new Yield Curves.
            msg = ("FV100a: You are not allowed to create a new Yield "
                   "Curve definition. Please contact TCU.")
            raise AccessValidationError(msg)
        elif operation == "Update":
            # Allow updating only unimportant fields.
            if check_attr(entity, entity.original()) == 1:
                msg = ("FV100b: You are not allowed to update Yield "
                       "Curve definition fields that are considered "
                       "important. Please contact TCU.")
                raise AccessValidationError(msg)
        else:
            raise ValueError("FV100: Unhandled operation '{0}'."
                                .format(operation))


@validate_entity("Volatility", "Insert")
@validate_entity("Volatility", "Update")
def rule_101_restrict_access_to_volatility_def(entity, operation):
    """Rule 101: Restrict access to Volatility Structure definitions.

    Users with component 'FV_Vol_full_access' can edit Volatility Structure
    definitions without restrictions.  Other users cannot create new
    Volatility Structures and can update only unimportant fields, which
    are defined in module SAGEN_YC_VOL_ACCESS.
    """
    user = acm.User()
    if not is_allowed(user, "FV_Vol_full_access"):
        if operation == "Insert":
            # Forbid creating new Volatility Structures.
            msg = ("FV101a: You are not allowed to create a new "
                   "Volatility Structure definition. Please contact TCU.")
            raise AccessValidationError(msg)
        elif operation == "Update":
            # Allow updating only unimportant fields.
            if check_attr(entity, entity.original()) == 1:
                msg = ("FV101b: You are not allowed to update Volatility "
                       "Structure definition fields that are considered "
                       "important. Please contact TCU.")
                raise AccessValidationError(msg)
        else:
            raise ValueError("FV101: Unhandled operation '{0}'."
                                .format(operation))
