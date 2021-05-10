'''
===================================================================================================
PURPOSE: This module will be used to validate which users can use the Hedge Effectiveness modules
            and what users are allowed to do within the UI
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''
import acm

import HedgeConstants


# Class contains private variables with public getter methods
class UserAccess:
    # Class is instantiated with an acm user object
    def __init__(self, user):
        self.user = user
        self._user_profiles = None
        self._user_components = None
        self._valid_statuses = None

    def get_user_profiles(self):
        if self._user_profiles:
            return self._user_profiles

        result = acm.FSet()
        # Usr level profiles
        for upl in acm.FUserProfileLink.Select('user="%s"' % self.user.Name()):
            result.Add(upl.UserProfile().Name())

        # Grp level profiles
        grp = self.user.UserGroup()
        for gpl in acm.FGroupProfileLink.Select('userGroup="%s"' % grp.Name()):
            result.Add(gpl.UserProfile().Name())

        self._user_profiles = result
        return result

    def get_user_components(self):
        if self._user_components:
            return self._user_components

        result = acm.FSet()
        profiles = self.get_user_profiles()

        for prof_name in profiles:
            for component in acm.FUserProfile[prof_name].ProfileComponents():
                result.Add(component.Component().CompName())

        self._user_components = result
        return result

    def is_hedge_user(self):
        profiles = self.get_user_profiles()
        if HedgeConstants.STR_SUPER_USER_PROFILE in profiles:
            return True

        for valid_profile in HedgeConstants.Hedge_User_Profiles.get_all_as_list():
            if valid_profile in profiles:
                return True

        return False

    def get_valid_statuses(self):
        if self._valid_statuses:
            return self._valid_statuses

        result = acm.FSet()
        m_dict = HedgeConstants.user_components()
        profiles = self.get_user_profiles()

        if HedgeConstants.STR_SUPER_USER_PROFILE in profiles:
            for status in HedgeConstants.Hedge_Relation_Status.get_all_as_list():
                result.Add(status)
            self._valid_statuses = result
            return result

        for prof_name in profiles:
            if prof_name in m_dict:
                result.AddAll(m_dict[prof_name])

        self._valid_statuses = result
        return result
