""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingJournalPairGenerator.py"

# operations
from FOperationsGenerators import PairGenerator

#-------------------------------------------------------------------------
# Generator for generating pairs of journals that match each other, in this
# case old and new journals to compare for amendment handling. If
#-------------------------------------------------------------------------
def GeneratePairs(newJournals, oldJournals):
    return PairGenerator.Generate(newJournals, oldJournals, __PairsCompare)

#-------------------------------------------------------------------------
def __PairsCompare(newPair, oldPair):
    if newPair and oldPair:
        if __PairsMatch(newPair, oldPair):
            return PairGenerator.Compare.EQUAL
        elif newPair.EventDate() <= oldPair.EventDate():
            return PairGenerator.Compare.PREDECESSOR
        else:
            return PairGenerator.Compare.SUCCESSOR

#-------------------------------------------------------------------------
def __PairsMatch(newPair, oldPair):
    if newPair.Currency() != oldPair.Currency():
        return False
    if newPair.IsPeriodic() and oldPair.IsPeriodic() and newPair.EventDate() != oldPair.EventDate():
        return False
    if newPair.ReallocationValue() != oldPair.ReallocationValue():
        return False
    return True
