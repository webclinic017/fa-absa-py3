""" CorporateActions:1.2.2 """

"""----------------------------------------------------------------------------
MODULE
    FCAStartRollback - Module used to rollback / undo Corporate Actions.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    A Macro variables window is displayed with different Corporate
    Actions possible to roll back.
----------------------------------------------------------------------------"""

import ael
import FCARollback
from FCAMisc import scr_upd, string_parse

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
voidel = ['Void', 'Delete']
try:
    ael.begin_transaction()

    cas = scr_upd('Script Update Done')
    cas2 = scr_upd('Script Update')

    ael_variables = [('ca_nbr', 'Undo Corporate Action:', 'string', cas, '', 1, 1),
                    ('void', 'Void Trades', 'string', voidel, 'Delete', 0, 0),
                    ('ref', 'Replace by:', 'string', cas2, '', 0, 0)]

    def ael_main(d):
        v = d.get('void')
        ca_nbr = d.get('ca_nbr')
            # ['Seqno.6 +5 on Stock: Spin-off; CORP; ExDate:2001-09-05']
        ref = d.get('ref') 
            # Seqno.5 +2 on Option: Merger; CORP; ExDate: 2001-09-05
        parsed2 = string_parse(str(ref), None) # 5 (i.e. ca_seqnbr to refer to)
        for canbr in ca_nbr:
            parsed = int(string_parse(str(canbr), None)) # 6 (i.e. ca_seqnbr)
            corpact = ael.CorpAction[parsed]
            rb = FCARollback.RollbackInfo(corpact)
            ### Rollback data:
            try:
                rb.rollback(void = v)
            except FCARollback.NotFound, e:
                print e
    ael.commit_transaction()
except:
    print 'Uncaught exception in FCAStartRollback.'
    ael.abort_transaction()
    raise


