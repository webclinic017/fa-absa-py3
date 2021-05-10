""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/upgrade/FAccountingUpdateAggregatedJournalInfo.py"
import acm

#-------------------------------------------------------------------------
def UpdateJournalInformation(ji, aggregationDate):
    aggregationLevel = ji.AccountingInstruction().AggregationLevel()

    if aggregationLevel == 'Contract Trade Number':
        UpdateContractTradeNumberJournalInfo(ji, aggregationDate)
    elif aggregationLevel == 'Contract Trdnbr and Moneyflow':
        UpdateContractTrdnbrAndMoneyflowJournalInfo(ji, aggregationDate)
    elif aggregationLevel == 'Moneyflow':
        UpdateMoneyflowJournalInfo(ji, aggregationDate)
    else:
        raise Exception('Journal information having aggregation level {} \
could not be updated'.format(aggregationLevel))

#-------------------------------------------------------------------------
def UpdateContractTrdnbrAndMoneyflowJournalInfo(ji, aggregationDate):
    contractTrade = ji.ContractTrade()

    assert contractTrade, 'Contract trade is missing.'

    SetTradeRelatedInfo(ji, contractTrade)

    ji.AggregationDate(aggregationDate)
    ji.MoneyFlowType('None')
    ji.Trade(None)
    ji.CashFlow(None)
    ji.Dividend(None)
    ji.Leg(None)
    ji.CombinationLink(None)
    ji.Payment(None)
    ji.Settlement(None)

#-------------------------------------------------------------------------
def UpdateContractTradeNumberJournalInfo(ji, aggregationDate):
    contractTrade = ji.ContractTrade()

    assert contractTrade, 'Contract trade is missing.'

    SetTradeRelatedInfo(ji, contractTrade)

    ji.AggregationDate(aggregationDate)
    ji.MoneyFlowType('None')
    ji.Trade(None)

#-------------------------------------------------------------------------
def UpdateMoneyflowJournalInfo(ji, aggregationDate):
    trade = ji.Trade()

    assert trade, 'Trade is missing.'

    SetTradeRelatedInfo(ji, trade)

    ji.AggregationDate(aggregationDate)
    ji.MoneyFlowType('None')
    ji.ContractTrade(None)
    ji.CashFlow(None)
    ji.Dividend(None)
    ji.Leg(None)
    ji.CombinationLink(None)
    ji.Payment(None)
    ji.Settlement(None)

#-------------------------------------------------------------------------
def SetTradeRelatedInfo(ji, trade):
    ji.Acquirer(trade.Acquirer())
    ji.Broker(trade.Broker())
    ji.Counterparty(trade.Counterparty())
    ji.Instrument(trade.Instrument())
    ji.Portfolio(trade.Portfolio())



