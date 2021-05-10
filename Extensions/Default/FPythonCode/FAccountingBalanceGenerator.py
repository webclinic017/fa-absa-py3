""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingBalanceGenerator.py"

# itertools
from itertools import groupby

#-------------------------------------------------------------------------
# Generator for generating balance related data
#-------------------------------------------------------------------------
def GenerateBalance(journals, keyfunc):
    for key, journals in groupby(journals, key=keyfunc):
        journals = list(journals)

        amount = sum(journal.Amount() for journal in journals)
        baseAmount = sum(journal.BaseAmount() for journal in journals)
        yield key, journals, amount, baseAmount
            