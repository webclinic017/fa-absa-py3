"""----------------------------------------------------------------------------
PROJECT                 :  D1 HF Linked Notes
PURPOSE                 :  This script sets/updates spot price of an input
                           instrument. The price is calculated as an aggregated
                           column value (specified by input column ID) of input
                           portfolios divided by an input constant.
DEPATMENT AND DESK      :  Prime Broking
REQUESTER               :  Marko Milutinovic
DEVELOPER               :  Libor Svoboda
CR NUMBER               :  CHNG0002553846
-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date        Change no     Developer              Description
-------------------------------------------------------------------------------
22/01/2015  2583130       Libor Svoboda          User-selectable column ID
"""
import os
import math
import acm
import FLogger
import at_price
from at_ael_variables import AelVariableHandler


LOG_LEVEL = {'INFO': 1, 'DEBUG': 2, 'WARNING': 3, 'ERROR': 4}

logger = FLogger.FLogger('hf_unit_pricer')


def validate_divisor(ael_input):
    """Hook validating divisor."""
    divisor = ael_variables.get('divisor')
    if float(ael_input.value) == 0.0:
        msg = 'Divisor must be non-zero.'
        acm.GetFunction('msgBox', 3)('HF Unit Pricer', msg, 0)
        divisor.value = 1.0


ael_variables = AelVariableHandler()
ael_variables.add(
    'column_id',
    label='Column ID_Settings',
    cls='string',
    default='PS Fair Value NAV',
    alt='Column ID.'
)

ael_variables.add(
    'portfolios',
    label='Portfolio names_Settings',
    cls='FPhysicalPortfolio',
    default='',
    multiple=True,
    alt='Physical portfolio names.'
)

ael_variables.add(
    'instrument',
    label='Instrument name_Settings',
    cls='FInstrument',
    default='',
    alt='Instrument name.'
)

ael_variables.add(
    'divisor',
    label='Divisor_Settings',
    cls='float',
    default=1.0,
    alt='Selected divisor.',
    hook=validate_divisor
)

ael_variables.add(
    'log_level',
    label='Log Level_Logging',
    cls='string',
    collection=list(LOG_LEVEL.keys()),
    default='ERROR',
)

ael_variables.add(
    'log_path',
    label='Log Directory_Logging',
    cls='string',
    default=r'/services/frontnt/Task/',
)


def init_logging(level, path):
    """Initialize logging."""
    logger.Reinitialize(
        level=LOG_LEVEL[level],
        keep=False,
        logOnce=False,
        logToConsole=False,
        logToPrime=True,
        logToFileAtSpecifiedPath=os.path.join(
            path,
            'hf_unit_pricer_%s.log' % acm.Time.DateToday()
        ),
        filters=None
    )


def get_fx_rate(date, orig_curr, new_curr):
    """Return conversion rate between original and 
    new currency for a given date.
    """
    if orig_curr is None or new_curr is None:
        return 1.0
    
    cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    return orig_curr.Calculation().FXRate(cs, new_curr, date).Number()


def report_error(error_msg):
    """Handle error logging and raise a custom exception using
    input error message.
    """
    logger.ELOG(error_msg)
    logger.LOG("hf_unit_pricer failed.")
    raise HFUnitPricerError(error_msg)


def convert_value(value, value_curr, output_curr, date):
    """Convert column value into output currency."""    
    return value * get_fx_rate(date, value_curr, output_curr)


def get_number(value):
    """Convert column value into a number."""
    if not value:
        return 0.0
    
    try:
        value = float(value)
    except (ValueError, TypeError):
        report_error("Column value cannot be converted into a number.")
    
    if math.isnan(value):
        report_error("Column value cannot be 'nan'.")
    
    return value


def get_currency(value):
    """Return currency of column value"""
    try:
        return acm.FCurrency[value.Unit().Text()]
    except AttributeError:
        return None  


def aggregate_portfolio_values(column_id, portfolios, date, currency):
    """Return aggregated column values (identified by input column_id) 
    of input portfolios for the given date and currency.
    """
    calc_space = acm.FCalculationSpace('FPortfolioSheet')
    calc_space.SimulateGlobalValue('Valuation Date', date)
    
    agg_value = 0
    for prf in portfolios:
        calc_space.SimulateValue(prf, 'Portfolio Currency', currency)
        try:
            column_value = calc_space.CalculateValue(prf, column_id)
        except RuntimeError as err:
            report_error("Calculating '%s' of portfolio '%s' failed: %s"
                         % (column_id, prf.Name(), err))
        
        value = convert_value(get_number(column_value), 
                              get_currency(column_value), currency, date)
        logger.LOG("'%s' of '%s': %s." % (column_id, prf.Name(), value))
        agg_value += value
    
    return agg_value


def ael_main(ael_params):
    init_logging(ael_params['log_level'], ael_params['log_path'])
    date_today = acm.Time.DateToday()
    column_id = ael_params['column_id']
    portfolios = ael_params['portfolios']
    instrument = ael_params['instrument']
    divisor = ael_params['divisor']
    logger.LOG(
        "hf_unit_pricer started for instrument '%s' and portfolio(s): %s."
        % (instrument.Name(), ', '.join([prf.Name() for prf in portfolios]))
    )
    
    agg_value = aggregate_portfolio_values(column_id,
                                           portfolios, 
                                           date_today, 
                                           instrument.Currency())
    new_spot = agg_value / divisor
    try:
        at_price.set_instrument_price(instrument,
                                      acm.FParty['SPOT'],
                                      new_spot,
                                      instrument.Currency(),
                                      date_today)
    except Exception as exc:
        report_error("Updating SPOT price of instrument '%s' failed: %s"
                     % (instrument.Name(), exc))
    
    logger.LOG("SPOT price of instrument '%s' updated to %s %s." 
               % (instrument.Name(), new_spot, instrument.Currency().Name()))
    logger.LOG("hf_unit_pricer finished successfully.")
    

class HFUnitPricerError(Exception):
    """Custom HF Unit Pricer error."""
    pass
