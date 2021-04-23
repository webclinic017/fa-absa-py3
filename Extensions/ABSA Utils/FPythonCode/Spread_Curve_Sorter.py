"""--------------------------------------------------------------------------
MODULE
   Spread_Curve_Sorter

DESCRIPTION
    This module sort a spread curve by its  spread points.

HISTORY 
Date: 2020-02-19
   
-----------------------------------------------------------------------------"""
import acm
import ael

from at_logging import getLogger

LOGGER = getLogger(__name__)

def get_calendarname(spread_curve):
    try:
        underlying_curve = spread_curve.UnderlyingCurve()
        first_benchmark = underlying_curve.Benchmarks()[0]
        for leg in first_benchmark.Instrument().Legs():
            return leg.ResetCalendar().Name()
        LOGGER.info("Succesfully retirved the calendar linked to the following curve {}".format(spread_curve.Name()))
    except Exception as e:
        LOGGER.error("Failed while trying to retrieve the calander linked to the following curve {}".format(spread_curve.Name()))
        LOGGER.info(e)

def business_days(start_date, period, calendar_name):
    try:
        sdate = ael.date(start_date).add_banking_day(ael.Calendar[calendar_name],
                                                     acm.FInstrument['ZAR'].SpotBankingDaysOffset())
        end_date = sdate.add_period(period).adjust_to_banking_day(ael.Instrument[acm.FInstrument['ZAR'].Currency().Name()], 'Mod. Preceding')
        return end_date
        LOGGER.info("The end date associated with the {}".format(period)+" spread point was calculated succesfully.")
    except Exception as e:
        LOGGER.error("Failed while tring to clalculate the end date associated with {}".format(period)+" spread point")
        LOGGER.info(e)


def sort_spreadpoints(curve_name):
    try:
        sorted_dict = {"Point Name": [],"Point End Date":[],"Spread Point":[]}
        curve = acm.FAttributeSpreadCurve["ZAR-MM-FundingSpr"]
        calendar_name = get_calendarname(curve)
        end_dates = [business_days(ael.date_today(), sp.Point().Name(), calendar_name) for  sp in curve.Attributes()[len(acm.FAttributeSpreadCurve[curve_name].Attributes()) - 1].Spreads()]
        spread_points = [sp  for sp in curve.Attributes()[len(acm.FAttributeSpreadCurve[curve_name].Attributes()) - 1].Spreads()]
        dict = {end_dates[counter]: spread_points[counter] for counter in range(len(end_dates))}
        for key in sorted(dict.keys()):
            sorted_dict["Point Name"].append(dict[key].Point().Name())
            sorted_dict["Point End Date"].append(key)
            sorted_dict["Spread Point"].append(dict[key].Spread()*100)
        return sorted_dict
        LOGGER.info("The {}".format(curve_name)+" curve was  successfully sorted by its spreadpoints.")
    except Exception as e:
        LOGGER.error("Failed while trying to sort {}".format(curve_name)+" by its spreadpoints.")
        LOGGER.info(e)

