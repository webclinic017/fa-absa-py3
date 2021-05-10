"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    SARBSecurityTransferInstructionCreatorScript

DESCRIPTION
    This module contains an AEL main script used for the generation of a SARB
    security transfer instructions.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-05-04      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

import DocumentGeneral
from SARBSecurityTransferInstructionBusinessProcessCreator import SARBSecurityTransferInstructionBusinessProcessCreator


ael_variables = []

ael_gui_parameters = {
    'windowCaption': 'Create SARB Security Transfer Instructions',
    'runButtonLabel': '&&Create',
    'runButtonTooltip': 'Create SARB Security Transfer Instructions',
    'hideExtraControls': True,
    'closeWhenFinished': False
}


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        SARBSecurityTransferInstructionBusinessProcessCreator().create_instruction_business_processes()
    except Exception as exception:
        DocumentGeneral.handle_script_exception(exception)


def run_script(extension_invocation_info):
    """
    Function used for executing the script from a menu
    extension.
    """
    acm.RunModuleWithParameters(__name__, acm.GetDefaultContext())
