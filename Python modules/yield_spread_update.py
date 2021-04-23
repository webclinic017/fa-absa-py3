"""----------------------------------------------------------------------------
DESCRIPTION
    Date                : 2021-02-10
    Purpose             : Update historical prime Jibar curves.
    Department and Desk : TODO
    Requester           : James Moodie
    Developer           : Buhlebezwe Ngubane

ENDDESCRIPTION
----------------------------------------------------------------------------"""
import acm
import datetime
from dateutil import parser
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()
ael_variables.add("spread_curve",
                    label = "Spread curve name",
                    cls = "string",
                    default="ZAR_Hypo_Prime",
                    mandatory = True)
ael_variables.add("spread",
                  label = "Spread",
                  cls = "double",
                  default = "0.0317",
                  mandatory = True)
ael_variables.add("start_date",
                  label = "Start Date",
                  alt = "Curve from this date (YYYY-MM-DD)",
                  cls = "string",
                  default = "2020-05-01",
                  mandatory = True)
ael_variables.add("end_date",
                  label = "End Date",
                  alt = "Curve before this date (YYYY-MM-DD)",
                  cls = "string",
                  default = "2020-08-21",
                  mandatory = True)

def ael_main(ael_params):
    LOGGER = getLogger(__name__)
    
    start_date = parser.parse(ael_params["start_date"]).date()
    end_date = parser.parse(ael_params["end_date"]).date()
    dates = []

    if start_date >= end_date:
        LOGGER.error("Invalid dates entered. Start date: %s greater than or equal to end date: %s"%(start_date, end_date))
        return
    
    while(start_date < end_date):
        dates.append(str(start_date))
        start_date = start_date + datetime.timedelta(1)
        
    LOGGER.info(dates)

    for date in dates:
        yc = acm.FAttributeSpreadCurve[ael_params['spread_curve']]
        yc_old = acm.GetHistoricalEntity(yc, date)
        yc_attr = yc_old.Attributes()[0]
        spreads = [sp for sp in yc_attr.Spreads()]
        acm.BeginTransaction()
        try:
            for spread in spreads:
                spread_clone = spread.Clone()
                spread_clone.Spread(ael_params["spread"])
                spread.Apply(spread_clone)
                spread.Commit()

            acm.CommitTransaction()
            LOGGER.info('ZAR_Hypo_Prime spreads updated on date %s' %date)
        except:
            acm.AbortTransaction()
            LOGGER.error('ZAR_Hypo_Prime spreads failed to update on date %s' %date)
