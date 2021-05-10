""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingTransporterDelete.py"

import acm
import time
import FRunScriptGUI
import FAccountingTransporter
from FBDPCurrentContext import Logme, CreateLog


class OperationsDeleteGUI(FRunScriptGUI.AelVariablesHandler):

    def __init__(self):

        ttLogToCon = ('Whether logging should be done in the Log Console or not.')
        ttLogToFile = 'Defines whether logging should be done to file.'
        ttLogFile = ('Name of the logfile. Could include the whole path, c:\temp\...')

        variables = [
                     ['book', 'Book name(s)', 'string', list(acm.FBook.Select('')), None, 0, 1, 'Select Book', None, True],
                     ['treatment', 'Treatment name(s)', 'string', list(acm.FTreatment.Select('')), None, 0, 1, 'Select Treatment', None, True],
                     ['accountinginstruction', 'Accounting Instruction name(s)', 'string', list(acm.FAccountingInstruction.Select('')), None, 0, 1, 'Select Accounting Instruction', None, True],
                     ['LogToConsole', 'Log to console_Logging', 'int', [1, 0], 1, 1, 0, ttLogToCon],
                     ['LogToFile', 'Log to file_Logging', 'int', [1, 0], 0, 1, 0, ttLogToFile, self.__OnLogToFile],
                     ['Logfile', 'Log file_Logging', 'string', None, 'AccountingDelete.log', 0, 0, ttLogFile, None, None]
                    ]

        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)

    def __OnLogToFile(self, index, fieldValues):
        self.Logfile.enable(fieldValues[index], 'You have to check Log To File to be able to select a Logfile.')
        return fieldValues

def ael_main(params):

    title = 'Accounting Delete'

    CreateLog(title, 1, params['LogToConsole'], params['LogToFile'], params['Logfile'], 0, "", "")

    Logme()('%s started by user %s at %s' % (title, str(acm.UserName()), time.ctime()))
    Logme()('')

    for bookName in params['book']:
        book = acm.FBook[bookName]
        if book:
            FAccountingTransporter.DeleteBook(book)

    for treatmentName in params['treatment']:
        treatment = acm.FTreatment[treatmentName]
        if treatment:
            FAccountingTransporter.DeleteTreatment(treatment)

    for accountingInstructionName in params['accountinginstruction']:
        accountingInstruction = acm.FAccountingInstruction[accountingInstructionName]
        if accountingInstruction:
            FAccountingTransporter.DeleteAccountingInstruction(accountingInstruction)

    Logme()('')
    Logme()('%s finished at %s.' % (title, time.ctime()))

ael_gui_parameters = {
                      'runButtonLabel':   'Delete',
                      'hideExtraControls': True,
                      'windowCaption' : 'Accounting Transporter Delete',
                      'version' : '%R%'
                      }

ael_variables = OperationsDeleteGUI()
