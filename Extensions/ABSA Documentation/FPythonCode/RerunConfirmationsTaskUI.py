"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    RerunConfirmationsTaskUI

DESCRIPTION
    This module contains UI elements used for controlling menu access to the
    'Rerun Operations STP' AEL main script.

    The items in this module are only necessary due to the FMenuExtension property
    ProfileComponent not working as expected for custom applications.  A related
    SPR 362932 was found that may address this from Front Arena version 2018.1.
    If it is found that this issue has been addressed in future versions, then this
    module can be removed and the FMenuExtension adjusted to invoke this script
    using Function=FRunScriptMENU.StartFunction and ProfileComponent=Rerun
    Operations STP.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-06-18      FAOPS-536       Stuart Wilson           Kgomotso Gumbo          Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import FUxCore


class MenuItem(FUxCore.MenuItem):
    """
    Menu item used to launch the 'Rerun Operations STP' AEL main
    script.
    """

    def __init__(self, extension_object):
        """
        Constructor.
        """
        pass

    @FUxCore.aux_cb
    def Invoke(self, eii):
        """
        Perform the action on the menu item being invoked.
        """
        if not self._user_has_access():
            return
        # Importing this module here in order to prevent any
        # import failure from breaking the UI.  This usually
        # occurs in dev environments when developers import
        # non-existent or broken hooks.
        import RerunConfirmationsTask
        acm.RunModuleWithParameters(RerunConfirmationsTask.__name__, acm.GetDefaultContext())

    @FUxCore.aux_cb
    def Applicable(self):
        """
        Determine whether or not the menu item should be visible
        (shown at all).
        """
        return self._user_has_access()

    @FUxCore.aux_cb
    def Enabled(self):
        """
        Determine whether or not the menu item should be enabled
        (vs greyed-out).
        """
        return self._user_has_access()

    @FUxCore.aux_cb
    def Checked(self):
        """
        Determine whether or not the menu item should be checked
        (have a check mark).
        """
        return False

    @staticmethod
    def _user_has_access():
        """
        Determine whether or not a user should have access to the
        menu item.
        """
        return acm.User().IsAllowed('Rerun Confirmations', 'Application')


@FUxCore.aux_cb
def create_menu_item(extension_object):
    """
    Function used to create and return the menu item.

    This function is referenced from the 'Rerun Operations STP'
    FMenuExtension.
    """
    return MenuItem(extension_object)
