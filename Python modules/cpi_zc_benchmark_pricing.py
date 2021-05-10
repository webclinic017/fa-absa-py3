"""
Date                    : 2017-08-10
Purpose                 : Pricing script for the new Zaro Coupon CPI benchmarks.
Project:                : FA Upgrade 2017
Developer               : Libor Svoboda
"""
import acm
from at_price import set_instrument_price
from at_logging import getLogger
from at_timeSeries import get_time_series_values
from at_ael_variables import AelVariableHandler


LOGGER = getLogger(__name__)
TODAY = acm.Time.DateToday()


ael_variables = AelVariableHandler()
ael_variables.add(
    'benchmarks',
    label='Zero Coupon Benchmarks',
    cls='FInstrument',
    multiple=True
)
ael_variables.add(
    'yieldcurve',
    label='CPI Curve',
    cls='FYieldCurve'
)


def update_price(ins, yc):
    cpi_est_date = acm.Time.DateAddDelta(ins.EndDate(), 0, -4, 0)
    try:
        cpi_est_ts = get_time_series_values('InflationEstimates', 
                                            yc.Oid(), cpi_est_date)[-1]
    except (TypeError, IndexError):
        LOGGER.error('CPI estimate for %s does not exist.' % cpi_est_date)
        return
    cpi_est = cpi_est_ts.TimeValue()
    index_date = acm.Time.DateAddDelta(ins.StartDate(), 0, -4, 0)
    index = ins.FirstReceiveLeg().IndexRef()
    query = 'instrument=%s and day="%s"' % (index.Oid(), index_date)
    initial_index = acm.FPrice.Select(query)[0].Settle()
    price = ((cpi_est / initial_index) - 1) * 100
    set_instrument_price(ins, acm.FParty['SPOT'], price, ins.Currency(), TODAY)
    set_instrument_price(ins, acm.FParty['SPOT_MID'], price, ins.Currency(), TODAY)
    LOGGER.info('%s price updated to %s.' % (ins.Name(), price))


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    benchmarks = ael_dict['benchmarks']
    yc = ael_dict['yieldcurve']
    
    for benchmark in benchmarks:
        update_price(benchmark, yc)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
    
    LOGGER.info("Completed successfully.")

