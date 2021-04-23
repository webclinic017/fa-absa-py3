""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitSetup.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FLimitSetup

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Setup script for the installation of items required by the limits base framework.

-------------------------------------------------------------------------------------------------------"""
import acm
import FLimitSettings
import FLimitUtils
import FUxCore


def InitialiseLimitStateChart():
    # pylint: disable-msg=E1101
    if FLimitSettings.CreateStandardDefaultStateChart():
        try:
            name = FLimitSettings.DefaultStateChart()
            if name and not acm.FStateChart[name]:
                if CanCreateStateChart():
                    FLimitUtils.CreateStandardLimitStateChart(name)
                    acm.Log('Created standard limit state chart "' + name + '".')
                else:
                    acm.Log('Default limit state chart "' + name + '" does not exist. '
                            'User does not have the required permissions to create it.')
        except Exception as e:
            acm.Log('Could not create standard limit state chart: ' + str(e))

def CanCreateStateChart():
    return CanCreateDatabaseObject('StateChart') and CanCreateDatabaseObject('TextObject')

def CanCreateDatabaseObject(objectType):
    recType = acm.FEnumeration['enum(B92RecordType)'].Enumeration(objectType)
    return acm.User().DBObjectActionAllowed(recType, 0, 1)

def ValidateLimitSetup():
    InitialiseLimitStateChart()

def CreateLimitSetupMenuItem(_eii):
    # pylint: disable-msg=W0232
    # Use a dummy menu item that will never be displayed to allow the python module 
    # (and thus limit setup check) to be run automatically when required
    class DummyMenuItem(FUxCore.MenuItem):
        def Applicable(self):
            return False
    return DummyMenuItem()


ValidateLimitSetup()

