""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/FAccountingRevaluation.py"
import acm, time

# operations
from FOperationsLoggers import ConsoleLogger

# accounting
from FAccountingEngineRevaluationCreator import CreateRevaluationGenerationEngine

#-------------------------------------------------------------------------
def BookSelection():
    return acm.FBook.Select("")

#-------------------------------------------------------------------------

afterMidnightTT = "Select this check box if the revaluation is started after midnight. The journals will then be created on the previous day."
ael_variables = [['books', 'Books', 'string', BookSelection, None, 1, 1, 'The books to perform revaluation on', None, 1],
                 ['startDate', 'Start Date', 'string', None, acm.Time.DateToday(), 0, 1, 'The date to revaluate journals from', None, 1],
                 ['endDate', 'End Date', 'string', None, acm.Time.DateToday(), 0, 1, 'The date to revaluate journals to', None, 1],
                 ['afterMidnight', 'Revaluation is started after midnight', 'int', [1, 0], 0, 0, 0, afterMidnightTT]]

#-------------------------------------------------------------------------
def ael_main(variablesDict):
    from FAccountingParams import detailedLogging
    books = [acm.FBook[name] for name in variablesDict['books']]
    startDate = acm.Time.AsDate(variablesDict['startDate'])
    endDate = acm.Time.AsDate(variablesDict['endDate'])
    afterMidnight = variablesDict['afterMidnight']

    if not startDate:
        startDate = acm.Time.DateToday()

    if not endDate:
        endDate = acm.Time.DateToday()

    if afterMidnight:
        startDate = acm.Time.DateAddDelta(startDate, 0, 0, -1)
        endDate = acm.Time.DateAddDelta(endDate, 0, 0, -1)

    logger = ConsoleLogger(detailedLogging)
    engine = CreateRevaluationGenerationEngine(logger)

    logger.LP_LogVerbose('Revaluation started at {}.\n'.format(time.ctime()))
    logger.LP_LogVerbose('Generation interval: {} to {}'.format(startDate, endDate))
    logger.LP_Flush()

    engine.Process(startDate, endDate, books)

    logger.LP_LogVerbose('Revaluation finished at {}.\n'.format(time.ctime()))
    logger.LP_Flush()
