"""----------------------------------------------------------------------------------------------------------
MODULE                  :       SettlementRegenerate
PURPOSE                 :       This module will regenerate a settlement.
DEPARTMENT AND DESK     :       IT
REQUASTER               :       Heinrich Cronje
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2011-08-22                      Heinrich Cronje                 Front Arena Upgrade 2010.2.
2019-07-24      FAU-312         Cuen Edwards                    Replaced custom regenerate functionality with
                                                                call to Front Arena command. Added security
                                                                on menu item.
-------------------------------------------------------------------------------------------------------------
"""

import acm
from at_logging import getLogger
import FUxCore


LOGGER = getLogger(__name__)


def _confirm_regenerate(shell, settlements):
    """
    Prompt the user to confirm regeneration of the currently selected
    settlements.
    """
    message = "The command Regenerate will be executed on the "
    if settlements.Size() == 1:
        message += "selected settlement."
    elif settlements.Size() > 1:
        message += "{number} selected settlements.".format(
            number=settlements.Size()
        )
    message += "\n\nDo you want to continue?"
    return acm.UX.Dialogs().MessageBoxYesNo(shell, 'Question', message) == 'Button1'


def _regenerate(settlements):
    """
    Regenerate the specified settlements.
    """
    failures = {}
    for settlement in settlements:
        try:
            command = acm.FRegeneratePayment(settlement)
            command.Execute()
            command.CommitResult()
            LOGGER.info('Regenerated settlement {oid}.'.format(
                oid=settlement.Oid()
            ))
        except Exception as exception:
            failures[settlement] = exception
            LOGGER.warn('Failed to regenerate settlement {oid}.'.format(
                oid=settlement.Oid()
            ))
    return failures


def _display_failures(shell, failures):
    """
    Display a list of settlements that failed to regenerate along
    with the associated exceptions.
    """
    settlements = list(failures.keys())
    settlements.sort(key=lambda s: s.Oid())
    message = "The following settlements failed to regenerate:\n"
    for settlement in settlements:
        message += "\n- {oid} - {exception}".format(
            oid=settlement.Oid(),
            exception=failures[settlement]
        )
    acm.UX.Dialogs().MessageBoxOKCancel(shell, 'Warning', message)


class MenuItem(FUxCore.MenuItem):
    """
    Menu item used to trigger the 'Regenerate Payment' command.
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
        settlements = eii.ExtensionObject()
        if _confirm_regenerate(shell, settlements):
            failures = _regenerate(settlements)
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
        if not acm.User().IsAllowed('Authorise Settlement', 'Operation'):
            return False
        if not acm.User().IsAllowed('Edit Settlements', 'Operation'):
            return False
        if not acm.User().IsAllowed('Regenerate Settlement', 'Operation'):
            return False
        return True


@FUxCore.aux_cb
def create_menu_item(extension_object):
    """
    Function used to create and return the menu item.

    This function is referenced from the 'Regenerate Payment'
    FMenuExtension.
    """
    return MenuItem(extension_object)
