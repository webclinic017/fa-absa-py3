'''
    Date                : 2020-01-10
    Purpose             : Activate user that should not have been inactivated by SAGEN_Disable_ARO_Users
    Department and Desk : Markets business and Markets IT
    Requester           : Marsha de Wet and Jochem Melis
    Developer           : Bhavnisha Sarawan
    CR Number           : 
'''

import acm

from at_logging import getLogger
from at_addInfo import delete, get_value, save
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)

def mark_users_active(activate_users):
    """Mark a user as active."""
    failed_actives = []
    successful_actives = []
    for username in activate_users:
        user = acm.FUser[username]
        try:
            acm.BeginTransaction()
            user_clone = user.Clone()
            user_clone.Inactive('False')
            reqnbr = get_value(user_clone, 'RequestNbr')
            if reqnbr:
                    reqnbr = reqnbr + ';SysActive'
            else:
                    reqnbr = ';SysActive'
            save(user_clone, 'RequestNbr', reqnbr)
            user.Apply(user_clone)
            user.Commit()
            acm.CommitTransaction()
            LOGGER.info('Activated user, %s' % (user.Name()))
        except Exception:
            acm.AbortTransaction()
            LOGGER.exception('Failed to activate, %s %s' % (user.Name(), user.FullName()))


    if len(successful_actives) > 0:
                LOGGER.info('Activated users')
                LOGGER.info(successful_actives)

    if len(failed_actives) > 0:
                for user in failed_actives:
                                LOGGER.exception('Failed to activate, %s %s' % (user.Name(), user.FullName())) 


ael_gui_parameters = {'hideExtracControls': True,
                      'windowCaption': 'Front Arena License inactive rollback'}

ael_variables = AelVariableHandler()
ael_variables.add("Activate_users",
                       label="Activate_users",
                       cls="string",
                       collection=acm.FUser.Select(""),
                       mandatory=True,
                       multiple=True, 
                       alt=("Mark users as active"))


def ael_main(parameters):
    activate_users = parameters["Activate_users"]
    mark_users_active(activate_users)
