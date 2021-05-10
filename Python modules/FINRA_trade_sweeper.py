
"""

FINRA_trade_sweeper
This modules sweeps all the FINRA eligibles trades
booked before FINRA market hours and performs a bulk reporting to TRACE.

History
=======
2021-02-22 Snowy Mabilu ARR-69 - Initial code

"""

import acm
import ael
import TRACEUtils

ael_variables = []


def get_failed_processes():
    query = """
        select b.seqnbr from BusinessProcess b
        where b.state_chart_seqnbr = {} 
        and subject_type = 'Trade' 
        and updat_time >=date_add_banking_day(today,'ZAR Johannesburg',-1) 
            """.format(acm.FStateChart[TRACEUtils.FINRA_STATE_CHART].Oid())
    return ael.asql(query)[1][0]


def ael_main(parameters):
    business_processes = get_failed_processes()
    for seq_nbr in business_processes:
        bp = acm.FBusinessProcess[seq_nbr[0]]
        trade = bp.Subject()
        if bp.CurrentStateName() == 'Failed':
            if TRACEUtils.is_trace_eligble(trade):
                TRACEUtils.trigger_finra_send(trade, 'report')
            elif TRACEUtils.is_valid_trade(TRACEUtils.CANCELLED_TRADES_QUERY,
                                           trade) and TRACEUtils.has_live_allocations(trade):
                TRACEUtils.trigger_finra_send(trade, 'report')
            else:
                bp.Delete()
        elif bp.CurrentStateName() not in ['Failed', 'Reported'] and TRACEUtils.is_trace_eligble(trade):
            bp.Delete()
            trade.Touch()
            trade.Commit()