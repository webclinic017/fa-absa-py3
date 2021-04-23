'''
    Date                : 2020-01-10
    Purpose             : Auto revoke license or set to inactive for 3m grace period
                          There are 2 tasks that work together. On initial run
                          only the inactive task must run. For BAU runs, the revoke is run first
                          to reclaim unused licenses and then the disable task is run 
                          to set the next of profiles not being used.
    Department and Desk : Markets business and Markets IT
    Requester           : Marsha de Wet and Jochem Melis
    Developer           : Bhavnisha Sarawan
    CR Number           : 
'''

import acm
import ael

from at_email import EmailHelper
from at_logging import getLogger
from at_addInfo import delete, get_value, save
from at_ael_variables import AelVariableHandler
from EnvironmentFunctions import is_production_environment

LOGGER = getLogger(__name__)
EXCLUDED_USERS = []
EXCLUDED_GROUPS = []
PREVIOUS_USER = acm.FUserGroup['Previous User']
AAM_PREVIOUS_USER = acm.FUserGroup['AAM Previous User']
GT_PREVIOUS_USER = acm.FUserGroup['Previous User GT TR']

def set_input_exluded_users(input_exempted_users):
    for user in input_exempted_users:
        EXCLUDED_USERS.append(acm.FUser[user])

def set_input_exluded_groups(input_exempted_groups):
    for group in input_exempted_groups:
        EXCLUDED_GROUPS.append(acm.FUserGroup[group])

def set_previous_user_groups():
    # Not added to task as this will run for a long time if accidently removed 
    # because some previous users are marked as inactive.
    
    EXCLUDED_GROUPS.append(PREVIOUS_USER)
    EXCLUDED_GROUPS.append(AAM_PREVIOUS_USER)
    EXCLUDED_GROUPS.append(GT_PREVIOUS_USER)
        
def get_users_for_revoking():
    users_for_revoking = []
    inactive_users = acm.FUser.Select('inactive=true')
    for user in inactive_users:
        if user in EXCLUDED_USERS or user.UserGroup() in EXCLUDED_GROUPS:
            continue
        users_for_revoking.append(user)
    return users_for_revoking

def get_users_for_inactivating(login_3m):
    users_for_inactivating = []
    for username in login_3m:
        user = acm.FUser[username]
        if user in EXCLUDED_USERS or user.UserGroup() in EXCLUDED_GROUPS:
            continue
        users_for_inactivating.append(user)
    return users_for_inactivating

def email_message():
    message = "Hello <br /><br />"
    message += ("Your Front Arena account has been inactivated as you "
        "have not used this account for 3 months.<br />"
        "This is part of the automated Front Arena license reclaim process.<br /><br />")
    message += ("You may contact FA RTB (ABCapITRTBFrontArena@absa.africa) "
        "to re-activate your account within the next 3 months.<br />"
        "Thereafter this account will be revoked and you will need to "
        "re-request a license and profile.<br /><br />")
    message += ("If you are a developer from a Tech function or "
        "a Sales Trader with an allocated SalesLight license, you may <br /> "
        "contact FA RTB (ABCapITRTBFrontArena@absa.africa) to change your license type. <br />"
        "This is only allocated (pending availability) to developers who do not support production or "
        "Sales Traders using FX Sales GUI.<br />")
    message += "<br /><br /><small>This email is automatically generated.</small>"
    return message

def send_email(successful_inactives):
    
    subject = "Front Arena SA account inactivated"
    
    email_sender = 'ABCapITRTBFrontArena@absa.africa'

    for username in successful_inactives:
        user = acm.FUser[username]
        if user.Email():
            email_helper = EmailHelper(email_message(), subject, [user.Email()],
                               email_sender, None)
            if str(acm.Class()) == "FACMServer":
                email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
                email_helper.host = EmailHelper.get_acm_host()
            try:
                email_helper.send()
            except Exception as e:
                LOGGER.warning("Warning email not sent: {0}\n".format(e))
        else:
            LOGGER.info('No email address for {0} {1}'.format(user.Name(), user.FullName()))

def get_last_login():
    """Return the last time a person logged in.
       
    Using asql because python takes very long.
    Finds all users who have not logged infor 3 months 
    but their profile was created more than 3 months ago.
    If you include ServiceAccount and/or PreviousUser, this will run for a long time.
    license_type = {10:'PreviousUser',7:'ServiceAccount',12:'SalesLight',11:'BTBNonProd',9:'DualProfile'}
    """
    users_for_inactivating = []
    
    query = """SELECT ul.creat_usrnbr
                    , max(ul.creat_time)
                INTO temp_maxtime
                FROM userlog ul
                WHERE ul.type = 'Login'
                GROUP BY ul.creat_usrnbr

                SELECT temp_maxtime.max
                       , u.userid
                FROM temp_maxtime
                     , user u
                WHERE 1=1
                      AND temp_maxtime.creat_usrnbr =* u.usrnbr
                      AND u.license_type not in (7,9,10,11,12)
                      AND u.creat_time < date_add_delta(TODAY, 0, -3, 0)"""   
    query_results = ael.asql(query)
    if query_results[1]:
        for result in query_results[1]:
            for r in result:
                max_login = r[0]
                user_login = r[1]
                if max_login == '' or max_login <= acm.Time().DateAddDelta(acm.Time.TimeNow(), 0, -3, 0):
                    users_for_inactivating.append(user_login)
    return users_for_inactivating

def inactivate_user(users_for_inactivating):
    """Mark a user as inactive without affecting other user details.
    
    This will be executed on the second task in a batch.
    Only new users who haven't logged in would be marked as inactive.
    RTB can untick the user if this should have not happened or run the rollback.
    """
    successful_inactives = []
    for user in users_for_inactivating:
        acm.BeginTransaction()
        try:
            user_clone = user.Clone()
            user_clone.Inactive('True')
            reqnbr = get_value(user_clone, 'RequestNbr')
            if reqnbr:
                reqnbr = reqnbr + ';SysInactive'
            else:
                reqnbr = ';SysInactive'
            save(user_clone, 'RequestNbr', reqnbr)
            user.Apply(user_clone)
            user.Commit()
            acm.CommitTransaction()
            successful_inactives.append(user.Name())
        except Exception:
            acm.AbortTransaction()
            LOGGER.exception('Failed to inactivate, {0} {1}'.format(user.Name(), user.FullName()))
                                                                
    if len(successful_inactives) > 0:
        LOGGER.info('Inactivated users')
        LOGGER.info(successful_inactives)
        if is_production_environment():
            send_email(successful_inactives)

def revoke_user(users_for_revoking):
    """Move a user whose been inactive for 3m to a Previous User group to reclaim the license.
    
    This will be executed on the first task in a batch.
    All users who were marked as inactive in the previous run will now be revoked to reuse the license.
    There are different Previous User groups for each "organisation" in CIB. 
    A person from a particular group must go into the corresponding Previous User group.
    Group Treasury is within ABSA CAPITAL due to access constraints as the two areas must 
    be able to see and change data created by the other area hence the Previous Group mapping.

    The user will have to raise a new profile request if they still need FA.
    """
    
    for user in users_for_revoking:
        acm.BeginTransaction()
        try:
            # Transaction here to ensure addinfo changes are saved.
            # I do not want to roll back the entire revoke if 1 user fails.
            user_clone = user.Clone()
            
            if user.UserGroup().Description().startswith('Group Treasury'):
                user_clone.UserGroup(GT_PREVIOUS_USER)
            if user.UserGroup().Description().startswith('AAM'):
                user_clone.UserGroup(AAM_PREVIOUS_USER)
            else:
                user_clone.UserGroup(PREVIOUS_USER)
                
            delete(user_clone, 'RoutingUser')
            delete(user_clone, 'BESA_ID')
            reqnbr = get_value(user_clone, 'RequestNbr')
            if reqnbr:
                reqnbr = reqnbr + ';SysRevoke'
            else:
                reqnbr = ';SysRevoke'
            save(user_clone, 'RequestNbr', reqnbr)
            
            user_clone.LicenceType(10)
            
            user.Apply(user_clone)
            user.Commit()
            acm.CommitTransaction()
            LOGGER.info('Revoked, {0} {1}'.format(user.Name(), user.FullName()))
        except Exception:
            acm.AbortTransaction()
            LOGGER.exception('Failed to revoke, {0} {1}'.format(user.Name(), user.FullName()))


ael_gui_parameters = {'hideExtracControls': True,
                      'windowCaption': 'Front Arena License clean up'}

ael_variables = AelVariableHandler()
ael_variables.add_bool("Inactivate",
                       label="Inactivate users",
                       alt=("Inactivate users by setting inactive field to True"))
ael_variables.add_bool("Revoke",
                       label="Revoke user access",
                       alt=("Revoke users access and move to Previous User"))
ael_variables.add("Exempted_Users",
                       label="Exempted_Users",
                       cls="string",
                       collection=acm.FUser.Select(""),
                       mandatory=False,
                       multiple=True, 
                       alt=("Users who should be exempted from this script"))
ael_variables.add("Exempted_Groups",
                       label="Exempted_Groups",
                       cls="string",
                       collection=acm.FUserGroup.Select(""),
                       mandatory=False,
                       multiple=True,
                       alt=("Groups that should be exempted from this script"))


def ael_main(parameters):
    inactivate = parameters["Inactivate"]
    revoke = parameters["Revoke"]
    input_exempted_users = parameters["Exempted_Users"]
    input_exempted_groups = parameters["Exempted_Groups"]
    
    set_input_exluded_users(input_exempted_users)
    set_input_exluded_groups(input_exempted_groups)
    
    if inactivate:
        query_results = get_last_login()
        users_for_inactivating = get_users_for_inactivating(query_results)
        if len(users_for_inactivating) > 0:
            inactivate_user(users_for_inactivating)
        else:
            LOGGER.info('No users to inactivate')
    if revoke:
        set_previous_user_groups()
        users_for_revoking = get_users_for_revoking()
        if len(users_for_revoking) > 0:
            revoke_user(users_for_revoking)
        else:
            LOGGER.info('No users to revoke')
