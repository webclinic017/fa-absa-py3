""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/FSettlementCommitterFunctions.py"
import acm

#-------------------------------------------------------------------------
def CommitCommitters(committerList, logger):
    commitSuccessful = True
    acm.BeginTransaction()
    try:
        for committer in committerList:
            settlement = committer.GetSettlement()
            RunSTPAndUpdateStateChart(settlement)
            committer.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        commitSuccessful = False
        logger.LP_Log("Exception occurred while committing settlements: {}".format(str(e)))
        logger.LP_Flush()
    return commitSuccessful

#-------------------------------------------------------------------------
def RunSTPAndUpdateStateChart(settlement):
    if settlement.IsValidForSTP():
        settlement.STP()
    stateChart = acm.Operations.GetMappedSettlementProcessStateChart(settlement)
    settlement.StateChart(stateChart)
    if settlement.IsValidForSTP():
        settlement.STP()