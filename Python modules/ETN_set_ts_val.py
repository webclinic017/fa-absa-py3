"""----------------------------------------------------------------------------
PROJECT                 :   ETN Pricing
PURPOSE                 :   Setting market value to Time Serie
DEPATMENT AND DESK      :   Prime Services, Commodities
REQUESTER               :   Byron Woods, Floyd Malatji
DEVELOPER               :   Ondrej Bahounek
CR NUMBER               :   CHG1000488229

Script enables to set Accumulated Market value directly to time serie
for given ETN and day.
Should be used by TCU when reset day is set explicitly by business.
If the Reset Day is a historical day (T0 < TODAY),
then 'ETN_update_daily_vals' should run for all days:
starting the first day after historical day (i.e. T+1) and ending TODAY


More info: https://confluence.barcapint.com/display/ABCAPFA/Commodities+-+ETN+solution

HISTORY
===============================================================================
Date        Change no      Developer        Description
-------------------------------------------------------------------------------
2018-08-07  CHG1000488229  Ondrej Bahounek  Initial Implementation
----------------------------------------------------------------------------"""

import acm
from CurrencyETNPricing import get_underlying_frn, save_to_timeserie
from at_timeSeries import add_time_series_value
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger()
ael_variables = AelVariableHandler()


def select_etns():
    query = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
    q = query.AddOpNode('AND')
    q.AddAttrNode('InsType', 'EQUAL', 'ETF')
    q.AddAttrNode('Underlying.InsType', 'EQUAL', 'EquityIndex')
    q.AddAttrNode('ValuationGrpChlItem.Name', 'EQUAL', 'CurrencyETN')
    return query.Select()


ael_variables.add(
    'inpt_etns',
    label='ETN',
    cls='FETF',
    collection=select_etns(),
    alt='ETN to have updated time serie.'
    )
ael_variables.add(
    'ts_date',
    label='Reset Date',
    cls='date',
    alt='Date for which time serie will be saved.'
    )
ael_variables.add(
    'ts_val',
    label='Value',
    cls='float',
    alt='Accumulated Mkt Pip for ETN for given day.'
    )


def ael_main(ael_dict):
    etn = ael_dict['inpt_etns']
    day = ael_dict['ts_date'].to_string("%Y-%m-%d")
    value = ael_dict['ts_val']
    
    LOGGER.info("ETN: '%s'", etn.Name())
    LOGGER.info("Day: '%s'", day)
    LOGGER.info("Value: '%s'", value)
    
    frn = get_underlying_frn(etn)
    save_to_timeserie(frn, value, day)
    LOGGER.info("Done.")
