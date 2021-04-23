""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/BDP/FCloseOpenSecurityLoan.py"
"""----------------------------------------------------------------------------
MODULE
    FCloseOpenSecurityLoan - Close and open security Loans

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm

import FBDPGui
import importlib
importlib.reload(FBDPGui)

ScriptName = "FCloseOpenSecurityLoan"

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FCloseOpenSecurityLoan')

ttSecLoans = "The security loans to close and open."
ttDate = ('Specify the close and open date. Trades will be created with this trade time')
ttUnderlying = "The new underlying."
ttDivFactor = "The new dividend factor."
ttLoanRate = "The new loan rate."

days = [acm.Time.DateToday(),
            'Today']


class FCloseOpenSecurityLoanVariables(FBDPGui.TestVariables):

    def __init__(self, *ael_variables):           
        
        # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
        self.createVariable(
                ['Trades',
                        'Security Loan Trades',
                        'FTrade', None, None,
                        0, 1, ttSecLoans, None])
        self.createVariable(
                ['date',
                'Close/Open Date',
                'string', days, 'Today',
                1, 0, ttDate])
        self.createVariable(
                ['Underlying',
                        'New Underlying',
                        'FStock', None, None,
                        0, 1, ttSecLoans, None])
        self.createVariable(
                ['DivFactor',
                        'New Dividend Factor',
                        'string', None, None,
                        0, 1, ttDivFactor, None])
        self.createVariable(
                ['LoanRate',
                        'New Loan Rate',
                        'string', None, None,
                        0, 1, ttLoanRate, None])
        FBDPGui.TestVariables.__init__(self, *ael_variables)


ael_variables = FCloseOpenSecurityLoanVariables()


def ael_main(dictionary):
    #Import Front modules
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPCurrentContext
    import FCloseOpenSecurityLoanPerform

    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    FBDPCommon.execute_script(FCloseOpenSecurityLoanPerform.perform,
                              dictionary)

