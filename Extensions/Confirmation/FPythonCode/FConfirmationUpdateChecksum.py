""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/scripts/FConfirmationUpdateChecksum.py"
import acm
import FRunScriptGUI
from FConfirmationChecksum import UpdateConfirmationChecksums


class ConfirmationChecksumUpdateGUI(FRunScriptGUI.AelVariablesHandler):
    def __init__(self):
        variables = self.__CreateAelVariables()
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)


    def __CreateAelVariables(self):
        ttConfirmations = 'Confirmation Selection'
        aelVariables=[['confirmations', 'Confirmations to update', 'FConfirmation', None, ConfirmationChecksumUpdateGUI.CreateConfirmationQuery(), 0, 1, ttConfirmations]]
        return aelVariables



    @staticmethod
    def CreateConfirmationQuery():
        query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
        op = query.AddOpNode('OR')
        op.AddAttrNode('Oid', 'EQUAL', None)
        op2 = query.AddOpNode('OR')
        op2.AddAttrNode('Status', 'EQUAL', None)
        op3 = query.AddOpNode('OR')
        op3.AddAttrNode('Trade.Oid', 'EQUAL', None)
        op4 = query.AddOpNode('OR')
        op4.AddAttrNode('CreateTime', 'EQUAL', None)

        return query


def ael_main(parameters):
    confirmations = parameters["confirmations"]
    acm.Log("-------------------------------------------")
    acm.Log("Started updating confirmation checksums.\n")
    UpdateConfirmationChecksums(confirmations)
    acm.Log("\nFinished updating confirmation checksums.")
    acm.Log("-------------------------------------------")

ael_gui_parameters = {
                      'runButtonLabel' : 'Run',
                      'hideExtraControls' : False,
                      'windowCaption' : 'Confirmation Checksum Update',
                      'version' : '%R%'
                      }

ael_variables = ConfirmationChecksumUpdateGUI()

