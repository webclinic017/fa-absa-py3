""" CorporateActions:1.2.2 """

"""----------------------------------------------------------------------------
MODULE 
    FCAPurgeRollbackTable - Module which deletes rows from CaRollbackData

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module deletes the CaRollbackData rows that correspond to ca_seqnbr 
    which are older than a certain Ex Date. The number of days old a corporate
    action has to be is specified at the beginning of the module.
----------------------------------------------------------------------------"""
#Enter number of days since Ex Date:
Days_Old = 100
Off = 1 # Off = 1 means nothing will actually happen. Off = 0 will delete info.

import ael

cut_off_date = ael.date_today().add_days(-Days_Old)
print('Corporate Actions with Ex Date older than %s will not be possible to '\
    'rollback.' % str(cut_off_date))

ca = ael.CorpAction
#rb = ael.CaRollbackData #Does not work on databases older than 3.4.0
seqnbr_list = []

for c in ca:
    if (c.ca_trade_status == 'Script Update Done' 
    or c.ca_ins_status == 'Script Update Done'):
        if c.ex_date < cut_off_date:
            t = ael.dbsql('select ca_seqnbr from ca_rollback_data '\
                          'where ca_seqnbr=%d' % c.seqnbr)
        if t != [[]]:
            seqnbr_list.append(c.seqnbr)

print('The following Corporate Actions will be deleted:', seqnbr_list)

for s in seqnbr_list:
    if Off == 0:
        print("Deleted", s)
        ael.dbsql('delete from ca_rollback_data where ca_seqnbr = %d' \
            % s)

