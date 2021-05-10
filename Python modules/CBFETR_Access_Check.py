'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CBFETR_Access_Check
PROJECT                 :       Cross Border Foreign Exchange Transaction Reporting
PURPOSE                 :       This module checks for Front Arena access to be able to initial Ad Hoc BoP 
                                Reporting from Front Arena.
DEPARTMENT AND DESK     :       Operations
REQUASTER               :       CBFETR Project - BOPCUS 3 Upgrade
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       CHNG0001209844
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2013-08-17      CHNG0001209844  Heinrich Cronje                 Initial Implementation

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    When this class is instantiated, Front Arena access is automatically validated.
    If a user has not got access to Operations Manager Application and Settlement 
    DBObject the Ad Hoc BoP Reporting module will not run.
'''

import acm

class CBFETR_Access_Check():
    def __init__(self):
        self.operationsManagerFlag = False
        self.settlementFlag = False
        self.check_BoP_AccessResult = False
        self.userProfile = None
        self.validate_User_Access()

    def check_BoP_Access(self):
        for component in self.userProfile.ProfileComponents():
            if (component.Component().Type() == 'Application' and component.Component().Name() == 'Operations Manager'):
                self.operationsManagerFlag = True

            if (component.Component().Type() == 'DBObject' and component.Component().Name() == 'Settlement'):
                self.settlementFlag = True
        
        if self.operationsManagerFlag and self.settlementFlag:
            self.check_BoP_AccessResult = True

    def validate_User_Access(self):
        user = acm.User()

        #user Profile Links
        userProfileLinks = user.Links()

        for link in userProfileLinks:
            self.userProfile = link.UserProfile()
            self.check_BoP_Access()

        if not self.check_BoP_AccessResult:
            #user Group
            userGroup = user.UserGroup()

            self.operationsManagerFlag = False
            self.settlementFlag = False
            groupProfileLinks = acm.FGroupProfileLink.Select('userGroup = %i' %userGroup.Oid())
            for link in groupProfileLinks:
                self.userProfile = link.UserProfile()
                self.check_BoP_Access()
