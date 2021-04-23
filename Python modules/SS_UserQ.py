import ael

def getUsers():
    return map(lambda x: x.userid, list(ael.User))

ael_variables = [('User', 'User', 'string', getUsers(), '', 1, 0)]

def ael_main(ael_dict):
    if len(ael_dict['User']):
        print(ael.User["ABEM805"].add_info('PasswordResetDate'))
