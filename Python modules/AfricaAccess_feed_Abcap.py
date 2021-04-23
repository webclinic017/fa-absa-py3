'''
Module is used to pull required data from front about its users and output to a txt document.  Will run daily for OneCert feed.

History
    05-02-2014         Marcus Ambrose         Initial deployment.
    28-09-2015         Fancy Dire             Updated the get_last_login method to use dbsql instead as it was taking too long for
                                              the AbCap instance.
    19-08-2019         Bhavnisha Sarawan      Update to ABSA CIB data
    28-01-2020         Bhavnisha Sarawan      Copied OneCert_feed_Abcap, changed footer, line output and file name to be sent to Africa Access instead of Barclays
    28-02-2020         Bhavnisha Sarawan      Add Ab number to the file so that Africa Access can link the FA ID to a person
    26-05-2020         Bhavnisha Sarawan      Remove active user flag, remove inactive users
    17-09-2020         Bhavnisha Sarawan      Add active user flag as hardcoded, remove footer, move Ab number column, add logic for LAM group as superusers, remove timestamp from filename
'''

import acm 
import ael
import re 
import datetime 
import FRunScriptGUI 
import os


def get_last_login():
    """Returns user's last login time"""
    query = ' \
        SELECT \
               distinct os_user,\
                max(creat_time)\
        FROM \
                user_log \
        WHERE \
                type =  1 \
        GROUP BY os_user'

    userLog = ael.dbsql(query)
    last_login = {}
    if userLog:
        for row in userLog[0]:
            last_login[row[0]] = row[1]
    return last_login


def get_privilege_status(user):
    """Returns 'Y' or 'N' depending if user has privileges"""
    group = user.UserGroup()
    grouplink = acm.FGroupProfileLink.Select("userGroup={0}".format(group.Oid()))
    if user.Links():
        for link in user.Links():
            if link.display_id() in ("ALL_COMPONENTS" or "IT LAM"):
                return 'Y'
    if group.Name() == 'IT LAM':
        return 'Y'
    for gl in grouplink:
        if gl.display_id() == "ALL_COMPONENTS":
            return 'Y'
    return 'N'

    
def get_active_users():
    """Returns active users"""
    active_users = []
    users = acm.FUser.Select('')
    
    for user in users:
        if not user.UserGroup().Name().__contains__('Previous'):
            active_users.append(user)
    return active_users

        
def get_username(user):
    """If a windows login is used, this is returned. Otherwise the citrix id is returned.""" 
    pattern = '^[A-Z][A-Z]'
    user_id = user.Name()

    if re.match(pattern, user_id):
        return user_id
    else:
        principle_pattern = re.compile('^[a-z][a-z]')
        for u in acm.FPrincipalUser.Select("user = " + user.Name()):
            arr = u.Principal().split('@')
            if re.match(principle_pattern, arr[0]):
                return arr[0]
        return user_id

        
def get_user_group(user):
    """Checks what user license type is and returns the user type (user or system)"""
    if user.LicenceType().Name() in ('ServiceAccount'):
        return 'System'
    return 'User'


def get_ab_number(user):
    """Returns the AB number value"""
    return user.add_info('AB Number')

directory_selection=FRunScriptGUI.DirectorySelection()

    
ael_variables = [
    ['File Path', 'File Path', directory_selection, None, directory_selection, 0, 1,
    'The file path to the directory where the report should be put. Environment variables can be specified for Windows (%VAR%) or Unix ($VAR).', None, 1]
    ]

        
def ael_main(ael_variables):
    
    dt = datetime.datetime.now()
    time_stamp = datetime.datetime.strftime(dt, "%Y%m%d_%H%M")   
    active_users = get_active_users() 
    length = len(active_users)
    
    file_path = ael_variables['File Path']
    file_name = "ABCAPFRONTARENA_PROD" + ".txt"
    lastLogin = get_last_login()
    last_login = ''
    
    with open(os.path.join(str(file_path), file_name), 'w') as file:
        header = "User_Unique_ID|User_Application_Account_ID|Application_Entitlement_Name|Privileged_Status|Account_Type|Active_Status|Last_Login_Date\n"
        file.write(header)
        
        for user in active_users:
            user_app_account_id = get_username(user)
            if user.UserGroup():
                app_profile_name = user.UserGroup().Name()
                account_type = get_user_group(user)
            ab_number = get_ab_number(user)
            if lastLogin.has_key(user.Name().lower()):
                last_login = acm.Time.DateTimeFromTime(lastLogin[user.Name().lower()])
            privileges = get_privilege_status(user)
            
            file.write("%s|%s|%s|%s|%s|%s|%s\n" % (ab_number, user_app_account_id, app_profile_name, privileges, account_type, 'Y', last_login))
    
    print "Wrote secondary output to: " + str(file_path) + "/" + file_name
