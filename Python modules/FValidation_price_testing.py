"""-----------------------------------------------------------------------------
PURPOSE              :  FValidation hooks for price testing objects
DEPARTMENT           :  PCT Valuations
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2021-02-23  CHG0154733     Libor Svoboda       Initial Implementation
"""
import ael
from FValidation_core import validate_entity, ValidationError
from FValidation_Utils import is_allowed


PT_CURVE_SUFFIX = '/PT'


def is_pt_curve(curve_name):
    if not curve_name.endswith(PT_CURVE_SUFFIX):
        return False
    original_curve_name = curve_name[:-len(PT_CURVE_SUFFIX)]
    if ael.YieldCurve[original_curve_name]:
        return True
    return False


@validate_entity('YieldCurve', 'Insert')
@validate_entity('YieldCurve', 'Update')
@validate_entity('YieldCurve', 'Delete')
def validate_price_testing_curve_update(entity, operation):
    curve_name = entity.yield_curve_name
    if not (is_pt_curve(curve_name)
            or (entity.original() 
                and is_pt_curve(entity.original().yield_curve_name))):
        return
    if not is_allowed(ael.user(), 'PT Update Curve'):
        raise ValidationError(('Failed to %s Price Testing curve "%s", '
                               'component "PT Update Curve" not in user '
                               'profile.') % (operation.lower(), curve_name))


@validate_entity('ContextLink', 'Insert')
@validate_entity('ContextLink', 'Update')
@validate_entity('ContextLink', 'Delete')
def validate_price_testing_curve_link(entity, operation):
    if entity.type not in ('Yield Curve', 'Repo'):
        return
    curve_name = entity.name
    if not (is_pt_curve(curve_name)
            or (entity.original() 
                and is_pt_curve(entity.original().name))):
        return
    if not is_allowed(ael.user(), 'PT Link Curve'):
        raise ValidationError(('Failed to %s context link with Price Testing '
                               'curve "%s", component "PT Link Curve" not in '
                               'user profile.') % (operation.lower(), curve_name))

