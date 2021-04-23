"""----------------------------------------------------------------------------
PROJECT                 :  Prime Services
PURPOSE                 :  Change name and full name of the counterparty
DEPARTMENT AND DESK     :  CIB Client Static
REQUESTER               :  Simone Meyer
DEVELOPER               :  Jakub Tomaga
CR NUMBER               :  3974633
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date         Change no   Developer       Description
--------------------------------------------------------------------------------
2016-09-27   3974633     Jakub Tomaga    Initial Implementation


CIB Client Static is experiencing issues with their user profile and party name
changes. When they change the name from the GUI, all add info fields' values
change to their default values. Update through the script keeps the add info
fields unchanged. This script removes the necessity for manual intervention.

"""

import acm
from at_ael_variables import AelVariableHandler
from PS_Functions import (get_pb_fund_shortname,
                          get_pb_fund_counterparty,
                          get_pb_fund_counterparties)


SHORTNAMES = [get_pb_fund_shortname(cp) for cp in get_pb_fund_counterparties()]


def party_name_hook(selected_variable):
    """Display current party name and fullname."""
    if selected_variable.value:
        cp = get_pb_fund_counterparty(selected_variable.value)
        cp_name = ael_variables.get('original_name')
        cp_name.value = cp.Name()
        cp_fullname = ael_variables.get('original_fullname')
        cp_fullname.value = cp.Fullname()
        

def verify_party_name_hook(selected_variable):
    """Verify if new party name is unique."""
    if selected_variable:
        name = selected_variable.value
        cpty = acm.FParty[name]
        if cpty:
            msg = "Party {0} already exists".format(name)
            selected_variable.value = ""
            acm.GetFunction('msgBox', 3)("Failed validation", msg, 0)


def verify_party_fullname_hook(selected_variable):
    """Verify if new party fullname is unique."""
    if len(selected_variable.value):
        fullname = selected_variable.value
        parties = acm.FParty.Select("fullname='{0}'".format(fullname))
        if parties:
            if len(parties) == 1:
                names = parties[0].Name()
            else:
                names = ','.join([party.Name() for party in parties])
            msg = "Party {0} has already fullname {1}".format(names, fullname)
            selected_variable.value = ""
            acm.GetFunction('msgBox', 3)("Failed validation", msg, 0)


ael_variables = AelVariableHandler()
ael_variables.add("shortname",
                  label="Fund Shortname",
                  collection=sorted(SHORTNAMES),
                  hook=party_name_hook)
ael_variables.add("original_name",
                  label="Original Counterparty Name",
                  enabled=False)
ael_variables.add("original_fullname",
                  label="Original Counterparty Full Name",
                  enabled=False)
ael_variables.add("new_name",
                  label="New Counterparty Name",
                  hook=verify_party_name_hook)
ael_variables.add("new_fullname",
                  label="New Counterparty Full Name",
                  hook=verify_party_fullname_hook)


def ael_main(config):
    """Update counterparty names for Prime Services fund."""
    shortname = config["shortname"]
    original_name = config["original_name"]
    new_name = config["new_name"]
    new_fullname = config["new_fullname"]

    try:
        party = acm.FParty[original_name]
        party.Name(new_name)
        party.Fullname(new_fullname)
        party.Commit()
        print("Fund: {0}".format(shortname))
        print("Counterparty Name: {0}".format(party.Name()))
        print("Counterparty Fullname: {0}".format(party.Fullname()))
        print("Completed Successfully")
    except Exception as ex:
        print("Error: {0}".format(ex))
