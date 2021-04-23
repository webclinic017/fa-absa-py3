"""-----------------------------------------------------------------------------
PURPOSE              :  FValidation hooks for user profile validations
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-10-08  CHG0130411     Libor Svoboda       Initial Implementation
"""
import ael
from FValidation_core import validate_entity, ValidationError


ALL_COMPS_PROFILES = [_f for _f in (
    ael.UserProfile[546], # ALL_COMPONENTS
    ael.UserProfile[557], # ALL_COMPS_NO_APPS
    ael.UserProfile[601], # TBRIT_SUPER_USER
) if _f]

ALL_COMPS_GROUPS = [_f for _f in (
    ael.Group[563], # IT RTB
    ael.Group[494], # Integration Process
    ael.Group[608], # PCG System User
    ael.Group[609], # SysUserProcess
    ael.Group[619], # System Data Feeds
    ael.Group[495], # System Processes
) if _f]


@validate_entity('UserProfileLink', 'Insert')
@validate_entity('UserProfileLink', 'Update')
@validate_entity('GroupProfileLink', 'Insert')
@validate_entity('GroupProfileLink', 'Update')
def validate_all_comps_profile_link(entity, operation):
    try:
        environment = ael.ServerData.select()[0].customer_name
    except IndexError:
        return
    if environment != 'Production':
        return
    if entity.record_type == 'UserProfileLink':
        if not entity.usrnbr:
            return
        group = entity.usrnbr.grpnbr
    else:
        group = entity.grpnbr
    profile = entity.profnbr
    if profile in ALL_COMPS_PROFILES and group not in ALL_COMPS_GROUPS:
        raise ValidationError(('User profile validation: Profile "%s" can be '
                                'only added to groups: %s.')
                              % (profile.profid, 
                                 ', '.join([group.grpid 
                                            for group in ALL_COMPS_GROUPS])))

