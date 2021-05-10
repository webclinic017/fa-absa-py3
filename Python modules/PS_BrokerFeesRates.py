'''
Date                    : [2012-02-15]
Purpose                 : [Fees rates for Prime Services]

Department and Desk     : [Prime Services]
Requester               : [Francois Henrion]
Developer               : [Peter Fabian]
CR Number               : [C000000892151]

HISTORY
========================================================================================================================
Date        Change no       Developer           Description
------------------------------------------------------------------------------------------------------------------------
2012-05-16  C194115         Peter Fabian        Changing constants to current values, added IPL cap and VAT factor, removed STRATE
2013-05-15  C1031015        Jan Sinkora         Merging constants with SAEQ_BrokerFees, getting VAT factor from the extension attribute.
2013-09-27  C1382968        Jan Sinkora         Updating the JSE fees based on the document attached to ABITFA-2224.
2014-06-12  C1997018        Peter Fabian        Moving the rates to time series plus caching
2017-04-04  4452477         Libor Svoboda       JSE cost updates 2017.
2018-07-03  CHG1000166517   Libor Svoboda       JSE cost updates 2018.
2019-06-26  CHG1001930222   Marian Zdrazil      Adding A2X cost algo - FAPE-34
'''
import acm
import PS_TimeSeriesFunctions


TODAY = acm.Time.DateToday()
VAT_ID = acm.FAel['PS_BrokerFeesRates']
VAT_TS = PS_TimeSeriesFunctions.GetTimeSeries("VAT_rate", VAT_ID)


class RateCache(object):
    """ Provide a simple cache for today's rates;
        rates for other days are available through 
        using slower lookups in respective time series
    """
    def __init__(self):
        self.entity = acm.FAel['PS_BrokerFeesRates']
        self.value_of = dict()
    
    def _get_time_series_value(self, time_series_id, date):
        ts = PS_TimeSeriesFunctions.GetTimeSeries(time_series_id, self.entity)
        if not ts:
            raise RuntimeError("No such time series: %s" % time_series_id)
        return PS_TimeSeriesFunctions.GetTimeSeriesPoint(ts, date).TimeValue()
    
    def get_value(self, time_series_id, date=TODAY):
        if date == TODAY:
            if time_series_id in self.value_of:
                return self.value_of[time_series_id]
            else:
                val = self._get_time_series_value(time_series_id, date)
                self.value_of[time_series_id] = val
                return val
        else:
            return self._get_time_series_value(time_series_id, date)


rates = RateCache()
BASIS_POINT_FACTOR = 10000.0

BROKER_TRADING_FACTOR = rates.get_value("Trading_factor") / BASIS_POINT_FACTOR
BROKER_TRADING_FLOOR = rates.get_value("Trading_floor")
BROKER_TRADING_CAP = rates.get_value("Trading_cap")

A2X_BROKER_TRADING_PASSIVE_FACTOR = rates.get_value("A2X_Trd_pass_factor") / BASIS_POINT_FACTOR
A2X_BROKER_TRADING_AGGRESSOR_FACTOR = rates.get_value("A2X_Trd_aggr_factor") / BASIS_POINT_FACTOR
A2X_BROKER_TRADING_CAP = rates.get_value("A2X_Trading_cap")

BROKER_CLEARING_FACTOR = rates.get_value("Clearing_factor") / BASIS_POINT_FACTOR
BROKER_CLEARING_FLOOR = rates.get_value("Clearing_floor")
BROKER_CLEARING_CAP = rates.get_value("Clearing_cap")

A2X_BROKER_CLEARING_FACTOR = rates.get_value("A2X_Clearing_factor") / BASIS_POINT_FACTOR
A2X_BROKER_CLEARING_CAP = rates.get_value("A2X_Clearing_cap")

BROKER_IPL_FACTOR = rates.get_value("IPL_factor") / BASIS_POINT_FACTOR
BROKER_IPL_CAP = rates.get_value("IPL_cap")

A2X_BROKER_IPL_FACTOR = rates.get_value("A2X_IPL_factor") / BASIS_POINT_FACTOR

BROKER_JSETS = rates.get_value("JSETS")

BROKER_FIXED = rates.get_value("Broker_fixed") / BASIS_POINT_FACTOR

BROKER_STT = rates.get_value("Broker_STT")

BROKER_STRATE_LOWER_LIMIT = rates.get_value("Strate_lower_lim")
BROKER_STRATE_UPPER_LIMIT = rates.get_value("Strate_upper_lim")
BROKER_STRATE_FACTOR = rates.get_value("Strate_factor") / BASIS_POINT_FACTOR
# The minimum fee is not exactly reflecting min/max value * factor,
# therefore it must be specified statically.
BROKER_STRATE_LOWER = rates.get_value("Strate_lower")

JSE_MEMBERSHIP_FEE = rates.get_value("JSE_membership")

OTHER_COSTS = rates.get_value("Other_costs_factor") / BASIS_POINT_FACTOR
OTHER_COSTS_CAP = rates.get_value("Other_costs_cap")
OTHER_COSTS_AGENCY = rates.get_value("Other_costs_agency") / BASIS_POINT_FACTOR
OTHER_COSTS_CAP_AGENCY = rates.get_value("Other_costs_cap_ag")
OTHER_COSTS_EQUITIES = rates.get_value("Other_costs_eq") / BASIS_POINT_FACTOR
OTHER_COSTS_CAP_EQUITIES = rates.get_value("Other_costs_cap_eq")
OTHER_COSTS_PRIME = rates.get_value("Other_costs_prime") / BASIS_POINT_FACTOR
OTHER_COSTS_CAP_PRIME = rates.get_value("Other_costs_cap_ps")
OTHER_COSTS_STRUCTURED = rates.get_value("Other_costs_st") / BASIS_POINT_FACTOR
OTHER_COSTS_CAP_STRUCTURED = rates.get_value("Other_costs_cap_st")

COMM_BROKER_ACS_FEE = rates.get_value("Comm_ACS_fee")
COMM_BROKER_ACS_FEE_AIB = rates.get_value("Comm_ACS_fee_AIB")
COMM_BROKER_IPL_FACTOR = rates.get_value("Comm_IPL_factor") # 0.0002

SWIFT_STRATE_FACTOR = rates.get_value("Swift_Strate_factor") / BASIS_POINT_FACTOR
SWIFT_STRATE_CAP = rates.get_value("Swift_Strate_cap")

BROKER_STRATE = rates.get_value("Broker_Strate") / BASIS_POINT_FACTOR
BROKER_STRATE_CAP = rates.get_value("Broker_Strate_cap")
BROKER_STRATE_AGENCY = rates.get_value("Broker_Str_ag") / BASIS_POINT_FACTOR
BROKER_STRATE_CAP_AGENCY = rates.get_value("Broker_Str_cap_ag")
BROKER_STRATE_EQUITIES = rates.get_value("Broker_Str_eq") / BASIS_POINT_FACTOR
BROKER_STRATE_CAP_EQUITIES = rates.get_value("Broker_Str_cap_eq")
BROKER_STRATE_PRIME = rates.get_value("Broker_Str_ps") / BASIS_POINT_FACTOR
BROKER_STRATE_CAP_PRIME = rates.get_value("Broker_Str_cap_ps")
BROKER_STRATE_STRUCTURED = rates.get_value("Broker_Str_st") / BASIS_POINT_FACTOR
BROKER_STRATE_CAP_STRUCTURED = rates.get_value("Broker_Str_cap_st")

CUSTODY_FEE = rates.get_value("Custody_fee") / BASIS_POINT_FACTOR
CUSTODY_FEE_CAP = rates.get_value("Custody_fee_cap")
CUSTODY_FEE_AGENCY = rates.get_value("Custody_fee_ag") / BASIS_POINT_FACTOR
CUSTODY_FEE_CAP_AGENCY = rates.get_value("Custody_fee_cap_ag")
CUSTODY_FEE_EQUITIES = rates.get_value("Custody_fee_eq") / BASIS_POINT_FACTOR
CUSTODY_FEE_CAP_EQUITIES = rates.get_value("Custody_fee_cap_eq")
CUSTODY_FEE_PRIME = rates.get_value("Custody_fee_ps") / BASIS_POINT_FACTOR
CUSTODY_FEE_CAP_PRIME = rates.get_value("Custody_fee_cap_ps")
CUSTODY_FEE_STRUCTURED = rates.get_value("Custody_fee_st") / BASIS_POINT_FACTOR
CUSTODY_FEE_CAP_STRUCTURED = rates.get_value("Custody_fee_cap_st")

RTM_FEE_FACTOR = rates.get_value("RTM_fee") / BASIS_POINT_FACTOR

VAT_RATE = rates.get_value("VAT_rate")
# VAT_FACTOR is based on the vatRate value which is set as 1 + vatfactor
VAT_FACTOR = VAT_RATE - 1.0


def get_value(temp, constant_name, *rest):
    return globals()[constant_name]


def get_vat_for_date(for_date):
    if not VAT_TS:
        raise RuntimeError("No such time series: 'VAT_rate'")
    return PS_TimeSeriesFunctions.GetTimeSeriesPoint(VAT_TS, for_date).TimeValue()

