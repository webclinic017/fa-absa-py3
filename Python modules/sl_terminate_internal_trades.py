"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Terminate No Collateral internal trades
                           This is a once-off onboarding script
                           for lender sweeping
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Danilo Mantoan
DEVELOPER               :  Peter Fabian
CR NUMBER               :  abcdef
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------

"""

import acm
import ael
from sl_lending_prop_stock import _sbl_positions_query, _trd_fee, _trd_price, _is_internal_trd


def _terminate_internal_trades(sbl_portfolio, termination_date):
    """ Terminate internal no collateral trades in
        the specified portfolio for specified date
    """
    # identify lend trades from ACS - Script Lending
    lend_trades = _sbl_positions_query(sbl_portfolio, termination_date)
    sbl_trades = lend_trades.Select()

    header = [ "Trade Number",
               "Portfolio",
               "CP Portfolio",
               "Underlying",
               "B/S",
               "SL Rate",
               "Original Price",
               "Quantity",
               "SL_ExternalInternal",
               "StartDate",
               "EndDate",
               "Borrower",
               "Fund / Lender",
               "Instrument.OpenEnd",
               "Trade Type",
               "Und Type",
               "Status",
               "Trader",
               "Orig End Date",
               "Orig Open End",
               "ScriptAction", ]
    print(",".join(header))

    cal = acm.FCalendar["ZAR Johannesburg"]

    for trd in sbl_trades:
        if _is_internal_trd(trd):
            try:
                i = ael.Instrument[trd.Instrument().Name()].clone()
                leg = i.legs()[0]
                orig_end_date = acm.Time.DateFromYMD(*leg.end_day.to_ymd())
                orig_open_end = i.open_end
                # find next possible end date
                # using acm & calendar here to correctly handle ZAR business days
                if ael.date_from_string(termination_date) > leg.start_day:
                    leg.end_day = ael.date_from_string(termination_date)
                else:
                    start_day = acm.Time.DateFromYMD(*leg.start_day.to_ymd())
                    leg.end_day = ael.date_from_string(cal.AdjustBankingDays(start_day, 1))

                leg.commit()
                ael.poll()

                i.terminate_open_end(leg.end_day)
                i.commit()
            except Exception as e:
                print("Could not terminate trade %s ins %s: %s" \
                    % (trd.Oid(), trd.Instrument().Name(), e))

            else:
                ael.poll()
                acm.PollAllEvents()
                acm.PollDbEvents()

                report_rec = [trd.Oid(),
                              trd.Portfolio().Name(),
                              trd.CounterPortfolio().Name(),
                              trd.Instrument().Underlying().Name(),
                              "Buy" if trd.QuantityInUnderlying() > 0 else "Sell",
                              _trd_fee(trd),
                              _trd_price(trd),
                              trd.QuantityInUnderlying(),
                              trd.Instrument().AdditionalInfo().SL_ExternalInternal(),
                              trd.Instrument().Legs()[0].StartDate(),
                              trd.Instrument().Legs()[0].EndDate(),
                              trd.AdditionalInfo().SL_G1Counterparty1(),
                              trd.AdditionalInfo().SL_G1Counterparty2(),
                              trd.Instrument().OpenEnd(),
                              trd.Type(),
                              trd.Instrument().Underlying().InsType(),
                              trd.Status(),
                              trd.Trader().Name(),
                              orig_end_date,
                              orig_open_end,
                              "Terminate",
                              ]
                print(",".join([str(item) for item in report_rec]))


# Variable Name, Display Name, Type, Candidate Values,
# Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
                 ['sbl_portfolio', "SBL Portfolio", "FPhysicalPortfolio", None,
                  None, 1, 0, "", None, 1],
                 ['date', 'Date', 'string', None, 
                  str(acm.Time.DateToday()), 1, 0, 'Sweeping Date', None, 1],
]


def ael_main(ael_dict):
    date = ael_dict['date']
    if date.upper() == "TODAY":
        date = acm.Time.DateToday()

    sbl_portfolio = ael_dict['sbl_portfolio'].Name()
    _terminate_internal_trades(sbl_portfolio, date)
    print("Done")
