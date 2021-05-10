"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    RerunConfirmationsTask

DESCRIPTION
    This module contains an AEL main script used for re-running confirmation
    processing for any eligible entities updated on or after a specified time.

    This task is not intended for normal use and exists only as a support
    tool to be used to resolve any missed processing without replaying AMB
    messages.

    Examples of situations in which this tool may prove useful are:

    - Recovery after missed processing caused by the Confirmation ATS
      not being restarted after the deployment of a new confirmation hook.

    - Recovery after failed processing caused by a coding error in a
      confirmation hook.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-06-18      FAOPS-536       Stuart Wilson           Kgomotso Gumbo          Initial implementation.
2020-06-11      FAOPS-814       Cuen Edwards            Kgomotso Gumbo          Improvements to prevent unnecessary event generation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime

import acm
import FConfirmationMain
from FConfirmationEventFactory import FConfirmationEventFactory
from FConfirmationProcess import GetConfirmationGeneratingObjects

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
import FValidation_settings


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
        alt="The time from which to rerun confirmations processing. Any eligible " +
            "entity updated on or after this time will be touched in order to " +
            "trigger confirmations processing."
    )
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()

ael_gui_parameters = {
    'windowCaption': 'Rerun Confirmations',
    'runButtonLabel': '&&Rerun',
    'runButtonTooltip': 'Rerun Confirmations',
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
        _validate_from_time(from_time)
        #_validate_running_as_fvalidation_exempt_user()
        _trigger_confirmation_processing(from_time)
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        if _is_prime():
            _show_error_dialog(exception)
            LOGGER.exception(exception)
        else:
            raise


def _validate_from_time(from_time):
    """
    Validate the from_time AEL parameter.
    """
    from_datetime = datetime.datetime.strptime(from_time, '%Y-%m-%d %H:%M:%S')
    datetime_today = datetime.datetime.today()
    from_datetime_limit = datetime_today - datetime.timedelta(days=7)
    if from_datetime < from_datetime_limit:
        raise ValueError("The from date may not be earlier than '{from_datetime_limit}'.".format(
            from_datetime_limit=from_datetime_limit
        ))
    if from_datetime > datetime_today:
        raise ValueError("The from date may not be in the future.")


def _validate_running_as_fvalidation_exempt_user():
    """
    Validate that the current user is exempt from FValidation.
    """
    if acm.UserName() not in FValidation_settings.SUPERUSERS:
        # Ensure that tool is run as a user exempt from FValidation
        # in order to avoid GUI pop-ups when touching entities.
        raise ValueError("This tool must be run by a user that is exempt from FValidation.")


def _trigger_confirmation_processing(from_time):
    """
    Trigger confirmation processing for any eligible objects updated
    since the specified from time.
    """
    entities = _get_entities_updated_since_time(from_time)
    for entity in entities:
        if not _entity_triggers_confirmation_processing(entity):
            info_message = "{entity_class} {entity_oid}, updated '{update_time}', would "
            info_message += "not trigger confirmation processing, skipping..."
            LOGGER.info(info_message.format(
                entity_class=entity.ClassName(),
                entity_oid=entity.Oid(),
                update_time=acm.Time.DateTimeFromTime(entity.UpdateTime())
            ))
            continue
        info_message = "{entity_class} {entity_oid}, updated '{update_time}', would "
        info_message += "trigger confirmation processing, touching..."
        LOGGER.info(info_message.format(
            entity_class=entity.ClassName(),
            entity_oid=entity.Oid(),
            update_time=acm.Time.DateTimeFromTime(entity.UpdateTime())
        ))
        entity.Touch()
        entity.Commit()


def _get_entities_updated_since_time(from_time):
    """
    Get any ACM entities updated since the specified time.
    """
    datetime_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    LOGGER.info("Finding entities updated since '{from_time}'...".format(
        from_time=from_time
    ))
    select_expression = "updat_time >= '{from_time}' and updat_time <= '{to_time}'".format(
        from_time=acm.Time.LocalToUtc(from_time),
        to_time=datetime_now
    )
    updated_entities = acm.FArray()
    for table_name in ['OPERATIONSDOCUMENT']:
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


def _entity_triggers_confirmation_processing(entity):
    """
    Determine whether or not an entity would trigger any confirmation
    processing.
    """
    if entity.IsKindOf(acm.FOperationsDocument):
        return True
    if entity.IsKindOf(acm.FParty):
        return True
    trades = GetConfirmationGeneratingObjects(entity)
    confirmation_events = FConfirmationEventFactory.GetConfirmationEvents()
    for trade in trades:
        for confirmation_event in confirmation_events:
            if confirmation_event.baseRule.IsSatisfiedBy(trade):
                return True
    return False


def _is_prime():
    """
    Determine whether or not the current session is executing via
    Prime.
    """
    return str(acm.Class()) == 'FTmServer'


def _show_error_dialog(exception):
    """
    Display an error dialog to the user.
    """
    message_box = acm.GetFunction('msgBox', 3)
    ok_button = 0
    error_icon = 16
    message_box('Error', str(exception), ok_button | error_icon)
