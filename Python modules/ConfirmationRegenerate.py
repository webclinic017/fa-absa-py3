"""----------------------------------------------------------------------------------------------------------
MODULE                  :       ConfirmationRegenerate
PURPOSE                 :       This module will regenerate a confirmation.
DEPARTMENT AND DESK     :       IT
REQUASTER               :       Heinrich Cronje
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       245285
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-06-08      245285          Heinrich Cronje                 Change function to use the confirmation engine
                                                                to regenerate the confirmation.
2019-07-24      FAU-312         Cuen Edwards                    Replaced custom regenerate functionality with
                                                                call to Front Arena command. Added security
                                                                on menu item.
-------------------------------------------------------------------------------------------------------------
"""

import acm
from at_logging import getLogger
import FUxCore


LOGGER = getLogger(__name__)


def _confirm_regenerate(shell, confirmations):
    """
    Prompt the user to confirm regeneration of the currently selected
    confirmations.
    """
    message = "The command Regenerate will be executed on the "
    if confirmations.Size() == 1:
        message += "selected confirmation."
    elif confirmations.Size() > 1:
        message += "{number} selected confirmations.".format(
            number=confirmations.Size()
        )
    message += "\n\nDo you want to continue?"
    return acm.UX.Dialogs().MessageBoxYesNo(shell, 'Question', message) == 'Button1'


def _regenerate(confirmations):
    """
    Regenerate the specified confirmations.
    """
    failures = {}
    for confirmation in confirmations:
        try:
            command = acm.FRegenerateConfirmation([confirmation])
            command.Execute()
            command.CommitResult()
            LOGGER.info('Regenerated confirmation {oid}.'.format(
                oid=confirmation.Oid()
            ))
        except Exception as exception:
            failures[confirmation] = exception
            LOGGER.warn('Failed to regenerate confirmation {oid}.'.format(
                oid=confirmation.Oid()
            ))
    return failures


def _display_failures(shell, failures):
    """
    Display a list of confirmations that failed to regenerate along
    with the associated exceptions.
    """
    confirmations = list(failures.keys())
    confirmations.sort(key=lambda c: c.Oid())
    message = "The following confirmations failed to regenerate:\n"
    for confirmation in confirmations:
        message += "\n- {oid} - {exception}".format(
            oid=confirmation.Oid(),
            exception=failures[confirmation]
        )
    acm.UX.Dialogs().MessageBoxOKCancel(shell, 'Warning', message)


class MenuItem(FUxCore.MenuItem):
    """
    Menu item used to trigger the 'Regenerate Confirmation' command.
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
        shell = eii.Parameter('shell')
        confirmations = eii.ExtensionObject()
        if _confirm_regenerate(shell, confirmations):
            failures = _regenerate(confirmations)
            if len(failures) > 0:
                _display_failures(shell, failures)

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
        return acm.User().IsAllowed('Regenerate Confirmation', 'Operation')


@FUxCore.aux_cb
def create_menu_item(extension_object):
    """
    Function used to create and return the menu item.

    This function is referenced from the 'Regenerate Confirmation'
    FMenuExtension.
    """
    return MenuItem(extension_object)
