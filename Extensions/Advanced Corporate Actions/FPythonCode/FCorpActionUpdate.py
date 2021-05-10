""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionUpdate.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionUpdate - GUI Module to update the old corporate action format into new ones.
     

DESCRIPTION
----------------------------------------------------------------------------"""


"""----------------------------------------------------------------------------
MODULE
    FCorpActionUpdate - GUI Module to update the old corporate action format into new ones.
     

DESCRIPTION
----------------------------------------------------------------------------"""

import FBDPGui
import FBDPCurrentContext
import FBDPCommon
import FCorpActionUpdatePerform

from FBDPCurrentContext import Logme, Summary

corpact_tp = ('The corporate actions to archive.')
ael_variables = FBDPGui.LogVariables(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['CorpActions',
                 'Corporate Actions',
                 'FCorporateAction', None, None,
                 1, 1, corpact_tp, None],
                )


def ael_main(dictionary):

    """
    Main function
    """
    FBDPCurrentContext.CreateLog('Corporate actions update',
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    
    FBDPCommon.execute_script(FCorpActionUpdatePerform.Perform, dictionary)
