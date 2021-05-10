"""-----------------------------------------------------------------------------
PURPOSE              :  Utility functions related to FBusinessProcess objects
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2020-06-03  CHG0103217     Libor Svoboda       Initial deployment
"""
import datetime

import acm


def year_and_month_from_valuation_date(business_process):
    # Used by YearAndMonthFromValuationDate FCustomMethod
    val_date = business_process.AdditionalInfo().BP_ValuationDate()
    if not val_date:
        return ''
    dt_date = datetime.date(*acm.Time.DateToYMD(val_date))
    return '{:%Y/%m}'.format(dt_date)

