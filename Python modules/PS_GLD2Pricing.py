"""
------------------------------------------------------------------------------------------------------------------------
Project:    Prime Brokerage Project
Department: Prime Services
Requester:  Eveshnee Naidoo
Developer:  Marian Zdrazil
CR Number:  FAPE-454 (Initial Deployment)
------------------------------------------------------------------------------------------------------------------------

HISTORY
========================================================================================================================
Developer               Change no     Date            Description
-----------------------------------------------------------------------------------------------------------------------
Marian Zdrazil          FAPE-454      2020-07-28      Initial implementation
-----------------------------------------------------------------------------------------------------------------------
"""
import acm

from PS_UploadPrices import _setInstrumentPrice
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

LOGGER = getLogger(__name__)


def get_instrument_price(instrument_name, market, price_date):
    """
        Get the (SPOT) market closing price for an instrument on a specific date.
    """

    query = 'instrument = "%s" and market = "%s" and day <= "%s"' % (instrument_name, market, price_date)
    prices = acm.FPrice.Select(query).SortByProperty('Day', False)

    if prices:
        price = prices[0].Settle()
        LOGGER.info('Historical price (%s) found for instrument=%s and date=%s' % (price, instrument_name, price_date))

        return price

    LOGGER.error('No historical price for instrument %s and date %s. Set price to 0.' % (instrument_name, price_date))

    return 0.0


def custom_date_hook(selected_variable):
    """
        Enable/Disable Custom Date based on Date value.
    """
    var_name = selected_variable.name

    date_value = selected_variable.handler.get(var_name)
    date_custom = selected_variable.handler.get("valDateCustom")

    if date_value.value == 'Custom Date':
        date_custom.enabled = True
    else:
        date_custom.enabled = False


TODAY = acm.Time().DateToday()

# Generate date lists to be used as drop downs in the GUI.
date_list = {'Custom Date': TODAY, 'Now': TODAY}
date_keys = list(date_list.keys())
date_keys.sort()

ael_variables = AelVariableHandler()
ael_variables.add('valDate',
                  label='Valuation Date',
                  cls='string',
                  collection=date_keys,
                  default='Now',
                  mandatory=True,
                  multiple=False,
                  alt=('ZAR/GLD2/CFD price will be set to ZAR/GLD SPOT Settle price on this date.'),
                  hook=custom_date_hook,
                  enabled=True)
ael_variables.add('valDateCustom',
                  label='Valuation Date Custom',
                  cls='string',
                  collection=None,
                  default=TODAY,
                  mandatory=False,
                  multiple=False,
                  alt='Custom valuation date',
                  hook=None,
                  enabled=True)


def ael_main(ael_dict):

    if ael_dict['valDate'] == 'Custom Date':
        val_date = ael_dict['valDateCustom']
    else:
        val_date = date_list[ael_dict['valDate']]

    try:
        LOGGER.info("Going to set ZAR/GLD2/CFD price equal to ZAR/GLD Spot settle price")
        inst_GLD_name = 'ZAR/GLD'
        inst_GLD2_CFD = acm.FInstrument['ZAR/GLD2/CFD']
        price = get_instrument_price(inst_GLD_name, 'SPOT', val_date)
        _setInstrumentPrice(inst_GLD2_CFD, price, val_date, 'SPOT')
        _setInstrumentPrice(inst_GLD2_CFD, price, val_date, 'internal')
    except Exception as exc:
        LOGGER.error("Cannot create price entry: %s" % exc)
    else:
        LOGGER.info("Completed Successfully.")
