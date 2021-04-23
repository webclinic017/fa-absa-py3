'''-----------------------------------------------------------------------------
PROJECT                 :  Money Market Demat amintenance
PURPOSE                 :  To update the expired amount 
DEPATMENT AND DESK      :  Ops
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Manan Ghosh
CR NUMBER               :  ABITFA - 4800
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------

2017-05-11              Manan Ghosh           To update the expired instruments to expired
2018-01-18              Manan Ghosh           To expire demat instruments on weekly basis

'''

import acm
from at_ael_variables import AelVariableHandler

INSquery = 'Demat_Expired_Instruments'

MMSS_ISIN_REQUEST_STATE_CHART_NAME = 'MM ISIN Management'

ael_variables = AelVariableHandler()

def ael_main(config):

    state_chart = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]

    past_expiry = acm.FStateChartEvent('Past expiry date')

    instruments = acm.FStoredASQLQuery[INSquery].Query().Select()

    for instr in instruments:
        processes = acm.BusinessProcess.FindBySubjectAndStateChart(instr, state_chart)
        if processes and len(processes) == 1:
            bp = processes[0]
            if not bp:
                print 'Business process for instrument [%s] is missing !! ' % instr.Name()
                continue

            cs = bp.CurrentStep()

            if cs.State().Name() == 'Active':
                print 'Updating instrument [%s] to Expired in Business process [%i] !! ' % (instr.Name(), bp.Oid())
                bp.HandleEvent(past_expiry, params = None, notes = None )
                bp.Commit()

