""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionArchive.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionArchive - GUI Module to archive corporate actions.
     

DESCRIPTION
----------------------------------------------------------------------------"""


import acm
import FBDPGui
import FBDPCurrentContext
import FBDPCommon
import FCorpActionPerformArchiving

beforedate_tp = ("The ExDate or Record Date of the corpation actions to archive must be before this date. ")
dividendEstimate_tp = ("Also archive the dividend estimates imported with the corporate action.")
corpact_tp = ('The selected corporate actions to archive.')
ael_variables = FBDPGui.TestVariables(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['CorpActions',
                 'Corporate Actions',
                 'FCorporateAction', None, None,
                 1, 1, corpact_tp, None],
                ['BeforeDate',
                'Before Date',
                'string', [acm.Time.DateToday(), 'Today'], 'Today',
                1, None, beforedate_tp],
                ['IncludeDividendEstimate',
                'Include Dividend Estimates',
                'int', ['0', '1'], None,
                None, None, dividendEstimate_tp]
                )


def ael_main(dictionary):

    """
    Main function
    """    
    FBDPCurrentContext.CreateLog('Corporate actions archiving',
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])
    
    FBDPCommon.execute_script(FCorpActionPerformArchiving.PerformCorpActionsArchiving, dictionary)
