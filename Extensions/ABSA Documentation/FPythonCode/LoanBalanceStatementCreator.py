"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    LoanBalanceStatementCreator.

DESCRIPTION
    This module contains an AEL main script used for the generation of loan
    facility balance statements for counterparties
-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-05-15      FAOPS-513       Stuart Wilson           Kershia Perumal         Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_ael_variables import AelVariableHandler
import DocumentConfirmationGeneral
import DocumentGeneral
from LoanBalanceStatementConfirmationCreator import LoanBalanceStatementConfirmationCreator
import StatementGeneral
from StatementGeneral import Month


ACQUIRER = acm.FParty['PRIMARY MARKETS']
EVENT = 'Loan Balance Statement'


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()
    # Acquirer.

    # Counterparty.
    ael_variable_handler.add(
        name='counterparty',
        label='Counterparty',
        cls=acm.FParty,
        mandatory=True,
        multiple=False,
        alt='The counterparty to generate an adhoc statement for.'
    )

    # From Date.
    ael_variable_handler.add(
        name='from_month',
        label='From Month',
        cls='string',
        mandatory=False,
        multiple=False,
        alt="The inclusive from month to generate a balance statement for. This can be " +
            "specified as the relative month 'Previous' or as a specific " +
            "month in the form YYYY/MM (e.g. 2018/01)."
    )
    # To Date.
    ael_variable_handler.add(
        name='to_month',
        label='To Month',
        cls='string',
        mandatory=False,
        multiple=False,
        alt="The inclusive to month to generate a balance statement for. This can be " +
            "specified as the relative month 'Previous' or as a specific " +
            "month in the form YYYY/MM (e.g. 2018/01)."
    )
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()

ael_gui_parameters = {
    'windowCaption': 'Create Loan Facility Statement',
    'runButtonLabel': '&&Create',
    'runButtonTooltip': 'Create Loan Facility Statement',
    'hideExtraControls': True,
    'closeWhenFinished': False
}

def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        counterparty = ael_parameters['counterparty']
        from_date, to_date = _get_date_range(ael_parameters)
        StatementGeneral.validate_statement_date_range(from_date, to_date)
        if _should_create_balance_statement(counterparty, from_date, to_date):
            LoanBalanceStatementConfirmationCreator().create_adhoc_statement_confirmation(
                ACQUIRER, counterparty, from_date, to_date)
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)


def _get_date_range(ael_parameters):
    """
    Get the date range to generate an adhoc statement for.
    """
    from_month = Month.parse_month(ael_parameters['from_month'])
    to_month = Month.parse_month(ael_parameters['to_month'])
    from_date = from_month.get_first_day_of_month()
    to_date = to_month.get_last_day_of_month()

    return from_date, to_date


def _should_create_balance_statement(counterparty, from_date, to_date):
    """
    Determine whether or not to create the adhoc statement.
    """
    existing_balance_statement_confirmations = DocumentConfirmationGeneral.get_existing_document_confirmations(
        EVENT, ACQUIRER, counterparty, from_date, to_date)
    if len(existing_balance_statement_confirmations) == 0:
        # No statement exists for the same criteria - create.
        return True
    # Existing statements found - ensure user has permission to recreate.
    else:
        if len(existing_balance_statement_confirmations) == 1:
            message = "An existing loan balance statement was "
            message += "found for the specified criteria:\n\n"
        else:
            message = "Existing loan balance statements were "
            message += "found for the specified criteria:\n\n"
        for confirmation in existing_balance_statement_confirmations:
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

