"""---------------------------------------------------------------------------
MODULE
    FANotifyUtils - generic methods required for the library

DESCRIPTION
    This module contains the genric methods used by the FANotification library.

---------------------------------------------------------------------------"""

import acm

def string_padding(data, limit=12):
    """Performs string padding. It limits the length of logger source in notification logs."""
    if len(data) < limit:
        data = data.ljust(limit)
    else:
        data = data[:limit]
    return data 

def get_acm_user(user):
    """Get ACM users"""
    acm_users = []
    invalid_users = []
    user_lst = string_as_list(user)
    if user_lst:
        for usr in user_lst:
            if acm.FUser[usr]:
                acm_users.append(acm.FUser[usr].Name())
            else:
                invalid_users.append(usr)
    return acm_users, invalid_users

def string_as_list(strng):
    """Returns a list from string separated by comma"""
    lst = []
    if isinstance(strng, str):
        try:
            lst = eval(strng)
        except Exception:
            strng_split = strng.split(',')
            for data in strng_split:
                lst.append(data.strip().strip("'").strip('"'))
    elif isinstance(strng, type([])):
        for i in strng:
            if isinstance(i, str):
                lst.append(i.strip())
            else:
                lst.append(i)
    return lst
