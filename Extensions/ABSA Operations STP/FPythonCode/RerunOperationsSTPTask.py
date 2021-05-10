"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    RerunOperationsSTPTask

DESCRIPTION
    This module contains an AEL main script used for re-running Operations
    STP for any eligible entities updated on or after a specified time.

    This task is not intended for normal use and exists only as a support
    tool to be used to resolve any missed STP without replaying AMB messages.

    Examples of situations in which this tool may prove useful are:

    - Recovery after missed processing caused by the Operations STP ATS
      not being restarted after the deployment of a new STP hook.

    - Recovery after failed processing caused by a coding error in an STP
      hook.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-05-22      FAOPS-520       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
2020-06-11      FAOPS-813       Cuen Edwards            Kgomotso Gumbo          Small improvements.
2020-09-06      FAOPS-919       Cuen Edwards            Kgomotso Gumbo          Improvements to allow for specifying the to time, event
                                                                                tables to examine, and the option to exclude touching
                                                                                entities already updated by the current user.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime

import acm

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import FValidation_settings
import OperationsSTPParameters
import SessionFunctions


LOGGER = getLogger(__name__)


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()
    # From Time.
    ael_variable_handler.add(
        name='from_time',
        label='From Time',
        cls='string',
        default=acm.Time.DateToday() + ' 00:00:00',
        mandatory=True,
        multiple=False,
        alt="The time from which to rerun Operations STP. Any eligible entity " +
            "updated on or after this time will be touched in order to trigger " +
            "Operations STP."
    )
    # To Time.
    ael_variable_handler.add(
        name='to_time',
        label='To Time',
        cls='string',
        default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        mandatory=True,
        multiple=False,
        alt="The time up until which to rerun Operations STP. Any eligible entity " +
            "updated on or before this time will be touched in order to trigger" +
            "Operations STP."
    )
    # Event Tables.
    ael_variable_handler.add(
        name='event_table_names',
        label='Event Tables',
        cls='string',
        collection=OperationsSTPParameters.eventTables,
        default=','.join(OperationsSTPParameters.eventTables),
        mandatory=True,
        multiple=True,
        alt="The STP event tables to examine for updates between the from and " +
            "to times. This option allows one to avoid touching unnecessary entities " +
            "when it is known which types of entity need to be touched."
    )
    # Exclude Updates By Current User.
    ael_variable_handler.add_bool(
        name='exclude_updates_by_current_user',
        label='Exclude Updates by Current User',
        default=True,
        mandatory=True,
        multiple=False,
        alt="Prevent touching entities already updated by the current user. This option " +
            "allows one to avoid touching the same entities multiple times in the event " +
            "of multiple executions of this tool."
    )
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()

ael_gui_parameters = {
    'windowCaption': 'Rerun Operations STP',
    'runButtonLabel': '&&Rerun',
    'runButtonTooltip': 'Rerun Operations STP',
    'hideExtraControls': True,
    'closeWhenFinished': False
}


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        start_date_time = datetime.datetime.today()
        LOGGER.info('Starting at {start_date_time}'.format(start_date_time=start_date_time))
        from_time = ael_parameters['from_time']
        to_time = ael_parameters['to_time']
        event_table_names = ael_parameters['event_table_names']
        exclude_updates_by_current_user = ael_parameters['exclude_updates_by_current_user']
        _validate_from_and_to_time(from_time, to_time)
        _validate_running_as_fvalidation_exempt_user()
        _trigger_stp(from_time, to_time, event_table_names, exclude_updates_by_current_user)
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        if SessionFunctions.is_prime():
            _show_error_dialog(exception)
            LOGGER.exception(exception)
        else:
            raise


def _validate_from_and_to_time(from_time, to_time):
    """
    Validate the from_time and to_time AEL parameters.
    """
    # Validate From Time.
    from_datetime = datetime.datetime.strptime(from_time, '%Y-%m-%d %H:%M:%S')
    datetime_today = datetime.datetime.today()
    from_datetime_limit = datetime_today - datetime.timedelta(days=7)
    if from_datetime < from_datetime_limit:
        raise ValueError("The from time may not be earlier than '{from_datetime_limit}'.".format(
            from_datetime_limit=from_datetime_limit
        ))
    if from_datetime > datetime_today:
        raise ValueError("The from time may not be in the future.")
    # Validate To Time.
    to_datetime = datetime.datetime.strptime(to_time, '%Y-%m-%d %H:%M:%S')
    if to_datetime > datetime_today:
        raise ValueError("The to time may not be in the future.")
    if to_datetime <= from_datetime:
        raise ValueError("The to time must after the from time.")


def _validate_running_as_fvalidation_exempt_user():
    """
    Validate that the current user is exempt from FValidation.
    """
    if acm.UserName() not in FValidation_settings.SUPERUSERS:
        # Ensure that tool is run as a user exempt from FValidation
        # in order to avoid GUI pop-ups when touching entities.
        raise ValueError("This tool must be run by a user that is exempt from FValidation.")


def _trigger_stp(from_time, to_time, event_table_names, exclude_updates_by_current_user):
    """
    Trigger STP processing for any eligible objects updated since the
    specified from time and to time.
    """
    entities = _get_entities_updated_between_times(from_time, to_time, event_table_names)
    for entity in entities:
        if exclude_updates_by_current_user and entity.UpdateUser() == acm.User():
            info_message = "{entity_class} {entity_oid}, already updated by the current user "
            info_message += "at '{update_time}', skipping..."
            LOGGER.info(info_message.format(
                entity_class=entity.ClassName(),
                entity_oid=entity.Oid(),
                update_time=acm.Time.DateTimeFromTime(entity.UpdateTime())
            ))
            continue
        if not _entity_triggers_stp(entity):
            info_message = "{entity_class} {entity_oid}, updated '{update_time}', would "
            info_message += "not trigger STP processing, skipping..."
            LOGGER.info(info_message.format(
                entity_class=entity.ClassName(),
                entity_oid=entity.Oid(),
                update_time=acm.Time.DateTimeFromTime(entity.UpdateTime())
            ))
            continue
        info_message = "{entity_class} {entity_oid}, updated '{update_time}', would "
        info_message += "trigger STP processing, touching..."
        LOGGER.info(info_message.format(
            entity_class=entity.ClassName(),
            entity_oid=entity.Oid(),
            update_time=acm.Time.DateTimeFromTime(entity.UpdateTime())
        ))
        try:
            entity.Touch()
            entity.Commit()
        except Exception as exception:
            LOGGER.exception(exception)


def _get_entities_updated_between_times(from_time, to_time, table_names):
    """
    Get any ACM entities updated between the specified from time and
    to time.
    """
    LOGGER.info("Finding entities updated between '{from_time}' and '{to_time}'...".format(
        from_time=from_time,
        to_time=to_time
    ))
    select_expression = "updat_time >= '{from_time}' and updat_time <= '{to_time}'".format(
        from_time=acm.Time.LocalToUtc(from_time),
        to_time=acm.Time.LocalToUtc(to_time)
    )
    updated_entities = acm.FArray()
    for table_name in table_names:
        table = acm.FTable['ADM.{table_name}'.format(
            table_name=table_name
        )]
        entities = table.Select(select_expression).AsArray()
        LOGGER.info("Found {number_of_entities} {table_name} entities updated since '{from_time}'.".format(
            number_of_entities=len(entities),
            table_name=table_name.lower(),
            from_time=from_time
        ))
        updated_entities.AddAll(entities)
    updated_entities.SortByProperty('UpdateTime')
    LOGGER.info("Found {number_of_entities} total entities updated since '{from_time}'.".format(
        number_of_entities=len(updated_entities),
        from_time=from_time
    ))
    return updated_entities


def _entity_triggers_stp(entity):
    """
    Determine whether or not an entity would trigger any STP hooks.
    """
    for stp_hook in OperationsSTPParameters.stpHooks:
        try:
            if stp_hook.IsTriggeredBy(entity):
                return True
        except:
            warning_message = "An exception occurred executing STP hook '{hook_name}'"
            warning_message += ".IsTriggeredBy() for {entity_class} {entity_oid}."
            warning_message = warning_message.format(
                hook_name=stp_hook.Name(),
                entity_class=entity.ClassName(),
                entity_oid=entity.Oid()
            )
            LOGGER.warning(warning_message, exc_info=True)
    return False


def _show_error_dialog(exception):
    """
    Display an error dialog to the user.
    """
    message_box = acm.GetFunction('msgBox', 3)
    ok_button = 0
    error_icon = 16
    message_box('Error', str(exception), ok_button | error_icon)
