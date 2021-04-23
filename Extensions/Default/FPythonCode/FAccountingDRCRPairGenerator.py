""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingDRCRPairGenerator.py"

import acm

# itertools
from itertools import groupby

# accounting
from FAccountingEnums import ReallocationStatus
from FAccountingSuspenseGenerator import GenerateSuspense

#-------------------------------------------------------------------------
# Default exception callback
#-------------------------------------------------------------------------
def __DefaultExceptionCb(exception, *_):
    raise exception

#-------------------------------------------------------------------------
# Generator for generating the DR/CR pairs
#-------------------------------------------------------------------------
def GenerateDRCRPairs(journals, genLink=False, revSort=False, filterFunc=None, exceptionCb=__DefaultExceptionCb):

    for keyTup, journals in groupby(sorted(journals, key=__Sort, reverse=revSort), key=__Sort):

        journalList = [j for j in journals if (filterFunc(j) if filterFunc else True)]

        try:
            yield __DebitCreditPair(journalList, keyTup, genLink)
        except AssertionError as e:
            exceptionCb(e, journalList, keyTup)

#-------------------------------------------------------------------------
def __ReallocSortValue(journal):
    if journal.ReallocationStatus() == ReallocationStatus.NONE:
        return 0
    elif journal.ReallocationStatus() == ReallocationStatus.TO_BE_REALLOCATED:
        return 1
    elif journal.ReallocationStatus() == ReallocationStatus.REALLOCATED:
        return 2

#-------------------------------------------------------------------------
def __Sort(journal):
    reallocVal = __ReallocSortValue(journal)
    return (journal.EventDate(), journal.Currency(), reallocVal, journal.JournalLink(), journal.JournalInformation())

#-------------------------------------------------------------------------
# Validation methods for
#-------------------------------------------------------------------------
def AssertUniqueKey(key, journals):
    assert (key in journals) == False, \
        "A journal in the debit/credit pair has the same key ({}) as another journal".format(key)

#-------------------------------------------------------------------------
def AssertSameJournalLink(journals, journalLink):
    assert all(j.JournalLink().Oid() == journalLink.Oid() for j in journals), \
        "All journals in the debit/credit pair does not have the same journal link"

#-------------------------------------------------------------------------
def AssertCompletePair(journals, journalLink):
    assert len(journals) >= journalLink.Journals().Size(), \
        "The debit/credit pair does not contain all journals with the same journal link"

#-------------------------------------------------------------------------
def AssertValidPair(journals, journalLink):

    if journalLink:
        AssertSameJournalLink(journals, journalLink)

        if journalLink.Journals().Size() > 0:
            AssertCompletePair(journals, journalLink)

#-------------------------------------------------------------------------
# Private class, not allowed to create any pairs except via the generator
#-------------------------------------------------------------------------
class __DebitCreditPair(object):

    #-------------------------------------------------------------------------
    def __init__(self, journals, keyTup, genLink=True):

        self.__date, self.__curr, self.__reallocVal, self.__link, self.__info = keyTup

        self.__journals = dict()
        self.__AddToDictionary(journals)

        if genLink and not self.__link:
            self.__link = acm.FJournalLink()
            self.__SetJournalLink(self.__link)

        AssertValidPair(self.Journals(), self.JournalLink())

    #-------------------------------------------------------------------------
    def Name(self):
        optKey = self.EventDate() if self.IsPeriodic() else None
        jlKey = self.JournalLink().Oid() if self.JournalLink() else None

        return "-".join([str(self.__info.Oid()), str(jlKey), str(optKey), str(self.__curr.Oid())])

    #-------------------------------------------------------------------------
    def Journals(self):
        return self.__journals.values()

    #-------------------------------------------------------------------------
    def JournalInformation(self):
        return self.__info

    #-------------------------------------------------------------------------
    def JournalLink(self):
        return self.__link

    #-------------------------------------------------------------------------
    def EventDate(self):
        return self.__date

    #-------------------------------------------------------------------------
    def AccountingInstruction(self):
        return self.__info.AccountingInstruction()

    #-------------------------------------------------------------------------
    def Currency(self):
        return self.__curr

    #-------------------------------------------------------------------------
    def ReallocationValue(self):
        return self.__reallocVal

    #-------------------------------------------------------------------------
    def IsPeriodic(self):
        return self.AccountingInstruction().IsPeriodic() if self.AccountingInstruction() else False

    #-------------------------------------------------------------------------
    def IsEmpty(self):
        return len(self.__journals) == 0

    #-------------------------------------------------------------------------
    def CompareAny(self, functor, *args):
        return any(functor(j, *args) for j in self.__journals.values())

    #-------------------------------------------------------------------------
    def CompareAll(self, functor, *args):
        return all(functor(j, *args) for j in self.__journals.values())

    #-------------------------------------------------------------------------
    def ComparePairsAny(self, pair, functor, *args):
        return self.__ComparePairsAny(pair, functor, *args) if pair else False

    #-------------------------------------------------------------------------
    def ComparePairsAll(self, pair, functor, *args):
        return self.__ComparePairsAll(pair, functor, *args) if pair else False

    #-------------------------------------------------------------------------
    def ComparePairsSameSize(self, pair):
        return len(self.__journals) == len(pair.Journals()) if pair else False

    #-------------------------------------------------------------------------
    def PerformWith(self, functor, *args):
        self.__PerformWith(functor, *args)

    #-------------------------------------------------------------------------
    def PerformWithPairs(self, pair, functor, *args):
        if pair:
            self.__PerformWithPairs(pair, functor, *args)

    #-------------------------------------------------------------------------
    def GenerateSuspenseJournals(self):
        self.__AddToDictionary(GenerateSuspense(self.Journals()))

    #-------------------------------------------------------------------------
    def RemoveInvalidJournals(self, validationFunc):
        if validationFunc:
            for key, journal in [(key, journal) for key, journal in self.__journals.iteritems()]:
                if not validationFunc(journal):
                    del self.__journals[key]

    #-------------------------------------------------------------------------
    def __ComparePairsAny(self, pair, functor, *args):
        return any(functor(j1, j2, *args) for j1, j2 in [(self.__Journal(key), pair.__Journal(key)) for key in self.__journals.keys()])

    #-------------------------------------------------------------------------
    def __ComparePairsAll(self, pair, functor, *args):
        return all(functor(j1, j2, *args) for j1, j2 in [(self.__Journal(key), pair.__Journal(key)) for key in self.__journals.keys()])

    #-------------------------------------------------------------------------
    def __PerformWith(self, functor, *args):
        for j in self.__journals.values():
            functor(j, *args)

    #-------------------------------------------------------------------------
    def __PerformWithPairs(self, pair, functor, *args):
        for j1, j2 in [(self.__Journal(key), pair.__Journal(key)) for key in self.__journals.keys()]:
            functor(j1, j2, *args)

    #-------------------------------------------------------------------------
    def __Journal(self, key):
        return self.__journals.get(key)

    #-------------------------------------------------------------------------
    def __SetJournalLink(self, link):
        for journal in self.Journals():
            journal.JournalLink(link)
            link.Journals().Add(journal)

    #-------------------------------------------------------------------------
    def __Sort(self, journal):
        oid = journal.JournalValueDefinition().Oid() if journal.JournalValueDefinition() else None
        debitOrCredit = None if oid else journal.DebitOrCredit()
        return (oid, debitOrCredit, journal.IsSuspenseAccountAmountDifference())

    #-------------------------------------------------------------------------
    def __AddToDictionary(self, journals):
        for journal in journals:
            key = self.__Sort(journal)
            AssertUniqueKey(key, self.__journals)
            self.__journals[key] = journal
