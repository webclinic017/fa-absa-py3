""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingQueriesBase.py"

import acm

# accounting
from FAccountingEnums import JournalCategory, JournalType, JournalAggregationLevel, AccountingInstructionType

#-------------------------------------------------------------------------
# Queries used by the accounting base engine
#-------------------------------------------------------------------------
def GetRelatedInsPortAggregatedJournalsQuery(ji):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalInformation.Instrument.Oid', 'EQUAL', ji.Instrument().Oid() if ji.Instrument() else 0)
    query.AddAttrNode('JournalInformation.Portfolio.Oid', 'EQUAL', ji.Portfolio().Oid() if ji.Portfolio() else 0)
    query.AddAttrNode('JournalInformation.Book.Oid', 'EQUAL', ji.Book().Oid() if ji.Book() else 0)
    query.AddAttrNode('JournalInformation.Treatment.Oid', 'EQUAL', ji.Treatment().Oid() if ji.Treatment() else 0)
    query.AddAttrNode('JournalInformation.AccountingInstruction.Oid', 'EQUAL', ji.AccountingInstruction().Oid() if ji.AccountingInstruction() else 0)
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)
    query.AddAttrNode('JournalType', 'NOT_EQUAL', JournalType.SIMULATED)
    return query

#-------------------------------------------------------------------------
def GetRelatedContractTradeAggregatedJournalsQuery(ji):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalInformation.ContractTrade.Oid', 'EQUAL', ji.ContractTrade().Oid() if ji.ContractTrade() else 0)
    query.AddAttrNode('JournalInformation.Book.Oid', 'EQUAL', ji.Book().Oid() if ji.Book() else 0)
    query.AddAttrNode('JournalInformation.Treatment.Oid', 'EQUAL', ji.Treatment().Oid() if ji.Treatment() else 0)
    query.AddAttrNode('JournalInformation.AccountingInstruction.Oid', 'EQUAL', ji.AccountingInstruction().Oid() if ji.AccountingInstruction() else 0)
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)
    query.AddAttrNode('JournalType', 'NOT_EQUAL', JournalType.SIMULATED)
    return query

#-------------------------------------------------------------------------
def GetRelatedContractTradeAndMoneyflowAggregatedJournalsQuery(ji):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalInformation.ContractTrade.Oid', 'EQUAL', ji.ContractTrade().Oid() if ji.ContractTrade() else 0)

    if ji.AggregationDate():
        query.AddAttrNode('JournalInformation.AggregationDate', 'EQUAL', ji.AggregationDate())

    query.AddAttrNode('JournalInformation.Book.Oid', 'EQUAL', ji.Book().Oid() if ji.Book() else 0)
    query.AddAttrNode('JournalInformation.Treatment.Oid', 'EQUAL', ji.Treatment().Oid() if ji.Treatment() else 0)
    query.AddAttrNode('JournalInformation.AccountingInstruction.Oid', 'EQUAL', ji.AccountingInstruction().Oid() if ji.AccountingInstruction() else 0)
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)
    query.AddAttrNode('JournalType', 'NOT_EQUAL', JournalType.SIMULATED)
    return query

#-------------------------------------------------------------------------
def GetRelatedSettlementJournalsQuery(ji):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalInformation.Settlement.Oid', 'EQUAL', ji.Settlement().Oid() if ji.Settlement() else 0)
    query.AddAttrNode('JournalInformation.Book.Oid', 'EQUAL', ji.Book().Oid() if ji.Book() else 0)
    query.AddAttrNode('JournalInformation.Treatment.Oid', 'EQUAL', ji.Treatment().Oid() if ji.Treatment() else 0)
    query.AddAttrNode('JournalInformation.AccountingInstruction.Oid', 'EQUAL', ji.AccountingInstruction().Oid() if ji.AccountingInstruction() else 0)
    query.AddAttrNode('JournalInformation.MoneyFlowType', 'EQUAL', ji.MoneyFlowType())
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)
    query.AddAttrNode('JournalType', 'NOT_EQUAL', JournalType.SIMULATED)
    return query

#-------------------------------------------------------------------------
def GetRelatedTradeJournalsQuery(ji):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalInformation.Trade.Oid', 'EQUAL', ji.Trade().Oid() if ji.Trade() else 0)
    query.AddAttrNode('JournalInformation.Book.Oid', 'EQUAL', ji.Book().Oid() if ji.Book() else 0)
    query.AddAttrNode('JournalInformation.Treatment.Oid', 'EQUAL', ji.Treatment().Oid() if ji.Treatment() else 0)
    query.AddAttrNode('JournalInformation.AccountingInstruction.Oid', 'EQUAL', ji.AccountingInstruction().Oid() if ji.AccountingInstruction() else 0)
    query.AddAttrNode('JournalInformation.MoneyFlowType', 'EQUAL', ji.MoneyFlowType())
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)
    query.AddAttrNode('JournalType', 'NOT_EQUAL', JournalType.SIMULATED)
    return query

#-------------------------------------------------------------------------
def GetRelatedJournalsQuery(ji):
    ai = ji.AccountingInstruction()
    aggLevel = ai.AggregationLevel()

    if ai:
        if aggLevel == JournalAggregationLevel.INSTRUMENT_AND_PORTFOLIO:
            return GetRelatedInsPortAggregatedJournalsQuery(ji)

        elif aggLevel == JournalAggregationLevel.CONTRACT_TRADE_NUMBER:
            return GetRelatedContractTradeAggregatedJournalsQuery(ji)

        elif aggLevel == JournalAggregationLevel.CONTRACT_TRADE_NUMBER_AND_MONEYFLOW:
            return GetRelatedContractTradeAndMoneyflowAggregatedJournalsQuery(ji)

        elif ai.Type() == AccountingInstructionType.SETTLEMENT:
            return GetRelatedSettlementJournalsQuery(ji)

        else:
            return GetRelatedTradeJournalsQuery(ji)

#-------------------------------------------------------------------------
def GetRelatedJournalsForPeriodQuery(ji, startDate, endDate):
    query = GetRelatedJournalsQuery(ji)

    query.AddAttrNode('EventDate', 'GREATER_EQUAL', startDate)
    query.AddAttrNode('EventDate', 'LESS_EQUAL', endDate)

    orNode = query.AddOpNode('OR')

    if ji.Book().OnlyReverseLiveJournals() and ji.AccountingInstruction().IsPeriodic():
        orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.LIVE)
        andNode = orNode.AddOpNode('AND')
        andNode.AddAttrNode("JournalType", 'EQUAL', JournalType.PERIODIC_REVERSED)
        andNode.AddAttrNode("EventDate", 'GREATER_EQUAL', ji.Book().ProcessDate())
    else:
        orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.LIVE)
        orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.PERIODIC_REVERSED)
        orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.REALLOCATION_REVERSED)
    return query

#-------------------------------------------------------------------------
def GetRelatedBeforeDateQuery(ji, date):
    query = GetRelatedJournalsQuery(ji)
    query.AddAttrNode('EventDate', 'LESS', date)

    orNode = query.AddOpNode('OR')
    orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.LIVE)
    orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.PERIODIC_REVERSED)
    orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.REALLOCATION_REVERSED)
    return query

#-------------------------------------------------------------------------
def GetRelatedAfterDateQuery(ji, date):
    query = GetRelatedJournalsQuery(ji)
    query.AddAttrNode('EventDate', 'GREATER', date)

    orNode = query.AddOpNode('OR')
    orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.LIVE)
    orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.PERIODIC_REVERSED)
    orNode.AddAttrNode("JournalType", 'EQUAL', JournalType.REALLOCATION_REVERSED)
    return query

#-------------------------------------------------------------------------
def GetSettlementJournalInfosQuery(ji):
    assert ji.Settlement(), 'ERROR: Journal information {} has no settlement'.format(ji.Oid())

    query = acm.CreateFASQLQuery(acm.FJournalInformation, 'AND')
    query.AddAttrNode('Settlement.Oid', 'EQUAL', ji.Settlement().Oid())
    query.AddAttrNode('AccountingInstruction.Oid', 'EQUAL', ji.AccountingInstruction().Oid())
    return query

#-------------------------------------------------------------------------
def GetInstrumentAndPortfolioJournalInfosQuery(ji):
    assert ji.Instrument(), 'ERROR: Journal information {} has no instrument'.format(ji.Oid())
    assert ji.Portfolio(), 'ERROR: Journal information {} has no portfolio'.format(ji.Oid())

    query = acm.CreateFASQLQuery(acm.FJournalInformation, 'AND')
    query.AddAttrNode('Portfolio.Oid', 'EQUAL', ji.Portfolio().Oid())
    query.AddAttrNode('Instrument.Oid', 'EQUAL', ji.Instrument().Oid())
    query.AddAttrNode('AccountingInstruction.Oid', 'EQUAL', ji.AccountingInstruction().Oid())
    return query

#-------------------------------------------------------------------------
def GetContractTradeNumberJournalInfosQuery(ji):
    assert ji.ContractTrade(), 'ERROR: Journal information {} has no contract trade'.format(ji.Oid())

    query = acm.CreateFASQLQuery(acm.FJournalInformation, 'AND')
    query.AddAttrNode('ContractTrade.Oid', 'EQUAL', ji.ContractTrade().Oid())
    query.AddAttrNode('AccountingInstruction.Oid', 'EQUAL', ji.AccountingInstruction().Oid())
    return query

#-------------------------------------------------------------------------
def GetTradeJournalInfosQuery(ji):
    assert ji.Trade(), 'ERROR: Journal information {} has no trade'.format(ji.Oid())

    query = acm.CreateFASQLQuery(acm.FJournalInformation, 'AND')
    query.AddAttrNode('Trade.Oid', 'EQUAL', ji.Trade().Oid())
    query.AddAttrNode('AccountingInstruction.Oid', 'EQUAL', ji.AccountingInstruction().Oid())
    return query

#-------------------------------------------------------------------------
def GetJournalInfosQuery(ji):
    ai = ji.AccountingInstruction()

    if ai:
        aggLevel = ai.AggregationLevel()

        if ai.Type() == AccountingInstructionType.SETTLEMENT:
            return GetSettlementJournalInfosQuery(ji)

        elif aggLevel == JournalAggregationLevel.INSTRUMENT_AND_PORTFOLIO:
            return GetInstrumentAndPortfolioJournalInfosQuery(ji)

        elif aggLevel == JournalAggregationLevel.CONTRACT_TRADE_NUMBER or \
             aggLevel == JournalAggregationLevel.CONTRACT_TRADE_NUMBER_AND_MONEYFLOW:
            return GetContractTradeNumberJournalInfosQuery(ji)

        else:
            return GetTradeJournalInfosQuery(ji)

#-------------------------------------------------------------------------
# Queries used by the cancellation reverser
#-------------------------------------------------------------------------
def GetLiveSettlementJournalsQuery(obj):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalInformation.Settlement.Oid', 'EQUAL', obj.Oid())
    query.AddAttrNode('JournalType', 'EQUAL', JournalType.LIVE)
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)
    return query

#-------------------------------------------------------------------------
def GetLiveTradeJournalsQuery(obj):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalInformation.Trade.Oid', 'EQUAL', obj.Oid())
    query.AddAttrNode('JournalType', 'EQUAL', JournalType.LIVE)
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)

    andNode = query.AddOpNode('AND')
    andNode.AddAttrNode('JournalInformation.AccountingInstruction.AggregationLevel', 'NOT_EQUAL', JournalAggregationLevel.CONTRACT_TRADE_NUMBER_AND_MONEYFLOW)
    andNode.AddAttrNode('JournalInformation.AccountingInstruction.AggregationLevel', 'NOT_EQUAL', JournalAggregationLevel.CONTRACT_TRADE_NUMBER)
    andNode.AddAttrNode('JournalInformation.AccountingInstruction.AggregationLevel', 'NOT_EQUAL', JournalAggregationLevel.INSTRUMENT_AND_PORTFOLIO)
    return query

#-------------------------------------------------------------------------
def GetLiveJournalsForAggregationLevels(obj, aggregationLevels):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('JournalType', 'EQUAL', JournalType.LIVE)
    query.AddAttrNode('JournalCategory', 'EQUAL', JournalCategory.STANDARD)

    aggNode = query.AddOpNode('OR')

    if JournalAggregationLevel.CONTRACT_TRADE_NUMBER in aggregationLevels:
        andNode = aggNode.AddOpNode('AND')
        andNode.AddAttrNode('JournalInformation.ContractTrade.Oid', 'EQUAL', obj.ContractTrade().Oid())
        andNode.AddAttrNode('JournalInformation.AccountingInstruction.AggregationLevel', 'EQUAL', JournalAggregationLevel.CONTRACT_TRADE_NUMBER)

    if JournalAggregationLevel.CONTRACT_TRADE_NUMBER_AND_MONEYFLOW in aggregationLevels:
        andNode = aggNode.AddOpNode('AND')
        andNode.AddAttrNode('JournalInformation.ContractTrade.Oid', 'EQUAL', obj.ContractTrade().Oid())
        andNode.AddAttrNode('JournalInformation.AccountingInstruction.AggregationLevel', 'EQUAL', JournalAggregationLevel.CONTRACT_TRADE_NUMBER_AND_MONEYFLOW)

    if JournalAggregationLevel.INSTRUMENT_AND_PORTFOLIO in aggregationLevels:
        andNode = aggNode.AddOpNode('AND')
        andNode.AddAttrNode('JournalInformation.Portfolio.Oid', 'EQUAL', obj.Portfolio().Oid())
        andNode.AddAttrNode('JournalInformation.Instrument.Oid', 'EQUAL', obj.Instrument().Oid())
        andNode.AddAttrNode('JournalInformation.AccountingInstruction.AggregationLevel', 'EQUAL', JournalAggregationLevel.INSTRUMENT_AND_PORTFOLIO)

    return query

#-------------------------------------------------------------------------
# Queries used by the incremental base amount processing workflow
#-------------------------------------------------------------------------
def GetPeriodicReversalQuery(journal):
    query = acm.CreateFASQLQuery(acm.FJournal, 'AND')
    query.AddAttrNode('ReversedJournal.Oid', 'EQUAL', journal.Oid())
    query.AddAttrNode("JournalType", 'EQUAL', JournalType.PERIODIC_REVERSAL)

    return query