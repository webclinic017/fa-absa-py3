""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingSetters.py"
#-------------------------------------------------------------------------
def IncrementalBaseAmountFailedUpdate(journal):
    assert journal, 'No journal given'

    journal.BaseAmount(0)
    journal.IsBaseAmountCalculationFailed(True)
