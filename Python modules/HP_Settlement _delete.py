import acm

settle_to_delete = [5703766,
5703767,
5703768,
5703769,
5703770,
5703771,
5703772,
5703773,
5703774,
5703775,
5703776,
5703777,
5703778,
5703779,
5703780,
5703781,
5703796,
5703797,
5703798,
5703799,
5703802,
5703803,
5703804,
5703805,
5703808,
5703809,
5703810,
5703811,
5703829,
5703830,
5703831,
5703832,
5703833,
5703834,
5703835,
5703836,
5703837,
5703838,
5703839,
5703840,
5703841,
5703842,
5703843,
5703844,
5703845,
5703846,
5703847,
5703848,
5703849,
5703850,
5703851,
5703852,
5703853,
5703854,
5703855,
5703856,
5703857,
5703858,
5703859,
5703860,
5703861,
5703862,
5703863,
5703864,
5703877,
5703878,
5703879,
5703880,
5703881,
5703882,
5703883,
5703884,
5703885,
5703886,
5703887,
5703888,
5703898,
5703899,
5703900,
5703901]

for sett in settle_to_delete:
    try:
        acm.BeginTransaction()
        s = acm.FSettlement[sett]

        ext_objs = s.ExternalObjects()
        for ext_obj in ext_objs:
            ext_obj.Parent(None)
            ext_obj.Commit()

        acm.CommitTransaction()
        print('updated EOs on settlement %s' % sett)
    except Exception, e:
        print('failed to update EOs on settlement %s' % sett)
        print(str(e))
        acm.AbortTransaction()

for sett in settle_to_delete:
    try:
        acm.BeginTransaction()
        s = acm.FSettlement[sett]
        child = s.Children()[0]
        docs = s.Documents()
        for doc in docs:
            doc.Delete()
        ext_objs = s.ExternalObjects()
        for ext_obj in ext_objs:
            ext_obj.Parent(None)
            for ext_child in ext_obj.Children():
                ext_child.Parent(None)
                ext_child.Delete()
            bp = acm.FBusinessProcess.Select('subject_type="ExternalObject" and subject_seqnbr = %d' % ext_obj.Oid())
            bp.Delete()
            ext_obj.Delete()

        child_si = child.StorageImage()
        child_si.Parent(None)
        child_si.Status('Settled')
        child_si.Commit()
        s.Delete()
        acm.CommitTransaction()
        print('deleted settlement %s' % sett)
    except Exception, e:
        print('failed to delete settlement %s' % sett)
        print(str(e))
        acm.AbortTransaction()
