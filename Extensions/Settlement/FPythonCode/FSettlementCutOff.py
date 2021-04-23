""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementCutOff.py"
"""----------------------------------------------------------------------------
MODULE
    FSettlementCutOff - Module which executes cut-off checks for settlements

    (c) Copyright 2008 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

DATA-PREP

REFERENCES
    See module FSettlementEOD

----------------------------------------------------------------------------"""
from FSettlementEnums import SettlementStatus
import FOperationsUtils as Utils

def start(check_historical):
    Utils.Log(True, '------------------------------------------------------------')
    pr = 'Check Settlement cut-off times...STARTED %s' % \
         time.asctime(time.localtime())
    Utils.LogAlways(pr)
    settlementCount = 0

    query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    if check_historical == 'Yes':
        query.AddAttrNode('InternalCutoffDay', 'LESS_EQUAL', acm.Time.DateToday())
    else:
        query.AddAttrNode('InternalCutoffDay', 'EQUAL', acm.Time.DateToday())
    query.AddAttrNode('IsBeforeCutoffTime', 'EQUAL', 'FALSE')
    queryAuthorised = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    queryAuthorised.AddAttrNode('Status', 'EQUAL', Utils.GetEnum("SettlementStatus", SettlementStatus.AUTHORISED))
    for settlement in queryAuthorised.Select():
        if query.IsSatisfiedBy(settlement):
            try:
                pr = 'Settlement %d has passed its cut-off time. Status set to Exception' % settlement.Oid()
                Utils.LogAlways(pr)
                clone = settlement.Clone()
                clone.IsHistoricValueDate('TRUE')
                clone.Status(SettlementStatus.EXCEPTION)
                settlement.Apply(clone)
                settlement.StateChart(acm.Operations.GetMappedSettlementProcessStateChart(settlement))
                updatedProcess = acm.Operations.HandleUpdateOnSettlementProcess(settlement, settlement.GetSettlementProcess(), "")
                settlement.UpdateStatusFromSettlementProcess(updatedProcess)
                settlement.Commit()
                if updatedProcess:
                    updatedProcess.Commit()
                settlementCount += 1
            except Exception as e:
                pr = 'Failed to update Settlement %d. The following exception occured: %s' % (settlement.Oid(), str(e))
                Utils.LogAlways(pr)




    pr = 'Processed %d settlements that had passed cut-off time' % settlementCount
    Utils.LogAlways(pr)
    pr = 'Check Settlement cut-off times...FINISHED %s' % \
        time.asctime(time.localtime())
    Utils.LogAlways(pr)
    Utils.LogAlways('------------------------------------------------------------')

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    if __name__ == "__main__":
        import sys, getopt

    import acm, time, ael
    import FOperationsUtils as Utils

    ael_variables = [('check_historical', 'Check historical settlements',
                       'string', ['Yes', 'No'], 'No', 0)]

    def ael_main(dictionary):
        start(dictionary["check_historical"])

except Exception as e:
    if 'ael_variables' in globals():
        del globals()['ael_variables']
    if 'ael_main' in globals():
        del globals()['ael_main']
    Utils.LogAlways('Could not run FOperationsSettlementCutOff due to ')
    Utils.LogAlways(str(e))
