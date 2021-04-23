""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FCorpActionApproval.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FCorpActionApproval - GUI Module to approve a corporate action 

DESCRIPTION
----------------------------------------------------------------------------"""


import acm
import FBDPGui
import FBDPCurrentContext
import importlib

cvCorpact = [acmCA.Name() for acmCA in acm.FCorporateAction.Select('status=pending')] + ['']

corpact_tp = ('The corporate action that needs to be approved.')
ael_variables = FBDPGui.LogVariables(
				# [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['CorpAction',
                 'CorpAction',
                 'string', cvCorpact, None,
                 1, 1, corpact_tp, None])

def ael_main(dictionary):

    """
    Main function
    """
    import FBDPCommon
    importlib.reload(FBDPCommon)
    
    FBDPCurrentContext.CreateLog('Corporate action Approval',
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    
    import FCAApproval
    importlib.reload(FCAApproval)
    
    dictionary['ScriptName'] = 'Corporate action Approval'
    FBDPCommon.execute_script(FCAApproval.perform, dictionary)
