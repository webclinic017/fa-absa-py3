"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    TermStatementAdhocCreatorScript.
    
DESCRIPTION
    This module contains an AEL main script used for the adhoc generation 
    of a term deposit statement for an acquirer and counterparty.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-05-15      FAOPS-127       Cuen Edwards            Elaine Visagie          Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import ael

from at_ael_variables import AelVariableHandler
import DocumentGeneral
import SessionFunctions
import StatementGeneral
from StatementGeneral import Month
from TermStatementConfirmationCreator import TermStatementConfirmationCreator
import TermStatementGeneral


def _period_type_ael_variable_changed(ael_variable):
    """
    Input hook for the 'period_type' AEL variable.
    """
    period_type = ael_variable.value
    month_ael_variable = ael_variables.get('month')
    from_date_ael_variable = ael_variables.get('from_date')
    to_date_ael_variable = ael_variables.get('to_date')
    if period_type == 'Month':
        month_ael_variable.enabled = True
        from_date_ael_variable.enabled = False
        to_date_ael_variable.enabled = False
    else:
        month_ael_variable.enabled = False
        from_date_ael_variable.enabled = True
        to_date_ael_variable.enabled = True


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()
    # Acquirer.    
    ael_variable_handler.add(
        name='acquirer',
        label='Acquirer',
        cls=acm.FInternalDepartment,
        mandatory=True,
        multiple=False,
        alt='The acquirer to generate an adhoc statement for.'
    )
    # Counterparty.
    ael_variable_handler.add(
        name='counterparty',
        label='Counterparty',
        cls=acm.FParty,
        mandatory=True,
        multiple=False,
        alt='The counterparty to generate an adhoc statement for.'
    )
    # Period Type.
    ael_variable_handler.add(
        name='period_type',
        label='Period Type',
        cls='string',
        collection=['Month', 'Custom'],
        default='Month',
        mandatory=True,
        multiple=False,
        alt='The period type to generate generate an adhoc statement for.',
        hook=_period_type_ael_variable_changed
    )
    # Month.
    ael_variable_handler.add(
        name='month',
        label='Month',
        cls='string',
        collection=['Previous'],
        default='Previous',
        mandatory=False,
        multiple=False,
        alt="The month to generate an adhoc statement for.  This can be " +
            "specified as the relative month 'Previous' or as a specific " +
            "month in the form YYYY/MM (e.g. 2018/01)."
    )
    # From Date.
    ael_variable_handler.add(
        name='from_date',
        label='From Date',
        cls='date',
        mandatory=False,
        multiple=False,
        alt="The inclusive from date to generate an adhoc statement for."
    )
    # To Date.
    ael_variable_handler.add(
        name='to_date',
        label='To Date',
        cls='date',
        mandatory=False,
        multiple=False,
        alt="The inclusive to date to generate an adhoc statement for."
    )
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()

ael_gui_parameters = {
    'windowCaption': 'Create Adhoc Term Statement',
    'runButtonLabel': '&&Create',
    'runButtonTooltip': 'Create Adhoc Term Statement',
    'hideExtraControls': True,
    'closeWhenFinished': False
}


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        acquirer = ael_parameters['acquirer']
        counterparty = ael_parameters['counterparty']
        from_date, to_date = _get_date_range(ael_parameters)
        StatementGeneral.validate_statement_date_range(from_date, to_date)
        if _should_create_adhoc_statement(acquirer, counterparty, from_date, to_date):
            TermStatementConfirmationCreator().create_adhoc_statement_confirmation(
                acquirer, counterparty, from_date, to_date)
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)


def _get_date_range(ael_parameters):
    """
    Get the date range to generate an adhoc statement for.
    """
    period_type = ael_parameters['period_type']
    from_date = None
    to_date = None
    if period_type == 'Month':
        month = Month.parse_month(ael_parameters['month'])
        from_date = month.get_first_day_of_month()
        to_date = month.get_last_day_of_month()
    elif period_type == 'Custom':
        if ael_parameters['from_date'] is not None:
            from_date = ael_parameters['from_date'].to_string(ael.DATE_ISO)
        if ael_parameters['to_date'] is not None:
            to_date = ael_parameters['to_date'].to_string(ael.DATE_ISO)
    else:
        raise ValueError("Invalid period type '{period_type}' specified.".format(
            period_type=period_type
        ))
    return (from_date, to_date)


def _should_create_adhoc_statement(acquirer, counterparty, from_date, to_date):
    """
    Determine whether or not to create the adhoc statement.
    """
    existing_statement_confirmations = TermStatementGeneral \
        .get_existing_statement_confirmations(acquirer, counterparty,
        from_date, to_date)
    if len(existing_statement_confirmations) == 0:
        # No statement exists for the same criteria - create.
        return True
    # Existing statements found - ensure user has permission to recreate.
    _ensure_recreate_statement_permitted()
    # Existing statement found and the user has permission to recreate - 
    # prompt the user for confirmation if running in Prime.
    if SessionFunctions.is_prime() and not _confirm_recreate_statement(existing_statement_confirmations):
        return False
    return True


def _ensure_recreate_statement_permitted():
    """
    Ensure that the current user has the necessary access rights to 
    recreate a statement.
    """
    operation_name = StatementGeneral.get_recreate_statement_operation_name()
    if acm.User().IsAllowed(operation_name, 'Operation'):
        return
    error_message = "A term deposit statement for the specified "
    error_message += "criteria already exists and you do not have the "
    error_message += "'{operation_name}' operation."
    raise RuntimeError(error_message.format(
        operation_name=operation_name
    ))


def _confirm_recreate_statement(existing_statement_confirmations):
    """
    Confirm whether or not to create an additional term deposit 
    statement when statement confirmations exist for the same
    criteria.
    """
    message = None
    if len(existing_statement_confirmations) == 1:
        message = "An existing term deposit statement was "
        message += "found for the specified criteria:\n\n"
    else:
        message = "Existing term deposit statements were "
        message += "found for the specified criteria:\n\n"
    for confirmation in existing_statement_confirmations:
        message += "- {oid} (status: '{status}', created: '{created}')\n".format(
            oid=confirmation.Oid(),
            status=confirmation.Status(),
            created=acm.Time.DateTimeFromTime(confirmation.CreateTime())
        )
    message += "\n"
    message += "Are you sure you want to create another one?"
    return DocumentGeneral.show_confirm_dialog('Statement exists', message)


def run_script(extension_invocation_info):
    """
    Function used for executing the script from a menu 
    extension.
    """
    acm.RunModuleWithParameters(__name__, acm.GetDefaultContext())
