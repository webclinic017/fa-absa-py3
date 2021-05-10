""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/upgrade/FAccountingUpgradeBalances.py"
import acm, time

# operations
from FOperationsResultCounter import ResultCounter
from FOperationsTransactionCommitter import TransactionCommitter
from FOperationsLoggers import ConsoleLogger

# accounting
from FAccountingOperations import Operation, GetOperations, GetOpForObject
from FAccountingQueries import GetJournalsForBalanceQuery
from FAccountingEnums import JournalCategory, JournalType, AccountingPeriodType

#-------------------------------------------------------------------------------
def GetNonSOFYBalances():
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.BALANCE)
    query.AddAttrNode('JournalType', 'NOT_EQUAL', JournalType.SIMULATED)
    query.AddAttrNode('AccountingPeriod.Type', 'NOT_EQUAL', AccountingPeriodType.START_OF_FISCAL_YEAR)

    return query.Select()

#-------------------------------------------------------------------------------
def GetLatestValueDateAmongJournals(balance):
    journalsForBalance = GetJournalsForBalanceQuery(balance).Select()
    journalsForBalance.SortByProperty('ValueDate', False)

    return journalsForBalance[0].ValueDate() if journalsForBalance else ''

#-------------------------------------------------------------------------
ael_variables = []

#-------------------------------------------------------------------------
def ael_main(params):
    logger = ConsoleLogger(True)

    logger.LP_Log('INFO: FAccountingUpgradeBalances started at {} \n'.format(time.ctime()))
    logger.LP_Flush()

    committer = TransactionCommitter(GetOperations(), ResultCounter)
    committer.PO_Init(logger)

    balances = GetNonSOFYBalances()
    transactionList = list()
    result = ResultCounter()
    dateToday = acm.Time.DateToday()
    for balance in balances:
        balanceClone = None
        if not balance.ValueDate():
            balanceClone = balance.Clone()
            latestDate = GetLatestValueDateAmongJournals(balanceClone)
            balanceClone.ValueDate(latestDate)
            balanceClone.EventDate(latestDate)
            balanceClone.ProcessDate(dateToday)

            transactionList.append((GetOpForObject(balanceClone), balanceClone))

        if len(transactionList) >= 100:
            result.RE_Accumulate(committer.CO_Commit(transactionList))
            del transactionList[:]

            logger.LP_Log('{} Balances updated so far...'.format(result.RE_ResultOpAndObjectType(Operation.UPDATE, 'FJournal')))
            logger.LP_Flush()

    result.RE_Accumulate(committer.CO_Commit(transactionList))

    logger.LP_Log('{} Balances updated'.format(result.RE_ResultOpAndObjectType(Operation.UPDATE, 'FJournal')))
    logger.LP_Log('INFO: FAccountingUpgradeBalances ended at {}'.format(time.ctime()))
    logger.LP_Flush()