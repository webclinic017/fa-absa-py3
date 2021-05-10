import ael
import acm
import at_time

from FRoutingExtensions import trade_system

def filter_EOD_trades(entity, trdnum, *args):
    trd = acm.FTrade[trdnum]
    trd_exec_time = at_time.acm_datetime(trd.ExecutionTime())
    trd_eod_time = acm.DateToday() + ' 19:00:00'
    
    if trade_system(trd) and trd_exec_time <= trd_eod_time:
        return 1
    else:
        return 0
