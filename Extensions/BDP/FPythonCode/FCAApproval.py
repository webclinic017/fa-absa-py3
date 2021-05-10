""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FCAApproval.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FCAApproval - Module which process the approval of the corp aciton.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm

import FBDPRollback
import FBDPCommon

from FBDPCurrentContext import Logme


def perform(execParam):
    rollback = FBDPRollback.RollbackWrapper('CorpActionApproval',
                    0, execParam)

    r = _FCAApproval(rollback, execParam)
    r.perform()
    rollback.end()
    del r

class _FCAApproval():

    def __init__(self, rollback, execParam):

        self._rollbackWrapper = rollback
        self._corpName = execParam['CorpAction'][0]
        self._corp = acm.FCorporateAction[self._corpName]
        if not self._corp:
            failMsg = ('Invalid corporate action with name'
                       '  {0}. '.format(self._corpName))
            Logme()(failMsg, 'ERROR')

    def perform(self):
        busEvt = self._corp.BusinessEvent()
        if not busEvt:
            failMsg = ('No business event associate with the'
                       ' corpAction {0}. '.format(self._corpName))
            Logme()(failMsg, 'ERROR')
            return

        links = busEvt.TradeLinks()
        for l in links:
            t = l.Trade()
            aelT = FBDPCommon.acm_to_ael(t)
            newT = aelT.clone()
            newT.status = 'FO Confirmed'
            self._rollbackWrapper.add_trade(newT, ['status'])

        aelCorpT = FBDPCommon.acm_to_ael(self._corp)
        aelCorp = aelCorpT.clone()
        aelCorp.status = 'Processed'
        self._rollbackWrapper.add(aelCorp, ['status'])
