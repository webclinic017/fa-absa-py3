"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    FCommonObjectFunctions.

DESCRIPTION
    This module contains functions relating to Front Arena objects of type
    FCommonObject.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-11-05                      Cuen Edwards                                    Initial Implementation.
2020-02-27      FAOPS-760       Cuen Edwards                                    Addition of Touch functionality.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
from at_logging import getLogger


LOGGER = getLogger(__name__)


def get_create_day(common_object):
    """
    Get the day on which an FCommonObject was created as an ACM date
    string.
    """
    return acm.Time.DateFromTime(common_object.CreateTime())


def get_update_day(common_object):
    """
    Get the day on which an FCommonObject was last updated as an ACM
    date string.
    """
    return acm.Time.DateFromTime(common_object.UpdateTime())


def touch_menu_function(eii):
    """
    Function used for touching currently selected objects from the
    'Touch' FMenuExtension.
    """
    shell = eii.Parameter('shell')
    common_objects = eii.ExtensionObject()
    if _confirm_touch(shell, common_objects):
        failures = _touch(common_objects)
        if len(failures) > 0:
            _display_failures(shell, failures)


def _confirm_touch(shell, common_objects):
    """
    Prompt the user to confirm the touching of the currently selected
    common objects.
    """
    message = "The "
    if common_objects.Size() == 1:
        message += "selected object"
    elif common_objects.Size() > 1:
        message += "{number} selected objects".format(
            number=common_objects.Size()
        )
    message += " will be touched.  This will result in the update time"
    message += " and user changing."
    message += "\n\nDo you want to continue?"
    return acm.UX.Dialogs().MessageBoxYesNo(shell, 'Question', message) == 'Button1'


def _touch(common_objects):
    """
    Touch and commit the specified common objects.

    This is useful for re-triggering event-driven functionality for
    any missed events.
    """
    failures = {}
    for common_object in common_objects:
        try:
            common_object.Touch()
            common_object.Commit()
            LOGGER.info('Touched {object_class} {oid}.'.format(
                object_class=common_object.ClassName(),
                oid=common_object.Oid()
            ))
        except Exception as exception:
            failures[common_object] = exception
            LOGGER.warn('Failed to touch {object_class} {oid}.'.format(
                object_class=common_object.ClassName(),
                oid=common_object.Oid()
            ))
    return failures


def _display_failures(shell, failures):
    """
    Display a list of common objects that were not successfully
    touched along with the associated exceptions.
    """
    common_objects = list(failures.keys())
    common_objects.sort(key=lambda c: c.Oid())
    message = "An error occurred touching the following objects:\n"
    for common_object in common_objects:
        message += "\n- {object_class} {oid} - {exception}".format(
            object_class=common_object.ClassName(),
            oid=common_object.Oid(),
            exception=failures[common_object]
        )
    acm.UX.Dialogs().MessageBoxOKCancel(shell, 'Warning', message)
