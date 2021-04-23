import acm

trdnbrs = [22520764, 23719913, 23965139, 19327235, 26091740, 14766857, 20439644, 21053165, 16206304, 27556232, 17732968,]


for trdnbr in trdnbrs:
    t=acm.FTrade[trdnbr]
    # change the status of these trades from Void to Simulated to
    #  a) allow the change (for other user than FMAINTENANCE), 
    #  b) so they are not archived again if we archive Void BSBacks
    t.Status('Simulated')
    t.ArchiveStatus(0)
    t.Commit()
    print "%s done" % t.Oid()

print "Completed Successfully"
