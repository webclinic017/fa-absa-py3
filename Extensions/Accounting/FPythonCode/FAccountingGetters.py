""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingGetters.py"
import acm

#-------------------------------------------------------------------------
def GetSourceObjects(trade, ai):
    objs = acm.FList()

    if ai.Type() == 'Trade':
        objs.Add(trade)
    elif ai.Type() == 'Money Flow':
        objs.AddAll(trade.MoneyFlows())
    elif ai.Type() == 'Leg':
        objs.AddAll(trade.LegAndTrades())
    elif ai.Type() == 'Combination':
        objs.AddAll(trade.CombInstrMapAndTrades())

    return objs

#-------------------------------------------------------------------------
def GetBookAndTreatmentLink(info):

    book, treatment, ai = info.Book(), info.Treatment(), info.AccountingInstruction()

    bookLink = book.BookLink(treatment) if book and treatment else None
    treatmentLink = book.TreatmentLink(treatment, ai) if book and treatment and ai else None

    return bookLink, treatmentLink

#-------------------------------------------------------------------------
def GetLinkedAccount(journal):
    linkedJournals = journal.LinkedJournals()
    assert len(linkedJournals) == 1
    return linkedJournals[0].Account()