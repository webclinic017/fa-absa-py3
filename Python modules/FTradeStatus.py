"""----------------------------------------------------------------------------
MODULE
    FTradeStatus
    (c) Copyright 2004 by Front Capital Systems AB. All rights reserved.


DESCRIPTION
    This module handles user rights for a user defined trade status.
    The following steps are needed to handle a new trade status e.g. "MyStatus"
    1. Enter a new Trade Status "MyStatus" in the corresponding application
    2. Enter 2 new Operations: "MyStatus" and "Modify MyStatus"
    3. Edit the 2 dictionaries below saying from which Statuses one is allowed
       to enter INTO the MyStatus, and which statuses are allowed to be entered
       into AFTER the MyStatus, given you have the Operation to do so.
    4. Assign the Operation "MyStatus" and "Modify MyStatus" to the profiles needing it
    5. Further criteria for when a status transition, or a modification should
       be allowed, can be added to check_trade_status_action
    6. Further criteria to when a new status is elible, can be added to
       change_trade_status_allowed
----------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no Developer          Description
--------------------------------------------------------------------------------
2012-09-04  PSB-236   Anwar Banoo        Amended the hardcoded users in change_trade_status_allowed method to use system groups instead
2017-05-16  Vojtech Sidorin  ABITFA-4789: Remove the rule that prevents changing the status of Funding Desk trades.
"""

import acm
import ael


# Dictionary showing from which statuses can one change INTO "MyStatus", e.g.
intoD = {'FO-FO Rejected' : ['Simulated', 'FO Confirmed'],
        'FO Sales' : ['Simulated']}

# Dictionary for which statuses that MyStatus can change into
afterD= {'FO-FO Rejected' : ['FO Confirmed'],
        'FO Sales' : ['FO Confirmed']}

# Dictionary to translate TradeStatus into corresponding Operation. At least
# add statuses of the afterD here in the format TradeStatus:Operation
# N.B. Always means that if it is an allowed transition status, you don't need
# the Operation in your profile.
trdStatOpD = { 'Simulated':'Always','FO Confirmed':'FO Confirm',
            'BO Confirmed':'BO Confirm', 'Void':'Always' }

sys_proc = ael.Group[495]
int_proc = ael.Group[494]
sys_exclude = [sys_proc, int_proc]


def is_component_in_user_profile(compname,ctype='Operation'):
    """Does this user have this component in one of his profiles"""
    if compname == 'Always': return 1

    user = acm.FUser[ael.userid()]

    groupLinks = acm.FGroupProfileLink.Select('userGroup=%s' %user.UserGroup().Name())

    for g in groupLinks:
        for c in g.UserProfile().ProfileComponents():
            if c.Component().Type() == ctype and c.Component().Name() == compname:
                return 1

    for l in user.Links():
        for lc in l.UserProfile().ProfileComponents():
            if lc.Component().Type() == ctype and lc.Component().Name() == compname:
                return 1
    return 0


def check_trade_status_action(trd_old, trd_new):
    """
    Is this TradeStatus transition allowed?
    0=No, 1=Yes, 2=Look at default rules
    """
    if ael.user().userid in ('FMAINTENANCE'):
        return 1
    tsv_list=[(mbr.nice_name) for mbr in ael.TradeStatusValue.select()]
    target_name = trd_new.status

    # No change in status
    if trd_new.status == trd_old.status:
        if target_name in tsv_list:
            return is_component_in_user_profile('Modify '+ target_name)

    # Change in status
    if target_name in tsv_list:
        return is_component_in_user_profile(target_name)
    elif trd_old.status in tsv_list:
        return is_component_in_user_profile(trdStatOpD[target_name])

    #fo part needs to be in the bo guys profile due to bug in front when changing trade status and premium is recalc'd due to rounding
    #spr raised for this - as soon as that is fixed, this can be removed!  Anwar
    if ((trd_old.status == 'FO Confirmed') and (trd_new.status == 'BO-BO Confirmed')):
        if trd_new.insaddr.instype in ('Bond', 'IndexLinkedBond', 'FRN', 'Bill', 'BuySellback', 'Repo/Reverse'):
            if is_component_in_user_profile('FO->BOBO') == 1:
                return 1

    # ABITFA-1930 it is not possible to change the status
    # from FO confirmed to any other confirmed status while a
    # trade is in allocate portfolio status.
    if trd_old.status == 'FO Confirmed' and trd_new.prfnbr.prfid.lower().startswith('allocate'):
        confirmed_statuses = ('BO Confirmed', 'BO-BO Confirmed', 'Legally Confirmed') # do not include 2:'FO Confirmed'
        if trd_new.status in confirmed_statuses:
            ael.log('It is not possible to change the status from FO confirmed '
                    'to any other confirmed status while a trade is in allocate '
                    'portfolio status.')
            return 0

    return 2


def change_trade_status_allowed(current, new, trade):
    """Given current status, should the new status be in the drop down list?"""
    if ael.user().grpnbr in sys_exclude:
        return 1

    tsv_list=[(mbr.nice_name) for mbr in ael.TradeStatusValue.select()]
    ret = 2
    if new in tsv_list:
        if current in intoD[new]:
            ret = is_component_in_user_profile(new)
    elif current in tsv_list:
        if new in afterD[current]:
            ret = is_component_in_user_profile(trdStatOpD[new])

    return ret
