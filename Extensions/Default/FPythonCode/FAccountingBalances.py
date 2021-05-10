""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/FAccountingBalances.py"
import acm, time

# operations
from FOperationsLoggers import ConsoleLogger

# accounting
from FAccountingEngineBalanceCreator import CreateBalanceGenerationEngine

#-------------------------------------------------------------------------
def BookSelection():
    return acm.FBook.Select("")

#-------------------------------------------------------------------------
afterMidnightTT = "Select this check box if the balances job is started after midnight. The journals will then be created on the previous day."
ael_variables = [['books', 'Books', 'string', BookSelection, None, 1, 1, 'The books to generate balances for', None, 1],
                 ['generationDate', 'Generation Date', 'string', None, acm.Time.DateToday(), 0, 1, 'The date to generate balances for', None, 1],
                 ['afterMidnight', 'Balances is started after midnight', 'int', [1, 0], 0, 0, 0, afterMidnightTT]]

#-------------------------------------------------------------------------
def ael_main(variablesDict):
    from FAccountingParams import detailedLogging
    books = [acm.FBook[name] for name in variablesDict['books']]
    date = acm.Time.AsDate(variablesDict['generationDate'])

    if not date:
        date = acm.Time.DateToday()

    if variablesDict['afterMidnight']:
        date = acm.Time.DateAddDelta(date, 0, 0, -1)

    logger = ConsoleLogger(detailedLogging)
    engine = CreateBalanceGenerationEngine(logger)

    logger.LP_LogVerbose('Balance generation started at {}.\n'.format(time.ctime()))
    logger.LP_LogVerbose('Generation date: {}'.format(date))
    logger.LP_Flush()

    engine.Process(date, books)

    logger.LP_LogVerbose('Balance generation finished at {}.\n'.format(time.ctime()))
    logger.LP_Flush()
