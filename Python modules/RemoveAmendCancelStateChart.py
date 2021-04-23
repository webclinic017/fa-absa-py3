import acm

theStateChart = 'DirectDeal'

#1. find and delete all BP that use the state chart
bps = acm.BusinessProcess().FindBySubjectAndStateChart(None, theStateChart)

for bp in bps:
    print "Deleting business process <%d> associated with state chart <%s>"%(bp.Oid(), theStateChart)
    bp.Delete()
sc = acm.FStateChart[theStateChart]
if sc:
    print "Deleting state chart <%s>"%(theStateChart)
    sc.Delete()

