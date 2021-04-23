"""-----------------------------------------------------------------------
MODULE
    AccessControl_DeleteUserProfile.py
  
HISTORY
==================================================================================
Date            Change no       Developer               Description
----------------------------------------------------------------------------------
2017/12/14                      Bhavnisha Sarawan       Delete User Profiles from User Groups, Users and the User Profile (Initial implementation)

--------------------------------------------------------------------------------"""

import acm

userlinks = acm.FUserProfileLink.Select('')
group = acm.FUserGroup.Select('')

def DeleteGroupLink(group, ListOfProfiles):
    for profileName in ListOfProfiles:
        try:
            for g in group:
                try:
                    grouplink = acm.FGroupProfileLink.Select("userGroup={0}".format(g.Oid()))
                except Exception, e:
                    print 'Group ', g.Name(), 'does not have profiles'
                for profile in grouplink:
                    if profile.UserProfile().Name() == profileName.Name():
                        try:
                            profile.Delete()
                            print 'Deleting {0} for {1}'.format(profileName.Name(), g.Name())
                        except Exception, e:
                            print 'ERROR deleting {0} for {1} with error {2}'.format(profileName.Name(), g.Name(), e)

        except Exception as e:
            print 'ERROR in group selection ...', e


def DeleteUserLink(userlinks, ListOfProfiles):
    for userlink in list(userlinks):
        if userlink.UserProfile() in ListOfProfiles:
            try:
                print 'Deleting {0} for {1}'.format(userlink.UserProfile().Name(), userlink.User().Name())
                userlink.Delete()
            except Exception as e:
                print 'ERROR deleting {0} for {1} with error {2}'.format(userlink.UserProfile().Name(), userlink.User().Name(), e)
     
def DeleteUserProfile(ListOfProfiles):
    for profileName in ListOfProfiles:
        try:    
            p = acm.FUserProfile[profileName.Name()]
            print 'Deleting {0}'.format(p.Name())
            p.Delete()
        except Exception as e:
            print 'ERROR deleting {0} with error {1}'.format(profileName.Name(), e)



ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Delete User Profile(s)'}

ael_variables = [['profiles', 'profiles', 'FUserProfile', None, None, 1, 1]]


def ael_main(parameter):
    
    ListOfProfiles = parameter["profiles"]
    print 'Processing grouplinks for deleting ...'
    DeleteGroupLink(group, ListOfProfiles)
    print 'Processing userlinks for deleting ...'
    DeleteUserLink(userlinks, ListOfProfiles)
    print 'Processing user profiles for deleting ...'
    DeleteUserProfile(ListOfProfiles)
    print 'Script completed'
