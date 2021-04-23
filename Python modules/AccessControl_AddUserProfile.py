"""-----------------------------------------------------------------------
MODULE
    AccessControl_AddUserProfile.py
  
HISTORY
==================================================================================
Date            Change no       Developer               Description
----------------------------------------------------------------------------------
2017/12/14                      Bhavnisha Sarawan       Add User Profiles to groups(Initial implementation)

--------------------------------------------------------------------------------"""

import acm

def AddProfileToGroups(ListOfGroups, ListOfProfiles):
    for profile in ListOfProfiles:
        for group in ListOfGroups:
            try:
                new_GroupProfileLink = acm.FGroupProfileLink()
                new_GroupProfileLink.UserGroup(group.Name())
                new_GroupProfileLink.UserProfile(profile.Name())
                print 'Adding {0} for {1} ...'.format(profile.Name(), group.Name()) 
                new_GroupProfileLink.Commit()
            except Exception as e:
                print 'ERROR adding {0} for {1} with error {2}'.format(profile.Name(), group.Name(), e) 


ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Add User Profile(s) to a Group'}

ael_variables = [['profiles', 'profiles', 'FUserProfile', None, None, 1, 1],
                    ['groups', 'groups', 'FUserGroup', None, None, 1, 1]]


def ael_main(parameter):
    
    ListOfProfiles = parameter["profiles"]
    ListOfGroups = parameter["groups"]
    print 'Processing profiles for addition to group ...'
    AddProfileToGroups(ListOfGroups, ListOfProfiles)
    print 'Script completed'

