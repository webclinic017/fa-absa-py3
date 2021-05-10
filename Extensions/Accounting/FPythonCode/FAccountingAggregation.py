""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingAggregation.py"

import acm

# accounting
from FAccountingGetters import GetSourceObjects

#-------------------------------------------------------------------------
def IsPositionCancelled(info):
    book, treatment, ai = info.Book(), info.Treatment(), info.AccountingInstruction()

    bookLink = book.BookLink(treatment) if book and treatment else None
    treatmentLink = book.TreatmentLink(treatment, ai) if book and treatment and ai else None

    assert bookLink and treatmentLink, "Missing booklink or treatmentlink for journal info {}".format(str(info))

    bookMapping = book.BookMappings()[0] if book.BookMappings() else None
    treatmentMapping = bookLink.TreatmentMappings()[0] if bookLink.TreatmentMappings() else None
    accInstrMapping = treatmentLink.AccountingInstructionMappings()[0] if treatmentLink.AccountingInstructionMappings() else None

    for trade in __GetTrades(ai, info):

        if bookMapping and (not bookMapping.Query() or bookMapping.Query().Query().IsSatisfiedBy(trade)):

            if treatmentMapping and (not treatmentMapping.Query() or treatmentMapping.Query().Query().IsSatisfiedBy(trade)):

                for obj in GetSourceObjects(trade, treatmentLink.AccountingInstruction()):

                    if accInstrMapping and (not accInstrMapping.Query() or accInstrMapping.Query().Query().IsSatisfiedBy(obj)):

                        return False
    return True

#-------------------------------------------------------------------------
def __GetTrades(ai, info):

    if ai.AggregationLevel() in ['Contract Trade Number', 'Contract Trdnbr and Moneyflow']:
        return acm.FTrade.Select("contractTrdnbr = {}".format(info.ContractTrade().Oid()))
    else:
        return acm.FTrade.Select("instrument = {} and portfolio = {}".format(info.Instrument().Oid(), info.Portfolio().Oid()))
