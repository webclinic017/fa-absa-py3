"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PreSettlementAdviceAdhocCreatorScript

DESCRIPTION
    This module contains an AEL main script used for the adhoc generation
    of a pre-settlement advice for a counterparty and instrument type.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import ael

from at_ael_variables import AelVariableHandler
import DocumentGeneral
from PreSettlementAdviceBusinessProcessCreator import PreSettlementAdviceBusinessProcessCreator
import PreSettlementAdviceGeneral


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()
    # Counterparty.
    ael_variable_handler.add(
        name='counterparty',
        label='Counterparty',
        cls=acm.FParty,
        mandatory=True,
        multiple=False,
        alt='The counterparty to generate an adhoc pre-settlement advice for.'
    )
    # Instrument Type.
    ael_variable_handler.add(
        name='instrument_type',
        label='Instrument Type',
        cls='string',
        collection=PreSettlementAdviceGeneral.get_supported_advice_instrument_types(),
        default='Swap',
        mandatory=True,
        multiple=False,
        alt='The instrument type to generate an adhoc pre-settlement advice for.'
    )
    # From Date.
    ael_variable_handler.add(
        name='from_date',
        label='From Date',
        cls='date',
        mandatory=True,
        multiple=False,
        alt="The inclusive from date to generate an adhoc pre-settlement advice for."
    )
    # To Date.
    ael_variable_handler.add(
        name='to_date',
        label='To Date',
        cls='date',
        mandatory=True,
        multiple=False,
        alt="The inclusive to date to generate an adhoc pre-settlement advice for."
    )
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()

ael_gui_parameters = {
    'windowCaption': 'Create Adhoc Pre-settlement Advice',
    'runButtonLabel': '&&Create',
    'runButtonTooltip': 'Create Adhoc Pre-settlement Advice',
    'hideExtraControls': True,
    'closeWhenFinished': False
}


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        counterparty = ael_parameters['counterparty']
        instrument_type = ael_parameters['instrument_type']
        from_date = ael_parameters['from_date'].to_string(ael.DATE_ISO)
        to_date = ael_parameters['to_date'].to_string(ael.DATE_ISO)
        PreSettlementAdviceGeneral.validate_advice_date_range(from_date, to_date)
        _ensure_advice_does_not_exist(counterparty, instrument_type, from_date, to_date)
        PreSettlementAdviceBusinessProcessCreator().create_adhoc_advice_business_process(counterparty,
            instrument_type, from_date, to_date)
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)


def _ensure_advice_does_not_exist(counterparty, instrument_type, from_date, to_date):
    """
    Ensure that a pre-settlement advice does not already exist for
    the same criteria.
    """
    if PreSettlementAdviceGeneral.advice_business_process_exists(counterparty, instrument_type, from_date, to_date):
        raise RuntimeError("A pre-settlement advice for the specified criteria already exists.")


def run_script(extension_invocation_info):
    """
    Function used for executing the script from a menu
    extension.
    """
    acm.RunModuleWithParameters(__name__, acm.GetDefaultContext())
