"""-----------------------------------------------------------------------------
PURPOSE              :  FValidation hooks for TextObject validations
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation
"""
import ael
from FValidation_core import validate_entity, ValidationError
from FValidation_Utils import is_allowed


@validate_entity('TextObject', 'Update')
@validate_entity('TextObject', 'Insert')
def restrict_statements_manual_actions(text_object, _operation):
    if not (text_object.type == 'Customizable' 
            and text_object.subtype == 'Statements'):
        return
    
    if is_allowed(ael.user(), 'Statements Manual Actions'):
        return
    
    msg = ('You are not allowed to perform the requested action. '
           'Component "Statements Manual Actions" not in user profile.')
    raise ValidationError(msg)

