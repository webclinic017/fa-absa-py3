import acm
from at_time import acm_date
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()

PRICE_ENTRY_DATE = acm_date('0d')

ael_variables.add(
    'curve_name',
    label='FX Curve Name',
    cls='FYieldCurve',
    default='ZAR-FX-OIS'
)
ael_variables.add(
    'rate_type',
    label='Rate Type',
    cls='string',
    default='Continuous'
)
ael_variables.add(
    'day_count',
    label='Day Count',
    cls='string',
    default='Act/365'
)
ael_variables.add(
    'display_type',
    label='Display Type',
    cls='string',
    default='Spot Rate'
)

FX_BENCHMARKS = ['ZAR/ON', 'ZAR/1w', 'ZAR/2w', 'ZAR/3w', 'ZAR/1m', 'ZAR/2m']


def calculate_rate(instrument, data):
    """Calculate the spot rate for benchmark"""
    fx_curve_ois = data['curve_name']
    fx_curve_ois = fx_curve_ois.IrCurveInformation()
    fx_curve_rate = fx_curve_ois.Rate(
        instrument.StartDate(),
        instrument.EndDate(),
        data['rate_type'],
        data['day_count'],
        data['display_type'],
        None, 0)
    return fx_curve_rate


def update_price_entry(instrument_name, rate, start_date):
    """Up date the rate in the price entry spot market"""
    for price in instrument_name.Prices():
        if price.Market().Name() in ['SPOT']:
            price.Bid(rate)
            price.Ask(rate)
            price.Last(rate)
            price.Settle(rate)
            price.Day(start_date)
            try:
                price.Commit()
                LOGGER.info("Successful Instreument: %s, Price: %s, Date: %s,\
                            Start Date: %s, End Date: %s",
                            instrument_name.Name(),
                            rate,
                            price.Day(),
                            instrument_name.StartDate(),
                            instrument_name.EndDate()
                            )
            except Exception as exc:
                LOGGER.exception("Error while committing the changes on the \
                                    trade: %s", exc)
            

def ael_main(ael_dict):
    for benchmark in FX_BENCHMARKS:
        ins = acm.FInstrument[benchmark]
        fx_curve_rate = calculate_rate(ins, ael_dict) 
        basis_curve_rate = round(fx_curve_rate, 8)*100
        update_price_entry(ins, basis_curve_rate, PRICE_ENTRY_DATE)
