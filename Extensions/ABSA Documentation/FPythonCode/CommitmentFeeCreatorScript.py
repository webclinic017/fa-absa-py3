"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    CommitmentFeeCreatorScript

DESCRIPTION
    This is the task file used to created Commitment Fee Invoices
-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-05      FAOPS-530       Joash Moodley                      Initial Implementation.

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm

from at_ael_variables import AelVariableHandler
from LoanOpsCommitmentFeeCreator import LoanOpsCommitmentFeeCreator as creator


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()  
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()

ael_gui_parameters = {
    'windowCaption': 'Create Commitment Fee Invoice',
    'runButtonLabel': '&&Create',
    'runButtonTooltip': 'Create Commitment Fee Invoice',
    'hideExtraControls': True,
    'closeWhenFinished': False
}


def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        today = acm.Time().DateToday()
        trades = acm.FStoredASQLQuery['Loan Ops Commitment Fee Invoice Trades Today'].Query().Select()
        for trade in trades:
            has_conf_instruction = False
            counterparty = trade.Counterparty()

            for instruction  in counterparty.ConfInstructions():
                if instruction.Name() == 'Curr Loan Ops Commitment Fee Email':
                    has_conf_instruction = True
                    break
            if has_conf_instruction:
                print(trade.Oid())
                invoice = creator('Loan Ops Commitment Fee', trade, today)
                invoice.create_commitment_fee_invoice()

    except Exception as exception:
        print(exception)


def run_script(extension_invocation_info):
    """
    Function used for executing the script from a menu 
    extension.
    """
    acm.RunModuleWithParameters(__name__, acm.GetDefaultContext())
