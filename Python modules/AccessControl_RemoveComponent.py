"""-----------------------------------------------------------------------
MODULE
    AccessControl_RemoveComponent.py
  
HISTORY
==================================================================================
Date            Change no       Developer               Description
----------------------------------------------------------------------------------
2017/12/14                      Bhavnisha Sarawan       Remove component(s) from a User Group (Initial implementation)

--------------------------------------------------------------------------------"""



import acm

def RemoveComponentFromUserProfile(ListOfComponents, ListOfProfiles):
    for profile in ListOfProfiles:
        for component in list(profile.ProfileComponents()):
            if component.Component().Name() in (ListOfComponents):
                try:
                    print 'Deleting {0} for {1} ...'.format(component.Component().Name(), profile.Name())
                    component.Delete()
                except Exception as e:
                    print 'ERROR deleting {0} for {1} with error {3}...'.format(component.Component().Name(), profile.Name(), e)


ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Remove component from a Group'}

ael_variables = [['profiles', 'profiles', 'FUserProfile', None, None, 1, 1],
                    ['component', 'component', 'string', None, None, 1, 1]]


def ael_main(parameter):
    
    ListOfProfiles = parameter["profiles"]
    ListOfComponents = parameter["component"]
    print ListOfProfiles, ListOfComponents
    print 'Processing user profiles for removal of components ...'
    RemoveComponentFromUserProfile(ListOfComponents, ListOfProfiles)
    print 'Script completed'

