""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/FAccountingEOFY.py"
import acm, time

# operations
from FOperationsLoggers import ConsoleLogger

# accounting
from FAccountingEngineEOFYCreator import CreateEOFYGenerationEngine

from FAccountingParams import detailedLogging

#-------------------------------------------------------------------------
def GetFiscalYears():
    accountingPeriods = acm.FAccountingPeriod.Select("")

    fiscalYears = {accountingPeriod.FiscalYear() for accountingPeriod in accountingPeriods}
    fiscalYears = list(fiscalYears)
    fiscalYears.sort(reverse=True)

    return fiscalYears

#-------------------------------------------------------------------------
ael_variables = [['books', 'Books', 'string', acm.FBook.Select(""), None, 1, 1, 'The books to run the end of fiscal year process for.', None, 1],
                ['fiscalYear', 'Fiscal Year', 'int', GetFiscalYears(), None, 1, 0, 'The Fiscal Year to run the end of fiscal year process for.', None, 1]]

#-------------------------------------------------------------------------
def ael_main(variablesDict):
    books = [acm.FBook[name] for name in variablesDict['books']]
    fiscalYear = variablesDict['fiscalYear']

    logger = ConsoleLogger(detailedLogging)

    if fiscalYear in GetFiscalYears():
        engine = CreateEOFYGenerationEngine(fiscalYear, logger)

        logger.LP_LogVerbose('End of fiscal year process started at {}'.format(time.ctime()))
        logger.LP_Flush()

        engine.Process(fiscalYear, books)

        logger.LP_LogVerbose('End of fiscal year process ended at {}'.format(time.ctime()))
        logger.LP_Flush()
    else:
        logger.LP_LogVerbose('End of fiscal year process was not run. There are no accounting periods having fiscal year {}.'.formatfiscalYear)
        logger.LP_Flush()
        